# -*- coding: utf-8 -*-
"""validate_blueprints — Spatial Validator CLI / 批量入口（项目代号 H · P2）。

用法：
    # 批量：references derived 目录（扫描其下 REF-* 子目录，只读）
    py -3 validate_blueprints.py --input "D:\\Games\\...\\references\\derived" --output <dir>

    # 单张：REF 派生目录 / normalized-blueprint.json / blueprint.json
    py -3 validate_blueprints.py --input "D:\\Games\\...\\derived\\REF-0001" --output <dir>

    # 从 metadata.jsonl 批量（需 --references-root 解析 ref_id → derived 目录）
    py -3 validate_blueprints.py --input blueprint_metadata.jsonl \
        --references-root "D:\\Games\\...\\references" --output <dir>

    # 自定义规则阈值
    py -3 validate_blueprints.py --input ... --output ... --rules validator_rules.json

输出（--output 目录）：
    validation_results.jsonl   每张蓝图一行（任务书第 11 节字段 + 逐规则明细）
    validation_summary.json    批次汇总（触发频率、hard_fail_rate 等）

纪律：输入全程只读；单张失败记 PARSE_FAILURE，不中断批次。
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from core import load_rules_config, validate_one  # noqa: E402


def collect_inputs(input_path: Path, references_root: Path | None) -> list[Path]:
    """把 --input 解析成一组 REF 派生目录 / IR 文件路径。"""
    if input_path.is_dir():
        subs = sorted(p for p in input_path.iterdir()
                      if p.is_dir() and p.name.startswith("REF-"))
        if subs:
            return subs
        return [input_path]  # 单个 REF 目录
    if input_path.suffix == ".jsonl":
        if references_root is None:
            raise SystemExit("--input 为 jsonl 时必须提供 --references-root")
        out = []
        with input_path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                rid = rec.get("ref_id")
                if rid:
                    out.append(Path(references_root) / "derived" / rid)
        return out
    return [input_path]  # 单个 IR 文件


def main() -> None:
    ap = argparse.ArgumentParser(description="Spatial Validator（V001–V012）批量/单张校验")
    ap.add_argument("--input", required=True,
                    help="REF 派生目录 / derived 根目录 / 单个 IR JSON / metadata.jsonl")
    ap.add_argument("--output", required=True, help="输出目录（写入工作区）")
    ap.add_argument("--references-root", default=None,
                    help="jsonl 输入时解析 ref_id 用")
    ap.add_argument("--rules", default=None, help="规则阈值 JSON（默认 validator_rules.json）")
    args = ap.parse_args()

    cfg = load_rules_config(args.rules)
    targets = collect_inputs(Path(args.input),
                             Path(args.references_root) if args.references_root else None)

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    results, failures = [], []
    for t in targets:
        try:
            results.append(validate_one(t, rules_config=cfg))
        except Exception as exc:  # noqa: BLE001 — 批次纪律
            failures.append({"ref_id": Path(t).name, "status": "PARSE_FAILURE",
                             "file": str(t), "error": f"{type(exc).__name__}: {exc}"})

    jsonl = out_dir / "validation_results.jsonl"
    with jsonl.open("w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
        for r in failures:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    n = len(results)
    rule_freq = Counter()
    for r in results:
        for rid in r["rules_triggered"]:
            rule_freq[rid] += 1
    status_dist = Counter(r["validation_status"] for r in results)
    summary = {
        "blueprints_validated": n,
        "parse_failures": failures,
        "status_distribution": dict(status_dist),
        "hard_fail_rate": round(status_dist.get("HARD_FAIL", 0) / n, 4) if n else 0.0,
        "warning_rate": round(
            sum(1 for r in results if r["warning_count"] > 0) / n, 4) if n else 0.0,
        "rule_trigger_frequency": {rid: rule_freq.get(rid, 0)
                                   for rid in sorted(cfg) if rid.startswith("V")},
    }
    (out_dir / "validation_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"validated": n, "failures": len(failures),
                      "hard_fail_rate": summary["hard_fail_rate"],
                      "jsonl": str(jsonl)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
