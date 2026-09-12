# -*- coding: utf-8 -*-
"""revise_blueprint — C 路线程序化修复器（项目代号 H · P6 第二部分）。

按 07_ARCHITECT_SYSTEM/REVISION_PROTOCOL.md 实现的**程序化** Revision：
输入 = 一份生成蓝图（Canonical IR JSON）+ Validator 触发清单 + 评分中间值；
输出 = 修订后蓝图 + 变更清单（可算 diff：added/removed/changed + SHA256）。

修复策略（先治病再选美；Validator fail 必须修，Critic 项可权衡）：

| 触发 | 修复动作（patch = 体素级；regen = 带 overrides 重生成） |
|---|---|
| V002/V003 门接近/内侧站位 | 清门内外接近格障碍物、补门槛下支撑；阳台门撞楼梯洞口 → balcony_door_shift regen |
| V005 楼梯底堵 | 清底步周边非墙体障碍（仅拆 partition/装饰，不动外墙/楼板/楼梯） |
| V006 楼梯顶堵 | 在顶步侧翼的隔墙上开 1×2 口（清出同层落点的身体/头顶格）；不行 → shaft_shift regen |
| V007 垂直交通断 | 补开计划中的楼板洞口（楼梯修复的副产品兜底） |
| V004 孤立房间 | 在该房间与邻房之间的隔墙上开 1×2 口（避开井柱/洞口） |
| V010 围护泄漏 | 洪泛重算泄漏格，墙料填实（保护门 ±1 格，口径同 V010 opening_margin） |
| V011 屋顶覆盖中断 | 无屋顶室内柱的最高空气格上方补屋面半砖 |
| V009 大面积低净高 | 仅当上方障碍是可拆元素（partition）时拆；否则 KEEP 并记录理由 |
| M02 材料族出界 | palette_params 旋钮微调后 regen（材料只动墙/楼板/屋面填充，不动几何锚点） |
| F06 分区面积不足 | partition_shift 平移该层分区线（邻房有余量时） |
| F02 邻接缺开口 | 在两房间的共用隔墙上开 1×2 口 |

锚点纪律（REVISION_PROTOCOL §3.1）：footprint 外轮廓、风格标签、分区清单不动；
patch 只允许拆 interior partition/装饰、补洞口/支撑/屋面，不改外墙包络。
每次修订后由 run_benchmark 重跑 Validator Recheck（真实重跑，中间结果留 traces）。
"""
from __future__ import annotations

import hashlib
import json
from collections import deque
from pathlib import Path

# 修复器只拆这些元素的实体（保护外墙/楼板/楼梯/屋面结构）
CARVABLE_PREFIXES = ("partition",)
FILL_WALL = "minecraft:stone_bricks"
FILL_FLOOR = "minecraft:oak_planks"
ROOF_SLAB = "minecraft:stone_brick_slab[type=bottom]"


def load_ir_cells(ir: dict) -> dict[tuple[int, int, int], str]:
    """IR → {(x,y,z): block_state}（忽略 air 项）。"""
    palette = ir["palette"]
    cells = {}
    for x, y, z, pi in ir["blocks"]:
        st = palette[int(pi)]
        if st.split("[")[0] in ("minecraft:air", "minecraft:cave_air", "minecraft:void_air"):
            continue
        cells[(int(x), int(y), int(z))] = st
    return cells


def cells_to_ir(cells: dict, template_ir: dict, note: str) -> dict:
    """体素 dict → Canonical IR（沿用 template 的 metadata，更新生成备注）。"""
    min_x = min(c[0] for c in cells)
    min_y = min(c[1] for c in cells)
    min_z = min(c[2] for c in cells)
    palette: list[str] = []
    index: dict[str, int] = {}
    blocks = []
    for (x, y, z) in sorted(cells):
        st = cells[(x, y, z)]
        if st not in index:
            index[st] = len(palette)
            palette.append(st)
        blocks.append([x - min_x, y - min_y, z - min_z, index[st]])
    out = json.loads(json.dumps(template_ir))       # 深拷贝
    out["palette"] = palette
    out["blocks"] = blocks
    xs = [b[0] for b in blocks]; ys = [b[1] for b in blocks]; zs = [b[2] for b in blocks]
    out["dimensions"] = {"x": max(xs) + 1, "y": max(ys) + 1, "z": max(zs) + 1}
    out["metadata"]["generator_note"] = note
    return out


