# -*- coding: utf-8 -*-
"""P0 验证性扫描脚本（只读访问 references 库）。

用途：
- 统计 derived/REF-* 目录数、normalized/proxy/preview 覆盖率；
- 抽查 Canonical IR 结构、air 表示方式、DataVersion 分布、Region 分布；
- 输出 JSON 结果，供 01_INVENTORY 三份文档引用。

用法：
    python audit_scan.py --references-root <references路径> --output <输出json>
"""
from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser(description="P0 参考库验证性扫描（只读）")
    ap.add_argument("--references-root", required=True, help="references 目录")
    ap.add_argument("--output", required=True, help="扫描结果 JSON 输出路径")
    args = ap.parse_args()

    root = Path(args.references_root)
    derived = root / "derived"
    catalog_path = root / "catalog" / "catalog.json"

    ref_dirs = sorted(p for p in derived.iterdir() if p.is_dir() and p.name.startswith("REF-"))

    coverage = {
        "blueprint.json": 0,
        "normalized/normalized-blueprint.json": 0,
        "normalized/normalization-report.json": 0,
        "normalized/original-blueprint.json": 0,
        "proxy/": 0,
        "preview-metadata.json": 0,
        "metadata.json": 0,
        "analysis.md": 0,
    }
    data_versions: collections.Counter = collections.Counter()
    region_counts: collections.Counter = collections.Counter()
    compatibility: collections.Counter = collections.Counter()
    unresolved_total = 0
    air_representations: collections.Counter = collections.Counter()
    air_in_blocks_stats = {"with_air": 0, "without_air": 0}
    samples = {}

    for rd in ref_dirs:
        for rel in list(coverage):
            if rel.endswith("/"):
                if (rd / rel.rstrip("/")).is_dir():
                    coverage[rel] += 1
            elif (rd / rel).is_file():
                coverage[rel] += 1

        # normalized IR：结构与 air 表示
        nb_path = rd / "normalized" / "normalized-blueprint.json"
        if nb_path.is_file():
            nb = json.loads(nb_path.read_text(encoding="utf-8"))
            palette = nb.get("palette", [])
            air_entries = [p for p in palette if "air" in p]
            for a in air_entries:
                air_representations[a.split("[")[0]] += 1
            used_idx = {b[3] for b in nb.get("blocks", [])}
            air_idx = {i for i, p in enumerate(palette) if "air" in p}
            if used_idx & air_idx:
                air_in_blocks_stats["with_air"] += 1
            else:
                air_in_blocks_stats["without_air"] += 1
            if rd.name in ("REF-0001", "REF-0123"):
                samples[rd.name] = {
                    "top_keys": list(nb.keys()),
                    "dimensions": nb.get("dimensions"),
                    "origin": nb.get("origin"),
                    "palette_size": len(palette),
                    "blocks": len(nb.get("blocks", [])),
                    "air_palette_entries": air_entries,
                    "sample_block": nb.get("blocks", [None])[0],
                }

        nr_path = rd / "normalized" / "normalization-report.json"
        if nr_path.is_file():
            nr = json.loads(nr_path.read_text(encoding="utf-8"))
            compatibility[str(nr.get("compatibility"))] += 1
            un = nr.get("unresolved")
            if isinstance(un, list):
                unresolved_total += len(un)
            elif isinstance(un, int):
                unresolved_total += un

    # DataVersion / Region 分布来自 catalog（OBSERVED）
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    for item in catalog:
        data_versions[str(item.get("minecraft_data_version") or item.get("original_data_version"))] += 1
        region_counts[str(item.get("region_count"))] += 1

    result = {
        "references_root": str(root),
        "ref_dir_count": len(ref_dirs),
        "coverage": coverage,
        "catalog_count": len(catalog),
        "data_version_distribution": dict(sorted(data_versions.items())),
        "region_count_distribution": dict(sorted(region_counts.items())),
        "compatibility_distribution": dict(sorted(compatibility.items())),
        "unresolved_total": unresolved_total,
        "air_palette_representations": dict(air_representations),
        "air_explicit_in_blocks": air_in_blocks_stats,
        "samples": samples,
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
