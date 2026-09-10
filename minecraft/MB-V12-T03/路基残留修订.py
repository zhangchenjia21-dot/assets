"""全量比对发现后期植被覆盖了十九格修订路基，恢复精确目标。"""
from pathlib import Path
import numpy as np,json,gzip
R=Path(__file__).parent;s=json.loads((R/'场景.json').read_text(encoding='utf8'));P=s['palette'];v=np.load(R/'阶段3b.npy');q=json.loads((R/'证据/最终全量比对.json').read_text(encoding='utf8'))
assert q['different_cells']==len(q['examples'])==19
b=[[x,y-56,z,int(v[x,y-56,z])] for x,y,z,expected,actual in q['examples']]
folder=R/'蓝图/3c-路基植被残留';folder.mkdir(exist_ok=True)
bp={'schema_version':1,'origin':{'x':0,'y':56,'z':0},'dimensions':{'x':128,'y':16,'z':128},'palette':P,'blocks':b}
with gzip.open(folder/'repair.json.gz','wt',encoding='utf8') as f:json.dump(bp,f,separators=(',',':'))
job={'world_path':'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V12-T03-河谷村落','phases':[{'palette':P,'operations':[[x,y+56,z,x,y+56,z,p] for x,y,z,p in b]}]}
(R/'作业/3c.json').write_text(json.dumps(job,separators=(',',':')),encoding='utf8')
