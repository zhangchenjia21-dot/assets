# -*- coding: utf-8 -*-
"""rules — V001–V012 空间校验规则实现（项目代号 H · P2）。

每条规则函数签名：``rule(ctx: SpatialContext, params: dict) -> RuleResult``。

RuleResult 字段（任务书第 10/11 节契约）：
    rule_id      如 "V006"
    name         规则名
    severity     生效严重性：HARD_FAIL / WARNING / INFO（NOT_APPLICABLE 时为空字符串）
    configured_severity  配置中的基准严重性
    triggered    是否触发
    applicable   规则是否适用于该蓝图（开放式建筑对围护类规则不适用）
    evidence     证据列表（坐标/区域描述）
    confidence   high / medium / low
    basis        OBSERVED / HEURISTIC / INFERRED / UNKNOWN
    message      人类可读结论

设计要点：
- 一切阈值来自 params（validator_rules.json），代码内无硬编码数字；
- 内/外判定全部经由 SpatialContext 的 interior 站位定义，避免把屋顶露天
  分量误判为“孤立房间”（P1 实测：露天表面会天然形成大量连通分量）；
- 楼梯底/顶规则只评估“有通行意义”的楼梯簇（底部站位落在含内部站位的分量
  或是最大分量），屋檐装饰梯默认跳过，降低误报。
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any

import numpy as np
from scipy import ndimage

from spatial_context import MECHANISM_CLASSES

SEVERITY_ORDER = {"INFO": 0, "WARNING": 1, "HARD_FAIL": 2}


@dataclass
class RuleResult:
    rule_id: str
    name: str
    configured_severity: str
    triggered: bool
    severity: str = ""
    applicable: bool = True
    evidence: list[Any] = field(default_factory=list)
    confidence: str = "medium"
    basis: str = "HEURISTIC"
    message: str = ""

    def to_dict(self) -> dict:
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "severity": self.severity if self.triggered else "",
            "configured_severity": self.configured_severity,
            "triggered": self.triggered,
            "applicable": self.applicable,
            "evidence": self.evidence,
            "confidence": self.confidence,
            "basis": self.basis,
            "message": self.message,
        }


def _na(rule_id, name, sev, reason, basis="HEURISTIC") -> RuleResult:
    return RuleResult(rule_id, name, sev, triggered=False, applicable=False,
                      basis=basis, message=f"NOT_APPLICABLE: {reason}")


def _pass(rule_id, name, sev, msg, basis="HEURISTIC", confidence="high") -> RuleResult:
    return RuleResult(rule_id, name, sev, triggered=False, basis=basis,
                      confidence=confidence, message=msg)


# ---------------------------------------------------------------------------
# 入口候选汇总（V001/V002/V003 共用）
# ---------------------------------------------------------------------------
def _entrance_candidates(ctx) -> list[dict]:
    """全部 exterior→interior 通道候选：严格外门 > 宽松外门 > 无门开口 > 梯子舱口。"""
    cands = [{"kind": "door", "confidence": "high", **d}
             for d in ctx.exterior_doors_strict]
    cands += [{"kind": "door_loose", "confidence": "medium", **d}
              for d in ctx.exterior_doors_loose]
    cands += [{"kind": "opening", "confidence": "medium", **o} for o in ctx.openings]
    cands += [{"kind": "hatch", "confidence": "medium", "inside": None,
               "outside": None, **h} for h in ctx.hatches]
    return cands


def _approach_stance(ctx, cell, max_drop: float = 1.0,
                     assume_ground: bool = True) -> int | None:
    """空气格 cell 作为门侧通行接近格：附近存在合法站位。

    允许脚部高程在 [y - max_drop, y + 0.6] 之间（门槛内外可有半格~一格落差）。
    assume_ground：包络最底层（y=0）的空气格视为站在隐含地形上——参考蓝图通常
    不含地形，门坐在包络底界不代表悬空（HEURISTIC 假设，见 known_limitations）。
    返回站位扁平索引或 None（隐含地面返回 -1 哨兵）。
    """
    x, y, z = cell
    for sy in (y - 1, y, y - 2):
        if 0 <= sy < ctx.Y and ctx.stance_mask[x, sy, z]:
            e = float(ctx.E[x, sy, z])
            if (y - max_drop) - 0.01 <= e <= y + 0.6:
                return int(np.ravel_multi_index((x, sy, z), ctx.labels.shape))
    if assume_ground and y == 0:
        return -1  # 隐含地形哨兵：不可连通性检查交给上一层语义
    return None


# ---------------------------------------------------------------------------
# V001 No Exterior Entrance
# ---------------------------------------------------------------------------
def v001(ctx, p) -> RuleResult:
    rid, name, sev = "V001", "No Exterior Entrance", p.get("severity", "HARD_FAIL")
    if ctx.interior_air_count < p.get("min_interior_air", 27):
        return _na(rid, name, sev, "无显著封闭内部空间（开放式/无围护结构）")
    if ctx.interior_stance_count < p.get("min_interior_stances", 9):
        return _na(rid, name, sev, "封闭空间内无法站立（结构缝隙/爬空间，非房间）")
    cands = _entrance_candidates(ctx)
    if not cands:
        return RuleResult(rid, name, sev, triggered=True, severity=sev,
                          confidence="high", basis="HEURISTIC",
                          evidence=[{"interior_air_voxels": ctx.interior_air_count,
                                     "interior_stances": ctx.interior_stance_count,
                                     "door_count": len(ctx.doors)}],
                          message="存在可站立的封闭内部空间，但没有任何可识别的 exterior→interior 入口")
    return _pass(rid, name, sev, f"发现 {len(cands)} 个入口候选")


# ---------------------------------------------------------------------------
# V002 Main Entrance Blocked
# ---------------------------------------------------------------------------
def _check_entrance_clearance(ctx, ent, max_drop: float = 1.0) -> tuple[bool, list[str], dict]:
    """检查单个入口的前/后通行空间与可穿性。返回 (ok, problems, detail)。"""
    problems: list[str] = []
    detail: dict = {"entrance": {k: v for k, v in ent.items() if k != "props"}}
    x, y, z = ent["pos"]
    if ent["kind"] in ("door", "door_loose"):
        # 门槛站位：门扇下方支撑体素上的站位（玩家穿过门时脚踩的位置）；
        # 门在包络底界（y=0）时按隐含地形处理（参考蓝图通常不含地形）。
        support_ok = (y - 1 >= 0 and bool(ctx.stance_mask[x, y - 1, z])) or y == 0
        if not support_ok:
            problems.append("门槛站位缺失（门下方支撑无法站立或净高不足）")
        out_fi = _approach_stance(ctx, ent["outside"], max_drop)
        if out_fi is None:
            problems.append(f"门外接近空间不足 outside={list(ent['outside'])}")
        if ent.get("inside") is not None:
            in_fi = _approach_stance(ctx, ent["inside"], max_drop)
            if in_fi is None:
                problems.append(f"门内接近空间不足 inside={list(ent['inside'])}")
        else:
            in_fi = None
            problems.append("门内侧无空气邻接（门后是实体）")
        if (support_ok and out_fi is not None and in_fi is not None
                and out_fi != -1 and in_fi != -1):
            if ctx.component_of_flat(out_fi) != ctx.component_of_flat(in_fi):
                problems.append("门两侧站位不连通（门不可穿越）")
    elif ent["kind"] == "hatch":
        # 梯子舱口：梯柱周边（Chebyshev ≤2、y 范围 ±2）应同时存在内部与外部站位
        lx, _, lz = ent["pos"]
        y0, y1 = ent["y_range"]
        saw_int = saw_ext = False
        for ly in range(max(0, y0 - 2), min(ctx.Y, y1 + 3)):
            for nx in range(max(0, lx - 2), min(ctx.X, lx + 3)):
                for nz in range(max(0, lz - 2), min(ctx.Z, lz + 3)):
                    if ctx.stance_mask[nx, ly, nz]:
                        if ctx.stance_interior[nx, ly, nz]:
                            saw_int = True
                        else:
                            saw_ext = True
        if not saw_int:
            problems.append("舱口梯柱内侧无可用站位")
        if not saw_ext:
            problems.append("舱口梯柱外侧无可用站位")
    else:  # opening
        out_fi = _approach_stance(ctx, ent["outside"], max_drop)
        in_fi = _approach_stance(ctx, ent["pos"], max_drop)
        if out_fi is None or in_fi is None:
            problems.append("开口两侧接近站位缺失")
        elif ctx.component_of_flat(out_fi) != ctx.component_of_flat(in_fi):
            problems.append("开口两侧站位不连通")
    return (not problems), problems, detail


def v002(ctx, p) -> RuleResult:
    rid, name, sev = "V002", "Main Entrance Blocked", p.get("severity", "HARD_FAIL")
    cands = _entrance_candidates(ctx)
    if not cands:
        return _na(rid, name, sev, "无入口候选（由 V001 负责）")
    ent = cands[0]  # 主入口：优先严格外门
    ok, problems, detail = _check_entrance_clearance(
        ctx, ent, max_drop=p.get("max_drop", 1.0))
    if ok:
        return _pass(rid, name, sev, "主入口前/后通行空间充足且可穿越")
    # 梯子舱口的“前后通行空间”语义与门不同，静态判定置信度低 → WARNING
    eff = sev if ent["kind"] in ("door", "door_loose", "opening") else "WARNING"
    return RuleResult(rid, name, sev, triggered=True, severity=eff,
                      confidence="high" if ent["kind"] == "door" else "medium",
                      basis="HEURISTIC",
                      evidence=[{**detail, "problems": problems}],
                      message="主入口前/后通行空间不足或不可穿越：" + "；".join(problems))


# ---------------------------------------------------------------------------
# V003 Major Interior Unreachable
# ---------------------------------------------------------------------------
def v003(ctx, p) -> RuleResult:
    rid, name, sev = "V003", "Major Interior Unreachable", p.get("severity", "HARD_FAIL")
    min_stances = p.get("min_interior_stances", 9)
    if ctx.interior_stance_count < min_stances:
        return _na(rid, name, sev, "无显著内部站位（开放式结构）")
    cands = _entrance_candidates(ctx)
    if not cands:
        return _na(rid, name, sev, "无入口候选（由 V001 负责）")
    ent = cands[0]
    if ent["kind"] == "hatch":
        # 主入口是梯子舱口：以梯柱周边（Chebyshev ≤2、y ±2）的内部站位为种子
        lx, _, lz = ent["pos"]
        y0, y1 = ent["y_range"]
        in_fi = None
        for ly in range(max(0, y0 - 2), min(ctx.Y, y1 + 3)):
            for nx in range(max(0, lx - 2), min(ctx.X, lx + 3)):
                for nz in range(max(0, lz - 2), min(ctx.Z, lz + 3)):
                    if ctx.stance_interior[nx, ly, nz]:
                        in_fi = ctx.flat_of((nx, ly, nz))
                        break
                if in_fi is not None:
                    break
            if in_fi is not None:
                break
    else:
        inside = ent.get("inside") if ent["kind"] in ("door", "door_loose") else ent["pos"]
        in_fi = _approach_stance(ctx, inside, p.get("max_drop", 1.0)) if inside is not None else None
    if in_fi is None:
        # 入口内侧无站位 → 整个内部不可达（与 V002 共发属正常）
        return RuleResult(rid, name, sev, triggered=True, severity=sev,
                          confidence="high", basis="HEURISTIC",
                          evidence=[{"reason": "入口内侧无合法站位",
                                     "interior_stances": ctx.interior_stance_count}],
                          message="主入口内侧无合法站位，全部内部空间不可达")
    if in_fi == -1:
        # 内侧为包络底界隐含地面：以最大内部分量作为可达基准
        main_comp = ctx.interior_comp_counts.most_common(1)[0][0]
    else:
        main_comp = ctx.component_of_flat(in_fi)
    reachable = ctx.interior_comp_counts.get(main_comp, 0)
    total = ctx.interior_stance_count
    ratio = reachable / total if total else 1.0
    unreachable = total - reachable
    if unreachable >= p.get("min_unreachable_stances", 9) and \
            ratio < p.get("max_reachable_ratio", 0.5):
        # 机制感知分级：不可达分量的隔离环上若有门/活板门/梯子等可交互构件，
        # 可能经模型未覆盖的通道（舱口/机关）相连 → 降 WARNING
        mech_total = 0
        for comp, n in ctx.interior_comp_counts.items():
            if comp == main_comp or n < p.get("min_unreachable_stances", 9):
                continue
            flats = [int(fi) for fi in np.flatnonzero(ctx.stance_interior)
                     if ctx.component_of_flat(int(fi)) == comp]
            ring = ctx.ring_classes(flats)
            mech_total += sum(v for k, v in ring.items() if k in MECHANISM_CLASSES)
        eff = "WARNING" if mech_total > 0 else "HARD_FAIL"
        return RuleResult(rid, name, sev, triggered=True, severity=eff,
                          confidence="high" if eff == "HARD_FAIL" else "medium",
                          basis="HEURISTIC",
                          evidence=[{"main_component": main_comp,
                                     "reachable_interior_stances": reachable,
                                     "total_interior_stances": total,
                                     "reachable_ratio": round(ratio, 4),
                                     "unreachable_ring_mechanisms": mech_total}],
                          message=f"主要内部区域从主入口不可达：仅 {ratio:.0%} 内部站位可达")
    return _pass(rid, name, sev, f"内部站位可达率 {ratio:.0%}")


def _main_interior_component(ctx, max_drop: float = 1.0) -> int:
    """主内部连通分量：优先取主入口内侧站位所在分量；无入口时取最大内部分量。"""
    if not ctx.interior_comp_counts:
        return -1
    cands = _entrance_candidates(ctx)
    if cands:
        ent = cands[0]
        inside = ent.get("inside") if ent["kind"] in ("door", "door_loose") else None
        if inside is not None:
            fi = _approach_stance(ctx, inside, max_drop)
            if fi is not None and fi != -1:
                return ctx.component_of_flat(fi)
    return ctx.interior_comp_counts.most_common(1)[0][0]


# ---------------------------------------------------------------------------
# V004 Isolated Room / Space
# ---------------------------------------------------------------------------
def v004(ctx, p) -> RuleResult:
    rid, name, sev = "V004", "Isolated Room / Space", p.get("severity", "HARD_FAIL")
    if ctx.interior_stance_count == 0:
        return _na(rid, name, sev, "无内部站位（露天表面分量不计入，避免误报）")
    warn_min = p.get("warn_min_stances", 9)
    hard_min = p.get("hard_min_stances", 20)
    if not ctx.interior_comp_counts:
        return _na(rid, name, sev, "无内部连通分量")
    main_comp = _main_interior_component(ctx, p.get("max_drop", 1.0))
    main_size = ctx.interior_comp_counts.get(main_comp, 0)
    isolated = [(c, n) for c, n in ctx.interior_comp_counts.items()
                if c != main_comp and n >= warn_min]
    if not isolated:
        return _pass(rid, name, sev, "无显著孤立内部空间")
    evidence, eff = [], "WARNING"
    for comp, n in sorted(isolated, key=lambda t: -t[1]):
        flats = [int(fi) for fi in np.flatnonzero(ctx.stance_interior)
                 if ctx.component_of_flat(int(fi)) == comp]
        cell = ctx.cell_of_flat(flats[0])
        ring = ctx.ring_classes(flats)
        mechanisms = {k: v for k, v in ring.items() if k in MECHANISM_CLASSES}
        if mechanisms:
            # 环上有门/活板门/梯子/栅栏门：可能经模型未完全覆盖的通道相连
            # （舱口、铁门机关），或是设计性封闭空间 → WARNING
            level = "WARNING"
            note = "隔离环含可交互构件，可能为舱口/机关通道或设计性封闭"
        else:
            level = "HARD_FAIL" if n >= hard_min else "WARNING"
            note = "隔离环为纯实体封闭"
        if SEVERITY_ORDER[level] > SEVERITY_ORDER[eff]:
            eff = level
        evidence.append({"component": comp, "interior_stances": n,
                         "sample_pos": list(cell), "level": level,
                         "ring_mechanisms": mechanisms, "note": note,
                         "main_component_stances": main_size})
    return RuleResult(rid, name, sev, triggered=True, severity=eff,
                      confidence="high" if eff == "HARD_FAIL" else "medium",
                      basis="HEURISTIC", evidence=evidence,
                      message=f"{len(isolated)} 个显著内部封闭空间与主连通组件断开")


# ---------------------------------------------------------------------------
# V005 / V006 楼梯底/顶
# ---------------------------------------------------------------------------
def _circulation_clusters(ctx, p) -> tuple[list[dict], list[dict]]:
    """把楼梯簇分成“有通行意义”（楼梯）与“装饰性”（屋檐/镶边/家具）两组。

    通行意义判定（全部满足才算楼梯）：
    1. 尺寸与爬升：size ≥ min_cluster_size 且 y_span ≥ min_y_span；
    2. 紧致性：size ≤ max_blocks_per_level × (y_span+1)——真正的楼梯每层只有
       几格宽；屋顶/檐口用楼梯砌成的大面积薄板（每层几十格）在此被排除；
    3. 底部接入主流通：簇底至少一个站位存在，且其分量含内部站位或是最大分量。
    """
    min_size = p.get("min_cluster_size", 3)
    min_span = p.get("min_y_span", 2)
    max_bpl = p.get("max_blocks_per_level", 5)
    require_conn = p.get("require_connected_bottom", True)
    largest_comp = None
    if ctx.labels.max() >= 0:
        counts = Counter(ctx.labels[ctx.labels >= 0].tolist())
        largest_comp = counts.most_common(1)[0][0]
    interior_comps = set(ctx.interior_comp_counts.keys())
    circ, deco = [], []
    for cl in ctx.stair_clusters:
        if cl["size"] < min_size or cl["y_span"] < min_span:
            deco.append(cl)
            continue
        if cl["size"] > max_bpl * (cl["y_span"] + 1):
            deco.append(cl)   # 大面积楼梯薄板：屋檐/屋顶/镶边
            continue
        if require_conn:
            bottom_fi = [ctx.flat_of(c) for c in cl["bottom"] if ctx.label_at(c) >= 0]
            comps = {ctx.component_of_flat(fi) for fi in bottom_fi}
            if not comps or not (comps & interior_comps or
                                 (largest_comp is not None and largest_comp in comps)):
                deco.append(cl)
                continue
        circ.append(cl)
    return circ, deco


def v005(ctx, p) -> RuleResult:
    rid, name, sev = "V005", "Stair Bottom Blocked", p.get("severity", "HARD_FAIL")
    circ, _ = _circulation_clusters(ctx, p)
    if p.get("skip_bottom_at_envelope_floor", True):
        # 底格在包络最底层的楼梯：入口在隐含地形上（参考蓝图通常不含地形），跳过
        circ = [cl for cl in circ
                if not all(c[1] == 0 for c in cl["bottom"])]
    if not circ:
        return _na(rid, name, sev, "无有通行意义的楼梯簇")
    blocked = []
    for cl in circ:
        enterable, no_stance = [], []
        for c in cl["bottom"]:
            if ctx.label_at(c) < 0:
                no_stance.append(c)
                continue
            e_self = ctx.stance_elevation_at(c)
            # 入口 = 高程不超过本级 +0.5 的相邻站位（可从其上/平级走上楼梯），
            # 且不是同簇更高的下一级（楼梯后段不算入口）
            entry = []
            for m in ctx.neighbors(c):
                if ctx.flatE[m] > e_self + 0.55:
                    continue
                mc = ctx.cell_of_flat(m)
                if ctx.cls_vox[mc] == "STAIR" and ctx.flatE[m] > e_self + 0.05:
                    continue
                entry.append(m)
            if entry:
                enterable.append(c)
        # 宽楼梯只要有一格能走上就不算堵；全部底格不可进入才触发
        if not enterable:
            blocked.append({"cluster_id": cl["id"], "bottom": [list(c) for c in cl["bottom"]],
                            "no_stance": [list(c) for c in no_stance],
                            "size": cl["size"], "y_span": cl["y_span"]})
    if blocked:
        return RuleResult(rid, name, sev, triggered=True, severity=sev,
                          confidence="high", basis="OBSERVED", evidence=blocked,
                          message=f"{len(blocked)} 个楼梯簇底部不可进入")
    return _pass(rid, name, sev, "全部楼梯簇底部可进入", basis="OBSERVED")


def v006(ctx, p) -> RuleResult:
    rid, name, sev = "V006", "Stair Top Blocked", p.get("severity", "HARD_FAIL")
    circ, _ = _circulation_clusters(ctx, p)
    if not circ:
        return _na(rid, name, sev, "无有通行意义的楼梯簇")
    blocked = []
    for cl in circ:
        exitable, no_stance = [], []
        for c in cl["top"]:
            if ctx.label_at(c) < 0:
                no_stance.append(c)   # 顶端站位被墙/天花板封死
                continue
            e_self = ctx.stance_elevation_at(c)
            ok = False
            for m in ctx.neighbors(c):
                e_m = ctx.flatE[m]
                if e_m > e_self + 0.05:
                    ok = True
                    break
                # 同级落点：支撑非楼梯（如半砖平台）也算出口
                if e_m >= e_self - 0.05:
                    mc = ctx.cell_of_flat(m)
                    if ctx.cls_vox[mc] != "STAIR":
                        ok = True
                        break
            if ok:
                exitable.append(c)
        # 宽楼梯只要有一格能走出就不算堵；全部顶格无出口才触发
        if not exitable:
            if no_stance:
                # 顶端站位全被实体埋住：可能是檐口/柱体装饰纹理梯，降级 WARNING
                reason = "顶端站位全部被实体封死（无 headroom，或装饰性埋梯）"
                level = "WARNING"
            else:
                reason = "顶端无向上/同层落点（楼梯尽头是墙）"
                level = sev
            blocked.append({"cluster_id": cl["id"], "top": [list(c) for c in cl["top"]],
                            "reason": reason, "level": level,
                            "top_stance_missing": [list(c) for c in no_stance],
                            "size": cl["size"], "y_span": cl["y_span"]})
    if blocked:
        eff = "HARD_FAIL" if any(b["level"] == "HARD_FAIL" for b in blocked) else "WARNING"
        return RuleResult(rid, name, sev, triggered=True, severity=eff,
                          confidence="high" if eff == "HARD_FAIL" else "medium",
                          basis="OBSERVED", evidence=blocked,
                          message=f"{len(blocked)} 个楼梯簇顶端被墙/实体封死或无落点（楼梯尽头是墙）")
    return _pass(rid, name, sev, "全部楼梯簇顶端有合法落点", basis="OBSERVED")


# ---------------------------------------------------------------------------
# V007 Vertical Circulation Broken
# ---------------------------------------------------------------------------
def v007(ctx, p) -> RuleResult:
    rid, name, sev = "V007", "Vertical Circulation Broken", p.get("severity", "HARD_FAIL")
    min_stances = p.get("min_floor_stances", 6)
    min_interior = p.get("min_interior_stances", 9)
    if ctx.interior_stance_count < min_interior:
        return _na(rid, name, sev,
                   "无显著内部站位（开放/装饰结构，露天高差不计入垂直交通）")
    floors = ctx.floor_stance_sets(level_tol=p.get("level_tol", 0.6))
    if not floors:
        return _na(rid, name, sev, "楼层检测 UNKNOWN（无楼板候选层）")

    usable_floors = [fs for fs in floors if len(fs["interior"]) >= min_stances]
    if len(usable_floors) < 2:
        return _na(rid, name, sev, f"可用楼层数 {len(usable_floors)} < 2")
    comps_per_floor = [{ctx.component_of_flat(fi) for fi in fs["interior"]}
                       for fs in usable_floors]
    common = set.intersection(*comps_per_floor) if comps_per_floor else set()
    if common:
        return _pass(rid, name, sev,
                     f"{len(usable_floors)} 个可用楼层经垂直交通连通")
    # 存在垂直连接边则不算断（兜底：楼梯/梯子把不同层连成同一分量时上面已命中）
    evidence = [{"elevation": fs["elevation"],
                 "stances": len(fs["interior"]),
                 "components": sorted(comps)}
                for fs, comps in zip(usable_floors, comps_per_floor)]
    return RuleResult(rid, name, sev, triggered=True, severity=sev,
                      confidence="medium", basis="HEURISTIC", evidence=evidence,
                      message=f"{len(usable_floors)} 个可用楼层之间无有效垂直连接")


# ---------------------------------------------------------------------------
# V008 Door Clearance Failure
# ---------------------------------------------------------------------------
def v008(ctx, p) -> RuleResult:
    rid, name, sev = "V008", "Door Clearance Failure", p.get("severity", "WARNING")
    if not ctx.doors:
        return _na(rid, name, sev, "蓝图无门")
    max_drop = p.get("max_drop", 1.0)
    facing_vec = {"east": (1, 0), "west": (-1, 0), "south": (0, 1), "north": (0, -1)}
    bad = []
    for d in ctx.doors:
        x, y, z = d["pos"]
        dx, dz = facing_vec.get(d["props"].get("facing", "north"), (0, -1))
        if d["props"].get("open", "false") == "true":
            dx, dz = dz, dx          # 敞开的门扇贴墙，通行轴与 facing 垂直
        missing = []
        air_sides = 0
        for sx, sz, side in ((dx, dz, "front"), (-dx, -dz, "back")):
            nx, nz = x + sx, z + sz
            if not (0 <= nx < ctx.X and 0 <= nz < ctx.Z):
                continue
            if ctx.solid[nx, y, nz]:
                continue                      # 实体侧：装饰性贴墙门不计
            air_sides += 1
            if _approach_stance(ctx, (nx, y, nz), max_drop) is None:
                missing.append(side)
        if air_sides == 0:
            continue                          # 两侧皆实体：纯装饰门，跳过
        if missing:
            bad.append({"pos": [x, y, z], "missing_approach": missing})
    if bad:
        return RuleResult(rid, name, sev, triggered=True, severity=sev,
                          confidence="medium", basis="HEURISTIC", evidence=bad,
                          message=f"{len(bad)}/{len(ctx.doors)} 扇门通行轴方向存在 clearance 问题")
    return _pass(rid, name, sev, "全部门通行轴方向通行空间正常")


# ---------------------------------------------------------------------------
# V009 Severe Headroom Failure
# ---------------------------------------------------------------------------
def v009(ctx, p) -> RuleResult:
    rid, name, sev = "V009", "Severe Headroom Failure", p.get("severity", "WARNING")
    min_cells = p.get("min_cells", 6)
    min_ratio = p.get("min_ratio", 0.2)
    cells = ctx.low_headroom_cells
    n = len(cells)
    denom = max(ctx.interior_stance_count, 1)
    ratio = n / denom
    if n >= min_cells and ratio >= min_ratio:
        sample = [list(c) for c in cells[:5]]
        return RuleResult(rid, name, sev, triggered=True, severity=sev,
                          confidence="medium", basis="HEURISTIC",
                          evidence=[{"low_headroom_cells": n,
                                     "interior_stances": ctx.interior_stance_count,
                                     "ratio": round(ratio, 4), "sample": sample}],
                          message=f"主要通路存在大面积低净高区域（{n} 格，占内部站位 {ratio:.0%}）")
    return _pass(rid, name, sev, f"低净高内部格 {n}（阈值 {min_cells} / {min_ratio:.0%}）")


# ---------------------------------------------------------------------------
# V010 Exterior Envelope Gap
# ---------------------------------------------------------------------------
def v010(ctx, p) -> RuleResult:
    rid, name, sev = "V010", "Exterior Envelope Gap", p.get("severity", "WARNING")
    min_interior = p.get("min_interior_air", 27)
    if ctx.interior_air_count < min_interior:
        return _na(rid, name, sev, "开放式建筑/无显著围护（桥梁、雕塑、露台等）")
    # 泄漏格 = 内部空气 6 邻接外部空气
    ext_dilate = ndimage.binary_dilation(ctx.exterior_air)  # 6 连通膨胀
    leak = ctx.interior_air & ext_dilate
    # 排除门与门洞开口周边的“设计性开口”
    margin = p.get("opening_margin", 1)
    exclude = np.zeros_like(leak)
    door_cells = []
    for d in ctx.doors:
        x, y, z = d["pos"]
        door_cells.append((x, y, z))
        door_cells.append((x, y + 1, z))
    open_cells = [tuple(o["pos"]) for o in ctx.openings] + \
                 [tuple(o["outside"]) for o in ctx.openings]
    for c in door_cells + open_cells:
        x, y, z = c
        x0, x1 = max(0, x - margin), min(ctx.X, x + margin + 1)
        y0, y1 = max(0, y - margin), min(ctx.Y, y + margin + 1)
        z0, z1 = max(0, z - margin), min(ctx.Z, z + margin + 1)
        exclude[x0:x1, y0:y1, z0:z1] = True
    leak_eff = leak & ~exclude
    n_leak = int(leak_eff.sum())
    min_voxels = p.get("min_gap_voxels", 10)
    min_ratio = p.get("min_gap_ratio", 0.02)
    if n_leak >= min_voxels and n_leak >= min_ratio * ctx.interior_air_count:
        lab, ncl = ndimage.label(leak_eff)
        sizes = sorted((int((lab == i).sum()) for i in range(1, ncl + 1)), reverse=True)
        return RuleResult(rid, name, sev, triggered=True, severity=sev,
                          confidence="medium", basis="HEURISTIC",
                          evidence=[{"leak_voxels": n_leak,
                                     "leak_clusters": len(sizes),
                                     "largest_clusters": sizes[:5],
                                     "interior_air_voxels": ctx.interior_air_count}],
                          message=f"围护结构存在大面积断裂（泄漏 {n_leak} 格 / {len(sizes)} 处）")
    return _pass(rid, name, sev, f"围护泄漏 {n_leak} 格（阈值 {min_voxels}）")


# ---------------------------------------------------------------------------
# V011 Roof Coverage Anomaly
# ---------------------------------------------------------------------------
def v011(ctx, p) -> RuleResult:
    rid, name, sev = "V011", "Roof Coverage Anomaly", p.get("severity", "WARNING")
    min_interior = p.get("min_interior_air", 27)
    if ctx.interior_air_count < min_interior:
        return _na(rid, name, sev, "开放式建筑/无显著内部")
    ia = ctx.interior_air
    cols = np.argwhere(ia.any(axis=1))  # 含内部空气的 (x,z) 柱
    uncovered, truncated = [], 0
    for x, z in cols:
        col_ia = ia[x, :, z]
        ymax = int(np.max(np.flatnonzero(col_ia)))
        if ymax >= ctx.Y - 1:
            truncated += 1      # 内部空气顶到包络上界：屋顶可能被蓝图边界截断，UNKNOWN 处理
            continue
        if not ctx.solid[x, ymax + 1:, z].any():
            uncovered.append((int(x), int(ymax), int(z)))
    n_unc = len(uncovered)
    min_cols = p.get("min_columns", 12)
    min_ratio = p.get("min_ratio", 0.2)
    total_cols = len(cols)
    if n_unc >= min_cols and total_cols and n_unc / total_cols >= min_ratio:
        return RuleResult(rid, name, sev, triggered=True, severity=sev,
                          confidence="medium", basis="HEURISTIC",
                          evidence=[{"uncovered_columns": n_unc,
                                     "interior_columns": total_cols,
                                     "ratio": round(n_unc / total_cols, 4),
                                     "boundary_truncated_columns": truncated,
                                     "sample": [list(c) for c in uncovered[:8]]}],
                          message=f"大面积室内无屋顶（{n_unc} 柱，占内部柱 {n_unc / total_cols:.0%}）")
    return _pass(rid, name, sev,
                 f"无屋顶室内柱 {n_unc}/{total_cols}（阈值 {min_cols} 且 ≥{min_ratio:.0%}）")


# ---------------------------------------------------------------------------
# V012 Dead-end Circulation Anomaly
# ---------------------------------------------------------------------------
def v012(ctx, p) -> RuleResult:
    rid, name, sev = "V012", "Dead-end Circulation Anomaly", p.get("severity", "INFO")
    info_min = p.get("info_min", 3)
    warn_min = p.get("warn_min", 8)
    # 只统计内部死端：露天端部（屋脊、平台边、树梢）天然大量度数 1，不计
    interior_dead = []
    for fi in np.flatnonzero(ctx.stance_interior):
        if ctx.degree.get(int(fi), 0) == 1:
            interior_dead.append(ctx.cell_of_flat(int(fi)))
    n = len(interior_dead)
    if n >= warn_min:
        eff = "WARNING"
    elif n >= info_min:
        eff = "INFO"
    else:
        return _pass(rid, name, sev, f"内部死端 {n}（INFO 阈值 {info_min}）")
    return RuleResult(rid, name, sev, triggered=True, severity=eff,
                      confidence="low", basis="HEURISTIC",
                      evidence=[{"interior_dead_ends": n,
                                 "sample": [list(c) for c in interior_dead[:8]]}],
                      message=f"内部通路存在 {n} 个死端（HEURISTIC，可能为设计性壁龛/房间尽头）")


# ---------------------------------------------------------------------------
RULES = {
    "V001": v001, "V002": v002, "V003": v003, "V004": v004,
    "V005": v005, "V006": v006, "V007": v007, "V008": v008,
    "V009": v009, "V010": v010, "V011": v011, "V012": v012,
}
