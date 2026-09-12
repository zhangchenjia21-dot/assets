"""仅把已审查的物理失败转为有界差量；不重建或精修建筑。"""
from pathlib import Path
import json,numpy as np
R=Path(__file__).resolve().parent;m=json.loads((R/'证据/baseline-实存.json').read_text(encoding='utf8'));pal=list(m['palette']);A=np.fromfile(R/'证据/baseline.u16',dtype='<u2').reshape(36,96,56).copy();before=A.copy();ledger=[]
def put(x,y,z,v,issue,reason,allowed):
 v=v if ':' in v else 'minecraft:'+v;old=pal[A[y-10,z,x]];assert any(k in old for k in allowed),(x,y,z,old)
 if v not in pal:pal.append(v)
 if old!=v:A[y-10,z,x]=pal.index(v);ledger.append({'at':[x,y,z],'before':old,'after':v,'issue':issue,'reason':reason,'phase':'bounded physical Core Repair'})
d=json.loads((R/'证据/baseline-物理扫描.json').read_text(encoding='utf8'))
for g in d['closure_candidates']:
 x,y,z=g['gap'];put(x,y,z,'stone_bricks','C2' if 'STAIR' in g['classification'] else 'C1','闭合已有墙柱或台阶至既有地坪；不改变 footprint',['minecraft:air'])
for x in range(29,32):put(x,16,75,'gravel','C3','接续后庭同标高铺地至库门阶前；补残余低槽',['minecraft:air'])
cuts=set()
for r in d['stair_lanes']:
 if r['name'].startswith('stair lane (') and ', 18, 25)' in r['name']:
  for c in r['collision_cells']:
   assert '_log[' in c['state'];cuts.add(tuple(c['at']))
assert len(cuts)==5,cuts
for x,y,z in sorted(cuts):put(x,y,z,'air','M1','只清除侵入既有梯井身体包络的梁残段',['_log['])
for x in [24,29]:
 for z in range(24,31):put(x,22,z,'stripped_dark_oak_log[axis=z]','M1','既有梯井两侧局部边梁承托，落于原楼板边带；不侵入四条步行线',['minecraft:air','_log[','dark_oak_planks'])
stage='01-Repair';folder=R/'蓝图'/stage;folder.mkdir(parents=True,exist_ok=True);files=[]
for y in range(0,36,12):
 for z in range(0,96,24):
  for x in range(0,56,24):
   a=A[y:y+12,z:z+24,x:x+24];b=before[y:y+12,z:z+24,x:x+24];yy,zz,xx=np.where(a!=b)
   if not len(xx):continue
   used=sorted(set(map(int,a[yy,zz,xx])));remap={v:i for i,v in enumerate(used)}
   bp={'schema_version':1,'origin':{'x':x,'y':y+10,'z':z},'dimensions':{'x':a.shape[2],'y':a.shape[0],'z':a.shape[1]},'palette':[pal[i] for i in used],'blocks':[[int(i),int(j),int(k),remap[int(v)]] for i,j,k,v in zip(xx,yy,zz,a[yy,zz,xx])],'metadata':{'name':'T12 bounded physical repair','source_kind':'AI_ORIGINAL','content_omissions':[]}}
   f=f'{x}-{y+10}-{z}.json';(folder/f).write_text(json.dumps(bp,separators=(',',':')),encoding='utf8');files.append(f)
(folder/'清单.json').write_text(json.dumps({'files':files,'changed':len(ledger)}),encoding='utf8');np.savez_compressed(R/(stage+'.npz'),blocks=A,palette=pal)
(R/'证据/Repair变更账本.json').write_text(json.dumps({'source':'baseline','stage':stage,'changes':ledger,'semantic_changes':False},ensure_ascii=False,indent=2),encoding='utf8');print('bounded repair cells',len(ledger))
