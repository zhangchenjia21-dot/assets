"""玩家高度透视发现西厢南端超出台地四格；补齐真实基础，不改变上部建筑。"""
from pathlib import Path
import numpy as np,json,gzip
R=Path(__file__).parent;s=json.loads((R/'场景.json').read_text(encoding='utf8'));P=s['palette'];V=np.load(R/'阶段4.npy');old=V.copy()
stone=P.index('minecraft:stone');rough=P.index('minecraft:cobblestone')
V[105:120,0:31,123:127]=stone
V[105,0:31,123:127]=rough;V[119,0:31,123:127]=rough;V[105:120,0:31,126]=rough
rows=[[int(x),int(y),int(z),int(V[x,y,z])] for x,y,z in np.argwhere(V!=old)]
lo=[min(r[a] for r in rows) for a in range(3)];hi=[max(r[a] for r in rows) for a in range(3)]
bp={'schema_version':1,'origin':{'x':lo[0],'y':lo[1]+63,'z':lo[2]},'dimensions':dict(zip(['x','y','z'],[b-a+1 for a,b in zip(lo,hi)])),'palette':P,'blocks':[[x-lo[0],y-lo[1],z-lo[2],p] for x,y,z,p in rows],'metadata':{'task':'MB-V11-T02','stage':'west-wing-foundation-repair'}}
folder=R/'蓝图/05-西厢基础修订';folder.mkdir(exist_ok=True)
with gzip.open(folder/'基础.json.gz','wt',encoding='utf8') as f:json.dump(bp,f,separators=(',',':'))
(R/'作业/05.json').write_text(json.dumps({'world_path':s['world'],'phases':[{'palette':P,'operations':[[x,y+63,z,x,y+63,z,p] for x,y,z,p in rows]}]},separators=(',',':')),encoding='utf8');np.save(R/'阶段5.npy',V);print(len(rows))
