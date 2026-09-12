# -*- coding: utf-8 -*-
"""从 catalog.json 生成 01_INVENTORY/BLUEPRINT_MANIFEST.md（123 行全量清单）。

用法：
    python build_manifest.py --catalog <catalog.json> --output <BLUEPRINT_MANIFEST.md>
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser(description="生成蓝图全量清单 Markdown")
    ap.add_argument("--catalog", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    catalog = json.loads(Path(args.catalog).read_text(encoding="utf-8"))
    catalog.sort(key=lambda i: i["reference_id"])

    lines = []
    lines.append("# BLUEPRINT_MANIFEST — 参考蓝图全量清单")
    lines.append("")
    lines.append(f"- 蓝图总数：**{len(catalog)}**")
    lines.append("- 数据来源：`references\\catalog\\catalog.json`（OBSERVED，只读）")
    lines.append("- 生成脚本：`scripts/build_manifest.py`")
    lines.append("- 字段说明：尺寸为 `x×y×z`（方块格）；style tags 来自 catalog 的 `styles`（tag:confidence），仅列出置信度 ≥0.5 的标签。")
    lines.append("")
    lines.append("| ref_id | 文件名 | 名称 | 尺寸 (x×y×z) | block_count | compatibility | primary_use | style tags |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for it in catalog:
        dims = it.get("dimensions") or {}
        size = f"{dims.get('x','?')}×{dims.get('y','?')}×{dims.get('z','?')}"
        styles = it.get("styles") or []
        tags = ", ".join(
            f"{s['tag']}:{s['confidence']:.2f}"
            for s in styles if s.get("confidence", 0) >= 0.5
        ) or "—"
        fname = (it.get("original_filename") or "").replace(".litematic", "")
        lines.append(
            f"| {it['reference_id']} | {fname} | {it.get('name','')} | {size} "
            f"| {it.get('block_count','')} | {it.get('compatibility','')} "
            f"| {it.get('primary_use','')} | {tags} |"
        )
    lines.append("")

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"written {out}, rows={len(catalog)}")


if __name__ == "__main__":
    main()
