"""实存近景后的局部修订：橘园外窗框透光开口、圆池绕行铺地。"""
from pathlib import Path
import json,gzip,numpy as np
R=Path(__file__).parent;s=json.loads((R/'场景.json').read_text(encoding='utf8'));P=s['palette'];old=np.load(R/'阶段03.npy');v=old.copy()
glass=P.index('minecraft:light_blue_stained_glass');quartz=P.index('minecraft:quartz_block');grass=P.index('minecraft:grass_block[snowy=false]');gravel=P.index('minecraft:gravel')
for x in range(30,58,6):v[x+1,67-56:72-56,130]=glass
for x in [40,46]:v[x,65-56:71-56,130]=quartz
v[40:47,70-56,130]=quartz
for x in range(95,130):
 for z in range(175,196):
  if ((x-112)/17)**2+((z-185)/10)**2<=1 and v[x,64-56,z]==grass:v[x,64-56,z]=gravel
np.save(R/'阶段03a.npy',v);mask=v!=old;folder=R/'蓝图/03a';folder.mkdir(parents=True,exist_ok=True);phases=[]
for x0 in [0,64,128]:
 q=np.argwhere(mask[x0:x0+64,:,:]);b=[[int(x),int(y),int(z-128),int(v[x0+x,y,z])] for x,y,z in q]
 if not b:continue
 bp={'schema_version':1,'origin':{'x':x0,'y':56,'z':128},'dimensions':{'x':64,'y':64,'z':80},'palette':P,'blocks':b}
 (folder/f'{x0}.json.gz').write_bytes(gzip.compress(json.dumps(bp,separators=(',',':')).encode(),mtime=0));phases.append({'palette':P,'operations':[[x+x0,y+56,z+128,x+x0,y+56,z+128,p] for x,y,z,p in b]})
(R/'作业/03a.json').write_text(json.dumps({'world_path':'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V15-T06-规则宫苑','phases':phases},separators=(',',':')),encoding='utf8');print(int(mask.sum()))
