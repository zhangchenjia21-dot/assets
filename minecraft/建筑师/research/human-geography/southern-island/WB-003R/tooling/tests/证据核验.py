"""在冻结缓存上独立核验样本设计、岸距、整段水面和路径边，不接触世界写接口。"""
import sys,json,math
from pathlib import Path
import numpy as np
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from L1_器件层.缓存读取器 import load,distance
from L1_器件层.源快照保护器 import write_json
from L0_公理层.基底契约 import BOUNDS,domains

out=Path(__file__).resolve().parents[2];a,m,_,_=load(out.parent/'WB-002R-R1');dd=domains(a,m)
plan=json.loads((out/'review/sampling-design.json').read_text(encoding='utf-8'))['sites'];rng=np.random.default_rng(3003);expected=[]
for domain in ('W','M','E'):
    sites=[(int(a['exposed_y'][z,x]),z+BOUNDS[1],x+BOUNDS[0]) for z,x in np.argwhere(dd[domain]&(a['x']%64==32)&(a['z']%64==32))]
    sites.sort()
    for stratum,group in enumerate(np.array_split(np.arange(len(sites)),3)):
        selected=[sites[i] for i in rng.choice(group,min(16,len(group)),replace=False)]
        for y,z,x in sorted(selected,key=lambda s:(s[1],s[2])):expected.append((domain,stratum,x,z,y))
assert expected==[(s['domain'],s['stratum'],s['x'],s['z'],s['surface_y']) for s in plan]
assert not m['east'][0].any() and not m['east'][-1].any() and not m['east'][:,0].any() and not m['east'][:,-1].any()
cross=json.loads((out/'profile/crossing-profile.json').read_text(encoding='utf-8'));minimum=cross['candidates'][0]['edge_to_edge_gap_blocks'];best=float('inf');pairs=0
east=np.argwhere(m['east']&m['shoreline']);west=np.argwhere(m['west']&m['shoreline'])
for p in west:
    subset=east[(np.abs(east[:,0]-p[0])<=minimum+1)&(np.abs(east[:,1]-p[1])<=minimum+1)]
    for q in subset:
        gap=math.hypot(max(abs(int(p[0])-int(q[0]))-1,0),max(abs(int(p[1])-int(q[1]))-1,0));best=min(best,gap);pairs+=1
assert abs(best-minimum)<1e-10
segments=[]
for c in cross['candidates']:
    if 'west' not in c:continue
    p=np.array([c['west']['z']-BOUNDS[1],c['west']['x']-BOUNDS[0]],float);q=np.array([c['east']['z']-BOUNDS[1],c['east']['x']-BOUNDS[0]],float);delta=q-p
    start=p+np.sign(delta)*np.minimum(abs(delta)/2,.5);end=q-np.sign(delta)*np.minimum(abs(delta)/2,.5);v=end-start;wet=0;dry=[];depth=[]
    # 闭方格slab相交，连只触角点的格也保守检查；不是等距抽样。
    for z in range(math.floor(min(start[0],end[0])-.5),math.ceil(max(start[0],end[0])+.5)+1):
        for x in range(math.floor(min(start[1],end[1])-.5),math.ceil(max(start[1],end[1])+.5)+1):
            if (z,x) in (tuple(p),tuple(q)):continue
            lo=0.;hi=1.
            for axis,coord in enumerate((z,x)):
                if v[axis]==0:
                    if not coord-.5<=start[axis]<=coord+.5:hi=-1;break
                else:
                    ts=sorted(((coord-.5-start[axis])/v[axis],(coord+.5-start[axis])/v[axis]));lo=max(lo,ts[0]);hi=min(hi,ts[1])
            if lo<=hi+1e-12:
                if a['water_y'][z,x]==-32768:dry.append([x+BOUNDS[0],z+BOUNDS[1]])
                else:wet+=1;depth.append(int(a['water_y'][z,x]-a['water_bottom'][z,x]+1))
    segments.append({'id':c['id'],'closed_cell_supercover_water_only':not dry,'water_cells':wet,'dry_cells':dry,'water_depth_min_max':[min(depth),max(depth)] if depth else None})
paths=json.loads((out/'profile/movement-corridors.json').read_text(encoding='utf-8'));checks=[]
base=1+2*np.nan_to_num(m['slope8'],nan=1.0)+m['relief32']/16+.5*m['step1']
for c in paths['candidates']:
    for label,path,want,weight in [('baseline',c['path'],c['cost'],4),('sensitivity',c['sensitivity']['path'],c['sensitivity']['cost'],16)]:
        cost=0.;last=None;maxstep=0
        for x,z,y in path:
            i=(z-BOUNDS[1],x-BOUNDS[0]);assert m['east'][i] and a['water_y'][i]==-32768 and a['exposed_y'][i]==y
            if last is not None:
                j,yy=last;assert abs(i[0]-j[0])+abs(i[1]-j[1])==1;step=abs(y-yy);maxstep=max(maxstep,step);cost+=(float(base[i])+float(base[j]))/2+weight*step**2
            last=i,y
        assert abs(cost-want)<1e-7
        checks.append({'id':c['id'],'variant':label,'edges':len(path)-1,'recomputed_cost':cost,'max_step':maxstep,'all_edges_dry_cardinal':True})
# 距离算法用小格网穷举独立验证，覆盖边缘和多个种子。
seed=np.zeros((11,13),bool);seed[0,12]=seed[5,7]=seed[10,0]=True;d=distance(seed)
for z,x in np.ndindex(seed.shape):assert d[z,x]==min(abs(z-a)+abs(x-b) for a,b in np.argwhere(seed))
write_json(out/'validation/geometry-sampling.json',{'status':'PASS','sample_design_exact_match':len(expected),'global_gap_independent_bounded_pair_check':{'gap':best,'evaluated_pairs':pairs},'crossing_exact_supercover':segments,'corridor_edges':checks,'distance_brute_force_cells':143,'east_boundary_guard':True,'limitations':'edge and deterministic rebuild checks do not independently prove global least-cost optimality; Dijkstra nonnegative graph algorithm provides that within chosen cost model'})
print('geometry and sample checks PASS',flush=True)
