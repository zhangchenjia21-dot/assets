"""按地面玩家视点降低花坛内部篱边，用苔藓薄层近似低修剪带；不改园室绿墙。"""
from pathlib import Path
import json,gzip,numpy as np
R=Path(__file__).parent;s=json.loads((R/'场景.json').read_text(encoding='utf8'));P=s['palette'];state='minecraft:moss_carpet'
if state not in P:P.append(state);s['colors'].append([62,104,44])
p=P.index(state);old=np.load(R/'阶段03a.npy');v=old.copy();leaf=P.index('minecraft:oak_leaves[distance=1,persistent=true,waterlogged=false]')
for x0 in [81,131]:
 for z0 in [122,156]:
  for x in range(x0-16,x0+17):
   for z in range(z0-13,z0+14):
    if v[x,65-56,z]==leaf:v[x,65-56,z]=p
np.save(R/'阶段03b.npy',v);s['palette']=P;(R/'场景.json').write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding='utf8');q=np.argwhere(v!=old);b=[[int(x-64),int(y),int(z-96),int(v[x,y,z])] for x,y,z in q];folder=R/'蓝图/03b';folder.mkdir(parents=True,exist_ok=True);bp={'schema_version':1,'origin':{'x':64,'y':56,'z':96},'dimensions':{'x':96,'y':32,'z':80},'palette':P,'blocks':b};(folder/'纹样低篱.json.gz').write_bytes(gzip.compress(json.dumps(bp,separators=(',',':')).encode(),mtime=0));(R/'作业/03b.json').write_text(json.dumps({'world_path':'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V15-T06-规则宫苑','phases':[{'palette':P,'operations':[[x+64,y+56,z+96,x+64,y+56,z+96,p] for x,y,z,p in b]}]},separators=(',',':')),encoding='utf8');print(len(b))
