"""几何距离与地形代价图只表达操作性阻力，不承诺船行、步行或道路可行性。"""
import heapq,math
from collections import deque
import numpy as np
from L0_公理层.基底契约 import BOUNDS

def approach_masks(a,m):
    land=m['land_component']>0;good=np.zeros(land.shape,bool);h=a['exposed_y']
    # 从岸柱沿任一卡方向进入陆地8格，逐步高差<=1；窗口起伏约束另加。
    for dz,dx in ((0,1),(0,-1),(1,0),(-1,0)):
        valid=land.copy();last=h
        for step in range(1,9):
            there=np.roll(h,(-dz*step,-dx*step),axis=(0,1));dry=np.roll(land,(-dz*step,-dx*step),axis=(0,1))
            valid &= dry&(np.abs(there-last)<=1);last=there
        good|=valid
    good[:8]=False;good[-8:]=False;good[:,:8]=False;good[:,-8:]=False
    return good&m['shoreline']&(m['relief16']<=8)

def nearest_pair(left,right):
    """穷尽实际岸柱单位方格间距，减去每轴两个半格；不是bbox间距。"""
    if not len(left) or not len(right):return None
    best=None
    for start in range(0,len(left),128):
        delta=np.maximum(np.abs(left[start:start+128,None,:]-right[None,:,:])-1,0)
        squared=(delta.astype(np.int64)**2).sum(axis=2);i,j=np.unravel_index(np.argmin(squared),squared.shape)
        value=int(squared[i,j]);p=tuple(map(int,left[start+i]));q=tuple(map(int,right[j]));candidate=(value,p,q)
        if best is None or candidate<best:best=candidate
    return best

def endpoint(a,m,p):
    z,x=p;h=a['exposed_y'];land=m['land_component']>0;options=[]
    for dz,dx in ((0,1),(0,-1),(1,0),(-1,0)):
        points=[(z,x)]
        for i in range(1,17):
            zz,xx=z+dz*i,x+dx*i
            if not(0<=zz<h.shape[0] and 0<=xx<h.shape[1]) or not land[zz,xx]:break
            points.append((zz,xx))
        ys=[int(h[v]) for v in points];steps=[abs(b-a) for a,b in zip(ys,ys[1:])]
        options.append({'path':[[xx+BOUNDS[0],zz+BOUNDS[1],int(h[zz,xx])] for zz,xx in points],'max_step':max(steps,default=0),'length_blocks':len(points)-1})
    options.sort(key=lambda o:(-min(o['length_blocks'],8),o['max_step'],-o['length_blocks'],o['path']))
    waters=[]
    for dz,dx in ((0,1),(0,-1),(1,0),(-1,0)):
        zz,xx=z+dz,x+dx
        if a['water_y'][zz,xx]!=-32768:waters.append({'x':xx+BOUNDS[0],'z':zz+BOUNDS[1],'top_y':int(a['water_y'][zz,xx]),'bottom_y':int(a['water_bottom'][zz,xx]),'depth_blocks':int(a['water_y'][zz,xx]-a['water_bottom'][zz,xx]+1)})
    return {'x':x+BOUNDS[0],'z':z+BOUNDS[1],'surface_y':int(h[z,x]),'relief16':int(m['relief16'][z,x]),'step1':int(m['step1'][z,x]),'straight_inland_approach':options[0],'adjacent_water':waters}

def crossing(a,m):
    good=approach_masks(a,m);west=np.argwhere(m['west']&m['shoreline']);east=np.argwhere(m['east']&m['shoreline']);results=[]
    selections=[('X-00','global minimum',west,east)]
    for i,(lo,hi) in enumerate(((1400,1750),(1750,2100),(2100,2550)),1):
        mask=good&(a['z']>=lo)&(a['z']<hi)
        selections.append((f'X-{i:02d}',f'low-approach shores in Z[{lo},{hi})',np.argwhere(m['west']&mask),np.argwhere(m['east']&mask)))
    for id,meaning,l,r in selections:
        best=nearest_pair(l,r)
        if best is None:results.append({'id':id,'status':'NO_ELIGIBLE_PAIR','selection':meaning});continue
        squared,p,q=best;delta=np.asarray(q,dtype=float)-p
        # 最近方格边界之间取样；独立验证时用supercover检查整段触及的格。
        start=np.asarray(p,dtype=float)+np.sign(delta)*np.minimum(abs(delta)/2,.5)
        end=np.asarray(q,dtype=float)-np.sign(delta)*np.minimum(abs(delta)/2,.5)
        points=start+(end-start)*np.linspace(0,1,max(3,math.ceil(math.sqrt(squared)*8)+1))[:,None]
        cells=np.floor(points+.5).astype(int);cells=np.unique(cells,axis=0)
        inner=[(int(z),int(x)) for z,x in cells if (int(z),int(x)) not in (p,q)]
        water=all(a['water_y'][z,x]!=-32768 for z,x in inner)
        # 审核发现短角切割可漏过离散抽样；逐网格穿越时点及其间隔中点检查闭方格。
        times={0.,1.};v=end-start
        for axis in (0,1):
            if v[axis]:
                for grid in range(math.floor(min(start[axis],end[axis]))-1,math.ceil(max(start[axis],end[axis]))+1):
                    t=(grid+.5-start[axis])/v[axis]
                    if 0<=t<=1:times.add(float(t))
        times=sorted(times);probes=times+[(u+w)/2 for u,w in zip(times,times[1:])];exact=set()
        for t in probes:
            z,x=start+t*v
            zs=range(math.ceil(z-.5-1e-9),math.floor(z+.5+1e-9)+1);xs=range(math.ceil(x-.5-1e-9),math.floor(x+.5+1e-9)+1)
            exact.update((zz,xx) for zz in zs for xx in xs)
        dry=sorted([list((x+BOUNDS[0],z+BOUNDS[1])) for z,x in exact if (z,x) not in (p,q) and a['water_y'][z,x]==-32768])
        results.append({'id':id,'selection':meaning,'edge_to_edge_gap_blocks':math.sqrt(squared),'shore_center_distance':float(np.linalg.norm(delta)),'west':endpoint(a,m,p),'east':endpoint(a,m,q),'sampled_straight_segment_water_only':water,'segment_sample_step_max':0.125,'exact_closed_cell_water_only':not dry,'intersected_dry_cells':dry,'status':'WATER_GAP_PROXY' if not dry else 'REJECTED_AS_CLEAR_STRAIGHT_CROSSING','interpretation':'surface geometric crossing proxy, not route/navigation authorization; exact check overrides sampled check'})
    return {'method':'exhaustive nearest unit-square shoreline distance; global plus three predeclared latitude bands with 8-block <=1 step inward approach and relief16<=8','candidates':results,'minimum_search_sizes':[len(west),len(east)]},good

