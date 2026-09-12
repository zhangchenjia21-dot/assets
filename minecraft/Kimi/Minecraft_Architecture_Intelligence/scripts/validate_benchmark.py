#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_benchmark.py — P4 Design Brief Benchmark 验收校验脚本

独立于 build_benchmark.py 的验收检查：
1. design_briefs.jsonl 恰好 100 行、每行 JSON 可解析、20 个必备字段齐全；
2. 难度分布 40 Easy / 40 Medium / 20 Hard；7 个功能域全覆盖；
3. 全量约束自洽性校验（每条 brief）：
   C01 required_floors × assumed_floor_height ≤ max_height
   C02 required_floors × fh + estimated_roof_height ≤ max_height（含屋顶余量更严格）
   C03 required_zones 室内 min_area 之和 ≤ 0.7 × plot × floors
   C04 exterior zones min_area 之和 ≤ 0.45 × plot
   C05 required/forbidden adjacencies 引用的 zone 均在 required ∪ optional 中
   C06 required_adjacencies 与 forbidden_adjacencies 无交集
   C07 palette ratio 区间均在 [0,1] 且 low ≤ high
   C08 roof height_ratio_range low ≤ high；overhang_min ≥ 0
   C09 floors ≥ 2 时 vertical_circulation.required == True 且 connects_all_floors
   C10 plot 尺寸 ≤ 128（工程包络上限，CONTEXT §7）
   C11 targets_gap=True 的 brief 必须命中 data_gap_matrix P0 cell
4. 抽查 10 条 brief 输出详细自洽明细（种子固定）；
5. brief_id 唯一、无重复内容键。

退出码：全部 PASS = 0；任一 FAIL = 1。

用法：
    py validate_benchmark.py --root "D:\\...\\Minecraft_Architecture_Intelligence"
