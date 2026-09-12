"""在当前只读快照上核查三个已人工选定的地形口袋；输出容量包络而非建筑形状。

搜索半径仅限制局部研究量级；树木、净空、坡折和已有内容裁切真实成员。
地下检查止于各柱地面以下 12 格，不能外推为深层无风险。
"""
import gzip,json,sqlite3,heapq
from collections import Counter,deque
import numpy as np
import 当前场地读取 as s
rows=json.load(gzip.open(s.CACHE/'surface.json.gz','rt',encoding='utf-8'))
by={(p['x'],p['z']):p for p in rows};observed=np.zeros((s.H,s.W),bool)
y=np.full(observed.shape,-32768,np.int16);trees=np.zeros(observed.shape,bool);hazard=np.zeros(observed.shape,bool)
for p in rows:
    z,x=p['z']-s.Z0,p['x']-s.X0;observed[z,x]=True;y[z,x]=p['ground_y']
    trees[z,x]=any('_log' in v[1] or '_wood' in v[1] for v in p['above'])
    hazard[z,x]=s.artificial(p['ground']) or p['ground'] in s.WATER or any(s.artificial(v[1]) for v in p['above'])
g=s.mask(next(n for n in s.read(s.PLAN/'settlement-nodes.json')['nodes'] if n['id']=='G1')['envelope'])
clear=s.mask(s.read(s.PLAN/'land-use.json')['building_exclusion_overlays'][0]['geometry'])
reader=s.Reader();blockentities=[];entities=[];pois=[];structures=[]
for cx,cz in s.read(s.CACHE/'capture.json')['selected_chunks']:
    d=reader.chunk(cx,cz)
    for be in d.get('block_entities',[]):
        p={k:int(be[k]) for k in ('x','y','z')};p['id']=str(be['id']);blockentities.append(p)
        if (p['x'],p['z']) in by:hazard[p['z']-s.Z0,p['x']-s.X0]=True
    for key,st in d.get('structures',{}).get('starts',{}).items():structures.append({'chunk':[cx,cz],'id':str(key),'summary':str(st)[:500]})
    ed=reader.chunk(cx,cz,'entities')
    if ed:
        for e in ed.get('Entities',[]):
            pos=[float(v) for v in e['Pos']]
            if (int(np.floor(pos[0])),int(np.floor(pos[2]))) in by:entities.append({'id':str(e['id']),'pos':pos,'item':str(e.get('Item',{}).get('id',''))})
    pd=reader.chunk(cx,cz,'poi')
    if pd:
        for section in pd.get('Sections',{}).values():
            for rec in section.get('Records',[]):pois.append({'type':str(rec.get('type')),'pos':[int(v) for v in rec['pos']]})

