"""增量复用同哈希区域，逐轮追踪东侧主陆体；不向世界请求写句柄。"""
import json,sqlite3,shutil
from pathlib import Path
from contextlib import ExitStack
from datetime import datetime,timezone
import numpy as np
from L1_器件层.源快照保护器 import ReadGuard,fingerprint,write_json
from L1_器件层.区域柱读取器 import Reader
from L1_器件层.区域指标计算器 import components

def execute(out,world):
    old=out.parent/'WB-002R'
    natural=out.parents[2]/'natural-geography'
    roots={'world':world,'WB-002R':old,**{n:natural/n for n in ('V1','NG-2','NG-3')}}
    for n in ('manifest','validation','raw-or-queryable','profile','reports','visual'): (out/n).mkdir(exist_ok=True)
    baseline=out/'manifest/source-before.json'
    if baseline.exists():raise ValueError('已有基线，不得覆盖')
    with ExitStack() as stack:
        for root in roots.values():stack.enter_context(ReadGuard(root))
        before={n:fingerprint(p) for n,p in roots.items()}
        write_json(baseline,before)
        previous=json.loads((old/'manifest/current-source-before.json').read_text(encoding='utf-8'))
        path=out/'raw-or-queryable/observed.sqlite'
        shutil.copyfile(old/'raw-or-queryable/observed.sqlite',path)
        db=sqlite3.connect(path)
        changed=[r for (r,) in db.execute('SELECT DISTINCT region FROM chunks') if before['world'][r]['sha256']!=previous['world'][r]['sha256']]
        refresh=list(db.execute('SELECT cx,cz FROM chunks WHERE region IN ('+','.join('?'*len(changed))+')',changed)) if changed else []
        for cx,cz in refresh:
            for table in ('samples','vegetation'):db.execute(f'DELETE FROM {table} WHERE x BETWEEN ? AND ? AND z BETWEEN ? AND ?',(cx*16,cx*16+15,cz*16,cz*16+15))
            db.execute('DELETE FROM vegetation_palette WHERE cx=? AND cz=?',(cx,cz))
            db.execute('DELETE FROM chunks WHERE cx=? AND cz=?',(cx,cz))
        reader=Reader(world,db)
        def read_chunk(cx,cz):
            db.executemany('INSERT INTO samples VALUES ('+','.join('?'*14)+')',[tuple(map(int,r)) for r in reader.read(cx,cz)])
        for cx,cz in refresh:read_chunk(cx,cz)
        db.commit()
        write_json(out/'manifest/reuse.json',{'changed_regions':changed,'refreshed_chunks':len(refresh),'reused_chunks':6080-len(refresh),'reused_columns':(6080-len(refresh))*256,'predecessor':'WB-002R/current-source-before.json','checked_at':datetime.now(timezone.utc).isoformat()})
        bounds=[-800,1376,415,2655];trace=[];status=None
        while True:
            x0,z0,x1,z1=bounds
            wet=np.fromiter((r[0]!=-32768 for r in db.execute('SELECT water_y FROM samples ORDER BY z,x')),dtype=bool).reshape(z1-z0+1,x1-x0+1)
            labels=components(~wet);target=int(labels[1800-z0,400-x0]);assert target
            zz,xx=np.where(labels==target)
            contacts={'west':bool(xx.min()==0),'east':bool(xx.max()==x1-x0),'north':bool(zz.min()==0),'south':bool(zz.max()==z1-z0)}
            entry={'bounds':bounds.copy(),'columns':int(wet.size),'east_target_area':len(xx),'east_target_bounds':[int(xx.min()+x0),int(zz.min()+z0),int(xx.max()+x0),int(zz.max()+z0)],'boundary_contacts':contacts,'decoded_chunks_cumulative':reader.decoded}
            trace.append(entry);write_json(out/'manifest/expansion-trace.json',trace);print(json.dumps(entry),flush=True)
            if not any(contacts.values()):status='CLOSED_WITHIN_STUDY';break
            new=[x0-512*contacts['west'],z0-512*contacts['north'],x1+512*contacts['east'],z1+512*contacts['south']]
            if any(abs(v-o)>2048 for v,o in zip(new,[-800,1376,415,2655])):status='CENSORED_AT_WORLD_OR_SAFETY_BOUND';break
            existing=set(db.execute('SELECT cx,cz FROM chunks'));needed=[(cx,cz) for cz in range(new[1]//16,new[3]//16+1) for cx in range(new[0]//16,new[2]//16+1) if (cx,cz) not in existing]
            missing=[]
            for cx,cz in needed:
                p=world/'dimensions/minecraft/overworld/region'/f'r.{cx//32}.{cz//32}.mca'
                if not p.exists():missing.append([cx,cz]);continue
                if p not in reader.headers:
                    with p.open('rb') as f:reader.headers[p]=f.read(8192)
                i=(cz%32)*32+cx%32
                if not int.from_bytes(reader.headers[p][4*i:4*i+4],'big'):missing.append([cx,cz])
            if missing:
                write_json(out/'manifest/missing-expansion-chunks.json',{'proposed_bounds':new,'missing':missing});status='CENSORED_AT_WORLD_OR_SAFETY_BOUND';break
            for i,(cx,cz) in enumerate(needed):
                read_chunk(cx,cz)
                if i%256==0:db.commit();print('expansion chunks',i,'/',len(needed),flush=True)
            db.commit();bounds=new
        relevant=[r for r, in db.execute('SELECT DISTINCT region FROM chunks ORDER BY region')]
        db.close()
        write_json(out/'profile/scope-completion.json',{'status':status,'scope_complete':status=='CLOSED_WITHIN_STUDY','east_mountain_landmass_touches_study_boundary':any(contacts.values()),'bounds':bounds,'anchor':[400,1800],'trace':'manifest/expansion-trace.json','resolution_blocks':1,'relevant_region_hashes':{r:before['world'][r]['sha256'] for r in relevant}})
        after={n:fingerprint(p) for n,p in roots.items()}
        write_json(out/'validation/extraction-source-audit.json',{'all_sources_unchanged':before==after,'world_writes':0,'immutable':{n:before[n]==after[n] for n in roots if n!='world'},'checked_at':datetime.now(timezone.utc).isoformat()})
        assert before==after
