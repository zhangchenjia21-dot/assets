"""在动态完整矩形上重建指标；旧西岛和东山地主体均保留独立统计。"""
import json,sqlite3
import numpy as np
from L1_器件层 import 区域指标计算器 as metrics
from L1_器件层.源快照保护器 import write_json

def derive(out):
    scope=json.loads((out/'profile/scope-completion.json').read_text(encoding='utf-8'))
    bounds=scope['bounds'];metrics.BOUNDS=tuple(bounds)
    a,biomes,states=metrics.load_observed(out/'raw-or-queryable/observed.sqlite')
    m=metrics.compute(a);print('terrain computed',flush=True)
    west=int(m['land_component'][2056-bounds[1],-248-bounds[0]])
    east=int(m['land_component'][1800-bounds[1],400-bounds[0]])
    whole=m['land_component']>0
    m['whole_group']=whole;m['west']=m['land_component']==west;m['east']=m['land_component']==east
    records={}
    for name in ('land_component','water_component','flat_component','gentle_component'):
        records[name]=[]
        for id,idx in metrics.groups(m[name]):
            obj=metrics.summary(idx,a,m,biomes);obj['id']=id
            obj['whole_group_columns']=int(whole.ravel()[idx].sum());records[name].append(obj)
    stats={name:metrics.summary(np.flatnonzero(mask),a,m,biomes) for name,mask in [('whole_group',whole),('west',m['west']),('east',m['east']),('all_study_land',m['land_component']>0)]}
    write_json(out/'profile/regional-summary.json',{'bounds':bounds,'columns':int(whole.size),'scope_status':scope['status'],'west_component':west,'east_component':east,'statistics':stats,'whole_group_definition':'all dry land in complete study rectangle, including both major anchor components and every small satellite; water separately indexed','resolution':{'terrain':1,'biome':'native 4x4x4 cells queried at filtered surface per column','vegetation':4}})
    write_json(out/'profile/land-components.json',records['land_component'])
    write_json(out/'profile/water-topology.json',{'land':records['land_component'],'water':records['water_component'],'method':'4-neighbor land; water requires intersecting actual vertical intervals','flow_and_navigation':'unknown'})
    enclosure={}
    for name in ('west','east'):
        complement=metrics.components(~m[name]);edge=np.unique(np.r_[complement[0],complement[-1],complement[:,0],complement[:,-1]])
        inside=(complement>0)&~np.isin(complement,edge)&(m['water_component']>0)
        enclosure[name]={'internal_water_columns':int(inside.sum()),'water_component_ids':[int(v) for v in np.unique(m['water_component'][inside])],'method':'complement components not reaching study edge; surface enclosure only'}
    write_json(out/'profile/internal-water.json',enclosure)
    write_json(out/'profile/biome-profile.json',{'by_scope':{k:v['biomes'] for k,v in stats.items()},'whole_rectangle':{biomes[int(k)]:int(v) for k,v in zip(*np.unique(a['filtered_biome'],return_counts=True))}})
    write_json(out/'profile/vegetation-profile.json',{'by_scope':{k:v['vegetation'] for k,v in stats.items()},'resolution':4,'dead_tree':'not established by logs or dry ground vegetation; Owner visual interpretation','vertical_scope':'above filtered ground through raw top'})
    x=a['x'][whole].astype(float);y=a['exposed_y'][whole].astype(float)
    corr=float(np.corrcoef(x,y)[0,1]);slope=float(np.dot(x-x.mean(),y-y.mean())/np.dot(x-x.mean(),x-x.mean()))
    bands=[]
    for lo in range(int(x.min())//128*128,int(x.max())+1,128):
        mask=whole&(a['x']>=lo)&(a['x']<lo+128)
        if mask.any():bands.append({'x_bounds':[lo,lo+127],'columns':int(mask.sum()),'elevation':metrics.distribution(a['exposed_y'][mask]),'flat_share':float(np.mean(m['terrain_class'][mask]==1))})
    write_json(out/'profile/terrain-profile.json',{'by_scope':stats,'longitude_bands':bands,'pearson_x_elevation':corr,'OLS_Y_per_100_X':slope*100,'R_squared':corr*corr,'whole_relief64':metrics.distribution(m['relief64'][whole]),'whole_Y_ge100_share':float(np.mean(a['exposed_y'][whole]>=100)),'whole_relief32_ge16_share':float(np.mean(m['relief32'][whole]>=16)),'thresholds':{'flat':'dry, relief32<=4, slope8<=0.125, step1<=1','gentle':'dry excluding flat, relief32<=8, slope8<=0.25, step1<=2','relief':'17/33/65 square, land-only min/max','slope':'central endpoints16 apart, all four endpoints dry','high_elevation_proxy':'Y>=100, operational only; not mountain identity','low_elevation_proxy':'Y<=65','ridge_position_proxy':'relief64>=8 and upper20% local land heights'}})
    (out/'profile/low-relief-components.jsonl').write_text(''.join(json.dumps(dict(o,id=('FLAT-' if name=='flat_component' else 'GENTLE-')+f'{o["id"]:05d}',class_name=name),ensure_ascii=False,sort_keys=True)+'\n' for name in ('flat_component','gentle_component') for o in records[name]),encoding='utf-8')
    alternatives,maps=metrics.numerical_zoning(a,m,whole)
    write_json(out/'profile/zoning-alternatives.json',alternatives)
    np.savez_compressed(out/'raw-or-queryable/derived.npz',**m,**maps)
    print(json.dumps({'stats':stats,'correlation':corr,'trend':slope*100}),flush=True)
