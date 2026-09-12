# -*- coding: utf-8 -*-
"""spatial_context — Spatial Validator 的共享空间上下文（项目代号 H · P2）。

把 12 条规则都要用的几何/连通性计算集中做一次：

- 体素化（复用 P1 blueprint_io / walkability，不改写）；
- exterior / interior air 洪泛（6 连通，包络边界种子）；
- walkability 图（return_labels + return_graph）：站位、分量、高程、邻接；
- 站位的 interior 归属：**站位支撑体素 u 的身体格 u+1 落在 interior air 中**
  （这是 P1 的关键教训：屋顶/树梢等露天表面会天然形成大量连通分量，
  只有“身体在内部空气里”的站位才算室内站位，否则全库误报）；
- 门 / 外门候选 / 门洞（无门开口）候选；
- 楼梯聚类（26 连通）、每个 cluster 的底/顶体素；
- 楼层启发式（与 P1 extract_blueprint_metadata 相同的密度法，参数外置）；
- 低净高候选格（有支撑但 clearance 失败且身体格是内部空气）。

所有判定需要的阈值都从 validator_rules.json 传入，本模块只存事实与派生掩码。
"""
from __future__ import annotations

import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy import ndimage

# 复用 P1 共享模块（scripts/ 与 05_SPATIAL_VALIDATOR/validator_source/ 同级工程内）
_SCRIPTS = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from blueprint_io import load_blueprint, to_voxels  # noqa: E402
import walkability  # noqa: E402
from walkability import _palette_params, classify_block  # noqa: E402

AIR_IDS = ("minecraft:air", "minecraft:cave_air", "minecraft:void_air")


