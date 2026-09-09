"""逐体素对照最终设计与实存，另核对主路净空与连续标高。"""
from pathlib import Path
import numpy as np,json,hashlib,gzip
R=Path(__file__).parent;E=R/'证据';s=json.loads((R/'场景.json').read_text(encoding='utf8'));meta=json.loads((E/'阶段5-实存.json').read_text(encoding='utf8'));actual=np.fromfile(E/'阶段5-实存.bin',np.uint8).reshape(meta['size']);expected=np.load(R/'阶段5.npy')
def canonical(p):
 if '[' not in p:return p
 a,b=p.split('[');return a+'['+','.join(sorted(b[:-1].split(',')))+']'
states=[canonical(p) for p in s['palette']];mapping=np.array([states.index(canonical(p)) if canonical(p) in states else 255 for p in meta['palette']],np.uint8);diff=mapping[actual]!=expected
unique,count=np.unique(actual[diff],return_counts=True);examples=np.argwhere(diff)[:20]
route=s['routes'][0]['cells'];bad=[];levels=[]
for x,y,z in route:
 if any('minecraft:air'!=meta['palette'][actual[x,y+k-63,z]] for k in [1,2]):bad.append([x,y,z])
 levels.append(y)
rep={'world':s['world'],'compared_voxels':int(actual.size),'different_voxels':int(diff.sum()),'different_actual_states':{meta['palette'][int(i)]:int(c) for i,c in zip(unique,count)},'difference_examples':[[int(x),int(y+63),int(z)] for x,y,z in examples],'main_route_center_samples':len(route),'main_route_blocked_center_samples':bad,'main_route_max_height_step':max(abs(a-b) for a,b in zip(levels,levels[1:])),'note':'主路净空按两整格；斜向采样结合连通性图，不替代真人客户端行走。','skill_sha256':hashlib.sha256((R/'来源/minecraft-builder-v1.1.md').read_bytes()).hexdigest()}
(E/'最终逐格核验.json').write_text(json.dumps(rep,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(rep,ensure_ascii=False))
buildings=[('教堂',108,72,156,90,96),('钟塔',102,70,109,77,96),('东厢',154,95,168,119,94),('西厢',105,100,119,126,94),('食堂',120,124,154,136,90),('客舍',78,128,97,142,82),('服务房',75,110,86,121,86),('门楼',62,149,72,157,76)]
airids=[i for i,p in enumerate(meta['palette']) if p=='minecraft:air'];support={name:{'floor_y':y,'air_cells_immediately_below_floor':int(np.isin(actual[x:X+1,y-64,z:Z+1],airids).sum())} for name,x,z,X,Z,y in buildings}
(E/'最终基础接触.json').write_text(json.dumps(support,ensure_ascii=False,indent=2),encoding='utf8')
# 审计数据压缩后仍可逐字节还原；不是完整存档。
for n in [1,2,3,4,5]:
 p=E/f'阶段{n}-实存.bin'
 with gzip.open(str(p)+'.gz','wb',compresslevel=9) as f:f.write(p.read_bytes())
# 仅任务候选：提取已用的大冠幅松，限定材质与包围盒，绝不调用资产晋升接口。
t=next(t for t in s['trees'] if t[0]==57 and t[2]==99);x,y,z,hh,r,kind=t;rows=[]
for xx in range(x-10,x+11):
 for yy in range(y,y+hh+4):
  for zz in range(z-9,z+10):
   p=meta['palette'][actual[xx,yy-63,zz]]
   if ('spruce_leaves' in p or 'oak_log' in p):rows.append((xx,yy,zz,p))
mins=[min(r[i] for r in rows) for i in range(3)];maxs=[max(r[i] for r in rows) for i in range(3)];pal=sorted(set(r[3] for r in rows));bp={'schema_version':1,'origin':dict(zip(['x','y','z'],mins)),'dimensions':dict(zip(['x','y','z'],[b-a+1 for a,b in zip(mins,maxs)])),'palette':pal,'blocks':[[x-mins[0],y-mins[1],z-mins[2],pal.index(p)] for x,y,z,p in rows],'metadata':{'temporary_id':'T02-C01','name':'坡地偏冠伞松','status':'CANDIDATE_ONLY','formal_library_registration':False}}
(R/'候选').mkdir(exist_ok=True);(R/'候选/T02-C01.json').write_text(json.dumps(bp,ensure_ascii=False,separators=(',',':')),encoding='utf8');print('CANDIDATE',mins,bp['dimensions'],len(rows))
