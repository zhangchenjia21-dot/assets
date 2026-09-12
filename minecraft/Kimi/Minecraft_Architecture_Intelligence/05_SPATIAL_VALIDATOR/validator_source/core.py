# -*- coding: utf-8 -*-
"""core — Spatial Validator 编排与评分（项目代号 H · P2）。

对一张蓝图：构建 SpatialContext → 跑 V001–V012 → 汇总任务书第 11 节字段：

    validation_status / hard_fail_count / warning_count / info_count /
    rules_triggered / walkability_score / connectivity_score /
    vertical_circulation_score / validator_confidence

评分定义（透明、可复算，全部 0–100 或 UNKNOWN）：
- walkability_score   = 100 × 合法站位 / 潜在站位（提供支撑的体素数）。
                        低分 = 大量“能站却站不了”的区域（净高/顶盖问题）。
- connectivity_score  = 内部站位优先：100 × 主入口所在分量内部站位 / 全部内部站位；
                        无内部站位时退化为 100 × largest_component_ratio。
- vertical_circulation_score = 可用楼层 ≤1 → 100；否则 100 × 与主流通连通的
                        可用楼层 / 可用楼层总数。楼层 UNKNOWN → UNKNOWN。
- validator_confidence = 未知方块（保守视为实体）越多置信度越低：
                        0 种 → high；≤3 种或占比 <2% → medium；否则 low。
"""
from __future__ import annotations

from pathlib import Path

from rules import RULES, RuleResult, _main_interior_component
from spatial_context import SpatialContext

DEFAULT_RULES_PATH = Path(__file__).resolve().parent.parent / "validator_rules.json"


def load_rules_config(path: str | Path | None = None) -> dict:
    import json
    p = Path(path) if path else DEFAULT_RULES_PATH
    return json.loads(p.read_text(encoding="utf-8"))


def _validator_confidence(ctx) -> str:
    unk_types = ctx.walk["unknown_block_type_count"]
    if unk_types == 0:
        return "high"
    if unk_types <= 3:
        return "medium"
    return "low"


def _vertical_score(ctx, params: dict):
    floors = ctx.floor_stance_sets(level_tol=params.get("level_tol", 0.6))
    if not ctx.floor_elevations:
        return "UNKNOWN"
    min_stances = params.get("min_floor_stances", 6)
    if ctx.interior_stance_count == 0:
        return "UNKNOWN"   # 开放结构不做垂直交通评分
    usable = [fs for fs in floors if len(fs["interior"]) >= min_stances]
    if len(usable) <= 1:
        return 100.0
    base_comps = {ctx.component_of_flat(fi) for fi in usable[0]["interior"]}
    connected = sum(1 for fs in usable
                    if {ctx.component_of_flat(fi) for fi in fs["interior"]} & base_comps)
    return round(100.0 * connected / len(usable), 1)


def validate_one(path: str | Path, rules_config: dict | None = None,
                 rules_path: str | Path | None = None) -> dict:
    """校验单张蓝图，返回任务书第 11 节字段 + 逐规则结果。"""
    cfg = rules_config if rules_config is not None else load_rules_config(rules_path)
    ctx = SpatialContext(path, floor_params=cfg.get("floor_detection"))

    results: list[RuleResult] = []
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

    if hard:
        status = "HARD_FAIL"
    elif warn:
        status = "WARNING"
    else:
        status = "PASS"

    # ---- 评分 ------------------------------------------------------------
    potential = max(ctx.potential_stance_voxels, 1)
    walkability_score = round(100.0 * ctx.walkable_voxels / potential, 1)
    if ctx.interior_stance_count > 0 and ctx.interior_comp_counts:
        main_comp = _main_interior_component(ctx)
        main_n = ctx.interior_comp_counts.get(main_comp, 0)
        connectivity_score = round(100.0 * main_n / ctx.interior_stance_count, 1)
    elif ctx.walkable_voxels > 0:
        connectivity_score = round(100.0 * ctx.walk["largest_component_ratio"], 1)
    else:
        connectivity_score = "UNKNOWN"
    vertical_score = _vertical_score(ctx, cfg.get("V007", {}).get("params", {}))

    return {
        "ref_id": ctx.ir.ref_id or ctx.path.name,
        "ir_source": ctx.ir.ir_source,
        "path": str(ctx.path),
        "validation_status": status,
        "hard_fail_count": len(hard),
        "warning_count": len(warn),
        "info_count": len(info),
        "rules_triggered": [r.rule_id for r in triggered],
        "walkability_score": walkability_score,
        "connectivity_score": connectivity_score,
        "vertical_circulation_score": vertical_score,
        "validator_confidence": _validator_confidence(ctx),
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