# 阶地中心由实际当前图人工辨认；不是先摆固定建筑矩形。
specs=[('S1','东侧高位缓台',[226,1700],19),('S2','北侧中段缓台',[193,1708],18),('S3','南侧生活口袋',[188,1752],19)]
eligible=g&~s.dilate(clear,2)&~s.dilate(hazard,4)&~s.dilate(trees,2)
candidates=[];claimed=np.zeros(g.shape,bool)
for cid,name,point,radius in specs:
    z,x=point[1]-s.Z0,point[0]-s.X0;assert eligible[z,x],(cid,point,'anchor not eligible')
    same=eligible&~claimed&(abs(y-int(y[z,x]))<=1)
    dist=np.full(g.shape,-1,np.int16);dist[z,x]=0;queue=[(z,x)]
    for zz,xx in queue:
        if dist[zz,xx]>=radius:continue
        for dz,dx in ((0,1),(0,-1),(1,0),(-1,0)):
            nz,nx=zz+dz,xx+dx
            if same[nz,nx] and dist[nz,nx]<0 and abs(int(y[nz,nx])-int(y[zz,xx]))<=1:
                dist[nz,nx]=dist[zz,xx]+1;queue.append((nz,nx))
    m=dist>=0;claimed|=m;buffer=s.dilate(m,4);assert observed[buffer].all()
    zvals,xvals=np.where(m);values=y[m];bufrows=[by[(int(xx)+s.X0,int(zz)+s.Z0)] for zz,xx in zip(*np.where(buffer))]
    subs=Counter();anomalies=[];toprisk=[];vegetation=Counter()
    for p in bufrows:
        for yy,name0 in p['above']:
            if name0 not in s.AIR:vegetation[name0]+=1
            if s.artificial(name0):toprisk.append([p['x'],yy,p['z'],name0])
        for yy in range(p['ground_y']-12,p['ground_y']+1):
            name0=reader.block(p['x'],yy,p['z']);subs[name0]+=1
            if name0 in s.AIR|s.WATER or name0=='minecraft:lava' or s.artificial(name0):anomalies.append([p['x'],yy,p['z'],name0])
    # 枚举接近旧预留中心线的步行见证；非设计入口或道路。
    pathpoints=[p for r in s.read(s.PLAN/'movement-network.json')['routes'][:2] for p in r['path']]
    targetset={(p[0],p[1]) for p in pathpoints};accessdist=np.full(g.shape,-1,np.int16);parents={};q=deque()
    for zz,xx in zip(*np.where(m)):
        accessdist[zz,xx]=0;q.append((int(zz),int(xx)))
    found=None
    while q:
        zz,xx=q.popleft()
        if (xx+s.X0,zz+s.Z0) in targetset:found=(zz,xx);break
        for dz,dx in ((0,1),(0,-1),(1,0),(-1,0)):
            nz,nx=zz+dz,xx+dx
            if 0<=nz<s.H and 0<=nx<s.W and observed[nz,nx] and not hazard[nz,nx] and not trees[nz,nx] and accessdist[nz,nx]<0 and abs(int(y[nz,nx])-int(y[zz,xx]))<=1:
                accessdist[nz,nx]=accessdist[zz,xx]+1;parents[(nz,nx)]=(zz,xx);q.append((nz,nx))
    assert found is not None
    access=[];cur=found
    while True:
        zz,xx=cur;access.append([xx+s.X0,zz+s.Z0,int(y[zz,xx])])
        if cur not in parents:break
        cur=parents[cur]
    access.reverse()
    # 检查是否存在不升高的局部排水方向；仅证明附近低地，不证明饮水或最终排水系统。
    lowest=min(((int(y[zz,xx]),int(zz),int(xx)) for zz,xx in zip(zvals,xvals)))
    _,zz,xx=lowest;visited={(zz,xx)};q=deque([(zz,xx)]);parents2={};outlet=None
    while q:
        zz,xx=q.popleft()
        if not buffer[zz,xx] and int(y[zz,xx])<lowest[0]:outlet=(zz,xx);break
        for dz,dx in ((0,1),(0,-1),(1,0),(-1,0)):
            nz,nx=zz+dz,xx+dx
            if 0<=nz<s.H and 0<=nx<s.W and observed[nz,nx] and (nz,nx) not in visited and int(y[nz,nx])<=int(y[zz,xx]):
                visited.add((nz,nx));parents2[(nz,nx)]=(zz,xx);q.append((nz,nx))
    drain=[]
    if outlet:
        cur=outlet
        while True:
            zz,xx=cur;drain.append([xx+s.X0,zz+s.Z0,int(y[zz,xx])])
            if cur not in parents2:break
            cur=parents2[cur]
        drain.reverse()
    entities_local=[e for e in entities if buffer[int(np.floor(e['pos'][2]))-s.Z0,int(np.floor(e['pos'][0]))-s.X0]]
    edges=[]
    for zz,xx in zip(zvals,xvals):
        for dz,dx in ((0,1),(1,0)):
            if m[zz+dz,xx+dx]:edges.append(abs(int(y[zz+dz,xx+dx])-int(y[zz,xx])))
    # 缓冲边界作开放边界的局部 priority flood，只检测小尺度闭洼；不等于流域洪水模型。
    filled=np.full(y.shape,32767,np.int16);heap=[]
    for zz,xx in zip(*np.where(buffer)):
        if not all(buffer[zz+dz,xx+dx] for dz,dx in ((0,1),(0,-1),(1,0),(-1,0))):
            filled[zz,xx]=y[zz,xx];heapq.heappush(heap,(int(y[zz,xx]),int(zz),int(xx)))
    while heap:
        level,zz,xx=heapq.heappop(heap)
        if filled[zz,xx]!=level:continue
        for dz,dx in ((0,1),(0,-1),(1,0),(-1,0)):
            nz,nx=zz+dz,xx+dx
            if buffer[nz,nx]:
                value=max(level,int(y[nz,nx]))
                if value<filled[nz,nx]:filled[nz,nx]=value;heapq.heappush(heap,(value,nz,nx))
    depths=filled[m]-y[m]
    candidates.append({'id':cid,'name':name,'study_anchor':point,'geometry':s.rle(m),'bounds':[int(xvals.min())+s.X0,int(zvals.min())+s.Z0,int(xvals.max())+s.X0,int(zvals.max())+s.Z0],'gross_usable_area':int(m.sum()),'buffer_geometry':s.rle(buffer),'buffer_area':int(buffer.sum()),'surface_elevation_range':[int(values.min()),int(values.max())],'median_ground_y':float(np.median(values)),'relief':int(np.ptp(values)),'adjacent_max_step':max(edges),'adjacent_mean_step':float(np.mean(edges)),'ground_materials':dict(Counter(by[(int(xx)+s.X0,int(zz)+s.Z0)]['ground'] for zz,xx in zip(zvals,xvals))),'terrain_scope_rule':{'reachable_steps':radius,'anchor_y_tolerance':1,'tree_trunk_buffer':2,'clearance_extra_margin':2,'candidate_buffer':4,'not_architecture_footprint':True},'above_buffer_palette':dict(vegetation),'identified_artificial_surface':toprisk,'block_entities_in_buffer':[e for e in blockentities if (e['x'],e['z']) in by and buffer[e['z']-s.Z0,e['x']-s.X0]],'entities_in_buffer':entities_local,'subsurface':{'depth_below_ground':12,'ground_included':True,'queried_blocks':sum(subs.values()),'palette_counts':dict(subs),'anomalies':anomalies,'buffer_risk_applies_to_site':True},'access_witness':access,'access_steps':len(access)-1,'drainage_witness':drain,'has_local_lower_outlet':bool(drain),'local_pit_check':{'maximum_fill_depth':int(depths.max()),'depressed_columns':int((depths>0).sum()),'boundary_assumption':'four-column buffer edge open; not catchment flood certification'},'status':'CURRENT SNAPSHOT CANDIDATE / AWAITING SEMANTIC COMPARISON'})
    print(cid,int(m.sum()),'Y',int(values.min()),int(values.max()),'access',len(access)-1,'drain',len(drain),'sub anomalies',len(anomalies),dict(Counter(v[3] for v in anomalies)),flush=True)
