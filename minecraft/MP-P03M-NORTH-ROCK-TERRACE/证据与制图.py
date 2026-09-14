"""只读允许清单中的事实，生成本轮统计和坐标图；不包含世界施工接口。

首次运行压缩保存已有逐列事实；后续可仅凭归档重建地图。
规划判断在 assessment-data.json 中人工表达，统计不自动裁决选址。
"""
from pathlib import Path
import json, hashlib, gzip, subprocess, datetime
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
MC = ROOT.parent
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
for folder in ['sources','evidence','maps']: (ROOT/folder).mkdir(exist_ok=True)
raw_path=ROOT/'evidence/surface.json.gz'
if not raw_path.exists():
    raw=Path('D:/Games/Minecraft/AI工程/MP-P03-cache/surface.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()=='d11f036d8baac7fabcfa7c4ed9ba804dd4862f55fc3d1ec2ce25cec68d6eb7f2'
    raw_path.write_bytes(gzip.compress(raw,mtime=0))
raw=gzip.decompress(raw_path.read_bytes())
assert hashlib.sha256(raw).hexdigest()=='d11f036d8baac7fabcfa7c4ed9ba804dd4862f55fc3d1ec2ce25cec68d6eb7f2'
data=json.loads(raw)
if not (ROOT/'sources/input-register.json').exists():
    revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=MC.parent,text=True).strip()
    sources=[]
    def register(rel,authority,use):
        p=MC/rel
        sources.append(dict(path=rel,sha256=sha(p),revision=revision,authority=authority,use=use))
    canon='建筑师/world/civilizations/CIV-001/README.md'
    register(canon,'APPROVED_CANON','文明身份、生产互补、地方自治、技术；不追读后续设计链接')
    (ROOT/'sources/Canon入口.md').write_bytes((MC/canon).read_bytes())
    pp='MP-P02R-EAST/implementation-packages.json'
    register(pp,'DESIGN_PROPOSAL','仅摘录 PACKAGE-01；不升级 Canon')
    write(ROOT/'sources/parent-package.json',next(p for p in read(MC/pp) if p['id']=='PACKAGE-01'))
    pr='MP-P02R-EAST/planning-data.json'
    register(pr,'DESIGN_PROPOSAL','仅 ROUTE-01/02，保留关系及上游调查证据，不当已建道路')
    write(ROOT/'sources/parent-routes.json',[p for p in read(MC/pr)['routes'] if p['id'] in ['ROUTE-01','ROUTE-02']])
    for name in ['world-read-provenance','current-surface-summary','shallow-void-columns','fabric-witnesses']:
        rel=f'MP-P03-NORTH-ROCK-TERRACE/evidence/{name}.json'
        register(rel,'OBSERVED / DERIVED','仅事实字段；忽略原文件中任何规划倾向语句')
        d=read(MC/rel)
        if name=='current-surface-summary': d={k:d[k] for k in ['core','context','classes','classification_note']}
        if name=='shallow-void-columns': d={k:d[k] for k in ['bounds','depth','columns_checked','void_columns','authority','origin']}
        if name=='world-read-provenance': d={k:v for k,v in d.items() if k!='block_entities'}
        write(ROOT/f'evidence/{name}.json',d)
    register('MP-P03-NORTH-ROCK-TERRACE/sources/source-register.json','PROVENANCE','只追溯事实调查；不采用旧 Skill 或方案')
    for name in ['现场地形.png','现场地表.png']:
        register(f'MP-P03-NORTH-ROCK-TERRACE/evidence/{name}','DERIVED','仅地理底图；本轮重新制图')
    skillrev=(ROOT/'sources/skill-revision.txt').read_text().strip()
    for p in sorted((ROOT/'sources/skill').rglob('*.md')):
        sources.append(dict(path='skill/codex/minecraft-planner/'+p.relative_to(ROOT/'sources/skill').as_posix(),sha256=sha(p),revision=skillrev,authority='SKILL_INSTRUCTION',local_copy=p.relative_to(ROOT).as_posix()))
    write(ROOT/'sources/input-register.json',sources)
void=read(ROOT/'evidence/shallow-void-columns.json')
cols=np.array([[v if v is not None else -999 for v in r] for r in data['columns']],dtype=np.int64)
assert len(cols)==92160 and data['missing_columns']==0
x0,z0,x1,z1=data['bounds']; shape=(z1-z0+1,x1-x0+1)
def raster(i):
    a=np.zeros(shape,dtype=np.int64);a[cols[:,1]-z0,cols[:,0]-x0]=cols[:,i];return a
