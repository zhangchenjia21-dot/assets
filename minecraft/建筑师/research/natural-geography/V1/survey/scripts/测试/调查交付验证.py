"""独立读取已完成的调查数据库，检查解析器一致性、查询与工程依赖；仅写验证报告。"""
import ast
import hashlib
import json
import random
import sqlite3
import sys
import io
import zlib
import gzip
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'scripts'))
sys.path.insert(0,str(ROOT.parents[1]/'AI-Blueprints'/'参考入库'/'第三方'))
from L3_外交层.自然调查接口 import rebuild_views
import nbtlib

def main():
    db=sqlite3.connect((ROOT/'raw'/'geography.sqlite').as_uri()+'?mode=ro',uri=True)
    m=json.loads(db.execute("SELECT value FROM meta WHERE key='manifest'").fetchone()[0])
    result={'schema_version':m['schema_version'],'integrity_check':db.execute('PRAGMA integrity_check').fetchone()[0]}
    result['counts']={t:db.execute(f'SELECT count(*) FROM {t}').fetchone()[0] for t in ('chunks','chunk_status','samples','cells','adjacency')}
    result['object_counts']=dict(db.execute('SELECT family,count(*) FROM objects WHERE active=1 GROUP BY family'))
    result['terrain_distribution']=[dict(zip(('type','cells','mean_elevation','max_elevation'),r)) for r in db.execute('SELECT terrain,count(*),avg(elevation),max(elevation) FROM cells GROUP BY terrain ORDER BY count(*) DESC')]
    result['biome_top20']=[dict(zip(('biome','cells'),r)) for r in db.execute('SELECT biome,count(*) FROM cells GROUP BY biome ORDER BY count(*) DESC LIMIT 20')]
    # 生产状态读取器使用跳过载荷的解析；此处使用完整 nbtlib 解码作独立交叉对照。
    world=Path(m['world_path']);source=json.loads((ROOT/'manifest'/'source-before.json').read_text(encoding='utf-8'))
    rng=random.Random(4903);chosen=[];result['status_parser_crosschecks']=[]
    for (status,) in db.execute('SELECT DISTINCT status FROM chunk_status'):
        rows=db.execute('SELECT c.cx,c.cz,c.region,c.sector,s.status,s.data_version FROM chunks c JOIN chunk_status s USING(cx,cz) WHERE s.status=?',(status,)).fetchall()
        chosen.extend(rng.sample(rows,min(8,len(rows))))
    for cx,cz,rel,sector,status,dv in chosen:
        raw=(world/rel).read_bytes()
        if hashlib.sha256(raw).hexdigest()!=source[rel]['sha256']:raise ValueError('验证源文件已变化')
        pos=sector*4096;n=int.from_bytes(raw[pos:pos+4],'big');compression=raw[pos+4]
        data=raw[pos+5:pos+4+n]
        if compression&128:data=(world/rel).parent.joinpath(f'c.{cx}.{cz}.mcc').read_bytes()
        if compression&127==2:data=zlib.decompress(data)
        elif compression&127==1:data=gzip.decompress(data)
        elif compression&127!=3:raise ValueError('unsupported compression')
        d=nbtlib.File.parse(io.BytesIO(data))
        ok=(int(d['xPos']),int(d['zPos']),str(d['Status']),int(d['DataVersion']))==(cx,cz,status,dv)
        result['status_parser_crosschecks'].append({'cx':cx,'cz':cz,'status':status,'pass':ok})
    result['coordinate_queries']=[]
    for id,raw in db.execute("SELECT id,details FROM objects WHERE family='SITE' AND active=1"):
        d=json.loads(raw);p=d['representative'];gx=p['x']//64;gz=p['z']//64
        row=db.execute('SELECT geo_id,terrain FROM cells WHERE gx=? AND gz=?',(gx,gz)).fetchone()
        status=db.execute('SELECT status FROM chunk_status WHERE cx=? AND cz=?',(p['x']//16,p['z']//16)).fetchone()
        members=[r[0] for r in db.execute('SELECT m.id FROM members m JOIN objects o USING(id) WHERE gx=? AND gz=? AND o.active=1',(gx,gz))]
        result['coordinate_queries'].append({'site':id,'point':p,'geo':row,'chunk_status':status,'members':members,'pass':id in members and status[0]=='minecraft:full'})
    result['unassigned_cells']=db.execute('SELECT count(*) FROM cells WHERE geo_id IS NULL').fetchone()[0]
    result['overlapping_geo_assignments']=db.execute("SELECT count(*) FROM (SELECT gx,gz,count(*) n FROM members JOIN objects USING(id) WHERE active=1 AND family='GEO' GROUP BY gx,gz HAVING n<>1)").fetchone()[0]
    result['world_audit']=json.loads((ROOT/'manifest'/'write-audit.json').read_text(encoding='utf-8'))
    violations=[]
    for path in (ROOT/'scripts').rglob('*.py'):
        tree=ast.parse(path.read_text(encoding='utf-8'),filename=str(path))
        layer=next((int(part[1]) for part in path.parts if part.startswith(('L0_','L1_','L2_','L3_'))),None)
        for node in ast.walk(tree):
            if isinstance(node,ast.ImportFrom) and node.module and node.module.startswith(('L0_','L1_','L2_','L3_')) and layer is not None:
                if int(node.module[1])>layer:violations.append(str(path)+': '+node.module)
    result['architecture_upward_imports']=violations
    def derivatives():
        return {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for directory in ('atlas','sites','visual') for p in (ROOT/directory).glob('*') if p.is_file()} | {'reports/summary.md':hashlib.sha256((ROOT/'reports'/'summary.md').read_bytes()).hexdigest()}
    rebuild_views(ROOT);before=derivatives();rebuild_views(ROOT);after=derivatives()
    result['derivative_regeneration_byte_identical']=before==after
    result['derived_file_count']=len(after)
    result['pass']=result['integrity_check']=='ok' and not violations and not result['unassigned_cells'] and not result['overlapping_geo_assignments'] and result['derivative_regeneration_byte_identical'] and all(r['pass'] for r in result['coordinate_queries']+result['status_parser_crosschecks']) and result['world_audit']['source_inventory_and_sha256_equal']
    (ROOT/'reports'/'delivery-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('pass','counts','object_counts','architecture_upward_imports','derivative_regeneration_byte_identical')}))
    if not result['pass']:raise SystemExit(1)

if __name__=='__main__':main()
