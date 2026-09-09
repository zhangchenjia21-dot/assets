import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from L2_流程层.查询汇编流程 import build
build(Path(__file__).resolve().parents[2])
