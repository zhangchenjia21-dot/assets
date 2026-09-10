"""针对本轮观察修订门楼上层入口和院内踩踏地表，保持其余建筑包络。"""
from pathlib import Path
import json,gzip,numpy as np,math
R=Path(__file__).parent;s=json.loads((R/'场景.json').read_text(encoding='utf8'));P=s['palette'];old=np.load(R/'阶段02.npy');v=old.copy()
def m(n):return P.index('minecraft:'+n)
def box(x,y,z,X,Y,Z,p):v[x:X+1,y-56:Y-55,z:Z+1]=p
brick=m('stone_bricks');wood=m('spruce_planks');gravel=m('gravel');coarse=m('coarse_dirt')
# 门楼北侧设院内上楼梯，出口接二层画廊；另一短梯继续上门楼屋顶。
for i in range(8):
 x,z,y=128,169-i,109+i
 box(x,109,z,x+1,y,z,brick);box(x,y,z,x+1,y,z,m('stone_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]'));box(x,y+1,z,x+1,y+3,z,0)
box(128,116,161,130,116,172,wood);box(128,117,161,130,119,172,0)
box(129,116,172,139,116,175,wood);box(129,117,172,139,119,175,0)
for i in range(8):
 x,z,y=128,169-i,109+i
 box(x,109,z,x+1,y,z,brick);box(x,y,z,x+1,y,z,m('stone_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]'));box(x,y+1,z,x+1,y+3,z,0)
# 画廊下木柱和梁属于有意支承，不填实外院。
for z in [162,167,171]:box(130,109,z,130,115,z,m('oak_log[axis=y]'))
box(134,116,170,139,116,171,wood)
for i in range(4):
 y,z=117+i,171+i;box(138,116,z,139,y,z,brick);box(138,y,z,139,y,z,m('stone_brick_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]'));box(138,y+1,z,139,y+3,z,0)
# 连续的砾石院面；踩踏土集中在马厩口、厨房口，不保留棋盘格。
for x in range(104,169):
 for z in range(75,178):
  for y in [108,111]:
   if v[x,y-56,z] in [gravel,coarse] and v[x,y+1-56,z]==0:
    service=(y==108 and ((x-124)**2/55+(z-157)**2/100<1 or (x-146)**2/32+(z-157)**2/45<1))
    v[x,y-56,z]=coarse if service else gravel
s['targets'] += [['外门楼画廊',134,117,175],['外门楼顶',138,121,177]]
mask=v!=old;np.save(R/'阶段02a.npy',v);future=np.load(R/'阶段03.npy');future[mask]=v[mask];np.save(R/'阶段03.npy',future)
(R/'场景.json').write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding='utf8')
folder=R/'蓝图/02a';folder.mkdir(exist_ok=True);ph=[];count=0
for x in range(0,256,32):
 for y in range(0,128,32):
  for z in range(0,256,32):
   q=np.argwhere(mask[x:x+32,y:y+32,z:z+32])
   if not len(q):continue
   b=[[int(a),int(c),int(d),int(v[x+a,y+c,z+d])] for a,c,d in q];count+=len(b)
   bp={'schema_version':1,'origin':{'x':x,'y':y+56,'z':z},'dimensions':{'x':32,'y':32,'z':32},'palette':P,'blocks':b}
   with gzip.open(folder/f'{x}-{y}-{z}.json.gz','wt',encoding='utf8') as f:json.dump(bp,f,separators=(',',':'))
   ph.append({'palette':P,'operations':[[x+a,y+c+56,z+d,x+a,y+c+56,z+d,p] for a,c,d,p in b]})
(R/'作业/02a.json').write_text(json.dumps({'world_path':'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V13-T04-山脊城堡','phases':ph},separators=(',',':')),encoding='utf8');print(count)
