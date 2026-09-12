"""MD-001P-R1 定向汇编：从固定 Git 基线恢复规划输入，只派生 P1，不扫描世界。

输出覆盖当前规划 JSON；政治成员与 P2–P5/N1–N4 几何必须原样保留。
阈值和包络参数是本任务人工规划判断，不是自动选址评分或施工边界。
"""
import json, subprocess, hashlib, sqlite3
from pathlib import Path
import numpy as np

OUT = Path(__file__).resolve().parents[1]
ROOT = OUT.parents[3]
REPO = ROOT.parents[1]
BASE = '4e276890000ffb87219aaaf1e8c2ea09cc6a8624'
STATUS = 'MD-001P-R1 PROPOSAL / AWAITING GPT + OWNER REVIEW'
X0, Z0, W, H = -400, 1440, 1600, 960

def previous(name):
    path = (OUT/name).relative_to(REPO).as_posix()
    return json.loads(subprocess.check_output(['git','show',f'{BASE}:{path}'],cwd=REPO))

def write(name, data):
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')

def mask(runs):
    a = np.zeros((H,W),bool)
    for z,l,r in runs: a[z-Z0,l-X0:r-X0+1] = True
    return a

def rle(a):
    runs=[]
    for z,row in enumerate(a):
        cuts=np.r_[0,np.where(row[1:]!=row[:-1])[0]+1,W]
        for l,r in zip(cuts[:-1],cuts[1:]):
            if row[l]:runs.append([z+Z0,int(l)+X0,int(r)+X0-1])
    return runs

def dilate(a, steps):
    a=a.copy()
    for _ in range(steps):
        b=a.copy();a[1:]|=b[:-1];a[:-1]|=b[1:];a[:,1:]|=b[:,:-1];a[:,:-1]|=b[:,1:]
    return a

sub=previous('subareas.json'); nodes=previous('settlement-nodes.json')
land=previous('land-use.json'); intensity=previous('human-use-intensity.json')
network=previous('movement-network.json'); master=previous('MASTERPLAN.json')
life=previous('resident-life-system.json'); p1=mask(sub['subareas'][0]['geometry'])
assert p1.sum()==13661
derived=ROOT/'research/human-geography/southern-island/WB-002R-R1/raw-or-queryable/derived.npz'
f=np.load(derived); sl=(slice(64,1024),slice(400,2000))
slope=f['slope8'][sl];relief=f['relief32'][sl];step=f['step1'][sl];shore=f['shoreline'][sl]
y=np.zeros((H,W),np.int16);artificial=np.zeros((H,W),bool);biomes={}
dbpath=derived.with_name('observed.sqlite')
with sqlite3.connect(dbpath.as_uri()+'?mode=ro',uri=True) as db:
    rows=db.execute('SELECT x,z,exposed_y,biome,artificial_material FROM samples WHERE x BETWEEN 89 AND 240 AND z BETWEEN 1664 AND 1841').fetchall()
    for x,z,yy,b,art in rows:
        if p1[z-Z0,x-X0]:y[z-Z0,x-X0]=yy;artificial[z-Z0,x-X0]=bool(art);biomes[(x,z)]=b
assert len(biomes)==13661
xx=np.indices(p1.shape)[1]+X0
# X130 是窄口后的规划阈值，不宣称为天然边界；整个阈值保持零建筑占地。
threshold=p1&(xx<130)
protected=p1&(dilate(shore,6)|~np.isfinite(slope)|artificial|(slope>.25)|(relief>8)|(step>2))
anchor=[190,1731]
eligible=p1&~protected&~threshold&(xx>=140)
distance=np.full((H,W),-1,np.int16);start=(anchor[1]-Z0,anchor[0]-X0)
assert eligible[start]
distance[start]=0;q=[start]
# 85 格可达邻域限制东侧扩宽段的社区尺度；岸线与不可判定坡度裁切真实轮廓。
for z,x in q:
    if distance[z,x]>=85:continue
    for dz,dx in ((0,1),(0,-1),(1,0),(-1,0)):
        zz,xxx=z+dz,x+dx
        if 0<=zz<H and 0<=xxx<W and eligible[zz,xxx] and distance[zz,xxx]<0:
            distance[zz,xxx]=distance[z,x]+1;q.append((zz,xxx))
