"""继承实存基准，仅生成有原因的 Finishing 增量及逐笔保护账本。"""
from pathlib import Path
import json,numpy as np
R=Path(__file__).resolve().parent
pal=json.loads((R/'证据/00-Baseline-实存.json').read_text(encoding='utf8'))['palette'];ids={s:i for i,s in enumerate(pal)}
A=np.fromfile(R/'证据/00-Baseline.u16',dtype='<u2').reshape(56,144,144).copy();base=A.copy();ledger=[]
def pid(s):
 s=s if ':' in s else 'minecraft:'+s
 if s not in ids:ids[s]=len(pal);pal.append(s)
 return ids[s]
def p(x,y,z,s,reason,kind='Allowed'):
 assert y<24
 old=pal[A[y-10,z,x]];new=pal[pid(s)]
 assert 'water[' not in old and 'water[' not in new
 if old==new:return
 A[y-10,z,x]=pid(s);ledger.append(dict(x=x,y=y,z=z,before=old,after=new,reason=reason,permission=kind))
def add(x,y,z,s,reason):
 assert pal[A[y-10,z,x]]=='minecraft:air',(x,y,z,pal[A[y-10,z,x]])
 p(x,y,z,s,reason)
def surface(x,y,z,s,reason,kind='Allowed'):
 assert pal[A[y-10,z,x]] not in ['minecraft:air','minecraft:water[level=0]']
 p(x,y,z,s,reason,kind)
def export(name,prev,start):
 d=R/'蓝图'/name;d.mkdir(parents=True,exist_ok=True);files=[]
 for y in range(0,56,14):
  for z in range(0,144,24):
   for x in range(0,144,24):
    a=A[y:y+14,z:z+24,x:x+24];b=prev[y:y+14,z:z+24,x:x+24];yy,zz,xx=np.where(a!=b)
    if not len(xx):continue
    used=sorted(set(map(int,a[yy,zz,xx])));remap={v:i for i,v in enumerate(used)}
    bp={'schema_version':1,'origin':dict(x=x,y=y+10,z=z),'dimensions':dict(x=a.shape[2],y=a.shape[0],z=a.shape[1]),'palette':[pal[i] for i in used],'blocks':[[int(i),int(j),int(k),remap[int(v)]] for i,j,k,v in zip(xx,yy,zz,a[yy,zz,xx])],'metadata':{'name':'T10 '+name,'source_kind':'AI_ORIGINAL','content_omissions':['Containers use verified empty native base state; no inventory NBT']}}
    f=f'{x}-{y+10}-{z}.json';(d/f).write_text(json.dumps(bp,separators=(',',':')),encoding='utf8');files.append(f)
 (d/'清单.json').write_text(json.dumps({'files':files,'changed':int((A!=prev).sum())}),encoding='utf8');np.savez_compressed(R/(name+'.npz'),blocks=A,palette=pal)
 (R/f'证据/{name}-修改账本.json').write_text(json.dumps(ledger[start:],ensure_ascii=False,indent=2),encoding='utf8');print(name,int((A!=prev).sum()))
prev=A.copy();start=len(ledger)
# 更衣储物依公共重复使用成立；分开的原生箱体可开盖、可使用。
for x in [64,67,70,73,90,93,96,99]:add(x,19,29,'chest[facing=south,type=single,waterlogged=false]','更衣保管：面向座席，箱盖上方保留空气')
for x in range(86,90):add(x,19,33,'stripped_oak_log[axis=y]','入口侧管理台，不占两条冷厅分流线')
add(89,20,33,'candle[candles=2,lit=true,waterlogged=false]','管理台任务灯，保留北窗自然光')
for x in [90,91]:add(x,21,102,'cut_sandstone','热浴后整理用品台，贴活动边缘不围池')
for x in [90,91]:add(x,22,102,'flower_pot','浴后油膏小器皿的方块转译，不声称有液体库存')
for x in range(119,123):add(x,17,98,'stripped_oak_log[axis=y]','燃料院劈分和整理工作台')
for x in [119,122]:add(x,18,98,'barrel[facing=up,open=false]','服务用品储存，位于可接近工作台端部')
add(120,18,98,'candle[candles=1,lit=true,waterlogged=false]','工作台任务照明，与既有燃料堆分离')
export('01-Functional',prev,start);prev=A.copy();start=len(ledger)
# 保持门洞几何，仅使既有砌体边界在近景可读。
for x in [78,86]:
 for y in range(19,23):
  for z in [26,27]:surface(x,y,z,'cut_sandstone','主入口既有实心门侧的石材收口')
for x in range(76,89):
 for z in range(58,65):
  if x in [76,88] or z in [58,64]:surface(x,18,z,'black_terracotta','冷厅平整地坪镶边，强调停留中心而不构成隔断')
for x,z in [(80,60),(81,61),(82,62),(83,61),(84,60),(82,60)]:surface(x,18,z,'black_terracotta','冷厅中央小尺度几何嵌饰')
# 湿区近身墙面形成可擦洗下墙与细窄压顶，保留上部鼓座和窗带安静。
for x in range(65,100):
 for z in range(93,124):
  if not (13.5<=((x-82)**2+(z-108)**2)**.5<=15):continue
  for y in [21,22,23]:
   if pal[A[y-10,z,x]]=='minecraft:bricks' and any(pal[A[y-10,z+dz,x+dx]]=='minecraft:air' for dx,dz in [(1,0),(-1,0),(0,1),(0,-1)]):
    surface(x,y,z,'smooth_quartz' if y==21 else ('white_terracotta' if y==22 else 'cut_sandstone'),'热室内侧可擦洗墙脚与压顶，仅换既有表面材料')
export('02-Architectural',prev,start);prev=A.copy();start=len(ledger)
for x in range(106,111):
 for y in range(19,22):
  if y<21 or x in [107,108,109]:surface(x,y,105,'polished_blackstone' if y<21 else 'gray_terracotta','炉口上方烟熏，由烟源向上减弱')
for x,z in [(80,29),(81,30),(82,31),(83,32),(84,31),(80,32)]:surface(x,18,z,'sandstone','入场脚步集中区域磨损；保持地坪标高')
for x in [135,136]:
 for z in range(114,119):surface(x,15,z,'coarse_dirt','服务院外少量踩踏地面，不改变地形或路线','Restricted')
export('03-Material',prev,start);prev=A.copy();start=len(ledger)
for x,z,y in [(64,60,20),(100,60,20),(71,83,22),(93,83,22)]:
 p(x,y,z,'candle[candles=3,lit=true,waterlogged=false]','冷暖休息边照明转为低位灯群，避免固定节距火把感')
export('04-Composition',prev,start)
# 近景复核后删减：双器皿与双桶抢占工作面，中央小纹样分散视线。
prev=A.copy();start=len(ledger)
p(91,22,102,'air','Restraint：删除重复油膏器皿，释放用品台面')
p(122,18,98,'air','Restraint：删除工作台端部重复储桶，保留整理工作面')
for x,z in [(80,60),(81,61),(82,62),(83,61),(84,60),(82,60)]:p(x,18,z,pal[base[8,z,x]],'Restraint：取消中央零散嵌饰，只保留外围边线与冷厅留白')
export('05-Restraint',prev,start)
