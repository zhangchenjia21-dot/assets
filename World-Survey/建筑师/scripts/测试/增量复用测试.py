"""固定事实与空间 ID 基线，用于一次真实缓存重跑前后核对；不访问世界。"""
import hashlib
import json
import sqlite3
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
db=sqlite3.connect((ROOT/'raw'/'geography.sqlite').as_uri()+'?mode=ro',uri=True)

def digest(sql):
    h=hashlib.sha256()
    for row in db.execute(sql):h.update((json.dumps(row,ensure_ascii=False)+'\n').encode())
    return h.hexdigest()

current={'samples_sha256':digest('SELECT * FROM samples ORDER BY x,z'),'active_id_members_sha256':digest('SELECT o.id,o.family,o.type,m.gx,m.gz FROM objects o JOIN members m USING(id) WHERE o.active=1 ORDER BY o.id,m.gx,m.gz'),'adjacency_sha256':digest('SELECT * FROM adjacency ORDER BY a,b')}
baseline=ROOT/'reports'/'incremental-baseline.json'
if sys.argv[1]=='capture':
    baseline.write_text(json.dumps(current,indent=2),encoding='utf-8');print('incremental baseline captured')
elif sys.argv[1]=='verify':
    before=json.loads(baseline.read_text(encoding='utf-8'))
    m=json.loads(db.execute("SELECT value FROM meta WHERE key='manifest'").fetchone()[0])
    result={'before':before,'after':current,'unchanged':before==current,'cached_regions':m['cached_region_count'],'expected_regions':m['coverage']['region_files'],'source_hashes_equal':m['hashes_equal']}
    result['pass']=result['unchanged'] and result['cached_regions']==result['expected_regions'] and result['source_hashes_equal']
    (ROOT/'reports'/'incremental-validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result))
    if not result['pass']:raise SystemExit(1)
else:raise ValueError('use capture or verify')
