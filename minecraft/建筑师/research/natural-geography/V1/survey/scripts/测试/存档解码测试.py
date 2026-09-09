"""覆盖 signed long、long 填充边界与负坐标空间索引。"""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from L0_公理层.地理契约 import packed,palette_value

class PackingTest(unittest.TestCase):
    def test_ten_bit_height_long_boundary(self):
        # 832 高度世界使用 10 bit，每 long 六值，剩余四位是填充。
        words=[(1 | 63<<10 | 128<<20 | 320<<30 | 640<<40 | 832<<50),17]
        self.assertEqual([packed(words,i,10) for i in range(7)],[1,63,128,320,640,832,17])
    def test_signed_block_word(self):
        self.assertEqual(packed([-1],15,4),15)
    def test_single_palette(self):
        self.assertEqual(palette_value({'palette':['water']},4095,4),'water')
    def test_negative_grid(self):
        self.assertEqual((-1//64,-64//64,-65//64),(-1,-1,-2))

if __name__=='__main__':unittest.main()
