"""玩家高度实存观察发现屋顶环带缺失，补齐封顶石，不覆盖内部楼梯出口。"""
from pathlib import Path
import json,gzip,numpy as np
R=Path(__file__).parent;s=json.loads((R/'场景.json').read_text(encoding='utf8'));P=s['palette'];v=np.load(R/'阶段03.npy');b=[];p=P.index('minecraft:stone_bricks')
for x in range(114,136):
 for z in range(86,109):
  if x<116 or x>133 or z<88 or z>106:
   if v[x,143-56,z]!=p:v[x,143-56,z]=p;b.append([x-112,143-128,z-80,p])
np.save(R/'阶段03a.npy',v);folder=R/'蓝图/03a';folder.mkdir(exist_ok=True)
bp={'schema_version':1,'origin':{'x':112,'y':128,'z':80},'dimensions':{'x':32,'y':32,'z':32},'palette':P,'blocks':b}
with gzip.open(folder/'tower-cap.json.gz','wt',encoding='utf8') as f:json.dump(bp,f,separators=(',',':'))
job={'world_path':'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V13-T04-山脊城堡','phases':[{'palette':P,'operations':[[x+112,y+128,z+80,x+112,y+128,z+80,p] for x,y,z,p in b]}]}
(R/'作业/03a.json').write_text(json.dumps(job,separators=(',',':')),encoding='utf8');print(len(b))
