"""检查实际状态的阶段边界；数值不代替语义与感知 Gate。"""
from pathlib import Path
import json,numpy as np,sys
R=Path(__file__).resolve().parent;s=sys.argv[1]
def read(n):
 m=json.loads((R/f'证据/{n}-实存.json').read_text(encoding='utf8'));a=np.fromfile(R/f'证据/{n}.u16',dtype='<u2').reshape(36,96,56)
 def norm(v):
  if '[' not in v:return v
  a,b=v.split('[',1);return a+'['+','.join(sorted(b[:-1].split(',')))+']'
 return np.array(list(map(norm,m['palette'])))[a],m
b,bm=read('04-Base');a,m=read(s);changed=a!=b
critical=np.zeros_like(changed)
for term in ['_log[','_stairs[','deepslate','glass_pane','furnace[','water[','water_cauldron']:
 critical|=np.char.find(b,term)>=0
# Core 护栏及低二层窗保留；前立面下槛是明确 Restricted 例外，不属于此掩码。
critical|=np.char.find(b,'_fence[')>=0
out={'stage':s,'world':m['name'],'same_world_identity':m['name']==bm['name']=='MB-V19-T11-京町家','critical_core_state_changes':int((critical&changed).sum()),'critical_changed_coordinates':[[int(x),int(y+10),int(z)] for y,z,x in np.argwhere(critical&changed)[:30]],'total_differences_from_baseline':int(changed.sum())}
out['well']={'source':a[7,70,28],'bottom':a[6,70,28],'sides':[a[7,70,27],a[7,70,29],a[7,69,28],a[7,71,28]],'fluid_update_stability':'not independently exercised'}
out['well_contained']=all('stone_bricks' in v for v in [out['well']['bottom']]+out['well']['sides']) and 'water[level=0]' in out['well']['source']
out['removed_core_solid_cells']=int(((b!='minecraft:air')&(a=='minecraft:air')).sum())
# 每个摆放的小物在整数格下方需有上表面；吊灯与架板单独由构造视图审查。
unsupported=[]
for y,z,x in np.argwhere(changed):
 v=a[y,z,x]
 if any(t in v for t in ['_carpet','flower_pot',':chest[',':barrel[','azalea']):
  below=a[y-1,z,x] if y else 'minecraft:air'
  if below=='minecraft:air' or ('_slab[' in below and 'type=bottom' in below):unsupported.append([int(x),int(y+10),int(z),v,below])
out['small_object_support_failures']=unsupported
out['limits']='掩码保护主要构件；墙面材质、家具及语义仍需逐项账本/平剖/路线审查。非客户端碰撞检查。'
(R/f'证据/{s}-阶段保护.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({k:out[k] for k in ['stage','critical_core_state_changes','removed_core_solid_cells','well_contained','small_object_support_failures']},ensure_ascii=True))