s.write(s.CACHE/'candidate-analysis.json',candidates)
s.write(s.CACHE/'content-analysis.json',{'block_entities':blockentities,'entities':entities,'poi_records':pois,'structure_starts':structures,'source_chunks':len(s.read(s.CACHE/'capture.json')['selected_chunks'])})

dbpath=s.ROOT/'research/human-geography/southern-island/WB-002R-R1/raw-or-queryable/observed.sqlite'
changes=[]
with sqlite3.connect(dbpath.as_uri()+'?mode=ro',uri=True) as db:
    names={int(i):json.loads(v)['Name'] for i,v in db.execute('SELECT id,json FROM states')}
    for p in rows:
        if not g[p['z']-s.Z0,p['x']-s.X0]:continue
        old=db.execute('SELECT exposed_y,exposed_state,surface_y,surface_state FROM samples WHERE x=? AND z=?',(p['x'],p['z'])).fetchone();assert old
        if (p['ground_y'],p['ground'],p['surface_y'],p['top'])!=(old[0],names[old[1]],old[2],names[old[3]]):changes.append({'point':[p['x'],p['z']],'current':[p['ground_y'],p['ground'],p['surface_y'],p['top']],'cache':[old[0],names[old[1]],old[2],names[old[3]]]})
s.write(s.CACHE/'cache-delta.json',{'compared_G1_columns':int(g.sum()),'changed_columns':len(changes),'changes':changes,'comparison_fields':['exposed_y','exposed_block_name','surface_y','surface_block_name'],'not_compared':'block properties, biome and historical below-ground state'})
print('cache changes',len(changes))
