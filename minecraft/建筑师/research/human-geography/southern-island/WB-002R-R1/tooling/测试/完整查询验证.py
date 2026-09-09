"""用实际成员和独立 SQL 检查范围、来源、复用、查询与导出一致性。"""
import sys,json,sqlite3,subprocess,ast
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tooling'))
from L1_器件层.源快照保护器 import write_json

def validate():
    db=sqlite3.connect((ROOT/'raw-or-queryable/regional-profile.sqlite').as_uri()+'?mode=ro',uri=True)
    assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    scope=json.loads((ROOT/'profile/scope-completion.json').read_text(encoding='utf-8'));x0,z0,x1,z1=scope['bounds'];n=(x1-x0+1)*(z1-z0+1)
    assert db.execute('SELECT count(*) FROM samples').fetchone()[0]==n
    assert db.execute('SELECT count(*) FROM metrics').fetchone()[0]==n
    assert not db.execute('SELECT count(*) FROM samples s LEFT JOIN chunks c ON c.cx=CAST(floor(s.x/16.0) AS INTEGER) AND c.cz=CAST(floor(s.z/16.0) AS INTEGER) WHERE c.cx IS NULL').fetchone()[0]
    assert not db.execute('SELECT count(*) FROM chunks c LEFT JOIN source_regions r USING(region) WHERE r.region IS NULL').fetchone()[0]
    assert not db.execute('SELECT count(*) FROM geometry_runs g LEFT JOIN objects o ON o.id=g.object_id WHERE o.id IS NULL').fetchone()[0]
    assert not db.execute('SELECT count(*) FROM metrics m LEFT JOIN objects o ON o.id=m.zone WHERE m.zone IS NOT NULL AND o.id IS NULL').fetchone()[0]
    for raw, in db.execute("SELECT json FROM objects WHERE id LIKE 'SIRZ-R1-%'"):
        for water in json.loads(raw)['water_relation']['water_component_ids']:assert db.execute('SELECT 1 FROM objects WHERE id=?',(f'WATER-{water:05d}',)).fetchone()
    for p in (ROOT/'profile').glob('*.json'):assert db.execute('SELECT json FROM profiles WHERE name=?',(p.stem,)).fetchone()[0]==p.read_text(encoding='utf-8')
    for p in (ROOT/'profile').glob('*.jsonl'):
        for line in p.read_text(encoding='utf-8').splitlines():
            obj=json.loads(line);assert obj==json.loads(db.execute('SELECT json FROM objects WHERE id=?',(obj['id'],)).fetchone()[0])
    arrays=np.load(ROOT/'raw-or-queryable/derived.npz');reconstructed={}
    rng=np.random.default_rng(2003);window_checks=0
    for _ in range(100):
        x=int(rng.integers(x0+33,x1-33));z=int(rng.integers(z0+33,z1-33))
        rows=list(db.execute('SELECT x,z,exposed_y,water_y FROM samples WHERE z BETWEEN ? AND ? AND x BETWEEN ? AND ?',(z-32,z+32,x-32,x+32)))
        points={(a,b):(h,w) for a,b,h,w in rows};h,w=points[x,z]
        if w!=-32768:continue
        for span in (16,32,64):
            vals=[v for a,b,v,w in rows if w==-32768 and abs(a-x)<=span//2 and abs(b-z)<=span//2]
            assert max(vals)-min(vals)==int(arrays['relief'+str(span)][z-z0,x-x0])
        ends=[points[x-8,z],points[x+8,z],points[x,z-8],points[x,z+8]]
        got=arrays['slope8'][z-z0,x-x0]
        if all(w==-32768 for h,w in ends):assert np.isclose(got,np.hypot((ends[1][0]-ends[0][0])/16,(ends[3][0]-ends[2][0])/16))
        else:assert np.isnan(got)
        window_checks+=1
    for key,prefix in [('land_component','LAND'),('water_component','WATER'),('flat_component','FLAT'),('gentle_component','GENTLE'),('zones','SIRZ-R1')]:
        actual=arrays[key];rebuilt=np.zeros(actual.shape,np.int32)
        areas={}
        for id,z,a,b in db.execute('SELECT object_id,z,x0,x1 FROM geometry_runs WHERE object_id LIKE ? ORDER BY object_id,z,x0',(prefix+'-%',)):
            i=int(id.split('-')[-1]);assert x0<=a<=b<=x1 and z0<=z<=z1
            assert not rebuilt[z-z0,a-x0:b-x0+1].any();rebuilt[z-z0,a-x0:b-x0+1]=i;areas[id]=areas.get(id,0)+b-a+1
        assert np.array_equal(actual,rebuilt)
        for id,count in areas.items():assert json.loads(db.execute('SELECT json FROM objects WHERE id=?',(id,)).fetchone()[0])['area_blocks2']==count
        reconstructed[key]=len(areas)
    anchor=int(arrays['land_component'][1800-z0,400-x0]);mask=arrays['land_component']==anchor
    touches=bool(mask[0].any() or mask[-1].any() or mask[:,0].any() or mask[:,-1].any())
    assert touches==scope['east_mountain_landmass_touches_study_boundary'];assert not(scope['scope_complete'] and touches)
    land=arrays['land_component'];assert not (land[0].any() or land[-1].any() or land[:,0].any() or land[:,-1].any())
    evaluations=json.loads((ROOT/'profile/owner-hypothesis-evaluation.json').read_text(encoding='utf-8'))['whole_scope_evaluation']
    assert [v['id'] for v in evaluations]==['H-01','H-02','H-03','H-04','H-05']
    assert all(v['scope']['bounds']==scope['bounds'] for v in evaluations)
    terrain=json.loads((ROOT/'profile/terrain-profile.json').read_text(encoding='utf-8'))
    assert evaluations[2]['machine_observation']['pearson']==terrain['pearson_x_elevation']
    assert evaluations[1]['machine_observation']['whole_flat_share']==terrain['by_scope']['whole_group']['flat_share']
    old=ROOT.parent/'WB-002R/raw-or-queryable/observed.sqlite';db.execute('ATTACH DATABASE ? AS old',(old.as_uri()+'?mode=ro',))
    reuse=json.loads((ROOT/'manifest/reuse.json').read_text(encoding='utf-8'));assert not reuse['changed_regions']
    for table in ('samples','vegetation','vegetation_palette','chunks','states','biomes'):
        assert db.execute(f'SELECT count(*) FROM (SELECT * FROM old.{table} EXCEPT SELECT * FROM {table})').fetchone()[0]==0
    cases=[['coordinate','--x','-248','--z','2056'],['coordinate','--x','1500','--z','2300'],['coordinate','--x','99999','--z','99999'],['zone','--id','SIRZ-R1-001'],['low-relief','--x','400','--z','1800','--radius','0'],['hypotheses'],['context','--x','-248','--z','2056','--radius','0']]
    for args in cases:
        cmd=[sys.executable,'-S',str(ROOT/'tooling/Bootstrap/查询命令.py'),*args];one=subprocess.check_output(cmd);assert one==subprocess.check_output(cmd);json.loads(one)
    for args in [['zone','--id','SIRZ-R1-999'],['context','--x','0','--z','0','--radius','-1']]:assert subprocess.run([sys.executable,'-S',str(ROOT/'tooling/Bootstrap/查询命令.py'),*args],capture_output=True).returncode==2
    for p in (ROOT/'tooling').rglob('*.py'):
        tree=ast.parse(p.read_text(encoding='utf-8'));parts=p.relative_to(ROOT/'tooling').parts
        if parts[0].startswith('L'):
            level=int(parts[0][1])
            for node in ast.walk(tree):
                if isinstance(node,ast.ImportFrom) and node.module and node.module.startswith(('L0_','L1_','L2_','L3_')):assert int(node.module[1])<=level
    write_json(ROOT/'validation/automated.json',{'status':'PASS','columns':n,'geometry_layers':reconstructed,'source_provenance':'complete','old_observation_tables_preserved':True,'scope_hard_gate':True,'independent_land_window_checks':window_checks,'hypotheses_bound_to_full_scope':True,'stdlib_query_cases':len(cases),'error_cases':2,'profile_exports_equal':True,'architecture_downward_imports':True})
    print('full query validation PASS',flush=True)
if __name__=='__main__':validate()
