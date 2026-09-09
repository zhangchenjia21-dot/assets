"""独立几何抽样、历史反例与命令契约验证；只写NG-3验证报告。"""
import ast, hashlib, json, math, random, sqlite3, subprocess, sys, tempfile
from pathlib import Path
import numpy as np

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tooling'))
from L3_外交层.图册公开接口 import query_atlas
from L1_器件层.图册存储器 import IdentityRegistry

def main():
    db = sqlite3.connect((ROOT/'raw-or-queryable/atlas.sqlite').as_uri()+'?mode=ro', uri=True)
    checks = []
    def check(condition, name):
        if not condition: raise AssertionError(name)
        checks.append(name)
    objects = {r[0]: json.loads(r[1]) for r in db.execute('SELECT id,details FROM atlas_objects')}
    check(db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok', 'SQLite integrity')
    check(len(objects)==67 and all(o['status']=='PROPOSED' and o['evidence_status'] in ('SUPPORTED','PROVISIONAL','UNRESOLVED') for o in objects.values()), '67 proposed objects with evidence status')
    for id in objects:
        check(db.execute('SELECT count(*) FROM lineage WHERE object_id=? AND source_kind != ?', (id,'algorithm')).fetchone()[0]>0, 'historical lineage '+id)
    exports = {o['id']:o for o in map(json.loads,(ROOT/'atlas/objects.jsonl').read_text(encoding='utf-8').splitlines())}
    check(all(exports[id]==query_atlas(ROOT,'object',id=id)['result'] for id in objects), 'all object exports match database and full lineage')
    rels = list(db.execute('SELECT source,target,kind FROM relations'))
    check(all(s in objects and t in objects for s,t,k in rels), 'no dangling relations')
    check(not any(k=='connected_to' for s,t,k in rels), 'no unsupported global water connection')
    check(all(o['flow_direction']=='unknown' for o in objects.values() if o['family']=='NHYD'), 'all hydrologic flow unknown')
    check(objects['NSITE-002']['type']=='mountain_front_gentle_apron_beside_river_lowland' and objects['NSITE-006']['type']=='connected_branching_channel_with_widened_reach', 'both NG2 reclassifications retained')
    check(objects['NFEAT-001']['type']=='local_rocky_ridge_saddle' and objects['NFEAT-004']['type']=='multi_opening_coastal_embayment', 'saddle and embayment limits retained')
    check(all(o['requires_world_write_authorization'] and o['requires_local_observation'] and o['planning_potential']=='terrain_observation_only' for o in objects.values() if o['family']=='NSITE'), 'NSITE is observation only')
    geometry = {}
    for gid,z0,z1,x0,x1 in db.execute('SELECT * FROM geometry_runs'): geometry.setdefault(gid,[]).append((x0,z0,x1,z1))
    def expected(x,z):
        return {id for id,o in objects.items() if any(a<=x<=c and b<=z<=d for a,b,c,d in geometry[o['geometry']['id']])}
    rng = random.Random(3003)
    points = [(rng.randint(-6224,3807),rng.randint(-6544,3487)) for _ in range(150)]
    points += [(-6224,-6544),(3807,3487),(-1,-1),(0,0),(-64,-64),(-65,-65),(1096,-1208),(-248,2056),(-5688,-1611)]
    for x,z in points:
        result=query_atlas(ROOT,'coordinate',x=x,z=z)['result']
        check({o['id'] for o in result['memberships']}==expected(x,z), f'coordinate members {x},{z}')
        check((result['cell_index']['gx'],result['cell_index']['gz'])==(x//64,z//64), f'floor cell {x},{z}')
    for x,z in [(-6225,-6544),(3808,3487),(0,3488),(0,-6545)]:
        r=query_atlas(ROOT,'coordinate',x=x,z=z)['result']
        check(r['coverage']=='OUTSIDE_SAMPLED_WORLD' and not r['memberships'] and r['cell_index'] is None,'outside extent '+str((x,z)))
    # 直接使用独立NG-2数组校验孔洞/水陆间隙，避免只验证同一份RLE的自洽性。
    ng2=ROOT.parent/'NG-2'
    for site,id,kind in [('SITE-003','NGEO-009','land'),('SITE-003','NHYD-019','water'),('SITE-019','NHYD-015','water'),('SITE-011','NHYD-020','water')]:
        assessment=json.loads((ng2/'assessments'/f'{site}.json').read_text(encoding='utf-8'))
        arrays=np.load(ng2/'raw-or-queryable'/f'{site}-topology1.npz')
        labels=arrays[kind+'_labels'];component=assessment['water_topology']['primary_'+kind]['component'];bounds=assessment['roi_bounds']
        mask=labels==component
        ys,xs=np.where(mask); bx0,bx1=int(xs.min()),int(xs.max());bz0,bz1=int(ys.min()),int(ys.max())
        cases=[(int(xs[i]),int(ys[i])) for i in np.linspace(0,len(xs)-1,30,dtype=int)]
        holes=np.argwhere(~mask[bz0:bz1+1,bx0:bx1+1])
        cases += [(int(p[1])+bx0,int(p[0])+bz0) for p in holes[::max(1,len(holes)//30)][:30]]
        for x,z in cases:
            hit=id in expected(x+bounds[0],z+bounds[1])
            check(hit==bool(mask[z,x]),f'NG2 independent mask {id} {x},{z}')
        check(len(holes)>0,'nonrectangular gaps verified '+id)
    for x,z,radius in [(-1,-1,0),(1096,-1208,128),(-248,2056,400),(4000,3500,250)]:
        wanted=set()
        for id,o in objects.items():
            if any((max(a-x,0,x-c)**2+max(b-z,0,z-d)**2)<=radius**2 for a,b,c,d in geometry[o['geometry']['id']]):wanted.add(id)
        r=query_atlas(ROOT,'context',x=x,z=z,radius=radius)['result']
        check({o['id'] for o in r['objects_within_radius']}==wanted,'context actual distance '+str((x,z,radius)))
        check(not r['world_write_authorized'] and not r['design_or_canon_generated'],'context authorization ceiling')
    cli=ROOT/'tooling/Bootstrap/图册命令.py'
    commands=[['coordinate','--x','-1','--z','-1'],['object','--id','NGEO-034'],['neighbors','--id','NGEO-009'],['search','--family','NHYD','--evidence-status','SUPPORTED'],['context','--x','1096','--z','-1208','--radius','128']]
    for args in commands:
        outputs=[subprocess.run([sys.executable,'-S',str(cli),*args],capture_output=True,check=True).stdout for _ in range(2)]
        check(outputs[0]==outputs[1] and json.loads(outputs[0])['schema_version']=='natural-atlas/1.0','stdlib-only deterministic CLI '+args[0])
    for args in [['object','--id','NGEO-999'],['context','--x','0','--z','0','--radius','-1']]:
        r=subprocess.run([sys.executable,'-S',str(cli),*args],capture_output=True)
        check(r.returncode==2 and 'error' in json.loads(r.stdout),'CLI expected error '+str(args))
    ledger=json.loads((ROOT/'atlas/id-registry.json').read_text(encoding='utf-8'))
    check(set(ledger)==set(objects) and len({v['stable_key'] for v in ledger.values()})==len(ledger),'unique IDs and stable keys')
    with tempfile.TemporaryDirectory() as temp:
        path=Path(temp)/'ledger.json';path.write_text(json.dumps({'NGEO-001':ledger['NGEO-001']}),encoding='utf-8')
        reg=IdentityRegistry(path);runs=[(b,d,a,c) for a,b,c,d in geometry[objects['NGEO-001']['geometry']['id']]]
        runs.sort()
        reg.bind('NGEO-001',ledger['NGEO-001']['stable_key'],runs)
        check(True,'same shape retains ID')
        for id,key,newruns in [('NGEO-001','changed',runs),('NGEO-001',ledger['NGEO-001']['stable_key'],[(0,0,0,0)]),('NGEO-002',ledger['NGEO-001']['stable_key'],runs)]:
            try:reg.bind(id,key,newruns)
            except ValueError:check(True,'ID drift rejected '+id+key)
            else:raise AssertionError('ID drift accepted')
        entry=dict(ledger['NGEO-001'],state='RETIRED');path.write_text(json.dumps({'NGEO-001':entry}),encoding='utf-8')
        try:IdentityRegistry(path).bind('NGEO-001',entry['stable_key'],runs)
        except ValueError:check(True,'retired ID cannot be recycled')
        else:raise AssertionError('retired ID reused')
    for path in (ROOT/'tooling').rglob('*.py'):
        tree=ast.parse(path.read_text(encoding='utf-8'))
        level=next((int(p[1]) for p in path.parts if p.startswith(('L0_','L1_','L2_','L3_'))),None)
        for node in ast.walk(tree):
            if isinstance(node,ast.ImportFrom) and node.module and node.module.startswith(('L0_','L1_','L2_','L3_')) and level is not None:
                check(int(node.module[1])<=level,'downward dependency '+path.name)
    store=ROOT/'raw-or-queryable/atlas.sqlite';manifest=json.loads((ROOT/'manifest/store.json').read_text(encoding='utf-8'))
    check(hashlib.sha256(store.read_bytes()).hexdigest()==manifest['sha256'],'store SHA256')
    db.close()
    report={'status':'PASS','checks':len(checks),'random_seed':3003,'random_points':150,'checked_contracts':checks,'world_writes':0}
    (ROOT/'validation').mkdir(exist_ok=True)
    (ROOT/'validation/automated.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':'PASS','checks':len(checks)}))

if __name__=='__main__':main()
