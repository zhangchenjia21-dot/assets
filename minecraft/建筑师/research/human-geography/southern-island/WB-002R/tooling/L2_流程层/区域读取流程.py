"""读取用例始终持源文件只读句柄；初始指纹不允许覆盖，seal覆盖本任务全时段。"""
import json,sqlite3,gzip,shutil
from contextlib import ExitStack
from datetime import datetime,timezone
from pathlib import Path
import nbtlib
from L0_公理层.区域契约 import BOUNDS,BASE,SCHEMA
from L1_器件层.源快照保护器 import ReadGuard,fingerprint,write_json
from L1_器件层.区域柱读取器 import Reader,connect

def sources(out):
    natural=out.parents[2]/'natural-geography'
    return {n:natural/n for n in ('V1','NG-2','NG-3')}

def audit(out,world,extract=False):
    roots={'world':world,**sources(out)}
    with ExitStack() as stack:
        for root in roots.values():stack.enter_context(ReadGuard(root))
        before={n:fingerprint(p) for n,p in roots.items()}
        if extract:
            if extract=='refresh':
                # Owner确认退出后新建epoch；原始基线和首轮观测必须保留，不能掩盖窗口之间的外部写入。
                if (out/'manifest/current-source-before.json').exists():raise ValueError('刷新基线已存在，不得覆盖')
                original=json.loads((out/'manifest/source-before.json').read_text(encoding='utf-8'))
                if any(original[n]!=before[n] for n in ('V1','NG-2','NG-3')):raise ValueError('历史证据变化')
                history=out/'raw-or-queryable/first-epoch';history.mkdir(exist_ok=True)
                old=out/'raw-or-queryable/observed.sqlite'
                with old.open('rb') as inp,(history/'observed.sqlite.gz').open('xb') as raw,gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0) as dst:shutil.copyfileobj(inp,dst)
                shutil.copyfile(out/'manifest/freshness.json',history/'freshness.json')
                shutil.copyfile(out/'validation/extraction-source-audit.json',history/'source-audit.json')
                old.unlink()
                write_json(out/'manifest/current-source-before.json',before)
                changes={k:{'before':original['world'].get(k),'after':before['world'].get(k)} for k in sorted(original['world'].keys()|before['world'].keys()) if original['world'].get(k)!=before['world'].get(k)}
                write_json(out/'manifest/epoch-transition.json',{'reason':'Owner confirmed save exited; protected refresh after detected external write','world_writes_by_task':0,'world_changed_between_epochs':changes,'initial_baseline_retained':'source-before.json','current_baseline':'current-source-before.json'})
            else:
                if (out/'manifest/source-before.json').exists():raise ValueError('禁止覆盖起始指纹')
                write_json(out/'manifest/source-before.json',before)
            level=nbtlib.load(world/'level.dat')['Data']
            if str(level['LevelName'])!='建筑师' or int(level['DataVersion'])!=4903:raise ValueError('world identity mismatch')
            x0,z0,x1,z1=BOUNDS;prefix='dimensions/minecraft/overworld/region/'
            relevant=[prefix+f'r.{x}.{z}.mca' for z in range(z0//512,z1//512+1) for x in range(x0//512,x1//512+1)]
            differences={}
            for name,rel in [('NG-2','manifest/world-after.json'),('NG-3','manifest/world-before.json')]:
                old=json.loads((roots[name]/rel).read_text(encoding='utf-8'))
                differences[name]=[p for p in relevant if p not in before['world'] or p not in old or before['world'][p]['sha256']!=old[p]['sha256']]
            status='REGION_CHANGED_SINCE_ATLAS' if any(differences.values()) else 'CURRENT_MATCH'
            write_json(out/'manifest/freshness.json',{'schema':SCHEMA,'execution_base':BASE,'checked_at':datetime.now(timezone.utc).isoformat(),'LevelName':str(level['LevelName']),'DataVersion':int(level['DataVersion']),'bounds':BOUNDS,'extension_blocks':[0,0,0,0],'regional_snapshot_status':status,'relevant_regions':relevant,'changed_relevant_regions':differences,'current_overworld_inventory':{p:v for p,v in before['world'].items() if p.startswith(prefix)},'source_policy':'Current world always decoded; Atlas is lineage, not exact current substitute'})
            path=out/'raw-or-queryable/observed.sqlite'
            if path.exists():raise ValueError('不能覆盖既有读取成果')
            db=connect(path);reader=Reader(world,db)
            for cz in range(z0//16,z1//16+1):
                for cx in range(x0//16,x1//16+1):
                    rows=reader.read(cx,cz)
                    db.executemany('INSERT INTO samples VALUES ('+','.join('?'*14)+')',[tuple(map(int,r)) for r in rows])
                db.commit()
                if (cz-z0//16)%8==0:print('decoded',reader.decoded,'chunks',flush=True)
            db.commit();assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok';db.close()
        original=json.loads((out/'manifest/source-before.json').read_text(encoding='utf-8'))
        baseline=json.loads((out/'manifest/current-source-before.json').read_text(encoding='utf-8')) if (out/'manifest/current-source-before.json').exists() else original
        after={n:fingerprint(p) for n,p in roots.items()}
        if before!=after:raise ValueError('读取期间源变化')
        report={'checked_at':datetime.now(timezone.utc).isoformat(),'world_writes':0,'world_unchanged_since_start':original['world']==after['world'],'world_unchanged_since_current_epoch':baseline['world']==after['world'],'immutable':{n:original[n]==after[n] for n in ('V1','NG-2','NG-3')},'inventory_hash_size_mtime_equal_current_epoch':baseline==after,'external_gap_record':'manifest/epoch-transition.json' if baseline!=original else None,'protection':'GENERIC_READ / FILE_SHARE_READ for all existing world/evidence files + complete inventory before/after','phase':'extraction' if extract else 'final seal'}
        write_json(out/'validation'/('extraction-source-audit.json' if extract else 'source-audit.json'),report)
        if baseline!=after or any(original[n]!=after[n] for n in ('V1','NG-2','NG-3')):raise ValueError('当前epoch或历史证据变化，见audit')
        print(json.dumps(report),flush=True)
