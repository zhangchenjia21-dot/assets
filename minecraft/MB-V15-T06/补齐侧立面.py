"""第二阶段近景发现侧立面缺少开窗节奏；仅修改登记墙面并保留入口。"""
from pathlib import Path
import json,gzip,numpy as np
R=Path(__file__).parent;s=json.loads((R/'场景.json').read_text(encoding='utf8'));P=s['palette'];old=np.load(R/'阶段02.npy');v=old.copy()
def box(x,y,z,X,Y,Z,p):v[x:X+1,y-56:Y-55,z:Z+1]=P.index('minecraft:'+p)
for x in [60,164]:
 for z in [47,54,61]:
  for y in [71,80]:
   box(x,y-1,z-1,x,y+4,z+2,'chiseled_sandstone');box(x,y,z,x,y+3,z+1,'light_blue_stained_glass')
 for z in [20,28,36]:box(x,70,z-1,x,76,z+2,'chiseled_sandstone');box(x,71,z,x,75,z+1,'light_blue_stained_glass')
 for y in [69,84]:box(x,y,42,x,y,68,'quartz_block')
mask=v!=old;np.save(R/'阶段02a.npy',v);future=np.load(R/'阶段03.npy');eligible=mask&(future==old);future[eligible]=v[eligible];np.save(R/'阶段03.npy',future)
folder=R/'蓝图/02a';folder.mkdir(parents=True,exist_ok=True);phases=[]
for x in [60,164]:
 q=np.argwhere(mask[x:x+1,:,:]);b=[[0,int(y),int(z),int(v[x,y,z])] for _,y,z in q];bp={'schema_version':1,'origin':{'x':x,'y':56,'z':0},'dimensions':{'x':1,'y':64,'z':96},'palette':P,'blocks':b}
 (folder/f'{x}.json.gz').write_bytes(gzip.compress(json.dumps(bp,separators=(',',':')).encode(),mtime=0));phases.append({'palette':P,'operations':[[x,y+56,z,x,y+56,z,p] for _,y,z,p in b]})
(R/'作业/02a.json').write_text(json.dumps({'world_path':'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V15-T06-规则宫苑','phases':phases},separators=(',',':')),encoding='utf8')
print(int(mask.sum()))
