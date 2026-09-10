"""独立外围核验脚本；源文件只读，初始清单仅保存本地，拒绝刷新旧基线。"""
import sys,json
from pathlib import Path
from contextlib import ExitStack
from datetime import datetime,timezone
sys.dont_write_bytecode=True
from 源快照保护器 import fingerprint,digest,write_json,ReadGuard
out=Path(__file__).resolve().parents[1];project=out.parents[3];cache=Path('D:/Games/Minecraft/AI工程/研究缓存/建筑师/AB-001P1R')
world=Path('D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/建筑师')
roots={'world':world,'Canon':project/'world','Grammar':project/'architecture',**{n:project/'research/natural-geography'/n for n in ('V1','NG-2','NG-3')},**{n:project/'research/human-geography/southern-island'/n for n in ('WB-002R','WB-002R-R1','WB-003R')}}
roots['AB-001P1']=out.parent/'AB-001P1'
with ExitStack() as stack:
    for root in roots.values():assert root.exists();stack.enter_context(ReadGuard(root))
    now={n:fingerprint(p) for n,p in roots.items()}
    if sys.argv[1]=='init':
        assert not (cache/'source-before.json').exists(),'不得覆盖任务初始源清单'
        write_json(cache/'source-before.json',now)
        r1=json.loads((roots['WB-002R-R1']/'profile/scope-completion.json').read_text(encoding='utf-8'))
        changes=[p for p,h in r1['relevant_region_hashes'].items() if now['world'].get(p,{}).get('sha256')!=h]
        write_json(out/'validation/freshness.json',{'checked_at':datetime.now(timezone.utc).isoformat(),'source_epoch':digest(cache/'source-before.json'),'relevant_regions':{p:now['world'][p] for p in r1['relevant_region_hashes']},'changed_regions':changes,'status':'CURRENT_MATCH' if not changes else 'DELTA_REQUIRED','method':'whole-file hash comparison; no broad NBT/world block scan','world_writes':0})
        assert not changes,'当前源与缓存不同，必须限制增量核验，不得沿用旧统计'
        manifest=json.loads((roots['WB-003R']/'manifest/raw-cache.json').read_text(encoding='utf-8'))
        for v in manifest['files']:
            if v['cache_id'].startswith('R1-'):assert digest(Path(v['local_path_hint']))==v['sha256']
    elif sys.argv[1]=='seal':
        before=json.loads((cache/'source-before.json').read_text(encoding='utf-8'));same={n:before[n]==now[n] for n in roots}
        write_json(out/'validation/source-audit.json',{'checked_at':datetime.now(timezone.utc).isoformat(),'source_epoch':digest(cache/'source-before.json'),'unchanged':same,'world_writes':0,'status':'PASS' if all(same.values()) else 'FAIL','method':'full relative filename, SHA256, size and mtime_ns comparison to task start','new_world_block_reads':0})
        assert all(same.values())
    else:raise ValueError('init or seal required')
print('source audit PASS',flush=True)