gateway=distance>=0
route=network['routes'][0];oldpath=route['path'];ix=next(i for i,p in enumerate(oldpath) if p[:2]==anchor)
pathmask=np.zeros((H,W),bool)
for x,z,_ in oldpath:pathmask[z-Z0,x-X0]=True
clearance=p1&dilate(pathmask,6)
# 净空是覆盖在混合街市之上的零建筑约束；不把总包络冒充建筑 footprint。
reserve=protected&~threshold
transit=clearance&~threshold&~reserve&~gateway
openland=p1&~(threshold|reserve|gateway|transit)
parts=[('L3','政治与通行阈值',threshold),('L9','门户街市与常住社区',gateway),('L2','岸线/未知坡度/地形保护',reserve),('L4','门户通行预留',transit),('L1','排水维护与结构性开放地',openland)]
assert sum(int(m.sum()) for _,_,m in parts)==13661

def metrics(m):
    z,x=np.where(m)
    def stat(v):
        values=v[m];values=values[np.isfinite(values)]
        return {'n':int(len(values)),'min':float(values.min()),'median':float(np.median(values)),'p90':float(np.percentile(values,90)),'max':float(values.max())} if len(values) else {'n':0}
    return {'area':int(m.sum()),'bounds':[int(x.min())+X0,int(z.min())+Z0,int(x.max())+X0,int(z.max())+Z0],'elevation':stat(y),'slope8':stat(slope),'relief32':stat(relief),'step1':stat(step),'shore_columns':int((m&shore).sum()),'unknown_slope_columns':int((m&~np.isfinite(slope)).sum()),'artificial_material_columns':int((m&artificial).sum()),'flat_gentle_columns':int((m&(slope<=.25)&(relief<=8)&(step<=2)).sum())}

g={'id':'G1','name':'P1 门户街市与常住社区','rank':'gateway_secondary_specialized','point':anchor,'observed':{'y':int(y[start]),'slope8':float(slope[start]),'relief32':int(relief[start])},'status':'PLANNING NODE / NOT LOCAL SITE GATE','envelope':rle(gateway),'envelope_area':int(gateway.sum()),'terrain':metrics(gateway),'density':[.35,.48],'height_use':'紧凑街院、上住下店与经营家庭近邻；具体层数未冻结','roles':['短途交易','短仓周转','驮运停驻','修理','旅宿饮食','日用品','向导消息','常住经营家庭','小公共服务'],'resident_roles':['铺户及家庭','仓管与搬运家庭','修理匠及学徒','饮食旅宿经营者','向导及照护者'],'complement_to_N1':'G1 即时交接/短住/短存；N1 深层市场/较大仓储/加工/公共生活与长期商业网络','growth':'扩宽段沿既有预留联系形成共享街院，先保通过，再逐院生长；不形成封口线性建筑墙','capacity_note':'gross envelope includes lanes and shared courts; clearance overlay forbids building footprint','clearance_columns':int((gateway&clearance).sum()),'building_eligible_ceiling_columns':int((gateway&~clearance).sum())}
assert round(g['envelope_area']*.48)<=g['building_eligible_ceiling_columns']
nodes['nodes'].append(g)
lu=np.zeros((H,W),np.uint8)
for item in land['zones']:lu[mask(item['geometry'])]=item['code']
for lid,_,m in parts:lu[m]=int(lid[1:])
land['zones'].append({'id':'L9','code':9,'name':'门户街市与常住社区','program':'短交易/短仓/饮食旅宿/修理与经营家庭混合；净空 overlay 不准建筑占用'})
for item in land['zones']:
    m=lu==item['code'];item['geometry']=rle(m);item['area']=int(m.sum())
