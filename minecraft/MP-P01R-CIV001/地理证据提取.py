"""仅从白名单自然数据生成本轮地理底图与查询缓存，不访问存档或其它规划。"""
from pathlib import Path
import gzip, hashlib, json, shutil, sqlite3
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
SRC=REPO/'minecraft/建筑师/research/human-geography/southern-island/WB-002R-R1'
CACHE=REPO.parents[1]/'MP-P01R-cache'
CACHE.mkdir(exist_ok=True)
(ROOT/'evidence').mkdir(exist_ok=True)
def dump(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
db=CACHE/'observed.sqlite'
if not db.exists():
    with gzip.open(SRC/'raw-or-queryable/observed.sqlite.gz','rb') as s,db.open('wb') as t: shutil.copyfileobj(s,t)
assert sha(db)=='01d115d6c686cc6d59772cfc68e1cbd50a5816045eeaa7f48fa8a4a8d4a791b7'
con=sqlite3.connect(db.as_uri()+'?mode=ro',uri=True)
arr=np.array(con.execute('select x,z,exposed_y,water_y from samples order by z,x').fetchall(),dtype=np.int32)
height=arr[:,2].reshape(2112,3264)
npz=np.load(SRC/'raw-or-queryable/derived.npz')
land=npz['land_component']; slope=npz['slope8']; relief=npz['relief32']
np.savez_compressed(CACHE/'natural.npz',height=height,land=land,slope=slope,relief=relief)
atlas=[]
for line in (REPO/'minecraft/建筑师/research/natural-geography/NG-3/atlas/objects.jsonl').open(encoding='utf-8'):
    o=json.loads(line)
    if o['family'] not in ['NGEO','NHYD']: continue
    b=o['geometry']['bounds']
    if b[2]>=-800 and b[0]<=2463 and b[3]>=1376 and b[1]<=3487: atlas.append(o)
dump(ROOT/'evidence/atlas-natural-subset.json',atlas)
print('ATLAS',[(o['id'],o.get('type'),o['geometry']['bounds'],o.get('summary')) for o in atlas])
print('SHAPES',height.shape,land.shape)
stats=[]
for cid in (1,2):
    m=land==cid
    stats.append(dict(component=cid,area=int(m.sum()),height_percentiles=np.percentile(height[m],[0,10,50,90,100]).tolist(),low_slope_columns=int((m&(slope<=.125)).sum())))
dump(ROOT/'evidence/natural-summary.json',stats)
# 色阶表达地面高程；水域独立着色，不把林冠当成建筑。
t=np.clip((height-63)/237,0,1)
color=np.zeros((*height.shape,3),dtype=np.uint8)
for c,(low,high) in enumerate(zip((188,204,157),(121,100,92))): color[:,:,c]=(low+(high-low)*t)
gy,gx=np.gradient(height.astype(float)); shade=np.clip(1+(gx+gy)*.024,.65,1.13)
color=np.uint8(np.clip(color*shade[:,:,None],0,255)); color[land==0]=(128,171,189)
im=Image.fromarray(color).resize((1632,1056))
canvas=Image.new('RGB',(1772,1210),'#f5f1e6');canvas.paste(im,(80,70));d=ImageDraw.Draw(canvas)
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',20)
d.text((80,15),'MP-P01R 原始自然底图｜X 向右，Z 向下；北 = -Z',font=font,fill='black')
for x in range(-800,2464,400):
    u=80+(x+800)/2;d.line((u,70,u,1126),fill='#d9ddd0',width=1);d.text((u,1135),str(x),font=font,fill='black')
for z in range(1400,3488,400):
    v=70+(z-1376)/2;d.line((80,v,1712,v),fill='#d9ddd0');d.text((5,v),str(z),font=font,fill='black')
canvas.save(ROOT/'evidence/自然底图.png')
con.close()
