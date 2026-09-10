"""按排序后的方块属性比较最终设计与存档，不忽略属性变化。"""
from pathlib import Path
import numpy as np,json,hashlib
R=Path(__file__).parent;E=R/'证据';s=json.loads((R/'场景.json').read_text(encoding='utf8'));m=json.loads((E/'阶段3c.json').read_text(encoding='utf8'))
def norm(p):
 if '[' not in p:return p
 a,b=p.split('[',1);return a+'['+','.join(sorted(b[:-1].split(',')))+']'
states=sorted(set(map(norm,s['palette']+m['palette'])));index={p:i for i,p in enumerate(states)}
a=np.array([index[norm(p)] for p in s['palette']])[np.load(R/'阶段3b.npy')];b=np.array([index[norm(p)] for p in m['palette']])[np.fromfile(E/'阶段3c.bin',np.uint8).reshape(m['size'])]
q=np.argwhere(a!=b);result={'cells':int(a.size),'different_cells':len(q),'comparison':'exact block id and sorted properties','examples':[[int(x),int(y+56),int(z),states[a[x,y,z]],states[b[x,y,z]]] for x,y,z in q[:30]],'actual_sha256':m['sha256']}
(E/'最终全量比对-3c.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(result,ensure_ascii=False))
