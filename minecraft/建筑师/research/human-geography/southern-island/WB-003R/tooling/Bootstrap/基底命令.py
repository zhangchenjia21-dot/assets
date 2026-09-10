import sys,argparse
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]));sys.path.append('D:/Games/Minecraft/AI工程/AI-Blueprints/参考入库/第三方')
from L3_外交层.基底公开接口 import run
p=argparse.ArgumentParser();p.add_argument('command');p.add_argument('--cache',type=Path,default=Path('D:/Games/Minecraft/AI工程/研究缓存/建筑师/WB-003R'));p.add_argument('--world',type=Path,default=Path('D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/建筑师'));args=p.parse_args()
run(args.command,Path(__file__).resolve().parents[2],args.cache.resolve(),args.world.resolve())
