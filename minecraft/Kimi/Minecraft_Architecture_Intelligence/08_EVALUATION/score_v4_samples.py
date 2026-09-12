# -*- coding: utf-8 -*-
"""score_v4_samples — P6 历史样本重评分（项目代号 H · Phase 8 第一部分）。

对 V4 历史 A/B/C 四份 Canonical IR 蓝图按 06_BENCHMARK/scoring_rubric.json 机器评分。

机器可评范围（诚实边界）：
- hard_validity（40）：全部由 08_EVALUATION/validator_runs/ 下的 Validator 原始输出驱动；
- functional_layout（25）：仅 F04（dead_end_ratio>0.20）可机器评；F01/F02/F03/F05/F06
  依赖房间语义（bedroom/kitchen/邻接/公私分区），IR 不可判定 → LLM_ONLY/HUMAN_REVIEW；
- style_compliance（20）：S01/S02（footprint_ratio）、S05（height_ratio）、S06（楼层数）
  对照 04_GRAMMARS/style_rules.json 区间机器评；S03 屋顶形式无机器分类器 → LLM_ONLY；
  S04/S07 需要 brief 屋顶区间/出檐硬性要求，V4 无机器可读 brief → NO_CONSTRAINT；
- material_coherence（10）：M02（材料族占比越出 style grammar [min,max]）与 M03（主导
  材料族是否符合设计文档声明）机器评；M01 无 banned_family 声明 → NO_CONSTRAINT；
- efficiency（5）：E01/E02/E03 全部需要 plot/max_height 机器可读约束，V4 样本没有
  → 整维 NO_CONSTRAINT，不计入总分。

总分口径：total_upper_bound = 四维得分合计（满分 95，efficiency 排除）。未评子项按
0 扣分计入，因此该总分是**上界估计**——人工补齐未评子项后得分只会更低或持平。
HARD FAIL 封顶按 rubric hard_fail_policy 应用于该上界。

用法：
    py -3 08_EVALUATION/score_v4_samples.py \
        --v4-root "D:\\Games\\...\\Architecture-V4" \
        --out-root "<Minecraft_Architecture_Intelligence 根>"

输入全程只读；输出写 08_EVALUATION/evaluation_data.jsonl。
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

RUBRIC_DEDUCT = {  # 来自 scoring_rubric.json hard_validity.items
    "V001": 12, "V002": 8, "V003": 12, "V004": 6, "V005": 6, "V006": 8,
    "V007": 10, "V008": 4, "V009": 6, "V010": 6, "V011": 6, "V012": 3,
}
GRADE_BANDS = [(85, "EXCELLENT"), (70, "GOOD"), (55, "PASSABLE"), (40, "POOR"), (0, "FAIL")]

# 目标 style/function：读自 B-design.md / C-design.md / summary.md（设计文档未使用
# taxonomy 标签，映射为 INFERRED；A 无设计文档，按 summary.md「乡居」取邻近 grammar，
# 标 GENERALIZATION_CASE）。Medieval 作为敏感性对照（B/C 的木框架+白色填充做法亦接近
# Medieval half-timbering）。
SAMPLES = {
    "A": {
        "file": "A-blueprint.json", "run": "A",
        "style_target": "Rustic", "style_basis": "INFERRED/GENERALIZATION_CASE（无设计文档；summary.md「双层乡居」）",
        "function_target": "Residential", "required_floors": 2,
        "required_floors_basis": "summary.md：三栋均含两层可用地板",
        "declared_families": ["stone", "wood"],
        "declared_basis": "summary.md/benchmark.json 主材料：石砖、深色橡木、云杉木、白色陶瓦、红砖",
    },
    "B": {
        "file": "B-blueprint.json", "run": "B",
        "style_target": "Rustic", "style_basis": "INFERRED（B-design.md：坡地木构住宅、悬挑、暖色材料）",
        "function_target": "Residential", "required_floors": 2,
        "required_floors_basis": "B-design.md：主楼两层、厨房翼单层",
        "declared_families": ["stone", "wood"],
        "declared_basis": "B-design.md §5：石材承重、暗橡木结构、方解石填充、深板岩屋顶、砖烟囱",
    },
    "C-before": {
        "file": "C-blueprint-before.json", "run": "C-before",
        "style_target": "Rustic", "style_basis": "INFERRED（C-design.md：乡村住宅、U 形庭院）",
        "function_target": "Residential", "required_floors": 2,
        "required_floors_basis": "C-design.md：两层地板搭接塔内楼梯",
        "declared_families": ["stone", "wood"],
        "declared_basis": "C-design.md Palette：石砖、暗橡木、云杉、方解石、砖烟囱",
    },
    "C-final": {
        "file": "C-blueprint-final.json", "run": "C-final",
        "style_target": "Rustic", "style_basis": "INFERRED（C-design.md：乡村住宅、U 形庭院）",
        "function_target": "Residential", "required_floors": 2,
        "required_floors_basis": "C-critique.md：KEEP 两层楼梯间",
        "declared_families": ["stone", "wood"],
        "declared_basis": "C-design.md Palette：石砖、暗橡木、云杉、方解石、砖烟囱",
    },
}
ALT_STYLE = "Medieval"  # 敏感性对照


def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def family_of(block_id: str, families: dict) -> str:
    """按 palette_dictionary 的 families 顺序做子串匹配（与 P1 提取口径一致）。"""
    for fam, spec in families.items():
        if any(pat in block_id for pat in spec["patterns"]):
            return fam
    return "UNKNOWN"


def style_check(value: float, rule: dict):
    """对照 grammar 区间。返回 (是否超 [min,max], 是否在 IQR 外)。"""
    lo, hi = rule["min"], rule["max"]
    p25, p75 = rule["p25"], rule["p75"]
    return (value < lo or value > hi), (value < p25 or value > p75)


def main() -> None:
    ap = argparse.ArgumentParser(description="V4 历史样本 rubric 机器评分（P6）")
    ap.add_argument("--v4-root", required=True, help="V4 样本目录（只读）")
    ap.add_argument("--out-root", required=True, help="Minecraft_Architecture_Intelligence 根")
    args = ap.parse_args()

    v4 = Path(args.v4_root)
    out = Path(args.out_root)
    sys.path.insert(0, str(out / "scripts"))

    from blueprint_io import load_blueprint, to_voxels  # noqa: E402
    import walkability  # noqa: E402

    style_rules = load_json(out / "04_GRAMMARS" / "style_rules.json")["rules"]
    palette_dict = load_json(out / "02_BLUEPRINT_METADATA" / "palette_dictionary.json")
    families = palette_dict["families"]

    def srule(style: str, dim: str) -> dict:
        for r in style_rules:
            if r["class"] == style and r["dimension"] == dim:
                return r
        raise KeyError(f"{style}.{dim}")

    now = datetime.now(timezone.utc).isoformat()
    lines = []
    for name, cfg in SAMPLES.items():
        ir_path = v4 / cfg["file"]
        run_path = out / "08_EVALUATION" / "validator_runs" / cfg["run"] / "validation_results.jsonl"
        vres = json.loads(run_path.read_text(encoding="utf-8").strip().splitlines()[0])

        ir = load_blueprint(ir_path)
        voxels, _air = to_voxels(ir)
        X, Y, Z = (int(v) for v in ir.dimensions)
        # 非空气体素计数与材料族占比（分母 = 非空气体素，与 palette_dictionary ratio_base 一致）
        air_idx = ir.air_indices
        fam_counts: dict[str, int] = {}
        non_air = 0
        for _x, _y, _z, pi in ir.blocks:
            pi = int(pi)
            if pi in air_idx:
                continue
            non_air += 1
            fam = family_of(ir.block_ids[pi], families)
            fam_counts[fam] = fam_counts.get(fam, 0) + 1
        fam_ratio = {f: round(c / non_air, 4) for f, c in sorted(fam_counts.items())}
        dominant_family = max(fam_counts, key=fam_counts.get) if fam_counts else "UNKNOWN"

        footprint_ratio = round(max(X, Z) / min(X, Z), 4)
        height_ratio = round(Y / max(X, Z), 4)

        walk = walkability.analyze(voxels, ir)
        dead_end_ratio = round(walk["dead_end_count"] / max(walk["walkable_voxels"], 1), 4)

        floors_detected = vres["diagnostics"]["floor_elevations"]
        n_floors = len(floors_detected) if isinstance(floors_detected, list) else None

        items: list[dict] = []

        # ---- hard_validity（40，全机器） ----------------------------------
        triggered = {r["rule_id"]: r for r in vres["rules"] if r["triggered"]}
        hard_ded = 0
        for rid, ded in RUBRIC_DEDUCT.items():
            if rid in triggered:
                sev = triggered[rid]["severity"]
                hard_ded += ded
                items.append({"id": rid, "dimension": "hard_validity", "status": "SCORED",
                              "max_deduct": ded, "deduct_applied": ded,
                              "evidence": {"validator_severity": sev,
                                           "message": triggered[rid]["message"]},
                              "formula": f"触发即扣 {ded}（rubric hard_validity.{rid}）"})
            else:
                app = next(r for r in vres["rules"] if r["rule_id"] == rid)["applicable"]
                items.append({"id": rid, "dimension": "hard_validity", "status": "SCORED",
                              "max_deduct": ded, "deduct_applied": 0,
                              "evidence": {"validator_triggered": False, "applicable": app},
                              "formula": "未触发 → 0 扣分"})
        hard_ded = min(hard_ded, 40)
        hard_score = 40 - hard_ded

        # ---- functional_layout（25：仅 F04 机器可评） ----------------------
        f04_ded = 3 if dead_end_ratio > 0.20 else 0
        items.append({"id": "F04", "dimension": "functional_layout", "status": "SCORED",
                      "max_deduct": 3, "deduct_applied": f04_ded,
                      "evidence": {"dead_end_ratio": dead_end_ratio,
                                   "dead_end_count": walk["dead_end_count"],
                                   "walkable_voxels": walk["walkable_voxels"]},
                      "formula": "dead_end_ratio = dead_end_count/walkable_voxels = "
                                 f"{walk['dead_end_count']}/{walk['walkable_voxels']} = {dead_end_ratio}；"
                                 "> 0.20 → 扣 3"})
        for fid, note in [("F01", "required_zone 缺失判定需房间语义（卧室/厨房等），IR 不可识别"),
                          ("F02", "required_adjacency 需 zone 身份，IR 不可识别"),
                          ("F03", "forbidden_adjacency 需 zone 身份，IR 不可识别"),
                          ("F05", "公私分区 IR 不可直接判定（grammar 仅 INFERRED 弱代理）"),
                          ("F06", "zone 净使用面积需 zone 语义切分，不可机器判定")]:
            items.append({"id": fid, "dimension": "functional_layout",
                          "status": "LLM_ONLY/HUMAN_REVIEW", "max_deduct": None,
                          "deduct_applied": 0, "evidence": {},
                          "formula": f"本报告不评该子项：{note}"})
        func_score = 25 - f04_ded  # 上界：未评子项按 0 扣分

        # ---- style_compliance（20：S01/S02/S05/S06 机器评） ----------------
        st = cfg["style_target"]
        fr_rule = srule(st, "footprint_ratio")
        s01 = s02 = 0
        out_range, out_iqr = style_check(footprint_ratio, fr_rule)
        if out_range:
            s01 = 5
        elif out_iqr:
            s02 = 3
        items.append({"id": "S01", "dimension": "style_compliance", "status": "SCORED",
                      "max_deduct": 5, "deduct_applied": s01,
                      "evidence": {"footprint_ratio": footprint_ratio,
                                   "grammar": f"STYLE.{st}.footprint_ratio",
                                   "min": fr_rule["min"], "max": fr_rule["max"]},
                      "formula": f"max(x,z)/min(x,z) = max({X},{Z})/min({X},{Z}) = {footprint_ratio}；"
                                 f"超出 [{fr_rule['min']},{fr_rule['max']}] → 扣 5"})
        items.append({"id": "S02", "dimension": "style_compliance", "status": "SCORED",
                      "max_deduct": 3, "deduct_applied": s02,
                      "evidence": {"footprint_ratio": footprint_ratio,
                                   "p25": fr_rule["p25"], "p75": fr_rule["p75"]},
                      "formula": f"{footprint_ratio} 在容忍区间内但超出 IQR "
                                 f"[{fr_rule['p25']},{fr_rule['p75']}] → 扣 3"})
        hr_rule = srule(st, "height_ratio")
        s05 = 3 if (height_ratio < hr_rule["min"] or height_ratio > hr_rule["max"]) else 0
        items.append({"id": "S05", "dimension": "style_compliance", "status": "SCORED",
                      "max_deduct": 3, "deduct_applied": s05,
                      "evidence": {"height_ratio": height_ratio,
                                   "grammar": f"STYLE.{st}.height_ratio",
                                   "min": hr_rule["min"], "max": hr_rule["max"]},
                      "formula": f"size_y/max(x,z) = {Y}/max({X},{Z}) = {height_ratio}；"
                                 f"超出 [{hr_rule['min']},{hr_rule['max']}] → 扣 3"})
        s06 = 0
        s06_status = "SCORED"
        if n_floors is None:
            s06_status = "LLM_ONLY/HUMAN_REVIEW"
        elif n_floors != cfg["required_floors"]:
            s06 = 3
        items.append({"id": "S06", "dimension": "style_compliance", "status": s06_status,
                      "max_deduct": 3, "deduct_applied": s06,
                      "evidence": {"floor_elevations": floors_detected,
                                   "detected_floors": n_floors,
                                   "required_floors": cfg["required_floors"],
                                   "required_basis": cfg["required_floors_basis"],
                                   "caveat": "楼板密度启发式（density≥0.30），已知会把密实屋顶/夹层误检为楼板"},
                      "formula": f"检测楼层 {n_floors} vs required {cfg['required_floors']}；不符 → 扣 3"})
        items.append({"id": "S03", "dimension": "style_compliance",
                      "status": "LLM_ONLY/HUMAN_REVIEW", "max_deduct": None, "deduct_applied": 0,
                      "evidence": {},
                      "formula": "本报告不评该子项：屋顶形式（折坡/攒尖/单坡）无机器分类器"})
        items.append({"id": "S04", "dimension": "style_compliance",
                      "status": "NO_CONSTRAINT", "max_deduct": None, "deduct_applied": 0,
                      "evidence": {},
                      "formula": "本报告不评该子项：V4 样本无机器可读 brief.roof 区间"})
        items.append({"id": "S07", "dimension": "style_compliance",
                      "status": "NO_CONSTRAINT", "max_deduct": None, "deduct_applied": 0,
                      "evidence": {"grammar_overhang_frequency": srule(st, "roof_overhang")["frequency"]},
                      "formula": f"本报告不评该子项：{st} 出檐为 OPTIONAL 频率特征，无硬性 overhang_min 要求"})
        style_ded = min(s01 + s02 + s05 + s06, 20)
        style_score = 20 - style_ded

        # 敏感性：同一组几何项对照 ALT_STYLE
        alt_fr = srule(ALT_STYLE, "footprint_ratio")
        alt_hr = srule(ALT_STYLE, "height_ratio")
        alt_out, alt_iqr = style_check(footprint_ratio, alt_fr)
        alt_s01 = 5 if alt_out else 0
        alt_s02 = 3 if (not alt_out and alt_iqr) else 0
        alt_s05 = 3 if (height_ratio < alt_hr["min"] or height_ratio > alt_hr["max"]) else 0
        style_sensitivity = {"alt_style": ALT_STYLE,
                             "S01": alt_s01, "S02": alt_s02, "S05": alt_s05, "S06": s06,
                             "style_score_alt": 20 - min(alt_s01 + alt_s02 + alt_s05 + s06, 20)}

        # ---- material_coherence（10：M02/M03 机器评） ----------------------
        m02 = 0
        m02_detail = {}
        for fam, dim in [("wood", "palette_wood_ratio"), ("stone", "palette_stone_ratio"),
                         ("glass", "palette_glass_ratio"), ("decorative", "palette_decorative_ratio")]:
            gr = srule(st, dim)
            rv = fam_ratio.get(fam, 0.0)
            if rv < gr["min"] or rv > gr["max"]:
                m02 += 2
                m02_detail[fam] = {"ratio": rv, "min": gr["min"], "max": gr["max"], "out": True}
            else:
                m02_detail[fam] = {"ratio": rv, "min": gr["min"], "max": gr["max"], "out": False}
        m02 = min(m02, 6)
        items.append({"id": "M02", "dimension": "material_coherence", "status": "SCORED",
                      "max_deduct": 6, "deduct_applied": m02,
                      "evidence": {"family_ratios": fam_ratio, "checks": m02_detail,
                                   "grammar_style": st, "ratio_base": "non_air_blocks"},
                      "formula": "族占比 = 族体素数/非空气体素数；每族超出 grammar [min,max] 扣 2，上限 6"})
        m03 = 0 if dominant_family in cfg["declared_families"] else 2
        items.append({"id": "M03", "dimension": "material_coherence", "status": "SCORED",
                      "max_deduct": 2, "deduct_applied": m03,
                      "evidence": {"dominant_family": dominant_family,
                                   "declared_families": cfg["declared_families"],
                                   "declared_basis": cfg["declared_basis"]},
                      "formula": f"主导族 {dominant_family} ∈ 声明 {cfg['declared_families']}？否则扣 2"})
        items.append({"id": "M01", "dimension": "material_coherence",
                      "status": "NO_CONSTRAINT", "max_deduct": None, "deduct_applied": 0,
                      "evidence": {},
                      "formula": "本报告不评该子项：V4 设计文档未声明 banned_family"})
        mat_ded = min(m02 + m03, 10)
        mat_score = 10 - mat_ded

        # ---- efficiency（5：整维 NO_CONSTRAINT） ---------------------------
        for eid in ("E01", "E02", "E03"):
            items.append({"id": eid, "dimension": "efficiency",
                          "status": "NO_CONSTRAINT", "max_deduct": None, "deduct_applied": 0,
                          "evidence": {},
                          "formula": "本报告不评该子项：V4 样本无机器可读 plot/max_height 约束"})

        # ---- 合计与封顶 ----------------------------------------------------
        total_upper = hard_score + func_score + style_score + mat_score  # 满分 95（efficiency 排除）
        hf = vres["hard_fail_count"]
        cap = 10 if hf >= 5 else 25 if hf >= 3 else 40 if hf >= 1 else 95
        total_capped = min(total_upper, cap)
        norm = round(total_capped / 95 * 100, 1)
        grade = next(label for lo, label in GRADE_BANDS if norm >= lo)

        excluded = [i["id"] for i in items if i["status"] != "SCORED"]
        lines.append({
            "sample": name,
            "evaluated_at": now,
            "source_file": str(ir_path),
            "validator_run": str(run_path),
            "validator": {k: vres[k] for k in
                          ("validation_status", "hard_fail_count", "warning_count",
                           "info_count", "rules_triggered", "walkability_score",
                           "connectivity_score", "vertical_circulation_score",
                           "validator_confidence")},
            "targets": {"style": st, "style_basis": cfg["style_basis"],
                        "function": cfg["function_target"],
                        "required_floors": cfg["required_floors"],
                        "required_floors_basis": cfg["required_floors_basis"]},
            "features": {"dimensions": {"x": X, "y": Y, "z": Z},
                         "non_air_blocks": non_air,
                         "footprint_ratio": footprint_ratio,
                         "height_ratio": height_ratio,
                         "floors_detected": floors_detected,
                         "dead_end_ratio": dead_end_ratio,
                         "family_ratios": fam_ratio,
                         "dominant_family": dominant_family},
            "scores": {"hard_validity": {"weight": 40, "deducted": hard_ded, "score": hard_score},
                       "functional_layout": {"weight": 25, "deducted": f04_ded, "score": func_score,
                                             "note": "仅 F04 机器可评，其余子项未评（按 0 扣分计，上界）"},
                       "style_compliance": {"weight": 20, "deducted": style_ded, "score": style_score,
                                            "note": "S01/S02/S05/S06 机器评；S03/S04/S07 未评"},
                       "material_coherence": {"weight": 10, "deducted": mat_ded, "score": mat_score,
                                              "note": "M02/M03 机器评；M01 未评"},
                       "efficiency": {"weight": 5, "score": None,
                                      "note": "整维 NO_CONSTRAINT，不计入总分"}},
            "style_sensitivity": style_sensitivity,
            "total_upper_bound_max95": total_upper,
            "hard_fail_count": hf,
            "hard_fail_cap": cap,
            "total_capped_max95": total_capped,
            "total_capped_normalized_100": norm,
            "grade": grade,
            "excluded_items": excluded,
            "total_formula": "total = (40−hard_ded)+(25−F04)+(20−style_ded)+(10−mat_ded)，"
                             "efficiency 未评不计入（满分 95）； capped = min(total, cap(hard_fail_count))；"
                             "未评子项按 0 扣分 → 上界估计",
            "items": items,
        })

    # ---- C 路线 revision 差异独立复算（与 evidence/C-revision-diff.json 交叉核对） ----
    ir_b = load_blueprint(v4 / "C-blueprint-before.json")
    ir_f = load_blueprint(v4 / "C-blueprint-final.json")
    map_b = {(int(x), int(y), int(z)): ir_b.palette[int(pi)] for x, y, z, pi in ir_b.blocks}
    map_f = {(int(x), int(y), int(z)): ir_f.palette[int(pi)] for x, y, z, pi in ir_f.blocks}
    added = removed = changed = 0
    removed_states: dict[str, int] = {}
    diff_positions = []
    for pos in set(map_b) | set(map_f):
        b, f = map_b.get(pos), map_f.get(pos)
        if b == f:
            continue
        diff_positions.append(pos)
        if b is None:
            added += 1
        elif f is None:
            removed += 1
            removed_states[b] = removed_states.get(b, 0) + 1
        else:
            changed += 1
    ev = load_json(v4 / "evidence" / "C-revision-diff.json")
    # 入口区域（V002 证据 pos (19,3,13) 及其接近格）与楼梯拆除分析
    entrance_zone = [p for p in diff_positions if 16 <= p[0] <= 23 and 2 <= p[1] <= 8 and 8 <= p[2] <= 18]
    stairs_removed = {k: v for k, v in removed_states.items() if "stairs" in k}
    stair_removed_ys = sorted({p[1] for p in diff_positions
                               if map_b.get(p, "") and "stairs" in map_b.get(p, "") and p not in map_f})
    revision = {
        "recomputed": {"total": len(diff_positions), "added": added,
                       "removed": removed, "changed": changed},
        "evidence_file": {"total": ev["total"], "summary": ev["summary"]},
        "cross_check_match": (len(diff_positions) == ev["total"] and added == ev["summary"]["added"]
                              and removed == ev["summary"]["removed"] and changed == ev["summary"]["changed"]),
        "note": "两 IR 坐标系均为蓝图局部坐标、包络最小角归零，可直接按坐标对齐比较；"
                "removed = final 不再占用该坐标（初稿从未施工）",
        "entrance_zone_diff_count": len(entrance_zone),
        "entrance_zone_definition": "x∈[16,23], y∈[2,8], z∈[8,18]（V002 证据入口 (19,3,13) 周边）",
        "stairs_removed_by_state": stairs_removed,
        "stairs_removed_y_levels": stair_removed_ys,
    }

    out_jsonl = out / "08_EVALUATION" / "evaluation_data.jsonl"
    with out_jsonl.open("w", encoding="utf-8") as f:
        for rec in lines:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        f.write(json.dumps({"sample": "_meta", "evaluated_at": now,
                            "scoring_script": str(Path(__file__).resolve()),
                            "c_revision_crosscheck": revision}, ensure_ascii=False) + "\n")

    # 控制台摘要
    for rec in lines:
        print(json.dumps({"sample": rec["sample"],
                          "hard_fail": rec["hard_fail_count"],
                          "warn": rec["validator"]["warning_count"],
                          "hard": rec["scores"]["hard_validity"]["score"],
                          "func": rec["scores"]["functional_layout"]["score"],
                          "style": rec["scores"]["style_compliance"]["score"],
                          "mat": rec["scores"]["material_coherence"]["score"],
                          "total95": rec["total_upper_bound_max95"],
                          "cap": rec["hard_fail_cap"],
                          "capped95": rec["total_capped_max95"],
                          "norm100": rec["total_capped_normalized_100"],
                          "grade": rec["grade"]}, ensure_ascii=False))
    print(json.dumps({"revision_crosscheck": revision["cross_check_match"],
                      "recomputed": revision["recomputed"]}, ensure_ascii=False))
    print(f"written: {out_jsonl}")


if __name__ == "__main__":
    main()
