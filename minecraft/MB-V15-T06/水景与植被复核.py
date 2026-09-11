"""实存水池分别核对连通/水位；植物只验证土壤支承，不冒充流体或生态运行。"""
from pathlib import Path
from collections import deque
import json,numpy as np
R=Path(__file__).parent;E=R/'证据';s=json.loads((R/'场景.json').read_text(encoding='utf8'));m=json.loads((E/'03c.json').read_text(encoding='utf8'));P=m['palette'];base=[p.split('[')[0] for p in P];v=np.fromfile(E/'03c.bin',np.uint8).reshape(m['size']);water=np.isin(v,[i for i,p in enumerate(base) if p=='minecraft:water']);report=[]
for p in s['pools']:
 x,y,z,X,Y,Z=p['bounds'];pts={tuple(map(int,a)) for a in np.argwhere(water[x:X+1,y-56:Y-55,z:Z+1])};total=len(pts);parts=[]
 while pts:
  q=deque([pts.pop()]);count=0
  while q:
   a,b,c=q.popleft();count+=1
   for t in [(a-1,b,c),(a+1,b,c),(a,b-1,c),(a,b+1,c),(a,b,c-1),(a,b,c+1)]:
    if t in pts:pts.remove(t);q.append(t)
  parts.append(count)
 report.append({'name':p['name'],'water_cells':total,'components':parts,'designed_water_y':p['level'],'fluid_update_stability':'unverified'})
plants=[i for i,p in enumerate(base) if p in ['minecraft:red_tulip','minecraft:white_tulip','minecraft:orange_tulip','minecraft:cornflower','minecraft:fern']];soils=[i for i,p in enumerate(base) if p in ['minecraft:dirt','minecraft:grass_block','minecraft:podzol']];invalid=[]
for x,y,z in np.argwhere(np.isin(v,plants)):
 if v[x,y-1,z] not in soils:invalid.append([int(x),int(y+56),int(z)])
out={'pools':report,'unsupported_plants':invalid,'plant_counts':{P[i]:int((v==i).sum()) for i in plants}};(E/'水景与植被检查.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(out,ensure_ascii=True))
