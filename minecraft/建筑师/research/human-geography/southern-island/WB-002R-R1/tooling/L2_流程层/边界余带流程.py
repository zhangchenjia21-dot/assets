"""整带缺块时读取仍存在的完整子矩形；不因最后一行缺块丢弃可读余带。"""
import json,sqlite3
from contextlib import ExitStack
from datetime import datetime,timezone
import numpy as np
from L1_器件层.源快照保护器 import ReadGuard,fingerprint,write_json
from L1_器件层.区域柱读取器 import Reader
from L1_器件层.区域指标计算器 import components

def extend(out,world):
    roots={'world':world,'WB-002R':out.parent/'WB-002R',**{n:out.parents[2]/'natural-geography'/n for n in ('V1','NG-2','NG-3')}}
    baseline=json.loads((out/'manifest/source-before.json').read_text(encoding='utf-8'))
    scope=json.loads((out/'profile/scope-completion.json').read_text(encoding='utf-8'))
    missing=json.loads((out/'manifest/missing-expansion-chunks.json').read_text(encoding='utf-8'))
    bounds=missing['proposed_bounds'];bounds[3]=min(z for x,z in missing['missing'])*16-1
    assert bounds[3]>scope['bounds'][3]
    assert all(z*16>bounds[3] for x,z in missing['missing'])
    # 实际探测到 z=218 的边缘区块仅 initialize_light；存在 region slot 不等于 full。
    bounds[3]=min(bounds[3],3487)
    with ExitStack() as stack:
        for root in roots.values():stack.enter_context(ReadGuard(root))
        assert {n:fingerprint(p) for n,p in roots.items()}==baseline
        write_json(out/'manifest/nonfull-boundary.json',{'chunk':[-50,218],'block_z':3488,'DataVersion':4903,'status':'minecraft:initialize_light','failed_proposed_bounds':missing['proposed_bounds'],'policy':'Only minecraft:full chunks accepted; no generation or world writes'})
        db=sqlite3.connect(out/'raw-or-queryable/observed.sqlite');reader=Reader(world,db);existing=set(db.execute('SELECT cx,cz FROM chunks'))
        needed=[(cx,cz) for cz in range(bounds[1]//16,bounds[3]//16+1) for cx in range(bounds[0]//16,bounds[2]//16+1) if (cx,cz) not in existing]
        for i,(cx,cz) in enumerate(needed):
            db.executemany('INSERT INTO samples VALUES ('+','.join('?'*14)+')',[tuple(map(int,r)) for r in reader.read(cx,cz)])
            if i%256==0:db.commit();print('available boundary band',i,'/',len(needed),flush=True)
        db.commit()
        x0,z0,x1,z1=bounds
        wet=np.fromiter((r[0]!=-32768 for r in db.execute('SELECT water_y FROM samples ORDER BY z,x')),dtype=bool).reshape(z1-z0+1,x1-x0+1)
        labels=components(~wet);target=int(labels[1800-z0,400-x0]);zz,xx=np.where(labels==target)
        contacts={'west':bool(xx.min()==0),'east':bool(xx.max()==x1-x0),'north':bool(zz.min()==0),'south':bool(zz.max()==z1-z0)}
        trace=json.loads((out/'manifest/expansion-trace.json').read_text(encoding='utf-8'))
        entry={'bounds':bounds,'columns':int(wet.size),'east_target_area':len(xx),'east_target_bounds':[int(xx.min()+x0),int(zz.min()+z0),int(xx.max()+x0),int(zz.max()+z0)],'boundary_contacts':contacts,'new_chunks':len(needed),'reason':'Read available rows before missing chunk row; keep complete 1-block rectangle'}
        trace.append(entry);write_json(out/'manifest/expansion-trace.json',trace)
        scope.update(bounds=bounds,scope_complete=not any(contacts.values()),east_mountain_landmass_touches_study_boundary=any(contacts.values()),status='CENSORED_AT_WORLD_OR_SAFETY_BOUND' if any(contacts.values()) else 'CLOSED_WITHIN_STUDY')
        scope['relevant_region_hashes']={r:baseline['world'][r]['sha256'] for r, in db.execute('SELECT DISTINCT region FROM chunks ORDER BY region')};db.close()
        write_json(out/'profile/scope-completion.json',scope)
        after={n:fingerprint(p) for n,p in roots.items()};assert after==baseline
        write_json(out/'validation/boundary-band-source-audit.json',{'all_sources_unchanged':True,'world_writes':0,'checked_at':datetime.now(timezone.utc).isoformat()})
        print(json.dumps(entry),flush=True)
