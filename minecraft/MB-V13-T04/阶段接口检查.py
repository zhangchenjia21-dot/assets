"""最终实际保存状态对照建筑阶段，复核后施工系统没有切坏前序外壳。"""
from pathlib import Path
import json,numpy as np
R=Path(__file__).parent;E=R/'证据';s=json.loads((R/'场景.json').read_text(encoding='utf8'))
def norm(p):
 if '[' not in p:return p
 a,b=p.split('[',1);return a+'['+','.join(sorted(b[:-1].split(',')))+']'
ms=[json.loads((E/(n+'.json')).read_text(encoding='utf8')) for n in ['02a','03']];P=sorted(set(norm(p) for m in ms for p in m['palette']));ids={p:i for i,p in enumerate(P)};arrays=[np.array([ids[norm(p)] for p in m['palette']])[np.fromfile(E/(n+'.bin'),np.uint8).reshape(m['size'])] for n,m in zip(['02a','03'],ms)];a,b=arrays
struct=np.array([not any(k in p for k in ['air','grass','fern','leaves','water','dirt','daisy','torch','fence']) for p in P])[a];loss=np.argwhere(struct&(a!=b));env=[]
for row in s['envelopes']:
 x,y,z,X,Y,Z=row['bounds'];before=a[x:X+1,y-56:min(128,Y+20-56),z:Z+1];after=b[x:X+1,y-56:min(128,Y+20-56),z:Z+1];mask=np.array([not any(k in p for k in ['air','torch','water']) for p in P])[before]
 env.append({'name':row['name'],'solid_changed':int((mask&(before!=after)).sum()),'volume_changed':int((before!=after).sum())})
rep={'comparison':'saved stage02a to saved stage03; exact properties normalized','previous_structure_changed':len(loss),'examples':[[int(x),int(y+56),int(z),P[a[x,y,z]],P[b[x,y,z]]] for x,y,z in loss[:20]],'envelopes_including_roof_headroom':env,'note':'torch/hay additions are intended; counts do not substitute visual inspection of intentional openings'}
(E/'系统接口复核.json').write_text(json.dumps(rep,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(rep,ensure_ascii=False))
