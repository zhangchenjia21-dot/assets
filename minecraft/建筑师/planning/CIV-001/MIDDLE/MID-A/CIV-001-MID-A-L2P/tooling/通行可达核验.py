import os
from pathlib import Path
from collections import deque
import json,numpy as np
C=Path(os.environ['MID_A_CACHE']);O=Path(os.environ['MID_A_OUTPUT']);a=np.load(C/'city-map.npz');y=a['height'];m=a['city']&~a['void']&~a['wet']&(a['logs']==0)
start=(1690-1453,290-89);assert m[start];par={start:None};q=deque([start])
while q:
 z,x=q.popleft()
 for dz,dx in [(1,0),(-1,0),(0,1),(0,-1)]:
  nz,nx=z+dz,x+dx
  if 0<=nz<m.shape[0] and 0<=nx<m.shape[1] and m[nz,nx] and (nz,nx) not in par and abs(int(y[nz,nx])-int(y[z,x]))<=1:par[(nz,nx)]=(z,x);q.append((nz,nx))
probes=[]
for x,z in [(89,1750),(245,1800),(365,1650)]:
 target=(z-1453,x-89);path=[];v=target
 if target in par:
  while v is not None:path.append([int(v[1])+89,int(v[0])+1453,int(y[v])]);v=par[v]
  path.reverse()
 probes.append(dict(target=[x,z],reached=target in par,path=path,length=len(path)-1 if path else None,reserve_columns=sum(bool(a['reserved'][v[1]-1453,v[0]-89]) for v in path)))
result=dict(schema='current-dry-step-probes/1',origin=[290,1690],method='4-neighbor BFS over current proposed city; max surface step1; exclude columns with sampled shallow void/water and stripped logs. Non-roof buffer may be traversed, not built on.',probes=probes,reachable_columns=len(par),limitations=['No headroom/width/animal collision, tree crown clearance, subsurface bearing or access rights proof','Exact witness is observation analysis, NOT proposed street geometry','Crossing a no-roof reserve requires L3 maintenance/ground verification; no infill authorization'])
(O/'evidence/access-probes.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print([(v['target'],v['reached'],v['length'],v['reserve_columns']) for v in probes])