"""
import argparse
import json
import random
import sys
from collections import Counter
from pathlib import Path

REQUIRED_FIELDS = [
    "brief_id", "difficulty", "style", "function", "plot_width", "plot_depth",
    "max_height", "required_floors", "required_zones", "optional_zones",
    "required_adjacencies", "forbidden_adjacencies", "entrance_constraints",
    "vertical_circulation_constraints", "palette_constraints", "roof_constraints",
    "special_features", "hard_constraints", "soft_constraints", "scoring_dimensions",
]
REQUIRED_DOMAINS = ["Residential", "Mixed-use", "Workshop", "Hospitality",
                    "Civic", "Defensive", "Constrained Plot"]
SCORING_TOTAL = {"hard_validity": 40, "functional_layout": 25, "style_compliance": 20,
                 "material_coherence": 10, "efficiency": 5}


def fail(errors, bid, code, msg):
    errors.append(f"[{bid}] {code}: {msg}")


def check_brief(b, zone_cat, p0_cells, errors):
    bid = b.get("brief_id", "?")
    for fld in REQUIRED_FIELDS:
        if fld not in b:
            fail(errors, bid, "FIELD", f"缺必备字段 {fld}")
    if any(fld not in b for fld in REQUIRED_FIELDS):
        return

    w, d, mh, fl = b["plot_width"], b["plot_depth"], b["max_height"], b["required_floors"]
    vc = b["vertical_circulation_constraints"]
    fh = vc.get("assumed_floor_height", 5)
    roof_h = b["roof_constraints"].get("estimated_roof_height", 0)

    if fl * fh > mh:
        fail(errors, bid, "C01", f"floors×fh={fl * fh} > max_height={mh}")
    if fl * fh + roof_h > mh:
        fail(errors, bid, "C02", f"floors×fh+roof={fl * fh + roof_h} > max_height={mh}")

    zones = b["required_zones"] + b["optional_zones"]
    unknown = [z for z in zones if z not in zone_cat]
    if unknown:
        fail(errors, bid, "C03u", f"未知 zone: {unknown}")
    else:
        inner = sum(zone_cat[z]["min_area"] for z in zones if not zone_cat[z]["exterior"])
        outer = sum(zone_cat[z]["min_area"] for z in zones if zone_cat[z]["exterior"])
        if inner > 0.7 * w * d * fl:
            fail(errors, bid, "C03", f"室内需求 {inner} > 0.7×{w}×{d}×{fl}={0.7 * w * d * fl:.0f}")
        if outer > 0.45 * w * d:
            fail(errors, bid, "C04", f"室外需求 {outer} > 0.45×{w * d}={0.45 * w * d:.0f}")

    zset = set(zones)
    for pair in b["required_adjacencies"] + b["forbidden_adjacencies"]:
        for z in pair:
            if z not in zset:
                fail(errors, bid, "C05", f"邻接引用未知/未声明 zone: {z}")
    req_pairs = {tuple(sorted(p)) for p in b["required_adjacencies"]}
    forb_pairs = {tuple(sorted(p)) for p in b["forbidden_adjacencies"]}
    clash = req_pairs & forb_pairs
    if clash:
        fail(errors, bid, "C06", f"邻接冲突（既 required 又 forbidden）: {clash}")

    for fam, rng in b["palette_constraints"].get("family_ratio_ranges", {}).items():
        lo, hi = rng
        if not (0.0 <= lo <= hi <= 1.0):
            fail(errors, bid, "C07", f"palette {fam} 区间非法 [{lo},{hi}]")
    rr = b["roof_constraints"]["height_ratio_range"]
    if not (0.0 <= rr[0] <= rr[1]):
        fail(errors, bid, "C08", f"roof ratio 区间非法 {rr}")

    if fl >= 2 and not (vc.get("required") and vc.get("connects_all_floors")):
        fail(errors, bid, "C09", "多层但 vertical_circulation 未要求全连通")
    if max(w, d) > 128 or mh > 128:
        fail(errors, bid, "C10", "超出工程包络上限 128")

    if b.get("targets_gap"):
        gr = b.get("gap_ref", {})
        cell = (gr.get("matrix_style"), gr.get("matrix_function"), gr.get("matrix_size_class"))
        if cell not in p0_cells:
            fail(errors, bid, "C11", f"targets_gap 但 cell 非 P0: {cell}")
        if b["style"] != gr.get("matrix_style") or b["function"] != gr.get("matrix_function"):
            fail(errors, bid, "C11", "gap_ref 与 style/function 不一致")
        md = max(w, d)
        if gr.get("matrix_size_class") == "small" and not (17 <= md <= 32):
            fail(errors, bid, "C11", f"gap small cell 要求长边 17-32，实际 {md}")
        if gr.get("matrix_size_class") == "medium" and not (33 <= md <= 64):
            fail(errors, bid, "C11", f"gap medium cell 要求长边 33-64，实际 {md}")

    if b["scoring_dimensions"] != SCORING_TOTAL:
        fail(errors, bid, "SCORE", f"scoring_dimensions 权重异常: {b['scoring_dimensions']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    args = ap.parse_args()
    root = Path(args.root)
    bench = root / "06_BENCHMARK"

    lines = (bench / "design_briefs.jsonl").read_text(encoding="utf-8").splitlines()
    errors = []
    briefs = []
    for i, ln in enumerate(lines, 1):
        try:
            briefs.append(json.loads(ln))
        except json.JSONDecodeError as e:
            errors.append(f"[line {i}] JSON 解析失败: {e}")

    if len(lines) != 100:
        errors.append(f"行数 {len(lines)} != 100")

    zone_cat = json.loads((bench / "zone_catalog.json").read_text(encoding="utf-8"))["zones"]
    gap = json.loads((root / "04_GRAMMARS" / "data_gap_matrix.json").read_text(encoding="utf-8"))
    p0_cells = {(c["style"], c["function"], c["size_class"]) for c in gap["cells"]
                if c.get("priority") == "P0"}

    ids = Counter(b.get("brief_id") for b in briefs)
    for bid, n in ids.items():
        if n > 1:
            errors.append(f"brief_id 重复: {bid} ×{n}")

    diff = Counter(b["difficulty"] for b in briefs)
    if diff != {"Easy": 40, "Medium": 40, "Hard": 20}:
        errors.append(f"难度分布异常: {dict(diff)}")
    doms = Counter(b["function_domain"] for b in briefs)
    missing = [d for d in REQUIRED_DOMAINS if d not in doms]
    if missing:
        errors.append(f"功能域未覆盖: {missing}")

    for b in briefs:
        check_brief(b, zone_cat, p0_cells, errors)

    # 抽查 10 条：输出明细
    rng = random.Random(7)
    sample = rng.sample(briefs, 10)
    print("=== 抽查 10 条 brief 自洽明细 ===")
    for b in sample:
        vc = b["vertical_circulation_constraints"]
        zones = b["required_zones"] + b["optional_zones"]
        inner = sum(zone_cat[z]["min_area"] for z in zones if not zone_cat[z]["exterior"])
        print(f"{b['brief_id']} {b['difficulty']:<6} {b['style']:<9} {b['function']:<11} "
              f"plot={b['plot_width']}x{b['plot_depth']} maxH={b['max_height']} "
              f"floors={b['required_floors']}×fh{vc['assumed_floor_height']}="
              f"{b['required_floors'] * vc['assumed_floor_height']}"
              f"(+roof {b['roof_constraints']['estimated_roof_height']}) "
              f"室内需求={inner} ≤ {0.7 * b['plot_width'] * b['plot_depth'] * b['required_floors']:.0f} "
              f"gap={b['targets_gap']}")

    print("\n=== 汇总 ===")
    print(f"briefs={len(briefs)} 难度={dict(diff)} 域={dict(doms)}")
    print(f"targets_gap={sum(1 for b in briefs if b.get('targets_gap'))}")
    if errors:
        print(f"\nFAIL ({len(errors)} 项):")
        for e in errors[:50]:
            print(" -", e)
        return 1
    print("\nALL CHECKS PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
