"""实际成员、尺度明确的地形代理；数值分组仅供模型审阅，不裁定自然语义。"""
import json,sqlite3
from collections import deque,Counter
import numpy as np
from L0_公理层.区域契约 import BOUNDS

def load_observed(path):
    db=sqlite3.connect(path.as_uri()+'?mode=ro',uri=True)
    names=[r[1] for r in db.execute('PRAGMA table_info(samples)')]
    rows=np.array(db.execute('SELECT * FROM samples ORDER BY z,x').fetchall(),dtype=np.int32)
    shape=(BOUNDS[3]-BOUNDS[1]+1,BOUNDS[2]-BOUNDS[0]+1)
    assert len(rows)==shape[0]*shape[1]
    result={name:rows[:,i].reshape(shape) for i,name in enumerate(names)}
    for k in ('leaf','trunk','dry_ground_vegetation','other_vegetation'):result[k]=np.full(shape,-1,np.int16)
    for x,z,*counts in db.execute('SELECT * FROM vegetation ORDER BY z,x'):
        for name,value in zip(('leaf','trunk','dry_ground_vegetation','other_vegetation'),counts):result[name][z-BOUNDS[1],x-BOUNDS[0]]=value
    biomes=dict(db.execute('SELECT id,name FROM biomes'));states={i:json.loads(s) for i,s in db.execute('SELECT * FROM states')};db.close()
    return result,biomes,states

def components(mask,top=None,bottom=None):
    """4邻接；水边仅在实测竖直水区间交叠时成立，不能跨干地或对角。"""
    labels=np.zeros(mask.shape,np.int32);height,width=mask.shape;count=0
    for z,x in zip(*np.where(mask)):
        if labels[z,x]:continue
        count+=1;labels[z,x]=count;q=deque([(int(z),int(x))])
        while q:
            a,b=q.popleft()
            for c,d in ((a-1,b),(a+1,b),(a,b-1),(a,b+1)):
                if c<0 or c>=height or d<0 or d>=width or not mask[c,d] or labels[c,d]:continue
                if top is not None and max(bottom[a,b],bottom[c,d])>min(top[a,b],top[c,d]):continue
                labels[c,d]=count;q.append((c,d))
    return labels

def extent_filter(a,radius,op):
    """可分离方窗极值，半径r表示边长2r+1；ROI边缘重复端点且另标截断。"""
    for axis in (0,1):
        pads=[(0,0),(0,0)];pads[axis]=(radius,radius)
        a=op(np.lib.stride_tricks.sliding_window_view(np.pad(a,pads,mode='edge'),radius*2+1,axis=axis),axis=-1)
    return a

def distribution(a):
    a=np.asarray(a);a=a[np.isfinite(a)]
    if not len(a):return None
    return dict(zip(('min','p10','p25','median','p75','p90','max'),map(float,np.percentile(a,[0,10,25,50,75,90,100]))),mean=float(a.mean()))