h=raster(3);water=raster(5);state=raster(4)
palette=data['palette']
def classify(s):
    s=s.split('[')[0].split(':')[-1]
    if s=='lava':return 4
    if s in ['grass_block','dirt','coarse_dirt','podzol','rooted_dirt','mycelium','farmland']:return 1
    if s in ['sand','red_sand','gravel']:return 2
    if s in ['stone','granite','diorite','andesite','tuff','deepslate','calcite','basalt','smooth_basalt'] or s.endswith('_ore'):return 0
    return 5
s=np.array([classify(v) for v in palette])[state]; s[water!=-999]=3
names=['ROCK','SOIL','SAND_GRAVEL','WATER','LAVA','OTHER']
def stats(b):
    x,z,X,Z=b;a=h[z-z0:Z-z0+1,x-x0:X-x0+1];c=s[z-z0:Z-z0+1,x-x0:X-x0+1]
    return dict(bounds=b,columns=int(a.size),ground_y_percentiles_0_10_50_90_100=np.percentile(a,[0,10,50,90,100]).tolist(),surface_counts={n:int((c==i).sum()) for i,n in enumerate(names)},observed_void_columns=sum(x<=v['x']<=X and z<=v['z']<=Z for v in void['void_columns']))
stats_all={'parent_search':stats([704,1520,895,1711]),'A':stats([752,1596,824,1672]),'B':stats([825,1596,884,1672])}
assert stats_all['parent_search']['surface_counts']==read(ROOT/'evidence/current-surface-summary.json')['core']['surface_counts']
write(ROOT/'evidence/independent-statistics.json',dict(authority='DERIVED',method='逐列事实重新分类；分窗为本轮调查提案，不是建成区；空气只在既有16格深扫描范围计数',windows=stats_all,void_scan_columns=void['columns_checked'],void_columns=len(void['void_columns'])))
# 同坐标平面与剖面：不生成路线可行性分数，也不把调查框算为建成面积。
font_path='C:/Windows/Fonts/msyh.ttc'
def font(n):return ImageFont.truetype(font_path,n)
W,H=1680,1240; scale=3; ox,oz=100,110
def pos(x,z):return (ox+(x-x0)*scale,oz+(z-z0)*scale)
colors=np.array([[166,167,162],[118,159,92],[207,184,132],[74,153,184],[236,78,28],[153,120,153]])
rgb=colors[s].astype(float)
dz,dx=np.gradient(h.astype(float));shade=np.clip(.93+.045*(-dx-dz),.6,1.15)
rgb=np.clip(rgb*shade[:,:,None],0,255).astype('uint8')
im=Image.new('RGB',(W,H),'#f4f1e8');im.paste(Image.fromarray(rgb).resize((960,864),Image.Resampling.NEAREST),(ox,oz));d=ImageDraw.Draw(im)
d.text((70,24),'MP-P03M｜北岩台：保留长期可能，分阶段兑现容量',font=font(30),fill='#203b43')
d.text((70,68),'SETTLEMENT · v0.4 · 事实快照 2026-09-13 · ↑北 −Z / 东 +X',font=font(20),fill='#42565a')
for x in range(640,960,32):
    px,_=pos(x,z0);d.line((px,oz,px,oz+864),fill='#d3d6ce');d.text((px-18,oz+872),str(x),font=font(16),fill='black')
for z in range(1488,1776,32):
    _,pz=pos(x0,z);d.line((ox,pz,ox+960,pz),fill='#d3d6ce');d.text((43,pz-10),str(z),font=font(16),fill='black')
def box(b,color,width=3):
    x,z,X,Z=b;d.rectangle((*pos(x,z),*pos(X+1,Z+1)),outline=color,width=width)
box([704,1520,895,1711],'#6b345a')
box(void['bounds'],'#734da6',1)
for v in void['void_columns']:
    px,pz=pos(v['x'],v['z']);d.rectangle((px,pz,px+2,pz+2),fill='#aa157c')
box([752,1596,824,1672],'#f5f0cf',5);box([825,1596,884,1672],'#edb149',5)
for label,x,z in [('A',775,1610),('B',860,1610)]:
    px,pz=pos(x,z);d.ellipse((px-20,pz-20,px+20,pz+20),fill='#203b43');d.text((px-10,pz-17),label,font=font(25),fill='white')
for z in range(1490,1770,5):
    px,pz=pos(840,z);d.line((px,pz,px,pz+6),fill='#253744',width=2)
for points in [[(650,1620),(720,1620),(770,1620)],[(685,1770),(730,1705),(770,1645)]]:
    # 虚线仅表达应调查的来向，不声称沿线可通行。
    for p,q in zip(points,points[1:]):
        for t in np.arange(0,1,.14):
            a=(p[0]+(q[0]-p[0])*t,p[1]+(q[1]-p[1])*t);u=min(t+.07,1);b=(p[0]+(q[0]-p[0])*u,p[1]+(q[1]-p[1])*u)
            d.line((*pos(*a),*pos(*b)),fill='#763212',width=4)