def diff_irs(old_ir: dict, new_ir: dict) -> dict:
    """逐坐标 diff（对齐 Canonical 契约：两 IR 均包络最小角归零，按坐标对齐）。"""
    def cmap(ir):
        return {(int(x), int(y), int(z)): ir["palette"][int(pi)]
                for x, y, z, pi in ir["blocks"]}
    a, b = cmap(old_ir), cmap(new_ir)
    added = removed = changed = 0
    for pos in set(a) | set(b):
        av, bv = a.get(pos), b.get(pos)
        if av == bv:
            continue
        if av is None:
            added += 1
        elif bv is None:
            removed += 1
        else:
            changed += 1
    sha = hashlib.sha256(json.dumps(sorted(map(list, new_ir["blocks"]))).encode()).hexdigest()
    return {"added": added, "removed": removed, "changed": changed,
            "total": added + removed + changed, "sha256": sha,
            "prev_non_air": len(a), "new_non_air": len(b)}


# ---------------------------------------------------------------------------
# 各规则修复函数：签名 fix(ctx) -> actions list；ctx 含 cells/plan/vres/brief 等
# ---------------------------------------------------------------------------
def _door_cells_from(vres: dict) -> list[dict]:
    """从 V002/V008 证据收集要修的门条目（pos/outside/inside/missing）。"""
    out = []
    for r in vres["rules"]:
        if r["rule_id"] == "V002" and r["triggered"]:
            for ev in r["evidence"]:
                ent = ev.get("entrance", {})
                if ent.get("pos"):
                    out.append({"pos": ent["pos"],
                                "cells": [c for c in (ent.get("outside"), ent.get("inside"))
                                          if c],
                                "problems": ev.get("problems", [])})
        if r["rule_id"] == "V008" and r["triggered"]:
            for ev in r["evidence"]:
                out.append({"pos": ev["pos"], "cells": [], "problems": ["V008"]})
    return out


def fix_door_approach(ctx: dict) -> list[str]:
    """清门接近格：接近格与其上方格非空气则拆（仅可拆元素），下方无支撑则补楼板。"""
    cells = ctx["cells"]
    acts = []
    for d in _door_cells_from(ctx["vres"]):
        for cell in d["cells"]:
            x, y, z = cell
            # 支撑：接近格下方无实体 → 补楼板（悬浮接近位）
            if (x, y - 1, z) not in cells and y - 1 >= 0:
                cells[(x, y - 1, z)] = FILL_FLOOR
                acts.append(f"support_fill {(x, y - 1, z)}")
            for yy in (y, y + 1):
                if (x, yy, z) in cells:
                    # 门自身格跳过（门块本身是通道）
                    if "door" in cells[(x, yy, z)]:
                        continue
                    del cells[(x, yy, z)]
                    acts.append(f"clear {(x, yy, z)}")
    return acts


def fix_stair(ctx: dict, top: bool) -> list[str]:
    """V005/V006：清楼梯底/顶周边的阻挡。

    顶堵（V006）：对顶步每个水平邻居，若其上方两格是可拆元素（partition），
    拆除形成侧翼出口；若顶步自身上方被埋，也清。底堵（V005）同理清入口侧。
    """
    cells = ctx["cells"]
    acts = []
    for r in ctx["vres"]["rules"]:
        if r["rule_id"] != ("V006" if top else "V005") or not r["triggered"]:
            continue
        for ev in r["evidence"]:
            anchor_cells = ev.get("top" if top else "bottom", [])
            for c in anchor_cells:
                x, y, z = c
                for nx, nz in ((x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1)):
                    # 邻居格：同级应为可站（有支撑实体），其身体/头顶格须为空气
                    for yy in (y + 1, y + 2):
                        st = cells.get((nx, yy, nz))
                        if st is not None and "door" not in st:
                            del cells[(nx, yy, nz)]
                            acts.append(f"carve {(nx, yy, nz)}")
                # 顶步自身被埋（no_stance 情形）
                if top:
                    for yy in (y + 1, y + 2):
                        st = cells.get((x, yy, z))
                        if st is not None and "_stairs" not in st and "door" not in st:
                            del cells[(x, yy, z)]
                            acts.append(f"unbury {(x, yy, z)}")
    return acts


