import json
import random
import time
import hashlib
import sys
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
import nbtlib
from L0_公理层.地理契约 import SCHEMA,ALGORITHM,STEP,neighbors
from L1_器件层.存档读取器 import ReadGuard,fingerprint,header,chunk,columns,verify_column
from L1_器件层.地理存储器 import connect,write_json,put_meta
from L1_器件层.地貌推导器 import components,derive_cells,build_atlas
from L1_器件层.地图生成器 import render,report
from L1_器件层.区块状态读取器 import region_metadata

def run(world,out):
    """持只读共享句柄扫描；仅输出目录允许落盘，任何格式或验证错误终止。"""
    started=datetime.now(timezone.utc).isoformat()
    write_json(out/'manifest'/'toolchain.json',{'schema':SCHEMA,'algorithm':ALGORITHM,'python':sys.version,'nbtlib':nbtlib.__version__,'nbtlib_path':nbtlib.__file__,'scripts_sha256':{p.relative_to(out).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (out/'scripts').rglob('*.py')}})
    with ReadGuard(world) as guard:
        print(f'guard held: {len(guard.handles)} files',flush=True)
        before=fingerprint(world);write_json(out/'manifest'/'source-before.json',before)
        level=nbtlib.load(world/'level.dat')['Data']
        if str(level['LevelName'])!='建筑师':raise ValueError('目标 LevelName 不匹配')
        if int(level['DataVersion'])!=4903:raise ValueError('未验证的 DataVersion')
        db=connect(out/'raw'/'geography.sqlite')
        previous=db.execute("SELECT value FROM meta WHERE key='world_path'").fetchone()
        if previous and json.loads(previous[0])!=str(world):raise ValueError('数据库绑定其他世界')
        put_meta(db,'world_path',str(world));put_meta(db,'schema',SCHEMA)
        dimension_dirs=sorted(p for p in world.rglob('region') if p.is_dir())
        dimensions=[{'region_path':p.relative_to(world).as_posix(),'region_files':len(list(p.glob('*.mca')))} for p in dimension_dirs]
        region_dir=world/'dimensions'/'minecraft'/'overworld'/'region'
        if region_dir not in dimension_dirs:raise ValueError('未发现 26.2 主世界目录')
        files=sorted(region_dir.glob('*.mca'));db.execute('DELETE FROM chunks')
        locations={};region_rows={}
        for p in files:
            rel=p.relative_to(world).as_posix();rows=header(p);region_rows[rel]=rows
            for cx,cz,sector,sectors,timestamp in rows:
                if sector<2 or (sector+sectors)*4096>p.stat().st_size:raise ValueError('越界 region location')
                locations[(cx,cz)]=(p,sector)
            db.executemany('INSERT INTO chunks VALUES (?,?,?,?,?,?,NULL)',[(cx,cz,rel,s,n,t) for cx,cz,s,n,t in rows])
        groups=sorted(components(locations),key=lambda g:(-len(g),min(g)))
        coverage_components=[]
        for i,g in enumerate(groups,1):
            db.executemany('UPDATE chunks SET component=? WHERE cx=? AND cz=?',[(i,*p) for p in g])
            coverage_components.append({'id':i,'chunks':len(g),'chunk_bounds':[min(p[0] for p in g),min(p[1] for p in g),max(p[0] for p in g),max(p[1] for p in g)]})
        xs=[p[0] for p in locations];zs=[p[1] for p in locations]
        bounds=[min(xs),min(zs),max(xs),max(zs)]
        # 缺失区块区分外部背景与真正封闭的洞；不把圆形外角当作 Chunky 失败。
        missing={(x,z) for x in range(bounds[0],bounds[2]+1) for z in range(bounds[1],bounds[3]+1) if (x,z) not in locations}
        holes=[]
        for g in components(missing):
            exterior=any(x in (bounds[0],bounds[2]) or z in (bounds[1],bounds[3]) for x,z in g)
            if not exterior:holes.append({'chunks':len(g),'chunk_bounds':[min(p[0] for p in g),min(p[1] for p in g),max(p[0] for p in g),max(p[1] for p in g)]})
        coverage={'region_files':len(files),'present_chunk_headers':len(locations),'chunk_bounds':bounds,'block_bounds':[bounds[0]*16,bounds[1]*16,bounds[2]*16+15,bounds[3]*16+15],'components':coverage_components,'absent_in_bbox':len(missing),'enclosed_holes':holes,'meaning':'header-present; full generation status inspected only on sampled chunks'}
        write_json(out/'manifest'/'coverage.json',coverage);db.commit()
        coverage['empty_region_files']=[p.name for p in files if p.stat().st_size==0]
        write_json(out/'manifest'/'coverage.json',coverage)
        print(f'header coverage: {len(locations)} chunks, {len(groups)} components',flush=True)
        for (rel,) in db.execute('SELECT path FROM status_regions').fetchall():
            if rel not in region_rows:
                db.execute('DELETE FROM status_regions WHERE path=?',(rel,))
                db.execute('DELETE FROM chunk_status WHERE region=?',(rel,))
        for ix,p in enumerate(files):
            rel=p.relative_to(world).as_posix();digest=before[rel]['sha256']
            old=db.execute('SELECT sha256 FROM status_regions WHERE path=?',(rel,)).fetchone()
            if old and old[0]==digest:continue
            rows=region_metadata(p,region_rows[rel])
            db.execute('DELETE FROM chunk_status WHERE region=?',(rel,))
            db.executemany('INSERT INTO chunk_status VALUES (?,?,?,?,?)',[(cx,cz,status,dv,rel) for cx,cz,status,dv in rows])
            db.execute('INSERT OR REPLACE INTO status_regions VALUES (?,?)',(rel,digest));db.commit()
            if ix%20==0:print(f'full-status audit regions {ix+1}/{len(files)}',flush=True)
        db.execute('DELETE FROM chunk_status WHERE NOT EXISTS(SELECT 1 FROM chunks c WHERE c.cx=chunk_status.cx AND c.cz=chunk_status.cz)')
        full={(cx,cz) for cx,cz in db.execute("SELECT cx,cz FROM chunk_status WHERE status='minecraft:full'")}
        full_groups=sorted(components(full),key=lambda g:(-len(g),min(g)))
        full_bounds=[min(p[0] for p in full),min(p[1] for p in full),max(p[0] for p in full),max(p[1] for p in full)]
        coverage['all_chunk_status_counts']=dict(db.execute('SELECT status,count(*) FROM chunk_status GROUP BY status'))
        coverage['full_chunk_bounds']=full_bounds
        coverage['full_block_bounds']=[full_bounds[0]*16,full_bounds[1]*16,full_bounds[2]*16+15,full_bounds[3]*16+15]
        coverage['full_components']=[{'chunks':len(g),'chunk_bounds':[min(p[0] for p in g),min(p[1] for p in g),max(p[0] for p in g),max(p[1] for p in g)]} for g in full_groups]
        coverage['nonfull_or_absent_in_full_bbox']=sum((x,z) not in full for x in range(full_bounds[0],full_bounds[2]+1) for z in range(full_bounds[1],full_bounds[3]+1))
        coverage['meaning']='All location entries and all chunk Status/DataVersion audited; use full_block_bounds for completed terrain, not header bounds.'
        write_json(out/'manifest'/'coverage.json',coverage);db.commit()
        print('full coverage '+json.dumps({k:v for k,v in coverage.items() if k.startswith('full') or k.startswith('all_chunk') or k=='nonfull_or_absent_in_full_bbox'}),flush=True)
        # 每个 64 格单元固定选左上区块；仅边缘无该区块时使用该单元内坐标最小的现有区块。
        selected={}
        for cx,cz in sorted(full):
            selected.setdefault((cx//4,cz//4),(cx,cz))
        selected_set=set(selected.values());status=Counter();scanned=0;cached=0;errors=[]
        current_regions=set(region_rows)
        for (old,) in db.execute('SELECT path FROM regions').fetchall():
            if old not in current_regions:
                db.execute('DELETE FROM samples WHERE region=?',(old,));db.execute('DELETE FROM regions WHERE path=?',(old,))
        old_algorithm=db.execute("SELECT value FROM meta WHERE key='algorithm'").fetchone()
        for ix,p in enumerate(files):
            rel=p.relative_to(world).as_posix();digest=before[rel]['sha256']
            previous_hash=db.execute('SELECT sha256 FROM regions WHERE path=?',(rel,)).fetchone()
            if previous_hash and previous_hash[0]==digest and old_algorithm and json.loads(old_algorithm[0])==ALGORITHM:
                cached+=1;continue
            db.execute('DELETE FROM samples WHERE region=?',(rel,))
            for cx,cz,sector,n,t in region_rows[rel]:
                if (cx,cz) not in selected_set:continue
                d=chunk(p,sector,cx,cz);status[str(d['Status'])]+=1
                if str(d['Status'])!='minecraft:full':
                    errors.append({'cx':cx,'cz':cz,'status':str(d['Status'])});continue
                for sample in columns(d):
                    db.execute('INSERT INTO samples VALUES (?,?,?,?,?,?)',(sample['x'],sample['z'],cx,cz,rel,json.dumps(sample)))
                scanned+=1
            db.execute('INSERT OR REPLACE INTO regions VALUES (?,?)',(rel,digest));db.commit()
            if ix%20==0:print(f'regions {ix+1}/{len(files)}, sampled chunks {scanned}, cached regions {cached}',flush=True)
        put_meta(db,'algorithm',ALGORITHM)
        checks=[]
        sample_rows=db.execute('SELECT cx,cz,observed FROM samples WHERE x%16 IN (8,-8)').fetchall()
        # 同时覆盖随机点、水面与最高点；验证从原始区块重新读取。
        rng=random.Random(4903)
        chosen=rng.sample(sample_rows,min(40,len(sample_rows)))
        water_rows=[r for r in sample_rows if json.loads(r[2])['water']]
        chosen+=rng.sample(water_rows,min(10,len(water_rows)))
        chosen+=sorted(sample_rows,key=lambda r:-json.loads(r[2])['surface_y'])[:5]
        for cx,cz,raw in chosen:
            path,sector=locations[(cx,cz)];checks.append(verify_column(chunk(path,sector,cx,cz),json.loads(raw)))
        write_json(out/'reports'/'sample-validation.json',checks)
        if not all(c['pass'] for c in checks):raise ValueError('原始区块交叉验证失败')
        print(f'verified {len(checks)} samples; deriving atlas',flush=True)
        cells=derive_cells(db);objects=build_atlas(db,cells);db.commit()
        after=fingerprint(world);write_json(out/'manifest'/'source-after.json',after)
        unchanged=before==after
        write_json(out/'manifest'/'write-audit.json',{'world_writes_by_tool':0,'source_inventory_and_sha256_equal':unchanged,'files':len(before),'total_bytes':sum(r['size'] for r in before.values()),'guard':'CreateFileW GENERIC_READ FILE_SHARE_READ; held for every original source file throughout scan; denies source writes/deletes','new_or_deleted_files':sorted(set(before)^set(after)),'changed':[p for p in before.keys()&after.keys() if before[p]!=after[p]]})
        if not unchanged:raise ValueError('源存档发生变化；调查不可验收')
        limitations=['64 格网格仅在每个单元的一个区块采五柱；跨格水体连通与狭窄地形可能漏检，面积为外推估计。','GEO 是阈值分类的连通分区，存在碎片与类别交错，不等同于语义完整的山脉或流域。','surface_y 包括树冠；exposed_y 只剥离显式植被，不能可靠消除所有植物、人工建筑、冰面或悬空地形。','河流、岛屿、半岛、谷地、山口等均是待复核候选；未证明真实河道连续性和流向。','汇流点、天然港口、瀑布、流域和高差水流转换没有可靠证据，保持 uncertain；海洋命名结合水方块与 biome，不依据 biome 独立判定。','边界触及对象是截断观测，不能判断世界外侧连通；全区块状态已审计，详细地形只解码采样区块。','未进行游戏内现场视觉复核：正式执行器会保存世界，退役 Observation/Bridge 不恢复；地图仅为离线派生证据。','对象 confidence 是启发式可信度标记，未经统计校准；局部规则阈值需在后续精查验证。']
        m={'schema_version':SCHEMA,'algorithm':ALGORITHM,'status':'PARTIAL','world_name':str(level['LevelName']),'world_path':str(world),'minecraft':str(level['Version']['Name']),'data_version':int(level['DataVersion']),'dimension':'minecraft:overworld','dimensions_on_disk':dimensions,'data_packs':[str(x) for x in level['DataPacks']['Enabled']],'started_at':started,'finished_at':datetime.now(timezone.utc).isoformat(),'coverage':coverage,'sampling_grid_blocks':STEP,'columns_per_sampled_chunk':5,'sampled_chunks':len(cells),'sample_columns':db.execute('SELECT count(*) FROM samples').fetchone()[0],'selected_cells':len(selected),'sample_coverage':len(cells)/len(selected),'new_scan_status_counts':dict(status),'skipped_nonfull_chunks':errors,'cached_region_count':cached,'world_writes':0,'hashes_equal':unchanged,'validation_points':len(checks),'object_counts':dict(Counter(o['family'] for o in objects)),'limitations':limitations,'status_reason':'基础事实层与校验已完成；高级形态识别仍为粗网格候选，现场视觉复核尚未进行。'}
        put_meta(db,'manifest',m);db.commit();write_json(out/'manifest'/'survey.json',m)
        render(db,out);report(db,out)
        integrity=db.execute('PRAGMA integrity_check').fetchone()[0]
        write_json(out/'reports'/'database-validation.json',{'integrity_check':integrity,'cells_without_geo':db.execute('SELECT count(*) FROM cells WHERE geo_id IS NULL').fetchone()[0],'active_objects_without_members':db.execute('SELECT count(*) FROM objects o WHERE active=1 AND NOT EXISTS(SELECT 1 FROM members m WHERE m.id=o.id)').fetchone()[0]})
        db.close();print(json.dumps({k:m[k] for k in ('status','sampled_chunks','sample_columns','sample_coverage','object_counts','hashes_equal')}),flush=True)

def regenerate(out):
    db=connect(out/'raw'/'geography.sqlite');render(db,out);report(db,out);db.close()
