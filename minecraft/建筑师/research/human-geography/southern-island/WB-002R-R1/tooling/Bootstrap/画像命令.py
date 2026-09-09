import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from L3_外交层.画像公开接口 import derive
derive(Path(__file__).resolve().parents[2])
