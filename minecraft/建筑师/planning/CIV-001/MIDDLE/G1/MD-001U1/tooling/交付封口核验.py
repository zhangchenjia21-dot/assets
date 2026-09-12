"""只核对正式源、保护输入和轻量交付；--rebuild 显式重建本轮设计以比较字节。"""
import sys,json,subprocess,importlib.util,re
from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
spec=importlib.util.spec_from_file_location('design',Path(__file__).with_name('街区设计编译.py'));d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
def files():return [p for root in [d.OUT,d.KIT] for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
def deterministic_files():return [p for p in files() if (p.suffix=='.png' or p.parent in [d.OUT,d.KIT]) and p.suffix in ['.json','.gz','.png']]
if '--rebuild' in sys.argv:
    before={str(p):d.sha(p) for p in deterministic_files()}
    for name in ['街区设计编译.py','场地关系核验.py','地域模板编译.py','街区审阅制图.py']:
        subprocess.run([sys.executable,'-X','utf8',str(Path(__file__).with_name(name))],check=True)
    mismatches=[p for p,h in before.items() if d.sha(Path(p))!=h]
    assert not mismatches,mismatches
    d.write(d.OUT/'validation/rebuild-check.json',{'compared_artifacts':len(before),'byte_identical':True,'sha256_by_path':{Path(p).relative_to(d.ROOT).as_posix():h for p,h in before.items()},'excludes':'freshness timestamps and delivery reports'})
proof=d.freshness();d.write(d.OUT/'validation/source-freshness-after.json',proof)
protected=d.read(d.OUT/'validation/source-inputs.json')['inputs']
for item in protected:assert d.sha(d.ROOT/item['path'])==item['sha256'],item['path']
cachefiles=[d.CACHE/'capture.json',d.CACHE/'surface.json.gz']+list((d.CACHE/'snapshot').iterdir())
epoch=d.read(d.CACHE/'capture.json')['snapshot_finished_at']
d.write(d.OUT/'validation/raw-cache-manifest.json',{'cache_id':'MD-001S1-current-world-reused-by-MD-001U1','status':'LOCAL_ONLY','retention':'PRESERVE_LOCAL',
 'schema':'Minecraft4903 Anvil+NBT snapshot / surface-json-gzip','source_epoch':epoch,'source_world_fingerprint':proof['files'][0]['sha256'],
 'rebuild_command':'See validation/README.md; no refresh from changed world without new lineage',
 'artifacts':[{'local_path_hint':str(p),'bytes':p.stat().st_size,'sha256':d.sha(p),'generated_at':datetime.fromtimestamp(p.stat().st_mtime,timezone.utc).isoformat()} for p in cachefiles]})
badlinks=[];jsoncount=0;pngcount=0
for p in files():
    if p.suffix=='.json':
        json.loads(p.read_text('utf8'),parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)));jsoncount+=1
    if p.suffix=='.png':
        with Image.open(p) as im:im.verify()
        pngcount+=1
    if p.suffix=='.md':
        for dest in re.findall(r'\]\(([^)]+)\)',p.read_text('utf8')):
            if '://' not in dest and not (p.parent/dest.split('#')[0]).exists():badlinks.append([str(p),dest])
assert not badlinks,badlinks
mods=d.read(d.KIT/'modules.json')['modules'];ids={v['id'] for v in mods}
for v in d.read(d.KIT/'typologies.json')['typologies']:
    assert set(v['optional_modules'])<=ids
    assert v['required_core'] and v['variation_knobs'] and v['terrain_adaptation'] and v['incompatible']
statuses=[]
for name,key in [('modules.json','modules'),('typologies.json','typologies'),('palette-families.json','families'),('variation-rules.json','rules')]:
    statuses.extend(v['status'] for v in d.read(d.KIT/name)[key])
k=d.read(d.KIT/'KIT.json');statuses.extend(v['status'] for v in k['shared_dna']+k['regional_dna'])
assert set(statuses)<={'PROPOSED','PREVIEW_VALIDATED'}
qa=d.read(d.OUT/'validation/design-qa.json')
assert not any(v['failures'] for v in qa['stairs']+qa['routes'])
assert qa['all_design_projection_outside_columns']==0 and qa['clearance_overlap']==0
env=d.read(d.OUT/'site-envelope.json');assert env['gross_columns']==len(d.cells(env['rle_inclusive']))==1310
manifest=[{'path':p.relative_to(d.ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':d.sha(p)} for p in files() if p.name not in ['delivery-check.json']]
size=sum(v['bytes'] for v in manifest)
assert size<15*1024*1024
d.write(d.OUT/'validation/delivery-check.json',{'status':'TECHNICAL_CHECKS_COMPLETED / NOT INDEPENDENT REVIEW','checked_at':datetime.now(timezone.utc).isoformat(),
 'json_parsed':jsoncount,'png_verified':pngcount,'protected_input_hashes_unchanged':len(protected),'invalid_links':badlinks,
 'kit_maturity_entries':len(statuses),'kit_built_accepted_entries':0,'model_routes_checked':len(qa['routes']),'stair_flights_checked':len(qa['stairs']),
 'payload_bytes_excluding_this_report_task_completion_current':size,'payload_MiB':round(size/1048576,3),'files':manifest,
 'world_writes':0,'broad_rescan':0,'formal_world_runtime_launches':0,'real_minecraft_collision':'UNVERIFIED','fluid_stability':'UNVERIFIED'})
print('delivery',len(manifest),'files',round(size/1048576,3),'MiB',jsoncount,'JSON',pngcount,'PNG',len(protected),'protected inputs')
