# -*- coding: utf-8 -*-
"""generate_fixtures — 程序化生成 Spatial Validator 回归测试夹具（项目代号 H · P2）。

生成 8 组合成 Canonical IR（schema_version=1）+ 1 组辅助负例，写入 tests/fixtures/：

    correct_entrance        正例：单层小屋，门/入口/围护/屋顶正常
    blocked_entrance        负例 → V002：门内侧紧贴实体柱，入口后无通行空间
    correct_stair           正例：两层楼 + 正常楼梯（含楼梯井开口）
    stair_top_blocked       负例 → V006：复现“楼梯尽头是墙”（顶端三面砌死）
    stair_bottom_blocked    负例 → V005：楼梯底部四周与下方入口全部封死
    isolated_room           负例 → V004：室内一堵无门隔墙隔出封闭房间
    broken_vertical_access  负例 → V007：两层楼，无楼梯/梯子
    correct_multifloor      正例：两层楼 + 正常楼梯（不同方位）
    no_exterior_entrance    辅助负例 → V001：全封闭无门小屋（V001 负例断言用）

夹具是合法 Canonical IR：{"schema_version":1, "palette":[...], "blocks":[[x,y,z,i],...]}，
只写非空气方块；包络内未覆盖坐标由 blueprint_io 按空气处理。

用法：
    py -3 tests/fixtures/generate_fixtures.py            # 生成全部夹具
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

STONE = "minecraft:stone"
DOOR_LO = "minecraft:oak_door[facing=north,half=lower,hinge=left,open=false,powered=false]"
DOOR_HI = "minecraft:oak_door[facing=north,half=upper,hinge=left,open=false,powered=false]"
STAIR_E = "minecraft:oak_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]"
STAIR_W = "minecraft:oak_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]"


class Scene:
    """体素场景构建器：放方块 → 导出 Canonical IR dict。"""

    def __init__(self, size: tuple[int, int, int]):
        self.size = size
        self.cells: dict[tuple[int, int, int], str] = {}

    def set(self, x: int, y: int, z: int, state: str) -> "Scene":
        self.cells[(x, y, z)] = state
        return self

    def fill(self, x0, y0, z0, x1, y1, z1, state: str) -> "Scene":
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                for z in range(z0, z1 + 1):
                    self.cells[(x, y, z)] = state
        return self

    def remove(self, x: int, y: int, z: int) -> "Scene":
        self.cells.pop((x, y, z), None)
        return self

    def to_ir(self) -> dict:
        palette = ["minecraft:air"]
        idx = {"minecraft:air": 0}
        blocks = []
        for (x, y, z), st in sorted(self.cells.items()):
            if st not in idx:
                idx[st] = len(palette)
                palette.append(st)
            blocks.append([x, y, z, idx[st]])
        return {
            "schema_version": 1,
            "metadata": {"generator": "generate_fixtures.py", "synthetic": True},
            "origin": [0, 0, 0],
            "dimensions": {"x": self.size[0], "y": self.size[1], "z": self.size[2]},
            "rotation": 0,
            "mirror": "NONE",
            "palette": palette,
            "blocks": blocks,
        }


# ---------------------------------------------------------------------------
# 建筑构件
# ---------------------------------------------------------------------------
FOOT = (2, 10)  # 房屋占地 x/z ∈ [2,10]，9×9；包络 13×13，四周留外部地面


def ground(sc: Scene) -> Scene:
    X, _, Z = sc.size
    return sc.fill(0, 0, 0, X - 1, 0, Z - 1, STONE)


def walls(sc: Scene, y0: int, y1: int) -> Scene:
    x0, x1 = FOOT
    z0, z1 = FOOT
    sc.fill(x0, y0, z0, x1, y1, z0, STONE)   # 北墙（正面）
    sc.fill(x0, y0, z1, x1, y1, z1, STONE)   # 南墙
    sc.fill(x0, y0, z0, x0, y1, z1, STONE)   # 西墙
    sc.fill(x1, y0, z0, x1, y1, z1, STONE)   # 东墙
    return sc


def slab_layer(sc: Scene, y: int, holes: list[tuple[int, int]] | None = None) -> Scene:
    x0, x1 = FOOT
    z0, z1 = FOOT
    sc.fill(x0, y, z0, x1, y, z1, STONE)
    for hx, hz in (holes or []):
        sc.remove(hx, y, hz)
    return sc


def place_door(sc: Scene, x: int, y: int, z: int) -> Scene:
    return sc.set(x, y, z, DOOR_LO).set(x, y + 1, z, DOOR_HI)


def single_story(with_door: bool = True) -> Scene:
    """单层小屋：地面 + 围墙 y1..3 + 屋顶 y4，正门朝北（-z）。"""
    sc = Scene((13, 6, 13))
    ground(sc)
    walls(sc, 1, 3)
    slab_layer(sc, 4)          # 屋顶
    if with_door:
        place_door(sc, 6, 1, 2)
    return sc


def two_story(stair: str | None = "east") -> Scene:
    """两层楼：围墙 y1..6，中层楼板 y3（楼梯井开洞），屋顶 y7。

    stair="east"：楼梯沿 z=4 从 x=3 升到 x=5（朝东上行），井洞 (3,4),(4,4)。
    stair="west"：楼梯沿 z=8 从 x=6 降到 x=4（朝西上行），井洞 (6,8),(5,8)。
    stair=None ：无楼梯（楼板不开洞）。
    """
    sc = Scene((13, 9, 13))
    ground(sc)
    walls(sc, 1, 6)
    if stair == "east":
        slab_layer(sc, 3, holes=[(3, 4), (4, 4)])
        sc.set(3, 1, 4, STAIR_E).set(4, 2, 4, STAIR_E).set(5, 3, 4, STAIR_E)
    elif stair == "west":
        slab_layer(sc, 3, holes=[(6, 8), (5, 8)])
        sc.set(6, 1, 8, STAIR_W).set(5, 2, 8, STAIR_W).set(4, 3, 8, STAIR_W)
    else:
        slab_layer(sc, 3)
    slab_layer(sc, 7)          # 屋顶
    place_door(sc, 6, 1, 2)
    return sc


# ---------------------------------------------------------------------------
# 8 组夹具 + 1 辅助
# ---------------------------------------------------------------------------
def build_all() -> dict[str, Scene]:
    fixtures: dict[str, Scene] = {}

    # 1. correct_entrance（正例）
    fixtures["correct_entrance"] = single_story(with_door=True)

    # 2. blocked_entrance（负例 → V002）：门内侧紧贴 2 格实体柱
    sc = single_story(with_door=True)
    sc.fill(6, 1, 3, 6, 2, 3, STONE)
    fixtures["blocked_entrance"] = sc

    # 3. correct_stair（正例）
    fixtures["correct_stair"] = two_story(stair="east")

    # 4. stair_top_blocked（负例 → V006）：顶端三面 y=4 层砌墙，“楼梯尽头是墙”
    sc = two_story(stair="east")
    for cell in [(5, 4, 3), (5, 4, 5), (6, 4, 4)]:
        sc.set(*cell, STONE)
    fixtures["stair_top_blocked"] = sc

    # 5. stair_bottom_blocked（负例 → V005）：底部楼梯四个接近方向全部封死
    sc = two_story(stair="east")
    for cell in [(3, 1, 3), (3, 2, 3), (3, 1, 5), (3, 2, 5), (4, 1, 4)]:
        sc.set(*cell, STONE)
    fixtures["stair_bottom_blocked"] = sc

    # 6. isolated_room（负例 → V004）：室内 x=6 无门隔墙，隔出封闭房间 B(x7..9)
    sc = single_story(with_door=False)     # 先不设门
    sc.fill(6, 1, 3, 6, 3, 9, STONE)       # 室内隔墙
    place_door(sc, 4, 1, 2)                # 房间 A 的门
    fixtures["isolated_room"] = sc

    # 7. broken_vertical_access（负例 → V007）：两层、楼板无洞、无楼梯无梯子
    fixtures["broken_vertical_access"] = two_story(stair=None)

    # 8. correct_multifloor（正例：两层 + 正常楼梯，不同方位）
    fixtures["correct_multifloor"] = two_story(stair="west")

    # 辅助负例 → V001：全封闭无门小屋
    fixtures["no_exterior_entrance"] = single_story(with_door=False)
    return fixtures


def main() -> None:
    out_dir = Path(__file__).resolve().parent
    fixtures = build_all()
    written = []
    for name, sc in fixtures.items():
        path = out_dir / f"{name}.json"
        path.write_text(json.dumps(sc.to_ir(), ensure_ascii=False), encoding="utf-8")
        written.append(path.name)
    print(json.dumps({"written": written, "dir": str(out_dir)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
