import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
sys.path.append('D:/Games/Minecraft/AI工程/AI-Blueprints/参考入库/第三方')
from L3_外交层.范围公开接口 import execute
execute(Path(__file__).resolve().parents[2],Path(sys.argv[1]))
