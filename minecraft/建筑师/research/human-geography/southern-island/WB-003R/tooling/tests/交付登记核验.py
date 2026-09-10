"""登记保留在本地的输入、冻结重建结果与轻量交付大小；失败不宣称交付成功。"""
import sys,json,hashlib,subprocess
from pathlib import Path
from datetime import datetime,timezone
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from L1_器件层.源快照保护器 import write_json,digest
out=Path(__file__).resolve().parents[2];cache=Path('D:/Games/Minecraft/AI工程/研究缓存/建筑师/WB-003R');old=out.parent/'WB-002R-R1'
source=json.loads((out/'manifest/source-fingerprint.json').read_text(encoding='utf-8'));epoch=source['source_epoch_sha256']
assert digest(cache/'source-before.json')==epoch
entries=[]
for id,path,schema,rebuild in [
    ('WB003R-MINERAL-COLUMNS',cache/'mineral-columns.json','economic-access-substrate/1.0; list of columns, blocks indexed Y+60','same unchanged world epoch: init then sample in a new empty cache; never overwrite retained cache'),
    ('WB003R-SOURCE-BEFORE',cache/'source-before.json','root -> relative file -> sha256,size,mtime_ns','historical initial inventory cannot be recreated after world changes; preserve original'),
    ('R1-OBSERVED',old/'raw-or-queryable/observed.sqlite','R1 observed SQLite','restore verified predecessor archive per R1 README'),
    ('R1-PROFILE',old/'raw-or-queryable/regional-profile.sqlite','R1 regional profile SQLite','restore verified predecessor archive per R1 README'),
    ('R1-DERIVED',old/'raw-or-queryable/derived.npz','R1 terrain/topology arrays','reuse predecessor artifact and source hashes; no new full-world scan')]:
    assert path.exists(),'MISSING_LOCAL_CACHE: '+id
    entries.append({'cache_id':id,'status':'LOCAL_ONLY','retention':'PRESERVE_LOCAL','sha256':digest(path),'bytes':path.stat().st_size,'schema':schema,'source_world_fingerprint':epoch,'source_epoch':source['checked_at'],'generated_at':datetime.fromtimestamp(path.stat().st_mtime,timezone.utc).isoformat(),'generated_at_basis':'existing file mtime; source audit time is separate','rebuild_command':rebuild,'local_path_hint':str(path),'remote_policy':'not included in this new bundle; predecessor historical archives remain unchanged'})
write_json(out/'manifest/raw-cache.json',{'schema':'raw-cache-manifest/1','files':entries})
write_json(out/'manifest/lineage.json',{'execution_base':'27720bc20502337e64991c700f17e63328b09844','predecessor':'WB-002R-R1 accepted @5c6bffe','reuse':'observed, derived and profile caches; original source region hashes current match','raw_hashes':{v['cache_id']:v['sha256'] for v in entries},'new_world_column_reads':144,'new_block_positions':25176,'whole_region_rescan':False,'world_writes':0,'canon_promotion':False})
before=json.loads((cache/'rebuild-before.json').read_text(encoding='utf-8-sig'));checks=[]
for item in before:
    if item['name'].endswith('human-geography-hypotheses.json'):continue
    got=digest(out/item['name']);assert got==item['sha256'],item['name'];checks.append({'path':item['name'],'sha256':got,'byte_identical':True})
