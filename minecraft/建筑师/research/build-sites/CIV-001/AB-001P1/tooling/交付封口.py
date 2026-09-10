"""只有源封口和候选核验通过才登记轻量包；工程PASS不覆盖Owner选择关口。"""
import sys,json
from pathlib import Path
sys.dont_write_bytecode=True
from 源快照保护器 import write_json
out=Path(__file__).resolve().parents[1]
for name in ('source-audit','geometry-check','independent-check','rebuild'):
    assert json.loads((out/f'validation/{name}.json').read_text(encoding='utf-8'))['status']=='PASS'
mapping=json.loads((out/'site-mapping.json').read_text(encoding='utf-8'));assert mapping['verdict']=='OWNER_SELECTION_REQUIRED' and mapping['selected_site'] is None
write_json(out/'validation/summary.json',{'engineering_checks':'PASS','site_mapping':'OWNER_SELECTION_REQUIRED','design_readiness':'NOT_READY','independent_review':'PENDING','world_writes':0,'world_block_reads':0,'broad_rescan':False,'immutable_roots':'world, V1, NG-2, NG-3, WB-002R, R1, WB-003R, World Canon, architecture including Grammar','validation':['source-audit.json','freshness.json','geometry-check.json','independent-check.json','rebuild.json','payload.json'],'limitations':'sparse vegetation; no in-game sightline, hidden structures, collision or buildability guarantee; neither candidate is an independent island'})
previous=-1
for _ in range(10):
    files=[p for p in out.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    assert not any(p.suffix in ('.sqlite','.npz','.gz') for p in files)
    total=sum(p.stat().st_size for p in files);assert total<=15*1024**2
    if previous==total:break
    previous=total
    write_json(out/'validation/payload.json',{'status':'PASS','bytes':total,'mib':round(total/1024**2,6),'files':len(files),'includes':'all research files, including this file; no raw cache','target_bytes':15*1024**2,'hard_limit_bytes':25*1024**2})
else:raise AssertionError('payload size did not converge')
print('review bundle verified',total,'bytes')
