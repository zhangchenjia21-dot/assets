"""将桥脚分隔出的两格水袋回填湿岸土，不切割桥体和主水道。"""
from pathlib import Path
import json,gzip,numpy as np
R=Path(__file__).parent;s=json.loads((R/'场景.json').read_text(encoding='utf8'));P=s['palette'];v=np.load(R/'阶段03.npy');b=[]
for y in [64,65]:
 assert P[int(v[107,y-56,174])].split('[')[0]=='minecraft:water'
 p=P.index('minecraft:mud');v[107,y-56,174]=p;b.append([0,y-64,0,p])
np.save(R/'阶段03a.npy',v);folder=R/'蓝图/03a';folder.mkdir(exist_ok=True)
bp={'schema_version':1,'origin':{'x':107,'y':64,'z':174},'dimensions':{'x':1,'y':2,'z':1},'palette':P,'blocks':b}
with gzip.open(folder/'岸脚.json.gz','wt',encoding='utf8') as f:json.dump(bp,f,separators=(',',':'))
(R/'作业/03a.json').write_text(json.dumps({'world_path':'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V14-T05-森林圣所','phases':[{'palette':P,'operations':[[107,y,174,107,y,174,P.index('minecraft:mud')] for y in [64,65]]}]},separators=(',',':')),encoding='utf8')