write_json(out/'validation/rebuild.json',{'status':'PASS','method':'fresh Python derive from immutable local inputs; compare byte SHA256 before/after','regenerated_artifacts':checks,'sample_design':'independent sorting/stratification recreation in geometry-sampling.json','human_hypotheses':'manually authored, not regenerated or program-judged'})
sub=json.loads((out/'profile/substrate-summary.json').read_text(encoding='utf-8'));cross=json.loads((out/'profile/crossing-profile.json').read_text(encoding='utf-8'));paths=json.loads((out/'profile/movement-corridors.json').read_text(encoding='utf-8'))
write_json(out/'review/key-metrics.json',{'sample_columns':144,'block_positions':25176,'world_writes':0,'whole_region_rescan':False,'domain_columns':{k:v['columns'] for k,v in sub['domains'].items()},'soil_lowrelief_fraction':{k:v['soil_lowrelief_fraction'] for k,v in sub['domains'].items()},'unassigned_land_columns':sub['unassigned_land_columns'],'crossings':[{k:c[k] for k in ('id','edge_to_edge_gap_blocks','status')} for c in cross['candidates']],'corridors':[{k:c[k] for k in ('id','length_blocks','maximum_single_step')} for c in paths['candidates']]})
limits=['Research masks are not exact human-region boundaries; 547618 land columns explicitly unassigned.','Soil/flat/biome/water geometry do not measure yields, fertility, population or buildability.','Vegetation sparse block observations are not tree counts or sustainable timber inventory.','Existing surface may include natural, generated structure or artificial blocks; no pristine-natural claim.','144 lattice columns with unequal domain sampling density and vertical extent cannot estimate regional ore reserves or absences.','Native biome resolution is 4x4x4; cache repeats per-column lookup.','Inland water means surface enclosure only; no water quality or replenishment proof.','X-02 sampled water-only result is rejected by exact closed-cell intersection; all discrepancy evidence retained.','Water gap and landing proxies are not harbors, navigation guarantees or trade routes.','Cost corridors lack headroom, collision, hazards and actor movement validation; C-02/C-03 sensitive to weights.','No source-world rescan, Canon, Architecture or Build changes.','Owner council-center referent remains OWNER_REFERENT / COORDINATE_TBD.','Full raw is LOCAL_ONLY; if missing report MISSING_LOCAL_CACHE; changed world cannot recreate old snapshot.']
write_json(out/'review/limitations.json',{'limitations':limits})
write_json(out/'review/index.json',{'task':'WB-003R','status':'IMPLEMENTATION COMPLETED / AWAITING INDEPENDENT REVIEW','entry_order':['manifest/lineage.json','manifest/source-fingerprint.json','review/key-metrics.json','review/sampling-design.json','review/stratified-witnesses.jsonl','profile/substrate-summary.json','profile/material-profile.json','profile/mineral-sample-profile.json','profile/water-access-profile.json','profile/crossing-profile.json','profile/movement-corridors.json','validation/geometry-sampling.json','validation/aggregate-witness-check.json','validation/rebuild.json','validation/source-audit.json','profile/human-geography-hypotheses.json','reports/经济与通达性前置画像.md','visual/substrate-access.png','manifest/raw-cache.json','review/limitations.json'],'critical_override':'X-02 rejected as clear straight crossing; exact geometry overrides finite sampling'})
audit=json.loads((out/'validation/source-audit.json').read_text(encoding='utf-8'));assert audit['full_inventory_hash_size_mtime_equal']
for name in ('geometry-sampling','aggregate-witness-check','targeted-read','rebuild'):assert json.loads((out/f'validation/{name}.json').read_text(encoding='utf-8'))['status']=='PASS'
write_json(out/'validation/summary.json',{'engineering_checks':'PASS','independent_review':'PENDING','world_writes':0,'world_and_predecessors_unchanged':True,'source_freshness':'CURRENT_MATCH','targeted_provenance':'144 chunk columns, 25176 scalar/vector name matches; region SHA256 bound','known_discrepancies':['X-02 rejected by exact geometry despite sampled water-only; retained'], 'checks':['geometry-sampling.json','aggregate-witness-check.json','targeted-read.json','source-audit.json','rebuild.json','payload.json'],'scope':'Research only; no whole-region rescan or raw upload','architecture':'L3->L2->L1->L0; Bootstrap/tests peripheral; predecessor data contract only'})
payload=out/'validation/payload.json';previous=-1
for _ in range(10):
    files=[p for p in out.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    assert not any(p.suffix in ('.sqlite','.npz','.gz') for p in files)
    total=sum(p.stat().st_size for p in files);assert total<=15*1024**2
    if total==previous:break
    previous=total;write_json(payload,{'status':'PASS','research_payload_bytes':total,'research_payload_mib':round(total/1024**2,6),'file_count':len(files),'target_bytes':15*1024**2,'hard_no_push_bytes':25*1024**2,'includes':'all research files including this audit; no compression discount','full_raw_newly_uploaded':False})
else:raise AssertionError('payload fixed point failed')
print('delivery registration PASS',total,'bytes',flush=True)
