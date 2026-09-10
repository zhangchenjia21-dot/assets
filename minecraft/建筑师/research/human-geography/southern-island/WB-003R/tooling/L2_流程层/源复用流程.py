"""冻结初始源清单，哈希匹配才复用；不以旧快照冒充变化后的当前事实。"""
import json,sqlite3
from contextlib import ExitStack
from datetime import datetime,timezone
from L1_器件层.源快照保护器 import ReadGuard,fingerprint,write_json,digest
def roots(out,world):
    return {'world':world,**{n:out.parents[2]/'natural-geography'/n for n in ('V1','NG-2','NG-3')},'WB-002R':out.parent/'WB-002R','R1':out.parent/'WB-002R-R1','canon':out.parents[3]/'world'}
def audit(out,cache,world,initial=False):
    rr=roots(out,world)
    with ExitStack() as stack:
        for p in rr.values():stack.enter_context(ReadGuard(p))
        now={n:fingerprint(p) for n,p in rr.items()}
        if initial:
            assert not (cache/'source-before.json').exists(),'不得覆盖初始epoch'
            write_json(cache/'source-before.json',now)
            old=json.loads((rr['R1']/'profile/scope-completion.json').read_text(encoding='utf-8'))
            changed=[p for p,h in old['relevant_region_hashes'].items() if now['world'].get(p,{}).get('sha256')!=h]
            report={'checked_at':datetime.now(timezone.utc).isoformat(),'source_epoch_sha256':digest(cache/'source-before.json'),'r1_source_regions':{p:now['world'].get(p) for p in old['relevant_region_hashes']},'changed_regions_since_R1':changed,'world_writes':0,'reuse_status':'CURRENT_MATCH' if not changed else 'REFRESH_REQUIRED','full_inventory':'LOCAL_ONLY source-before.json'}
            write_json(out/'manifest/source-fingerprint.json',report)
            assert not changed,'当前源变化，须界定delta，禁止自动全域重扫'
            store=json.loads((rr['R1']/'manifest/store.json').read_text(encoding='utf-8'))
            for item in store['files']:assert digest(rr['R1']/'raw-or-queryable'/item['name'])==item['sha256']
        else:
            before=json.loads((cache/'source-before.json').read_text(encoding='utf-8'))
            write_json(out/'validation/source-audit.json',{'checked_at':datetime.now(timezone.utc).isoformat(),'world_writes':0,'world_unchanged_since_start':before['world']==now['world'],'immutable':{n:before[n]==now[n] for n in rr if n!='world'},'full_inventory_hash_size_mtime_equal':before==now})
            assert before==now
    print('source audit PASS',flush=True)
