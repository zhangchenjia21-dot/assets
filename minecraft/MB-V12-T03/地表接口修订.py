"""阶段3实存检查后：移动井体，石标落地。"""
from pathlib import Path
import numpy as np,json,gzip
R=Path(__file__).parent;s=json.loads((R/'场景.json').read_text(encoding='utf8'));P=s['palette'];old=np.load(R/'阶段3.npy');v=old.copy();base=np.load(R/'阶段2b.npy')
v[100:105,14:16,137:142]=base[100:105,14:16,137:142]
c=P.index('minecraft:cobblestone');w=P.index('minecraft:water[level=0]')
v[105:109,0:16,147:151]=c;v[106:108,15,148:150]=w
for x in range(48,79,5):
 for z in [79,80]:
  v[x,27,z]=base[x,27,z]
  yy=max(y for y in range(27) if v[x,y,z]!=0)
  v[x,yy+1,z]=P.index('minecraft:sandstone')
mask=v!=old;np.save(R/'阶段3b.npy',v)
folder=R/'蓝图/3b-公共井与石标接口';folder.mkdir(exist_ok=True);ph=[];count=0
for x in range(0,256,32):
 for y in range(0,80,32):
  for z in range(0,256,32):
   q=np.argwhere(mask[x:x+32,y:y+32,z:z+32])
   if not len(q):continue
   b=[[int(a),int(c),int(d),int(v[x+a,y+c,z+d])] for a,c,d in q];count+=len(b);bp={'schema_version':1,'origin':{'x':x,'y':y+56,'z':z},'dimensions':{'x':32,'y':min(32,80-y),'z':32},'palette':P,'blocks':b}
   with gzip.open(folder/f'{x}_{y}_{z}.json.gz','wt',encoding='utf8') as f:json.dump(bp,f,separators=(',',':'))
   ph.append({'palette':P,'operations':[[x+a,y+c+56,z+d,x+a,y+c+56,z+d,p] for a,c,d,p in b]})
(R/'作业/3b.json').write_text(json.dumps({'world_path':'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V12-T03-河谷村落','phases':ph},separators=(',',':')),encoding='utf8');print(count)
