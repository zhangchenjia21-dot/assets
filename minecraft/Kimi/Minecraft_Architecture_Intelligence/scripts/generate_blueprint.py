# -*- coding: utf-8 -*-
"""generate_blueprint — 参数化参考生成器（项目代号 H · P6 第二部分）。

**性质声明（诚实性）**：本生成器是 programmatic reference generator (rule-driven)：
由 07_ARCHITECT_SYSTEM/architect_rules.json 的数值区间与硬规则驱动的确定性
参数化算法，**不是 LLM Architect**。用途：在离线、零世界写入前提下验证
B（规则约束单轮）vs C（Architect→Validator→Critic→Revision→Recheck）管线在
机器可测指标上的差异，以及 Validator / Benchmark / Rulepack 是否形成闭环。
其输出质量是"规则直译"的天花板，不代表任何 LLM 的水平。

输入：一条 design brief（06_BENCHMARK/design_briefs.jsonl 行）+ 规则资源。
输出：Canonical IR JSON（schema_version=1，palette + blocks 四元组，
与 references\\derived 同构，可被 05_SPATIAL_VALIDATOR 直接消费）。

## 生成管线（各阶段遵循的规则在注释中标注规则 id）

1. plan_from_brief：footprint / 楼层分配 / 层高 / 屋顶剖面 / 入口 / 分区带，
   尺寸取自 brief 与 style_rules.json 实测区间（footprint_ratio、floor_height、
   roof_height_ratio、height_ratio）。
2. build_voxels：楼板→外墙→楼梯井（计划层落位）→隔墙→门窗→屋顶→装饰，
   逐元素打 tag（供 C 路线 Revision 定向修改）。
3. seal_envelope：6 连通洪泛自检围护密闭性，填补非设计性泄漏
   （GA-002/GA-005 与 V010/V011 属规则覆盖项，规则驱动生成器理应自检；
   门与设计性开口 ±1 格保护，与 V010 opening_margin 口径一致）。
4. fit_palette：材料族占比对照 brief.palette_constraints 做确定性参数调整
   （墙骨料石/木比例、地毯覆盖率、屋顶材料族），重建直至入界或次数耗尽。
5. to_ir：体素 dict → Canonical IR（包络最小角归零，dimensions 紧贴包络）。

## 单轮（B）已知的"规则未覆盖"盲区（诚实声明，非故意埋雷）

- 隔墙规划只避让楼梯井的**二维柱位**，不感知楼梯顶部落点/侧翼的三维净空
  （VA-G-02 在平面图层面无对应检查）→ 紧张地块上可能堵楼梯顶部出口；
- 楼梯落位检查"跑道+接近格放得下、不撞门 clearance"，不强制顶部继续
  向前的落点余量；
- 门廊进深按 V002 的静态判定语义（接近站位存在）而非 brief 的 2 格净深。
这些交互冲突是否存在由 Validator 实测；B 结果就是单轮忠实结果，
若全部零缺陷也如实报告。

运行：
    py -3 scripts/generate_blueprint.py --briefs 06_BENCHMARK/design_briefs.jsonl \
        --brief-id BRIEF-0006 --out <目录>
环境：见 scripts/README.md（py -3 + 只读挂载 site-packages）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import deque
from pathlib import Path

# ---------------------------------------------------------------------------
# 材料族 → 原版方块代表（映射口径 = 02_BLUEPRINT_METADATA/palette_dictionary.json
# 的子串匹配规则；每个代表方块均已核对落在目标族且 walkability 分类正确）。
# ---------------------------------------------------------------------------
MAT = {
    "foundation": "minecraft:cobblestone",          # stone 族，FULL
    "wall_stone": "minecraft:stone_bricks",         # stone 族，FULL
    "wall_wood": "minecraft:oak_planks",            # wood 族，FULL
    "floor": "minecraft:oak_planks",                # wood 族，FULL
    "partition": "minecraft:oak_planks",            # wood 族，FULL
    "roof_stair_stone": "minecraft:stone_brick_stairs",  # stone 族，STAIR
    "roof_stair_wood": "minecraft:oak_stairs",      # wood 族，STAIR
    "roof_cap": "minecraft:stone_bricks",
    "stair": "minecraft:oak_stairs",                # 室内楼梯，wood 族
    "glass": "minecraft:glass",                     # glass 族，FULL（封围护）
    "door": "minecraft:oak_door",                   # functional 族，DOOR（非铁可过）
    "carpet": "minecraft:white_carpet",             # decorative 族，CARPET（可站）
    "lantern": "minecraft:lantern",                 # decorative 族，NONSOLID
    "plate": "minecraft:oak_pressure_plate",        # functional 族，薄片可站(0.1)
    "chimney": "minecraft:stone_bricks",
    "fence": "minecraft:oak_fence",                 # wood 族，FENCE（露台栏）
}

# 公私属性（仅用于分区排布启发；公私分区本身 INFERRED，
# 见 04_GRAMMARS/functional_rules.json zone_semantics，不做判定）
PRIVATE_ZONES = {"bedroom", "guest_room", "living_quarters"}
PUBLIC_ZONES = {"living_hall", "common_room", "great_hall", "shop_front",
                "forge", "workshop_floor", "gate_passage", "guard_room",
                "tower_core", "farmhouse", "barn", "storage_hall"}

_DIRECTION_VEC = {"E": (1, 0), "W": (-1, 0), "S": (0, 1), "N": (0, -1)}
_FACING_NAME = {(1, 0): "east", (-1, 0): "west", (0, 1): "south", (0, -1): "north"}
# MC 约定：+z = 南。facing 属性 = 门/楼梯朝向；Validator 通行轴映射见 rules.py。
_DOWNHILL = {"south": "north", "north": "south", "east": "west", "west": "east"}


def load_resources(out_root: Path) -> dict:
    """加载规则资源（只读）。"""
    def j(p): return json.loads((out_root / p).read_text(encoding="utf-8"))
    return {
        "architect_rules": j(Path("07_ARCHITECT_SYSTEM/architect_rules.json")),
        "style_rules": j(Path("04_GRAMMARS/style_rules.json"))["rules"],
        "palette_dictionary": j(Path("02_BLUEPRINT_METADATA/palette_dictionary.json")),
        "zone_catalog": j(Path("06_BENCHMARK/zone_catalog.json"))["zones"],
    }


def style_rule(res: dict, style: str, dim: str) -> dict | None:
    for r in res["style_rules"]:
        if r["class"] == style and r["dimension"] == dim:
            return r
    return None


def family_of(block_id: str, families: dict) -> str:
    """与 P1 extract / score_v4_samples 完全一致的族匹配口径。"""
    for fam, spec in families.items():
        if any(pat in block_id for pat in spec["patterns"]):
            return fam
    return "UNKNOWN"


# ---------------------------------------------------------------------------
# 1. 平面规划
# ---------------------------------------------------------------------------
def plan_from_brief(brief: dict, res: dict, overrides: dict | None = None) -> dict:
    """把 brief 翻译成确定性平面方案。

    overrides 供 C 路线 Revision 微调（partition_shift / shaft_shift /
    palette_params / window_stride）；footprint / 风格 / 分区锚点不可变
    （REVISION_PROTOCOL §3.1）。
    """
    ov = overrides or {}
    W, D, H = brief["plot_width"], brief["plot_depth"], brief["max_height"]
    F = brief["required_floors"]
    zones = list(brief["required_zones"])
    zc = res["zone_catalog"]
    style = brief["style"]
    roof_c = brief["roof_constraints"]
    o = max(int(roof_c.get("overhang_min", 0)), 1)   # 出檐（S07）

    # ---- 入口立面（先于 footprint：门廊边距影响选址） ----------------------
    facing_req = brief["entrance_constraints"].get("facing", "any")
    side = facing_req if facing_req in _DIRECTION_VEC else "S"
    dvec = _DIRECTION_VEC[side]

    # ---- footprint 搜索 ---------------------------------------------------
    # 约束：E03 投影占比 [0.3,0.9]；zone 容量；风格 footprint_ratio 区间。
    interior_zones = [z for z in zones if not zc.get(z, {}).get("exterior", False)]
    exterior_zones = [z for z in zones if zc.get(z, {}).get("exterior", False)]
    need_area = sum(zc[z]["min_area"] for z in interior_zones)
    fr = style_rule(res, style, "footprint_ratio") or {"min": 1.0, "max": 3.0,
                                                       "p25": 1.0, "p75": 2.0}
    apron_need = 2                                # 门廊深度（V002 接近位）
    assumed_fh = brief["vertical_circulation_constraints"].get("assumed_floor_height", 5)
    run_need = assumed_fh + 1 if brief["required_floors"] >= 2 else 0
    best = None
    for bw in range(5, W + 1):
        for bd in range(5, D + 1):
            interior = (bw - 2) * (bd - 2)
            if interior <= 0 or interior * F < need_area * 1.30:
                continue
            # 直跑楼梯可行性：最长内墙线 ≥ 跑道长（fh 步 + 接近格）
            if run_need and max(bw - 2, bd - 2) < run_need:
                continue
            env_x = bw + 2 * o + (apron_need if side in ("E", "W") else 0)
            env_z = bd + 2 * o + (apron_need if side in ("S", "N") else 0)
            if env_x > W or env_z > D:
                continue
            proj = (env_x * env_z) / (W * D)
            if not (0.30 <= proj <= 0.90):
                continue
            ratio = max(env_x, env_z) / min(env_x, env_z)
            if not (fr["min"] <= ratio <= fr["max"]):
                continue
            in_iqr = fr["p25"] <= ratio <= fr["p75"]
            score = (1 if in_iqr else 0,
                     -abs(ratio - (fr["p25"] + fr["p75"]) / 2), -bw * bd)
            if best is None or score > best[0]:
                best = (score, bw, bd)
    if best is None:
        raise ValueError(f"{brief['brief_id']}: footprint 无可行解（plot {W}x{D}）")
    _, bw, bd = best

    # 居中放置，再按各侧边距（出檐 o；入口侧另加门廊 2）收敛
    bx0 = (W - bw) // 2
    bz0 = (D - bd) // 2
    need_w = o + (apron_need if side == "W" else 0)
    need_e = o + (apron_need if side == "E" else 0)
    need_n = o + (apron_need if side == "N" else 0)
    need_s = o + (apron_need if side == "S" else 0)
    bx0 = min(max(bx0, need_w), W - bw - need_e)
    bz0 = min(max(bz0, need_n), D - bd - need_s)
    bx0, bz0 = max(0, bx0), max(0, bz0)
    footprint = [bx0, bz0, bx0 + bw - 1, bz0 + bd - 1]
    ix0, iz0, ix1, iz1 = bx0 + 1, bz0 + 1, bx0 + bw - 2, bz0 + bd - 2

    # 门开在入口立面中点
    bx1, bz1 = bx0 + bw - 1, bz0 + bd - 1
    if side == "E":
        door_pos = (bx1, bz0 + bd // 2)
    elif side == "W":
        door_pos = (bx0, bz0 + bd // 2)
    elif side == "N":
        door_pos = (bx0 + bw // 2, bz0)
    else:
        door_pos = (bx0 + bw // 2, bz1)
    entrance = {"side": side, "pos": list(door_pos),
                "facing": _FACING_NAME[dvec], "dvec": list(dvec)}

    # ---- 层高与屋顶剖面 ---------------------------------------------------
    # STYLE.<style>.floor_height 区间（无则默认）；assumed_floor_height 优先；
    # 总高 = F*fh + 2(墙顶到屋面基层) + rise ≤ max_height；屋顶占比 ∈ brief 区间（S04）。
    # 屋顶为"逐柱梯形覆盖"（见 _build_roof）：每个屋盖柱都有面层方块，
    # pitch>1 时低层屋面会变密——若超过楼层密度阈值(0.30)会被 P1 楼层启发式
    # 误检为楼板（S06 扣分；该启发式的已知局限，见 score 证据 caveat）。
    # 因此选型评分里加入"屋面稀疏度"估计：ratio 合规优先，其次尽量无假楼板。
    fh_rule = style_rule(res, style, "floor_height")
    assumed = brief["vertical_circulation_constraints"].get("assumed_floor_height", 5)
    lo_r, hi_r = roof_c.get("height_ratio_range", [0.0, 0.5])
    form = roof_c.get("form", "gable")
    base_form = {"curved_gable": "gable", "curved_hip": "hip"}.get(form, form)
    if base_form not in ("gable", "hip"):
        base_form = "gable"                        # form=any → 默认双坡
    span = min(bw, bd) + 2 + 2 * o                 # 坡顶跨度（含墙与出檐）
    span_long = max(bw, bd) + 2 + 2 * o

    def rise_of(pitch_seq):
        """按 inset 序列求达到半跨的层数。"""
        k = 0
        while pitch_seq(k) * 2 < span and k < 64:
            k += 1
        return max(k, 1)

    def inset_uniform(p):
        return lambda k: k * p

    def inset_curved(p):
        # 曲面近似：第一步 2:1（缓），其后 1:1（陡）——阶梯拟合翘角/卷棚
        return lambda k: 0 if k == 0 else (2 + (k - 1))

    def est_false_floor(seq) -> bool:
        """估计屋面任一层实体密度是否 ≥0.30（P1 楼层启发式阈值）。"""
        env_area = span * span_long
        for k in range(0, 16):
            lo_k, hi_k = seq(k), seq(k + 1)
            if lo_k * 2 >= span:
                break
            rows = min(hi_k, (span + 1) // 2) - lo_k    # 本层覆盖的单侧行数
            if rows <= 0:
                continue
            layer_cells = 2 * rows * span_long
            if layer_cells / env_area >= 0.30:
                return True
        return False

    chosen = None
    chimney_extra = 2 if "chimney" in brief.get("special_features", []) else 0
    for fh in [assumed, 5, 4, 6, 7]:
        if fh < 4:                                 # 室内净高 fh-1 ≥ 3（HC_HEADROOM_MIN）
            continue
        if fh_rule and not (fh_rule["min"] <= fh <= fh_rule["max"]):
            continue
        for pitch in ((1,) if form.startswith("curved") else (1, 2, 3, 4)):
            seq = inset_curved(pitch) if form.startswith("curved") else inset_uniform(pitch)
            rise = rise_of(seq)
            total = F * fh + 2 + rise + chimney_extra   # 烟囱高出屋脊 2 格
            if total > H:
                continue
            roof_ratio = rise / total
            ratio_ok = lo_r - 1e-9 <= roof_ratio <= hi_r + 1e-9
            # ratio 合规 > 无假楼板 > fh 接近 assumed > 缓坡
            score = (1 if ratio_ok else 0,
                     0 if est_false_floor(seq) else 1,
                     1 if total >= 0.65 * H else 0,
                     -abs(fh - assumed), -pitch)
            if chosen is None or score > chosen[0]:
                chosen = (score, fh, pitch, rise, total)
    if chosen is None:
        # 兜底：最小合规层高 + 最缓坡（S04 可能扣分，如实记录，不伪造合规）
        fh, pitch = 4, 3
        seq = inset_uniform(pitch)
        rise = rise_of(seq)
    else:
        _, fh, pitch, rise, _total = chosen
    roof_base_y = F * fh + 2
    roof = {"form": form, "base_form": base_form, "base_y": roof_base_y,
            "pitch": pitch, "rise": rise, "overhang": o,
            "curved": form.startswith("curved")}

    # ---- 分区 → 楼层分配 ----------------------------------------------------
    pairs = [tuple(p) for p in brief.get("required_adjacencies", [])]
    forbidden = {tuple(sorted(p)) for p in brief.get("forbidden_adjacencies", [])}
    parent = {z: z for z in interior_zones}

    def find(z):
        while parent[z] != z:
            parent[z] = parent[parent[z]]
            z = parent[z]
        return z

    for a, b in pairs:
        if a in parent and b in parent:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[rb] = ra
    clusters: dict[str, list[str]] = {}
    for z in interior_zones:
        clusters.setdefault(find(z), []).append(z)

    def cluster_key(cl):
        pub = sum(1 for z in cl if z in PUBLIC_ZONES)
        prv = sum(1 for z in cl if z in PRIVATE_ZONES)
        return (-pub, prv, sorted(cl))

    cluster_list = sorted(clusters.values(), key=cluster_key)
    floors_zones: list[list[str]] = [[] for _ in range(F)]
    if F == 1:
        floors_zones[0] = list(interior_zones)
    else:
        for j, cl in enumerate(cluster_list):
            floors_zones[min(j, F - 1)].extend(cl)
    # 私密区不上地面层（grammar 弱代理：上层私密，INFERRED）
    for z in list(floors_zones[0]):
        if z in PRIVATE_ZONES and F >= 2:
            floors_zones[0].remove(z)
            floors_zones[F - 1].append(z)
    # 外部 zone（如 watch_platform）→ 顶层外侧阳台平台（DOOR 块门连通；
    # 不用门洞开口——无门开口会让洪泛把室内判定为外部，P2 实测教训）。
    # 其邻接对伙伴拉上同层（邻接=经阳台门可通）。
    balcony = None
    for z in exterior_zones:
        balcony = {"zone": z, "floor": F - 1, "min_area": zc[z]["min_area"]}
        for a, b_ in pairs:
            partner = b_ if a == z else (a if b_ == z else None)
            if partner in interior_zones:
                for fi in range(F):
                    if partner in floors_zones[fi]:
                        floors_zones[fi].remove(partner)
                        floors_zones[F - 1].append(partner)
    # 容量回退：任一层超载则把最后的簇上移
    floor_area = (bw - 2) * (bd - 2)
    for fi in range(F):
        while sum(zc[z]["min_area"] for z in floors_zones[fi]) > floor_area * 0.80 \
                and fi + 1 < F and floors_zones[fi]:
            floors_zones[fi + 1].append(floors_zones[fi].pop())

    # ---- 每层房间划分（带状 guillotine） -----------------------------------
    # CIR-G-01：主入口直入主空间——把最公共 zone 分到门所在带；
    # 邻接对放相邻带；禁配对之间无开口。
    rooms: list[dict] = []
    partitions: list[dict] = []
    dpx, dpz = entrance["pos"]
    door_inner = (dpx - dvec[0], dpz - dvec[1])
    for fi in range(F):
        zs = floors_zones[fi]
        if not zs:
            continue
        order = sorted(zs, key=lambda z: (z not in PUBLIC_ZONES, z))
        for a, b_ in pairs:                        # 邻接对排相邻
            if a in order and b_ in order:
                ia, ib = order.index(a), order.index(b_)
                if abs(ia - ib) != 1:
                    order.insert(min(ia + 1, len(order) - 1), order.pop(ib))
        long_x = (ix1 - ix0) >= (iz1 - iz0)
        L = (ix1 - ix0 + 1) if long_x else (iz1 - iz0 + 1)
        n_bands = len(order)
        wall_gap = n_bands - 1                    # 隔墙厚度：带间各留 1 格墙线
        usable = L - wall_gap
        total_need = sum(zc[z]["min_area"] for z in order)
        widths = [max(3, round(usable * zc[z]["min_area"] / total_need)) for z in order]
        while sum(widths) > usable:
            i = max(range(len(widths)), key=lambda t: widths[t])
            widths[i] -= 1
        while sum(widths) < usable:
            widths[-1] += 1
        shift = ov.get("partition_shift", {}).get(str(fi))
        if shift and len(widths) >= 2 and widths[1] - shift >= 3:
            widths[0] += shift
            widths[1] -= shift
        # 先算带的几何位置（带间留 1 格隔墙线，墙不占任何房间面积）
        bands = []
        cursor = ix0 if long_x else iz0
        for w in widths:
            if long_x:
                bands.append([cursor, iz0, cursor + w - 1, iz1])
            else:
                bands.append([ix0, cursor, ix1, cursor + w - 1])
            cursor += w + 1
        # 再把 zone 排到带上：order[0]（最公共）落门所在带（仅地面层）
        assignment: list[str | None] = [None] * len(order)
        rest = list(order)
        if fi == 0 and len(order) > 1:
            di = next((i for i, r in enumerate(bands)
                       if r[0] <= door_inner[0] <= r[2]
                       and r[1] <= door_inner[1] <= r[3]), 0)
            assignment[di] = rest.pop(0)
        for z in rest:
            # 邻接伙伴已排 → 相邻空带；否则第一个空带
            put = None
            for a, b_ in pairs:
                if z == a and b_ in assignment:
                    j = assignment.index(b_)
                    put = next((t for t in (j - 1, j + 1)
                                if 0 <= t < len(order) and assignment[t] is None), None)
                elif z == b_ and a in assignment:
                    j = assignment.index(a)
                    put = next((t for t in (j - 1, j + 1)
                                if 0 <= t < len(order) and assignment[t] is None), None)
            if put is None:
                put = assignment.index(None)
            assignment[put] = z
        for band, z in zip(bands, assignment):
            rooms.append({"floor": fi, "zone": z, "rect": band})
        for zi in range(len(bands) - 1):           # 相邻带的隔墙与开口
            a, b_ = assignment[zi], assignment[zi + 1]
            is_forbidden = tuple(sorted((a, b_))) in forbidden
            ra, rb = bands[zi], bands[zi + 1]
            if long_x:
                wall = {"floor": fi, "axis": "x", "pos": ra[2] + 1,
                        "span": [max(ra[1], rb[1]), min(ra[3], rb[3])]}
            else:
                wall = {"floor": fi, "axis": "z", "pos": ra[3] + 1,
                        "span": [max(ra[0], rb[0]), min(ra[2], rb[2])]}
            if wall["span"][0] > wall["span"][1]:
                continue
            if not is_forbidden:
                mid = (wall["span"][0] + wall["span"][1]) // 2
                wall["opening_at"] = mid
            partitions.append(wall)

    # ---- 阳台平台（外部 zone 的物理实现） ------------------------------------
    # 顶层外墙外侧 3×4 悬挑平台 + 栏板 + 墙上 DOOR 块门。阳台选入口立面的
    # 对侧（deterministic）；边距不足 3 格时收缩到 2 格（plot 内）。
    roof["rect"] = [bx0, bz0, bx1, bz1]
    if balcony is not None:
        fi = balcony["floor"]
        opp = {"E": "W", "W": "E", "S": "N", "N": "S"}[side]
        dvx, dvz = _DIRECTION_VEC[opp]
        # 平台沿墙宽 7、向外深 3（不足则收缩）：栏板外沿后净站位
        # (depth-1)×(width-2)，对着 zone min_area 尺寸
        if opp in ("E", "W"):
            wx = bx1 if opp == "E" else bx0
            depth = 3 if (0 <= wx + dvx * 3 < W) else 2
            half = 3
            cz = min(max(bz0 + half + 1, bz0 + bd // 2), bz1 - half - 1)
            rect = [min(wx + dvx, wx + dvx * depth), cz - half,
                    max(wx + dvx, wx + dvx * depth), cz + half]
            door_at = [wx, cz]
            if not (0 <= rect[0] and rect[2] < W):
                rect = None
        else:
            wz = bz1 if opp == "S" else bz0
            depth = 3 if (0 <= wz + dvz * 3 < D) else 2
            half = 3
            cx = min(max(bx0 + half + 1, bx0 + bw // 2), bx1 - half - 1)
            rect = [cx - half, min(wz + dvz, wz + dvz * depth),
                    cx + half, max(wz + dvz, wz + dvz * depth)]
            door_at = [cx, wz]
            if not (0 <= rect[1] and rect[3] < D):
                rect = None
        if rect is not None:
            # Revision 覆盖：沿墙平移阳台门（单轮可能把门放在楼梯洞口旁）
            shift = ov.get("balcony_door_shift", 0)
            if shift:
                if opp in ("E", "W"):
                    cz2 = min(max(door_at[1] + shift, rect[1]), rect[3])
                    rect[1], rect[3] = min(rect[1], cz2), max(rect[3], cz2)
                    door_at = [door_at[0], cz2]
                else:
                    cx2 = min(max(door_at[0] + shift, rect[0]), rect[2])
                    rect[0], rect[2] = min(rect[0], cx2), max(rect[2], cx2)
                    door_at = [cx2, door_at[1]]
            balcony.update({"side": opp, "rect": rect, "door_at": door_at,
                            "dvec": [dvx, dvz]})
            rooms.append({"floor": fi, "zone": balcony["zone"],
                          "rect": rect, "exterior": True})
        else:
            balcony = None                        # 地块放不下 → 如实缺区（F01 扣）

    plan = {
        "footprint": footprint, "interior": [ix0, iz0, ix1, iz1],
        "floors": F, "floor_height": fh, "slab_ys": [i * fh for i in range(F)],
        "wall_top_y": F * fh + 1, "roof": roof,
        "entrance": entrance, "rooms": rooms, "partitions": partitions,
        "balcony": balcony, "style": style,
        "protected_cells": [],                        # 设计性开口（seal 保护）
        "palette_params": {
            "wall_wood_fraction": 0.30,
            "floor_stone_fraction": 0.5,
            "carpet_coverage": 0.25 if "decorative" in
                brief["palette_constraints"].get("family_ratio_ranges", {}) else 0.0,
            "roof_family": "stone" if style in ("Chinese", "Japanese") else "wood",
            "window_stride": 4,
            **ov.get("palette_params", {}),
        },
        "shaft_shift": ov.get("shaft_shift", {}),
    }
    return plan


# ---------------------------------------------------------------------------
# 2. 体素构建
# ---------------------------------------------------------------------------
class Builder:
    """cells: (x,y,z) → block state；tags: (x,y,z) → 元素名（供 Revision 定向修改）。"""

    def __init__(self):
        self.cells: dict[tuple[int, int, int], str] = {}
        self.tags: dict[tuple[int, int, int], str] = {}

    def put(self, x, y, z, state, tag):
        self.cells[(x, y, z)] = state
        self.tags[(x, y, z)] = tag

    def remove(self, x, y, z):
        self.cells.pop((x, y, z), None)
        self.tags.pop((x, y, z), None)

    def solid(self, x, y, z):
        return (x, y, z) in self.cells


def _stair_state(mat_key: str, facing: str) -> str:
    return f"{MAT[mat_key]}[facing={facing},half=bottom,shape=straight]"


def _inset_at(plan_roof: dict, k: int) -> int:
    """第 k 层屋面相对屋盖边的内缩格数（uniform / curved 两种剖面）。"""
    if plan_roof.get("curved"):
        return 0 if k == 0 else (2 + (k - 1))
    return k * plan_roof["pitch"]


def build_voxels(brief: dict, plan: dict, res: dict) -> Builder:
    b = Builder()
    bx0, bz0, bx1, bz1 = plan["footprint"]
    ix0, iz0, ix1, iz1 = plan["interior"]
    F, fh = plan["floors"], plan["floor_height"]
    pp = plan["palette_params"]
    ent = plan["entrance"]
    roof = plan["roof"]
    balcony = plan.get("balcony")
    wt = plan["wall_top_y"]
    dpx, dpz = ent["pos"]
    dx, dz = ent["dvec"]

    # ---- 楼板（全 footprint 满铺，含墙下；楼层密度启发式 ≥0.3 由此保证） ----
    # 地面层石/木按 floor_stone_fraction 确定性混铺（拟合旋钮；语法依据：
    # foundation_stone_base 只约束墙基座，楼板材质是自由度）。
    floor_stone_frac = pp.get("floor_stone_fraction", 0.5)
    for fi, sy in enumerate(plan["slab_ys"]):
        for x in range(bx0, bx1 + 1):
            for z in range(bz0, bz1 + 1):
                t = ((x * 3 + z * 5 + fi * 11) % 100) / 100.0
                mat = MAT["foundation"] if t < floor_stone_frac else MAT["floor"]
                b.put(x, sy, z, mat, f"slab_f{fi}")

    # ---- 外墙（y=slab+1..wall_top_y；底层 stone 基座，以上按
    #       wall_wood_fraction 确定性混砌） -----------------------------------
    wood_frac = pp["wall_wood_fraction"]
    for fi, sy in enumerate(plan["slab_ys"]):
        y_lo, y_hi = sy + 1, (wt if fi == F - 1 else plan["slab_ys"][fi + 1])
        wall_cells = ([(x, z) for x in range(bx0, bx1 + 1) for z in (bz0, bz1)]
                      + [(x, z) for z in range(bz0 + 1, bz1) for x in (bx0, bx1)])
        for x, z in wall_cells:
            for y in range(y_lo, y_hi + 1):
                corner = (x in (bx0, bx1)) and (z in (bz0, bz1))
                if y == 1 or corner:
                    mat = MAT["wall_stone"]
                else:
                    t = ((x * 7 + z * 13 + y * 3) % 100) / 100.0
                    mat = MAT["wall_wood"] if t < wood_frac else MAT["wall_stone"]
                b.put(x, y, z, mat, "wall")

    # ---- 楼梯井计划层落位（VA-G-01/02 的二维转译；三维盲区见模块 docstring） ----
    # 先按"每层独立直跑"落位；任一过渡不可行则整楼退化为"折返楼梯塔"
    # （相邻两柱、逐层换向——上下行梯段在层平面上互不竖向重叠，
    # 且上段底步恰好是下段顶步的侧邻：V006 顶部落点天然成立）。
    shafts = []
    if F >= 2:
        door_clear = {(dpx - dx * k, dpz - dz * k) for k in range(1, 3)}
        try:
            for i in range(F - 1):
                shafts.append(_place_shaft(plan, i,
                                           door_clear if i == 0 else set(), shafts))
        except ValueError:
            shafts = _place_switchback(plan, door_clear, F)
    plan["shafts"] = shafts                       # 记入元数据（Revision 定向修复用）
    for sh in shafts:
        _build_shaft(b, plan, sh)
    hole_cols = set()
    step_cols = set()
    for sh in shafts:
        hole_cols |= set(sh["hole_cols"])
        step_cols |= set(sh["step_cols"])

    # ---- 屋顶（先于隔墙构建：顶层隔墙要"填到屋面"，依赖屋面实体已存在） ----------
    _build_roof(b, plan)

    # ---- 隔墙（到上一层楼板底；顶层一直填到屋面，消除"墙顶走道"——
    #       墙顶是可站表面，悬空于房间内会形成孤立内部连通分量，V004 实测） ------
    for pt in plan["partitions"]:
        sy = plan["slab_ys"][pt["floor"]]
        y_top = wt if pt["floor"] == F - 1 else plan["slab_ys"][pt["floor"] + 1]
        lo, hi = pt["span"]
        for t in range(lo, hi + 1):
            x, z = (pt["pos"], t) if pt["axis"] == "x" else (t, pt["pos"])
            if (x, z) in hole_cols or (x, z) in step_cols:
                continue                          # 井柱位整柱留空（楼梯穿过）
            is_opening = pt.get("opening_at") == t
            yy = sy + 1
            while True:
                if is_opening and yy <= sy + 2:
                    yy += 1                       # 1×2 门洞（其上封到屋面）
                    continue
                if b.solid(x, yy, z):
                    break                         # 撞到上一层楼板/屋面 → 到顶
                if pt["floor"] != F - 1 and yy >= y_top:
                    break                         # 非顶层：到上一层楼板底为止
                if yy > y_top + plan["roof"]["rise"] + 2:
                    break                         # 保险上限（屋面必定先撞到）
                b.put(x, yy, z, MAT["partition"], "partition")
                yy += 1

    # ---- 主入口门 + 门廊（GA-002/GA-003） ------------------------------------
    facing = ent["facing"]
    b.put(dpx, 1, dpz,
          f"{MAT['door']}[facing={facing},half=lower,hinge=left,open=false]", "door")
    b.put(dpx, 2, dpz,
          f"{MAT['door']}[facing={facing},half=upper,hinge=left,open=false]", "door")
    dx, dz = ent["dvec"]
    px, pz = (-dz, dx)
    for k in range(1, 3):                          # 门外 2 深 × 3 宽石板（V002 接近位）
        for w in (-1, 0, 1):
            ax, az = dpx + dx * k + px * w, dpz + dz * k + pz * w
            if not b.solid(ax, 0, az):
                b.put(ax, 0, az, MAT["foundation"], "apron")

    # ---- 窗户（glass，FULL 封围护；密度 stride 由 fit 阶段可调） --------------
    stride = max(3, int(pp.get("window_stride", 4)))
    for fi, sy in enumerate(plan["slab_ys"]):
        wy = sy + 2
        if wy > wt - 1:
            continue
        for x, z in ([(x, bz0) for x in range(ix0, ix1 + 1)]
                     + [(x, bz1) for x in range(ix0, ix1 + 1)]
                     + [(bx0, z) for z in range(iz0, iz1 + 1)]
                     + [(bx1, z) for z in range(iz0, iz1 + 1)]):
            if (x + z + fi) % stride != 1:
                continue
            if abs(x - dpx) + abs(z - dpz) <= 1 and fi == 0:
                continue                           # 主入口门旁不开窗
            if balcony is not None and fi == balcony["floor"] and \
                    abs(x - balcony["door_at"][0]) + abs(z - balcony["door_at"][1]) <= 1:
                continue                           # 阳台门旁不开窗
            b.put(x, wy, z, MAT["glass"], "window")

    # ---- 阳台平台（外部 zone：悬挑板 + 栏板 + 墙上 DOOR 门） -------------------
    if balcony is not None:
        _build_balcony(b, plan)

    # ---- 烟囱（special_features 含 chimney 时） --------------------------------
    if "chimney" in brief.get("special_features", []):
        rcx0, rcz0, rcx1, rcz1 = roof["rect"]
        cx, cz = rcx0 + 1, rcz0 + 1                 # 屋盖内角部
        if (cx, cz) in step_cols or (cx, cz) in hole_cols:
            cx, cz = rcx1 - 1, rcz0 + 1
        top = roof["base_y"] + roof["rise"] + 2
        for y in range(1, top + 1):
            b.put(cx, y, cz, MAT["chimney"], "chimney")

    # ---- 室内装饰（地毯 + 灯笼，coverage 由 fit 阶段控制） ----------------------
    _decorate(b, plan, pp["carpet_coverage"])

    # ---- 设计性开口保护登记（seal_envelope 跳过 ±1 格；DOOR 块对洪泛是实体，
    # 主入口/阳台门天然被保护，此处仅兜底） -------------------------------------
    for (x, y, z), t in b.tags.items():
        if t == "door":
            for ddx in (-1, 0, 1):
                for ddy in (-1, 0, 1):
                    for ddz in (-1, 0, 1):
                        plan["protected_cells"].append([x + ddx, y + ddy, z + ddz])
    return b


def _place_shaft(plan: dict, from_floor: int, door_clear: set,
                 existing: list[dict]) -> dict:
    """为 from_floor → from_floor+1 选择楼梯井（直跑，沿外墙内侧 1 格）。

    计划层检查（规则直译）：跑道 fh 步 + 1 接近格都在室内、不撞门 clearance、
    不与其他井柱位重叠；顶部继续向前的落点格只作加分项、**不作硬约束**
    （单轮盲区；C 路线由 Validator V006 实测兜底）。
    """
    ix0, iz0, ix1, iz1 = plan["interior"]
    fh = plan["floor_height"]
    shift = plan.get("shaft_shift", {}).get(str(from_floor), 0)
    taken = set(door_clear)
    for sh in existing:
        taken |= set(sh["step_cols"]) | set(sh["hole_cols"]) | {tuple(sh["approach"])}
    # 跑道线：四条内墙线（方向 = 沿线方向）
    lines = [("N", (1, 0), [(x, iz0) for x in range(ix0, ix1 + 1)]),
             ("S", (1, 0), [(x, iz1) for x in range(ix0, ix1 + 1)]),
             ("W", (0, 1), [(ix0, z) for z in range(iz0, iz1 + 1)]),
             ("E", (0, 1), [(ix1, z) for z in range(iz0, iz1 + 1)])]
    cands = []
    for wname, dvec, line in lines:
        for start_i in range(len(line)):
            run = []
            ok = True
            for j in range(fh + 1):                # 1 接近格 + fh 步
                idx = start_i + j + shift
                if idx >= len(line):
                    ok = False
                    break
                cell = line[idx]
                if cell in taken:
                    ok = False
                    break
                run.append(cell)
            if not ok:
                continue
            approach, steps = run[0], run[1:]
            cont_i = start_i + fh + 1 + shift       # 顶部继续向前落点格
            cont_ok = cont_i < len(line) and line[cont_i] not in taken
            # 顶步侧翼（垂直跑道方向）是否朝室内开敞（加分，不强制）
            dx, dz = dvec
            side_free = 0
            tx, tz = steps[-1]
            for sx, sz in ((-dz, dx), (dz, -dx)):
                nx, nz = tx + sx, tz + sz
                if ix0 <= nx <= ix1 and iz0 <= nz <= iz1:
                    side_free += 1
            score = (1 if cont_ok else 0, side_free, -start_i)
            cands.append((score, wname, dvec, approach, steps))
    if not cands:
        raise ValueError(f"floor {from_floor}: 无可行楼梯井（run={fh}+1）")
    cands.sort(key=lambda c: c[0], reverse=True)
    _, wname, dvec, approach, steps = cands[0]
    # 顶部两步的上方楼板需开洞（站位净高 v1/v2 沿跑道传递）：
    # 步 j（y=sy0+1+j）要求 v1/v2 无实体 → 倒二(j=fh-3)的 v2 与倒一(j=fh-2)的 v1
    # 落在楼板面 sy1=sy0+fh → 开洞柱位 = step_cols[fh-3], step_cols[fh-2]；
    # 顶步(j=fh-1)占据楼板格本身（楼梯替代楼板）。
    hole_cols = steps[-3:-1] if fh >= 3 else []
    return {"from_floor": from_floor, "wall": wname, "dvec": list(dvec),
            "approach": approach, "step_cols": list(steps),
            "hole_cols": list(hole_cols),
            "base_y": plan["slab_ys"][from_floor]}


def _place_switchback(plan: dict, door_clear: set, F: int) -> list[dict]:
    """折返楼梯塔（紧张地块兜底）：两条相邻柱、逐层换向。

    几何论证（与 walkability 边规则对齐）：
    - 上段底步（colB, 索引 s+fh-1, y=sy+1）与下段顶步（colA, 同索引, y=sy）
      侧邻且 ΔE=1.0、双端支撑均为楼梯 → 合法边；下段顶步因此总有"向上"出口
      （V006 对每段都满足）；
    - 两段在 y 区间上错开一层楼板，竖向无重叠（净高冲突不存在）；
    - 26 连通聚类会把全塔并为一个 cluster：V005 只看塔底（flight0 底步，
      接近格在 colA[s-1]），V006 只看塔顶（末段顶步，其侧邻为另一柱的
      楼板格 → 同级落点）。
    """
    ix0, iz0, ix1, iz1 = plan["interior"]
    fh = plan["floor_height"]
    walls = [("N", (1, 0), [(x, iz0) for x in range(ix0, ix1 + 1)],
              [(x, iz0 + 1) for x in range(ix0, ix1 + 1)]),
             ("S", (1, 0), [(x, iz1) for x in range(ix0, ix1 + 1)],
              [(x, iz1 - 1) for x in range(ix0, ix1 + 1)]),
             ("W", (0, 1), [(ix0, z) for z in range(iz0, iz1 + 1)],
              [(ix0 + 1, z) for z in range(iz0, iz1 + 1)]),
             ("E", (0, 1), [(ix1, z) for z in range(iz0, iz1 + 1)],
              [(ix1 - 1, z) for z in range(iz0, iz1 + 1)])]
    chosen = None
    for wname, dvec, col_a, col_b in walls:
        n = len(col_a)
        for s in range(1, n - fh):            # 需 colA[s-1] 与 colB[s+fh] 存在
            flight0 = [col_a[s - 1 + j] for j in range(fh + 1)]
            if any(c in door_clear for c in flight0):
                continue
            chosen = (wname, dvec, col_a, col_b, s)
            break
        if chosen:
            break
    if chosen is None:
        raise ValueError(f"折返楼梯塔无可行位置（需内墙线 ≥ fh+2={fh + 2}）")
    wname, dvec, col_a, col_b, s = chosen
    shafts = []
    for i in range(F - 1):
        col = col_a if i % 2 == 0 else col_b
        if i % 2 == 0:                        # dir=+1：底步在索引 s
            steps = [col[s + j] for j in range(fh)]
            approach = col[s - 1]
        else:                                 # dir=-1：底步在索引 s+fh-1
            steps = [col[s + fh - 1 - j] for j in range(fh)]
            approach = col[s + fh]
        hole_cols = steps[-3:-1] if fh >= 3 else []
        shafts.append({"from_floor": i, "wall": wname, "dvec": list(dvec),
                       "approach": approach, "step_cols": list(steps),
                       "hole_cols": list(hole_cols), "mode": "switchback",
                       "base_y": plan["slab_ys"][i]})
    return shafts


def _build_shaft(b: Builder, plan: dict, sh: dict) -> None:
    """构建直跑楼梯 + 上一层楼板开洞。

    步 j 位于 step_cols[j]、y=base_y+1+j（E=+0.5/步；相邻步 ΔE=1.0 且支撑为
    楼梯 → 可走，见 walkability 边规则）；顶步 y=上一层楼板面（楼梯替代楼板格，
    落点 ΔE=0.5）；facing=上行方向（生成约定，Validator 不依赖该属性）。
    """
    sy0 = sh["base_y"]
    dx, dz = sh["dvec"]
    face = _FACING_NAME[(dx, dz)]
    for j, (x, z) in enumerate(sh["step_cols"]):
        b.put(x, sy0 + 1 + j, z, _stair_state("stair", face), "stair")
    sy1 = sy0 + plan["floor_height"]
    for x, z in sh["hole_cols"]:
        b.remove(x, sy1, z)


def _build_balcony(b: Builder, plan: dict) -> None:
    """阳台平台：外部 zone（如 watch_platform）的物理实现。

    - 平台板：balcony.rect 区域在该层楼板高程 sy 满铺石板；
    - 栏板：平台外沿一圈 FENCE（跳过靠墙侧与门线）；
    - 门：外墙 door_at 处放 DOOR 块（facing 朝外）——DOOR 对洪泛是实体、
      对 walkability 可通行，内外判定与连通性两不误（无门开口会导致
      室内/外洪泛互通，P2 教训）。
    """
    bal = plan["balcony"]
    fi = bal["floor"]
    sy = plan["slab_ys"][fi]
    rx0, rz0, rx1, rz1 = bal["rect"]
    dvx, dvz = bal["dvec"]
    door_x, door_z = bal["door_at"]
    facing = _FACING_NAME[(dvx, dvz)]
    for x in range(rx0, rx1 + 1):
        for z in range(rz0, rz1 + 1):
            b.put(x, sy, z, MAT["foundation"], "balcony_slab")
    # 栏板：平台外沿，但跳过靠墙内沿（栏板会堵门线）
    skip_x = rx1 if dvx < 0 else (rx0 if dvx > 0 else None)   # 靠墙内沿列
    skip_z = rz1 if dvz < 0 else (rz0 if dvz > 0 else None)
    for x in range(rx0, rx1 + 1):
        for z in (rz0, rz1):
            if z == skip_z:
                continue
            b.put(x, sy + 1, z, MAT["fence"], "balcony_rail")
    for z in range(rz0, rz1 + 1):
        for x in (rx0, rx1):
            if x == skip_x:
                continue
            b.put(x, sy + 1, z, MAT["fence"], "balcony_rail")
    # 门（墙上，面朝阳台）
    b.put(door_x, sy + 1, door_z,
          f"{MAT['door']}[facing={facing},half=lower,hinge=left,open=false]", "door")
    b.put(door_x, sy + 2, door_z,
          f"{MAT['door']}[facing={facing},half=upper,hinge=left,open=false]", "door")


def _build_roof(b: Builder, plan: dict) -> None:
    """坡顶构建：逐柱梯形覆盖（per-column terraced surface）。

    对屋盖矩形（墙线 + 出檐）内每个 (x,z) 柱：
      t = 柱到屋盖边的水平距离（gable 只算垂直于脊的方向；hip 取四边最小）
      k = level_of(t)：满足 inset(k) ≤ t 的最大层号 → 面层位于 base_y + k
      方块：踏步沿（t == inset(k)）用楼梯（facing=下坡向，外观约定），
            踏面用半砖（bottom slab，0.5 高实体）——两种都是实体，保证密封。

    密封不变量（供 V010/V011）：
    - 任一室内柱最高空气格上方必有面层实体（逐柱覆盖）；
    - 外墙线柱在面层以下（base_y .. base_y+k-1）用 wall_stone 填实——
      山墙三角与檐口楔由此统一封住（墙顶 wt = base_y - 1，垂直接续）。
    残留泄漏由 seal_envelope 洪泛兜底。

    注意：pitch>1 时屋面基层会变密（每 pitch 行才升一层），可能超过
    P1 楼层密度阈值 0.30 → 被误检为"楼板"（S06 扣分的已知启发式局限，
    在 plan 选型时已优先规避，见 est_false_floor）。
    """
    roof = plan["roof"]
    o, base_y = roof["overhang"], roof["base_y"]
    pp = plan["palette_params"]
    fam = pp["roof_family"]
    stair_key = "roof_stair_stone" if fam == "stone" else "roof_stair_wood"
    slab_state = "minecraft:stone_brick_slab[type=bottom]" if fam == "stone" \
        else "minecraft:oak_slab[type=bottom]"
    wx0, wz0, wx1, wz1 = roof["rect"]               # 被覆盖的墙线矩形
    rx0, rz0, rx1, rz1 = wx0 - o, wz0 - o, wx1 + o, wz1 + o
    span_x, span_z = rx1 - rx0 + 1, rz1 - rz0 + 1

    def level_of(t: int) -> int:
        k = 0
        while _inset_at(roof, k + 1) <= t:
            k += 1
        return k

    along_x = span_x >= span_z                      # gable 脊沿长轴
    ring_cols = ([(x, z) for x in range(wx0, wx1 + 1) for z in (wz0, wz1)]
                 + [(x, z) for z in range(wz0 + 1, wz1) for x in (wx0, wx1)])
    ring_set = set(ring_cols)

    for x in range(rx0, rx1 + 1):
        for z in range(rz0, rz1 + 1):
            if roof["base_form"] == "gable":
                t = min(z - rz0, rz1 - z) if along_x else min(x - rx0, rx1 - x)
                if along_x:
                    facing = "north" if (z - rz0) <= (rz1 - z) else "south"
                else:
                    facing = "west" if (x - rx0) <= (rx1 - x) else "east"
            else:  # hip：四边取最近边，并列时按固定顺序（确定性）
                dists = [(z - rz0, "north"), (rz1 - z, "south"),
                         (x - rx0, "west"), (rx1 - x, "east")]
                t, facing = min(dists, key=lambda d: d[0])
            k = level_of(t)
            riser = (t == _inset_at(roof, k))
            state = _stair_state(stair_key, facing) if riser else slab_state
            b.put(x, base_y + k, z, state, "roof")
            # 墙线柱：面层以下填实（山墙三角 + 檐口楔统一封口）
            if (x, z) in ring_set:
                for y in range(base_y, base_y + k):
                    if not b.solid(x, y, z):
                        b.put(x, y, z, MAT["wall_stone"], "eave_fill")


def _decorate(b: Builder, plan: dict, carpet_coverage: float) -> None:
    """地毯（CARPET 可站）+ 沿墙灯笼（NONSOLID）。

    地毯只铺室内楼板格，避开井柱位/洞口/门口通路（门内外 2 格）。
    覆盖图案确定性：(x*5+z*11+floor*7) % 100 < coverage*100。
    """
    ix0, iz0, ix1, iz1 = plan["interior"]
    ent = plan["entrance"]
    dx, dz = ent["dvec"]
    dpx, dpz = ent["pos"]
    door_path = {(dpx - dx * k, dpz - dz * k) for k in range(0, 3)}
    # 隔墙门洞柱（1×2 开口）也不铺地毯/压板——保持门洞为纯空气通道
    for pt in plan.get("partitions", []):
        if pt.get("opening_at") is not None:
            t = pt["opening_at"]
            x, z = (pt["pos"], t) if pt["axis"] == "x" else (t, pt["pos"])
            door_path.add((x, z))
    step_cols = {(x, z) for (x, y, z), t in b.tags.items() if t == "stair"}
    for fi, sy in enumerate(plan["slab_ys"]):
        for x in range(ix0, ix1 + 1):
            for z in range(iz0, iz1 + 1):
                if (x, z) in door_path or (x, z) in step_cols:
                    continue
                if not b.solid(x, sy, z):
                    continue                        # 楼板洞口
                if ((x * 5 + z * 11 + fi * 7) % 100) < carpet_coverage * 100:
                    b.put(x, sy + 1, z, MAT["carpet"], "carpet")
    for fi, sy in enumerate(plan["slab_ys"]):
        for x in range(ix0, ix1 + 1):
            if (x + fi) % 6 == 2 and not b.solid(x, sy + 1, iz0) \
                    and (x, iz0) not in door_path and (x, iz0) not in step_cols:
                b.put(x, sy + 1, iz0, MAT["lantern"], "lantern")
    # 压力板点缀（functional 族，0.1 高薄片可站，不产生孤立站位）：
    # 材料拟合的"稀释"旋钮——stone/wood 双高超界时只能靠提高其它族占比收敛。
    plate_density = plan["palette_params"].get("plate_density", 0.02)
    if plate_density > 0:
        for fi, sy in enumerate(plan["slab_ys"]):
            for x in range(ix0, ix1 + 1):
                for z in range(iz0, iz1 + 1):
                    if (x, z) in door_path or (x, z) in step_cols:
                        continue
                    if b.solid(x, sy + 1, z) or not b.solid(x, sy, z):
                        continue
                    if ((x * 13 + z * 17 + fi * 3) % 100) < plate_density * 100:
                        b.put(x, sy + 1, z, MAT["plate"], "plate")


# ---------------------------------------------------------------------------
# 3. 围护密闭自检（GA-002/GA-005 → V010/V011 的生成侧预防）
# ---------------------------------------------------------------------------
def seal_envelope(b: Builder, plan: dict) -> int:
    """6 连通洪泛（自扩展包络边界）找"室内⇄室外"泄漏格并填墙。

    跳过 plan["protected_cells"]（门/设计性开口 ±1 格，与 V010 opening_margin
    口径一致）。返回填补格数。迭代 ≤5 轮（填补可能暴露新泄漏面）。
    """
    protected = {tuple(c) for c in plan.get("protected_cells", [])}
    filled_total = 0
    for _ in range(5):
        xs = [c[0] for c in b.cells]
        ys = [c[1] for c in b.cells]
        zs = [c[2] for c in b.cells]
        x0, y0, z0 = min(xs) - 1, min(ys) - 1, min(zs) - 1
        X = max(xs) - x0 + 2
        Y = max(ys) - y0 + 2
        Z = max(zs) - z0 + 2
        solid = set(b.cells)
        seen: set[tuple[int, int, int]] = set()
        dq: deque = deque()
        for x in range(x0, x0 + X):
            for y in range(y0, y0 + Y):
                for z in (z0, z0 + Z - 1):
                    c = (x, y, z)
                    if c not in solid:
                        seen.add(c)
                        dq.append(c)
        for x in range(x0, x0 + X):
            for z in range(z0, z0 + Z):
                for y in (y0, y0 + Y - 1):
                    c = (x, y, z)
                    if c not in solid and c not in seen:
                        seen.add(c)
                        dq.append(c)
        for y in range(y0, y0 + Y):
            for z in range(z0, z0 + Z):
                for x in (x0, x0 + X - 1):
                    c = (x, y, z)
                    if c not in solid and c not in seen:
                        seen.add(c)
                        dq.append(c)
        while dq:
            cx, cy, cz = dq.popleft()
            for ddx, ddy, ddz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0),
                                  (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                n = (cx + ddx, cy + ddy, cz + ddz)
                if n in solid or n in seen:
                    continue
                if not (x0 <= n[0] < x0 + X and y0 <= n[1] < y0 + Y
                        and z0 <= n[2] < z0 + Z):
                    continue
                seen.add(n)
                dq.append(n)
        # 泄漏格 = 非实体、非外部空气、6 邻接外部空气（限扩展盒内，盒外不算）
        leaks = set()
        for cx, cy, cz in seen:
            for ddx, ddy, ddz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0),
                                  (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                n = (cx + ddx, cy + ddy, cz + ddz)
                if not (x0 < n[0] < x0 + X - 1 and y0 < n[1] < y0 + Y - 1
                        and z0 < n[2] < z0 + Z - 1):
                    continue
                if n in solid or n in seen or n in protected:
                    continue
                leaks.add(n)
        if not leaks:
            break
        for x, y, z in leaks:
            b.put(x, y, z, MAT["wall_stone"], "seal_fill")
        filled_total += len(leaks)
    return filled_total


# ---------------------------------------------------------------------------
# 4. 材料族占比拟合（确定性迭代重建）
# ---------------------------------------------------------------------------
def measure_family_ratios(b: Builder, res: dict) -> tuple[dict, str, int]:
    fams = res["palette_dictionary"]["families"]
    counts: dict[str, int] = {}
    non_air = 0
    for state in b.cells.values():
        bid = state.split("[")[0]
        non_air += 1
        fam = family_of(bid, fams)
        counts[fam] = counts.get(fam, 0) + 1
    ratios = {f: round(c / non_air, 4) for f, c in sorted(counts.items())}
    dominant = max(counts, key=counts.get) if counts else "UNKNOWN"
    return ratios, dominant, non_air


def fit_palette(brief: dict, res: dict, overrides: dict | None = None,
                max_iter: int = 20) -> tuple[Builder, dict, dict]:
    """重建循环：构建 → 量占比 → 调参数，直到全部约束族入界或次数耗尽。

    调整旋钮（全部确定性，无 RNG）：wall_wood_fraction（石/木天平）、
    carpet_coverage（decorative 主旋钮）、roof_family（粗调）、
    window_stride（glass 超限修剪）。拟合历史完整记录：拟合不成时残留
    偏差进入评分，不掩饰。
    """
    ranges = brief["palette_constraints"].get("family_ratio_ranges", {})
    plan = plan_from_brief(brief, res, overrides)
    history = []
    pp = dict(plan["palette_params"])
    b = None
    steps = {"wall_wood_fraction": 0.10, "floor_stone_fraction": 0.15,
             "carpet_coverage": 0.10}
    last_dir: dict[str, int] = {}
    for it in range(max_iter):
        plan["palette_params"] = dict(pp)
        plan["protected_cells"] = []
        b = build_voxels(brief, plan, res)
        seal_n = seal_envelope(b, plan)
        ratios, dominant, non_air = measure_family_ratios(b, res)
        bad = {}
        for f, (lo, hi) in ranges.items():
            rv = ratios.get(f, 0.0)
            if rv < lo - 1e-9 or rv > hi + 1e-9:
                bad[f] = {"ratio": rv, "range": [lo, hi]}
        history.append({"iter": it, "params": dict(pp), "ratios": ratios,
                        "out_of_range": bad, "seal_filled": seal_n})
        if not bad:
            break
        # 每轮只动"最差违规族"的主旋钮（相对偏差最大者优先；旋钮饱和时
        # 联动粗调 roof_family / floor_stone_fraction）
        def rel_dev(f, info):
            lo, hi = info["range"]
            width = max(hi - lo, 0.05)
            r = info["ratio"]
            return (max(lo - r, 0) + max(r - hi, 0)) / width
        worst = max(bad, key=lambda f: rel_dev(f, bad[f]))
        info = bad[worst]
        low = info["ratio"] < info["range"][0]
        knob = {"stone": "floor_stone_fraction", "wood": "wall_wood_fraction",
                "decorative": "carpet_coverage"}.get(worst)
        # stone/wood 双高（或对方不在低位、互换无空间）→ 只能稀释：提高
        # decorative / functional / glass 的占比（在各自区间上限内）
        structural_high = all(f in bad and bad[f]["ratio"] > bad[f]["range"][1]
                              for f in ("stone", "wood") if f in ranges) \
            and any(f in bad and bad[f]["ratio"] > bad[f]["range"][1]
                    for f in ("stone", "wood"))
        swap_ok = True
        if worst in ("stone", "wood") and not low:
            other = "wood" if worst == "stone" else "stone"
            if other in ranges:
                o_lo, o_hi = ranges[other]
                swap_ok = ratios.get(other, 0) < (o_lo + o_hi) / 2
            else:
                swap_ok = False

        def dilute() -> bool:
            if "decorative" in ranges:
                d_lo, d_hi = ranges["decorative"]
                if pp.get("carpet_coverage", 0) < 0.9 and \
                        ratios.get("decorative", 0) + 0.06 <= d_hi + 1e-9:
                    pp["carpet_coverage"] = pp.get("carpet_coverage", 0) + 0.08
                    return True
            elif pp.get("carpet_coverage", 0) < 0.5:
                pp["carpet_coverage"] = pp.get("carpet_coverage", 0) + 0.10
                return True
            if pp.get("plate_density", 0.02) < 0.20:
                pp["plate_density"] = pp.get("plate_density", 0.02) + 0.03
                return True
            if "glass" in ranges:
                g_lo, g_hi = ranges["glass"]
                if ratios.get("glass", 0) + 0.004 <= g_hi + 1e-9 and \
                        pp.get("window_stride", 4) > 3:
                    pp["window_stride"] -= 1
                    return True
            return False

        if knob is not None and not low and worst in ("stone", "wood") \
                and (structural_high or not swap_ok):
            if not dilute():
                break
        elif knob is not None:
            # 方向反转 → 步长减半（二分收敛，防振荡）
            d = 1 if low else -1
            if last_dir.get(knob) == -d:
                steps[knob] = max(steps[knob] / 2, 0.005)
            last_dir[knob] = d
            lo_k, hi_k = (0.0, 1.0) if knob == "floor_stone_fraction" else (0.0, 0.9)
            cur = pp.get(knob, 0.5)
            nxt = min(hi_k, max(lo_k, cur + d * steps[knob]))
            pp[knob] = nxt
            if nxt == cur:                      # 旋钮饱和 → 屋顶族粗调或稀释
                if worst in ("stone", "wood"):
                    pp["roof_family"] = ("stone" if low else "wood") \
                        if worst == "stone" else ("wood" if low else "stone")
                    if not dilute():
                        break
                else:
                    break
        elif worst == "glass":
            pp["window_stride"] = max(3, pp.get("window_stride", 4) + (2 if not low else -1))
        else:                                   # 其它族无旋钮 → 残留如实记录
            break
    # 循环结束时 b 对应的是"上一次调整前"的参数；用最终参数补一次重建，
    # 保证 fit_info 的 ratios 与返回的 b 严格一致（可复算纪律）。
    plan["palette_params"] = dict(pp)
    plan["protected_cells"] = []
    b = build_voxels(brief, plan, res)
    seal_n = seal_envelope(b, plan)
    ratios, dominant, non_air = measure_family_ratios(b, res)
    bad = {f: {"ratio": ratios.get(f, 0.0), "range": [lo, hi]}
           for f, (lo, hi) in ranges.items()
           if ratios.get(f, 0.0) < lo - 1e-9 or ratios.get(f, 0.0) > hi + 1e-9}
    history.append({"iter": "final", "params": dict(pp), "ratios": ratios,
                    "out_of_range": bad, "seal_filled": seal_n})
    fit_info = {"iterations": len(history), "converged": not bad,
                    "final_ratios": ratios,
                    "residual_out_of_range": bad,
                    "seal_filled_last": seal_n}
    # ---- 终末微调（polish）：逐格交换 stone↔wood 墙/楼板/填充格 ------------
    # 重建循环的旋钮粒度对小区间不够细；polish 是材料级微调（不动几何），
    # 仍由 ranges 驱动；不可收敛时残留偏差如实保留进 fit_info。
    if not fit_info["converged"]:
        swaps = _polish_palette(b, res, ranges)
        ratios, dominant, non_air = measure_family_ratios(b, res)
        bad = {f: {"ratio": ratios.get(f, 0.0), "range": [lo, hi]}
               for f, (lo, hi) in ranges.items()
               if ratios.get(f, 0.0) < lo - 1e-9 or ratios.get(f, 0.0) > hi + 1e-9}
        fit_info["polish_swaps"] = swaps
        fit_info["final_ratios"] = ratios
        fit_info["residual_out_of_range"] = bad
        fit_info["converged"] = not bad
    # ---- 双参数网格兜底：坐标下降可能卡在局部极小；两主旋钮对占比近似线性，
    # 6×6 网格直接搜索可行点（重建便宜；只在没有收敛时触发） ----------------
    if not fit_info["converged"]:
        import itertools
        grid = [i / 10 for i in range(0, 11, 2)]
        found = None
        for fs, wf in itertools.product(grid, grid):
            pp2 = dict(pp)
            pp2["floor_stone_fraction"] = fs
            pp2["wall_wood_fraction"] = wf
            plan["palette_params"] = dict(pp2)
            plan["protected_cells"] = []
            b2 = build_voxels(brief, plan, res)
            seal_envelope(b2, plan)
            r2, _d2, _n2 = measure_family_ratios(b2, res)
            ok = all(lo - 1e-9 <= r2.get(f, 0.0) <= hi + 1e-9
                     for f, (lo, hi) in ranges.items())
            if ok:
                found = (b2, pp2, r2)
                break
        if found:
            b, pp, ratios = found
            plan["palette_params"] = dict(pp)
            fit_info["grid_fallback"] = {"floor_stone_fraction": pp["floor_stone_fraction"],
                                         "wall_wood_fraction": pp["wall_wood_fraction"]}
            fit_info["final_ratios"] = ratios
            fit_info["residual_out_of_range"] = {}
            fit_info["converged"] = True
    return b, plan, fit_info


def _polish_palette(b: Builder, res: dict, ranges: dict, max_swaps: int = 200) -> int:
    """逐格交换材料族（stone_bricks ↔ oak_planks），每次交换都取
    "能减少总违规量"的方向；无改善即停。返回交换次数。"""
    fams = res["palette_dictionary"]["families"]
    swappable = [c for c, t in b.tags.items()
                 if t in ("wall", "gable_fill", "eave_fill", "seal_fill")
                 or t.startswith("slab_") or t == "roof"]
    n = 0
    for _ in range(max_swaps):
        ratios, _dom, non_air = measure_family_ratios(b, res)
        viol = {}
        for f, (lo, hi) in ranges.items():
            rv = ratios.get(f, 0.0)
            viol[f] = max(lo - rv, 0.0) - max(rv - hi, 0.0)   # >0 短缺 / <0 超出
        worst_over = max(((f, v) for f, v in viol.items() if v < 0),
                         key=lambda t: t[1], default=None)
        worst_under = min(((f, v) for f, v in viol.items() if v > 0),
                          key=lambda t: t[1], default=None)
        if worst_over is None:
            break
        f_over = worst_over[0]
        # 目标族：短缺的其它族优先；否则取距上限余量最大的族
        if worst_under is not None:
            f_to = worst_under[0]
        else:
            headroom = {f: hi - ratios.get(f, 0.0)
                        for f, (lo, hi) in ranges.items() if f != f_over}
            f_to = max(headroom, key=headroom.get, default=None)
        if f_to not in ("stone", "wood") or f_over not in ("stone", "wood"):
            break                               # 只支持 stone↔wood 互换
        src_ids = ["minecraft:stone_bricks", "minecraft:cobblestone"] \
            if f_over == "stone" else ["minecraft:oak_planks"]
        dst_state = MAT["wall_wood"] if f_over == "stone" else MAT["wall_stone"]
        tgt = next((c for c in swappable
                    if b.cells.get(c, "").split("[")[0] in src_ids), None)
        if tgt is None:
            break
        b.cells[tgt] = dst_state
        n += 1
    return n


# ---------------------------------------------------------------------------
# 5. IR 输出
# ---------------------------------------------------------------------------
def to_ir(b: Builder, plan: dict, brief: dict, fit_info: dict,
          generator_note: str) -> dict:
    """体素 dict → Canonical IR（schema_version=1）。包络最小角归零。"""
    min_x = min(c[0] for c in b.cells)
    min_y = min(c[1] for c in b.cells)
    min_z = min(c[2] for c in b.cells)
    shifted = {(x - min_x, y - min_y, z - min_z): s
               for (x, y, z), s in b.cells.items()}
    dim_x = max(c[0] for c in shifted) + 1
    dim_y = max(c[1] for c in shifted) + 1
    dim_z = max(c[2] for c in shifted) + 1
    palette: list[str] = []
    index: dict[str, int] = {}
    blocks = []
    for (x, y, z) in sorted(shifted):
        st = shifted[(x, y, z)]
        if st not in index:
            index[st] = len(palette)
            palette.append(st)
        blocks.append([x, y, z, index[st]])
    plan_out = json.loads(json.dumps(plan))
    plan_out["coord_offset"] = [min_x, min_y, min_z]
    return {
        "schema_version": 1,
        "metadata": {
            "generator": "programmatic reference generator (rule-driven) — NOT an LLM",
            "generator_script": "scripts/generate_blueprint.py",
            "generator_note": generator_note,
            "brief_id": brief["brief_id"],
            "style": brief["style"],
            "function_domain": brief["function_domain"],
            "generation": plan_out,
            "palette_fit": fit_info,
            "litematica": {"format_version": 6, "minecraft_data_version": 4903,
                           "regions": ["generated"],
                           "note": "离线生成，未写入任何世界"},
        },
        "origin": [0, 0, 0],
        "dimensions": {"x": dim_x, "y": dim_y, "z": dim_z},
        "rotation": None,
        "mirror": None,
        "palette": palette,
        "blocks": blocks,
    }


def generate(brief: dict, res: dict, overrides: dict | None = None,
             note: str = "initial single-pass (route B faithful)") -> tuple[dict, dict]:
    """主入口：brief + 资源 → (IR dict, plan)。C 路线 Revision 通过 overrides 复用。"""
    b, plan, fit_info = fit_palette(brief, res, overrides)
    ir = to_ir(b, plan, brief, fit_info, note)
    return ir, plan


def write_ir(ir: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ir, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="参数化参考生成器（rule-driven，非 LLM）")
    ap.add_argument("--briefs", required=True, help="design_briefs.jsonl")
    ap.add_argument("--brief-id", required=True)
    ap.add_argument("--out-root", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--out", required=True, help="输出 IR 路径")
    args = ap.parse_args()
    out_root = Path(args.out_root)
    res = load_resources(out_root)
    brief = None
    for line in Path(args.briefs).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rec = json.loads(line)
            if rec["brief_id"] == args.brief_id:
                brief = rec
                break
    if brief is None:
        raise SystemExit(f"brief 不存在: {args.brief_id}")
    ir, plan = generate(brief, res)
    write_ir(ir, Path(args.out))
    print(json.dumps({"brief_id": brief["brief_id"],
                      "dimensions": ir["dimensions"],
                      "blocks": len(ir["blocks"]),
                      "palette_size": len(ir["palette"]),
                      "palette_fit": ir["metadata"]["palette_fit"]},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
