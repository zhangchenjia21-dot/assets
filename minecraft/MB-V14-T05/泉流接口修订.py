"""为分段水位补连续跌水接口，限定在原泉沟断面，不改变林地和后续结构。"""
from pathlib import Path
import json,gzip,numpy as np,math
R=Path(__file__).parent;s=json.loads((R/'场景.json').read_text(encoding='utf8'));P=s['palette'];old=np.load(R/'阶段01.npy');v=old.copy();water=P.index('minecraft:water[level=0]')
for z,low,high in [(65,70,72),(83,68,70),(104,65,68),(184,64,65),(211,63,64)]:
 cx=round(148+12*math.sin((z-42)/31)) if z<129 else round(111+10*math.sin((z-174)/26))
 for x in range(cx-2,cx+3):v[x,low-56:high-55,z]=water
# 原泉沟末端错误转向形成的小水袋恢复为原土丘。
for x in range(98,105):
 for z in range(129,132):
  west=10*math.exp(-((x-72)/44)**2-((z-94)/56)**2);north=13*math.exp(-((x-166)/57)**2-((z-48)/35)**2);east=7*math.exp(-((x-205)/34)**2-((z-132)/55)**2)
  swale=-3*math.exp(-((x-(122+12*math.sin(z/34)))/16)**2)*math.exp(-((z-156)/65)**2)
  pocket=1.3*math.sin(x/13+z/19)*math.sin(z/11)*min(1,(west+north+east)/8);y=round(64+west+north+east+swale+pocket)
  for yy in range(56,y+1):v[x,yy-56,z]=P.index('minecraft:grass_block[snowy=false]') if yy==y else P.index('minecraft:dirt') if yy>=y-2 else P.index('minecraft:stone')
# 两条短沟分别把泉流接入池北岸、把池水导入下游；宽五格、连续水位。
for pts in [[(153,127),(149,132),(146,135)],[(123,165),(116,170),(109,175)]]:
 for (x,z),(X,Z) in zip(pts,pts[1:]):
  n=max(abs(X-x),abs(Z-z))
  for k in range(n+1):
   a=round(x+(X-x)*k/n);c=round(z+(Z-z)*k/n)
   for dx in range(-2,3):
    for dz in range(-1,2):
     xx,zz=a+dx,c+dz
     v[xx,7,zz]=P.index('minecraft:mud');v[xx,8:10,zz]=water
     for yy in range(66,70):
      if v[xx,yy-56,zz] in [P.index('minecraft:stone'),P.index('minecraft:dirt'),P.index('minecraft:grass_block[snowy=false]')]:v[xx,yy-56,zz]=0
mask=v!=old;np.save(R/'阶段01a.npy',v)
for name in ['02','03']:
 f=np.load(R/f'阶段{name}.npy');eligible=mask&(f==old);f[eligible]=v[eligible];np.save(R/f'阶段{name}.npy',f)
folder=R/'蓝图/01a';folder.mkdir(exist_ok=True);ph=[]
for x in range(0,256,32):
 for y in range(0,96,32):
  for z in range(0,256,32):
   q=np.argwhere(mask[x:x+32,y:y+32,z:z+32])
   if not len(q):continue
   b=[[int(a),int(c),int(d),int(v[x+a,y+c,z+d])] for a,c,d in q];bp={'schema_version':1,'origin':{'x':x,'y':y+56,'z':z},'dimensions':{'x':32,'y':32,'z':32},'palette':P,'blocks':b}
   with gzip.open(folder/f'{x}-{y}-{z}.json.gz','wt',encoding='utf8') as f:json.dump(bp,f,separators=(',',':'))
   ph.append({'palette':P,'operations':[[x+a,y+c+56,z+d,x+a,y+c+56,z+d,p] for a,c,d,p in b]})
(R/'作业/01a.json').write_text(json.dumps({'world_path':'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V14-T05-森林圣所','phases':ph},separators=(',',':')),encoding='utf8');print(int(mask.sum()))
