"""静态空间证据：通行、支承、蓝图差异分开输出，不判定建筑质量。"""
from pathlib import Path
from collections import deque
import numpy as np,json,sys
R=Path(__file__).resolve().parent;s=sys.argv[1];m=json.loads((R/f'证据/{s}-实存.json').read_text(encoding='utf8'));A=np.fromfile(R/f'证据/{s}.u16',dtype='<u2').reshape(84,144,160);pal=m['palette']
passable=np.array([v.split('[')[0] in ['minecraft:air','minecraft:cave_air','minecraft:void_air','minecraft:torch','minecraft:short_grass'] for v in pal])[A];solid=~passable & np.array([v!='UNGENERATED' for v in pal])[A]
walk=np.zeros_like(solid);walk[1:-1]=solid[:-2]&passable[1:-1]&passable[2:];seen=np.zeros_like(solid);seed=(6,56,28) if s in ['01-Macro','02-Meso'] else (4,56,10);q=deque([seed]);seen[seed]=True
while q:
 y,z,x=q.popleft()
 for dz,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
  a,b=x+dx,z+dz
  if not(0<=a<160 and 0<=b<144):continue
  for dy in [-1,0,1]:
   yy=y+dy
   if 0<yy<83 and walk[yy,b,a] and not seen[yy,b,a]:seen[yy,b,a]=True;q.append((yy,b,a))
targets={'前室':[28,18,56],'中殿':[45,18,56],'北侧廊':[57,18,43],'十字交叉':[95,18,56],'北耳堂':[95,18,29],'南耳堂':[95,18,82],'唱诗席':[112,19,56],'圣坛前':[120,19,56],'回廊':[55,18,79],'参事堂':[103,18,102],'宿舍楼下':[87,18,108],'宿舍楼上':[85,27,106]}
targets.update({'北附属礼拜堂':[111,18,32],'南附属礼拜堂':[111,18,83]})
routes={k:{'xyz':v,'reachable':bool(seen[v[1]-12,v[2],v[0]])} for k,v in targets.items()}
# 从实体地表做六邻接根连通，不将几何连通等同结构物理或空间质量。
visited=np.zeros_like(solid);visited[0]=solid[0];q=deque((0,z,x) for z in range(144) for x in range(160) if solid[0,z,x])
while q:
 y,z,x=q.popleft()
 for dy,dz,dx in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
  a,b,c=y+dy,z+dz,x+dx
  if 0<=a<84 and 0<=b<144 and 0<=c<160 and solid[a,b,c] and not visited[a,b,c]:visited[a,b,c]=True;q.append((a,b,c))
orphans=np.argwhere(solid&~visited);out={'stage':s,'start_xyz':[seed[2],seed[0]+12,seed[1]],'routes':routes,'method':'Cardinal voxel traversal with two-cell headroom and <=1 cell rise; not client walking','unrooted_solid_cells':len(orphans),'unrooted_examples_xyz':[[int(x),int(y+12),int(z)] for y,z,x in orphans[:30]],'unrooted_states':sorted(set(pal[A[y,z,x]] for y,z,x in orphans))}
planstage='04-Repair' if s=='reload' else s;f=R/f'{planstage}-方案.npz'
if f.exists():
 E=np.load(f)
 def norm(v):
  if '[' not in v:return v
  a,b=v.split('[',1);return a+'['+','.join(sorted(b[:-1].split(',')))+']'
 unique={v:i for i,v in enumerate(sorted(set(map(norm,pal))|set(map(norm,E['palette']))))};actual=np.array([unique[norm(v)] for v in pal])[A];expected=np.array([unique[norm(v)] for v in E['palette']])[E['blocks']];bad=(actual!=expected);out['full_volume_compared']=int(bad.size);out['blueprint_difference']=int(bad.sum())
out['interpretation']='Combine these checks with massing, sections, internal perspectives, openings, roof and stair review. No regression verdict.'
(R/f'证据/{s}-核验.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(out,ensure_ascii=False))
