"""校验当前提案表达、原始证据及归档一致性；不裁决规划质量。

世界仅计算已知三文件SHA256；地图重建无需存档读取。
"""
from pathlib import Path
import hashlib,json,gzip,subprocess,sys,datetime,contextlib,io,runpy
R=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
tracked_before={p.relative_to(R).as_posix():sha(p) for p in list((R/'maps').glob('*.png'))+[R/'planning-data.json']}
with contextlib.redirect_stdout(io.StringIO()):ns=runpy.run_path(str(R/'街区规划与制图.py'))
assert tracked_before=={key:sha(R/key) for key in tracked_before},'Rebuild differs'
p=read(R/'planning-data.json');ledger=p['area_ledger'];packages=read(R/'implementation-packages.json')
assert not ledger['collisions']
assert ledger['union_area']==1457 and 1200<=ledger['union_area']<=1600
assert sum(o['accounting_area_blocks2'] for o in packages)==ledger['union_area']
assert sum(o['households'] for o in packages)==sum(o['households'] for o in p['parcels'])==4
assert ledger['union_area']+ledger['unallocated_scope_area']==ledger['scope_cell_center_area']
objects=p['parcels']+p['shared_spaces']+p['lanes']+p['blocks']+p['frontages'];ids={o['id'] for o in objects}
assert len(ids)==len(objects)
for pack in packages:
    assert pack['child_scale']=='URBAN_ENSEMBLE' and not pack['world_write_authorization']
    assert set(pack['scope_refs'])<=ids
for o in p['parcels']+p['shared_spaces']+p['lanes']:
    assert o['metrics']['void16_columns']==0
for o in p['parcels']:
    assert o['metrics']['outside_scope_cells']==0
    assert o['metrics']['public_edge_adjacent_cells']>0
# 独立核对公共空间格心拓扑；此项不声称实际路线可用。
public=ns['public'];pending=set(zip(*public.nonzero()));components=[]
while pending:
    seed=pending.pop();stack=[seed];component={seed}
    while stack:
        j,i=stack.pop()
        for q in [(j-1,i),(j+1,i),(j,i-1),(j,i+1)]:
            if q in pending:pending.remove(q);stack.append(q);component.add(q)
    components.append(len(component))
assert len(components)==1,components
input_checks=[]
for rec in read(R/'sources/source-register.json'):
    path=R/rec['local_copy'] if 'local_copy' in rec else R.parent/rec['path']
    actual=sha(path);assert actual==rec['sha256'],rec['path']
    input_checks.append(dict(path=rec['path'],sha256=actual,unchanged=True))
provenance=read(R/'evidence/world-read-provenance.json');world_checks=[]
for rel,hashes in provenance['source_and_snapshot_hashes'].items():
    actual=sha(Path(provenance['source_path'])/rel);assert actual==hashes['source_sha256']
    world_checks.append(dict(path=rel,initial_sha256=hashes['source_sha256'],final_sha256=actual,unchanged=True))
raw_checks=[]
for name in ['near-ground.json.gz','surface-crop.json.gz']:
    raw=gzip.decompress((R/'evidence'/name).read_bytes());d=json.loads(raw)
    assert len(d['columns'])==4543
    raw_checks.append(dict(path='evidence/'+name,uncompressed_sha256=hashlib.sha256(raw).hexdigest(),columns=len(d['columns'])))
assert all(len(c['state_ids'])==29 for c in json.loads(gzip.decompress((R/'evidence/near-ground.json.gz').read_bytes()))['columns'])
for path in R.rglob('*.json'):read(path)
diff=subprocess.check_output(['git','-c','core.quotePath=false','diff','--name-only','HEAD'],cwd=R.parent.parent,text=True,encoding='utf-8').splitlines()
assert all('MP-P04-WEST-APPROACH' in name for name in diff),diff
result=dict(task=p['id'],checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),world_writes=0,world_files=world_checks,input_checks=input_checks,raw_evidence=raw_checks,
    technical_checks=dict(json_parse=True,source_hashes_unchanged=True,deterministic_rebuild=True,no_parcel_lane_cell_overlap=True,public_cell_components=components,parcel_public_cell_adjacency=True,original_void16_exclusion=True,package_accounting_sum=1457,selected_households=4,tracked_changes_scoped=True),
    visual_review='实际查看4张地图；修正深空气符号被填色遮蔽、阶段容量说明及门前衔接，补入空间编号',
    unverified=['真实movement/collision及驮畜转弯','季节供水与日需','地权与通行协议','结构安全及深空气连通范围','未来建筑净空','污物终端与峰值货流'],
    scope_limits=['仅相关三世界文件哈希，不声称全存档所有文件核对','源快照日期不是实时玩家视角','几何格心检查不替代连续工程净宽或规划质量','不评价Skill回归PASS/FAIL'])
write(R/'validation.json',result)
manifest={q.relative_to(R).as_posix():dict(sha256=sha(q),bytes=q.stat().st_size) for q in sorted(R.rglob('*')) if q.is_file() and q.name!='manifest.json'}
write(R/'manifest.json',manifest)
print(json.dumps(dict(files=len(manifest),bytes=sum(v['bytes'] for v in manifest.values()),technical_checks=result['technical_checks']),ensure_ascii=False))
