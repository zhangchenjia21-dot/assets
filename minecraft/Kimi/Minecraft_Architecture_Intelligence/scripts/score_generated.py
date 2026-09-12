# -*- coding: utf-8 -*-
"""score_generated — 生成样本的 rubric 机器评分（项目代号 H · P6 第二部分）。

对 generate_blueprint.py 产出的 Canonical IR 按 06_BENCHMARK/scoring_rubric.json
机器评分。口径与 08_EVALUATION/score_v4_samples.py 一致（同一 RUBRIC_DEDUCT、
同一族匹配、同一 dead_end_ratio 定义、同一封顶策略），差异仅在：

- 生成样本有机器可读 brief → S03/S04/S07、M01、E01/E02/E03、F01/F02/F03/F06
  从"未评"升级为机器可评（zone/分区/开口经由 IR metadata.generation 的生成
  方案记录定位，面积与开口存在性均用体素几何复核，不只信声明）；
- F05（公私分区）维持 LLM_ONLY/HUMAN_REVIEW——functional grammar 明确该性质
  不可从 IR 判定（INFERRED 弱代理），不伪造机器判定；
- 总分满分 100（五维全评），封顶策略不变（1/3/5 个 HARD FAIL → 40/25/10）。

targets_gap=true 的 brief：S01/S05 按 style grammar [min,max] 容忍区间判定、
S02（IQR 偏离）豁免并标注 GENERALIZATION_CASE（rubric §style_compliance note）。

所有中间值写入 record["items"] / record["features"]，全部数字可复算。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

_RUBRIC_DEDUCT = {  # scoring_rubric.json hard_validity.items
    "V001": 12, "V002": 8, "V003": 12, "V004": 6, "V005": 6, "V006": 8,
    "V007": 10, "V008": 4, "V009": 6, "V010": 6, "V011": 6, "V012": 3,
}
GRADE_BANDS = [(85, "EXCELLENT"), (70, "GOOD"), (55, "PASSABLE"), (40, "POOR"), (0, "FAIL")]

# banned_family → 判定子串（palette_dictionary 六族不含这两个子族，按 id 关键词判）
_BANNED_PATTERNS = {
    "concrete": ["concrete"],
    "terracotta_bright": ["white_terracotta", "orange_terracotta",
                          "magenta_terracotta", "light_blue_terracotta",
                          "yellow_terracotta", "lime_terracotta",
                          "pink_terracotta", "red_terracotta"],
}


def _style_rule(style_rules, style, dim):
    for r in style_rules:
        if r["class"] == style and r["dimension"] == dim:
            return r
    return None


def _family_of(block_id, families):
    for fam, spec in families.items():
        if any(pat in block_id for pat in spec["patterns"]):
            return fam
    return "UNKNOWN"


def _roof_form_classify(ir, roof_base_y):
    """几何屋顶形制分类器：统计 roof_base_y 及以上 STAIR 方块的 facing 分布。
    gable → 2 个主导方向；hip → 4 方向各 ≥15%；无楼梯 → flat/unknown。"""
    dirs = {}
    n = 0
    for x, y, z, pi in ir.blocks:
        if y < roof_base_y:
            continue
        bid = ir.block_ids[int(pi)]
        if "_stairs" not in bid:
            continue
        f = ir.properties[int(pi)].get("facing", "?")
        dirs[f] = dirs.get(f, 0) + 1
        n += 1
    if n == 0:
        return "none", dirs
    dominant = [d for d, c in dirs.items() if c / n >= 0.15]
    if len(dominant) >= 4:
        return "hip", dirs
    if len(dominant) == 2:
        return "gable", dirs
    return "irregular", dirs


def score_generated(brief: dict, ir_path, vres: dict, ctx, res: dict,
                    pipeline: str, evaluated_at: str) -> dict:
    """单条生成样本评分。ir_path 已加载；vres 为 Validator 结果；ctx 为其
    SpatialContext（复用，避免重复构建）。返回与 V4 记录同构的 dict。"""
    ir = ctx.ir
    gen = ir.raw.get("metadata", {}).get("generation", {})
    fit = ir.raw.get("metadata", {}).get("palette_fit", {})
    plan_rooms = gen.get("rooms", [])
    off = gen.get("coord_offset", [0, 0, 0])
    slab_ys = gen.get("slab_ys", [0])
    balcony = gen.get("balcony")
    style = brief["style"]
    gap = bool(brief.get("targets_gap", False))
    style_rules = res["style_rules"]
    fams = res["palette_dictionary"]["families"]
    zc = res["zone_catalog"]

    X, Y, Z = (int(v) for v in ir.dimensions)
    air_idx = ir.air_indices

    # ---- 基础特征 ----------------------------------------------------------
    non_air = 0
    fam_counts: dict[str, int] = {}
    banned_hits: dict[str, int] = {}
    for _x, _y, _z, pi in ir.blocks:
        pi = int(pi)
        if pi in air_idx:
            continue
        non_air += 1
        bid = ir.block_ids[pi]
        fam_counts[_family_of(bid, fams)] = fam_counts.get(_family_of(bid, fams), 0) + 1
        for bf in brief["palette_constraints"].get("banned_families", []):
            pats = _BANNED_PATTERNS.get(bf, [bf])
            if any(p in bid for p in pats):
                banned_hits[bf] = banned_hits.get(bf, 0) + 1
    fam_ratio = {f: round(c / non_air, 4) for f, c in sorted(fam_counts.items())}
    dominant_family = max(fam_counts, key=fam_counts.get) if fam_counts else "UNKNOWN"
    footprint_ratio = round(max(X, Z) / min(X, Z), 4)
    height_ratio = round(Y / max(X, Z), 4)
    floors_detected = vres["diagnostics"]["floor_elevations"]
    n_floors = len(floors_detected) if isinstance(floors_detected, list) else None
    dead_end_ratio = round(ctx.walk["dead_end_count"] / max(ctx.walk["walkable_voxels"], 1), 4)

    roof_base_y = gen.get("roof", {}).get("base_y", Y)
    roof_form_det, roof_facing_dist = _roof_form_classify(ir, roof_base_y)
    # 屋面高度 = 屋面（STAIR/SLAB 方块，≥roof_base_y）实际顶 − 基层；烟囱等
    # 实心突出物不计入（roof_height_ratio 的语义是屋顶体量，不是最高点）
    roof_surf_ys = [int(y) for x, y, z, pi in ir.blocks
                    if int(y) >= roof_base_y
                    and ("_stairs" in ir.block_ids[int(pi)]
                         or "_slab" in ir.block_ids[int(pi)])]
    roof_top = max(roof_surf_ys) + 1 if roof_surf_ys else roof_base_y
    roof_h = roof_top - roof_base_y
    roof_ratio = round(roof_h / Y, 4) if Y else 0.0

    # 出檐几何测量：y=2 墙环 bbox vs 屋盖基层（roof_base_y）bbox
    wall_cells = [(int(x), int(z)) for x, y, z, pi in ir.blocks if int(y) == 2]
    roof_cells = [(int(x), int(z)) for x, y, z, pi in ir.blocks if int(y) == roof_base_y]
    overhang = None
    if wall_cells and roof_cells:
        wx0 = min(c[0] for c in wall_cells); wx1 = max(c[0] for c in wall_cells)
        wz0 = min(c[1] for c in wall_cells); wz1 = max(c[1] for c in wall_cells)
        rx0 = min(c[0] for c in roof_cells); rx1 = max(c[0] for c in roof_cells)
        rz0 = min(c[1] for c in roof_cells); rz1 = max(c[1] for c in roof_cells)
        overhang = min(wx0 - rx0, rx1 - wx1, wz0 - rz0, rz1 - wz1)

    items: list[dict] = []

    # ---- hard_validity（40，全机器，Validator 驱动，与 V4 同口径） ------------
    triggered = {r["rule_id"]: r for r in vres["rules"] if r["triggered"]}
    hard_ded = 0
    for rid, ded in _RUBRIC_DEDUCT.items():
        if rid in triggered:
            hard_ded += ded
            items.append({"id": rid, "dimension": "hard_validity", "status": "SCORED",
                          "max_deduct": ded, "deduct_applied": ded,
                          "evidence": {"validator_severity": triggered[rid]["severity"],
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

    # ---- functional_layout（25） ---------------------------------------------
    # zone 净面积：房间矩形（生成方案记录 + coord_offset 对齐 IR 坐标）内、
    # 该层楼板高程 ±0.6 的（内部）站位计数——纯几何复核。
    stance_flat = np.flatnonzero(ctx.stance_mask)
    st_coords = [ctx.cell_of_flat(int(fi)) for fi in stance_flat]
    st_E = ctx.flatE[stance_flat]
    st_int = ctx.stance_interior.ravel()[stance_flat]

    def zone_area(room):
        fi = room["floor"]
        e0 = slab_ys[fi] + 1 if fi < len(slab_ys) else None
        if e0 is None:
            return 0
        x0, z0, x1, z1 = room["rect"]
        x0 -= off[0]; z0 -= off[2]; x1 -= off[0]; z1 -= off[2]
        want_interior = not zc.get(room["zone"], {}).get("exterior", False)
        n = 0
        for (cx, cy, cz), e, is_int in zip(st_coords, st_E, st_int):
            if abs(float(e) - e0) <= 0.6 and x0 <= cx <= x1 and z0 <= cz <= z1:
                if bool(is_int) == want_interior:
                    n += 1
        return n

    room_by_zone = {r["zone"]: r for r in plan_rooms}
    f01 = f06 = 0
    zone_area_detail = {}
    for z in brief["required_zones"]:
        room = room_by_zone.get(z)
        if room is None:
            # 外部 zone 无房间记录 → 由 balcony 实现兜底判定（缺区扣 4）
            f01 += 4
            zone_area_detail[z] = {"status": "missing_room"}
            continue
        area = zone_area(room)
        zone_area_detail[z] = {"area": area, "min_area": zc[z]["min_area"],
                               "rect": room["rect"], "floor": room["floor"]}
        if area == 0:
            f01 += 4
        if area < zc[z]["min_area"]:
            f06 += 2
    f01 = min(f01, 12)
    f06 = min(f06, 6)
    items.append({"id": "F01", "dimension": "functional_layout", "status": "SCORED",
                  "max_deduct": 12, "deduct_applied": f01,
                  "evidence": {"zones": zone_area_detail},
                  "formula": "每缺 1 个 required_zone（无房间记录或净站位面积=0）扣 4，上限 12；"
                             "面积=房间矩形内该层楼板高程±0.6 的（内/外部）站位数"})
    items.append({"id": "F06", "dimension": "functional_layout", "status": "SCORED",
                  "max_deduct": 6, "deduct_applied": f06,
                  "evidence": {"zones": zone_area_detail},
                  "formula": "zone 净使用面积 < zone_catalog min_area，每个扣 2，上限 6"})

    # 邻接：同层相邻带且共用隔墙上存在实际开口（几何复核：开口格为空气×2 高），
    # 或塔室↔露台经 terrace_opening。
    cells_set = {(int(x), int(y), int(z)): int(pi) for x, y, z, pi in ir.blocks}

    def opening_exists(ra, rb, fi):
        sy = slab_ys[fi] + off[1]
        ax0, az0, ax1, az1 = [ra[0] - off[0], ra[1] - off[2], ra[2] - off[0], ra[3] - off[2]]
        bx0, bz0, bx1, bz1 = [rb[0] - off[0], rb[1] - off[2], rb[2] - off[0], rb[3] - off[2]]

        # 两 rect 之间夹着隔墙线：扫描两 rect 最近边之间的中间格，
        # 若某柱在 (sy+1, sy+2) 两格皆可通行（空气或薄片类：地毯/压力板/灯笼）
        # → 存在实际可通行开口。口径与 walkability 一致（薄片不挡路）。
        passable_pat = ("carpet", "pressure_plate", "lantern")

        def scan(x, z):
            ok = True
            for yy in (sy + 1, sy + 2):
                pi_ = cells_set.get((x, yy, z))
                if pi_ is None:
                    continue
                if not any(p in ir.block_ids[pi_] for p in passable_pat):
                    ok = False
                    break
            return ok

        if ax1 < bx0:  # a 左 b 右，墙线应在 ax1+1..bx0-1
            for x in range(ax1 + 1, bx0):
                for z in range(max(az0, bz0), min(az1, bz1) + 1):
                    if scan(x, z):
                        return True
        if bx1 < ax0:
            for x in range(bx1 + 1, ax0):
                for z in range(max(az0, bz0), min(az1, bz1) + 1):
                    if scan(x, z):
                        return True
        if az1 < bz0:
            for z in range(az1 + 1, bz0):
                for x in range(max(ax0, bx0), min(ax1, bx1) + 1):
                    if scan(x, z):
                        return True
        if bz1 < az0:
            for z in range(bz1 + 1, az0):
                for x in range(max(ax0, bx0), min(ax1, bx1) + 1):
                    if scan(x, z):
                        return True
        return False

    f02 = f03 = 0
    adj_detail = []
    forbidden = {tuple(sorted(p)) for p in brief.get("forbidden_adjacencies", [])}
    for a, b_ in brief.get("required_adjacencies", []):
        ra, rb = room_by_zone.get(a), room_by_zone.get(b_)
        ok = False
        note = ""
        if ra and rb and ra["floor"] == rb["floor"]:
            ok = opening_exists(ra["rect"], rb["rect"], ra["floor"])
            note = "same_floor"
        elif ra and rb:
            note = "different_floors"
        # 房间↔阳台（外部 zone）：几何扫描——阳台门格存在 DOOR 块且朝向外侧
        if not ok and balcony and (a == balcony["zone"] or b_ == balcony["zone"]):
            bfi = balcony["floor"]
            bsy = slab_ys[bfi] + off[1]
            dx_, dz_ = balcony["door_at"][0] - off[0], balcony["door_at"][1] - off[2]
            pi_ = cells_set.get((dx_, bsy + 1, dz_))
            ok = pi_ is not None and "_door" in ir.block_ids[pi_]
            note = note or "balcony_door_scan"
        if not ok:
            f02 += 3
        adj_detail.append({"pair": [a, b_], "satisfied": ok, "note": note})
    f02 = min(f02, 8)
    items.append({"id": "F02", "dimension": "functional_layout", "status": "SCORED",
                  "max_deduct": 8, "deduct_applied": f02,
                  "evidence": {"adjacencies": adj_detail},
                  "formula": "required_adjacency 不满足每对扣 3（上限 8）；满足=同层相邻带间"
                             "存在实际 1×2 开口（几何扫描空气格）或房间↔阳台门存在"})
    fb_detail = []
    for a, b_ in brief.get("forbidden_adjacencies", []):
        ra, rb = room_by_zone.get(a), room_by_zone.get(b_)
        violated = False
        if ra and rb and ra["floor"] == rb["floor"]:
            violated = opening_exists(ra["rect"], rb["rect"], ra["floor"])
        if violated:
            f03 += 4
        fb_detail.append({"pair": [a, b_], "violated": violated})
    f03 = min(f03, 8)
    items.append({"id": "F03", "dimension": "functional_layout", "status": "SCORED",
                  "max_deduct": 8, "deduct_applied": f03,
                  "evidence": {"forbidden": fb_detail},
                  "formula": "forbidden_adjacency 出现每对扣 4（上限 8）；出现=两 zone 房间"
                             "同层且存在直接开口"})
    f04 = 3 if dead_end_ratio > 0.20 else 0
    items.append({"id": "F04", "dimension": "functional_layout", "status": "SCORED",
                  "max_deduct": 3, "deduct_applied": f04,
                  "evidence": {"dead_end_ratio": dead_end_ratio,
                               "dead_end_count": ctx.walk["dead_end_count"],
                               "walkable_voxels": ctx.walk["walkable_voxels"]},
                  "formula": "dead_end_ratio = dead_end_count/walkable_voxels；> 0.20 → 扣 3"})
    items.append({"id": "F05", "dimension": "functional_layout",
                  "status": "LLM_ONLY/HUMAN_REVIEW", "max_deduct": None,
                  "deduct_applied": 0,
                  "evidence": {"grammar_basis": "functional_rules zone_semantics: "
                                              "公私分区不可从 IR 直接判定（INFERRED 弱代理）"},
                  "formula": "本报告不评该子项：IR 不可判定，交由 LLM/人工"})
    func_ded = min(f01 + f02 + f03 + f04 + f06, 25)
    func_score = 25 - func_ded

    # ---- style_compliance（20） -----------------------------------------------
    fr_rule = _style_rule(style_rules, style, "footprint_ratio")
    s01 = s02 = 0
    gen_note = "GENERALIZATION_CASE（targets_gap=true）：S01 按 [min,max] 判定，S02 豁免" if gap else ""
    if fr_rule:
        if not (fr_rule["min"] <= footprint_ratio <= fr_rule["max"]):
            s01 = 5
        elif not gap and not (fr_rule["p25"] <= footprint_ratio <= fr_rule["p75"]):
            s02 = 3
    items.append({"id": "S01", "dimension": "style_compliance", "status": "SCORED",
                  "max_deduct": 5, "deduct_applied": s01,
                  "evidence": {"footprint_ratio": footprint_ratio,
                               "grammar": f"STYLE.{style}.footprint_ratio",
                               "min": fr_rule["min"] if fr_rule else None,
                               "max": fr_rule["max"] if fr_rule else None,
                               "note": gen_note},
                  "formula": f"max(x,z)/min(x,z)=max({X},{Z})/min({X},{Z})={footprint_ratio}"})
    items.append({"id": "S02", "dimension": "style_compliance",
                  "status": "EXEMPT/GENERALIZATION_CASE" if gap else "SCORED",
                  "max_deduct": 3, "deduct_applied": s02,
                  "evidence": {"footprint_ratio": footprint_ratio,
                               "p25": fr_rule["p25"] if fr_rule else None,
                               "p75": fr_rule["p75"] if fr_rule else None},
                  "formula": "容忍区间内但超出 IQR 扣 3" + ("；gap 豁免" if gap else "")})
    # S03 屋顶形式：几何分类器（屋面 STAIR facing 分布）
    want_form = brief["roof_constraints"].get("form", "any")
    want_base = {"curved_gable": "gable", "curved_hip": "hip"}.get(want_form, want_form)
    s03 = 0
    if want_base not in ("any",) and roof_form_det != want_base:
        s03 = 5
    items.append({"id": "S03", "dimension": "style_compliance", "status": "SCORED",
                  "max_deduct": 5, "deduct_applied": s03,
                  "evidence": {"roof_form_required": want_form,
                               "roof_form_detected": roof_form_det,
                               "facing_distribution": roof_facing_dist,
                               "classifier": "屋面 STAIR facing 分布：2 主导方向=gable，"
                                             "4 方向各≥15%=hip；curved_* 按基形判定"},
                  "formula": f"要求 {want_form}（基形 {want_base}）vs 检测 {roof_form_det}；不符扣 5"})
    lo_r, hi_r = brief["roof_constraints"].get("height_ratio_range", [0, 1])
    s04 = 0 if (lo_r - 1e-9 <= roof_ratio <= hi_r + 1e-9) else 3
    items.append({"id": "S04", "dimension": "style_compliance", "status": "SCORED",
                  "max_deduct": 3, "deduct_applied": s04,
                  "evidence": {"roof_height_ratio": roof_ratio, "range": [lo_r, hi_r],
                               "roof_h": roof_h, "envelope_y": Y,
                               "basis": "INFERRED：roof_base_y 取生成方案记录（几何代理 UNKNOWN）"},
                  "formula": f"roof_h/Y = {roof_h}/{Y} = {roof_ratio} ∈ [{lo_r},{hi_r}]？否则扣 3"})
    hr_rule = _style_rule(style_rules, style, "height_ratio")
    s05 = 0
    if hr_rule and not (hr_rule["min"] <= height_ratio <= hr_rule["max"]):
        s05 = 3
    items.append({"id": "S05", "dimension": "style_compliance", "status": "SCORED",
                  "max_deduct": 3, "deduct_applied": s05,
                  "evidence": {"height_ratio": height_ratio,
                               "grammar": f"STYLE.{style}.height_ratio",
                               "min": hr_rule["min"] if hr_rule else None,
                               "max": hr_rule["max"] if hr_rule else None,
                               "note": gen_note},
                  "formula": f"size_y/max(x,z) = {Y}/max({X},{Z}) = {height_ratio}"})
    s06 = 0
    s06_status = "SCORED"
    if n_floors is None:
        s06_status = "LLM_ONLY/HUMAN_REVIEW"
    elif n_floors != brief["required_floors"]:
        s06 = 3
    items.append({"id": "S06", "dimension": "style_compliance", "status": s06_status,
                  "max_deduct": 3, "deduct_applied": s06,
                  "evidence": {"floor_elevations": floors_detected,
                               "detected_floors": n_floors,
                               "required_floors": brief["required_floors"],
                               "caveat": "楼板密度启发式（density≥0.30），已知会把密实屋顶/"
                                         "夹层误检为楼板"},
                  "formula": f"检测楼层 {n_floors} vs required {brief['required_floors']}"})
    omin = brief["roof_constraints"].get("overhang_min", 0)
    s07 = 0
    if omin > 0 and (overhang is None or overhang < omin):
        s07 = 2
    items.append({"id": "S07", "dimension": "style_compliance", "status": "SCORED",
                  "max_deduct": 2, "deduct_applied": s07,
                  "evidence": {"overhang_measured": overhang, "overhang_min": omin,
                               "measurement": "y=2 墙环 bbox 与屋面基层 bbox 各边差的最小值"},
                  "formula": f"出檐 {overhang} ≥ {omin}？否则扣 2"})
    style_ded = min(s01 + s02 + s03 + s04 + s05 + s06 + s07, 20)
    style_score = 20 - style_ded

    # ---- material_coherence（10） ----------------------------------------------
    m01 = 0
    for bf, cnt in banned_hits.items():
        m01 += 4
    m01 = min(m01, 8)
    items.append({"id": "M01", "dimension": "material_coherence", "status": "SCORED",
                  "max_deduct": 8, "deduct_applied": m01,
                  "evidence": {"banned_hits": banned_hits,
                               "pattern_map": _BANNED_PATTERNS},
                  "formula": "每出现 1 个 banned_family 扣 4（上限 8）；按 block_id 关键词判定"})
    m02 = 0
    m02_detail = {}
    for fam, (lo, hi) in brief["palette_constraints"].get("family_ratio_ranges", {}).items():
        rv = fam_ratio.get(fam, 0.0)
        out = rv < lo - 1e-9 or rv > hi + 1e-9
        if out:
            m02 += 2
        m02_detail[fam] = {"ratio": rv, "range": [lo, hi], "out": out}
    m02 = min(m02, 6)
    items.append({"id": "M02", "dimension": "material_coherence", "status": "SCORED",
                  "max_deduct": 6, "deduct_applied": m02,
                  "evidence": {"family_ratios": fam_ratio, "checks": m02_detail,
                               "ratio_base": "non_air_blocks",
                               "palette_fit": fit},
                  "formula": "族占比 = 族体素数/非空气体素数；每族超 brief 区间扣 2，上限 6"})
    dom_families = brief["palette_constraints"].get("dominant_families", [])
    m03 = 0 if dominant_family in dom_families else 2
    items.append({"id": "M03", "dimension": "material_coherence", "status": "SCORED",
                  "max_deduct": 2, "deduct_applied": m03,
                  "evidence": {"dominant_family": dominant_family,
                               "dominant_families": dom_families},
                  "formula": f"主导族 {dominant_family} ∈ {dom_families}？否则扣 2"})
    mat_ded = min(m01 + m02 + m03, 10)
    mat_score = 10 - mat_ded

    # ---- efficiency（5，生成样本全部机器可评） ----------------------------------
    W, D, H = brief["plot_width"], brief["plot_depth"], brief["max_height"]
    e01 = 2 if non_air > W * D * H * 0.35 else 0
    items.append({"id": "E01", "dimension": "efficiency", "status": "SCORED",
                  "max_deduct": 2, "deduct_applied": e01,
                  "evidence": {"non_air": non_air,
                               "threshold": round(W * D * H * 0.35, 1)},
                  "formula": f"non_air {non_air} > plot×H×0.35 = {W}×{D}×{H}×0.35？扣 2"})
    e02 = 1 if Y < 0.6 * H else 0
    items.append({"id": "E02", "dimension": "efficiency", "status": "SCORED",
                  "max_deduct": 1, "deduct_applied": e02,
                  "evidence": {"height": Y, "max_height": H},
                  "formula": f"实际高 {Y} < 0.6×{H}？扣 1（限高浪费）"})
    proj = X * Z / (W * D)
    e03 = 0 if (0.3 - 1e-9 <= proj <= 0.9 + 1e-9) else 2
    items.append({"id": "E03", "dimension": "efficiency", "status": "SCORED",
                  "max_deduct": 2, "deduct_applied": e03,
                  "evidence": {"projection_ratio": round(proj, 4)},
                  "formula": f"投影 {X}×{Z}/{W}×{D} = {proj:.3f} ∈ [0.3,0.9]？否则扣 2"})
    eff_ded = min(e01 + e02 + e03, 5)
    eff_score = 5 - eff_ded

    # ---- 合计与封顶（rubric hard_fail_policy） -----------------------------------
    total = hard_score + func_score + style_score + mat_score + eff_score
    hf = vres["hard_fail_count"]
    cap = 10 if hf >= 5 else 25 if hf >= 3 else 40 if hf >= 1 else 100
    total_capped = min(total, cap)
    grade = next(label for lo, label in GRADE_BANDS if total_capped >= lo)
    excluded = [i["id"] for i in items if i["status"] not in ("SCORED",)]

    return {
        "evaluated_at": evaluated_at,
        "features": {"dimensions": {"x": X, "y": Y, "z": Z},
                     "non_air_blocks": non_air,
                     "footprint_ratio": footprint_ratio,
                     "height_ratio": height_ratio,
                     "floors_detected": floors_detected,
                     "dead_end_ratio": dead_end_ratio,
                     "family_ratios": fam_ratio,
                     "dominant_family": dominant_family,
                     "roof_form_detected": roof_form_det,
                     "roof_height_ratio": roof_ratio,
                     "roof_overhang": overhang,
                     "zone_areas": zone_area_detail},
        "scores": {"hard_validity": {"weight": 40, "deducted": hard_ded, "score": hard_score},
                   "functional_layout": {"weight": 25, "deducted": func_ded, "score": func_score,
                                         "note": "F01/F02/F03/F04/F06 机器评（几何复核）；"
                                                 "F05 维持 LLM_ONLY（grammar 声明 IR 不可判）"},
                   "style_compliance": {"weight": 20, "deducted": style_ded, "score": style_score,
                                        "note": "S01–S07 全机器评；S03 屋面 facing 分类器，"
                                                "S04 roof_base_y 取生成方案记录（INFERRED 代理）"},
                   "material_coherence": {"weight": 10, "deducted": mat_ded, "score": mat_score,
                                          "note": "M01/M02/M03 全机器评"},
                   "efficiency": {"weight": 5, "deducted": eff_ded, "score": eff_score,
                                  "note": "E01/E02/E03 机器评（brief 约束机器可读）"}},
        "total_upper_bound_max100": total,
        "hard_fail_count": hf,
        "hard_fail_cap": cap,
        "total_capped_max100": total_capped,
        "grade": grade,
        "excluded_items": excluded,
        "total_formula": "total = Σ五维（满分 100）；capped = min(total, cap(hard_fail_count))，"
                         "cap: 1→40 / ≥3→25 / ≥5→10；未评子项按 0 扣分（仅 F05）",
        "items": items,
    }
