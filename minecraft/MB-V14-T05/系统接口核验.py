"""比较阶段实存；列出后施工系统对旧体素的覆盖，并核对建筑包络。"""
from pathlib import Path
import json,numpy as np
R=Path(__file__).parent;E=R/'证据';s=json.loads((R/'场景.json').read_text(encoding='utf8'))
def norm(p):
 if '[' not in p:return p
 a,b=p.split('[',1);return a+'['+','.join(sorted(b[:-1].split(',')))+']'
metas={n:json.loads((E/(n+'.json')).read_text(encoding='utf8')) for n in ['01a','02','03','03a','03b']};P=sorted(set(norm(p) for m in metas.values() for p in m['palette']));ids={p:i for i,p in enumerate(P)}
V={n:np.array([ids[norm(p)] for p in m['palette']])[np.fromfile(E/(n+'.bin'),np.uint8).reshape(m['size'])] for n,m in metas.items()};out={}
for a,b in [('01a','02'),('02','03'),('03','03a'),('03a','03b'),('02','03b')]:
 mask=V[a]!=V[b];pairs={}
 for p,q in np.unique(np.stack([V[a][mask],V[b][mask]],axis=1),axis=0):pairs[P[p]+' -> '+P[q]]=int(((V[a]==p)&(V[b]==q)&mask).sum())
 out[a+'→'+b]={'changed_cells':int(mask.sum()),'state_transitions':pairs}
out['architecture_envelopes']={}
for e in s['envelopes']:
 x,y,z,X,Y,Z=e['bounds'];cut=(slice(x,X+1),slice(y-56,Y-55),slice(z,Z+1));old=V['02'][cut];new=V['03b'][cut];mask=old!=new
 out['architecture_envelopes'][e['name']]={'bounds':e['bounds'],'changed_cells':int(mask.sum()),'changes':[[int(x+a),int(y+b),int(z+c),P[old[a,b,c]],P[new[a,b,c]]] for a,b,c in np.argwhere(mask)]}
(E/'系统接口检查.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(out,ensure_ascii=False))