land['zones'][2].update(name='政治与通行阈值',program='X89 接口后窄段净空、视线、避让和集散；零建筑 footprint，不创造收费制度')
land['building_exclusion_overlays']=[{'id':'P1-THROUGH-CLEARANCE','geometry':rle(clearance),'area':int(clearance.sum()),'restriction':'no building footprint; 6-block Manhattan reservation about R0 path, not road width or street alignment'}]
p=sub['subareas'][0];p.update(name='中域门户聚落区',water_movement_relation='X89 政治接口 → G1 门户社区 → N1 主镇；岸线留维护和排水',suitable_and_unsuitable='扩宽平缓段紧凑混合居住与短交易；窄阈值、岸线及通行净空不建；不作收费站或军事门城',intensity='阈值 H2 / 街市 H3 / 开放 H1 / 保护 H0',open_land_program='政治视线与避让、岸线排水维护、结构性植被、居民小供给；不以高密为由填满')
p['land_use_budget']={f'L{i}':int((p1&(lu==i)).sum()) for i in range(1,10)}
p['internal_parts']=[{'land_use':lid,'name':name,'area':int(m.sum()),'geometry':rle(m)} for lid,name,m in parts]
iv=np.zeros((H,W),np.uint8)
for item in intensity['zones']:iv[mask(item['geometry'])]=item['code']
iv[threshold|transit]=2;iv[reserve]=0;iv[openland]=1;iv[gateway]=3
for item in intensity['zones']:
    m=mask([run for s in sub['subareas'] for run in s['geometry']])&(iv==item['code']);item['geometry']=rle(m);item['area']=int(m.sum())
intensity['zones'][2]['meaning']='政治阈值和主次通行预留；不再代表整个 P1'
intensity['capacity'].append({'node':'G1','gross_envelope_area':g['envelope_area'],'indicative_footprint_ratio':g['density'],'footprint_capacity':[round(g['envelope_area']*v) for v in g['density']],'meaning':'mature intention; no building footprint in through-clearance overlay'})
intensity['middle_indicative_territory_footprint_ratio']=[sum(c['footprint_capacity'][i] for c in intensity['capacity'])/391002 for i in (0,1)]
intensity['P1_threshold_footprint_ratio']=[0,0]
intensity['comparison_status']+='; R1 adds a specialized gateway, does not expand other settlements'
segments=[]
for rid,src,dst,path in [('R1a','I-C','G1',oldpath[ix:][::-1]),('R1b','G1','N1',oldpath[:ix+1][::-1])]:
    dy=np.diff(np.array(path)[:,2]);r=dict(route);r.update(id=rid,name=f'{src} ↔ {dst}',**{'from':src,'to':dst},path=path,length_blocks=len(path)-1,ascent=int(dy[dy>0].sum()),descent=int(-dy[dy<0].sum()),max_surface_step=int(abs(dy).max()),source='MD-001P R0 R1 split at cached G1 anchor; no new route search');segments.append(r)
network['routes']=segments+network['routes'][1:]
network['corridor_chains']=[{'id':'R1','nodes':['I-C','G1','N1'],'segments':['R1a','R1b'],'semantic':'Gateway → Principal Hub; bidirectional resident and exchange continuum, not continuous built ribbon'}]
network['commons_interface']['allocation']='X89 threshold stays clear; G1 in widening handles immediate exchanges and residents; N1 remains principal hub; no Commons expansion'
life['households'].append({'group':'门户铺户、短仓经营者、修理者、饮食旅宿经营者与家庭','home_work_relation':'G1 上住下店或前作后院；常住人口不等同旅客，公共饮水、食物与照护在地可达；大宗分拨与复杂服务转往 N1'})
for system in life['systems']:
    if system['id']=='LIFE-MOBILITY':system['providers']=['R1a','R1b']+system['providers'][1:]
    else:system['providers'].append('G1')