def cost_search(a,m,start,goals,cliff_weight):
    mask=m['east'].ravel().astype(bool);h=a['exposed_y'].ravel();width=a['x'].shape[1]
    base=1+2*np.nan_to_num(m['slope8'].ravel(),nan=1.0)+m['relief32'].ravel()/16+0.5*m['step1'].ravel()
    dist=np.full(len(mask),np.inf);prev=np.full(len(mask),-1,np.int32);dist[start]=0;queue=[(0.,int(start))];pending=set(goals);visited=0
    while queue and pending:
        value,i=heapq.heappop(queue)
        if value!=dist[i]:continue
        visited+=1;pending.discard(i)
        for j in (i-width,i-1,i+1,i+width):
            if not mask[j]:continue
            step=int(h[i])-int(h[j]);cost=(float(base[i])+float(base[j]))/2+cliff_weight*step*step
            v=value+cost
            if v<dist[j]:dist[j]=v;prev[j]=i;heapq.heappush(queue,(v,j))
    results=[]
    for goal in goals:
        if not np.isfinite(dist[goal]):results.append({'status':'UNREACHABLE'});continue
        route=[int(goal)]
        while route[-1]!=start:route.append(int(prev[route[-1]]));assert route[-1]>=0
        route.reverse();ys=h[route];zz,xx=np.divmod(route,width)
        results.append({'status':'COST_GRAPH_PATH','cost':float(dist[goal]),'length_blocks':len(route)-1,'maximum_single_step':int(np.abs(np.diff(ys)).max()),'ascent_blocks':int(np.maximum(np.diff(ys),0).sum()),'descent_blocks':int(np.maximum(-np.diff(ys),0).sum()),'path':[[int(x+BOUNDS[0]),int(z+BOUNDS[1]),int(y)] for x,z,y in zip(xx,zz,ys)],'indices':route})
    return results,visited

def corridors(a,m,dd):
    def medoid(mask):
        idx=np.flatnonzero(mask);assert len(idx);x=a['x'].ravel()[idx];z=a['z'].ravel()[idx]
        return int(idx[np.argmin((x-x.mean())**2+(z-z.mean())**2)])
    start=medoid(dd['M']&(a['exposed_y']<=90)&(m['terrain_class']>0))
    goals=[medoid(dd['E']&(a['exposed_y']>=180)&(a['z']>=lo)&(a['z']<hi)) for lo,hi in ((1450,2150),(2150,2650),(2650,3250))]
    baseline,visited=cost_search(a,m,start,goals,4);sensitive,_=cost_search(a,m,start,goals,16)
    records=[]
    for i,(p,q) in enumerate(zip(baseline,sensitive),1):
        aa=set(p.pop('indices'));bb=set(q.pop('indices'));p['id']=f'C-{i:02d}';p['sensitivity']={'cliff_weight':16,'cost':q['cost'],'length_blocks':q['length_blocks'],'maximum_single_step':q['maximum_single_step'],'path_member_jaccard':len(aa&bb)/len(aa|bb),'path':q['path']};records.append(p)
    return {'resolution_blocks':1,'graph':'4-neighbor dry columns of east island only; water excluded; no diagonal corner cutting','node_cost':'1 + 2*slope8 + relief32/16 + 0.5*step1; missing slope8 ->1.0 (unknown penalized)','edge_cost':'mean(endpoint node costs) + cliff_weight*(actual height difference)^2','cliff_weight':4,'endpoint_selection':'start nearest centroid of M low/gentle Y<=90; destinations nearest centroids of E Y>=180 in predeclared north/central/south Z bands; research probes, not settlement sites','visited_nodes_baseline':visited,'candidates':records,'limitations':'finite cliff penalty permits jumps; cost paths are not confirmed walkable routes, roads or trade routes'}
