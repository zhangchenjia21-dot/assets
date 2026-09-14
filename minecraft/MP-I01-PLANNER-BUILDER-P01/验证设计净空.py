"""设计模型的局部连续体积筛查；不是Minecraft碰撞引擎或实机通行认证。"""
from pathlib import Path
import json,math,gzip
R=Path(__file__).resolve().parent
d=json.loads((R/'design/voxel-design.json').read_text(encoding='utf-8'))
states={(x,y,z):d['palette'][i] for x,y,z,i,t in d['blocks']}
n=json.loads(gzip.decompress((R/'evidence/site-columns.json.gz').read_bytes()))
for c in n['columns']:
 for i,sid in enumerate(c['state_ids']):
  p=(c['x'],c['ground_y']-24+i,c['z'])
  if p not in states:states[p]=n['palette'][sid]
def shapes(p,s):
 x,y,z=p
 if s=='minecraft:air':return []
 if '_stairs' in s:
  upper=(x+.5,y+.5,z,x+1,y+1,z+1)
  if 'facing=north' in s:upper=(x,y+.5,z,x+1,y+1,z+.5)
  if 'facing=south' in s:upper=(x,y+.5,z+.5,x+1,y+1,z+1)
  return [(x,y,z,x+1,y+.5,z+1),upper]
 if 'fence' in s:
  return [(x+.375,y,z,x+.625,y+1.5,z+1)] if 'north=true' in s else [(x,y,z+.375,x+1,y+1.5,z+.625)]
 return [(x,y,z,x+1,y+1,z+1)]
solids=[(p,q) for p,s in states.items() for q in shapes(p,s)]
def surface(x,z,low,high):
 return max([low]+[q[4] for p,q in solids if q[0]<=x<q[3] and q[2]<=z<q[5] and low<=q[4]<=high])
def line(a,b):
 n=max(1,math.ceil(math.dist(a,b)/.1))
 return [tuple(a[j]+(b[j]-a[j])*i/n for j in range(2)) for i in range(n+1)]
routes={
 'E1-entry-work':([(755.5,1634.5),(755.5,1631.5)],132,132),
 'E2-entry-live':([(763.5,1632.5),(763.5,1630.5)],133,133),
 'E3-controlled-step':([(757.5,1629.5),(760.5,1629.5)],132,133),
 'E4-stair':([(760.5,1627.5),(765.5,1627.5)],133,137),
 'E4-upper-continuation':([(765.5,1627.5),(765.5,1629.5),(760.5,1629.5)],137,137),
 'E5-rear-door':([(760.5,1628.5),(760.5,1625.5)],133,133),
 'E5-yard-continuation':([(760.5,1625.5),(758.5,1625.5),(758.5,1627.5),(752.5,1627.5),(752.5,1632.5)],130,133)
}
out=[]
for name,(waypoints,lo,hi) in routes.items():
 points=[]
 for a,b in zip(waypoints,waypoints[1:]):points+=line(a,b)
 failures=[];trace=[]
 for x,z in points:
  # 足宽范围的最高支承面作为保守爬阶包络；不宣称引擎真的允许该步移。
  y=max(surface(x+dx,z+dz,lo,hi) for dx in [-.29,0,.29] for dz in [-.29,0,.29]);body=(x-.3,y+.001,z-.3,x+.3,y+1.8,z+.3)
  hits=[p for p,q in solids if all(body[i]<q[i+3]-1e-6 and body[i+3]>q[i]+1e-6 for i in range(3))]
  if hits:failures.append({'point':[x,y,z],'hits':hits})
  trace.append([round(x,3),y,round(z,3)])
 out.append({'edge':name,'samples':len(points),'obstruction_count':len(failures),'failures':failures[:12],'trace':trace})
result={'method':'0.1block path sampling, 0.6x1.8 body, conservative high support surface; inherited terrain overridden by proposed design cells','routes':out,'real_minecraft_movement':'UNVERIFIED','excluded':'outside parcel, dynamic doors/furniture/fluid/true step physics','construction_closure_clearance_gate':'UNVERIFIED; design screening only'}
(R/'evidence/local-clearance-screen.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print([(x['edge'],x['obstruction_count']) for x in out])