panel=[('事实 / 推导底图',24),('灰 岩面   绿 土面   黄 砂砾',18),('蓝 可见水   橙 熔岩   紫 其它',18),('洋红点：地面下16格内观测空气',18),('细紫框：空洞扫描范围，区外未知',18),('',10),('本轮提案 / 非施工边界',24),('紫红外框：父案搜索窗',18),('白框 A：优先调查西中部岩台',18),('金框 B：后续东侧调查窗',18),('A / B 均非已确认建设用地',18),('棕虚线：中域、西南来向待查',18),('黑虚线：另图剖面 X=840',18),('',10),('容量：条件范围，非实测人口',24),('首段 12–16户 / 3,500–5,000格²',18),('扩展累计12–24户 / 3,500–8,000格²',18),('不把A、B框面积相加当容量',18),('',10),('实际空间后果',24),('货运先接西侧，生活围绕供水接口',18),('东侧先查浅空洞与松散表面',18),('北崖不默认港口；南水不默认饮水',18),('保留土面；不全台填平或填洞',18)]
y=110
for text,size in panel:d.text((1090,y),text,font=font(size),fill='#203b43');y+=size+12
d.line((100,1030,250,1030),fill='#203b43',width=5);d.text((100,1040),'50 blocks',font=font(18),fill='#203b43')
d.text((100,1090),'关系腹地延伸至图外中域与地方共同体；没有按半径划定。',font=font(21),fill='#203b43')
d.text((100,1126),'水质、水量、通行权、驮畜净空、稳定性均未由这张图证明。',font=font(21),fill='#203b43')
d.text((100,1162),'底图：surface.json.gz；本轮没有进入游戏、启动服务器或写世界。',font=font(19),fill='#203b43')
im.save(ROOT/'maps/约束与分阶段空间.png')
im=Image.new('RGB',(1480,910),'#f4f1e8');d=ImageDraw.Draw(im)
d.text((65,25),'MP-P03M｜实测地形剖面：取水与浅层地基不是同一问题',font=font(29),fill='#203b43')
profiles=[]
for index,(axis,fixed,start,end) in enumerate([('Z',840,1488,1775),('X',1620,640,895)]):
    left,top,bottom=90,120+index*365,375+index*365
    points=[];rows=[]
    for v in range(start,end+1):
        x,z=(fixed,v) if axis=='Z' else (v,fixed)
        y=int(h[z-z0,x-x0]);wy=int(water[z-z0,x-x0]);px=left+(v-start)*3;py=bottom-(y-30)*1.65;points.append((px,py));rows.append([x,z,y,None if wy==-999 else wy])
        if wy!=-999:d.ellipse((px-2,bottom-(wy-30)*1.65-2,px+2,bottom-(wy-30)*1.65+2),fill='#238db5')
        for a in void['void_columns']:
            if a['x']==x and a['z']==z:
                for yy in a['void_y']:d.point((px,bottom-(yy-30)*1.65),fill='#b71785')
    d.line(points,fill='#394945',width=3)
    for y in [60,100,140]:
        py=bottom-(y-30)*1.65;d.text((40,py-8),str(y),font=font(17),fill='#394945')
    for v in range(start,end+1,32):d.text((left+(v-start)*3-16,bottom+8),str(v),font=font(16),fill='#394945')
    d.text((70,top-32),f'{axis}方向剖面；固定 '+('X=' if axis=='Z' else 'Z=')+str(fixed),font=font(22),fill='#394945')
    profiles.append(dict(axis=axis,fixed=fixed,fields=['x','z','ground_y','water_y'],samples=rows))
d.text((1030,150),'蓝：观测水面高度',font=font(20),fill='#238db5');d.text((1030,190),'洋红：已查浅层空气',font=font(20),fill='#b71785')
for i,t in enumerate(['北侧低水面与台顶有明显高差。','高处蓄水可缓冲搬运，但不产水。','打井需证实含水与普通开凿负担。','南部水点同样需要查水质、供给。','水平3px/格；垂直1.65px/格。','这是诊断切线，不是道路设计。']):d.text((990,260+i*40),t,font=font(18),fill='#394945')
d.text((80,827),'X/Z 为实际 Minecraft 坐标，Y 为逐列地面；水、空气不推断水文或结构稳定。',font=font(21),fill='#394945')
im.save(ROOT/'maps/地形与浅层剖面.png');write(ROOT/'evidence/section-samples.json',profiles)
print(json.dumps(stats_all,ensure_ascii=False))
