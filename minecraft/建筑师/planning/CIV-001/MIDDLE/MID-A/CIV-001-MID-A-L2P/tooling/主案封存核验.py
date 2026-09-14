"""主方案先封存再开放 Legacy；校验不能悄悄重写承诺。"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,subprocess
p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--freeze',action='store_true');g.add_argument('--verify',action='store_true');a=p.parse_args()
P=Path(__file__).resolve().parents[1];f=P/'validation/PRIMARY-FREEZE.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if a.freeze:
 assert not f.exists(),'Freeze exists; never overwrite'
 excluded={'COMPLETION.md','LEGACY-COMPARISON.md','validation/PRIMARY-FREEZE.json','validation/legacy-read-ledger.json','validation/delivery-verification.json'}
 files={v.relative_to(P).as_posix():sha(v) for v in sorted(P.rglob('*')) if v.is_file() and v.relative_to(P).as_posix() not in excluded and '__pycache__' not in v.parts}
 result=dict(schema='primary-freeze/1',plan_revision='CIV-001-MID-A-L2P-r1',created_utc=datetime.now(timezone.utc).isoformat(),base_commit='2e1bfd4',legacy_reads_this_run_before_freeze=False,prior_conversation_contains_legacy=True,world_writes=0,files=files)
 f.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
else:
 result=json.loads(f.read_text('utf-8'))
 for name,expected in result['files'].items():assert sha(P/name)==expected,name
print(f'{len(result["files"])} primary files frozen/verified; not planning acceptance.')
