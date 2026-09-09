"""只从已采集数据库生成证据；地貌解释由独立assessment记录，不由阈值自动命名。"""
import json
from collections import Counter
import numpy as np
from L1_器件层.区块柱读取器 import connect
from L1_器件层.局部指标计算器 import metrics,topology
from L1_器件层.源文件保护器 import write_json
from L1_器件层.局部图生成器 import render,detail_views

def derive(out):
    db=connect(out/'raw-or-queryable/refinement.sqlite')
    configs=json.loads((out/'manifest/roi-plan.json').read_text(encoding='utf-8'))
    records={id:json.loads(raw) for id,raw in db.execute('SELECT id,json FROM targets')}
    targets={id:r['v1'] for id,r in records.items()}
    for id,config in configs.items():
        p=targets[id]['representative'];b=config['bounds']
        old=json.loads((out/'assessments'/f'{id}-metrics.json').read_text(encoding='utf-8'))
        result=metrics(db,id,config,p,out)
        result['water_topology']=topology(db,id,config,p,out) if config.get('topology') else old['water_topology']
        if 'critical_depression_test' in old:result['critical_depression_test']=old['critical_depression_test']
        entities=[]
        for raw, in db.execute('SELECT block_entities FROM chunks WHERE cx BETWEEN ? AND ? AND cz BETWEEN ? AND ?',(b[0]//16,b[2]//16,b[1]//16,b[3]//16)):
            entities.extend(e for e in json.loads(raw) if b[0]<=e['x']<=b[2] and b[1]<=e['z']<=b[3])
        notable=[]
        for e in entities:
            if e['id'] in ('minecraft:sculk_sensor','minecraft:sculk_shrieker','minecraft:sculk_catalyst'):continue
            h=db.execute('SELECT exposed_y FROM samples WHERE x=? AND z=?',(e['x'],e['z'])).fetchone()
            if h and e['y']>=h[0]-8:notable.append(dict(e,observed_exposed_y=h[0]))
            elif e['id'].startswith('waystones:'):notable.append(dict(e,observed_exposed_y=h[0] if h else None))
        result['material_context']={'meaning':'candidate materials and block entities are observations, not human-origin attribution','block_entity_counts':dict(Counter(e['id'] for e in entities)),'near_surface_or_waystone_entities':notable,'surface_candidate_states':[{'state':json.loads(raw),'count':n} for raw,n in db.execute('SELECT st.json,count(*) FROM samples s JOIN target_samples t USING(x,z) JOIN states st ON st.id=s.surface_state WHERE target=? AND artificial_material=1 GROUP BY st.id',(id,))]}
        result['observed_extrema']={}
        for order in ('ASC','DESC'):
            r=db.execute('SELECT s.x,s.exposed_y,s.z FROM samples s JOIN target_samples t USING(x,z) WHERE target=? ORDER BY exposed_y '+order+' LIMIT 1',(id,)).fetchone()
            result['observed_extrema']['min' if order=='ASC' else 'max']=list(r)
        result['profiles']={name:{'columns':n,'min_y':lo,'max_y':hi,'length_blocks':dist,'resolution':'1 block along axial profiles; sqrt(2) horizontal distance along diagonal profiles'} for name,n,lo,hi,dist in db.execute('SELECT name,count(*),min(elevation),max(elevation),max(distance) FROM profiles WHERE target=? GROUP BY name',(id,))}
        if config.get('topology'):
            a=np.load(out/'raw-or-queryable'/f'{id}-topology1.npz');label=result['water_topology']['primary_water']['component'];mask=a['water_labels']==label
            sections=[]
            # 固定坐标断面保存所有连续水段；宽度是轴向柱数，不冒充法向最窄口宽。
            for axis,coords in [('z',[-4300,-4200,-4100,-4000,-3900,-3800,-3700] if id=='SITE-011' else []),('x',[-256,0,255,256,512,1096] if id=='SITE-019' else [])]:
                for c in coords:
                    if axis=='z' and b[1]<=c<=b[3]:line=mask[c-b[1],:];origin=b[0]
                    elif axis=='x' and b[0]<=c<=b[2]:line=mask[:,c-b[0]];origin=b[1]
                    else:continue
                    starts=np.flatnonzero(np.diff(np.r_[False,line,False].astype(int))==1);ends=np.flatnonzero(np.diff(np.r_[False,line,False].astype(int))==-1)-1
                    sections.append({'fixed_axis':axis,'coordinate':c,'water_runs':[{'from':int(origin+s),'to':int(origin+e),'width_columns':int(e-s+1)} for s,e in zip(starts,ends)]})
            result['water_sections']=sections
        write_json(out/'assessments'/f'{id}-metrics.json',result)
        print(id+' derived metrics complete',flush=True)
    render(db,out,configs,targets);detail_views(db,out,configs,targets)
    db.close()
