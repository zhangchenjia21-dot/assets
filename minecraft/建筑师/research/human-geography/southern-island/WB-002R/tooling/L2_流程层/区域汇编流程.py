"""从本轮冻结观测和显式解释组装查询库；成员不从bbox推断。"""
import json,sqlite3,shutil
import numpy as np
from L0_公理层.区域契约 import SCHEMA,BASE,material_category
from L1_器件层.区域指标计算器 import load_observed,summary,groups,runs
from L1_器件层.源快照保护器 import write_json,digest

def build(out):
    a,biomes,states=load_observed(out/'raw-or-queryable/observed.sqlite');m=dict(np.load(out/'raw-or-queryable/derived.npz'))
    decision=json.loads((out/'profile/zoning-decision.json').read_text(encoding='utf-8'));zones=m[decision['membership_source']].astype(np.int16)
    records=[]
    water_witness=json.loads((out/'profile/topology-witnesses.json').read_text(encoding='utf-8'))
    for id,indices in groups(zones):
        obj=summary(indices,a,m,biomes);obj.update({'id':f'SIRZ-{id:03d}','label':decision['labels'][id-1],'status':'RESEARCH_CANDIDATE','boundary_confidence':decision['boundary_confidence'],'transition_limitations':decision['transition_limitations'],'discrete_internal_zoning_established':False,'lineage':['NGEO-009','NFEAT-003','NHYD-019','current observed.sqlite samples/chunks -> manifest/current-source-before.json'],'geometry_semantics':'actual current main-island dry column mask; one reference unit, not uniform terrain or political boundary'})
        records.append(obj)
        obj['water_relationship']={k:water_witness[k] for k in ('main_internal_water_components','internal_water_columns','exterior_water_components')}
    (out/'profile/natural-zones.jsonl').write_text(''.join(json.dumps(o,ensure_ascii=False,sort_keys=True)+'\n' for o in records),encoding='utf-8',newline='\n')
    target=out/'raw-or-queryable/regional-profile-building.sqlite'
    if target.exists():raise ValueError('unfinished build exists')
    # 观测库是本任务独立快照；复制它保留原始事实，派生表单独建在最终查询库。
    shutil.copyfile(out/'raw-or-queryable/observed.sqlite',target);db=sqlite3.connect(target)
    # 原读取器派生版本可能带历史兼容空表；只移除本任务副本中的空外围表。
    for table in ('profiles','target_samples','targets','assessments'):
        if db.execute('SELECT 1 FROM sqlite_master WHERE type=? AND name=?',('table',table)).fetchone():
            if db.execute('SELECT count(*) FROM '+table).fetchone()[0]:raise ValueError('unexpected nonempty legacy table '+table)
            db.execute('DROP TABLE '+table)
    db.executescript('''CREATE TABLE metrics(x INTEGER,z INTEGER,slope8 REAL,step1 INTEGER,relief16 INTEGER,relief32 INTEGER,relief64 INTEGER,land_component INTEGER,water_component INTEGER,terrain_class INTEGER,flat_component INTEGER,gentle_component INTEGER,shoreline INTEGER,local_highland_proxy INTEGER,local_lowland_proxy INTEGER,ridge_position_proxy INTEGER,zone TEXT,PRIMARY KEY(z,x)) WITHOUT ROWID;
    CREATE TABLE objects(id TEXT PRIMARY KEY,json TEXT);
    CREATE TABLE geometry_runs(object_id TEXT,z INTEGER,x0 INTEGER,x1 INTEGER,PRIMARY KEY(object_id,z,x0)) WITHOUT ROWID;
    CREATE TABLE profiles(name TEXT PRIMARY KEY,json TEXT);
    CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT);
    CREATE TABLE material_categories(state_id INTEGER PRIMARY KEY,category TEXT);
    CREATE TABLE source_regions(region TEXT PRIMARY KEY,sha256 TEXT,size INTEGER,mtime_ns INTEGER);''')
    db.executemany('INSERT INTO material_categories VALUES (?,?)',[(id,material_category(s['Name'])) for id,s in sorted(states.items())])
    freshness=json.loads((out/'manifest/freshness.json').read_text(encoding='utf-8'))
    db.executemany('INSERT INTO source_regions VALUES (?,?,?,?)',[(p,freshness['current_overworld_inventory'][p]['sha256'],freshness['current_overworld_inventory'][p]['size'],freshness['current_overworld_inventory'][p]['mtime_ns']) for p in freshness['relevant_regions']])
    fields=('slope8','step1','relief16','relief32','relief64','land_component','water_component','terrain_class','flat_component','gentle_component','shoreline','local_highland_proxy','local_lowland_proxy','ridge_position_proxy')
    for z in range(a['x'].shape[0]):
        rows=[]
        for x in range(a['x'].shape[1]):
            values=[float(m[k][z,x]) if k=='slope8' and np.isfinite(m[k][z,x]) else None if k=='slope8' else int(m[k][z,x]) for k in fields]
            rows.append((int(a['x'][z,x]),int(a['z'][z,x]),*values,f'SIRZ-{zones[z,x]:03d}' if zones[z,x] else None))
        db.executemany('INSERT INTO metrics VALUES ('+','.join('?'*17)+')',rows)
    for path in sorted((out/'profile').glob('*.json')):db.execute('INSERT INTO profiles VALUES (?,?)',(path.stem,path.read_text(encoding='utf-8')))
    objects=list(records)
    objects += [json.loads(line) for line in (out/'profile/low-relief-components.jsonl').read_text(encoding='utf-8').splitlines()]
    topo=json.loads((out/'profile/water-topology.json').read_text(encoding='utf-8'))
    for family,key in [('LAND','land'),('WATER','water')]:objects += [dict(o,id=f'{family}-{o["id"]:05d}',geometry_semantics='actual 1-block component; ROI-edge components censored') for o in topo[key]]
    for obj in sorted(objects,key=lambda o:o['id']):db.execute('INSERT INTO objects VALUES (?,?)',(obj['id'],json.dumps(obj,ensure_ascii=False,sort_keys=True)))
    for labels,prefix,digits in [(zones,'SIRZ',3),(m['flat_component'],'FLAT',5),(m['gentle_component'],'GENTLE',5),(m['land_component'],'LAND',5),(m['water_component'],'WATER',5)]:
        db.executemany('INSERT INTO geometry_runs VALUES (?,?,?,?)',[(f'{prefix}-{id:0{digits}d}',z,x0,x1) for id,z,x0,x1 in runs(labels)])
    db.execute('INSERT INTO meta VALUES (?,?)',('schema',SCHEMA));db.execute('INSERT INTO meta VALUES (?,?)',('execution_base',BASE))
    db.execute('INSERT INTO meta VALUES (?,?)',('snapshot',json.dumps({k:freshness[k] for k in ('checked_at','regional_snapshot_status','bounds')} ,sort_keys=True)))
    db.commit();assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok';db.close();target.replace(out/'raw-or-queryable/regional-profile.sqlite')
    write_json(out/'manifest/profile.json',{'schema':SCHEMA,'base':BASE,'columns':int(a['x'].size),'source_chunks':6080,'vegetation_sampling':4,'source_resolution':1,'research_units':len(records),'discrete_internal_zones':0,'world_writes':0,'observed_sha256':digest(out/'raw-or-queryable/observed.sqlite')})
    print('regional SQLite built',flush=True)
