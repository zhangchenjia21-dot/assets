"""比较实存与基准、增量账本及冻结几何；不据数值宣告审美或回归结果。"""
from pathlib import Path
import numpy as np,json,sys
R=Path(__file__).resolve().parent;s=sys.argv[1]
def norm(v):
 if '[' not in v:return v
 a,b=v.split('[',1);return a+'['+','.join(sorted(b[:-1].split(',')))+']'
def read(n):
 m=json.loads((R/f'证据/{n}-实存.json').read_text(encoding='utf8'));return np.array(list(map(norm,m['palette'])))[np.fromfile(R/f'证据/{n}.u16',dtype='<u2').reshape(56,144,144)]
B=read('00-Baseline');A=read(s);diff=A!=B;stages=['01-Functional','02-Architectural','03-Material','04-Composition','05-Restraint'];end=4 if s=='reload' else stages.index(s);ledger=[]
for stage in stages[:end+1]:ledger+=json.loads((R/f'证据/{stage}-修改账本.json').read_text(encoding='utf8'))
expected=B.copy()
for v in ledger:
 x,y,z=v['x'],v['y']-10,v['z'];assert expected[y,z,x]==norm(v['before']);expected[y,z,x]=norm(v['after'])
water=np.char.startswith(B,'minecraft:water[')|np.char.startswith(A,'minecraft:water[')
shape=lambda a:~np.isin(a,['minecraft:air','minecraft:cave_air'])
occupied=shape(B);removed=occupied&~shape(A)
out={'stage':s,'baseline_changed_cells':int(diff.sum()),'unexplained_actual_changes':int((A!=expected).sum()),'frozen_Y24_and_above_changed':int(diff[14:].sum()),'water_state_changes':int((diff&water).sum()),'baseline_solid_removed':int(removed.sum()),'restricted_edits':[v for v in ledger if v['permission']=='Restricted'],'interpretation':'Semantic review still required: material substitutions retain occupied shape; all additions are logged furniture/props below Y24.'}
qa=json.loads((R/f'证据/{s}-核验.json').read_text(encoding='utf8'));out['all_14_expected_edges']=all(v['reachable_via_expected_portal'] for v in qa['edges'].values());out['orphan_cells']=qa['orphan_cells'];out['static_water_leaks']=qa['water']['side_or_bottom_open_to_air']
(R/f'证据/{s}-阶段保护.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({k:v for k,v in out.items() if k!='restricted_edits'},ensure_ascii=False))
assert not out['unexplained_actual_changes'] and not out['frozen_Y24_and_above_changed'] and not out['water_state_changes'] and not out['baseline_solid_removed'] and out['all_14_expected_edges'] and not out['orphan_cells']
