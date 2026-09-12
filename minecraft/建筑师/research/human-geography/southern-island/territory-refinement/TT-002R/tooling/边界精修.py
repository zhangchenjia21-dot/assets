"""研究外围：只读已接受缓存，输出 Owner prior 的有限地形精修草稿；无世界接口。"""
import json, hashlib, shutil, sqlite3
from pathlib import Path
from collections import deque
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT=Path(__file__).resolve().parents[1]
ROOT=OUT.parents[4]
CACHE=Path('D:/Games/Minecraft/AI工程/研究缓存/建筑师/TT-002R')
STATUS='REFINED_DRAFT / AWAITING GPT + OWNER ACCEPTANCE'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        while b:=f.read(1048576): h.update(b)
    return h.hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def write(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
def edges(a):
    # 坐标表示真实 block-corner 边，不用格心折线代替边界。
    v=((a[:,:-1]==2)&(a[:,1:]==3))|((a[:,:-1]==3)&(a[:,1:]==2))
    z,x=np.where(v);vertical=np.column_stack((x-799,z+1376,x-799,z+1377))
    v=((a[:-1]==2)&(a[1:]==3))|((a[:-1]==3)&(a[1:]==2))
    z,x=np.where(v);horizontal=np.column_stack((x-800,z+1377,x-799,z+1377))
    return np.concatenate((vertical,horizontal)).astype(int)
def components_edges(es):
    nodes={}
    for i,e in enumerate(es):
        for p in (tuple(e[:2]),tuple(e[2:])):nodes.setdefault(p,[]).append(i)
    seen=set();parts=[]
    for i in range(len(es)):
        if i in seen:continue
        q=[i];seen.add(i);part=[]
        while q:
            j=q.pop();part.append(j)
            for p in (tuple(es[j,:2]),tuple(es[j,2:])):
                for k in nodes[p]:
                    if k not in seen:seen.add(k);q.append(k)
        parts.append(part)
    return sorted(parts,key=len,reverse=True)
def distance(points,segments):
    # 精确欧氏点到闭单位边距离；分批计算避免输出全域 dense 距离图。
    result=[];lo=np.minimum(segments[:,:2],segments[:,2:]);hi=np.maximum(segments[:,:2],segments[:,2:])
    for start in range(0,len(points),512):
        p=np.asarray(points[start:start+512])[:,None,:]
        d=np.maximum(np.maximum(lo-p,p-hi),0)
        result.extend(np.sqrt((d*d).sum(axis=2).min(axis=1)).tolist())
    return np.array(result)
def describe(v):
    v=np.asarray(v);v=v[np.isfinite(v)]
    return {'n':int(len(v)),'mean':float(v.mean()) if len(v) else 0,'median':float(np.median(v)) if len(v) else 0,'p90':float(np.percentile(v,90)) if len(v) else 0,'max':float(v.max()) if len(v) else 0}
def topology(a,c):
    # 独立四邻接遍历保留天然离岛；没有自动删除小片的后处理。
    mask=a==c;seen=np.zeros(mask.shape,bool);parts=[];h,w=a.shape
    for z,x in zip(*np.where(mask)):
        if seen[z,x]:continue
        seen[z,x]=True;q=deque([(int(z),int(x))]);n=0;shore=False;neighbors=set()
        while q:
            zz,xx=q.popleft();n+=1
            for dz,dx in ((0,1),(0,-1),(1,0),(-1,0)):
                nz,nx=zz+dz,xx+dx
                if not(0<=nz<h and 0<=nx<w):shore=True;continue
                v=a[nz,nx]
                if v==255:shore=True
                elif v!=c:neighbors.add(int(v))
                elif not seen[nz,nx]:seen[nz,nx]=True;q.append((nz,nx))
        parts.append({'area':n,'seed':[int(x)-800,int(z)+1376],'enclave':not shore and len(neighbors)==1})
    return sorted(parts,key=lambda p:-p['area'])

for d in ('visual','reports','validation'): (OUT/d).mkdir(exist_ok=True)
source=OUT/'input/owner-draft-rev153.json';doc=read(source)
assert sha(source)=='4fce4c14295ba3f5dd760e31b8a1e3f63fe139002c9eb427ff8d4648a6aef2e6'
assert doc['schema']=='civ-territories/1' and doc['revision']==153
assert doc['source']['id']=='94fc4687358a9fd5dd542997538822bfdba7b83bd76c4825fd84bd0116ea3d21'
assert doc['source']['bounds']==[-800,1376,2463,3487]
resolved=[]
for ref in doc['source']['references']:
    p=ROOT/ref['path']
    if not p.exists():
        # 附件的 D-020 路径文字损坏；只按已知同一决策文件和确切 hash 核对，不猜源。
        assert ref['path'].startswith('decisions/D-020_')
        matches=list((ROOT/'decisions').glob('D-020_*.md'));assert len(matches)==1;p=matches[0]
    assert sha(p)==ref['sha256'] and p.stat().st_size==ref['bytes']
    resolved.append({'provided_path':ref['path'],'resolved_path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)})
a=np.full((2112,3264),255,np.uint8)
for z,x0,x1,c in doc['runs']:
    assert all(isinstance(t,int) for t in (z,x0,x1,c)) and 0<=c<6 and 1376<=z<=3487 and -800<=x0<=x1<=2463
    assert (a[z-1376,x0+800:x1+801]==255).all();a[z-1376,x0+800:x1+801]=c
assert [int((a==i).sum()) for i in range(6)]==[92124,575397,395144,1194016,0,0]
r1=ROOT/'research/human-geography/southern-island/WB-002R-R1/raw-or-queryable'
f=np.load(r1/'derived.npz');assert np.array_equal(a!=255,f['land_component']>0)
db=sqlite3.connect((r1/'observed.sqlite').as_uri()+'?mode=ro',uri=True)
y=np.asarray(db.execute('SELECT exposed_y FROM samples ORDER BY z,x').fetchall(),np.int16).reshape(a.shape);db.close()
slope=f['slope8'];relief=f['relief32'];oldedges=edges(a);parts=components_edges(oldedges);main=oldedges[parts[0]]
refined=a.copy();rows=[]
# 模型先选择内谷东缘这一连续地貌段；程序仅在该段内寻找可复核的坡折。
# 其他地段证据不足，保持 Owner 原线；不按全域分数重新分配。
for z in range(1895,2091):
    zz=z-1376
    v=main[(main[:,1]==z)&(main[:,3]==z+1)]
    if len(v)!=1:continue
    oldx=int(v[0,0]);x=oldx+800
    assert a[zz,x-1]==2 and a[zz,x]==3
    candidates=np.arange(x-48,x+49)
    rise=(y[zz,candidates+8].astype(float)-y[zz,candidates-8])/16
    # 正的东西高差定位向东抬升坡面；slope8 与 relief32 同时提供近场地形支持。
    terrain=rise+.10*np.minimum(slope[zz,candidates],2)+.15*np.minimum(relief[zz,candidates]/32,2)
    score=terrain-.02*abs(candidates-x)
    valid=np.array([np.isin(a[zz-4:zz+5,min(k,x)-4:max(k,x)+5],[2,3]).all() for k in candidates])
    valid &= np.isfinite(score)
    if not valid[48]:continue
    score[~valid]=-np.inf
    eligible=np.where(valid & (score>=score.max()-.15) & (rise>=.8) & (relief[zz,candidates]>=32))[0]
    j=int(min(eligible,key=lambda k:(abs(int(candidates[k])-x),-score[k]))) if len(eligible) else 48
    newx=int(candidates[j])
    # 增益不足保留原线；仅为地形证据门槛，不追求面积均衡，也不平滑输出线。
    if score[j]-score[48]<.35 or rise[j]<.8 or relief[zz,newx]<32:newx=x
    if newx<x:refined[zz,newx:x]=3
    elif newx>x:refined[zz,x:newx]=2
    rows.append({'z':z,'old_x':oldx,'new_x':newx-800,'shift_x':newx-x,'old_y':int(y[zz,x]),'new_y':int(y[zz,newx]),'old_slope8':float(slope[zz,x]),'new_slope8':float(slope[zz,newx]),'old_relief32':int(relief[zz,x]),'new_relief32':int(relief[zz,newx]),'old_eastward_rise16':float((int(y[zz,x+8])-int(y[zz,x-8]))/16),'eastward_rise16':float((int(y[zz,newx+8])-int(y[zz,newx-8]))/16),'score_gain':float(score[j]-score[48]),'west_gentle_component_64':int(f['gentle_component'][zz,newx-64])})
changed=refined!=a;zz,xx=np.where(changed);newedges=edges(refined);newparts=components_edges(newedges);newmain=newedges[newparts[0]]
changed_distance=distance(np.column_stack((xx-799.5,zz+1376.5)),main)
line_distance=distance((newmain[:,:2]+newmain[:,2:])/2,main)
assert len(xx)>0 and changed_distance.max()<=64 and line_distance.max()<=64
assert np.isin(a[changed],[2,3]).all() and np.isin(refined[changed],[2,3]).all()
locked={}
for name,c in [('commons',0),('west',1)]:
    before=a==c;after=refined==c;assert np.array_equal(before,after)
    locked[name]={'count':int(before.sum()),'before_sha256':hashlib.sha256(np.packbits(before).tobytes()).hexdigest(),'after_sha256':hashlib.sha256(np.packbits(after).tobytes()).hexdigest()}
p1r=ROOT/'research/build-sites/CIV-001/AB-001P1R'
for name,c in [('commons',0),('connector',2)]:
    geo=read(p1r/(name+'-geometry.json'));mask=np.zeros(a.shape,bool)
    for z,l,h in geo['runs']:mask[z-1376,l+800:h+801]=True
    assert (a[mask]==c).all() and (refined[mask]==c).all()
    locked['accepted_'+name]={'count':int(mask.sum()),'geometry_sha256':sha(p1r/(name+'-geometry.json')),'unchanged':True}
locked['all_non_middle_east']={'count':int((~np.isin(a,[2,3])).sum()),'unchanged':bool((a[~np.isin(a,[2,3])]==refined[~np.isin(a,[2,3])]).all())}
assert np.array_equal(a!=255,refined!=255) and not np.isin(refined,[4,5]).any()
top={}
for c in (2,3):
    before=topology(a,c);after=topology(refined,c)
    assert len(before)==len(after)
    assert before[1:]==after[1:]
    assert sum(p['enclave'] for p in after)<=sum(p['enclave'] for p in before)
    top[str(c)]={'before_component_count':len(before),'after_component_count':len(after),'before_largest':before[0]['area'],'after_largest':after[0]['area'],'unchanged_secondary_components':True,'before_enclaves':sum(p['enclave'] for p in before),'after_enclaves':sum(p['enclave'] for p in after)}
assert len(parts)==len(newparts)
assert set(map(tuple,oldedges[[i for p in parts[1:] for i in p]]))==set(map(tuple,newedges[[i for p in newparts[1:] for i in p]]))
shutil.copyfile(source,OUT/'baseline-owner-draft.json')
result=json.loads(json.dumps(doc));result.update(status=STATUS,revision=154,owner=None)
result['exportedAt']=None
result['refinement']={'task':'TT-002R','baseline_sha256':sha(source),'method':'local east-facing valley-rim terrain fit; no smoothing','world_writes':0,'new_world_block_reads':0,'owner_acceptance':'PENDING'}
result['runs']=[]
for z,row in enumerate(refined):
    cuts=np.r_[0,np.where(row[1:]!=row[:-1])[0]+1,len(row)]
    for l,h in zip(cuts[:-1],cuts[1:]):
        if row[l]!=255:result['runs'].append([z+1376,int(l)-800,int(h)-801,int(row[l])])
(OUT/'refined-draft.json').write_text(json.dumps(result,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
delta={'status':STATUS,'changed_columns':int(changed.sum()),'middle_to_east':int(((a==2)&(refined==3)).sum()),'east_to_middle':int(((a==3)&(refined==2)).sum()),'before_areas':[int((a==i).sum()) for i in range(6)],'after_areas':[int((refined==i).sum()) for i in range(6)],'displacement':{'definition':'Euclidean distance from refined main unit-edge midpoint to closest Owner main closed unit edge; all edges equally weighted, unchanged edges included','boundary':describe(line_distance),'changed_column_centers':describe(changed_distance),'changed_boundary_only':describe(line_distance[line_distance>0])},'over_64_segments':[],'locked':locked,'row_witnesses':rows}
write(OUT/'boundary-delta.json',delta)
write(OUT/'validation/geometry.json',{'status':'PASS','coverage':int((a!=255).sum()),'no_unassigned_or_disputed':True,'changed_within_64':True,'main_edge_counts':[len(main),len(newmain)],'nonmain_edges_unchanged':True,'locked':locked,'topology':top})
# 诊断统计用距 Owner 邻边陆柱的保守 L1 带，明确区别于最终欧氏位移检验。
dist=np.full(a.shape,999,np.int16)
for x0,z0,x1,z1 in main:
    if x0==x1:dist[z0-1376,x0+799:x0+801]=0
    else:dist[z0-1377:z0-1375,x0+800]=0
for _ in range(128):
    d=dist.copy();dist[1:]=np.minimum(dist[1:],d[:-1]+1);dist[:-1]=np.minimum(dist[:-1],d[1:]+1);dist[:,1:]=np.minimum(dist[:,1:],d[:,:-1]+1);dist[:,:-1]=np.minimum(dist[:,:-1],d[:,1:]+1)
stats={}
for label,arr in [('before',a),('after',refined)]:
    stats[label]={str(c):{name:describe(values[(arr==c)&(dist<128)]) for name,values in [('elevation',y),('slope8',slope),('relief32',relief)]} for c in (2,3)}
corridors=read(ROOT/'research/human-geography/southern-island/WB-003R/profile/movement-corridors.json')
movement=[]
for p in corridors['candidates']:
    q=np.asarray(p['path']);inds=(q[:,1]-1376,q[:,0]+800);inside=dist[inds]<128
    movement.append({'id':p['id'],'path_columns_in_diagnostic_band':int(inside.sum()),'path_columns_reassigned':int(changed[inds].sum()),'meaning':'existing terrain-cost research path, not road / trade route / mandatory political corridor'})
write(OUT/'validation/terrain-comparison.json',{'band':'conservative L1 distance <128 to Owner edge incident columns; no full region reclassification','statistics':stats,'changed_terrain':{name:describe(v[changed]) for name,v in [('elevation',y),('slope8',slope),('relief32',relief)]},'movement':movement,'movement_source_sha256':sha(ROOT/'research/human-geography/southern-island/WB-003R/profile/movement-corridors.json')})
# 统一图框、精确边与图例；图仅用于阅读，JSON RLE 为成员事实。
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',18);small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',14)
crop=(218,1658,1094,2512);x0,z0,x1,z1=crop
colors=np.array([[226,189,102],[92,189,152],[174,147,220],[232,142,105],[155,169,184],[239,110,152]],np.uint8)
segdefs=[('S1',1786,1850,'北岸接入：保留'),('S2',1851,1894,'北侧肩部：保留'),('S3',1895,1960,'内谷东北坡：东域西压'),('S4',1961,2030,'内谷东壁：东域西压'),('S5',2031,2090,'南向坡麓：东域西压'),('S6',2091,2200,'弥散坡面：保留'),('S7',2201,2300,'南段山侧：保留'),('S8',2301,2383,'海岸坡面：保留')]
for mode in ('before','after','diff','terrain-overlay'):
    rgb=np.zeros((*a.shape,3),np.uint8);rgb[:]=[25,48,70]
    if mode in ('before','after'):
        arr=a if mode=='before' else refined;land=arr!=255;rgb[land]=colors[arr[land]]
    else:
        v=np.clip((y.astype(float)-60)/160,0,1);rgb=np.stack([60+v*185,150-v*80,100-v*40],axis=2).astype(np.uint8);rgb[a==255]=[25,48,70]
        if mode=='diff':rgb[~changed]=(rgb[~changed]*.55).astype(np.uint8);rgb[changed]=[255,210,60]
    mapim=Image.fromarray(rgb[z0-1376:z1-1376,x0+800:x1+800]);im=Image.new('RGB',(1170,950),(19,29,40));im.paste(mapim,(40,65));dr=ImageDraw.Draw(im)
    dr.text((25,12),'TT-002R  '+mode+'  |  REFINED DRAFT · 未接受',font=font,fill='white')
    def line(es,color):
        for x,z,xx,zz in es:dr.line((40+x-x0,65+z-z0,40+xx-x0,65+zz-z0),fill=color,width=2)
    if mode!='after':line(main,'#ffffff')
    if mode!='before':line(newmain,'#43e6f2')
    dr.text((930,65),'白：Owner 原线\n青：精修线\n黄：变更列\n\n北 ↑  东 →\n1 px = 1 block',font=small,fill='white',spacing=8)
    for sid,lo,hi,text in segdefs:
        rowsel=main[(main[:,1]>=lo)&(main[:,1]<=hi)];point=rowsel[len(rowsel)//2];px,pz=point[:2]
        dr.text((40+px-x0+10,65+pz-z0),sid,font=font,fill='white')
        dr.text((930,210+(int(sid[1:])-1)*65),sid+' '+text.split('：')[0]+'\n'+text.split('：')[1],font=small,fill='white')
    for z in range(1700,2500,100):dr.text((1,65+z-z0),str(z),font=small,fill='white')
    for x in range(300,1100,100):dr.text((40+x-x0,42),str(x),font=small,fill='white')
    dr.text((40,925),'缓存高程底图：绿低 / 红高（Y60–220 饱和）；非单一等高线切分。world writes = 0',font=small,fill='white')
    im.save(OUT/'visual'/(mode+'.png'))
segmentstats=[]
for sid,lo,hi,name in segdefs:
    m=changed.copy();m[:max(0,lo-1376)]=False;m[hi-1376+1:]=False
    rr=[row for row in rows if lo<=row['z']<=hi]
    segmentstats.append({'id':sid,'z_range':[lo,hi],'interpretation':name,'changed_columns':int(m.sum()),'middle_to_east':int((m&(a==2)).sum()),'east_to_middle':int((m&(a==3)).sum()),'max_row_shift':max([abs(t['shift_x']) for t in rr],default=0)})
write(OUT/'validation/segments.json',segmentstats)
write(OUT/'validation/summary.json',{'status':STATUS,'technical_checks':'PASS','world_writes':0,'new_world_block_reads':0,'broad_rescan':0,'baseline_sha256':sha(source),'refined_sha256':sha(OUT/'refined-draft.json'),'resolved_sources':resolved,'changed_columns':int(changed.sum()),'freshness':'CACHED_EPOCH_ONLY; no current-world freshness claim'})
print(json.dumps({'changed':int(changed.sum()),'delta':delta['after_areas'],'max_boundary_displacement':float(line_distance.max()),'segments':segmentstats,'topology':top},ensure_ascii=False))
