"""验证数据、来源与确定性制图；Gate语义判断由Planner报告承担。

默认只在当前归档写校验结果；世界文件只读SHA256，不启动游戏。
"""
from pathlib import Path
import json,hashlib,gzip,subprocess,sys,datetime
R=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
data=read(R/'assessment-data.json'); c=data['capacity']
assert data['world_writes']==0 and not data['world_write_authorization'] and not data['builder_ready']
assert c['first_residential_stage']['total_area_range_blocks2']==[12*100+2300,16*150+2600]
assert c['conditional_long_term_area_range_blocks2']==[12*100+2300,24*150+4400]
raw=gzip.decompress((R/'evidence/surface.json.gz').read_bytes()); rawhash=hashlib.sha256(raw).hexdigest()
assert rawhash=='d11f036d8baac7fabcfa7c4ed9ba804dd4862f55fc3d1ec2ce25cec68d6eb7f2'
input_checks=[]
for rec in read(R/'sources/input-register.json'):
    p=R/rec['local_copy'] if 'local_copy' in rec else R.parent/rec['path']
    actual=sha(p); assert actual==rec['sha256'],str(p)
    input_checks.append(dict(path=rec['path'],sha256=actual,unchanged=True))
provenance=read(R/'evidence/world-read-provenance.json')
world_checks=[]
for rel,expected in provenance['source_before'].items():
    actual=sha(Path(provenance['source_path'])/rel);assert actual==expected
    world_checks.append(dict(path=rel,baseline_sha256=expected,final_sha256=actual,unchanged=True))
old={p.name:sha(p) for p in (R/'maps').glob('*.png')}
subprocess.run([sys.executable,str(R/'证据与制图.py')],check=True,stdout=subprocess.DEVNULL)
assert old=={p.name:sha(p) for p in (R/'maps').glob('*.png')},'地图重建不确定'
stats=read(R/'evidence/independent-statistics.json')
assert sum(stats['windows']['parent_search']['surface_counts'].values())==36864
assert stats['void_columns']==603
ids=[s['id'] for s in data['spatial_objects']];assert len(ids)==len(set(ids))
for obj in data['spatial_objects']:
    if 'bounds_inclusive_xz' in obj:
        x,z,X,Z=obj['bounds_inclusive_xz'];assert 640<=x<=X<=959 and 1488<=z<=Z<=1775
for p in R.rglob('*.json'):read(p)
tracked_diff=subprocess.check_output(['git','diff','--name-only','HEAD','--','.'],cwd=R.parent.parent,text=True,encoding='utf-8').strip().splitlines()
assert all('MP-P03M-NORTH-ROCK-TERRACE' in p for p in tracked_diff),tracked_diff
result=dict(task=data['id'],checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),world_writes=0,
    world_identity=provenance['world'],source_snapshot_utc=provenance['read_utc'],
    current_source_freshness='相关3文件与原快照、本轮初始及末次哈希相同；未声称整个世界文件清单验证',
    world_hash_checks=world_checks,input_hash_checks=input_checks,
    raw_uncompressed_sha256=rawhash,raw_column_count=92160,
    technical_checks=dict(json_parse=True,capacity_arithmetic=True,source_hashes=True,source_world_selected_files_unchanged=True,map_rebuild_identical=True,observed_class_counts=True,coordinates_within_survey=True,tracked_changes_scoped=True),
    visual_review='Planner实际打开检查两图：文字可读、坐标与图例齐备；修正剖面引用文字',
    excluded_claims=['不是现场通行验证','不是水文/饮用水验证','不是结构安全验证','不是地权批准','不是Skill回归判定'],
    limits=['不运行游戏或服务器','空洞扫描仅指定窗地下16格','静态数据不证明社会关系','未读取禁用规划和审核文件','制图复现需要Python、NumPy、Pillow与微软雅黑字体'])
dump(R/'validation.json',result)
manifest={p.relative_to(R).as_posix():dict(sha256=sha(p),bytes=p.stat().st_size) for p in sorted(R.rglob('*')) if p.is_file() and p.name!='manifest.json'}
dump(R/'manifest.json',manifest)
print(json.dumps(dict(files=len(manifest),bytes=sum(v['bytes'] for v in manifest.values()),technical_checks=result['technical_checks']),ensure_ascii=False))
