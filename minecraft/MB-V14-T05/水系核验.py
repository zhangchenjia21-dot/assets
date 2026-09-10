"""只读统计实存水体六邻接分量；连通不代表长时间流体模拟。"""
from pathlib import Path
from collections import deque
import json,sys,numpy as np
R=Path(__file__).parent/'证据';n=sys.argv[1]
m=json.loads((R/(n+'.json')).read_text(encoding='utf8'));v=np.fromfile(R/(n+'.bin'),np.uint8).reshape(m['size'])
water={tuple(map(int,p)) for p in np.argwhere(np.isin(v,[i for i,p in enumerate(m['palette']) if p.split('[')[0]=='minecraft:water']))};out=[]
while water:
 p=water.pop();q=deque([p]);pts=[p]
 while q:
  x,y,z=q.popleft()
  for t in [(x-1,y,z),(x+1,y,z),(x,y-1,z),(x,y+1,z),(x,y,z-1),(x,y,z+1)]:
   if t in water:water.remove(t);q.append(t);pts.append(t)
 a=np.array(pts);lo=a.min(0);hi=a.max(0);lo[1]+=m['y0'];hi[1]+=m['y0'];out.append({'blocks':len(pts),'min':lo.tolist(),'max':hi.tolist()})
out.sort(key=lambda x:-x['blocks']);(R/(n+'-水系连通.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(out)