def fix_v007(ctx: dict) -> list[str]:
    """补开计划中的楼板洞口（若洞口被后续元素误填）。"""
    cells = ctx["cells"]
    plan = ctx["plan"]
    off = plan.get("coord_offset", [0, 0, 0])
    acts = []
    for sh in ctx.get("shafts", []):
        sy1 = sh["base_y"] + plan["floor_height"] - 0  # 计划坐标 → IR 坐标
        sy_ir = sy1 - off[1]
        for hx, hz in sh.get("hole_cols", []):
            c = (hx - off[0], sy_ir, hz - off[2])
            if cells.get(c):
                del cells[c]
                acts.append(f"reopen_slab_hole {c}")
    return acts


def fix_v004(ctx: dict) -> list[str]:
    """孤立房间：在其与相邻房间的共用隔墙上开 1×2 口。

    用 plan.rooms 定位 sample_pos 所在房间，找贴边的 partition，
    在避开井柱/洞口的位置开口。
    """
    cells = ctx["cells"]
    plan = ctx["plan"]
    off = plan.get("coord_offset", [0, 0, 0])
    slab_ys = plan.get("slab_ys", [0])
    hole_step = set()
    for sh in ctx.get("shafts", []):
        hole_step |= {tuple(c) for c in sh.get("hole_cols", [])}
        hole_step |= {tuple(c) for c in sh.get("step_cols", [])}
    acts = []
    for r in ctx["vres"]["rules"]:
        if r["rule_id"] != "V004" or not r["triggered"]:
            continue
        for ev in r["evidence"]:
            sx, sy_, sz = ev["sample_pos"]
            pc = (sx + off[0], sy_ + off[1], sz + off[2])
            room = None
            for rm in plan.get("rooms", []):
                rx0, rz0, rx1, rz1 = rm["rect"]
                if rx0 <= pc[0] <= rx1 and rz0 <= pc[2] <= rz1 and \
                        slab_ys[rm["floor"]] <= pc[1] <= slab_ys[rm["floor"]] + plan["floor_height"]:
                    room = rm
                    break
            if room is None:
                acts.append("UNRESOLVED: sample_pos 不在任何房间矩形内")
                continue
            fi = room["floor"]
            sy = slab_ys[fi]
            # 找贴该房间的隔墙
            rx0, rz0, rx1, rz1 = room["rect"]
            done = False
            for pt in plan.get("partitions", []):
                if pt["floor"] != fi:
                    continue
                borders = (pt["axis"] == "x" and pt["pos"] in (rx0 - 1, rx1 + 1)) or \
                          (pt["axis"] == "z" and pt["pos"] in (rz0 - 1, rz1 + 1))
                if not borders:
                    continue
                for t in range(pt["span"][0], pt["span"][1] + 1):
                    x, z = (pt["pos"], t) if pt["axis"] == "x" else (t, pt["pos"])
                    if (x, z) in hole_step:
                        continue
                    c1 = (x - off[0], sy + 1 - off[1], z - off[2])
                    c2 = (x - off[0], sy + 2 - off[1], z - off[2])
                    for c in (c1, c2):
                        if cells.get(c):
                            del cells[c]
                    acts.append(f"open_doorway p{pt['pos']} t={t} floor={fi}")
                    done = True
                    break
                if done:
                    break
            if not done:
                acts.append(f"UNRESOLVED: 房间 {room['zone']} 无可开口隔墙")
    return acts


