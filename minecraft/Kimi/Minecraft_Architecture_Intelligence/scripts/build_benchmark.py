#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_benchmark.py — P4 Design Brief Benchmark 生成器（项目代号 H）

生成 06_BENCHMARK/design_briefs.jsonl（100 条）、zone_catalog.json、
coverage_stats.json、benchmark_split.json。

设计原则：
- 一切数值锚定真实库产物（style_rules.json / functional_rules.json /
  data_gap_matrix.json / blueprint_metadata.jsonl），不发明离谱数值；
- 约束内部自洽：required_floors × 层高 + 屋顶余量 ≤ max_height；
  required_zones 最小面积之和 ≤ 可用面积（脚本内置断言）；
- targets_gap=True 的 brief 对应 data_gap_matrix 中 priority==P0 的缺口组合，
  用于测试 Architect 在缺样本组合上的泛化；
- 确定性：固定随机种子，可复跑产出完全一致。

用法：
    py build_benchmark.py --root "D:\\...\\Minecraft_Architecture_Intelligence"
"""
import argparse
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

VERSION = "P4-1.0"
SEED = 42

# ---------------------------------------------------------------------------
# 风格参数：数值取自 04_GRAMMARS/style_rules.json 的 p25/p75（OBSERVED/HEURISTIC）
# fh = 假定层高（含楼板），参考 Rustic floor_height med 6.0 (3-12)、Japanese med 8。
# 此处取保守值 5~6：Minecraft 净高 3 + 楼板 1 + 余量。
# ---------------------------------------------------------------------------
STYLE_PARAMS = {
    "Medieval": {
        "fh": 5, "roof_form": "gable",
        "roof_ratio": [0.05, 0.25], "overhang_min": 1,
        "footprint_ratio": [1.05, 1.23],   # STYLE.Medieval.footprint_ratio p25/p75
        "palette_ranges": {"stone": [0.35, 0.65], "wood": [0.10, 0.25], "glass": [0.0, 0.03]},
        "dominant_families": ["stone", "wood"],
        "banned_families": ["concrete", "terracotta_bright"],
    },
    "Rustic": {
        "fh": 5, "roof_form": "gable",
        "roof_ratio": [0.05, 0.20], "overhang_min": 1,
        "footprint_ratio": [1.10, 1.40],   # STYLE.Rustic.footprint_ratio p25/p75
        "palette_ranges": {"wood": [0.15, 0.32], "stone": [0.25, 0.48], "glass": [0.0, 0.03], "decorative": [0.03, 0.12]},
        "dominant_families": ["wood", "stone"],
        "banned_families": ["concrete"],
    },
    "Fantasy": {
        "fh": 6, "roof_form": "any",
        "roof_ratio": [0.0, 0.25], "overhang_min": 0,
        "footprint_ratio": [1.00, 1.53],   # STYLE.Fantasy.footprint_ratio p25/p75
        "palette_ranges": {"stone": [0.45, 0.78], "decorative": [0.04, 0.16], "wood": [0.02, 0.18]},
        "dominant_families": ["stone", "decorative"],
        "banned_families": [],
    },
    "Japanese": {
        "fh": 6, "roof_form": "curved_gable",
        "roof_ratio": [0.09, 0.30], "overhang_min": 2,
        "footprint_ratio": [1.06, 2.10],   # STYLE.Japanese.footprint_ratio p25/p75
        "palette_ranges": {"wood": [0.20, 0.32], "stone": [0.25, 0.65], "glass": [0.0, 0.01]},
        "dominant_families": ["wood", "stone"],
        "banned_families": ["concrete"],
    },
    "Chinese": {
        "fh": 5, "roof_form": "curved_hip",
        "roof_ratio": [0.11, 0.35], "overhang_min": 2,
        "footprint_ratio": [1.04, 1.29],   # STYLE.Chinese.footprint_ratio p25/p75
        "palette_ranges": {"wood": [0.17, 0.24], "stone": [0.45, 0.65], "glass": [0.0, 0.02]},
        "dominant_families": ["wood", "stone"],
        "banned_families": ["concrete"],
    },
}

# ---------------------------------------------------------------------------
# Zone 目录：min_area 为最小净使用面积（方块数），exterior=True 占用地皮但不占建筑包络
# 落地为 06_BENCHMARK/zone_catalog.json，供 Validator/Architect 复用
# ---------------------------------------------------------------------------
ZONE_CATALOG = {
    # interior
    "living_hall":     {"min_area": 20, "exterior": False},
    "bedroom":         {"min_area": 12, "exterior": False},
    "kitchen":         {"min_area": 12, "exterior": False},
    "storage":         {"min_area": 9,  "exterior": False},
    "cellar":          {"min_area": 9,  "exterior": False},
    "study":           {"min_area": 9,  "exterior": False},
    "workshop_floor":  {"min_area": 16, "exterior": False},
    "forge":           {"min_area": 16, "exterior": False},
    "shop_front":      {"min_area": 12, "exterior": False},
    "living_quarters": {"min_area": 12, "exterior": False},
    "office":          {"min_area": 9,  "exterior": False},
    "storage_hall":    {"min_area": 25, "exterior": False},
    "barn":            {"min_area": 20, "exterior": False},
    "common_room":     {"min_area": 24, "exterior": False},
    "guest_room":      {"min_area": 12, "exterior": False},
    "stable":          {"min_area": 16, "exterior": False},
    "great_hall":      {"min_area": 30, "exterior": False},
    "archive":         {"min_area": 12, "exterior": False},
    "meeting_room":    {"min_area": 12, "exterior": False},
    "chapel":          {"min_area": 25, "exterior": False},
    "shrine":          {"min_area": 9,  "exterior": False},
    "scriptorium":     {"min_area": 12, "exterior": False},
    "bell_tower_core": {"min_area": 9,  "exterior": False},
    "keep":            {"min_area": 25, "exterior": False},
    "armory":          {"min_area": 12, "exterior": False},
    "gate_passage":    {"min_area": 8,  "exterior": False},
    "guard_room":      {"min_area": 9,  "exterior": False},
    "tower_core":      {"min_area": 9,  "exterior": False},
    "farmhouse":       {"min_area": 16, "exterior": False},
    "silo":            {"min_area": 9,  "exterior": False},
    "crypt":           {"min_area": 9,  "exterior": False},
    # exterior（占 plot 不计包络容量）
    "courtyard":       {"min_area": 16, "exterior": True},
    "balcony":         {"min_area": 6,  "exterior": True},
    "field":           {"min_area": 30, "exterior": True},
    "yard":            {"min_area": 12, "exterior": True},
    "loading_dock":    {"min_area": 12, "exterior": True},
    "cloister":        {"min_area": 12, "exterior": True},
    "wall_walk":       {"min_area": 8,  "exterior": True},
    "watch_platform":  {"min_area": 9,  "exterior": True},
    "sign_post":       {"min_area": 4,  "exterior": True},
}

# ---------------------------------------------------------------------------
# 功能模板：按难度给出 zones / 邻接 / 楼层 / plot 档位
# plot_band: small(9-15) / medium(16-30) / large(31-60) / xlarge(61-100)
# ---------------------------------------------------------------------------
T = {
    "Residential": {
        "domain": "Residential",
        "Easy":   dict(floors=(1, 1), band=["small", "medium"],
                       req=["living_hall", "bedroom"], opt=["kitchen", "storage"],
                       adj=[], forb=[], features=["chimney"]),
        "Medium": dict(floors=(2, 2), band=["small", "medium"],
                       req=["living_hall", "bedroom", "kitchen"], opt=["storage", "cellar", "balcony"],
                       adj=[["living_hall", "kitchen"]], forb=[], features=["chimney", "flower_boxes"]),
        "Hard":   dict(floors=(2, 3), band=["medium", "large"],
                       req=["living_hall", "bedroom", "kitchen", "study", "cellar"],
                       opt=["storage", "balcony"],
                       adj=[["living_hall", "kitchen"], ["bedroom", "study"]],
                       forb=[["kitchen", "bedroom"]], features=["chimney", "bay_window", "dormer"]),
    },
    "Mixed-use": {
        "domain": "Mixed-use",
        "Easy":   dict(floors=(1, 2), band=["small", "medium"],
                       req=["shop_front", "living_quarters"], opt=["storage"],
                       adj=[], forb=[], features=["awning"]),
        "Medium": dict(floors=(2, 2), band=["medium"],
                       req=["shop_front", "living_quarters", "storage"], opt=["workshop_floor", "yard"],
                       adj=[["shop_front", "storage"]], forb=[], features=["awning", "sign_post"]),
        "Hard":   dict(floors=(2, 3), band=["medium", "large"],
                       req=["shop_front", "workshop_floor", "living_quarters", "storage", "cellar"],
                       opt=["yard"],
                       adj=[["shop_front", "workshop_floor"], ["workshop_floor", "storage"]],
                       forb=[["workshop_floor", "living_quarters"]],
                       features=["awning", "sign_post", "display_window"]),
    },
    "Workshop": {
        "domain": "Workshop",
        "Easy":   dict(floors=(1, 1), band=["small", "medium"],
                       req=["workshop_floor", "storage"], opt=["yard"],
                       adj=[["workshop_floor", "storage"]], forb=[], features=["workbench_cluster"]),
        "Medium": dict(floors=(1, 2), band=["medium"],
                       req=["workshop_floor", "storage", "living_quarters"],
                       opt=["yard", "cellar"],
                       adj=[["workshop_floor", "storage"]], forb=[],
                       features=["workbench_cluster", "chimney"]),
        "Hard":   dict(floors=(2, 2), band=["medium", "large"],
                       req=["workshop_floor", "forge", "storage", "living_quarters", "office"],
                       opt=["yard"],
                       adj=[["workshop_floor", "forge"], ["workshop_floor", "storage"]],
                       forb=[["forge", "living_quarters"]],
                       features=["chimney", "crane", "workbench_cluster"]),
    },
    "Blacksmith": {
        "domain": "Workshop",
        "Easy":   dict(floors=(1, 1), band=["small"],
                       req=["forge", "storage"], opt=["yard"],
                       adj=[["forge", "storage"]], forb=[], features=["chimney", "water_trough"]),
        "Medium": dict(floors=(1, 2), band=["small", "medium"],
                       req=["forge", "storage", "living_quarters"], opt=["yard"],
                       adj=[["forge", "storage"]], forb=[["forge", "living_quarters"]],
                       features=["chimney", "water_trough", "anvil_station"]),
        "Hard":   dict(floors=(2, 2), band=["medium"],
                       req=["forge", "storage", "living_quarters", "office"], opt=["yard"],
                       adj=[["forge", "storage"]], forb=[["forge", "living_quarters"]],
                       features=["chimney", "water_trough", "anvil_station"]),
    },
    "Warehouse": {
        "domain": "Workshop",
        "Easy":   dict(floors=(1, 1), band=["medium"],
                       req=["storage_hall"], opt=["loading_dock"],
                       adj=[], forb=[], features=["hoist"]),
        "Medium": dict(floors=(1, 2), band=["medium", "large"],
                       req=["storage_hall", "office"], opt=["loading_dock", "cellar"],
                       adj=[["storage_hall", "office"]], forb=[], features=["hoist", "wide_door"]),
        "Hard":   dict(floors=(2, 3), band=["large"],
                       req=["storage_hall", "office", "cellar"], opt=["loading_dock"],
                       adj=[["storage_hall", "office"]], forb=[["cellar", "office"]],
                       features=["hoist", "wide_door", "crane"]),
    },
    "Farm": {
        "domain": "Workshop",   # 基准域映射：Farm 归入 Workshop（生产-仓储域），见 BENCHMARK_SPEC
        "Easy":   dict(floors=(1, 1), band=["medium", "large"],
                       req=["farmhouse", "field"], opt=["barn"],
                       adj=[], forb=[], features=["fence_line"]),
        "Medium": dict(floors=(1, 2), band=["large"],
                       req=["farmhouse", "barn", "field"], opt=["stable", "silo"],
                       adj=[["farmhouse", "barn"]], forb=[], features=["fence_line", "well"]),
        "Hard":   dict(floors=(2, 2), band=["large"],
                       req=["farmhouse", "barn", "field", "stable", "silo"], opt=["cellar"],
                       adj=[["farmhouse", "barn"], ["barn", "stable"]], forb=[["stable", "farmhouse"]],
                       features=["fence_line", "well", "windmill"]),
    },
    "Inn": {
        "domain": "Hospitality",
        "Easy":   dict(floors=(1, 2), band=["small", "medium"],
                       req=["common_room", "guest_room"], opt=["kitchen"],
                       adj=[], forb=[], features=["sign_post"]),
        "Medium": dict(floors=(2, 2), band=["medium"],
                       req=["common_room", "kitchen", "guest_room"], opt=["cellar", "balcony"],
                       adj=[["common_room", "kitchen"]], forb=[["kitchen", "guest_room"]],
                       features=["sign_post", "chimney"]),
        "Hard":   dict(floors=(2, 3), band=["medium", "large"],
                       req=["common_room", "kitchen", "guest_room", "cellar", "stable"],
                       opt=["balcony", "yard"],
                       adj=[["common_room", "kitchen"], ["common_room", "guest_room"]],
                       forb=[["stable", "guest_room"], ["kitchen", "guest_room"]],
                       features=["sign_post", "chimney", "brewery_corner"]),
    },
    "Civic": {
        "domain": "Civic",
        "Easy":   dict(floors=(1, 1), band=["medium"],
                       req=["great_hall"], opt=["office"],
                       adj=[], forb=[], features=["banner"]),
        "Medium": dict(floors=(2, 2), band=["medium", "large"],
                       req=["great_hall", "office", "archive"], opt=["courtyard"],
                       adj=[["great_hall", "office"]], forb=[], features=["banner", "bell"]),
        "Hard":   dict(floors=(2, 3), band=["large"],
                       req=["great_hall", "office", "archive", "meeting_room"],
                       opt=["courtyard", "bell_tower_core"],
                       adj=[["great_hall", "meeting_room"], ["office", "archive"]],
                       forb=[["archive", "great_hall"]],
                       features=["banner", "bell", "colonnade"]),
    },
    "Religious": {
        "domain": "Civic",
        "Easy":   dict(floors=(1, 1), band=["small", "medium"],
                       req=["chapel"], opt=["shrine"],
                       adj=[], forb=[], features=["stained_glass"]),
        "Medium": dict(floors=(1, 2), band=["medium"],
                       req=["chapel", "shrine"], opt=["scriptorium", "cloister"],
                       adj=[["chapel", "shrine"]], forb=[], features=["stained_glass", "bell"]),
        "Hard":   dict(floors=(2, 3), band=["large"],
                       req=["chapel", "scriptorium", "bell_tower_core"],
                       opt=["cloister", "crypt"],
                       adj=[["chapel", "bell_tower_core"]], forb=[["crypt", "chapel"]],
                       features=["stained_glass", "bell", "rose_window"]),
    },
    "Castle": {
        "domain": "Defensive",
        "Easy":   dict(floors=(2, 2), band=["large"],
                       req=["keep", "courtyard", "gate_passage"], opt=["wall_walk"],
                       adj=[["gate_passage", "courtyard"], ["keep", "courtyard"]],
                       forb=[], features=["battlements"]),
        "Medium": dict(floors=(2, 3), band=["large", "xlarge"],
                       req=["keep", "courtyard", "gate_passage", "wall_walk"],
                       opt=["armory", "stable"],
                       adj=[["gate_passage", "courtyard"], ["keep", "courtyard"], ["wall_walk", "gate_passage"]],
                       forb=[["stable", "keep"]], features=["battlements", "portcullis"]),
        "Hard":   dict(floors=(3, 4), band=["xlarge"],
                       req=["keep", "great_hall", "courtyard", "gate_passage", "wall_walk", "armory"],
                       opt=["chapel", "stable"],
                       adj=[["gate_passage", "courtyard"], ["keep", "courtyard"],
                            ["great_hall", "keep"], ["wall_walk", "gate_passage"]],
                       forb=[["stable", "great_hall"]],
                       features=["battlements", "portcullis", "drawbridge", "murder_holes"]),
    },
    "Tower": {
        "domain": "Defensive",
        "Easy":   dict(floors=(2, 3), band=["small"],
                       req=["tower_core", "watch_platform"], opt=["guard_room"],
                       adj=[["tower_core", "watch_platform"]], forb=[], features=["crenellation"]),
        "Medium": dict(floors=(3, 4), band=["small"],
                       req=["tower_core", "watch_platform", "guard_room"], opt=["armory"],
                       adj=[["tower_core", "watch_platform"], ["tower_core", "guard_room"]],
                       forb=[], features=["crenellation", "arrow_slits"]),
        "Hard":   dict(floors=(4, 5), band=["small"],
                       req=["tower_core", "watch_platform", "guard_room", "armory", "living_quarters"],
                       opt=["cellar"],
                       adj=[["tower_core", "watch_platform"], ["guard_room", "armory"]],
                       forb=[["armory", "living_quarters"]],
                       features=["crenellation", "arrow_slits", "beacon"]),
    },
    "Gate": {
        "domain": "Defensive",
        "Easy":   dict(floors=(1, 2), band=["small", "medium"],
                       req=["gate_passage", "guard_room"], opt=[],
                       adj=[["gate_passage", "guard_room"]], forb=[], features=["portcullis"]),
        "Medium": dict(floors=(2, 2), band=["small", "medium"],
                       req=["gate_passage", "guard_room", "wall_walk"], opt=["armory"],
                       adj=[["gate_passage", "guard_room"], ["wall_walk", "gate_passage"]],
                       forb=[], features=["portcullis", "battlements"]),
        "Hard":   dict(floors=(2, 3), band=["medium"],
                       req=["gate_passage", "guard_room", "wall_walk", "armory", "watch_platform"],
                       opt=["cellar"],
                       adj=[["gate_passage", "guard_room"], ["wall_walk", "gate_passage"],
                            ["guard_room", "armory"]],
                       forb=[["armory", "gate_passage"]],
                       features=["portcullis", "battlements", "murder_holes"]),
    },
}

# plot 档位边界（参照 blueprint_metadata 实库分布：max(x,z) ≤15:14 / 16-30:26 / 31-60:35 / >60:48）
BANDS = {"small": (9, 15), "medium": (16, 30), "large": (31, 60), "xlarge": (61, 96)}

# 功能域配额：domain -> list of (function, difficulty, count)
# 难度合计 40 Easy / 40 Medium / 20 Hard
DOMAIN_PLAN = [
    ("Residential", [("Residential", "Easy", 15), ("Residential", "Medium", 6), ("Residential", "Hard", 2)]),
    ("Mixed-use",   [("Mixed-use", "Easy", 3), ("Mixed-use", "Medium", 6), ("Mixed-use", "Hard", 3)]),
    ("Workshop",    [("Workshop", "Easy", 3), ("Workshop", "Medium", 2),
                     ("Blacksmith", "Medium", 2), ("Blacksmith", "Hard", 1),
                     ("Warehouse", "Easy", 1), ("Warehouse", "Medium", 3),
                     ("Farm", "Easy", 1), ("Farm", "Medium", 1)]),
    ("Hospitality", [("Inn", "Easy", 4), ("Inn", "Medium", 5), ("Inn", "Hard", 3)]),
    ("Civic",       [("Civic", "Easy", 2), ("Civic", "Medium", 4), ("Civic", "Hard", 2),
                     ("Religious", "Easy", 1), ("Religious", "Medium", 2), ("Religious", "Hard", 1)]),
    ("Defensive",   [("Tower", "Easy", 3), ("Tower", "Medium", 2),
                     ("Gate", "Easy", 1), ("Gate", "Medium", 2), ("Gate", "Hard", 1),
                     ("Castle", "Medium", 3), ("Castle", "Hard", 3)]),
    ("Constrained Plot", [("Residential", "Easy", 3), ("Workshop", "Easy", 2), ("Inn", "Easy", 1),
                          ("Residential", "Medium", 2),
                          ("Inn", "Hard", 1), ("Tower", "Hard", 2), ("Workshop", "Hard", 1)]),
]

# P0 缺口组合（style, function, matrix_size_class, count）——对应 data_gap_matrix top_gaps
# matrix size_class 复用 V6C2 scale：tiny≤16 / small≤32 / medium≤64
GAP_PLAN = [
    ("Medieval", "Inn",        "small",  2),
    ("Rustic",   "Inn",        "small",  2),
    ("Medieval", "Civic",      "small",  2),
    ("Rustic",   "Civic",      "small",  1),
    ("Rustic",   "Civic",      "medium", 1),
    ("Medieval", "Blacksmith", "small",  1),
    ("Medieval", "Blacksmith", "medium", 1),
    ("Rustic",   "Blacksmith", "medium", 1),
    ("Medieval", "Warehouse",  "small",  1),
    ("Medieval", "Warehouse",  "medium", 1),
    ("Rustic",   "Warehouse",  "small",  1),
    ("Medieval", "Gate",       "small",  2),
    ("Rustic",   "Gate",       "small",  1),
    ("Rustic",   "Gate",       "medium", 1),
    ("Medieval", "Farm",       "small",  1),
    ("Rustic",   "Farm",       "medium", 1),
]

# 非缺口 brief 的 style 轮转池（样本充足类优先，PROVISIONAL 类保底覆盖）
STYLE_POOL = ["Medieval", "Rustic", "Fantasy", "Japanese", "Chinese"]

SCORING_WEIGHTS = {
    "hard_validity": 40, "functional_layout": 25, "style_compliance": 20,
    "material_coherence": 10, "efficiency": 5,
}


def load_inputs(root: Path):
    with open(root / "04_GRAMMARS" / "data_gap_matrix.json", encoding="utf-8") as f:
        gap = json.load(f)
    p0_cells = {(c["style"], c["function"], c["size_class"]) for c in gap["cells"]
                if c.get("priority") == "P0"}
    return p0_cells


def pick_dims(rng, band, footprint_ratio, gap_size_class=None):
    """按档位与风格长宽比采样 plot 尺寸；gap brief 需落在 matrix size_class 边界内
    （V6C2 scale 规则：tiny≤16 / small 17-32 / medium 33-64 / large ≤128）。"""
    lo, hi = BANDS[band]
    if gap_size_class == "small":
        lo, hi = 17, 32
    elif gap_size_class == "medium":
        lo, hi = 33, 64
    w = rng.randint(lo, hi)
    r = rng.uniform(*footprint_ratio)
    d = int(round(w * r))
    d = max(lo, min(hi, d))
    if d < w:  # 保持 w <= d 无必要，交换使长边为 depth 亦可；此处仅记录
        w, d = d, w
    return w, d


def zones_capacity_ok(w, d, floors, req, opt):
    """容量自检：室内区 ≤ 0.7 × plot × floors；室外区 ≤ 0.45 × plot。"""
    plot = w * d
    inner = sum(ZONE_CATALOG[z]["min_area"] for z in req + opt if not ZONE_CATALOG[z]["exterior"])
    outer = sum(ZONE_CATALOG[z]["min_area"] for z in req + opt if ZONE_CATALOG[z]["exterior"])
    return inner <= 0.7 * plot * floors and outer <= 0.45 * plot


def build_hard_constraints(floors, enclosed=True):
    """hard_constraints 引用 05_SPATIAL_VALIDATOR 规则编号 V001-V012（任务书 §10）。"""
    hc = [
        {"id": "HC_WITHIN_ENVELOPE", "validator_ref": "GEO",
         "rule": "全部方块位于 plot_width × plot_depth × max_height 包络内", "params": {}},
        {"id": "HC_ZONE_CAPACITY", "validator_ref": "CAP",
         "rule": "required_zones 均能分配到满足 min_area 的净使用空间", "params": {"zone_catalog": "zone_catalog.json"}},
        {"id": "HC_ENTRANCE_EXISTS", "validator_ref": "V001",
         "rule": "存在至少 1 个 exterior→interior 可识别入口", "params": {"min_count": 1}},
        {"id": "HC_ENTRANCE_CLEARANCE", "validator_ref": "V002",
         "rule": "主入口前后各 ≥2 格无阻挡，头顶 ≥3 格", "params": {"front": 2, "back": 2, "headroom": 3}},
        {"id": "HC_MAIN_SPACE_REACHABLE", "validator_ref": "V003",
         "rule": "所有 required_zones 可从主入口步行到达", "params": {}},
        {"id": "HC_NO_ISOLATED_ROOM", "validator_ref": "V004",
         "rule": "不存在与主连通分量断开且 ≥8 体素的封闭空间（设计性 vault 除外）", "params": {"min_voxels": 8}},
        {"id": "HC_HEADROOM_MIN", "validator_ref": "V009",
         "rule": "主要通行路径净高 ≥3，任意可通行位置净高 ≥2", "params": {"main_path": 3, "any": 2}},
    ]
    if floors >= 2:
        hc += [
            {"id": "HC_VERTICAL_CONNECTED", "validator_ref": "V007",
             "rule": "全部楼层存在有效垂直连接（楼梯/梯子），且落点可站立", "params": {"means": ["stairs", "ladder"]}},
            {"id": "HC_STAIR_BOTTOM_CLEAR", "validator_ref": "V005",
             "rule": "垂直交通底部入口可进入", "params": {}},
            {"id": "HC_STAIR_TOP_CLEAR", "validator_ref": "V006",
             "rule": "垂直交通顶部落点非实体且头顶 ≥2 格（对应真实失败案例'楼梯尽头是墙'）",
             "params": {"headroom": 2}},
        ]
    if enclosed:
        hc += [
            {"id": "HC_ENVELOPE_INTACT", "validator_ref": "V010",
             "rule": "围护结构无高置信度大面积断裂（露台/门廊除外）", "params": {}},
            {"id": "HC_ROOF_COVERAGE", "validator_ref": "V011",
             "rule": "室内区域屋顶覆盖完整，无异常中断", "params": {}},
        ]
    return hc


def build_soft_constraints(style, difficulty):
    sp = STYLE_PARAMS[style]
    sc = [
        {"id": "SC_FOOTPRINT_RATIO", "dimension": "style_compliance",
         "rule": f"平面长宽比落在 {style} p25-p75 区间 {sp['footprint_ratio']}",
         "target": sp["footprint_ratio"]},
        {"id": "SC_ROOF_RATIO", "dimension": "style_compliance",
         "rule": f"屋顶高度占比落在 {style} 实测区间 {sp['roof_ratio']}",
         "target": sp["roof_ratio"]},
        {"id": "SC_PALETTE_RANGE", "dimension": "material_coherence",
         "rule": f"主材料族占比落在 {style} grammar 区间",
         "target": sp["palette_ranges"]},
        {"id": "SC_DEAD_END", "dimension": "functional_layout",
         "rule": "非设计性死路占比 ≤0.20（参考实库 dead_end_ratio p75 约 0.19-0.25）",
         "target": {"dead_end_ratio_max": 0.20}},
    ]
    if difficulty in ("Medium", "Hard"):
        sc.append({"id": "SC_BLOCK_BUDGET", "dimension": "efficiency",
                   "rule": "总方块数 ≤ plot × max_height × 0.35（occupancy 效率上限）",
                   "target": {"occupancy_max": 0.35}})
    return sc


def make_brief(idx, style, function, difficulty, band, rng, targets_gap, gap_cell, constrained=False):
    sp = STYLE_PARAMS[style]
    tmpl = T[function][difficulty]
    floors = rng.randint(*tmpl["floors"])
    w, d = pick_dims(rng, band, sp["footprint_ratio"],
                     gap_size_class=gap_cell[2] if gap_cell else None)
    if constrained:
        # Constrained Plot：强制小面宽，以垂直发展补偿
        w = rng.randint(9, 13)
        d = rng.randint(max(w, 10), 15)
        floors = max(floors, 2 if difficulty != "Hard" else 3)

    fh = sp["fh"]
    max_dim = max(w, d)
    roof_h = max(3, min(14, int(round(0.22 * max_dim))))
    margin = 1 if (difficulty == "Hard" or constrained) else rng.randint(2, 4)
    max_height = floors * fh + roof_h + margin

    req = list(tmpl["req"])
    opt = [z for z in tmpl["opt"]]
    # 容量兜底：容量不足时先砍 optional，再扩 plot
    while not zones_capacity_ok(w, d, floors, req, opt) and opt:
        opt.pop()
    guard = 0
    while not zones_capacity_ok(w, d, floors, req, opt) and guard < 30:
        w += 2
        d += 2
        guard += 1
    assert zones_capacity_ok(w, d, floors, req, opt), f"capacity fail idx={idx}"
    assert floors * fh <= max_height, f"height fail idx={idx}"

    entrance_facing = rng.choice(["S", "N", "E", "W"]) if constrained else "any"
    brief = {
        "brief_id": f"BRIEF-{idx:04d}",
        "difficulty": difficulty,
        "style": style,
        "function": function,
        "function_domain": T[function]["domain"] if not constrained else "Constrained Plot",
        "targets_gap": targets_gap,
        "plot_width": w,
        "plot_depth": d,
        "max_height": max_height,
        "required_floors": floors,
        "required_zones": req,
        "optional_zones": opt,
        "required_adjacencies": tmpl["adj"],
        "forbidden_adjacencies": tmpl["forb"],
        "entrance_constraints": {
            "min_count": 1,
            "max_count": 1 if difficulty == "Easy" else 2,
            "facing": entrance_facing,
            "reachable_from_plot_edge": True,
            "front_clearance": {"width": 2, "depth": 2, "headroom": 3},
        },
        "vertical_circulation_constraints": {
            "required": floors >= 2,
            "means": ["stairs"] if difficulty != "Easy" else ["stairs", "ladder"],
            "connects_all_floors": floors >= 2,
            "assumed_floor_height": fh,
            "stair_top_min_headroom": 2,
        },
        "palette_constraints": {
            "dominant_families": sp["dominant_families"],
            "family_ratio_ranges": sp["palette_ranges"],
            "banned_families": sp["banned_families"],
            "basis": f"STYLE.{style}.palette_* p25-p75 (style_rules.json)",
        },
        "roof_constraints": {
            "form": sp["roof_form"],
            "height_ratio_range": sp["roof_ratio"],
            "overhang_min": sp["overhang_min"],
            "full_coverage": True,
            "estimated_roof_height": roof_h,
        },
        "special_features": list(tmpl["features"]),
        "hard_constraints": build_hard_constraints(floors, enclosed=True),
        "soft_constraints": build_soft_constraints(style, difficulty),
        "scoring_dimensions": dict(SCORING_WEIGHTS),
    }
    return brief


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="Minecraft_Architecture_Intelligence 根目录")
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args()
    root = Path(args.root)
    outdir = root / "06_BENCHMARK"
    outdir.mkdir(parents=True, exist_ok=True)

    p0_cells = load_inputs(root)
    rng = random.Random(args.seed)

    # 1) 展开配额计划为 (function, difficulty) 序列
    plan = []
    for domain, entries in DOMAIN_PLAN:
        for function, difficulty, count in entries:
            for _ in range(count):
                plan.append({"function": function, "difficulty": difficulty,
                             "constrained": domain == "Constrained Plot"})

    # 2) 展开缺口计划，绑定到匹配的 plan 槽位（function 需一致）
    gap_assign = {}   # plan_index -> (style, matrix_size_class)
    used_gap = []
    for style, function, msc, count in GAP_PLAN:
        assert (style, function, msc) in p0_cells, f"非 P0 缺口: {style}/{function}/{msc}"
        hit = 0
        for i, p in enumerate(plan):
            if hit >= count:
                break
            if i in gap_assign or p["function"] != function:
                continue
            gap_assign[i] = (style, msc)
            hit += 1
        used_gap.append((style, function, msc, hit))
        assert hit == count, f"缺口槽位不足: {style}/{function}/{msc} 需 {count} 得 {hit}"

    # 3) 逐槽生成 brief
    briefs = []
    style_cursor = 0
    seen = set()
    for i, p in enumerate(plan):
        function, difficulty = p["function"], p["difficulty"]
        if i in gap_assign:
            style, msc = gap_assign[i]
            band = "medium"   # gap 尺寸由 pick_dims 的 size_class 夹取控制（17-32 / 33-64）
            targets_gap, gap_cell = True, (style, function, msc)
        else:
            style = STYLE_POOL[style_cursor % len(STYLE_POOL)]
            style_cursor += 1
            bands = T[function][difficulty]["band"]
            band = bands[i % len(bands)]
            targets_gap, gap_cell = False, None
        if p["constrained"]:
            band = "small"
        b = make_brief(i + 1, style, function, difficulty, band, rng,
                       targets_gap, gap_cell, constrained=p["constrained"])
        if gap_cell:
            b["gap_ref"] = {"matrix_style": gap_cell[0], "matrix_function": gap_cell[1],
                            "matrix_size_class": gap_cell[2], "matrix_priority": "P0"}
        key = (b["style"], b["function"], b["difficulty"], b["plot_width"], b["plot_depth"],
               b["max_height"], b["required_floors"], tuple(b["required_zones"]))
        assert key not in seen, f"重复 brief: {key}"
        seen.add(key)
        briefs.append(b)

    # 4) 汇总校验
    assert len(briefs) == 100, len(briefs)
    diff_c = Counter(b["difficulty"] for b in briefs)
    assert diff_c == {"Easy": 40, "Medium": 40, "Hard": 20}, diff_c
    dom_c = Counter(b["function_domain"] for b in briefs)
    required_domains = {"Residential", "Mixed-use", "Workshop", "Hospitality",
                        "Civic", "Defensive", "Constrained Plot"}
    assert required_domains <= set(dom_c), dom_c

    # 5) 写 design_briefs.jsonl / zone_catalog.json
    with open(outdir / "design_briefs.jsonl", "w", encoding="utf-8") as f:
        for b in briefs:
            f.write(json.dumps(b, ensure_ascii=False) + "\n")
    with open(outdir / "zone_catalog.json", "w", encoding="utf-8") as f:
        json.dump({"version": VERSION, "zones": ZONE_CATALOG}, f, ensure_ascii=False, indent=1)

    # 6) 覆盖统计
    cov = defaultdict(int)
    for b in briefs:
        cov[(b["style"], b["function"], b["difficulty"])] += 1
    stats = {
        "version": VERSION,
        "seed": args.seed,
        "total": len(briefs),
        "difficulty_counts": dict(diff_c),
        "domain_counts": dict(dom_c),
        "domain_difficulty": {f"{dom}|{dif}": n for (dom, dif), n in
                              sorted(Counter((b['function_domain'], b['difficulty']) for b in briefs).items())},
        "style_counts": dict(Counter(b["style"] for b in briefs)),
        "function_counts": dict(Counter(b["function"] for b in briefs)),
        "targets_gap_count": sum(1 for b in briefs if b["targets_gap"]),
        "style_function_difficulty": [
            {"style": s, "function": fn, "difficulty": dif, "count": n}
            for (s, fn, dif), n in sorted(cov.items())
        ],
        "size_band_counts": dict(Counter(
            "small" if max(b["plot_width"], b["plot_depth"]) <= 15 else
            "medium" if max(b["plot_width"], b["plot_depth"]) <= 30 else
            "large" if max(b["plot_width"], b["plot_depth"]) <= 60 else "xlarge"
            for b in briefs)),
    }
    with open(outdir / "coverage_stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=1)

    # 7) dev/test 分层划分 30/70（按 difficulty × function_domain 分层）
    strata = defaultdict(list)
    for b in briefs:
        strata[(b["difficulty"], b["function_domain"])].append(b["brief_id"])
    srng = random.Random(args.seed + 1)
    dev, test = [], []
    for key, ids in sorted(strata.items()):
        ids = sorted(ids)
        srng.shuffle(ids)
        k = max(1, round(len(ids) * 0.3))
        dev.extend(ids[:k])
        test.extend(ids[k:])
    # 精修到 30/70
    srng.shuffle(test)
    while len(dev) > 30:
        test.append(dev.pop())
    while len(dev) < 30:
        dev.append(test.pop())
    split = {
        "version": VERSION,
        "ratio": "30/70",
        "method": "按 difficulty × function_domain 分层抽样，种子固定可复跑",
        "usage": {
            "dev": "规则调参 / prompt 迭代 / Validator 阈值校准专用，禁止用于最终对比报告",
            "test": "最终 B vs C 与跨模型对比仅在 test 上运行一次，避免过拟合",
        },
        "dev": sorted(dev),
        "test": sorted(test),
        "dev_strata": {f"{d}|{dom}": n for (d, dom), n in
                       sorted(Counter((b['difficulty'], b['function_domain'])
                                      for b in briefs if b['brief_id'] in dev).items())},
    }
    with open(outdir / "benchmark_split.json", "w", encoding="utf-8") as f:
        json.dump(split, f, ensure_ascii=False, indent=1)

    print(json.dumps({"total": stats["total"], "difficulty": stats["difficulty_counts"],
                      "domains": stats["domain_counts"], "styles": stats["style_counts"],
                      "targets_gap": stats["targets_gap_count"],
                      "dev": len(dev), "test": len(test)}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
