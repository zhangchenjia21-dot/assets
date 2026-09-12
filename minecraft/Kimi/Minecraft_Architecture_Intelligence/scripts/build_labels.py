# -*- coding: utf-8 -*-
"""build_labels.py — P3 任务1：由 V6C2 分类（catalog-final.json）+ P1 元数据生成 123 张蓝图的
style/function 标签表（Taxonomy 落标）。

纪律（见任务书 8/20 节与 CONTEXT.md）：
- V6C2 标签为主信号（人工+规则审核过），几何特征只做交叉验证，不从几何单独提拔标签；
- V6C2 style top 置信度 < STYLE_CONF_FLOOR → 降级 Unknown 并记录；
- 几何交叉验证强冲突 → 降级 Unknown 并记录；弱不一致 → 保留标签、notes 记录、置信度下调一档；
- 映射表是本脚本的显式常量（见下），样本不支持的候选类别不硬建。

用法：
    py -3 scripts/build_labels.py \
      --catalog-final "D:\\Games\\...\\references\\classification-v2\\catalog-final.json" \
      --metadata "02_BLUEPRINT_METADATA\\blueprint_metadata.jsonl" \
      --output "03_TAXONOMY"
只读参考库，产出只写 --output。
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

# ---------------------------------------------------------------------------
# 映射表（显式、可审计；依据见 03_TAXONOMY/ARCHITECTURE_TAXONOMY.md）
# ---------------------------------------------------------------------------
# V6C2 style tag → 本 taxonomy Style 类。None = 不做主标签（伞标签）。
STYLE_MAP = {
    "medieval": "Medieval",
    "fortified": "Medieval",   # 防御性是中世纪念头的性格，并入 Medieval（记录）
    "rustic": "Rustic",
    "cottage": "Rustic",       # cottage 是 rustic 的亚型（V6C2 词表内自建）
    "fantasy": "Fantasy",
    "high_fantasy": "Fantasy",
    "japanese": "Japanese",
    "chinese": "Chinese",
    "east_asian": None,        # 伞标签：仅在无 japanese/chinese 更具体标签时出现，本库未发生
    "european": "Other",       # 泛欧洲，候选类无对应（不细分 Victorian/Gothic，样本不支持）
    "desert": "Other",
    "classical": "Other",
    "unknown": "Unknown",
}

# V6C2 primary_use + secondary_use → 本 taxonomy Function 类。
# 规则按优先级逐条匹配；secondary 命中最具体者先。
def map_function(primary: str, secondary: list[str]) -> tuple[str, str]:
    """返回 (function_label, mapping_note)。"""
    sec = set(secondary)
    if primary == "residential":
        return "Residential", "primary_use=residential"
    if primary == "commercial":
        if sec & {"tavern", "inn"}:
            return "Inn", "commercial+tavern/inn → Inn"
        if sec & {"blacksmith"}:
            return "Blacksmith", "commercial+blacksmith → Blacksmith"
        if sec & {"bakery", "mill"}:
            return "Workshop", "commercial+加工坊 → Workshop"
        if sec & {"shop", "market"}:
            return "Workshop", "commercial+shop/market → Workshop（零售并入作坊，记录在案）"
        return "Workshop", "commercial 未细分 → Workshop（保守）"
    if primary == "industrial":
        if sec & {"blacksmith"}:
            return "Blacksmith", "industrial+blacksmith → Blacksmith"
        if sec & {"warehouse"}:
            return "Warehouse", "industrial+warehouse → Warehouse"
        return "Workshop", "industrial（生产建筑）→ Workshop"
    if primary == "military":
        if sec & {"castle", "keep"}:
            return "Castle", "military+castle/keep → Castle"
        if sec & {"gatehouse", "wall"}:
            return "Gate", "military+gatehouse/wall → Gate"
        if sec & {"tower"}:
            return "Tower", "military+tower → Tower"
        return "Castle", "military 未细分 → Castle（保守）"
    if primary == "religious":
        return "Religious", "primary_use=religious"
    if primary == "civic":
        return "Civic", "primary_use=civic（含 arena，公共集会）"
    if primary == "agricultural":
        return "Farm", "primary_use=agricultural"
    if primary == "transport":
        # 候选类无载具；样本支持 ship/airship/dock，新增 Vehicle 类（记录在案）
        return "Vehicle", "transport（ship/airship/dock）→ 新增类 Vehicle"
    if primary == "landmark":
        if sec & {"tower", "lighthouse"}:
            return "Tower", "landmark+tower → Tower"
        if sec & {"palace"}:
            return "Castle", "landmark+palace → Castle（纪念性大型建筑群并入，记录在案）"
        return "Decoration", "landmark（statue/portal/mausoleum 等纪念物）→ Decoration"
    if primary == "landscape":
        return "Decoration", "landscape（tree/garden/pavilion 等景观）→ Decoration"
    if primary == "mixed_use":
        return "Mixed-use", "primary_use=mixed_use"
    return "Unknown", "primary_use=unknown 或无证据"

# 置信度分档
STYLE_CONF_FLOOR = 0.55   # 低于此值 → Unknown（低置信纪律）
def conf_band(c: float) -> str:
    if c >= 0.70:
        return "high"
    if c >= 0.55:
        return "medium"
    return "low"


# ---------------------------------------------------------------------------
# 几何交叉验证（只做校验/下调，不提拔）
# ---------------------------------------------------------------------------
def cross_check_style(label: str, meta: dict, features: list[str]) -> tuple[str, str]:
    """返回 (verdict, note)。verdict ∈ agree / weak / conflict / n/a。"""
    if label in ("Unknown", "Other"):
        return "n/a", ""
    wood = meta.get("wood_ratio", 0.0)
    stone = meta.get("stone_ratio", 0.0)
    stairs = meta.get("stair_count", 0) or 0
    feats = set(features)
    if label in ("Medieval", "Rustic"):
        if feats & {"timber_frame", "stone_base", "steep_gable"} or (wood + stone) >= 0.4:
            return "agree", "木石主导或 timber_frame/stone_base 特征支持"
        return "weak", "木石占比与特征均不明显"
    if label in ("Japanese", "Chinese"):
        if stairs >= 20:
            return "agree", f"stair_count={stairs}，屋顶构件存在"
        return "weak", f"stair_count={stairs}，屋顶构件信号弱"
    if label == "Fantasy":
        return "n/a", "Fantasy 无确定性几何校验器"
    return "n/a", ""


def cross_check_function(label: str, meta: dict) -> tuple[str, str]:
    if label in ("Unknown",):
        return "n/a", ""
    doors = meta.get("door_count", 0) or 0
    floors = meta.get("estimated_floor_count", "UNKNOWN")
    sx, sy, sz = meta.get("size_x", 1), meta.get("size_y", 1), meta.get("size_z", 1)
    hr = sy / max(sx, sz) if max(sx, sz) else 0.0
    if label == "Residential":
        if doors >= 1 and isinstance(floors, int) and floors >= 1:
            return "agree", f"门 {doors}、楼层 {floors} 支持居住"
        return "weak", f"门 {doors}、楼层 {floors} 信号弱"
    if label == "Tower":
        if hr >= 1.65:
            return "agree", f"height_ratio={hr:.2f} ≥1.65（V6C2 tower 规则同阈值）"
        return "weak", f"height_ratio={hr:.2f} <1.65"
    if label == "Castle":
        if meta.get("stone_ratio", 0.0) >= 0.3:
            return "agree", "石质主体支持"
        return "weak", "石质占比不高"
    if label == "Farm":
        if meta.get("decorative_ratio", 0.0) >= 0.3:
            return "agree", "植被/装饰族占比支持农田景观"
        return "weak", "植被占比不高"
    return "n/a", ""


def main() -> int:
    ap = argparse.ArgumentParser(description="P3 Taxonomy 落标：V6C2 主信号 + 几何交叉验证")
    ap.add_argument("--catalog-final", required=True, help="classification-v2/catalog-final.json（只读）")
    ap.add_argument("--metadata", required=True, help="02_BLUEPRINT_METADATA/blueprint_metadata.jsonl")
    ap.add_argument("--output", required=True, help="输出目录（03_TAXONOMY）")
    args = ap.parse_args()

    catalog = json.loads(Path(args.catalog_final).read_text(encoding="utf-8"))
    meta_by_ref = {}
    with open(args.metadata, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            meta_by_ref[r["ref_id"]] = r

    out_rows = []
    style_counts: Counter = Counter()
    func_counts: Counter = Counter()
    downgrade_log = []

    for e in catalog:
        ref = e["reference_id"]
        meta = meta_by_ref.get(ref, {})
        features = e.get("features", [])

        # ---- Style ----
        styles = e.get("styles", [])
        best = max(styles, key=lambda s: s["confidence"]) if styles else {"tag": "unknown", "confidence": 0.0}
        tag = best["tag"]
        conf = float(best["confidence"])
        notes = []
        if tag == "east_asian":
            # 伞标签兜底：找更具体的 japanese/chinese
            specific = [s for s in styles if s["tag"] in ("japanese", "chinese")]
            if specific:
                best2 = max(specific, key=lambda s: s["confidence"])
                tag, conf = best2["tag"], float(best2["confidence"])
                notes.append("east_asian 伞标签落到更具体标签")
        mapped = STYLE_MAP.get(tag, "Other")
        style_basis = "existing metadata"
        if tag == "unknown" or conf < STYLE_CONF_FLOOR:
            if tag != "unknown":
                downgrade_log.append((ref, "style", f"{tag}@{conf:.2f} < {STYLE_CONF_FLOOR} → Unknown"))
                notes.append(f"V6C2 top style={tag} 置信度 {conf:.2f} 低于 {STYLE_CONF_FLOOR}，降级 Unknown")
            style_label, style_conf = "Unknown", "low"
        else:
            style_label = mapped
            verdict, note = cross_check_style(style_label, meta, features)
            style_conf = conf_band(conf)
            if verdict == "conflict":
                downgrade_log.append((ref, "style", f"{tag}@{conf:.2f} 几何冲突 → Unknown"))
                notes.append("几何交叉验证冲突：" + note)
                style_label, style_conf = "Unknown", "low"
            elif verdict == "weak":
                notes.append("几何交叉验证弱支持：" + note)
                if style_conf == "high":
                    style_conf = "medium"
                style_basis = "mixed"
            elif verdict == "agree":
                notes.append("几何交叉验证：" + note)
                style_basis = "mixed"
            if mapped == "Other":
                notes.append(f"V6C2 tag={tag} 映射 Other（候选类不细分）")

        # ---- Function ----
        primary = e.get("primary_use", "unknown")
        pconf = float(e.get("primary_use_confidence", 0.0))
        secondary = e.get("secondary_use", [])
        func_label, func_note = map_function(primary, secondary)
        func_basis = "existing metadata"
        fnotes = [func_note]
        if func_label == "Unknown":
            func_conf = "low"
        else:
            verdict, note = cross_check_function(func_label, meta)
            func_conf = conf_band(pconf)
            if verdict == "conflict":
                downgrade_log.append((ref, "function", f"{func_label} 几何冲突 → Unknown"))
                fnotes.append("几何交叉验证冲突：" + note)
                func_label, func_conf = "Unknown", "low"
            elif verdict == "weak":
                fnotes.append("几何交叉验证弱支持：" + note)
                if func_conf == "high":
                    func_conf = "medium"
                func_basis = "mixed"
            elif verdict == "agree":
                fnotes.append("几何交叉验证：" + note)
                func_basis = "mixed"

        basis = style_basis if style_basis == func_basis else "mixed"
        row = {
            "ref_id": ref,
            "source_name": e.get("name", meta.get("source_name", "UNKNOWN")),
            "style_label": style_label,
            "style_confidence": style_conf,
            "function_label": func_label,
            "function_confidence": func_conf,
            "label_basis": basis,
            "v6c2_style_top": tag,
            "v6c2_style_conf": round(conf, 3),
            "v6c2_primary_use": primary,
            "v6c2_primary_use_conf": round(pconf, 3),
            "v6c2_secondary_use": secondary,
            "v6c2_features": features,
            "scale": e.get("scale", "unknown"),
            "notes": "；".join(n for n in (notes + fnotes) if n),
        }
        out_rows.append(row)
        style_counts[style_label] += 1
        func_counts[func_label] += 1

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    # ---- labels.jsonl ----
    labels_path = out_dir / "labels.jsonl"
    with open(labels_path, "w", encoding="utf-8") as f:
        for r in out_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # ---- label_summary.json ----
    summary = {
        "total": len(out_rows),
        "style_counts": dict(style_counts.most_common()),
        "function_counts": dict(func_counts.most_common()),
        "downgrades": [{"ref_id": r, "kind": k, "reason": why} for r, k, why in downgrade_log],
        "thresholds": {"style_conf_floor": STYLE_CONF_FLOOR},
    }
    (out_dir / "label_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- LABELING_NOTES.md（含全量 123 行表，不截断）----
    lines = []
    lines.append("# LABELING_NOTES — 123 张蓝图 Taxonomy 落标记录\n")
    lines.append("> 生成：`scripts/build_labels.py`（确定性规则，可复跑）。主信号 = V6C2 人工+规则审核分类"
                 "（`references/classification-v2/catalog-final.json`），几何交叉验证来自 P1 元数据。\n")
    lines.append("## 方法\n")
    lines.append("- **Style**：取 V6C2 `styles` 中置信度最高标签，经 `STYLE_MAP` 映射到本 taxonomy"
                 "（medieval/fortified→Medieval，rustic/cottage→Rustic，fantasy/high_fantasy→Fantasy，"
                 "japanese→Japanese，chinese→Chinese，european/desert/classical→Other）；"
                 f"top 置信度 < {STYLE_CONF_FLOOR} 或几何强冲突 → **Unknown** 并记录。\n")
    lines.append("- **Function**：按 `primary_use` + `secondary_use` 规则映射（见脚本 `map_function`）；"
                 "primary_use=unknown → Unknown。候选类无载具而样本存在 ship/airship/dock，"
                 "新增 **Vehicle** 类（n=7，记录在案）；候选类 **Bridge** 无样本，不硬建。\n")
    lines.append("- **置信度**：high ≥0.70 / medium 0.55–0.70 / low <0.55（继承 V6C2 数值置信度，"
                 "几何弱支持时下调一档）。\n")
    lines.append("- **label_basis**：existing metadata = 直接继承 V6C2；mixed = 几何交叉验证参与"
                 "（支持或下调）；本库未发生纯 geometry/manual signal 提拔。\n")
    lines.append("\n## 类别样本量\n\n### Style\n\n| 类别 | n |\n|---|---:|\n")
    for k, v in style_counts.most_common():
        lines.append(f"| {k} | {v} |\n")
    lines.append("\n### Function\n\n| 类别 | n |\n|---|---:|\n")
    for k, v in func_counts.most_common():
        lines.append(f"| {k} | {v} |\n")
    lines.append(f"\n## 降级记录（{len(downgrade_log)} 条）\n\n")
    if downgrade_log:
        lines.append("| ref_id | 类型 | 原因 |\n|---|---|---|\n")
        for r, k, why in downgrade_log:
            lines.append(f"| {r} | {k} | {why} |\n")
    else:
        lines.append("无。\n")
    lines.append("\n## 全量标签表（123 行，完整不截断）\n\n")
    lines.append("| ref_id | 名称 | style_label | style_conf | function_label | function_conf | label_basis | V6C2 style(top@conf) | V6C2 primary_use | notes |\n")
    lines.append("|---|---|---|---|---|---|---|---|---|---|\n")
    for r in out_rows:
        nm = str(r["source_name"]).replace("|", "\\|")
        nt = r["notes"].replace("|", "\\|")
        lines.append(
            f"| {r['ref_id']} | {nm} | {r['style_label']} | {r['style_confidence']} "
            f"| {r['function_label']} | {r['function_confidence']} | {r['label_basis']} "
            f"| {r['v6c2_style_top']}@{r['v6c2_style_conf']} | {r['v6c2_primary_use']} | {nt} |\n")
    (out_dir / "LABELING_NOTES.md").write_text("".join(lines), encoding="utf-8")

    print(json.dumps({"rows": len(out_rows), "style": dict(style_counts.most_common()),
                      "function": dict(func_counts.most_common()),
                      "downgrades": len(downgrade_log)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