life['gateway_life']={'food':'G1 日用品与饮食，向 N1 高频补货；不声称粮产自给','water':'须另验清洁供水/储水，岸水不自动可饮；取水与畜粪分流','waste':'共享院短存、边缘维护；不堵净空、不向海岸直接排放','fire':'装卸在院内、净空连续、热工与睡眠分隔；不在窄口储燃料','public':'消息、向导、照护与小协商兼用；无新增关税/执法制度','tenure':'保障居民全天过境和共享院使用；不切等宽宅地','N1_relation':'两节点共享日常经济链；G1 不复制 N1 的完整市场和公共中心'}
first={'recommended_type':'门户街市共享周转与生活院','node':'G1','role':'短仓、称量交接、饮食/日用品与常住经营者生活并存；非强制查验或收费场所','scale':'中等规模，数百 block-column 的主体及必需共享院量级；不定尺寸/层数/地块','first_gate':'Only after GPT + Owner R1 acceptance and separate Local Site Gate authorization; within G1, outside threshold and clearance; anchor is not building coordinate','alternatives':[{'type':'主镇街市公共秤验与仓院','node':'N1','condition':'若 Owner 优先主镇公共生活样板或 G1 饮水/人工内容/通行复核不通过；承担市场内部称量与记录，不重复门户即时交接'},{'type':'工匠合作修造院','node':'N2','condition':'仅在加工居民样板优先且台地条件获复核时'}],'decision':'R0 N1 recommendation reconsidered and replaced; short storage most naturally at gateway, resident services prevent single-logistics interpretation','world_write_authorized':False}
master.update(status=STATUS,planning_revision='R1',lineage={'base_commit':BASE,'previous_implementation':'97a37e4a64cba8cd769980724ea8849305fe8fa1','decision':'D-026','scope':'P1 targeted revision'},first_build_recommendation=first)
master['subareas'][0]['name']=p['name']
master['settlement_hierarchy'].append({'id':'G1','rank':g['rank'],'point':anchor,'envelope_area':g['envelope_area']})
master['proposed_corridors']['ids']=[r['id'] for r in network['routes']]
master['land_use_zones']['ids'].append('L9');master['commons_interface']=network['commons_interface']
master['reserved_no_build_terrain']['area']=land['zones'][1]['area']
master['building_exclusion_overlays']={'file':'land-use.json','ids':['P1-THROUGH-CLEARANCE'],'threshold_no_build':'L3'}
master['phasing']=[{'id':'F0','scope':'GPT + Owner R1 review; no Site Gate auto-authorization'},{'id':'F1','scope':'G1 shared turnover/life courtyard recommendation; only separately authorized Site Gate, then design'},{'id':'F2','scope':'G1 living infill and N1 principal mixed neighborhood grow together; protected through access, no ribbon wall'},*master['phasing'][3:]]
for name,data in [('MASTERPLAN',master),('subareas',sub),('settlement-nodes',nodes),('land-use',land),('human-use-intensity',intensity),('movement-network',network),('resident-life-system',life)]:
    data['status']=STATUS;write(name+'.json',data)
evidence={'status':STATUS,'base_commit':BASE,'world_writes':0,'new_world_block_reads':0,'broad_rescan':0,'cache_reads':'P1 bounding box of existing observed.sqlite; existing derived.npz','p1_terrain':p['terrain'],'gateway':g,'parts':[{'id':lid,'name':name,'area':int(m.sum())} for lid,name,m in parts],'through_clearance_columns':int(clearance.sum()),'threshold_x_exclusive':130,'gateway_west_limit':140,'reachable_distance_limit':85,'shore_buffer_steps':6,'political_cut_x':89,'threshold_building_coverage':[0,0],'r0_footprint_ratio':previous('human-use-intensity.json')['middle_indicative_territory_footprint_ratio'],'r1_footprint_ratio':intensity['middle_indicative_territory_footprint_ratio'],'added_footprint_columns':intensity['capacity'][-1]['footprint_capacity'],'source_files':{str(derived.relative_to(ROOT)):hashlib.sha256(derived.read_bytes()).hexdigest()}}
write('validation/gateway-evidence.json',evidence)
print(json.dumps({k:evidence[k] for k in ('parts','r0_footprint_ratio','r1_footprint_ratio','added_footprint_columns')},ensure_ascii=False));print('G1',g['terrain'],'clearance',g['clearance_columns'])
