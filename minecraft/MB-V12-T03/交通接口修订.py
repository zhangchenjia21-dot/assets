"""阶段2读回后的局部重构：北路避让农舍，修复上层交通与支承。"""
from pathlib import Path
import numpy as np,json,gzip,math
R=Path(__file__).parent;s=json.loads((R/'场景.json').read_text(encoding='utf8'));P=s['palette'];old=np.load(R/'阶段2.npy');v=old.copy();terrain=np.load(R/'阶段1c.npy')
def mid(name):return P.index('minecraft:'+name)
def box(x,y,z,X,Y,Z,p):v[x:X+1,y-56:Y-55,z:Z+1]=p
stone=mid('stone');cobble=mid('cobblestone');wood=mid('oak_planks');log=mid('oak_log[axis=y]');beam=mid('stripped_oak_log[axis=x]');clay=mid('packed_mud');plaster=mid('white_terracotta');gravel=mid('gravel');stair=mid('spruce_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]')
# 先恢复冲突旧路区域的地形，再重建指定农舍，避免旧切口残留。
v[112:125,:35,59:93]=terrain[112:125,:35,59:93]
box(106,73,67,119,86,82,0);box(107,56,68,118,72,81,cobble);box(108,72,69,117,72,80,wood);box(107,73,68,118,76,81,clay);box(108,73,69,117,76,80,0)
for x in [107,112,117]:box(x,73,68,x,76,68,log);box(x,73,81,x,76,81,log)
for z in [68,73,78]:box(107,73,z,107,76,z,log);box(118,73,z,118,76,z,log)
box(107,76,68,118,76,68,beam);box(107,76,81,118,76,81,beam)
for x in range(106,120):
 y=77+min(x-106,119-x);face='east' if x<112.5 else 'west';box(x,y,67,x,y,82,mid(f'bamboo_stairs[facing={face},half=bottom,shape=straight,waterlogged=false]'))
 if 107<=x<=118:box(x,77,68,x,y-1,68,plaster);box(x,77,81,x,y-1,81,plaster)
box(118,73,72,118,75,73,0)
for x in [110,115]:box(x,74,68,x,75,68,0)
def road(pts,width=3):
 surface={};cells=[]
 for a,b in zip(pts,pts[1:]):
  x,y,z=a;X,Y,Z=b;dx,dz=X-x,Z-z;ll=dx*dx+dz*dz
  for xx in range(min(x,X)-2,max(x,X)+3):
   for zz in range(min(z,Z)-2,max(z,Z)+3):
    t=max(0,min(1,((xx-x)*dx+(zz-z)*dz)/ll));distance=(xx-x-dx*t)**2+(zz-z-dz*t)**2
    if distance<=(width/2)**2 and ((xx,zz) not in surface or distance<surface[xx,zz][0]):surface[xx,zz]=(distance,round(y+(Y-y)*t))
  n=max(abs(dx),abs(dz));cells.extend([[round(x+dx*k/n),round(y+(Y-y)*k/n),round(z+dz*k/n)] for k in range(n+1)])
 for (x,z),(d,y) in surface.items():box(x,56,z,x,y-1,z,stone);box(x,y,z,x,y,z,gravel);box(x,y+1,z,x,y+3,z,0)
 return [[x,surface[x,z][1],z] for x,y,z in cells]
route=road([(113,72,92),(124,72,89),(125,74,72),(125,75,62),(110,77,54),(98,79,63),(86,81,61)],3)
s['routes'][2]={'name':'北庄道（绕宅修订）','cells':route};s['routes'][0]['cells']=s['routes'][0]['cells'][:next(i for i,p in enumerate(s['routes'][0]['cells']) if p[0]==113 and p[2]==92)+1]
for r in s['routes']:
 if r['name']=='宅前F':r['cells']=road([(119,72,72),(125,74,72)],3)
# 磨坊上粮阶顶部接入门洞；庄园木阶的下部做连续梯梁实体。
box(179,72,87,180,72,89,wood);box(179,73,87,180,75,89,0)
for i in range(7):
 x,z,y=75,48-i,81+i;box(x,82,z,x+1,max(82,y-1),z,wood);box(x,y,z,x+1,y,z,stair);box(x,y+1,z,x+1,y+3,z,0)
for d in s['doors']:
 if d['name'] in ['厅屋E','东岸H']:
  h=next(a for a in s['homes'] if a[0]==d['name']);d['inside']=[(h[1]+h[3])//2,h[5]+1,(h[2]+h[4])//2]
# 原采样的对角投影偶有一格舍入差，按附近真实路面修正，不越过障碍或更改地面。
for r in s['routes']:
 for p in r['cells']:
  x,y,z=p
  if v[x,y+1-56,z]!=0 and v[x,y+2-56,z]==0 and v[x,y+3-56,z]==0 and P[int(v[x,y+1-56,z])].startswith('minecraft:gravel'):p[1]+=1
np.save(R/'阶段2b.npy',v);future=np.load(R/'阶段3.npy');mask=v!=old;future[mask]=v[mask];np.save(R/'阶段3.npy',future);(R/'场景.json').write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding='utf8')
folder=R/'蓝图/2b-北路住宅与上层接口';folder.mkdir(exist_ok=True);ph=[];count=0
for x in range(0,256,32):
 for y in range(0,80,32):
  for z in range(0,256,32):
   q=np.argwhere(mask[x:x+32,y:y+32,z:z+32])
   if not len(q):continue
   b=[[int(a),int(c),int(d),int(v[x+a,y+c,z+d])] for a,c,d in q];count+=len(b);bp={'schema_version':1,'origin':{'x':x,'y':y+56,'z':z},'dimensions':{'x':32,'y':min(32,80-y),'z':32},'palette':P,'blocks':b}
   with gzip.open(folder/f'{x}_{y}_{z}.json.gz','wt',encoding='utf8') as f:json.dump(bp,f,separators=(',',':'))
   ph.append({'palette':P,'operations':[[x+a,y+c+56,z+d,x+a,y+c+56,z+d,p] for a,c,d,p in b]})
(R/'作业/2b.json').write_text(json.dumps({'world_path':'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V12-T03-河谷村落','phases':ph},separators=(',',':')),encoding='utf8');print(count)
