"""核对本轮初始完整指纹；不重置 baseline，也不掩盖外部变化。"""
import sys,json
from pathlib import Path
from contextlib import ExitStack
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tooling'));sys.path.append('D:/Games/Minecraft/AI工程/AI-Blueprints/参考入库/第三方')
import nbtlib
from L1_器件层.源快照保护器 import ReadGuard,fingerprint,write_json
world=Path(sys.argv[1]);roots={'world':world,'WB-002R':ROOT.parent/'WB-002R',**{n:ROOT.parents[2]/'natural-geography'/n for n in ('V1','NG-2','NG-3')}}
before=json.loads((ROOT/'manifest/source-before.json').read_text(encoding='utf-8'))
with ExitStack() as stack:
    for root in roots.values():stack.enter_context(ReadGuard(root))
    after={n:fingerprint(p) for n,p in roots.items()}
    level=nbtlib.load(world/'level.dat')['Data'];assert str(level['LevelName'])=='建筑师' and int(level['DataVersion'])==4903
    report={'checked_at':datetime.now(timezone.utc).isoformat(),'world_writes':0,'world_unchanged_since_start':before['world']==after['world'],'immutable':{n:before[n]==after[n] for n in roots if n!='world'},'inventory_hash_size_mtime_equal':before==after,'LevelName':str(level['LevelName']),'DataVersion':int(level['DataVersion']),'protection':'GENERIC_READ / FILE_SHARE_READ on all existing world and historical evidence files; whole inventory SHA256 / size / mtime comparison'}
    write_json(ROOT/'validation/source-audit.json',report);assert before==after;print(json.dumps(report))