def compute(a):
    h=a['exposed_y'];wet=a['water_y']!=-32768;land=~wet
    result={'land_component':components(land),'water_component':components(wet,a['water_y'],a['water_bottom'])}
    slope=np.full(h.shape,np.nan,np.float32);valid=land[8:-8,8:-8]&land[:-16,8:-8]&land[16:,8:-8]&land[8:-8,:-16]&land[8:-8,16:]
    s=np.hypot((h[8:-8,16:]-h[8:-8,:-16])/16,(h[16:,8:-8]-h[:-16,8:-8])/16)
    slope[8:-8,8:-8]=np.where(valid,s,np.nan);result['slope8']=slope
    step=np.zeros(h.shape,np.int16)
    shore=np.zeros(h.shape,bool)
    for axis in (0,1):
        first=[slice(None),slice(None)];second=first.copy();first[axis]=slice(None,-1);second[axis]=slice(1,None);first=tuple(first);second=tuple(second)
        delta=np.where(land[first]&land[second],np.abs(h[first]-h[second]),0)
        step[first]=np.maximum(step[first],delta);step[second]=np.maximum(step[second],delta)
        shore[first]|=land[first]&wet[second];shore[second]|=land[second]&wet[first]
    result['step1']=step;result['shoreline']=shore
    for span in (16,32,64):
        high=extent_filter(np.where(land,h,-32768),span//2,np.max);low=extent_filter(np.where(land,h,32767),span//2,np.min)
        result['relief'+str(span)]=np.where(land,high-low,-1).astype(np.int16)
    # 仅为本低岛的相对高低地/脊顶位置代理，不能把Y72自动命名为山地。
    result['local_highland_proxy']=(land&(h>=72)).astype(np.int8)
    result['local_lowland_proxy']=(land&(h<=65)).astype(np.int8)
    result['ridge_position_proxy']=(land&(high-low>=8)&((h-low)>=0.8*(high-low))).astype(np.int8)
    flat=land&(result['relief32']<=4)&(slope<=0.125)&(step<=1)
    gentle=land&~flat&(result['relief32']<=8)&(slope<=0.25)&(step<=2)
    result['terrain_class']=np.where(flat,1,np.where(gentle,2,0)).astype(np.int8)
    result['flat_component']=components(flat);result['gentle_component']=components(gentle)
    return result

def groups(labels):
    flat=labels.ravel();idx=np.flatnonzero(flat);idx=idx[np.argsort(flat[idx],kind='stable')]
    for group in np.split(idx,np.flatnonzero(np.diff(flat[idx]))+1):
        if len(group):yield int(flat[group[0]]),group

def summary(indices,a,m,biomes):
    w=a['x'].shape[1];z,x=np.divmod(indices,w);maskvals=lambda name:a[name].ravel()[indices]
    sample=maskvals('leaf')>=0
    counts=Counter(int(i) for i in maskvals('filtered_biome'))
    return {'area_blocks2':len(indices),'bounds':[int(x.min()+BOUNDS[0]),int(z.min()+BOUNDS[1]),int(x.max()+BOUNDS[0]),int(z.max()+BOUNDS[1])],'elevation':distribution(maskvals('exposed_y')),'slope8':distribution(m['slope8'].ravel()[indices]),'relief32':distribution(m['relief32'].ravel()[indices]),'biomes':{biomes[k]:v for k,v in sorted(counts.items())},'flat_share':float(np.mean(m['terrain_class'].ravel()[indices]==1)),'gentle_share':float(np.mean(m['terrain_class'].ravel()[indices]==2)),'shoreline_columns':int(m['shoreline'].ravel()[indices].sum()),'touches_roi':bool(x.min()==0 or z.min()==0 or x.max()==w-1 or z.max()==a['x'].shape[0]-1),'vegetation':{'sample_columns':int(sample.sum()),**{k:{'occupied_fraction':float(np.mean(maskvals(k)[sample]>0)) if sample.any() else None,'blocks_per_sample':float(np.mean(maskvals(k)[sample])) if sample.any() else None} for k in ('leaf','trunk','dry_ground_vegetation','other_vegetation')}}}

def runs(labels):
    for z,row in enumerate(labels):
        starts=np.r_[0,np.flatnonzero(row[1:]!=row[:-1])+1];ends=np.r_[starts[1:],len(row)]
        for s,e in zip(starts,ends):
            if row[s]:yield int(row[s]),z+BOUNDS[1],int(s+BOUNDS[0]),int(e-1+BOUNDS[0])

def numerical_zoning(a,m,island):
    """比较k=2..5的属性聚类，保留碎片性；不把kmeans当作自然区数量真值。"""
    h=a['exposed_y'];cells=[];features=[];bids=sorted(np.unique(a['filtered_biome'][island]).tolist())
    for z in range(0,h.shape[0],16):
        for x in range(0,h.shape[1],16):
            roi=np.s_[z:z+16,x:x+16];mask=island[roi]
            if not mask.any():continue
            obs=(a['leaf'][roi]>=0)&mask
            vals=[float(np.median(h[roi][mask])),float(np.mean(m['relief32'][roi][mask])),float(np.nanmean(m['slope8'][roi][mask])) if np.isfinite(m['slope8'][roi][mask]).any() else 0,float(np.mean(a['leaf'][roi][obs]>0)) if obs.any() else 0,float(np.mean(a['trunk'][roi][obs]>0)) if obs.any() else 0,float(np.mean(m['terrain_class'][roi][mask]>0))]
            vals += [float(np.mean(a['filtered_biome'][roi][mask]==b)) for b in bids]
            features.append(vals);cells.append((z,x))
    # 固定物理尺度避免罕见biome的近零方差将一个小斑块放大成宏观分区。
    f=np.array(features);scale=np.array([8,8,0.25,0.25,0.05,0.5]+[1]*len(bids));v=(f-f.mean(axis=0))/scale
    results=[];maps={}
    for k in range(2,6):
        best=None
        for seed in (2,17,83):
            rng=np.random.default_rng(seed);centers=[v[rng.integers(len(v))]]
            while len(centers)<k:
                distances=np.min(((v[:,None,:]-np.array(centers)[None,:,:])**2).sum(axis=2),axis=1)
                centers.append(v[rng.choice(len(v),p=distances/distances.sum())])
            centers=np.array(centers)
            for _ in range(60):
                labels=np.argmin(((v[:,None,:]-centers[None,:,:])**2).sum(axis=2),axis=1);new=np.array([v[labels==i].mean(axis=0) if np.any(labels==i) else centers[i] for i in range(k)])
                if np.allclose(new,centers,rtol=0,atol=1e-9):break
                centers=new
            sse=float(((v-centers[labels])**2).sum())
            if best is None or sse<best[0]:best=(sse,labels,centers)
        sse,labels,centers=best;order=sorted(range(k),key=lambda i:float(f[labels==i,0].mean()));renum={old:new+1 for new,old in enumerate(order)}
        grid=np.zeros(h.shape,np.int16)
        for (z,x),label in zip(cells,labels):grid[z:z+16,x:x+16]=renum[int(label)]
        grid[~island]=0;maps['k'+str(k)]=grid
        results.append({'k':k,'standardized_sse':sse,'mean_features_by_elevation_order':[f[labels==i].mean(axis=0).tolist() for i in order],'area_shares':[float(np.mean(grid[island]==i+1)) for i in range(k)],'spatial_components':[int(components(grid==i+1).max()) for i in range(k)],'semantics':'numerical alternatives only; model must judge continuity and transitions'})
    return {'features':['elevation','relief32','slope8','leaf_occupancy','trunk_occupancy','flat_plus_gentle_share']+['biome_'+str(b) for b in bids],'fixed_feature_scales':scale.tolist(),'algorithm':'kmeans++ seeds 2,17,83; minimum SSE; standardized_sse uses fixed physical feature scales, no geographic coordinates','alternatives':results},maps