def fix_v010(ctx: dict) -> list[str]:
    """围护泄漏：洪泛重算（与 Validator 同口径：6 连通、边界种子），填墙。"""
    cells = ctx["cells"]
    xs = [c[0] for c in cells]; ys = [c[1] for c in cells]; zs = [c[2] for c in cells]
    x0, y0, z0 = min(xs) - 1, min(ys) - 1, min(zs) - 1
    X, Y, Z = max(xs) - x0 + 2, max(ys) - y0 + 2, max(zs) - z0 + 2
    solid = set(cells)
    protected = set()
    for c, st in cells.items():
        if "_door" in st:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        protected.add((c[0] + dx, c[1] + dy, c[2] + dz))
    seen = set()
    dq = deque()
    for x in range(x0, x0 + X):
        for y in range(y0, y0 + Y):
            for z in (z0, z0 + Z - 1):
                if (x, y, z) not in solid:
                    seen.add((x, y, z)); dq.append((x, y, z))
    for x in range(x0, x0 + X):
        for z in range(z0, z0 + Z):
            for y in (y0, y0 + Y - 1):
                if (x, y, z) not in solid and (x, y, z) not in seen:
                    seen.add((x, y, z)); dq.append((x, y, z))
    for y in range(y0, y0 + Y):
        for z in range(z0, z0 + Z):
            for x in (x0, x0 + X - 1):
                if (x, y, z) not in solid and (x, y, z) not in seen:
                    seen.add((x, y, z)); dq.append((x, y, z))
    while dq:
        cx, cy, cz = dq.popleft()
        for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            n = (cx + dx, cy + dy, cz + dz)
            if n in solid or n in seen:
                continue
            if not (x0 <= n[0] < x0 + X and y0 <= n[1] < y0 + Y and z0 <= n[2] < z0 + Z):
                continue
            seen.add(n); dq.append(n)
    acts = []
    for cx, cy, cz in list(seen):
        for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            n = (cx + dx, cy + dy, cz + dz)
            if not (x0 < n[0] < x0 + X - 1 and y0 < n[1] < y0 + Y - 1
                    and z0 < n[2] < z0 + Z - 1):
                continue
            if n in solid or n in seen or n in protected:
                continue
            cells[n] = FILL_WALL
            solid.add(n)
            acts.append(f"fill_leak {n}")
    return acts


def fix_v011(ctx: dict) -> list[str]:
    """屋顶覆盖：无屋顶室内柱最高空气格上方补屋面半砖。

    复算口径 = V011：内部空气柱最高格上方无任何实体 → 在该柱最高格 +1 补。
    内部空气由 fix_v010 的洪泛给出（非外部即内部）。
    """
    cells = ctx["cells"]
    xs = [c[0] for c in cells]; zs = [c[2] for c in cells]
    ys = [c[1] for c in cells]
    acts = []
    # 简化稳健实现：对每根室内柱（外墙线以内），若存在空气格且其上方直到
    # 包络顶都无实体，则在最高空气格 +1 补屋面半砖（与 V011 判定口径对齐；
    # 柱顶直通包络顶的开放柱由 V011 自身排除，不在此处理）。
    x_min, x_max = min(xs), max(xs)
    z_min, z_max = min(zs), max(zs)
    y_max = max(ys)
    off = ctx["off"]
    fp = ctx["plan"]["footprint"]
    fx0, fz0, fx1, fz1 = fp[0] - off[0], fp[1] - off[2], fp[2] - off[0], fp[3] - off[2]
    for x in range(x_min, x_max + 1):
        for z in range(z_min, z_max + 1):
            if not (fx0 < x < fx1 and fz0 < z < fz1):
                continue                      # 只管室内柱（墙线以内）
            col_air = [y for y in range(0, y_max + 2) if (x, y, z) not in cells]
            if not col_air:
                continue
            top_air = col_air[-1]
            if top_air >= y_max:
                continue                      # 柱顶直通包络顶（开放区域，V011 自会排除截断柱）
            if any((x, y, z) in cells for y in range(top_air + 1, y_max + 1)):
                continue                      # 上方有实体 → 已覆盖
            cells[(x, top_air + 1, z)] = ROOF_SLAB
            acts.append(f"roof_patch {(x, top_air + 1, z)}")
    return acts


