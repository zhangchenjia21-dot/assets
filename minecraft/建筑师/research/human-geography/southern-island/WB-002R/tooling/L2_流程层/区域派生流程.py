import json,sqlite3
import numpy as np
from L0_公理层.区域契约 import BOUNDS,SCHEMA
from L1_器件层.区域指标计算器 import load_observed,compute,summary,groups,distribution,numerical_zoning
from L1_器件层.源快照保护器 import write_json

def derive(out):
    a,biomes,states=load_observed(out/'raw-or-queryable/observed.sqlite');m=compute(a)
    island_id=int(m['land_component'][2056-BOUNDS[1],-248-BOUNDS[0]])
    if not island_id:raise ValueError('历史代表点当前为水，须模型重新指定主岛')
    island=m['land_component']==island_id;m['main_island']=island
    records={}
    for name in ('land_component','water_component','flat_component','gentle_component'):
        records[name]=[]
        for id,idx in groups(m[name]):
            obj=summary(idx,a,m,biomes);obj['id']=id;obj['main_island_columns']=int(island.ravel()[idx].sum());obj['uncertainty']='Operational current surface mask; ROI edges censored, vegetation filtering and local thresholds do not establish pristine origin, build suitability or navigability.';records[name].append(obj)
    info=summary(np.flatnonzero(island),a,m,biomes)
    x=a['x'][island].astype(float);y=a['exposed_y'][island].astype(float)
    corr=float(np.corrcoef(x,y)[0,1]);slope=float(np.dot(x-x.mean(),y-y.mean())/np.dot(x-x.mean(),x-x.mean()))
    bands=[]
    for lo in range(int(x.min())//128*128,int(x.max())+1,128):
        mask=island&(a['x']>=lo)&(a['x']<lo+128)
        if mask.any():bands.append({'x_bounds':[lo,lo+127],'columns':int(mask.sum()),'elevation':distribution(a['exposed_y'][mask])})
    ng2=out.parents[2]/'natural-geography/NG-2/raw-or-queryable/SITE-003-topology1.npz';old=np.load(ng2)
    comparison={key:int(np.count_nonzero(a[new]!=old[key])) for key,new in [('height','exposed_y'),('water_top','water_y'),('water_bottom','water_bottom'),('surface','surface_y')]}
    write_json(out/'profile/current-vs-NG2.json',{'column_differences':comparison,'note':'Region SHA may differ due to non-surface chunk data; compares actual surface fields, not biome numeric IDs'})
    write_json(out/'profile/regional-summary.json',{'schema':SCHEMA,'bounds':BOUNDS,'columns':int(a['x'].size),'main_island_component':island_id,'main_island':info,'main_island_topology':'4-neighbor dry surface columns at historical representative point; identity not redefined to match Owner impression','current_surface_origin':'possible natural or artificial intervention; no pristine-landscape claim'})
    write_json(out/'profile/biome-profile.json',{'main_island':info['biomes'],'roi':{biomes[int(k)]:int(v) for k,v in zip(*np.unique(a['filtered_biome'],return_counts=True))},'resolution':'1-block column lookup of native 4x4x4 biome cells at filtered surface Y; raw-top biome retained separately'})
    write_json(out/'profile/terrain-profile.json',{'main_island':info,'elevation_relief16':distribution(m['relief16'][island]),'elevation_relief64':distribution(m['relief64'][island]),'step1':distribution(m['step1'][island]),'slope8_valid_share':float(np.mean(np.isfinite(m['slope8'][island]))),'longitude_bands':bands,'pearson_x_elevation':corr,'OLS_Y_per_100_X':slope*100,'R_squared':corr*corr,'thresholds':{'LOW_RELIEF_FLAT':'land, relief32<=4, central8 slope<=0.125, max land neighbor step<=1','GENTLE_SLOPE':'land excluding flat, relief32<=8, slope<=0.25, step<=2','windows':'relief16/32/64 uses 17/33/65-square land-only max-min; slope8 central endpoints 16 blocks apart with 4 land endpoints; no interpolation','uncertainty':'water/ROI boundary can censor metrics; exact patch masks are operational morphology, not buildable land'}})
    write_json(out/'profile/vegetation-profile.json',{'main_island':info['vegetation'],'resolution':4,'vertical_scope':'all blocks strictly above filtered ground to raw WORLD_SURFACE at 4-block sample X/Z','semantics':'occupied sample fraction and blocks per sampled column, not tree counts or species ecology','dead_tree':'Owner visual interpretation pending block/biome evidence; logs alone cannot distinguish live/dead tree'})
    write_json(out/'profile/terrain-position-proxies.json',{'definitions':{'local_highland_proxy':'dry land Y>=72; local raised-ground proxy, not mountain classification','local_lowland_proxy':'dry land Y<=65; low-elevation proxy only','ridge_position_proxy':'dry land, relief64>=8 and height in upper20% of local 65x65 land-only min/max range; can include scarps, no verified ridge axis'},'main_island_counts':{k:int(m[k][island].sum()) for k in ('local_highland_proxy','local_lowland_proxy','ridge_position_proxy')},'uncertainty':'Fixed operational thresholds; no land use, ridge-route or regional boundary inference'})
    write_json(out/'profile/water-topology.json',{'land':records['land_component'],'water':records['water_component'],'main_island_id':island_id,'method':'4-neighbor dry land; water neighbors require actual vertical water intervals overlapping','flow_direction':'unknown','navigability':'unknown','ROI_boundary':'components touching ROI are censored, not confirmed independent islands/lakes'})
    (out/'profile/low-relief-components.jsonl').write_text(''.join(json.dumps(dict(o,id=('FLAT-' if name=='flat_component' else 'GENTLE-')+f'{o["id"]:05d}',class_name=name),sort_keys=True,ensure_ascii=False)+'\n' for name in ('flat_component','gentle_component') for o in records[name]),encoding='utf-8',newline='\n')
    alternatives,maps=numerical_zoning(a,m,island);write_json(out/'profile/zoning-alternatives.json',alternatives)
    np.savez_compressed(out/'raw-or-queryable/derived.npz',**m,**maps)
    print(json.dumps({'island':info,'correlation':corr,'trend_per100':slope*100,'components':{k:len(v) for k,v in records.items()},'surface_changes':comparison},ensure_ascii=True),flush=True)
