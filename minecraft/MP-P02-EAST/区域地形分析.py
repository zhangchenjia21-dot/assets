"""区域自然证据白名单读取；计算地形候选与阻力，不授予场地语义。"""
from pathlib import Path
from collections import deque
import gzip,hashlib,json,shutil,sqlite3
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[1];CACHE=REPO.parents[1]/'MP-P02-cache'
SRC=REPO/'minecraft/建筑师/research/human-geography/southern-island/WB-002R-R1'
CACHE.mkdir(exist_ok=True);(ROOT/'evidence').mkdir(exist_ok=True)
def dump(n,v):(ROOT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
db=CACHE/'observed.sqlite'
if not db.exists():
 with gzip.open(SRC/'raw-or-queryable/observed.sqlite.gz','rb') as a,db.open('wb') as b:shutil.copyfileobj(a,b)
assert hashlib.sha256(db.read_bytes()).hexdigest()=='01d115d6c686cc6d59772cfc68e1cbd50a5816045eeaa7f48fa8a4a8d4a791b7'
conn=sqlite3.connect(db.as_uri()+'?mode=ro',uri=True)
# 自然图形分析覆盖东岛及西侧接驳接口，不定义政治界限。
B=[256,1440,2175,3263]; W=1920;H=1824
a=np.array(conn.execute('select exposed_y,water_y,artificial_material from samples where x between 256 and 2175 and z between 1440 and 3263 order by z,x').fetchall(),dtype=np.int32)
h=a[:,0].reshape(H,W);water=a[:,1].reshape(H,W);art=a[:,2].reshape(H,W)
p=np.load(SRC/'raw-or-queryable/derived.npz');sel=(slice(64,1888),slice(1056,2976))
l=p['land_component'][sel];s=p['slope8'][sel];r=p['relief32'][sel]
np.savez_compressed(CACHE/'regional-natural.npz',height=h,land=l,slope=s,relief=r,water_y=water,artificial=art)
# 8格聚合保留保守土地/低坡占比；不是识别村庄的评分器。
def mean8(a):return a.reshape(H//8,8,W//8,8).mean((1,3))
good=(l==2)&(s<=.20)&(r<=12)
mask=(mean8(good)>=.75)&(mean8(l==2)==1)
seen=np.zeros(mask.shape,bool);patches=[]
for zz,xx in zip(*np.where(mask)):
 zz,xx=int(zz),int(xx)
 if seen[zz,xx]:continue
 q=deque([(zz,xx)]);seen[zz,xx]=True;cells=[]
 while q:
  z,x=q.popleft();cells.append((z,x))
  for dz,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
   nz,nx=z+dz,x+dx
   if 0<=nz<mask.shape[0] and 0<=nx<mask.shape[1] and mask[nz,nx] and not seen[nz,nx]:seen[nz,nx]=True;q.append((nz,nx))
 if len(cells)<6:continue
 zs=[c[0] for c in cells];xs=[c[1] for c in cells];patches.append(dict(id='',coarse_area_blocks2=len(cells)*64,bounds=[256+min(xs)*8,1440+min(zs)*8,256+max(xs)*8+7,1440+max(zs)*8+7],representative_xz=[256+int(np.median(xs))*8+4,1440+int(np.median(zs))*8+4],cells=cells))
patches.sort(key=lambda p:-p['coarse_area_blocks2'])
for i,p in enumerate(patches):p['id']=f'TERRAIN-{i+1:03d}'
dump('evidence/terrain-patches.json',{'authority':'DERIVED','method':'8-block cells; >=75% columns slope8<=0.20 & relief32<=12; 100% east land; 4-connected; minimum6cells','not_buildable_area':True,'patches':patches})
summary=dict(bounds=B,authority='DERIVED',east_land_columns=int((l==2).sum()),artificial_flag_columns=int(((art>0)&(l==2)).sum()),artificial_flag_values=np.unique(art,return_counts=True)[0].tolist(),interpretation='材料标记不等于建筑识别；没有方块体积、道路或地籍观测。Fabric 保持 UNVERIFIED。',coarse_patch_count=len(patches),top_patch_areas=[x['coarse_area_blocks2'] for x in patches[:12]],terrain_thresholds_are_analysis_assumptions=True)
dump('evidence/regional-summary.json',summary)
t=np.clip((h-63)/237,0,1);rgb=np.stack([190-66*t,205-105*t,162-70*t],axis=-1)
gy,gx=np.gradient(h.astype(float));rgb=np.uint8(np.clip(rgb*np.clip(1+.03*(gx+gy),.65,1.12)[:,:,None],0,255));rgb[l!=2]=[123,166,184]
im=Image.fromarray(rgb).resize((960,912));canvas=Image.new('RGB',(1100,1040),'#f6f1e7');canvas.paste(im,(75,60));d=ImageDraw.Draw(canvas);font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',17)
for x in range(400,2176,200):u=75+(x-256)/2;d.line((u,60,u,972),fill='#d3d7ca');d.text((u,980),str(x),font=font,fill='black')
for z in range(1600,3264,200):v=60+(z-1440)/2;d.line((75,v,1035,v),fill='#d3d7ca');d.text((5,v),str(z),font=font,fill='black')
for p in patches[:45]:
 x,z=p['representative_xz'];u=75+(x-256)/2;v=60+(z-1440)/2;d.ellipse((u-3,v-3,u+3,v+3),fill='#b43a28');d.text((u+4,v),p['id'][-3:],font=font,fill='#942e22')
d.text((75,15),'MP-P02 自然地形口袋索引（仅派生，非聚落）',font=font,fill='black');canvas.save(ROOT/'evidence/地形口袋索引.png')
print(json.dumps(summary));print(json.dumps([{k:v for k,v in p.items() if k!='cells'} for p in patches[:35]]))
conn.close()