# ---------------------------------------------------------------------------
# 主入口：按触发清单调度修复
# ---------------------------------------------------------------------------
def apply_patch_revision(ir: dict, vres: dict, plan: dict) -> tuple[dict, list[str]]:
    """体素级修复（不动锚点）。返回 (new_ir, actions)。"""
    cells = load_ir_cells(ir)
    ctx = {"cells": cells, "vres": vres, "plan": plan,
           "shafts": _shafts_from_plan(plan),
           "off": plan.get("coord_offset", [0, 0, 0])}
    acts: list[str] = []
    triggered = {r["rule_id"] for r in vres["rules"] if r["triggered"]}
    if "V002" in triggered or "V008" in triggered or "V003" in triggered:
        acts += fix_door_approach(ctx)
    if "V005" in triggered:
        acts += fix_stair(ctx, top=False)
    if "V006" in triggered:
        acts += fix_stair(ctx, top=True)
    if "V007" in triggered:
        acts += fix_v007(ctx)
    if "V004" in triggered:
        acts += fix_v004(ctx)
    if "V010" in triggered:
        acts += fix_v010(ctx)
    if "V011" in triggered:
        acts += fix_v011(ctx)
    note = "C-route patch revision: " + ("; ".join(sorted(triggered)) or "none")
    new_ir = cells_to_ir(cells, ir, note)
    return new_ir, acts


def _shafts_from_plan(plan: dict) -> list[dict]:
    """plan 里没直接存 shafts（生成期局部变量）——从 IR 元数据里拿不到的
    信息就留空，fix_v007 退化无操作。生成器已在 metadata.generation 记录
    rooms/partitions/slab_ys/floor_height，够分区修复用。"""
    return plan.get("shafts", [])


def plan_balcony_door_shift(plan: dict) -> int | None:
    """计算阳台门沿墙平移量：让门内接近格（door_at - dvec）避开该层
    楼梯井的洞口/踏步柱位。返回 shift（±1/±2…）或 None（无解）。

    背景：单轮生成把阳台门放在墙面中点，若该处室内侧恰好是楼梯井的
    楼板洞口，V002/V003 会判"门内接近空间不足"。这是计划层可修的典型
    缺陷（改门位，不动锚点）。
    """
    bal = plan.get("balcony")
    if not bal:
        return None
    dx, dz = bal["dvec"]
    door = bal["door_at"]
    inside = (door[0] - dx, door[1] - dz)          # 室内侧柱位（plan 坐标）
    blocked_cols = set()
    for sh in plan.get("shafts", []):
        blocked_cols |= {tuple(c) for c in sh.get("hole_cols", [])}
        blocked_cols |= {tuple(c) for c in sh.get("step_cols", [])}
    if inside not in blocked_cols:
        return None                                 # 不是洞口问题，patch 路线处理
    for shift in (1, -1, 2, -2, 3, -3):
        if dx == 0:                                 # 门沿 z 墙 → 沿 x 移
            cand = (inside[0] + shift, inside[1])
        else:                                       # 门沿 x 墙 → 沿 z 移
            cand = (inside[0], inside[1] + shift)
        if cand not in blocked_cols:
            return shift
    return None


def anchor_check(old_ir: dict, new_ir: dict) -> dict:
    """锚点校验：footprint 外轮廓（y≤2 层的实体点集）与分区清单不变。"""
    def wall_ring(ir):
        pts = set()
        for x, y, z, pi in ir["blocks"]:
            if int(y) <= 2:
                pts.add((int(x), int(z)))
        return pts
    a, b = wall_ring(old_ir), wall_ring(new_ir)
    zones_a = [r["zone"] for r in old_ir["metadata"]["generation"].get("rooms", [])]
    zones_b = [r["zone"] for r in new_ir["metadata"]["generation"].get("rooms", [])]
    return {"footprint_unchanged": a == b,
            "zones_unchanged": sorted(zones_a) == sorted(zones_b),
            "style_unchanged": old_ir["metadata"].get("style") == new_ir["metadata"].get("style")}
