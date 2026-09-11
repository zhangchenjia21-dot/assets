"""比较保存阶段，量化后施工对建筑和水体的覆盖；不作回归裁定。"""
from pathlib import Path
import json,numpy as np
R=Path(__file__).parent;E=R/'证据';s=json.loads((R/'场景.json').read_text(encoding='utf8'))
def norm(p):
 if '[' not in p:return p
 a,b=p.split('[',1);return a+'['+','.join(sorted(b[:-1].split(',')))+']'
M={n:json.loads((E/(n+'.json')).read_text(encoding='utf8')) for n in ['01','02','02a','03','03a','03b','03c']};P=sorted(set(norm(p) for m in M.values() for p in m['palette']));ids={p:i for i,p in enumerate(P)};V={n:np.array([ids[norm(p)] for p in m['palette']])[np.fromfile(E/(n+'.bin'),np.uint8).reshape(m['size'])] for n,m in M.items()};out={}
for a,b in [('01','02'),('02','02a'),('02a','03'),('03','03a'),('03a','03b'),('03b','03c')]:
 old,new=V[a],V[b];mask=old!=new;pairs={}
 for p,q in np.unique(np.stack([old[mask],new[mask]],axis=1),axis=0):pairs[P[p]+' → '+P[q]]=int((mask&(old==p)&(new==q)).sum())
 out[a+'→'+b]={'changes':int(mask.sum()),'transitions':pairs}
out['final_architecture_changes_after_02a']={}
for b in s['buildings']:
 x,y,z,X,Y,Z=b['bounds'];cut=(slice(x-1,X+2),slice(y-56,min(Y-52,64)),slice(z-1,Z+2));out['final_architecture_changes_after_02a'][b['name']]=int((V['02a'][cut]!=V['03c'][cut]).sum())
out['micro_water_changes']=[[int(x),int(y+56),int(z),P[int(V['03'][x,y,z])]] for x,y,z in np.argwhere((V['02a']!=V['03'])&np.isin(V['02a'],[i for i,p in enumerate(P) if p.startswith('minecraft:water')]))]
(E/'系统接口复核.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'architecture':out['final_architecture_changes_after_02a'],'water_changes':out['micro_water_changes']},ensure_ascii=True))
