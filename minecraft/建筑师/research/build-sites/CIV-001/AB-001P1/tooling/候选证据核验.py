"""以SQLite逐行和坐标查询独立复核派生范围及关键见证；不读写Minecraft方块。"""
import sys,json,sqlite3,statistics,subprocess
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
import numpy as np
sys.dont_write_bytecode=True
from 源快照保护器 import digest,write_json
out=Path(__file__).resolve().parents[1];project=out.parents[3];r1=project/'research/human-geography/southern-island/WB-002R-R1';wb=project/'research/human-geography/southern-island/WB-003R';cache=Path('D:/Games/Minecraft/AI工程/研究缓存/建筑师/AB-001P1')
core=['site-candidates.json','review/surface-witnesses.json','visual/site-candidates.png']+[f'geometry/{c}-{kind}-runs.json' for c in ('A','B') for kind in ('land','flat-patch')]
if len(sys.argv)>1 and sys.argv[1]=='snapshot':
    write_json(cache/'rebuild-before.json',{p:digest(out/p) for p in core});print('rebuild hashes saved');sys.exit(0)
db=sqlite3.connect((r1/'raw-or-queryable/observed.sqlite').as_uri()+'?mode=ro',uri=True);db.row_factory=sqlite3.Row
fresh=json.loads((out/'validation/freshness.json').read_text(encoding='utf-8'));assert fresh['status']=='CURRENT_MATCH'
profile=json.loads((out/'site-candidates.json').read_text(encoding='utf-8'));witnesses=[];results=[]
with np.load(r1/'raw-or-queryable/derived.npz') as npz:land=npz['land_component'];terrain=npz['terrain_class']
def witness(x,z,role):
    row=dict(db.execute('SELECT * FROM samples WHERE x=? AND z=?',(x,z)).fetchone());region=f'dimensions/minecraft/overworld/region/r.{x//512}.{z//512}.mca'
    row['exposed_block']=json.loads(db.execute('SELECT json FROM states WHERE id=?',(row['exposed_state'],)).fetchone()[0])['Name'];row.update(role=role,parent_component=int(land[z-1376,x+800]),source_region=region,source_sha256=fresh['relevant_regions'][region]['sha256']);witnesses.append(row);return row
for c in profile['candidates']:
    runs=json.loads((out/c['geometry']).read_text(encoding='utf-8'))['runs'];ys=[];palette=Counter();flags=0;used=set()
    for z,x0,x1 in runs:
        assert x0<=x1
        for row in db.execute('SELECT x,exposed_y,exposed_state,artificial_material FROM samples WHERE z=? AND x BETWEEN ? AND ? ORDER BY x',(z,x0,x1)):
            x,y,s,flag=row;assert (x,z) not in used;used.add((x,z));assert land[z-1376,x+800]==c['parent'];ys.append(y);palette[s]+=1;flags+=int(flag>0)
    assert len(ys)==c['land_columns'];assert min(ys)==c['terrain']['elevation']['min'] and statistics.median(ys)==c['terrain']['elevation']['median'] and max(ys)==c['terrain']['elevation']['max'];assert flags==c['existing_surface']['artificial_material_flag_columns']
    merged=Counter()
    for s,n in palette.items():merged[json.loads(db.execute('SELECT json FROM states WHERE id=?',(s,)).fetchone()[0])['Name']]+=n
    assert dict(merged)==c['existing_surface']['surface_palette']
    for edge in c['parent_continuations']:
        for k in ('inside','outside'):
            x,z=edge[k];row=witness(x,z,c['id']+' continuation '+k);assert row['parent_component']==c['parent']
    for shore in c['shore_water']['witnesses']:
        for k in ('land','water'):
            x,z,y=shore[k];row=witness(x,z,c['id']+' shore '+k);assert row['exposed_y' if k=='land' else 'water_y']==y
    x0,z0,x1,z1=c['terrain']['largest_all_flat_square']['bounds'];assert all((x,z) in used and terrain[z-1376,x+800]==1 for z in range(z0,z1+1) for x in range(x0,x1+1))
    for x,z in ((x0,z0),(x1,z1)):witness(x,z,c['id']+' flat diagnostic corner')
    for ray in c['views']['rays']:
        x,z,y=ray['horizon_sample_xzy'];row=witness(x,z,c['id']+' terrain horizon '+ray['direction']);assert max(row['exposed_y'],row['water_y'])==y
    results.append({'candidate':c['id'],'raw_sql_columns_checked':len(ys),'elevation_material_flags_match':True,'parent_membership':True,'flat_square_members':(x1-x0+1)*(z1-z0+1)})
