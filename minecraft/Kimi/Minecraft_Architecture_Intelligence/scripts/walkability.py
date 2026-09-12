# -*- coding: utf-8 -*-
"""walkability — Minecraft 玩家可通行近似模型（项目代号 H · P1 核心共享模块）。

P2 Spatial Validator 将复用本模块。目标不是完整模拟物理，而是可靠检测建筑空间错误
（“楼梯尽头是墙”、入口不可达、孤立房间、垂直交通断裂）。

## 玩家近似
- 宽 1 格、高 1.8 格（按 2-block clearance 检查，脚部 + 头部）；
- step-up ≤ 0.5 格：同层可走、半砖/地毯/雪层可站上；
- 楼梯可走：相邻楼梯站位高差 0.5 自然衔接；另允许 ≤1.0 高差且至少一端支撑为楼梯；
- 梯子可攀爬：同一 (x,z) 连续梯柱把各层相邻站位连成垂直通道；
- 不模拟跳跃（跳跃上 1 格不属于“可通行”常规语义）。

## 站位（stance）模型
站位锚定在**支撑方块**所在体素 u，脚部高程 E = u.y + surface(u)。
- full cube / top slab / top stair / 8 层雪 → surface 1.0（脚在 u 顶面，身体占 u+1、u+2）；
- bottom slab / bottom stair / bottom 关闭活板门 → surface 0.5；
- 地毯 / 压力板 / 单层雪 → surface ≈ 0.1（近似按 0.1 处理高差判定，仍满足 ≤0.5）；
- air / 水 / 梯子等不提供 surface，不产生站位。

## 净高（clearance）检查（向量化）
对表面高 s 的站位：
1. 体素 u 内 surface 以上无实体（构造保证）；
2. v1 = u+1：无实体 或 solid_lo[v1] ≥ s + 0.8；
3. v2 = u+2：仅当 s + 1.8 > 2.0 时，要求 无实体 或 solid_lo[v2] ≥ s - 0.2。
（每个体素的实体近似为单个区间 [solid_lo, solid_hi]，足够覆盖原版常见碰撞体。）

## 连通图
- 节点 = 全部合法站位；
- 边 = 水平 4 邻接且 |ΔE| ≤ 0.5；或 |ΔE| ≤ 1.0 且任一端支撑为楼梯；
- 梯柱边：同一梯柱相邻站位按高程排序链式相连（记为 vertical）；
- 连通分量用 scipy.sparse.csgraph.connected_components（union-find 量级）。

## 方块分类表（数据驱动）
``BLOCK_CLASS_RULES`` 为有序规则表：每条 (谓词, 类名)。可用 ``--class-table``
传入同名结构 JSON 覆盖/扩展。未知方块分类为 UNKNOWN，保守视为实体阻挡，
并计入 ``unknown_block_types`` 统计。

## 输出
``analyze(voxels, ir)`` 返回 dict：
walkable_voxels / walkable_components / largest_component_ratio /
isolated_space_count / vertical_connections / dead_end_count /
unknown_block_types / class_counts / component_sizes（供调用方进一步诊断）。
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy import sparse
from scipy.sparse import csgraph

# ---------------------------------------------------------------------------
# 方块分类表（数据驱动）
# ---------------------------------------------------------------------------
# 类名语义：
#   AIR            空气类（无碰撞）
#   FULL           实心整格
#   SLAB           半砖（按 half/type 属性区分 bottom/top/double）
#   STAIR          楼梯（按 half 属性区分 bottom/top）
#   DOOR           门（open=true 可过；非铁质 closed 视为可交互通过；铁质 closed 阻挡）
#   TRAPDOOR       活板门（open 可过；closed 按 half 视为半砖）
#   FENCE          栅栏（碰撞高 1.5，不可跨越）
#   WALL           石墙（同栅栏）
#   GLASS_PANE     玻璃板（同栅栏）
#   LADDER         梯子/藤蔓类可攀爬（无站位、产生垂直边）
#   CARPET         地毯（薄，可站上）
#   SNOW_LAYER     雪层（按 layers 属性，8 层视为整格）
#   PRESSURE_PLATE 压力板/按钮类薄片
#   WATER          水（可穿越但不产生站位）
#   UNKNOWN        未知（保守视为整格实体，计入统计）

# 每条规则：(关键字列表, 类名)。按顺序匹配 block_id 的子串；先匹配先生效。
# 注意避开误命中（如 "door" 命中 "trapdoor"），trapdoor 规则必须在 door 之前。
BLOCK_CLASS_RULES: list[tuple[list[str], str]] = [
    (["cave_air", "void_air", ":air", "minecraft:air"], "AIR"),
    (["_trapdoor"], "TRAPDOOR"),
    (["_door"], "DOOR"),
    (["_stairs"], "STAIR"),
    (["_slab"], "SLAB"),
    (["_carpet"], "CARPET"),
    (["snow_layer", ":snow"], "SNOW_LAYER"),
    (["ladder", "vine", "scaffolding"], "LADDER"),
    (["_fence_gate"], "FENCE_GATE"),
    (["_fence"], "FENCE"),
    (["_wall"], "WALL"),
    (["_pane"], "GLASS_PANE"),          # glass_pane / stained_glass_pane
    (["_bars"], "GLASS_PANE"),          # 铁栏杆等，同玻璃板阻挡
    # 薄面可站（≈0.1–0.45 高）：篝火/阳光探测器/红石器件/压力板/蜡烛
    (["campfire", "daylight_detector", "comparator", "repeater",
      "pressure_plate", "candle"], "PRESSURE_PLATE"),
    # 无碰撞装饰（花草/农作物/树苗/蕨类等）：可穿越、不产生站位
    (["lilac", "peony", "rose_bush", "sunflower", "tall_grass", "short_grass",
      "fern", "flower", "tulip", "orchid", "dandelion", "poppy", "allium",
      "azure", "bluet", "daisy", "cornflower", "wither_rose", "sapling",
      "azalea", "fungus", "mushroom", "roots", "sprouts", "sugar_cane",
      "bamboo", "kelp", "seagrass", "lily_pad", "lily_of_the_valley",
      "wheat", "carrots", "potatoes", "beetroots", "nether_wart", "cocoa",
      "sweet_berry", "dead_bush", "dripleaf", "eyeblossom", "pitcher",
      "pink_petals", "propagule"], "PLANT"),
    # 无碰撞功能件：火把/按钮/告示牌/旗帜/铁轨/红石线/绊线/灯笼/蛛网/拉杆/头/蛋
    (["torch", "lantern", "_button", "_sign", "_banner", ":rail", "_rail",
      "redstone_wire", "tripwire", "cobweb", ":web", "lever", "end_rod",
      "skull", "_head", "turtle_egg", "dragon_egg", "conduit", "potted_",
      "nether_portal", "soul_fire", ":fire", ":light", "glow_lichen",
      "sea_pickle"], "NONSOLID"),
    (["water"], "WATER"),
    (["lava"], "LAVA"),
]

# 显式整格方块白名单外的处理：凡不匹配任何规则的，先按 block_id 再查
# KNOWN_FULL_KEYWORDS（常见装饰/功能方块按整格处理），否则 UNKNOWN。
KNOWN_FULL_KEYWORDS = [
    "stone", "dirt", "grass_block", "planks", "log", "wood", "brick", "glass",
    "concrete", "terracotta", "wool", "sand", "gravel", "clay", "ore",
    "obsidian", "bedrock", "prismarine", "quartz", "deepslate", "tuff",
    "andesite", "diorite", "granite", "basalt", "blackstone", "calcite",
    "dripstone", "magma", "netherrack", "nylium", "soul_s", "end_stone",
    "purpur", "copper", "iron_block", "gold_block", "diamond", "emerald",
    "lapis", "redstone_block", "coal_block", "hay_block", "moss", "mud",
    "packed_mud", "ice", "snow_block", "bone_block", "coral", "sponge",
    "bookshelf", "crafting_table", "furnace", "chest", "barrel", "loom",
    "smithing_table", "cartography", "fletching", "grindstone", "stonecutter",
    "anvil", "enchanting", "brewing", "cauldron", "composter", "jukebox",
    "note_block", "beacon", "piston", "observer", "dropper", "dispenser",
    "hopper", "lectern", "bed", "shulker", "lamp", "leaves",
    "cactus", "melon", "pumpkin", "cake",
    "amethyst", "chain", "bell", "lightning_rod", "sculk",
    "ochre", "resin", "pale_moss", "creaking", "honeycomb", "slime_block",
    "honey_block", "barrier", "structure", "command",
    "stem", "hyphae", "podzol", "netherite", "smoker", "crafter",
    "froglight", "shroomlight", "target", "bee_nest", "beehive",
    "decorated_pot", "powder_snow", "farmland", "wart_block",
]


def classify_block(block_id: str, props: dict[str, str]) -> str:
    """按规则表分类方块；未知返回 UNKNOWN。"""
    bid = block_id.lower()
    for keywords, cls in BLOCK_CLASS_RULES:
        for kw in keywords:
            if kw in bid:
                return cls
    for kw in KNOWN_FULL_KEYWORDS:
        if kw in bid:
            return "FULL"
    return "UNKNOWN"


# ---------------------------------------------------------------------------
# 体素参数化：每个体素 → (surface, solid_lo, solid_hi, flags)
# ---------------------------------------------------------------------------
# flags 位： 1=是楼梯  2=是梯子  4=可穿越液体
F_STAIR = 1
F_LADDER = 2
F_FLUID = 4


def _palette_params(ir) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, list[str]]:
    """对 palette 每项计算 (surface, solid_lo, solid_hi, flags)。

    surface: 提供脚部支撑的高程（无支撑 = 0，同时 none_solid 且无支撑 → 无站位）
    solid_lo/solid_hi: 实体区间（无实体 = lo=1.0, hi=1.0）
    另返回每类 class 名列表（供统计）。
    """
    n = len(ir.palette)
    surface = np.zeros(n, dtype=np.float32)
    has_surface = np.zeros(n, dtype=bool)
    solid_lo = np.ones(n, dtype=np.float32)
    solid_hi = np.ones(n, dtype=np.float32)
    flags = np.zeros(n, dtype=np.uint8)
    classes: list[str] = []

    for i, (bid, props) in enumerate(zip(ir.block_ids, ir.properties)):
        cls = classify_block(bid, props)
        classes.append(cls)

        def set_solid(lo: float, hi: float) -> None:
            solid_lo[i], solid_hi[i] = lo, hi

        def set_surface(s: float) -> None:
            surface[i], has_surface[i] = s, True

        if cls == "AIR":
            pass
        elif cls in ("PLANT", "NONSOLID"):
            pass  # 无碰撞：可穿越、不产生站位
        elif cls == "FULL":
            set_solid(0.0, 1.0)
            set_surface(1.0)
        elif cls == "SLAB":
            t = props.get("type", props.get("half", "bottom"))
            if t == "double":
                set_solid(0.0, 1.0)
                set_surface(1.0)
            elif t == "top":
                set_solid(0.5, 1.0)
                set_surface(1.0)
            else:  # bottom
                set_solid(0.0, 0.5)
                set_surface(0.5)
        elif cls == "STAIR":
            flags[i] |= F_STAIR
            if props.get("half", "bottom") == "top":
                set_solid(0.5, 1.0)
                set_surface(1.0)
            else:
                set_solid(0.0, 0.5)
                set_surface(0.5)
        elif cls == "DOOR":
            is_iron = "iron" in bid
            is_open = props.get("open", "false") == "true"
            if is_open or not is_iron:
                # 敞开的门可过；非铁质关门玩家可交互开启，连通性上视为可过
                pass
            else:
                set_solid(0.0, 1.0)  # 关闭的铁门阻挡
        elif cls == "TRAPDOOR":
            if props.get("open", "false") == "true":
                pass  # 开启的活板门贴在侧面，近似无碰撞
            elif props.get("half", "bottom") == "top":
                set_solid(0.5, 1.0)
                set_surface(1.0)
            else:
                set_solid(0.0, 0.5)
                set_surface(0.5)
        elif cls in ("FENCE", "WALL", "GLASS_PANE", "FENCE_GATE"):
            # 栅栏门 open 可过；closed 视为“玩家可交互开启”（同非铁质门语义）→ 可过
            if cls == "FENCE_GATE":
                pass
            else:
                set_solid(0.0, 1.0)
                set_surface(1.0)  # 顶面可站（仅能从 ≥0.5 高差抵达，不模拟跳栅栏）
        elif cls == "LADDER":
            flags[i] |= F_LADDER
        elif cls == "CARPET":
            set_solid(0.0, 0.1)
            set_surface(0.1)
        elif cls == "SNOW_LAYER":
            try:
                layers = int(props.get("layers", "1"))
            except ValueError:
                layers = 1
            if layers >= 8:
                set_solid(0.0, 1.0)
                set_surface(1.0)
            else:
                h = min(layers, 7) * 0.125
                set_solid(0.0, h)
                set_surface(h)
        elif cls == "PRESSURE_PLATE":
            set_solid(0.0, 0.1)
            set_surface(0.1)
        elif cls in ("WATER", "LAVA"):
            flags[i] |= F_FLUID
        else:  # UNKNOWN：保守按整格实体
            set_solid(0.0, 1.0)
            set_surface(1.0)

    return surface, has_surface, solid_lo, solid_hi, flags, classes


# ---------------------------------------------------------------------------
# 主分析入口
# ---------------------------------------------------------------------------
def analyze(voxels: np.ndarray, ir, isolated_min_size: int = 8, return_labels: bool = False,
            return_graph: bool = False) -> dict:
    """对体素蓝图执行 walkability 分析。

    参数:
        voxels: (x,y,z) int32，值为 ir.palette 索引（blueprint_io.to_voxels 的输出）。
        ir: BlueprintIR（提供 palette 属性与 block_ids）。
        isolated_min_size: 小于该体素数的非最大分量不计入 isolated_space_count
            （避免把屋顶边缘、装饰小平台误判为“孤立空间”）。
        return_labels: 额外返回全包络分量标签与站位高程。
        return_graph: 额外返回站位图的边数组（graph_src/graph_dst，扁平体素索引，
            双向均已写入）。供 P2 Validator 做邻接查询，不影响既有输出。

    返回: 见模块 docstring。
    """
    surface, has_surface, solid_lo, solid_hi, flags, classes = _palette_params(ir)

    # 体素级参数展开
    idx = voxels
    v_surf = surface[idx]
    v_has_surf = has_surface[idx]
    v_slo = solid_lo[idx]
    v_flag = flags[idx]

    X, Y, Z = voxels.shape

    # --- 站位合法性：clearance 检查 -------------------------------------
    # 站位 = 体素 u 提供 surface，且上方净高满足 1.8。
    s = v_surf
    legal = v_has_surf.copy()

    # v1（u+1 层）：需无实体 或 solid_lo >= s + 0.8
    no_solid_v1 = np.ones_like(legal)
    slo_v1 = np.ones_like(v_slo)
    no_solid_v1[:, :-1, :] = solid_lo[idx[:, 1:, :]] >= 1.0
    slo_v1[:, :-1, :] = solid_lo[idx[:, 1:, :]]
    v1_ok = no_solid_v1 | (slo_v1 >= s + 0.8)
    v1_ok[:, -1, :] = True  # 包络顶界外视为空气
    legal &= v1_ok

    # v2（u+2 层）：仅当 s + 1.8 > 2.0（即 s > 0.2）时需要检查
    needs_v2 = s > 0.2001
    no_solid_v2 = np.ones_like(legal)
    slo_v2 = np.ones_like(v_slo)
    no_solid_v2[:, :-2, :] = solid_lo[idx[:, 2:, :]] >= 1.0
    slo_v2[:, :-2, :] = solid_lo[idx[:, 2:, :]]
    v2_ok = no_solid_v2 | (slo_v2 >= np.maximum(s - 0.2, 0.0))
    legal &= (~needs_v2) | v2_ok

    # 站位高程 E = y + s
    yy = np.arange(Y, dtype=np.float32)[None, :, None]
    E = yy + s
    E = np.where(legal, E, np.nan)

    # --- 边：水平 4 邻接 × 支撑高差 dy ∈ {-1, 0, +1} ----------------------
    # 站位锚定在支撑体素上，因此“走上半砖/楼梯”在体素空间里是斜向 (±1 层) 的：
    # 平地 stance 在 (x, y=0)，半砖 stance 在 (x+1, y=1)。ΔE 规则负责过滤合法性。
    edges_src: list[np.ndarray] = []
    edges_dst: list[int] = []

    def flat_index(a: np.ndarray) -> np.ndarray:
        """布尔/掩码数组对应的扁平体素索引。"""
        return np.flatnonzero(a)

    # 支撑为楼梯的掩码（用于 ≤1.0 高差的楼梯边）
    is_stair_support = (v_flag & F_STAIR) > 0

    step_edges = 0
    for axis in (0, 2):
        n_axis = E.shape[axis]
        for dy in (-1, 0, 1):
            y0 = max(0, -dy)
            y1 = min(Y, Y - dy)
            if y1 <= y0 or n_axis < 2:
                continue
            # 构造 a/b 切片：b 是 a 沿 axis +1、沿 y +dy 的邻居
            sl_a = [slice(None)] * 3
            sl_b = [slice(None)] * 3
            sl_a[axis] = slice(0, n_axis - 1)
            sl_b[axis] = slice(1, n_axis)
            sl_a[1] = slice(y0, y1)
            sl_b[1] = slice(y0 + dy, y1 + dy)
            a = E[tuple(sl_a)]
            b = E[tuple(sl_b)]
            stair_a = is_stair_support[tuple(sl_a)]
            stair_b = is_stair_support[tuple(sl_b)]
            both = ~np.isnan(a) & ~np.isnan(b)
            dE = np.abs(a - b)
            walk = both & (dE <= 0.5001)
            # 楼梯助推：高差 ≤1.0 且至少一端支撑为楼梯
            walk |= both & (dE <= 1.0001) & (dE > 0.5001) & (stair_a | stair_b)
            if not walk.any():
                continue

            # 还原全局扁平索引
            shape_a = list(E.shape)
            shape_a[axis] -= 1
            shape_a[1] = y1 - y0
            mask_idx = np.flatnonzero(walk)
            coords = list(np.unravel_index(mask_idx, shape_a))
            coords[1] = coords[1] + y0  # 还原 y 偏移
            src = np.ravel_multi_index(coords, E.shape)
            coords_dst = [coords[0].copy(), coords[1].copy(), coords[2].copy()]
            coords_dst[axis] = coords_dst[axis] + 1
            coords_dst[1] = coords_dst[1] + dy
            dst = np.ravel_multi_index(coords_dst, E.shape)
            edges_src.append(src)
            edges_src.append(dst)
            edges_dst.extend(dst.tolist())
            edges_dst.extend(src.tolist())
            step_edges += int(walk.sum())

    if edges_src:
        src_all = np.concatenate(edges_src)
        dst_all = np.array(edges_dst, dtype=np.int64)
    else:
        src_all = np.zeros(0, dtype=np.int64)
        dst_all = np.zeros(0, dtype=np.int64)

    # --- 梯子垂直边 ------------------------------------------------------
    # 对每个站位计算脚部体素 fy = floor(E)，若其 4 邻（fy 与 fy-1 两层，
    # 覆盖“走下梯子踏上平台”的情形）接触梯柱，则把该站位挂到对应 (x,z) 梯柱，
    # 同柱站位按高程排序链式相连。
    ladder_mask = (v_flag & F_LADDER) > 0
    stance_mask = legal
    ladder_edges = 0
    if ladder_mask.any() and stance_mask.any():
        from collections import defaultdict

        col_stances: dict[tuple[int, int], list[tuple[float, int]]] = defaultdict(list)
        stance_coords = np.argwhere(stance_mask)
        for sx, sy, sz in stance_coords:
            e_val = float(E[sx, sy, sz])
            fy = int(math.floor(e_val + 1e-6))
            fi = int(np.ravel_multi_index((sx, sy, sz), E.shape))
            for ly in (fy, fy - 1):
                if ly < 0 or ly >= Y:
                    continue
                for nx, nz in ((sx - 1, sz), (sx + 1, sz), (sx, sz - 1), (sx, sz + 1)):
                    if 0 <= nx < X and 0 <= nz < Z and ladder_mask[nx, ly, nz]:
                        col_stances[(nx, nz)].append((e_val, fi))
        for (_lx, _lz), stances in col_stances.items():
            # 按高程分组（0.5 精度）：同梯柱上同一高度的多个站位可能分属不同
            # 房间（墙隔开），但它们都能抓住梯子——相邻高程组之间做完全二部连接，
            # 否则排序链式只把“紧挨着的下一个”站位挂上去，其余房间会被漏接。
            groups: dict[float, list[int]] = defaultdict(list)
            for e, fi in stances:
                groups[round(e * 2) / 2].append(fi)
            levels = sorted(groups)
            for e1, e2 in zip(levels, levels[1:]):
                if abs(e2 - e1) >= 0.9:  # 真正的垂直连接
                    for f1 in groups[e1]:
                        for f2 in groups[e2]:
                            src_all = np.concatenate([src_all, [f1, f2]])
                            dst_all = np.concatenate([dst_all, [f2, f1]])
                            ladder_edges += 1

    # --- 连通分量 ---------------------------------------------------------
    stance_idx = flat_index(stance_mask)
    n_nodes = len(stance_idx)
    total_voxels = int(voxels.size)

    if n_nodes > 0:
        graph = sparse.coo_matrix(
            (np.ones(len(src_all)), (src_all, dst_all)),
            shape=(total_voxels, total_voxels),
        ).tocsr()
        n_comp_all, labels_all = csgraph.connected_components(graph, directed=False)
        comp_labels = labels_all[stance_idx]
        # 分量大小（仅统计含站位的分量）
        unique, counts = np.unique(comp_labels, return_counts=True)
        sizes = counts.astype(np.int64)
        sizes_sorted = np.sort(sizes)[::-1]
        n_components = len(sizes)
        largest_ratio = float(sizes_sorted[0] / n_nodes) if n_nodes else 0.0
        isolated = int(((sizes_sorted[1:] >= isolated_min_size)).sum())
        # 死端：度数为 1 的站位节点（图中的边均在站位之间，直接 bincount）
        stance_set = np.zeros(total_voxels, dtype=bool)
        stance_set[stance_idx] = True
        deg = np.zeros(total_voxels, dtype=np.int64)
        np.add.at(deg, src_all, 1)
        dead_ends = int((deg[stance_idx] == 1).sum())
    else:
        n_components = 0
        largest_ratio = 0.0
        isolated = 0
        dead_ends = 0
        sizes_sorted = np.zeros(0, dtype=np.int64)

    # 垂直连接：楼梯边（ΔE>0.001）+ 梯子边
    # 近似统计：楼梯步进边中高差 >0 的视为垂直连接
    vertical_connections = ladder_edges
    if n_nodes > 0 and len(src_all) > 0:
        flatE = E.ravel()
        m = ~np.isnan(flatE[src_all]) & ~np.isnan(flatE[dst_all])
        vertical_connections += int((np.abs(flatE[src_all[m]] - flatE[dst_all[m]]) > 0.001).sum() // 2)

    # 未知方块统计
    unknown_types = sorted({ir.block_ids[i] for i, c in enumerate(classes) if c == "UNKNOWN"})
    from collections import Counter

    class_counts = Counter(classes)

    result = {
        "walkable_voxels": int(n_nodes),
        "walkable_components": int(n_components),
        "largest_component_ratio": round(largest_ratio, 4),
        "isolated_space_count": isolated,
        "vertical_connections": int(vertical_connections),
        "dead_end_count": dead_ends,
        "ladder_vertical_edges": int(ladder_edges),
        "step_edges": int(step_edges),
        "unknown_block_types": unknown_types,
        "unknown_block_type_count": len(unknown_types),
        "class_counts": dict(class_counts),
        "component_sizes_top10": sizes_sorted[:10].tolist(),
        "envelope_voxels": total_voxels,
    }
    if return_labels:
        # 诊断/测试用：全包络分量标签（-1=非站位）与站位高程
        lab = np.full(total_voxels, -1, dtype=np.int64)
        if n_nodes > 0:
            lab[stance_idx] = comp_labels
        result["labels"] = lab.reshape(voxels.shape)
        result["stance_elevation"] = E
    if return_graph:
        # P2 Validator 用：站位图边（双向）与站位合法性掩码
        result["graph_src"] = src_all
        result["graph_dst"] = dst_all
        result["stance_mask"] = stance_mask
    return result


def main() -> None:
    ap = argparse.ArgumentParser(description="蓝图 walkability 分析")
    ap.add_argument("path", help="REF 派生目录或 blueprint.json")
    ap.add_argument("--isolated-min-size", type=int, default=8)
    args = ap.parse_args()

    from blueprint_io import load_blueprint, to_voxels

    ir = load_blueprint(args.path)
    voxels, _air = to_voxels(ir)
    result = analyze(voxels, ir, isolated_min_size=args.isolated_min_size)
    result["ref_id"] = ir.ref_id
    result["ir_source"] = ir.ir_source
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
