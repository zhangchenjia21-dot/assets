"""验证查询/成员/来源与确定性；与200+原始柱独立检查分别报告。"""
import ast,json,sqlite3,subprocess,sys
from pathlib import Path
import numpy as np
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tooling'))
from L3_外交层.区域公开接口 import query_profile
from L0_公理层.区域契约 import BOUNDS
from L1_器件层.源快照保护器 import write_json

def main():
    db=sqlite3.connect((ROOT/'raw-or-queryable/regional-profile.sqlite').as_uri()+'?mode=ro',uri=True)
    checks=[]
    def check(test,label):
        if not test:raise AssertionError(label)
        checks.append(label)
    check(db.execute('PRAGMA integrity_check').fetchone()[0]=='ok','SQLite integrity')
    check(db.execute('SELECT count(*) FROM samples').fetchone()[0]==1556480,'complete 1-block ROI coverage')
    check(db.execute('SELECT count(*) FROM vegetation').fetchone()[0]==97280,'4-block vegetation coverage')
    check(db.execute('SELECT count(*) FROM chunks').fetchone()[0]==6080,'all source chunks recorded')
    fresh=json.loads((ROOT/'manifest/freshness.json').read_text(encoding='utf-8'))
    check(set(r[0] for r in db.execute('SELECT DISTINCT region FROM chunks'))==set(fresh['relevant_regions']),'chunk -> region -> snapshot provenance')
    for p in sorted((ROOT/'profile').glob('*.json')):
        check(json.loads(db.execute('SELECT json FROM profiles WHERE name=?',(p.stem,)).fetchone()[0])==json.loads(p.read_text(encoding='utf-8')),'profile export '+p.name)
    for p in ('natural-zones.jsonl','low-relief-components.jsonl'):
        for obj in map(json.loads,(ROOT/'profile'/p).read_text(encoding='utf-8').splitlines()):
            check(json.loads(db.execute('SELECT json FROM objects WHERE id=?',(obj['id'],)).fetchone()[0])==obj,'object export '+obj['id'])
    m=np.load(ROOT/'raw-or-queryable/derived.npz');shape=m['main_island'].shape
    ids=set(r[0] for r in db.execute('SELECT id FROM objects'));check(all(r[0] in ids for r in db.execute('SELECT DISTINCT object_id FROM geometry_runs')),'no dangling geometry')
    for prefix,key in [('SIRZ','main_island'),('LAND','land_component'),('WATER','water_component'),('FLAT','flat_component'),('GENTLE','gentle_component')]:
        actual=np.zeros(shape,np.int32)
        for id,z,x0,x1 in db.execute('SELECT * FROM geometry_runs WHERE object_id LIKE ?',(prefix+'-%',)):
            zz=z-BOUNDS[1];a=x0-BOUNDS[0];b=x1-BOUNDS[0]+1
            check(not actual[zz,a:b].any(),'nonoverlap '+id+f' {z},{x0}')
            actual[zz,a:b]=int(id.split('-')[1])
        check(np.array_equal(actual,m[key]),'full member reconstruction '+prefix)
    # 直接方窗极值核对派生值；不复用生产filter。
    h=np.array(db.execute('SELECT exposed_y FROM samples ORDER BY z,x').fetchall(),dtype=np.int16).reshape(shape)
    rng=np.random.default_rng(22)
    for _ in range(100):
        z=int(rng.integers(32,shape[0]-32));x=int(rng.integers(32,shape[1]-32))
        if m['land_component'][z,x]:
            roi=np.s_[z-16:z+17,x-16:x+17];values=h[roi][m['land_component'][roi]>0]
            check(int(values.max()-values.min())==m['relief32'][z,x],'direct relief window '+str((x,z)))
    for x,z in [(-248,2056),(-800,1376),(415,2655),(-1,1700),(0,1700)]:
        r=query_profile(ROOT,'coordinate',x=x,z=z)['result'];p=r['point'];i=z-BOUNDS[1];j=x-BOUNDS[0]
        check(p['land_component']==int(m['land_component'][i,j]) and p['water_component']==int(m['water_component'][i,j]),'coordinate topology '+str((x,z)))
        check(p['zone']==('SIRZ-001' if m['main_island'][i,j] else None),'zone membership '+str((x,z)))
    for x,z in [(-801,1376),(416,2655),(-1,-1),(-6225,3500)]:check(query_profile(ROOT,'coordinate',x=x,z=z)['result']['coverage']=='OUTSIDE_STUDY_AREA','outside '+str((x,z)))
    for args in [('zone',{'id':'SIRZ-999'}),('context',{'x':0,'z':1700,'radius':-1})]:
        try:query_profile(ROOT,args[0],**args[1])
        except (ValueError,KeyError):check(True,'expected query error '+args[0])
        else:raise AssertionError('error not raised')
    cli=ROOT/'tooling/Bootstrap/区域命令.py'
    for args in [['coordinate','--x','-248','--z','2056'],['zone','--id','SIRZ-001'],['low-relief','--x','-248','--z','2056','--radius','16'],['context','--x','-248','--z','2056','--radius','16'],['hypotheses']]:
        outs=[subprocess.run([sys.executable,'-S',str(cli),*args],capture_output=True,check=True).stdout for _ in range(2)]
        check(outs[0]==outs[1] and json.loads(outs[0])['schema']=='southern-island-profile/1.0','standard-library deterministic CLI '+args[0])
    # 地形patch存在bbox内非成员，查询不能将这些间隙覆盖。
    gaps=0
    for id,raw in db.execute('SELECT id,json FROM objects WHERE id LIKE ? ORDER BY id',('FLAT-%',)):
        obj=json.loads(raw);x0,z0,x1,z1=obj['bounds'];label=int(id.split('-')[1]);region=m['flat_component'][z0-BOUNDS[1]:z1-BOUNDS[1]+1,x0-BOUNDS[0]:x1-BOUNDS[0]+1]
        if np.any(region!=label):gaps+=1
    check(gaps>0,'nonrectangular flat component bbox gaps present')
    witnesses=json.loads((ROOT/'profile/topology-witnesses.json').read_text(encoding='utf-8'))
    for route in witnesses['routes']:
        points=route['actual_path'];check(all(m['land_component'][z-BOUNDS[1],x-BOUNDS[0]]==route['component'] for x,z in points),'dry path witness')
        check(all(abs(x-a)+abs(z-b)==1 for (x,z),(a,b) in zip(points,points[1:])),'4-neighbor witness')
    for path in (ROOT/'tooling').rglob('*.py'):
        tree=ast.parse(path.read_text(encoding='utf-8'));level=next((int(p[1]) for p in path.parts if p.startswith(('L0_','L1_','L2_','L3_'))),None)
        for node in ast.walk(tree):
            if isinstance(node,ast.ImportFrom) and node.module and node.module.startswith(('L0_','L1_','L2_','L3_')) and level is not None:check(int(node.module[1])<=level,'downward dependency '+path.name)
    db.close();write_json(ROOT/'validation/automated.json',{'status':'PASS','assertions':len(checks),'checks_summary':['full column/component/zone reconstruction','all JSON exports equal SQLite','query CLI deterministic with python -S','source provenance','100 direct-window random samples','bbox gaps and actual land paths','syntax and downward dependencies'],'flat_components_with_bbox_gaps':gaps,'world_writes':0,'independent_raw_column_report':'raw-column-crosscheck.json (separate required validation)'});print('query/store validation PASS',len(checks),flush=True)
if __name__=='__main__':main()
