"""登记只读来源与包大小；工程核验不自行接受政治边界或恢复P2。"""
import sys,json,subprocess
from pathlib import Path
sys.dont_write_bytecode=True
from 源快照保护器 import digest,write_json
out=Path(__file__).resolve().parents[1];project=out.parents[3];cache=Path('D:/Games/Minecraft/AI工程/研究缓存/建筑师/AB-001P1R');p1=out.parent/'AB-001P1';r1=project/'research/human-geography/southern-island/WB-002R-R1'
fresh=json.loads((out/'validation/freshness.json').read_text(encoding='utf-8'));assert fresh['status']=='CURRENT_MATCH'
for name in ('source-audit','geometry','independent','rebuild'):assert json.loads((out/f'validation/{name}.json').read_text(encoding='utf-8'))['status']=='PASS'
inputs=[p1/'geometry/A-land-runs.json',p1/'site-candidates.json',r1/'raw-or-queryable/derived.npz',r1/'raw-or-queryable/observed.sqlite']
write_json(out/'validation/lineage.json',{'execution_base':subprocess.check_output(['git','rev-parse','d83d155'],text=True).strip(),'source_epoch':fresh['source_epoch'],'source_A_implementation':'3008f3663a4873dea8bb983c81abc221cfb6b095','inputs':[{'path':p.relative_to(project).as_posix(),'sha256':digest(p),'bytes':p.stat().st_size} for p in inputs],'raw_cache':{'cache_id':'AB001P1R-SOURCE-BEFORE','status':'LOCAL_ONLY','retention':'PRESERVE_LOCAL','schema':'root -> relative file -> sha256,size,mtime_ns','sha256':digest(cache/'source-before.json'),'bytes':(cache/'source-before.json').stat().st_size,'source_world_fingerprint':fresh['source_epoch'],'source_epoch':fresh['checked_at'],'generated_at':fresh['checked_at'],'rebuild_command':'historical initial inventory cannot be recreated after source changes; preserve local file; init only for new task epoch','local_path_hint':str(cache/'source-before.json')},'world_writes':0,'new_world_block_reads':0,'broad_rescan':False})
write_json(out/'validation/summary.json',{'engineering_checks':'PASS','independent_review':'PENDING','preferred_cut_plane_x':89,'commons_area':92124,'connector_area':13661,'A_area':105785,'partition_complete_disjoint':True,'commons_components':1,'connector_components':1,'parent_continuation_excluding_commons':True,'exact_outline_and_RLE':True,'source_and_predecessors_immutable':True,'world_writes':0,'new_world_block_reads':0,'broad_rescan':False,'P2':'HOLD','checks':['freshness.json','source-audit.json','geometry.json','independent.json','rebuild.json','lineage.json','payload.json']})
write_json(out/'review/index.json',{'status':'AWAITING INDEPENDENT REVIEW','entry':['commons-boundary.json','reports/联盟公地边界拟合.md','visual/commons-connector-boundary.png','commons-geometry.json','connector-geometry.json','review/cross-sections.json','review/parent-continuation.json','validation/summary.json'],'stop':'GPT acceptance then Program/Capacity recalculation; no P2 or Build'})
previous=-1
for _ in range(10):
    files=[p for p in out.rglob('*') if p.is_file() and '__pycache__' not in p.parts];total=sum(p.stat().st_size for p in files)
    assert not any(p.suffix in ('.sqlite','.npz','.gz') for p in files);assert total<=15*1024**2
    if total==previous:break
    previous=total;write_json(out/'validation/payload.json',{'status':'PASS','bytes':total,'mib':round(total/1024**2,6),'files':len(files),'scope':'all new research files, including this audit; raw local only','target_bytes':15*1024**2,'hard_limit_bytes':25*1024**2})
else:raise AssertionError('payload fixed point failed')
print('delivery PASS',total,'bytes')
