import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from L1_器件层.完整地图生成器 import render
render(Path(__file__).resolve().parents[2])
