"""将完整观测、显式研究区成员及指标汇编为标准库可查询存储。"""
import json,sqlite3,shutil
import numpy as np
from L1_器件层 import 区域指标计算器 as metrics
from L0_公理层.区域契约 import material_category,SCHEMA,BASE
from L1_器件层.源快照保护器 import write_json,digest

def build(out):
    scope=json.loads((out/'profile/scope-completion.json').read_text(encoding='utf-8'));metrics.BOUNDS=tuple(scope['bounds'])
    a,biomes,states=metrics.load_observed(out/'raw-or-queryable/observed.sqlite');m=dict(np.load(out/'raw-or-queryable/derived.npz'))
    decision=json.loads((out/'profile/zoning-decision.json').read_text(encoding='utf-8'))
    internal=json.loads((out/'profile/internal-water.json').read_text(encoding='utf-8'))
    zones=np.zeros(a['x'].shape,np.int16)
    records=[]
    for i,unit in enumerate(decision['units'],1):
        mask=m[unit['mask']].astype(bool);assert not np.any(zones[mask]);zones[mask]=i
        obj=metrics.summary(np.flatnonzero(mask),a,m,biomes)
        obj.update(unit);obj.update(id=f'SIRZ-R1-{i:03d}',status='NOT_WORLD_CANON',geometry='actual member RLE in geometry_runs',water_relation=internal[unit['mask']])
        records.append(obj)
    m['zones']=zones;np.savez_compressed(out/'raw-or-queryable/derived.npz',**m)
    (out/'profile/natural-zones.jsonl').write_text(''.join(json.dumps(o,ensure_ascii=False,sort_keys=True)+'\n' for o in records),encoding='utf-8')
    target=out/'raw-or-queryable/regional-profile-building.sqlite';assert not target.exists()
    shutil.copyfile(out/'raw-or-queryable/observed.sqlite',target);db=sqlite3.connect(target)
    for table in ('profiles','target_samples','targets','assessments'):
        if db.execute('SELECT 1 FROM sqlite_master WHERE type=? AND name=?',('table',table)).fetchone():
            assert not db.execute('SELECT count(*) FROM '+table).fetchone()[0];db.execute('DROP TABLE '+table)
    fields=('slope8','step1','relief16','relief32','relief64','land_component','water_component','terrain_class','flat_component','gentle_component','shoreline','local_highland_proxy','local_lowland_proxy','ridge_position_proxy')
    db.executescript('CREATE TABLE metrics(x INTEGER,z INTEGER,'+','.join(k+(' REAL' if k=='slope8' else ' INTEGER') for k in fields)+',zone TEXT,PRIMARY KEY(z,x)) WITHOUT ROWID; CREATE TABLE objects(id TEXT PRIMARY KEY,json TEXT); CREATE TABLE geometry_runs(object_id TEXT,z INTEGER,x0 INTEGER,x1 INTEGER,PRIMARY KEY(object_id,z,x0)) WITHOUT ROWID; CREATE TABLE profiles(name TEXT PRIMARY KEY,json TEXT); CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT); CREATE TABLE material_categories(state_id INTEGER PRIMARY KEY,category TEXT); CREATE TABLE source_regions(region TEXT PRIMARY KEY,sha256 TEXT,size INTEGER,mtime_ns INTEGER);')
    db.executemany('INSERT INTO material_categories VALUES (?,?)',[(i,material_category(s['Name'])) for i,s in sorted(states.items())])
    source=json.loads((out/'manifest/source-before.json').read_text(encoding='utf-8'))['world']
    db.executemany('INSERT INTO source_regions VALUES (?,?,?,?)',[(p,source[p]['sha256'],source[p]['size'],source[p]['mtime_ns']) for p in scope['relevant_region_hashes']])
    for z in range(zones.shape[0]):
        rows=[]
        for x in range(zones.shape[1]):
            values=[float(m[k][z,x]) if k=='slope8' and np.isfinite(m[k][z,x]) else None if k=='slope8' else int(m[k][z,x]) for k in fields]
            rows.append((int(a['x'][z,x]),int(a['z'][z,x]),*values,f'SIRZ-R1-{zones[z,x]:03d}' if zones[z,x] else None))
        db.executemany('INSERT INTO metrics VALUES ('+','.join('?'*17)+')',rows)
    for path in sorted((out/'profile').glob('*.json')):db.execute('INSERT INTO profiles VALUES (?,?)',(path.stem,path.read_text(encoding='utf-8')))
    objects=records+[json.loads(s) for s in (out/'profile/low-relief-components.jsonl').read_text(encoding='utf-8').splitlines()]
    topo=json.loads((out/'profile/water-topology.json').read_text(encoding='utf-8'))
    for prefix,key in [('LAND','land'),('WATER','water')]:objects += [dict(o,id=f'{prefix}-{o["id"]:05d}') for o in topo[key]]
    for o in sorted(objects,key=lambda o:o['id']):db.execute('INSERT INTO objects VALUES (?,?)',(o['id'],json.dumps(o,ensure_ascii=False,sort_keys=True)))
    for labels,prefix,digits in [(zones,'SIRZ-R1',3),(m['flat_component'],'FLAT',5),(m['gentle_component'],'GENTLE',5),(m['land_component'],'LAND',5),(m['water_component'],'WATER',5)]:
        db.executemany('INSERT INTO geometry_runs VALUES (?,?,?,?)',((f'{prefix}-{i:0{digits}d}',z,x0,x1) for i,z,x0,x1 in metrics.runs(labels)))
    db.executemany('INSERT INTO meta VALUES (?,?)',[('schema',SCHEMA),('execution_base',BASE),('scope',json.dumps(scope,sort_keys=True))]);db.commit()
    assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok';db.close();target.replace(out/'raw-or-queryable/regional-profile.sqlite')
    write_json(out/'manifest/profile.json',{'schema':SCHEMA,'base':BASE,'columns':int(zones.size),'world_writes':0,'observed_sha256':digest(out/'raw-or-queryable/observed.sqlite'),'scope_status':scope['status']})
    print('query store built',flush=True)
