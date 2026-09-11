"""仅清除橘园窗面修订误伸入门洞中央的三格玻璃，保留门楣上方采光窗。"""
from pathlib import Path
import json,gzip,numpy as np
R=Path(__file__).parent;s=json.loads((R/'场景.json').read_text(encoding='utf8'));P=s['palette'];v=np.load(R/'阶段03b.npy');a=P.index('minecraft:air');g=P.index('minecraft:light_blue_stained_glass')
for y in [67,68,69]:assert v[43,y-56,130]==g;v[43,y-56,130]=a
np.save(R/'阶段03c.npy',v);folder=R/'蓝图/03c';folder.mkdir(parents=True,exist_ok=True);bp={'schema_version':1,'origin':{'x':43,'y':67,'z':130},'dimensions':{'x':1,'y':3,'z':1},'palette':P,'blocks':[[0,y,0,a] for y in range(3)]};(folder/'门洞.json.gz').write_bytes(gzip.compress(json.dumps(bp,separators=(',',':')).encode(),mtime=0));(R/'作业/03c.json').write_text(json.dumps({'world_path':'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V15-T06-规则宫苑','phases':[{'palette':P,'operations':[[43,67,130,43,69,130,a]]}]},separators=(',',':')),encoding='utf8')
