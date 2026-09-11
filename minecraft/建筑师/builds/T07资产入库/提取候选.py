from pathlib import Path
import ast,math,json,hashlib
import numpy as np
R=Path(__file__).resolve().parent;S=R.parent/'发布/assets/minecraft/MB-V15-T07';L=R.parent/'MB-V15-T07'
meta=json.loads((S/'证据/05-Water-实存元数据.json').read_text(encoding='utf8'));raw=(L/'证据/05-Water-实存方块.u16').read_bytes()
assert hashlib.sha256(raw).hexdigest()==meta['sha256'];A=np.frombuffer(raw,dtype='<u2').reshape(meta['shape_yzx'])
mask={}
def put(x,y,z,s):mask[x,y,z]=s
def box(x,y,z,X,Y,Z,s):
 for yy in range(y,Y+1):
  for zz in range(z,Z+1):
   for xx in range(x,X+1):put(xx,yy,zz,s)
env=dict(np=np,math=math,put=put,box=box,H=np.full((240,288),20),trees=[])
tree=ast.parse((S/'生成场景.py').read_text(encoding='utf8'));lines=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='line'];palm=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='palm')
for fn in [lines[0],palm]:exec(compile(ast.Module(body=[fn],type_ignores=[]),'<candidate>','exec'),env)
env['palm'](68,82,14,-1,.63)
exec(compile(ast.Module(body=[lines[1]],type_ignores=[]),'<repair>','exec'),env);env['palm'](68,82,14,-1,.63)
top=(67,34,82)
for n in range(7):
 a=.63+n*math.tau/7;length=5+n%3
 for j in range(2,length):
  end=(round(top[0]+j*math.cos(a)),round(top[1]+2*math.sin(math.pi*j/length)-j*.38),round(top[2]+j*math.sin(a)))
  for side in [-1,1]:env['line'](end,(end[0]+round(math.cos(a+side*math.pi/2)),end[1],end[2]+round(math.sin(a+side*math.pi/2))),'jungle_leaves')
treepoints=[p for p in mask if p[1]>=21]
shelterpoints=[(x,y,z) for y in range(21,28) for z in range(162,169) for x in range(156,167) if meta['palette'][A[y-12,z,x]]!='minecraft:air']
records=[]
for ident,name,points,anchor,kind in [('AI-T07-PALM-B','羽状椰枣树 B',treepoints,[68,21,82],'TREE'),('AI-T07-CANOPY-A','木脊布棚 A',shelterpoints,[156,21,162],'OPEN_SHELTER')]:
 lo=np.min(points,axis=0).tolist();hi=np.max(points,axis=0).tolist();pal=[];blocks=[]
 for x,y,z in sorted(points):
  state=meta['palette'][A[y-12,z,x]]
  assert state!='minecraft:air'
  if kind=='TREE':assert state.split('[')[0] in ['minecraft:jungle_log','minecraft:jungle_wood','minecraft:jungle_leaves']
  if state not in pal:pal.append(state)
  blocks.append([x-lo[0],y-lo[1],z-lo[2],pal.index(state)])
 contract={'kind':kind,'front':'SOUTH','anchor':[anchor[i]-lo[i] for i in range(3)]}
 if kind=='OPEN_SHELTER':contract.update(route=[[x,0,3] for x in range(11)],supports=[[x,4,z] for x in [0,10] for z in [0,6]])
 bp={'schema_version':1,'origin':dict(x=0,y=0,z=0),'dimensions':dict(zip(['x','y','z'],[hi[i]-lo[i]+1 for i in range(3)])),'palette':pal,'blocks':blocks,'metadata':{'name':name,'source_kind':'AI_ORIGINAL','asset_contract':contract,'content_omissions':[]}}
 d=R/ident;d.mkdir(parents=True,exist_ok=True);(d/'blueprint.json').write_text(json.dumps(bp,ensure_ascii=False,indent=2),encoding='utf8')
 provenance={'id':ident,'name':name,'world':meta['world'],'source_stage':'05-Water','snapshot_sha256':meta['sha256'],'bounds':[lo,hi],'blocks':len(blocks),'extraction':'Tree author coordinate mask includes original and repaired feather paths; shelter exact reviewed bounds. States read from saved snapshot; no redesign or terrain.'}
 (d/'提取来源.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2),encoding='utf8');records.append(provenance)
print(json.dumps(records,ensure_ascii=True))