surface=json.loads((out/'review/surface-witnesses.json').read_text(encoding='utf-8'))['witnesses']
for w in surface:
    row=witness(w['x'],w['z'],w['candidate']+' surface signal');assert row['exposed_block']==w['block'] and row['exposed_y']==w['y']
cross=json.loads((wb/'profile/crossing-profile.json').read_text(encoding='utf-8'))['candidates'][0]
for name,candidate in [('west','B'),('east','A')]:
    end=cross[name];c=next(c for c in profile['candidates'] if c['id']==candidate);x,z=end['x'],end['z'];lo,top,hi,bottom=c['window'];assert lo<=x<=hi and top<=z<=bottom and land[z-1376,x+800]==c['parent']
write_json(out/'review/key-witnesses.json',{'coordinate_order':'named x,z,exposed_y fields; observation points, not selected site','witnesses':witnesses})
write_json(out/'validation/independent-check.json',{'status':'PASS','checks':results,'key_coordinate_witnesses':len(witnesses),'X00_endpoints_membership':'west in B; east in A','no_new_world_block_read':True,'limits':'independent SQLite aggregation checks candidate derivation; predecessor topology itself is reused accepted evidence, not independently rescanned'})
before=json.loads((cache/'rebuild-before.json').read_text(encoding='utf-8'));checks={p:before[p]==digest(out/p) for p in core};assert all(checks.values())
write_json(out/'validation/rebuild.json',{'status':'PASS','method':'fresh process candidate compilation from same readonly R1 cache; SHA256 before/after','artifacts':{p:{'sha256':digest(out/p),'byte_identical':checks[p]} for p in core},'interpretation':'manual mapping verdict excluded from automatic regeneration'})
inputs=[r1/'raw-or-queryable/observed.sqlite',r1/'raw-or-queryable/derived.npz',r1/'profile/land-components.json',wb/'profile/crossing-profile.json']
write_json(out/'validation/lineage.json',{'execution_base':'55ef954e96bafaa9eb938d6e62614e5cef43b331','accepted_research':{'WB-002R-R1':'5c6bffe8efbb0a5b0f53d8dfe036e012294b9c96','WB-003R':'ff84715a261139cc035094d44498e942e317cf54'},'inputs':[{'path':p.relative_to(project).as_posix(),'sha256':digest(p),'bytes':p.stat().st_size,'copied_raw':False} for p in inputs],'source_epoch':fresh['source_epoch'],'raw_cache':{'cache_id':'AB001P1-SOURCE-BEFORE','status':'LOCAL_ONLY','retention':'PRESERVE_LOCAL','schema':'named root -> relative file -> sha256,size,mtime_ns','sha256':digest(cache/'source-before.json'),'bytes':(cache/'source-before.json').stat().st_size,'source_world_fingerprint':fresh['source_epoch'],'source_epoch':fresh['checked_at'],'generated_at':datetime.fromtimestamp((cache/'source-before.json').stat().st_mtime,timezone.utc).isoformat(),'rebuild_command':'historical before inventory must be preserved; only new task baseline may use 源证据核验.py init','local_path_hint':str(cache/'source-before.json')},'new_world_block_reads':0,'broad_rescan':False})
write_json(out/'review/index.json',{'verdict':'OWNER_SELECTION_REQUIRED','status':'AWAITING INDEPENDENT REVIEW / OWNER MAPPING CONFIRMATION','read_order':['site-mapping.json','visual/site-candidates.png','reports/中心岛SiteGate.md','site-candidates.json','review/key-witnesses.json','review/surface-witnesses.json','validation/freshness.json','validation/lineage.json','validation/geometry-check.json','validation/independent-check.json','validation/rebuild.json','validation/source-audit.json','validation/payload.json'],'scope_stop':'no selected site, no architecture plan, no world write'})
db.close();print('independent candidate checks PASS',len(witnesses),flush=True)
