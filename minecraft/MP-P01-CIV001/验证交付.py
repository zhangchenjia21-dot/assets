"""验证本轮地图/对象/坐标与来源，不以机器校验代替规划独立审核。"""
from pathlib import Path
import json,hashlib,math,sqlite3,subprocess
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent;repo=R.parents[1]
def read(n):return json.loads((R/n).read_text(encoding='utf8'))
plan=read('planning-objects.json');a=np.load(R/'terrain-sample.npz');h=a['elevation'];land=a['land_component'];ids={n['id'] for n in plan['nodes']};assert len(ids)==9
db=sqlite3.connect('file:D:/Games/Minecraft/AI工程/MP-P01-cache/observed.sqlite?mode=ro',uri=True)
for n in plan['nodes']:
 x,z=n['geometry']['coordinates'];i=(z-1380)//8;j=(x+796)//8;assert int(h[i,j])==n['observed_at_sample']['exposed_y']==db.execute('select exposed_y from samples where x=? and z=?',(x,z)).fetchone()[0];assert int(land[i,j])==n['observed_at_sample']['land_component'];assert n['authority']=='DESIGN_PROPOSAL'
nodes={n['id']:n for n in plan['nodes']};rid={r['id'] for r in plan['routes']}
for r in plan['routes']:
 assert r['from'] in ids and r['to'] in ids;points=r['geometry']['coordinates'];assert points[0]==nodes[r['from']]['geometry']['coordinates'];assert points[-1]==nodes[r['to']]['geometry']['coordinates']
 for x,z in points:assert -800<=x<=2463 and 1376<=z<=3487
 if r['mode']=='land':assert all(land[(z-1380)//8,(x+796)//8]==nodes[r['from']]['observed_at_sample']['land_component'] for x,z in points);assert r['max_sample_grade']<=.75
for f in read('flows-externalities.json'):assert set(f['routes'])<=rid
for p in read('implementation-packages.json')['packages']:assert not p['direct_builder_ready'] and not p['world_write_authorization']
images=[]
for p in (R/'maps').glob('*.png'):
 with Image.open(p) as im:im.load();images.append({'file':p.name,'dimensions':list(im.size)})
sources=read('source-register.json');changed=[]
for s in sources['sources']:
 if 'git_commit' in s:
  raw=subprocess.check_output(['git','show',s['git_commit']+':'+s['path']],cwd=repo);assert hashlib.sha256(raw).hexdigest()==s['sha256']
 if s['id'].startswith('DATA-'):
  path=repo/s['path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==s['sha256']
  local=subprocess.check_output(['git','hash-object',str(path)],cwd=repo,text=True).strip();remote=subprocess.check_output(['git','rev-parse','origin/main:'+s['path']],cwd=repo,text=True).strip();assert local==remote,s['path']
out={'plan':'MP-P01','revision':1,'world_reads':0,'world_writes':0,'source_hashes_match':True,'node_sample_queries':9,'node_sample_differences':0,'routes_with_valid_endpoints':len(plan['routes']),'land_candidate_max_grade':.75,'route_usable_clearance_or_navigation':'UNVERIFIED','map_coordinate_transform':'pixel=(70+(X+800)/2,110+(Z-1376)/2); 500 blocks = 250 px','images_decoded':images,'handoff':'L0 to L1 only','skill_regression_verdict':'NOT_ASSIGNED','independent_review':'PENDING'}
(R/'validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
(R/'SHA256.json').write_text(json.dumps({p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in R.rglob('*') if p.is_file() and p.name!='SHA256.json'},ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(out,ensure_ascii=False))
