from pathlib import Path
from collections import deque
import numpy as np,json,sys
R=Path(__file__).resolve().parent;s=sys.argv[1];m=json.loads((R/f'证据/{s}-实存元数据.json').read_text());A=np.fromfile(R/f'证据/{s}-实存方块.u16',dtype='<u2').reshape(52,240,288);pal=m['palette']
solid=np.array([not any(k in v.split('[')[0] for k in ['air','water','short_grass','fern','wheat','carrots','dead_bush','torch']) and v!='UNGENERATED' for v in pal])[A]
seen=np.zeros_like(solid);q=deque([(0,z,x) for z in range(240) for x in range(288) if solid[0,z,x]]);seen[0]=solid[0]
def flood(q):
    comp=[]
    while q:
        y,z,x=q.popleft();comp.append((y,z,x))
        for dy,dz,dx in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
            a,b,c=y+dy,z+dz,x+dx
            if 0<=a<52 and 0<=b<240 and 0<=c<288 and solid[a,b,c] and not seen[a,b,c]:seen[a,b,c]=True;q.append((a,b,c))
    return comp
flood(q);orphans=[]
for y,z,x in zip(*np.where(solid&~seen)):
    if seen[y,z,x]:continue
    seen[y,z,x]=True;cells=flood(deque([(int(y),int(z),int(x))]));coords=np.array(cells);states=sorted(set(pal[A[a,b,c]] for a,b,c in cells));orphans.append({'blocks':len(cells),'bounds_yzx':[coords.min(axis=0).tolist(),coords.max(axis=0).tolist()],'states':states,'cells_yzx':cells})
out={'stage':s,'method':'six-neighbour connection to y=12 ground, excluding fluid and herbs; intentional overhangs reviewed separately','orphan_components':len(orphans),'orphan_blocks':sum(c['blocks'] for c in orphans),'components':orphans}
(R/f'证据/{s}-完整性.json').write_text(json.dumps(out,ensure_ascii=False),encoding='utf8');print(json.dumps({k:v for k,v in out.items() if k!='components'},ensure_ascii=False));print([(c['blocks'],c['states'],c['bounds_yzx']) for c in orphans[:15]])
