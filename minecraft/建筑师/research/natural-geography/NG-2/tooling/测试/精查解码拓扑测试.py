"""检查跨 long 填充、signed long 与不允许跨干桥/斜角/不同水位伪连通的拓扑契约。"""
import sys
import unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
sys.path.append('D:/Games/Minecraft/AI工程/AI-Blueprints/参考入库/第三方')
from L1_器件层.区块柱读取器 import unpack
from L1_器件层.局部指标计算器 import components,outer_ring

class RefinementTests(unittest.TestCase):
    def test_island_inner_pond_is_not_outer_sea(self):
        land=np.zeros((9,9),bool);land[2:7,2:7]=True;land[4,4]=False
        outer,inner=outer_ring(land)
        self.assertFalse(outer[4,4]);self.assertTrue(inner[4,4]);self.assertEqual(int(outer.sum()),20)
    def test_open_cove_is_part_of_outer_boundary(self):
        land=np.zeros((9,9),bool);land[2:7,2:7]=True;land[2:5,4]=False
        outer,inner=outer_ring(land)
        self.assertTrue(outer[4,4]);self.assertFalse(inner.any())
    def test_ten_bit_padded_heightmap(self):
        words=[1|(63<<10)|(128<<20)|(320<<30)|(640<<40)|(832<<50),17]
        self.assertEqual(unpack(words,10,7).tolist(),[1,63,128,320,640,832,17])
    def test_signed_palette(self):self.assertEqual(unpack([-1],4,16).tolist(),[15]*16)
    def test_diagonal_water_not_connected(self):
        labels,counts=components(np.eye(2,dtype=bool));self.assertEqual(counts,[1,1])
    def test_nonoverlapping_water_heights_not_connected(self):
        labels,counts=components(np.ones((1,2),bool),np.array([[62,70]]),np.array([[60,68]]));self.assertEqual(counts,[1,1])
    def test_shared_water_y_connects_under_ice(self):
        labels,counts=components(np.ones((1,2),bool),np.array([[62,61]]),np.array([[45,47]]));self.assertEqual(counts,[2])
    def test_single_column_dry_bridge_is_preserved(self):
        mask=np.ones((5,5),bool);mask[:,2]=False
        labels,counts=components(mask);self.assertEqual(sorted(counts),[10,10])

if __name__=='__main__':unittest.main()
