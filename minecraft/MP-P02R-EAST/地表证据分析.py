"""只读取获准自然快照；材质族是显式解释表，不推断矿床、土层或产量。"""
from pathlib import Path
import sqlite3,json,hashlib,gzip,shutil
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[1];CACHE=ROOT.parents[3]/'MP-P02R-cache';SRC=REPO/'minecraft/建筑师/research/human-geography/southern-island/WB-002R-R1'
(ROOT/'evidence').mkdir(exist_ok=True)
def dump(n,v):(ROOT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
CACHE.mkdir(exist_ok=True)
db=CACHE/'observed.sqlite'
if not db.exists():
 with gzip.open(SRC/'raw-or-queryable/observed.sqlite.gz','rb') as inp,db.open('xb') as out:shutil.copyfileobj(inp,out)
assert hashlib.sha256(db.read_bytes()).hexdigest()=='01d115d6c686cc6d59772cfc68e1cbd50a5816045eeaa7f48fa8a4a8d4a791b7'
c=sqlite3.connect(db.as_uri()+'?mode=ro',uri=True)
B=[320,1456,2111,3263];W=1792;H=1808
a=np.array(c.execute('select exposed_y,exposed_state,artificial_material from samples where x between 320 and 2111 and z between 1456 and 3263 order by z,x').fetchall(),dtype=np.int32)
h=a[:,0].reshape(H,W);states=a[:,1].reshape(H,W);art=a[:,2].reshape(H,W)
names={i:json.loads(t)['Name'] for i,t in c.execute('select id,json from states')};p=np.load(SRC/'raw-or-queryable/derived.npz');sl=(slice(80,1888),slice(1120,2912));land=p['land_component'][sl];s=p['slope8'][sl];rel=p['relief32'][sl]
families={'SOIL_SURFACE':['grass_block','dirt','coarse_dirt','podzol','rooted_dirt','mycelium'], 'ROCK_SURFACE':['stone','granite','andesite','diorite','basalt','smooth_basalt','blackstone','deepslate','calcite','tuff','coal_ore','iron_ore','copper_ore','gold_ore','emerald_ore','deepslate_iron_ore','deepslate_coal_ore'], 'SAND_GRAVEL':['sand','red_sand','gravel'], 'TERRACOTTA_SURFACE':['terracotta','white_terracotta','light_gray_terracotta','orange_terracotta','brown_terracotta','red_terracotta','yellow_terracotta'], 'MUD_CLAY':['mud','packed_mud','clay'], 'SNOW_ICE':['snow','snow_block','ice','packed_ice','blue_ice'], 'SURFACE_PLANT':['moss_block','pale_moss_block','bush','short_grass','tall_grass','dandelion','fern','large_fern','poppy','dead_bush']}
classes=['NON_EAST_LAND','SOIL_SURFACE','ROCK_SURFACE','SAND_GRAVEL','TERRACOTTA_SURFACE','MUD_CLAY','SNOW_ICE','SURFACE_PLANT','OTHER_UNRESOLVED'];class_by_name={f'minecraft:{n}':classes.index(k) for k,v in families.items() for n in v}
lut=np.full(max(names)+1,8,dtype=np.uint8)
for i,n in names.items():lut[i]=class_by_name.get(n,8)
surface=lut[states];surface[land!=2]=0
v=np.array(c.execute('select x,z,leaf,trunk,dry_ground_vegetation,other_vegetation from vegetation where x between 320 and 2111 and z between 1456 and 3263 order by z,x').fetchall(),dtype=np.int32)
assert len(v)==(H//4)*(W//4)
veg=v[:,2:].reshape(H//4,W//4,4);np.savez_compressed(CACHE/'surface-natural.npz',height=h,land=land,slope=s,relief=rel,surface=surface,states=states,artificial=art,vegetation=veg)
dump('evidence/surface-legend.json',dict(classes=classes,explicit_mapping=families,unknown_policy='未明确列出的材质为OTHER_UNRESOLVED；人工标记独立保留，不按外观断言天然/人工。',substrate='UNRESOLVED：只有 exposed_state，不含向下土层剖面',vegetation='4格采样列是否有叶/木/其它植被，不伪装逐格冠幅或可持续产量',state_dictionary=names))
def profile(b):
 x0,z0,x1,z1=b;a=(slice(z0-1456,z1-1456+1),slice(x0-320,x1-320+1));m=land[a]==2;cnt=int(m.sum());surf=surface[a]
 vv=v[(v[:,0]>=x0)&(v[:,0]<=x1)&(v[:,1]>=z0)&(v[:,1]<=z1)];vv=vv[land[vv[:,1]-1456,vv[:,0]-320]==2]
 return dict(bounds=b,land_columns=cnt,elevation_percentiles=np.percentile(h[a][m],[10,50,90]).round(1).tolist(),gentle_columns=int((m&(s[a]<=.15)&(rel[a]<=10)).sum()),surface_counts={k:int(((surf==i)&m).sum()) for i,k in enumerate(classes) if i},surface_ratios={k:round(float(((surf==i)&m).sum()/cnt),4) for i,k in enumerate(classes) if i},vegetation_samples=len(vv),leaf_presence_ratio=round(float((vv[:,2]>0).mean()),4),any_vegetation_presence_ratio=round(float((vv[:,2:].sum(1)>0).mean()),4),artificial_flag_columns=int((art[a][m]>0).sum()),authority='DERIVED',source_refs=['SRC-OBS','SRC-DERIVED'],limitations=['土深/肥力/岩质/矿床/饮水未证','植被为采样占比','低坡地不等于可建地'])
# 地表比较先于选址；分片规则是空间分箱，不给人文角色评分。
tiles=[]
for z in range(1520,3025,192):
 for x in range(512,1921,192):
  b=[x,z,min(x+191,2111),min(z+191,3263)]
  if ((land[z-1456:b[3]-1456+1,x-320:b[2]-320+1]==2).sum())<10000:continue
  tiles.append(profile(b))
dump('evidence/surface-tiles.json',tiles)
dump('evidence/parent-search-profiles.json',{'north':profile([510,1540,990,2020]),'south':profile([1350,2510,1830,2990])})
palette=np.array([[125,173,194],[158,181,109],[153,148,141],[220,198,148],[185,130,100],[127,113,98],[222,234,238],[82,136,82],[186,143,188]],dtype=np.uint8)
base=Image.fromarray(palette[surface]).resize((896,904));im=Image.new('RGB',(1110,1030),'#f5f1e8');im.paste(base,(80,65));d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',18)
d.text((80,15),'MP-P02R · 地表材质证据（非地质/产量图）',font=font,fill='#29434a')
for x in range(400,2100,200):u=80+(x-320)/2;d.line((u,65,u,969),fill='#aab5a0');d.text((u,977),str(x),font=font,fill='black')
for z in range(1600,3264,200):vv=65+(z-1456)/2;d.line((80,vv,976,vv),fill='#aab5a0');d.text((5,vv),str(z),font=font,fill='black')
im.save(ROOT/'evidence/地表调查底图.png')
print('tiles',len(tiles));print(json.dumps([{'bounds':p['bounds'],'gentle':p['gentle_columns'],'soil':p['surface_ratios']['SOIL_SURFACE'],'rock':p['surface_ratios']['ROCK_SURFACE'],'terracotta':p['surface_ratios']['TERRACOTTA_SURFACE'],'leaf':p['leaf_presence_ratio'],'Y':p['elevation_percentiles']} for p in tiles],ensure_ascii=False))
c.close()
