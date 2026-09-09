import json,gzip,shutil,sqlite3
from contextlib import ExitStack
from datetime import datetime,timezone
import nbtlib
from L0_公理层.图册契约 import BASE,SCHEMA
from L1_器件层.源快照保护器 import ReadGuard,fingerprint,write_json,digest

def gate(out,world,final=False):
    """首次绑定证据指纹；复核只报告差异，不写源文件，不因玩家元数据变化判定地形过期。"""
    v1=out.parent/'V1';ng2=out.parent/'NG-2';prefix='dimensions/minecraft/overworld/region/'
    with ExitStack() as stack:
        for root in (world,v1,ng2):stack.enter_context(ReadGuard(root))
        before=fingerprint(world);evidence={'V1':fingerprint(v1),'NG-2':fingerprint(ng2)}
        level=nbtlib.load(world/'level.dat')['Data']
        current={k:v for k,v in before.items() if k.startswith(prefix)}
        baselines={'V1':json.loads((v1/'survey/manifest/source-after.json').read_text(encoding='utf-8')),'NG-2':json.loads((ng2/'manifest/world-after.json').read_text(encoding='utf-8'))}
        matches={}
        for name,old in baselines.items():
            old={k:v for k,v in old.items() if k.startswith(prefix)}
            matches[name]={'added':sorted(current.keys()-old.keys()),'deleted':sorted(old.keys()-current.keys()),'changed':[k for k in sorted(current.keys()&old.keys()) if current[k]['sha256']!=old[k]['sha256']]}
        identity={'LevelName':str(level['LevelName']),'DataVersion':int(level['DataVersion'])}
        status='CURRENT_MATCH' if current and all(not any(v.values()) for v in matches.values()) and identity=={'LevelName':'建筑师','DataVersion':4903} else 'TERRAIN_CHANGED' if current else 'UNVERIFIABLE'
        after=fingerprint(world)
        if before!=after:raise ValueError('核验期间源文件变化')
        report={'schema_version':SCHEMA,'execution_base':BASE,'checked_at':datetime.now(timezone.utc).isoformat(),'identity':identity,'geography_snapshot_status':status,'comparison':matches,'world_path':str(world),'region_count':len(current),'world_writes':0,'world_inventory_before_after_equal':True,'freshness_scope':'Overworld region inventory and SHA256; player/time metadata excluded from freshness verdict','protection':'all existing world and accepted evidence files held GENERIC_READ/FILE_SHARE_READ; complete inventory compared','in_game_visual_review':'BLOCKED_BY_SAFE_ENVIRONMENT'}
        if final:
            original=json.loads((out/'manifest/evidence-before.json').read_text(encoding='utf-8'))
            report['V1_NG2_immutable']=evidence==original
            report['world_unchanged_since_start']=before==json.loads((out/'manifest/world-before.json').read_text(encoding='utf-8'))
            if evidence!=original:raise ValueError('V1/NG-2证据变化')
            write_json(out/'validation/final-source-audit.json',report)
        else:
            if (out/'manifest/evidence-before.json').exists():raise ValueError('初始gate已存在；请使用final复核，不能覆盖起始指纹')
            write_json(out/'manifest/world-before.json',before);write_json(out/'manifest/evidence-before.json',evidence)
            write_json(out/'manifest/current-regions.json',current);write_json(out/'manifest/freshness.json',report)
        print(json.dumps(report,ensure_ascii=True))
        if status!='CURRENT_MATCH':raise ValueError('仅允许historical/proposed stale结果；不得生成current Atlas')

def prepare(out):
    """只解压V1副本到NG-3忽略的缓存；NG-2使用已有导出索引，不复制500万柱。"""
    cache=out/'raw-or-queryable/input-cache';cache.mkdir(parents=True,exist_ok=True)
    dest=cache/'v1.sqlite';source=out.parent/'V1/survey/raw/geography.sqlite.gz'
    if not dest.exists():
        with gzip.open(source,'rb') as src,dest.open('xb') as dst:shutil.copyfileobj(src,dst)
    db=sqlite3.connect(dest.as_uri()+'?mode=ro',uri=True)
    if db.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise ValueError('V1解压库损坏')
    write_json(out/'manifest/input-cache.json',{'source':'../V1/survey/raw/geography.sqlite.gz','source_sha256':digest(source),'uncompressed_sha256':digest(dest),'retained_in_git':False})
    print('V1 cache:',db.execute('SELECT count(*) FROM cells').fetchone()[0],'cells');db.close()
