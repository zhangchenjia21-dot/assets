# -*- coding: utf-8 -*-
"""walkability 模型单元测试（合成体素场景）。

运行（在 $OUT 根目录下）：
    py -3 -m unittest tests.test_walkability -v

覆盖场景：
1. 平地可走                    6. 栅栏挡人
2. 2 格高墙挡人                7. 梯子垂直连通
3. 半砖可站上（0.5 步高）      8. 净高不足不可站
4. 楼梯连通上下层              9. 未知方块统计
5. 门可过（open / 木质 closed；铁门 closed 阻挡）  10. 死端检测

说明：露天场景里“墙顶/高台顶”本身也是合法站位（天空无遮挡），会形成自己的
小组件，因此断言一律用分量标签（labels）判断两侧连通性，而不是数组件总数。
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

# 让测试可直接找到 scripts/ 下的模块
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import walkability  # noqa: E402
from blueprint_io import BlueprintIR  # noqa: E402


def make_ir(palette: list[str]) -> BlueprintIR:
    """从 palette 字符串列表构造最小 BlueprintIR（供合成场景）。"""
    from blueprint_io import parse_block_state

    block_ids, props = [], []
    for st in palette:
        bid, p = parse_block_state(st)
        block_ids.append(bid)
        props.append(p)
    return BlueprintIR(
        path=Path("synthetic"),
        ir_source="normalized",
        ref_id=None,
        schema_version=1,
        metadata={},
        origin=(0, 0, 0),
        dimensions=(0, 0, 0),
        rotation=None,
        mirror=None,
        palette=palette,
        block_ids=block_ids,
        properties=props,
        blocks=np.zeros((0, 4), dtype=np.int32),
    )


class Scene:
    """合成场景构建器：按名称放方块。"""

    def __init__(self, size: tuple[int, int, int]):
        self.names: list[str] = ["minecraft:air"]
        self.idx: dict[str, int] = {"minecraft:air": 0}
        self.vox = np.zeros(size, dtype=np.int32)

    def id_of(self, state: str) -> int:
        if state not in self.idx:
            self.idx[state] = len(self.names)
            self.names.append(state)
        return self.idx[state]

    def fill(self, x0, y0, z0, x1, y1, z1, state: str) -> "Scene":
        i = self.id_of(state)
        self.vox[x0:x1 + 1, y0:y1 + 1, z0:z1 + 1] = i
        return self

    def analyze(self, **kw):
        kw.setdefault("return_labels", True)
        ir = make_ir(self.names)
        return walkability.analyze(self.vox, ir, **kw)


STONE = "minecraft:stone"


def label_at(result, x, y, z):
    return int(result["labels"][x, y, z])


class TestWalkability(unittest.TestCase):
    def test_flat_ground_walkable(self):
        """平地：5×5 石板地面，其上为空气 → 25 个站位、1 个分量。"""
        sc = Scene((5, 5, 5))
        sc.fill(0, 0, 0, 4, 0, 4, STONE)
        r = sc.analyze()
        self.assertEqual(r["walkable_voxels"], 25)
        self.assertEqual(r["walkable_components"], 1)
        self.assertAlmostEqual(r["largest_component_ratio"], 1.0)

    def test_two_block_wall_blocks(self):
        """2 格高墙挡人：墙两侧地面站位分属不同分量。"""
        sc = Scene((5, 4, 5))
        sc.fill(0, 0, 0, 4, 0, 4, STONE)          # 地面
        sc.fill(2, 1, 0, 2, 2, 4, STONE)          # 高 2 的墙
        r = sc.analyze(isolated_min_size=1)
        left = label_at(r, 1, 0, 2)               # 地面支撑体素（墙左）
        right = label_at(r, 3, 0, 2)              # 墙右
        self.assertNotEqual(left, -1)
        self.assertNotEqual(right, -1)
        self.assertNotEqual(left, right)
        self.assertGreaterEqual(r["walkable_components"], 2)

    def test_slab_step_up(self):
        """半砖可站上：地面 → bottom 半砖抬高区，0.5 步高连通。"""
        sc = Scene((6, 4, 3))
        sc.fill(0, 0, 0, 5, 0, 2, STONE)                       # 地面
        sc.fill(3, 1, 0, 5, 1, 2, "minecraft:stone_slab[type=bottom]")  # 半砖抬高区
        r = sc.analyze()
        self.assertEqual(r["walkable_components"], 1)
        # 站位：左侧地面 3×3=9 + 半砖 3×3=9 = 18
        self.assertEqual(r["walkable_voxels"], 18)

    def test_stairs_connect_floors(self):
        """楼梯连通上下层：连续 3 级楼梯从地面升到 3 格高平台。"""
        sc = Scene((8, 6, 3))
        sc.fill(0, 0, 0, 7, 0, 2, STONE)          # 地面
        sc.fill(2, 1, 1, 2, 1, 1, "minecraft:oak_stairs[facing=east,half=bottom]")
        sc.fill(3, 2, 1, 3, 2, 1, "minecraft:oak_stairs[facing=east,half=bottom]")
        sc.fill(4, 3, 1, 4, 3, 1, "minecraft:oak_stairs[facing=east,half=bottom]")
        sc.fill(5, 3, 0, 7, 3, 2, STONE)          # 高平台（顶面 4.0）
        r = sc.analyze()
        base = label_at(r, 1, 0, 1)               # 楼梯入口前的地面站位
        top = label_at(r, 6, 3, 1)                # 平台顶面站位
        self.assertNotEqual(base, -1)
        self.assertNotEqual(top, -1)
        self.assertEqual(base, top)
        self.assertEqual(r["walkable_components"], 1)
        self.assertGreater(r["vertical_connections"], 0)

    def test_door_passable(self):
        """敞开的门可过：墙中橡木 open 门两侧站位同分量。"""
        sc = Scene((5, 4, 5))
        sc.fill(0, 0, 0, 4, 0, 4, STONE)
        sc.fill(2, 1, 0, 2, 2, 4, STONE)          # 墙
        sc.fill(2, 1, 2, 2, 1, 2, "minecraft:oak_door[facing=east,half=lower,hinge=left,open=true,powered=false]")
        sc.fill(2, 2, 2, 2, 2, 2, "minecraft:oak_door[facing=east,half=upper,hinge=left,open=true,powered=false]")
        r = sc.analyze(isolated_min_size=1)
        self.assertEqual(label_at(r, 1, 0, 2), label_at(r, 3, 0, 2))

    def test_closed_wooden_door_passable_but_iron_blocked(self):
        """木质关门可交互通过；关闭的铁门阻挡。"""
        sc = Scene((5, 4, 5))
        sc.fill(0, 0, 0, 4, 0, 4, STONE)
        sc.fill(2, 1, 0, 2, 2, 4, STONE)
        sc.fill(2, 1, 2, 2, 1, 2, "minecraft:oak_door[facing=east,half=lower,hinge=left,open=false,powered=false]")
        sc.fill(2, 2, 2, 2, 2, 2, "minecraft:oak_door[facing=east,half=upper,hinge=left,open=false,powered=false]")
        r = sc.analyze(isolated_min_size=1)
        self.assertEqual(label_at(r, 1, 0, 2), label_at(r, 3, 0, 2))

        sc2 = Scene((5, 4, 5))
        sc2.fill(0, 0, 0, 4, 0, 4, STONE)
        sc2.fill(2, 1, 0, 2, 2, 4, STONE)
        sc2.fill(2, 1, 2, 2, 1, 2, "minecraft:iron_door[facing=east,half=lower,hinge=left,open=false,powered=false]")
        sc2.fill(2, 2, 2, 2, 2, 2, "minecraft:iron_door[facing=east,half=upper,hinge=left,open=false,powered=false]")
        r2 = sc2.analyze(isolated_min_size=1)
        self.assertNotEqual(label_at(r2, 1, 0, 2), label_at(r2, 3, 0, 2))

    def test_fence_blocks(self):
        """栅栏挡人：1 格高栅栏（碰撞 1.5）两侧站位不同分量。"""
        sc = Scene((5, 4, 5))
        sc.fill(0, 0, 0, 4, 0, 4, STONE)
        sc.fill(2, 1, 0, 2, 1, 4, "minecraft:oak_fence[east=false,north=false,south=false,west=false,waterlogged=false]")
        r = sc.analyze(isolated_min_size=1)
        self.assertNotEqual(label_at(r, 1, 0, 2), label_at(r, 3, 0, 2))

    def test_ladder_vertical_connection(self):
        """梯子垂直连通：地面 → 梯柱 → 3 格高平台同分量。"""
        sc = Scene((5, 6, 5))
        sc.fill(0, 0, 0, 4, 0, 4, STONE)          # 地面
        sc.fill(4, 3, 0, 4, 3, 4, STONE)          # 高台（顶面 4.0）
        for y in (1, 2, 3):                        # 梯柱贴在高台侧面 x=3, z=2
            sc.fill(3, y, 2, 3, y, 2, "minecraft:ladder[facing=east,waterlogged=false]")
        r = sc.analyze(isolated_min_size=1)
        ground = label_at(r, 2, 0, 2)             # 梯旁地面站位
        top = label_at(r, 4, 3, 2)                # 高台顶面站位
        self.assertNotEqual(ground, -1)
        self.assertNotEqual(top, -1)
        self.assertEqual(ground, top)
        self.assertGreaterEqual(r["ladder_vertical_edges"], 1)

    def test_low_ceiling_not_standable(self):
        """净高不足：距地面 1 格处压顶板 → 地板站位全部非法（顶板顶面除外）。"""
        sc = Scene((5, 3, 5))
        sc.fill(0, 0, 0, 4, 0, 4, STONE)          # 地面
        sc.fill(0, 2, 0, 4, 2, 4, STONE)          # 顶板（净空 1 格 < 1.8）
        r = sc.analyze()
        # 地面支撑体素上的站位全部因净高不足被清除
        self.assertEqual(label_at(r, 2, 0, 2), -1)
        self.assertEqual(label_at(r, 0, 0, 0), -1)
        # 顶板顶面（露天）仍是合法站位
        self.assertNotEqual(label_at(r, 2, 2, 2), -1)

    def test_unknown_block_counted(self):
        """未知方块：标 UNKNOWN 计入统计，保守视为阻挡。"""
        sc = Scene((3, 3, 3))
        sc.fill(0, 0, 0, 2, 0, 2, STONE)
        sc.fill(1, 1, 1, 1, 1, 1, "mymod:strange_machine")
        r = sc.analyze()
        self.assertIn("mymod:strange_machine", r["unknown_block_types"])
        self.assertEqual(r["unknown_block_type_count"], 1)

    def test_dead_end_detection(self):
        """死端：1 格宽走廊尽头被封死 → 存在死端节点。"""
        sc = Scene((7, 3, 3))
        sc.fill(0, 0, 0, 6, 0, 2, STONE)          # 地面
        sc.fill(0, 1, 0, 6, 2, 0, STONE)          # 南墙
        sc.fill(0, 1, 2, 6, 2, 2, STONE)          # 北墙
        sc.fill(6, 1, 1, 6, 2, 1, STONE)          # 东端封死
        r = sc.analyze()
        self.assertGreaterEqual(r["dead_end_count"], 1)


if __name__ == "__main__":
    unittest.main()