class SpatialContext:
    """一张蓝图的全部共享空间事实。"""

    def __init__(self, path, floor_params: dict | None = None):
        ir = load_blueprint(path)
        voxels, air_index = to_voxels(ir)
        self.ir = ir
        self.path = Path(path)
        self.voxels = voxels
        self.air_index = air_index
        self.X, self.Y, self.Z = voxels.shape

        # ---- 实体 / 空气 ------------------------------------------------
        air_idx = {i for i, bid in enumerate(ir.block_ids) if bid in AIR_IDS}
        self.solid = ~np.isin(voxels, list(air_idx))
        self.non_air = int(self.solid.sum())
        air_mask = ~self.solid

        # ---- exterior / interior air（6 连通洪泛，边界种子） -------------
        air_labels, _ = ndimage.label(air_mask)  # 默认 structure = 6 连通
        boundary_labels = set(np.unique(np.concatenate([
            air_labels[0, :, :].ravel(), air_labels[-1, :, :].ravel(),
            air_labels[:, 0, :].ravel(), air_labels[:, -1, :].ravel(),
            air_labels[:, :, 0].ravel(), air_labels[:, :, -1].ravel(),
        ]))) - {0}
        self.exterior_air = np.isin(air_labels, list(boundary_labels)) if boundary_labels \
            else np.zeros_like(air_mask)
        self.interior_air = air_mask & ~self.exterior_air
        self.interior_air_count = int(self.interior_air.sum())

        # ---- walkability（带标签与图） -----------------------------------
        self.walk = walkability.analyze(voxels, ir, return_labels=True, return_graph=True)
        self.labels = self.walk["labels"]            # (x,y,z) int, -1=非站位
        self.E = self.walk["stance_elevation"]       # (x,y,z) float, nan=非站位
        self.stance_mask = self.walk["stance_mask"]
        self.walkable_voxels = self.walk["walkable_voxels"]

        # palette 级参数（surface / solid 区间），供低净高与评分判定
        surface, has_surface, solid_lo, solid_hi, _flags, _classes = _palette_params(ir)
        self.v_has_surface = has_surface[voxels]
        self.v_solid_lo = solid_lo[voxels]
        # 潜在站位 = 提供支撑且正上方一格无实体（真正能站上去的位置）；
        # 包络顶界外视为空气
        no_solid_above = np.ones_like(self.v_has_surface)
        no_solid_above[:, :-1, :] = self.v_solid_lo[:, 1:, :] >= 1.0
        self.potential_stance_voxels = int((self.v_has_surface & no_solid_above).sum())

        # ---- 站位的 interior 归属：身体格 u+1 是内部空气 -----------------
        body_interior = np.zeros_like(self.interior_air)
        body_interior[:, :-1, :] = self.interior_air[:, 1:, :]
        self.stance_interior = self.stance_mask & body_interior
        self.interior_stance_count = int(self.stance_interior.sum())

        # ---- 站位图邻接（扁平索引） --------------------------------------
        self.flatE = self.E.ravel()
        self.adj: dict[int, list[int]] = defaultdict(list)
        src, dst = self.walk["graph_src"], self.walk["graph_dst"]
        for a, b in zip(src.tolist(), dst.tolist()):
            self.adj[a].append(b)
        # 度数（死端判定）；每条边双向都写，度数 = 邻接数
        self.degree = {n: len(set(ns)) for n, ns in self.adj.items()}

        # interior 站位按分量聚合
        self.interior_comp_counts: Counter = Counter()
        for fi in np.flatnonzero(self.stance_interior):
            self.interior_comp_counts[int(self.labels.ravel()[fi])] += 1

        # ---- 方块类掩码 ---------------------------------------------------
        classes = np.array([classify_block(b, p) for b, p in
                            zip(ir.block_ids, ir.properties)], dtype=object)
        self.cls_vox = classes[voxels]  # (x,y,z) 类名

        # ---- 门 -----------------------------------------------------------
        self.doors: list[dict] = []     # 每个：pos(lower), upper, props
        door_positions = np.argwhere(self.cls_vox == "DOOR")
        seen_lower: set[tuple[int, int, int]] = set()
        for x, y, z in door_positions:
            props = ir.properties[int(voxels[x, y, z])]
            if props.get("half", "lower") != "lower":
                continue
            seen_lower.add((int(x), int(y), int(z)))
            self.doors.append({"pos": (int(x), int(y), int(z)), "props": props})
        self.door_mask = self.cls_vox == "DOOR"

        # 外门候选：通行轴由 door 的 facing 属性决定（facing=north/south → z 轴，
        # east/west → x 轴）。轴上一侧为外部空气、另一侧为任意空气 → 严格候选；
        # 仅一侧外部空气 → 宽松候选。内侧空气不要求 flood 判定为 interior——
        # 带无玻璃窗/拱洞的建筑内部空气会被洪泛吸收成 exterior（P2 实测 REF-0003）。
        _FACING_VEC = {"east": (1, 0), "west": (-1, 0),
                       "south": (0, 1), "north": (0, -1)}
        _FACING_OUT_NAME = {(1, 0): "east", (-1, 0): "west",
                            (0, 1): "south", (0, -1): "north"}
        self.exterior_doors_strict: list[dict] = []
        self.exterior_doors_loose: list[dict] = []
        for d in self.doors:
            x, y, z = d["pos"]
            dx, dz = _FACING_VEC.get(d["props"].get("facing", "north"), (0, -1))
            if d["props"].get("open", "false") == "true":
                # 敞开的门扇面板旋转 90° 贴墙，通行轴与 facing 垂直
                dx, dz = dz, dx
            sides = []
            for sx, sz in ((dx, dz), (-dx, -dz)):
                nx, nz = x + sx, z + sz
                if 0 <= nx < self.X and 0 <= nz < self.Z and not self.solid[nx, y, nz]:
                    sides.append({"cell": (nx, y, nz),
                                  "exterior": bool(self.exterior_air[nx, y, nz]),
                                  "dir": _FACING_OUT_NAME[(sx, sz)]})
            ext_sides = [s for s in sides if s["exterior"]]
            if len(sides) == 2 and ext_sides:
                outside = ext_sides[0]
                inside = next(s for s in sides if s is not outside)
                self.exterior_doors_strict.append(
                    {"pos": d["pos"], "outside": outside["cell"],
                     "inside": inside["cell"], "facing_out": outside["dir"]})
            elif ext_sides:
                self.exterior_doors_loose.append(
                    {"pos": d["pos"], "outside": ext_sides[0]["cell"],
                     "inside": None, "facing_out": ext_sides[0]["dir"]})

        # ---- 门洞开口候选（无门的 interior↔exterior 水平开口） ------------
        # 内部空气格 c（某站位的身体格）与外部空气格 n 同层 4 邻接，
        # 且两侧下方都有合法站位 → 玩家可穿越的开口。
        self.openings: list[dict] = []
        ia = self.interior_air
        for axis in (0, 2):
            sl_a = [slice(None)] * 3
            sl_b = [slice(None)] * 3
            sl_a[axis] = slice(0, -1)
            sl_b[axis] = slice(1, None)
            pair = ia[tuple(sl_a)] & self.exterior_air[tuple(sl_b)]
            pair2 = self.exterior_air[tuple(sl_a)] & ia[tuple(sl_b)]
            for m, flip in ((pair, False), (pair2, True)):
                for ca, cb in self._pair_cells(m, axis, flip):
                    if self._stance_below(ca) and self._stance_below(cb):
                        inside = ca if self.interior_air[ca] else cb
                        outside = cb if self.interior_air[ca] else ca
                        self.openings.append({"pos": inside, "outside": outside})

        # ---- 楼梯聚类（26 连通） ------------------------------------------
        stair_mask = self.cls_vox == "STAIR"
        self.stair_clusters: list[dict] = []
        if stair_mask.any():
            lab, n = ndimage.label(stair_mask, structure=np.ones((3, 3, 3), dtype=int))
            for cid in range(1, n + 1):
                cells = np.argwhere(lab == cid)
                ys = cells[:, 1]
                ymin, ymax = int(ys.min()), int(ys.max())
                bottom = [tuple(int(v) for v in c) for c in cells[ys == ymin]]
                top = [tuple(int(v) for v in c) for c in cells[ys == ymax]]
                self.stair_clusters.append({
                    "id": cid, "size": int(len(cells)),
                    "y_min": ymin, "y_max": ymax, "y_span": ymax - ymin,
                    "bottom": bottom, "top": top,
                    "cells": [tuple(int(v) for v in c) for c in cells],
                })

        # ---- 梯子柱 -------------------------------------------------------
        ladder_mask = self.cls_vox == "LADDER"
        ladder_cells = np.argwhere(ladder_mask)
        cols: dict[tuple[int, int], list[int]] = {}
        for x, y, z in ladder_cells:
            cols.setdefault((int(x), int(z)), []).append(int(y))
        self.ladder_columns = len(cols)

        # 垂直舱口入口：梯柱的某些格 6 邻接内部空气、另一些格 6 邻接外部空气
        # （活板门 + 梯子的舱口入口，水平开口检测覆盖不到，P2 实测 REF-0005）
        self.hatches: list[dict] = []
        for (lx, lz), ys in cols.items():
            touch_int = touch_ext = False
            for ly in ys:
                for nx, ny, nz in ((lx - 1, ly, lz), (lx + 1, ly, lz),
                                   (lx, ly, lz - 1), (lx, ly, lz + 1),
                                   (lx, ly - 1, lz), (lx, ly + 1, lz)):
                    if 0 <= nx < self.X and 0 <= ny < self.Y and 0 <= nz < self.Z:
                        if self.interior_air[nx, ny, nz]:
                            touch_int = True
                        elif self.exterior_air[nx, ny, nz]:
                            touch_ext = True
            if touch_int and touch_ext:
                self.hatches.append({"pos": (lx, int(np.mean(ys)), lz),
                                     "y_range": (min(ys), max(ys))})

        # ---- 楼层启发式（与 P1 同法，参数外置） ---------------------------
        fp = floor_params or {}
        self.floor_elevations = self._detect_floors(
            density_threshold=fp.get("density_threshold", 0.30),
            min_gap=fp.get("min_gap", 2),
        )

        # ---- 低净高候选格：有支撑但站位非法，且身体格是内部空气 ------------
        low = self.v_has_surface & ~self.stance_mask & body_interior
        self.low_headroom_cells = [tuple(int(v) for v in c) for c in np.argwhere(low)]

    # ------------------------------------------------------------------
    def _pair_cells(self, mask, axis, flip):
        """把 (a|b 切片对) 布尔掩码还原成全局坐标对。"""
        coords = np.argwhere(mask)
        out = []
        for c in coords:
            a = [int(c[0]), int(c[1]), int(c[2])]
            b = a.copy()
            b[axis] += 1
            if flip:
                out.append((tuple(b), tuple(a)))  # (exterior, interior) 顺序无所谓
            else:
                out.append((tuple(a), tuple(b)))
        return out

    def _stance_below(self, cell) -> bool:
        """cell 是空气格；其下方一格若提供合法站位则返回 True。"""
        x, y, z = cell
        return y - 1 >= 0 and bool(self.stance_mask[x, y - 1, z])

    def _detect_floors(self, density_threshold: float, min_gap: int) -> list[int]:
        """楼层行走面高程（HEURISTIC，与 P1 extract 同法）。

        某 y 层实体占比 ≥ 阈值 → 楼板候选层；连续候选层分组，取组顶 +1；
        合并间隔 < min_gap 的层。
        """
        X, Y, Z = self.X, self.Y, self.Z
        if X * Z == 0 or Y == 0:
            return []
        layer_density = self.solid.sum(axis=(0, 2)) / (X * Z)
        cand = np.flatnonzero(layer_density >= density_threshold)
        groups: list[list[int]] = []
        for yv in cand.tolist():
            if groups and yv - groups[-1][-1] <= 1:
                groups[-1].append(yv)
            else:
                groups.append([yv])
        elevations: list[int] = []
        for g in groups:
            e = g[-1] + 1
            if elevations and e - elevations[-1] < min_gap:
                continue
            elevations.append(e)
        return elevations

    # ------------------------------------------------------------------
    # 供规则使用的查询接口
    # ------------------------------------------------------------------
    def label_at(self, cell) -> int:
        return int(self.labels[cell])

    def stance_elevation_at(self, cell) -> float:
        return float(self.E[cell])

    def neighbors(self, cell) -> list[int]:
        """站位体素 cell 的图邻居（扁平索引）。"""
        if self.labels[cell] < 0:
            return []
        return self.adj.get(int(np.ravel_multi_index(cell, self.labels.shape)), [])

    def flat_of(self, cell) -> int:
        return int(np.ravel_multi_index(cell, self.labels.shape))

    def cell_of_flat(self, fi: int) -> tuple[int, int, int]:
        return tuple(int(v) for v in np.unravel_index(fi, self.labels.shape))

    def floor_stance_sets(self, level_tol: float = 0.6):
        """每个楼层高程 → 该层站位（扁平索引）集合（全部 / 仅内部）。"""
        out = []
        if not self.floor_elevations:
            return out
        stance_flat = np.flatnonzero(self.stance_mask)
        stance_E = self.flatE[stance_flat]
        stance_int = self.stance_interior.ravel()[stance_flat]
        for e in self.floor_elevations:
            on = np.abs(stance_E - e) <= level_tol
            out.append({
                "elevation": e,
                "all": set(stance_flat[on].tolist()),
                "interior": set(stance_flat[on & stance_int].tolist()),
            })
        return out

    def component_of_flat(self, fi: int) -> int:
        return int(self.labels.ravel()[fi])

    def ring_classes(self, stance_flat_set) -> Counter:
        """一组站位（扁平索引）身体格 1 圈邻域内的方块类计数。

        用于判断孤立内部空间与外界的隔离方式：环上出现 DOOR/TRAPDOOR/LADDER/
        FENCE_GATE 等可交互构件时，该空间可能经模型未完全覆盖的通道相连
        （舱口、机关门），应降级为 WARNING；环上全是实体才是真正封死。
        """
        mask = np.zeros(self.labels.size, dtype=bool)
        idx = np.fromiter(stance_flat_set, dtype=np.int64, count=len(stance_flat_set))
        if idx.size == 0:
            return Counter()
        mask[idx] = True
        mask3 = mask.reshape(self.labels.shape)
        body = np.zeros_like(mask3)
        body[:, 1:, :] = mask3[:, :-1, :]     # 身体格
        ring = ndimage.binary_dilation(body) & ~body
        return Counter(self.cls_vox[ring].tolist())


MECHANISM_CLASSES = ("DOOR", "TRAPDOOR", "LADDER", "FENCE_GATE")
