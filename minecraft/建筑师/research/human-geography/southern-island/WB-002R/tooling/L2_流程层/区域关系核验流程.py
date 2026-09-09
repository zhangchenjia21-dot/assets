"""用实际成员路径和内外补集解释岛片；路径只证明表层拓扑，不证明角色通行。"""
import json,sqlite3
from collections import deque
import numpy as np
from L0_公理层.区域契约 import BOUNDS
from L1_器件层.区域指标计算器 import load_observed,components,summary,distribution
from L1_器件层.源快照保护器 import write_json

def analyze(out):
    a,biomes,states=load_observed(out/'raw-or-queryable/observed.sqlite');m=dict(np.load(out/'raw-or-queryable/derived.npz'));main=m['main_island'];ll=m['land_component'];wl=m['water_component']
    complement=components(~main);edge=np.unique(np.r_[complement[0],complement[-1],complement[:,0],complement[:,-1]]);interior=(~main)&~np.isin(complement,edge)
    outer_water_ids=sorted(int(i) for i in np.unique(wl[~main&~interior]) if i)
    ponds=sorted(int(i) for i in np.unique(wl[interior]) if i)
    routes=[]
    def path(requested_start,requested_end,component):
        mask=ll==component;zz,xx=np.where(mask)
        def nearest(p):
            i=np.argmin((xx+BOUNDS[0]-p[0])**2+(zz+BOUNDS[1]-p[1])**2);return int(zz[i]),int(xx[i])
        start=nearest(requested_start);end=nearest(requested_end);q=deque([start]);parent={start:None}
        while q:
            z,x=q.popleft()
            if (z,x)==end:break
            for p in ((z-1,x),(z+1,x),(z,x-1),(z,x+1)):
                if 0<=p[0]<mask.shape[0] and 0<=p[1]<mask.shape[1] and mask[p] and p not in parent:parent[p]=(z,x);q.append(p)
        assert end in parent
        points=[];p=end
        while p is not None:points.append([p[1]+BOUNDS[0],p[0]+BOUNDS[1]]);p=parent[p]
        return {'requested_anchors':[requested_start,requested_end],'component':component,'actual_path':points[::-1],'land_columns':len(points),'meaning':'surface 4-neighbor land witness only; no slope, headroom or navigation assertion'}
    routes.append(path([-200,1550],[-248,2056],int(ll[2056-BOUNDS[1],-248-BOUNDS[0]])))
    routes.append(path([-50,1800],[400,1800],2))
    midpoint=(int(a['x'][main].min())+int(a['x'][main].max()))/2
    halves={name:summary(np.flatnonzero(main&mask),a,m,biomes) for name,mask in [('west',a['x']<=midpoint),('east',a['x']>midpoint)]}
    sensitivity=[]
    for relief,slope in [(2,.125),(4,.125),(6,.1875),(8,.25)]:
        good=main&(m['relief32']<=relief)&(m['slope8']<=slope)&(m['step1']<=1)
        sensitivity.append({'relief32_max':relief,'slope8_max':slope,'max_step1':1,'main_island_share':float(good.sum()/main.sum())})
    db=sqlite3.connect((out/'raw-or-queryable/observed.sqlite').as_uri()+'?mode=ro',uri=True)
    palette=dict(db.execute('SELECT name,sum(count) FROM vegetation_palette GROUP BY name ORDER BY name'))
    material={states[int(k)]['Name']:int(v) for k,v in zip(*np.unique(a['exposed_state'][main],return_counts=True))}
    # 同名多种Properties的状态需要归并，否则会静默覆盖面积。
    material={}
    for k,v in zip(*np.unique(a['exposed_state'][main],return_counts=True)):
        name=states[int(k)]['Name'];material[name]=material.get(name,0)+int(v)
    db.close()
    write_json(out/'profile/surface-materials.json',{'main_island_filtered_materials':material,'vegetation_palette_sampled_ROI':palette,'semantics':'observed block names/properties only; dirt_path or logs do not establish player origin or dead-tree ecology'})
    write_json(out/'profile/topology-witnesses.json',{'main_internal_water_components':ponds,'internal_water_columns':int((interior&(wl>0)).sum()),'exterior_water_components':outer_water_ids,'routes':routes,'western_piece_interpretation':'north and south lobes are one C-shaped island; central separate-looking lobe is connected to eastern ROI-edge body','Owner_referents':'No Owner coordinates supplied; these are explicit map-based candidate referents, not certain identification of their viewpoint'})
    write_json(out/'profile/west-east-comparison.json',{'split_X':midpoint,'halves':halves,'flat_threshold_sensitivity':sensitivity,'eastern_context':summary(np.flatnonzero(ll==2),a,m,biomes),'context_scope':'eastern component touches ROI; not surveyed as a complete island'})
    print(json.dumps({'internal_water_components':len(ponds),'internal_water_columns':int((interior&(wl>0)).sum()),'routes':[r['land_columns'] for r in routes],'flat_threshold_sensitivity':sensitivity}),flush=True)
