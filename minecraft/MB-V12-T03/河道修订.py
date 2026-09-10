"""阶段1实际透视发现河面覆盖层；只清理河道范围，保留阶段1原始证据。"""
from pathlib import Path
import numpy as np,json,gzip,math
R=Path(__file__).parent;s=json.loads((R/'场景.json').read_text(encoding='utf8'));P=s['palette'];old=np.load(R/'阶段1.npy');v=old.copy();clear=[]
for z in range(75,256):
 center=137+17*math.sin(z/48)+7*math.sin(z/21);width=6+1.2*math.sin(z/17)
 for x in range(256):
  if abs(x-center)<width and P[int(v[x,7,z])].split('[')[0] in ['minecraft:grass_block','minecraft:dirt']:clear.append([x,63,z])
for x in range(round(137+17*math.sin(100/48)+7*math.sin(100/21)),161):
 for z in range(100,103):
  for y in range(63,72):
   if P[int(v[x,y-56,z])].split('[')[0] in ['minecraft:grass_block','minecraft:dirt','minecraft:stone']:clear.append([x,y,z])
for x,y,z in clear:v[x,y-56,z]=0
np.save(R/'阶段1b.npy',v)
# 后续已有施工批次没有指定这些清理格；同步最终预期模型，原阶段蓝图不改写。
for n in [2,3]:
 a=np.load(R/f'阶段{n}.npy')
 for x,y,z in clear:
  if a[x,y-56,z]==old[x,y-56,z]:a[x,y-56,z]=0
 np.save(R/f'阶段{n}.npy',a)
rows=[[int(x),int(y+56),int(z),0] for x,y,z in np.argwhere(v!=old)];folder=R/'蓝图/1b-河面与尾水沟清理';folder.mkdir(exist_ok=True);ph=[]
for z in range(64,256,64):
 b=[r for r in rows if z<=r[2]<z+64]
 if not b:continue
 lo=[min(r[i] for r in b) for i in range(3)];hi=[max(r[i] for r in b) for i in range(3)];bp={'schema_version':1,'origin':dict(zip(['x','y','z'],lo)),'dimensions':dict(zip(['x','y','z'],[h-l+1 for l,h in zip(lo,hi)])),'palette':P,'blocks':[[x-lo[0],y-lo[1],zz-lo[2],p] for x,y,zz,p in b]}
 with gzip.open(folder/f'{z}.json.gz','wt',encoding='utf8') as f:json.dump(bp,f,separators=(',',':'))
 ph.append({'palette':P,'operations':[[x,y,zz,x,y,zz,p] for x,y,zz,p in b]})
(R/'作业/1b.json').write_text(json.dumps({'world_path':'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V12-T03-河谷村落','phases':ph},separators=(',',':')),encoding='utf8');print('河道修订',len(rows))
