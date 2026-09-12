# -*- coding: utf-8 -*-
"""run_benchmark — B vs C 离线对比实验管线（项目代号 H · P6 第二部分）。

对每条选定的 design brief：

- **路线 B**（规则约束单轮）：generate_blueprint 生成 → Validator → rubric 评分。
  单轮忠实结果，不返修。
- **路线 C**（REVISION_PROTOCOL 程序化实现）：同一生成器出初稿（与 B 逐方块一致）
  → Validator → 有 HARD_FAIL/可修 WARNING 则 revise_blueprint 修订 → Validator
  Recheck（真实重跑）→ 无客观错误后进程序化 Critic（rubric 机器子项 + CR-SC-01
  类材料检查）→ 可修项再修订 → 收敛/上限 3 轮止。每轮蓝图 + Validator 输出 +
  diff（含 SHA256）写入 generated/_traces/<brief_id>/。

锚点纪律：footprint / 风格 / 分区清单在修订中不变（revise_blueprint.anchor_check
逐轮验证）；diff > 30% 触发回退检查（协议 §3.2）。

产出：
- 08_EVALUATION/generated/B/<brief_id>.json 与 generated/C/<brief_id>.json
- 08_EVALUATION/generated/_traces/<brief_id>/round*.json|validation|diff
- 08_EVALUATION/evaluation_data.jsonl 追加 24 条记录（与 V4 记录同构）
- 08_EVALUATION/p6b_summary.json（汇总表数据，供报告复算）

用法：
    py -3 scripts/run_benchmark.py --out-root <Minecraft_Architecture_Intelligence>
环境：py -3 + 只读 site-packages（见 scripts/README.md）。零写入 D:\\Games。
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# 选定 brief（dev 集内；4 Easy / 5 Medium / 3 Hard；覆盖 6 功能域；
# targets_gap=true × 3：BRIEF-0043/0053/0065）
# ---------------------------------------------------------------------------
SELECTED = [
    "BRIEF-0006",  # Easy   Residential  Medieval
    "BRIEF-0037",  # Easy   Workshop     Rustic
    "BRIEF-0053",  # Easy   Hospitality  Rustic  (gap)
    "BRIEF-0091",  # Easy   Constrained  Medieval
    "BRIEF-0017",  # Medium Residential Rustic
    "BRIEF-0030",  # Medium Mixed-use    Chinese
    "BRIEF-0056",  # Medium Hospitality  Japanese
    "BRIEF-0065",  # Medium Civic        Rustic  (gap)
    "BRIEF-0096",  # Medium Constrained  Medieval
    "BRIEF-0043",  # Hard   Workshop     Rustic  (gap)
    "BRIEF-0068",  # Hard   Civic        Rustic
    "BRIEF-0099",  # Hard   Constrained  Japanese
]

# Validator 触发后可程序化修复的规则（V012=INFO 不修，V009 视障碍性质而定）
FIXABLE_VALIDATOR = {"V002", "V003", "V004", "V005", "V006", "V007", "V008",
                     "V010", "V011"}


def load_briefs(path: Path) -> dict[str, dict]:
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            b = json.loads(line)
            out[b["brief_id"]] = b
    return out


def make_validator(out_root: Path):
    """导入 P2 Validator 源码构建校验函数（与 CLI 同一代码路径，另留 ctx 供评分）。"""
    sys.path.insert(0, str(out_root / "05_SPATIAL_VALIDATOR" / "validator_source"))
    from spatial_context import SpatialContext          # noqa: E402
    from rules import RULES                               # noqa: E402
    from core import load_rules_config                    # noqa: E402
    from rules import _main_interior_component             # noqa: E402
    cfg = load_rules_config(out_root / "05_SPATIAL_VALIDATOR" / "validator_rules.json")

    def validate_with_ctx(path):
        """core.validate_one 的等价实现，额外返回 SpatialContext（评分复用）。"""
        ctx = SpatialContext(path, floor_params=cfg.get("floor_detection"))
        results = []
        for rid in sorted(RULES):
            rcfg = cfg.get(rid, {})
            if not rcfg.get("enabled", True):
                continue
            params = dict(rcfg.get("params", {}))
            params["severity"] = rcfg.get("severity", "WARNING")
            results.append(RULES[rid](ctx, params))
        triggered = [r for r in results if r.triggered]
        hard = [r for r in triggered if r.severity == "HARD_FAIL"]
        warn = [r for r in triggered if r.severity == "WARNING"]
        info = [r for r in triggered if r.severity == "INFO"]
        status = "HARD_FAIL" if hard else ("WARNING" if warn else "PASS")
        potential = max(ctx.potential_stance_voxels, 1)
        walkability_score = round(100.0 * ctx.walkable_voxels / potential, 1)
        if ctx.interior_stance_count > 0 and ctx.interior_comp_counts:
            main_comp = _main_interior_component(ctx)
            connectivity_score = round(100.0 * ctx.interior_comp_counts.get(main_comp, 0)
                                       / ctx.interior_stance_count, 1)
        elif ctx.walkable_voxels > 0:
            connectivity_score = round(100.0 * ctx.walk["largest_component_ratio"], 1)
        else:
            connectivity_score = "UNKNOWN"
        # vertical（与 core._vertical_score 同口径）
        floors = ctx.floor_stance_sets(level_tol=cfg.get("V007", {}).get("params", {})
                                       .get("level_tol", 0.6))
        if not ctx.floor_elevations:
            vertical = "UNKNOWN"
        elif ctx.interior_stance_count == 0:
            vertical = "UNKNOWN"
        else:
            min_st = cfg.get("V007", {}).get("params", {}).get("min_floor_stances", 6)
            usable = [fs for fs in floors if len(fs["interior"]) >= min_st]
            if len(usable) <= 1:
                vertical = 100.0
            else:
                base = {ctx.component_of_flat(fi) for fi in usable[0]["interior"]}
                conn = sum(1 for fs in usable
                           if {ctx.component_of_flat(fi) for fi in fs["interior"]} & base)
                vertical = round(100.0 * conn / len(usable), 1)
        unk = ctx.walk["unknown_block_type_count"]
        vres = {
            "ref_id": ctx.ir.ref_id or Path(path).stem,
            "ir_source": ctx.ir.ir_source,
            "path": str(path),
            "validation_status": status,
            "hard_fail_count": len(hard),
            "warning_count": len(warn),
            "info_count": len(info),
            "rules_triggered": [r.rule_id for r in triggered],
            "walkability_score": walkability_score,
            "connectivity_score": connectivity_score,
            "vertical_circulation_score": vertical,
            "validator_confidence": "high" if unk == 0 else ("medium" if unk <= 3 else "low"),
            "diagnostics": {
                "walkable_voxels": ctx.walkable_voxels,
                "potential_stance_voxels": ctx.potential_stance_voxels,
                "interior_air_voxels": ctx.interior_air_count,
                "interior_stances": ctx.interior_stance_count,
                "walkable_components": ctx.walk["walkable_components"],
                "floor_elevations": ctx.floor_elevations or "UNKNOWN",
                "door_count": len(ctx.doors),
                "stair_clusters": len(ctx.stair_clusters),
                "unknown_block_types": ctx.walk["unknown_block_types"],
            },
            "rules": [r.to_dict() for r in results],
        }
        return vres, ctx

    return validate_with_ctx


def main() -> None:
    ap = argparse.ArgumentParser(description="B vs C 离线对比实验（P6b）")
    ap.add_argument("--out-root", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--only", default=None, help="只跑某条 brief（调试用）")
    args = ap.parse_args()
    out_root = Path(args.out_root)
    sys.path.insert(0, str(out_root / "scripts"))

    import generate_blueprint as gen                          # noqa: E402
    import revise_blueprint as rev                             # noqa: E402
    import score_generated as sg                               # noqa: E402

    res = gen.load_resources(out_root)
    briefs = load_briefs(out_root / "06_BENCHMARK" / "design_briefs.jsonl")
    validate = make_validator(out_root)
    now = datetime.now(timezone.utc).isoformat()

    gen_dir = out_root / "08_EVALUATION" / "generated"
    trc_root = gen_dir / "_traces"
    records: list[dict] = []
    summary_rows: list[dict] = []

    for bid in SELECTED:
        if args.only and bid != args.only:
            continue
        brief = briefs[bid]
        trc = trc_root / bid
        trc.mkdir(parents=True, exist_ok=True)

        # ============ 路线 B：规则约束单轮 ============
        ir_b, plan_b = gen.generate(brief, res, note="route B: rule-driven single pass")
        path_b = gen_dir / "B" / f"{bid}.json"
        gen.write_ir(ir_b, path_b)
        vres_b, ctx_b = validate(path_b)
        rec_b = sg.score_generated(brief, path_b, vres_b, ctx_b, res, "B", now)
        rec_b.update({
            "sample": f"{bid}|B", "pipeline": "B", "brief_id": bid,
            "difficulty": brief["difficulty"],
            "function_domain": brief["function_domain"], "style": brief["style"],
            "targets_gap": bool(brief.get("targets_gap", False)),
            "source_file": str(path_b),
            "validator_run": "inline:run_benchmark.py（core.validate_one 同代码路径）",
            "validator": {k: vres_b[k] for k in
                          ("validation_status", "hard_fail_count", "warning_count",
                           "info_count", "rules_triggered", "walkability_score",
                           "connectivity_score", "vertical_circulation_score",
                           "validator_confidence")},
            "targets": {"style": brief["style"],
                        "style_basis": "brief（设计任务书字段，机器可读）",
                        "function": brief["function_domain"],
                        "required_floors": brief["required_floors"],
                        "required_floors_basis": "brief.required_floors"},
        })
        records.append(rec_b)

        # ============ 路线 C：Validator→Revision→Recheck 循环 ============
        # 初稿与 B 完全一致（同一生成器同一参数，确定性）
        cur_ir = ir_b
        path_c = gen_dir / "C" / f"{bid}.json"
        revision_rounds = []
        overrides: dict = {}
        keep_notes: list[dict] = []
        critic_log: list[dict] = []
        prev_ir = None
        rollback = False
        for rnd in range(3):
            p = trc / f"round{rnd}_blueprint.json"
            gen.write_ir(cur_ir, p)
            vres, ctx = validate(p)
            (trc / f"round{rnd}_validation.json").write_text(
                json.dumps(vres, ensure_ascii=False, indent=1), encoding="utf-8")
            triggered = set(vres["rules_triggered"])
            hard = vres["hard_fail_count"] > 0
            fixable = triggered & FIXABLE_VALIDATOR
            # --- Critic 阶段：无客观错误才评审（协议 §2.4 先治病再选美） ---
            critic_changes = []
            if not hard and not fixable:
                rec_now = sg.score_generated(brief, p, vres, ctx, res, "C", now)
                for it in rec_now["items"]:
                    if it["deduct_applied"] and it["id"] == "M02":
                        critic_changes.append({"item": "M02", "action": "palette_refit"})
                    elif it["deduct_applied"] and it["id"] == "F02":
                        critic_changes.append({"item": "F02", "action": "open_doorway"})
                    elif it["deduct_applied"] and it["id"] in ("S02", "S05", "S06",
                                                               "S03", "S04", "F04"):
                        keep_notes.append({"item": it["id"],
                                           "reason": "锚点锁定（footprint/层高/屋顶体量）"
                                                     "或参考生成器天花板，协议允许 KEEP"})
                critic_log.append({"round": rnd,
                                   "deducted_items": [i["id"] for i in rec_now["items"]
                                                      if i["deduct_applied"]],
                                   "changes": critic_changes})
                if not critic_changes:
                    break                               # 收敛：无 important 可修项
                if "M02" in [c["item"] for c in critic_changes]:
                    # 材料微调：按当前实测占比推旋钮方向
                    ratios = rec_now["features"]["family_ratios"]
                    cur_pp = cur_ir["metadata"]["generation"].get("palette_params", {})
                    adj = dict(overrides.get("palette_params", {}))
                    for f, (lo, hi) in brief["palette_constraints"]["family_ratio_ranges"].items():
                        rv = ratios.get(f, 0.0)
                        if rv > hi and f == "stone":
                            adj["floor_stone_fraction"] = max(0.0,
                                cur_pp.get("floor_stone_fraction", 0.5) - 0.07)
                        elif rv > hi and f == "wood":
                            adj["wall_wood_fraction"] = max(0.0,
                                cur_pp.get("wall_wood_fraction", 0.3) - 0.05)
                        elif rv < lo and f == "wood":
                            adj["wall_wood_fraction"] = min(0.9,
                                cur_pp.get("wall_wood_fraction", 0.3) + 0.05)
                    overrides["palette_params"] = adj

            # --- Revision 阶段 ---
            prev_ir = cur_ir
            # 阳台门移位（regen 类修复：撞楼梯洞口的门沿墙平移）
            # 只在"本轮仍触发 V002/V003 且移位量新计算"时产生 regen，
            # 避免收敛后拿旧 overrides 空转重生成（diff=0 的无效轮）。
            plan_meta = cur_ir["metadata"]["generation"]
            new_override = False
            if ("V002" in triggered or "V003" in triggered):
                shift = rev.plan_balcony_door_shift(plan_meta)
                if shift is not None and overrides.get("balcony_door_shift") != shift:
                    overrides["balcony_door_shift"] = shift
                    new_override = True
            if new_override or "M02" in [c["item"] for c in critic_changes]:
                cur_ir, cur_plan = gen.generate(brief, res, overrides,
                                                note=f"C-route regen round {rnd + 1}")
                acts = [f"regen overrides={json.dumps(overrides, ensure_ascii=False)}"]
            else:
                new_ir, acts = rev.apply_patch_revision(cur_ir, vres, plan_meta)
                if acts:
                    cur_ir = new_ir
                    cur_plan = plan_meta
            if not acts:
                keep_notes.append({"item": "revision",
                                   "reason": "触发项无可程序化修复动作，转人工"})
                break
            diff = rev.diff_irs(prev_ir, cur_ir)
            anchors = rev.anchor_check(prev_ir, cur_ir)
            (trc / f"round{rnd + 1}_diff.json").write_text(json.dumps(
                {"round": rnd + 1, "actions": acts, "diff": diff,
                 "anchors": anchors,
                 "overrides": overrides}, ensure_ascii=False, indent=1), encoding="utf-8")
            prev_non_air = max(diff["prev_non_air"], 1)
            ratio = diff["total"] / prev_non_air
            revision_rounds.append({"round": rnd + 1, "actions": acts,
                                    "diff_total": diff["total"],
                                    "diff_ratio": round(ratio, 4),
                                    "diff_sha256": diff["sha256"],
                                    "anchors": anchors})
            if ratio > 0.30:
                # 协议 §3.2 回退检查：超阈 → 回退上一版，终止迭代转人工
                rollback = True
                cur_ir = prev_ir
                revision_rounds[-1]["rollback"] = True
                keep_notes.append({"item": "diff_threshold",
                                   "reason": f"diff_ratio {ratio:.2%} > 30%，回退并转人工"})
                break
            if diff["total"] == 0:
                # 协议 §3.3 收敛：本轮修订无实质变更，剩余意见全部 KEEP → 停
                revision_rounds[-1]["converged_noop"] = True
                revision_rounds.pop()             # 无变更不计入修订轮数/代价
                break

        # 终稿：写 C 蓝图 + 最终 Validator Recheck（真实重跑）
        gen.write_ir(cur_ir, path_c)
        vres_c, ctx_c = validate(path_c)
        (trc / "final_validation.json").write_text(
            json.dumps(vres_c, ensure_ascii=False, indent=1), encoding="utf-8")
        rec_c = sg.score_generated(brief, path_c, vres_c, ctx_c, res, "C", now)
        rec_c.update({
            "sample": f"{bid}|C", "pipeline": "C", "brief_id": bid,
            "difficulty": brief["difficulty"],
            "function_domain": brief["function_domain"], "style": brief["style"],
            "targets_gap": bool(brief.get("targets_gap", False)),
            "source_file": str(path_c),
            "validator_run": "inline:run_benchmark.py（core.validate_one 同代码路径）",
            "validator": {k: vres_c[k] for k in
                          ("validation_status", "hard_fail_count", "warning_count",
                           "info_count", "rules_triggered", "walkability_score",
                           "connectivity_score", "vertical_circulation_score",
                           "validator_confidence")},
            "targets": {"style": brief["style"],
                        "style_basis": "brief（设计任务书字段，机器可读）",
                        "function": brief["function_domain"],
                        "required_floors": brief["required_floors"],
                        "required_floors_basis": "brief.required_floors"},
            "revision": {
                "rounds": len(revision_rounds),
                "total_changed_cells": sum(r["diff_total"] for r in revision_rounds),
                "per_round": revision_rounds,
                "rollback": rollback,
                "critic_log": critic_log,
                "keep_notes": keep_notes,
                "overrides_final": overrides,
                "initial_hard_fail": vres_b["hard_fail_count"],
                "final_hard_fail": vres_c["hard_fail_count"],
                "fixed": vres_b["hard_fail_count"] > 0 and vres_c["hard_fail_count"] == 0,
            },
        })
        records.append(rec_c)

        summary_rows.append({
            "brief_id": bid, "difficulty": brief["difficulty"],
            "function_domain": brief["function_domain"], "style": brief["style"],
            "targets_gap": bool(brief.get("targets_gap", False)),
            "B": {"hard_fail": vres_b["hard_fail_count"], "warn": vres_b["warning_count"],
                  "validator_score": rec_b["scores"]["hard_validity"]["score"],
                  "functional_score": rec_b["scores"]["functional_layout"]["score"],
                  "style_score": rec_b["scores"]["style_compliance"]["score"],
                  "material_score": rec_b["scores"]["material_coherence"]["score"],
                  "efficiency_score": rec_b["scores"]["efficiency"]["score"],
                  "total": rec_b["total_capped_max100"], "grade": rec_b["grade"]},
            "C": {"hard_fail": vres_c["hard_fail_count"], "warn": vres_c["warning_count"],
                  "validator_score": rec_c["scores"]["hard_validity"]["score"],
                  "functional_score": rec_c["scores"]["functional_layout"]["score"],
                  "style_score": rec_c["scores"]["style_compliance"]["score"],
                  "material_score": rec_c["scores"]["material_coherence"]["score"],
                  "efficiency_score": rec_c["scores"]["efficiency"]["score"],
                  "total": rec_c["total_capped_max100"], "grade": rec_c["grade"]},
            "revision_cost": {"rounds": len(revision_rounds),
                              "changed_cells": sum(r["diff_total"]
                                                   for r in revision_rounds)},
            "fixed_by_C": rec_c.get("revision", {}).get("fixed", False),
        })
        print(json.dumps({"brief": bid,
                          "B": summary_rows[-1]["B"], "C": summary_rows[-1]["C"],
                          "revision_cost": summary_rows[-1]["revision_cost"]},
                         ensure_ascii=False))

    # ---- 追加 evaluation_data.jsonl -----------------------------------------
    out_jsonl = out_root / "08_EVALUATION" / "evaluation_data.jsonl"
    with out_jsonl.open("a", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        f.write(json.dumps({
            "sample": "_meta_p6b", "evaluated_at": now,
            "experiment": "B vs C offline run（programmatic reference generator, rule-driven）",
            "generator": "scripts/generate_blueprint.py — NOT an LLM",
            "scripts": {"generator": "scripts/generate_blueprint.py",
                        "reviser": "scripts/revise_blueprint.py",
                        "scorer": "scripts/score_generated.py",
                        "pipeline": "scripts/run_benchmark.py"},
            "selected_briefs": SELECTED,
            "scoring_scope": "五维全机器评（F05 维持 LLM_ONLY）；满分 100；"
                             "封顶策略同 rubric hard_fail_policy",
        }, ensure_ascii=False) + "\n")

    # ---- 汇总 JSON（报告复算用） ---------------------------------------------
    def mean(xs):
        xs = list(xs)
        return round(sum(xs) / len(xs), 2) if xs else None

    summ = {
        "generated_at": now,
        "selected_briefs": SELECTED,
        "n_briefs": len(summary_rows),
        "rows": summary_rows,
        "aggregate": {
            "B": {"hard_fail_rate": round(sum(1 for r in summary_rows
                                            if r["B"]["hard_fail"] > 0) / len(summary_rows), 4),
                  "validator_score": mean(r["B"]["validator_score"] for r in summary_rows),
                  "functional_score": mean(r["B"]["functional_score"] for r in summary_rows),
                  "style_score": mean(r["B"]["style_score"] for r in summary_rows),
                  "material_score": mean(r["B"]["material_score"] for r in summary_rows),
                  "efficiency_score": mean(r["B"]["efficiency_score"] for r in summary_rows),
                  "total": mean(r["B"]["total"] for r in summary_rows)},
            "C": {"hard_fail_rate": round(sum(1 for r in summary_rows
                                            if r["C"]["hard_fail"] > 0) / len(summary_rows), 4),
                  "validator_score": mean(r["C"]["validator_score"] for r in summary_rows),
                  "functional_score": mean(r["C"]["functional_score"] for r in summary_rows),
                  "style_score": mean(r["C"]["style_score"] for r in summary_rows),
                  "material_score": mean(r["C"]["material_score"] for r in summary_rows),
                  "efficiency_score": mean(r["C"]["efficiency_score"] for r in summary_rows),
                  "total": mean(r["C"]["total"] for r in summary_rows),
                  "revision_rounds": mean(r["revision_cost"]["rounds"] for r in summary_rows),
                  "revision_cells": mean(r["revision_cost"]["changed_cells"]
                                         for r in summary_rows)},
            "c_fix_success": {
                "initial_hard_fail_n": sum(1 for r in summary_rows if r["B"]["hard_fail"] > 0),
                "fixed_n": sum(1 for r in summary_rows if r["fixed_by_C"]),
            },
        },
    }
    (out_root / "08_EVALUATION" / "p6b_summary.json").write_text(
        json.dumps(summ, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"written": str(out_jsonl), "records_appended": len(records),
                      "summary": "08_EVALUATION/p6b_summary.json",
                      "aggregate": summ["aggregate"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
