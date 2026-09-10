"""阶段1完整性检查发现对角主干断面；补成面接触，保留既有冠幅与树位。"""
from pathlib import Path
import numpy as np,json,gzip
R=Path(__file__).parent;s=json.loads((R/'场景.json').read_text(encoding='utf8'));P=s['palette'];old=np.load(R/'阶段1b.npy');v=old.copy();wood=P.index('minecraft:oak_log[axis=y]');added=set()
def connected_line(a,b):
 last=list(a);n=max(abs(b[i]-a[i]) for i in range(3))
 for j in range(n+1):
  now=[round(a[i]+(b[i]-a[i])*j/max(n,1)) for i in range(3)]
  for axis in range(3):
   while last[axis]!=now[axis]:
    last[axis]+=1 if now[axis]>last[axis] else -1;x,y,z=last
    if v[x,y-56,z]==0:v[x,y-56,z]=wood;added.add((x,y,z))
for x,y,z,h,r in s['trees']:
 connected_line((x,y,z),(x+1,y+h-4,z))
 for dx,dz,dh in [(-3,2,-2),(3,-1,0),(1,3,-3)]:connected_line((x,y+h-7,z),(x+dx,y+h+dh-3,z+dz))
np.save(R/'阶段1c.npy',v)
for n in [2,3]:
 a=np.load(R/f'阶段{n}.npy')
 for x,y,z in added:
  if a[x,y-56,z]==0:a[x,y-56,z]=wood
 np.save(R/f'阶段{n}.npy',a)
folder=R/'蓝图/1c-树干面接触修订';folder.mkdir(exist_ok=True);ph=[]
for tx in range(0,256,64):
 for tz in range(0,256,64):
  rows=[[x,y,z,wood] for x,y,z in sorted(added) if tx<=x<tx+64 and tz<=z<tz+64]
  if not rows:continue
  lo=[min(r[i] for r in rows) for i in range(3)];hi=[max(r[i] for r in rows) for i in range(3)];bp={'schema_version':1,'origin':dict(zip(['x','y','z'],lo)),'dimensions':dict(zip(['x','y','z'],[b-a+1 for a,b in zip(lo,hi)])),'palette':P,'blocks':[[x-lo[0],y-lo[1],z-lo[2],p] for x,y,z,p in rows]}
  with gzip.open(folder/f'{tx}_{tz}.json.gz','wt',encoding='utf8') as f:json.dump(bp,f,separators=(',',':'))
  ph.append({'palette':P,'operations':[[x,y,z,x,y,z,p] for x,y,z,p in rows]})
(R/'作业/1c.json').write_text(json.dumps({'world_path':'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V12-T03-河谷村落','phases':ph},separators=(',',':')),encoding='utf8');print('树干接触修订',len(added))
