"""恢复细节阶段误覆盖的湿岸与水体，并清除失去土壤支承的草本。"""
from pathlib import Path
import json,gzip,numpy as np
R=Path(__file__).parent;E=R/'证据';s=json.loads((R/'场景.json').read_text(encoding='utf8'));P=s['palette'];old=np.load(R/'阶段03a.npy');v=old.copy();prior=np.load(R/'阶段02.npy');herbs=[i for i,p in enumerate(P) if p in ['minecraft:fern','minecraft:short_grass','minecraft:allium','minecraft:blue_orchid','minecraft:lily_of_the_valley']]
wet=[i for i,p in enumerate(P) if p.split('[')[0] in ['minecraft:water','minecraft:mud']];mask=np.isin(v,herbs)&np.isin(prior,wet);v[mask]=prior[mask];restored=int(mask.sum())
soils=[i for i,p in enumerate(P) if p.split('[')[0] in ['minecraft:grass_block','minecraft:dirt','minecraft:coarse_dirt','minecraft:podzol','minecraft:moss_block','minecraft:mud']];removed=[]
for x,y,z in np.argwhere(np.isin(v,herbs)):
 if y==0 or v[x,y-1,z] not in soils:removed.append([int(x),int(y+56),int(z),P[int(v[x,y,z])]]);v[x,y,z]=0
np.save(R/'阶段03b.npy',v);b=[[int(x),int(y+56),int(z),int(v[x,y,z])] for x,y,z in np.argwhere(v!=old)];folder=R/'蓝图/03b';folder.mkdir(exist_ok=True)
lo=np.array(b)[:,:3].min(0).tolist();hi=np.array(b)[:,:3].max(0).tolist()
bp={'schema_version':1,'origin':dict(zip(['x','y','z'],lo)),'dimensions':dict(zip(['x','y','z'],[c-a+1 for a,c in zip(lo,hi)])),'palette':P,'blocks':[[x-lo[0],y-lo[1],z-lo[2],p] for x,y,z,p in b]}
with gzip.open(folder/'湿岸.json.gz','wt',encoding='utf8') as f:json.dump(bp,f,separators=(',',':'))
(R/'作业/03b.json').write_text(json.dumps({'world_path':'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V14-T05-森林圣所','phases':[{'palette':P,'operations':[[x,y,z,x,y,z,p] for x,y,z,p in b]}]},separators=(',',':')),encoding='utf8')
rep={'restored_wet_cells':restored,'removed_unsupported_herbs':removed,'total_changes':len(b)};(E/'湿岸植被修订.json').write_text(json.dumps(rep,ensure_ascii=False,indent=2),encoding='utf8');print(rep)
