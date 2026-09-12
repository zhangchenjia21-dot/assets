"""规划外围：把人工规划判断绑定到既有逐柱证据；不产生建筑蓝图或世界写入。"""
import json,hashlib,heapq,sqlite3
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
OUT=Path(__file__).resolve().parents[1];ROOT=OUT.parents[3]
CACHE=Path('D:/Games/Minecraft/AI工程/研究缓存/建筑师/MD-001P')
STATUS='MASTERPLAN PROPOSAL / AWAITING GPT + OWNER REVIEW'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        while b:=f.read(1048576):h.update(b)
    return h.hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(name,d):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')),encoding='utf-8',newline='\n')
def rle(mask):
    runs=[]
    for z,row in enumerate(mask):
        cuts=np.r_[0,np.where(row[1:]!=row[:-1])[0]+1,len(row)]
        for l,h in zip(cuts[:-1],cuts[1:]):
            if row[l]:runs.append([z+Z0,int(l)+X0,int(h)+X0-1])
    return runs
def summary(mask):
    zz,xx=np.where(mask)
    def stats(v):
        v=v[mask];v=v[np.isfinite(v)]
        return {'n':int(len(v)),'min':float(v.min()) if len(v) else None,'median':float(np.median(v)) if len(v) else None,'p90':float(np.percentile(v,90)) if len(v) else None,'max':float(v.max()) if len(v) else None}
    ids,counts=np.unique(gentle[mask],return_counts=True)
    return {'area':int(mask.sum()),'bounds':[int(xx.min())+X0,int(zz.min())+Z0,int(xx.max())+X0,int(zz.max())+Z0] if len(xx) else None,'elevation':stats(y),'slope8':stats(slope),'relief32':stats(relief),'shore_columns':int((mask&shore).sum()),'flat_gentle_columns':int((mask&(relief<=8)&(slope<=.25)&(step<=2)).sum()),'moderate_adaptation_columns':int((mask&(relief<=24)&(slope<=.75)&(step<=3)).sum()),'major_gentle_components':[{'source_id':int(ids[j]),'overlap_columns':int(counts[j])} for j in np.argsort(counts)[::-1][:5] if ids[j]!=0],'biomes':[{'name':biome_names[int(k)],'columns':int(n)} for k,n in zip(*np.unique(biome[mask],return_counts=True))],'artificial_material_columns':int((mask&artificial).sum())}

territory=ROOT/'research/human-geography/southern-island/territory-refinement/TT-002R/refined-draft.json';doc=read(territory)
assert doc['revision']==154 and doc['source']['id']=='94fc4687358a9fd5dd542997538822bfdba7b83bd76c4825fd84bd0116ea3d21'
for ref in doc['source']['references']:
    p=ROOT/ref['path']
    if not p.exists():p=next((ROOT/'decisions').glob('D-020_*.md'))
    assert sha(p)==ref['sha256']
full=np.full((2112,3264),255,np.uint8)
for z,l,h,c in doc['runs']:full[z-1376,l+800:h+801]=c
assert int((full==2).sum())==391002
# 小裁框覆盖中域全部成员，包括远东北的 7 格 secondary；周围仍保留政治邻域。
X0,Z0,X1,Z1=-400,1440,1200,2400;sl=(slice(Z0-1376,Z1-1376),slice(X0+800,X1+800))
a=full[sl];m=a==2;H,W=m.shape
r1=ROOT/'research/human-geography/southern-island/WB-002R-R1/raw-or-queryable';f=np.load(r1/'derived.npz')
slope=f['slope8'][sl];relief=f['relief32'][sl];step=f['step1'][sl];gentle=f['gentle_component'][sl];shore=f['shoreline'][sl]
db=sqlite3.connect((r1/'observed.sqlite').as_uri()+'?mode=ro',uri=True)
rows=db.execute('SELECT exposed_y,biome,artificial_material FROM samples WHERE z>=? AND z<? AND x>=? AND x<? ORDER BY z,x',(Z0,Z1,X0,X1)).fetchall()
vals=np.array(rows,np.int32).reshape(H,W,3);y=vals[:,:,0];biome=vals[:,:,1];artificial=vals[:,:,2]>0;biome_names=dict(db.execute('SELECT * FROM biomes'));db.close()
connector=np.zeros(m.shape,bool)
p1r=ROOT/'research/build-sites/CIV-001/AB-001P1R'
for z,l,h in read(p1r/'connector-geometry.json')['runs']:connector[z-Z0,l-X0:h-X0+1]=True
assert connector.sum()==13661 and m[connector].all()

# 以下 seed 是经本轮地形审阅选择的规划节点；算法不裁决社会功能。
nodes=[
 {'id':'N1','name':'低地混合主镇','rank':'principal_hub','point':[308,1639],'target_envelope':30000,'density':[.45,.60],'height_use':'以2–3层上住下作/下店为主；仓院不统一加层','roles':['日常市场','居民商住','仓储转运','轻加工','旅宿','地方公共服务'],'growth':'先有低地道路交汇和交换，再由邻街院落增建；不以 connector 为唯一中心'},
 {'id':'N2','name':'中台工匠居民节点','rank':'secondary','point':[470,1800],'target_envelope':14500,'density':[.35,.48],'height_use':'紧凑2层及顺坡错层，具体层数后续设计','roles':['修造','小批加工','工匠家庭','日常供应','上山货物整备'],'growth':'在已识别台地沿上山联系线成组增建，重作业留在院内'},
 {'id':'N3','name':'北高台交换居民镇','rank':'secondary','point':[849,1660],'target_envelope':24000,'density':[.35,.48],'height_use':'紧凑2层，台地边缘分级处理','roles':['东域货物交换','仓储','居民','畜力接替','旅宿','地方服务'],'growth':'依较宽连续缓地形成第二级市场与社区，连接东界，不占山体陡岸'},
 {'id':'N4','name':'内谷居民与修整聚落','rank':'secondary','point':[435,2034],'target_envelope':9500,'density':[.30,.42],'height_use':'1–2层紧凑院落；不能填谷扩地','roles':['居民','工具修理','食物小供给','南路中继','家庭手工业'],'growth':'依内谷缓地发展常住社区，谷壁与水岸保留，不扩成平原城镇'}]
for n in nodes:
    x,z=n['point'];assert m[z-Z0,x-X0]
    n['observed']={'y':int(y[z-Z0,x-X0]),'slope8':float(slope[z-Z0,x-X0]),'relief32':int(relief[z-Z0,x-X0]),'gentle_component':int(gentle[z-Z0,x-X0])};n['status']='PLANNING NODE / NOT LOCAL SITE GATE'
cost=(1+2*np.nan_to_num(slope,nan=1.)+relief/16+.5*step).ravel();heights=y.ravel();valid=m.ravel()
def dijkstra(seeds,need_parent=False):
    # 与 WB-003R 相同的干陆四邻接研究成本；不是行走时间或已存在道路。
    dist=np.full(H*W,np.inf);labels=np.zeros(H*W,np.int16);parent=np.full(H*W,-1,np.int32) if need_parent else None;q=[]
    for x,z,lab in seeds:
        i=(z-Z0)*W+x-X0;assert valid[i];dist[i]=0;labels[i]=lab;heapq.heappush(q,(0.,i))
    while q:
        d,i=heapq.heappop(q)
        if d!=dist[i]:continue
        x=i%W
        for j in (i-1 if x else -1,i+1 if x+1<W else -1,i-W if i>=W else -1,i+W if i+W<H*W else -1):
            if j<0 or not valid[j]:continue
            dd=d+(cost[i]+cost[j])/2+4*float(heights[j]-heights[i])**2
            if dd<dist[j]:dist[j]=dd;labels[j]=labels[i]
            else:continue
            if parent is not None:parent[j]=i
            heapq.heappush(q,(dd,j))
    return dist.reshape(H,W),labels.reshape(H,W),parent

all_dist,labels,_=dijkstra([(*n['point'],i+2) for i,n in enumerate(nodes)])
secondary=m&~np.isfinite(all_dist);assert secondary.sum()==7
labels[secondary]=4;labels[connector]=1;labels[~m]=0
subnames=['connector 窄带与跨界前庭','低地—西岸生活交换盆地','中央台地及坡面过渡','北部高位缓地与东向接口','南内谷—狭岸生产生活带']
relations=[('Commons X89 政治陆路接口；禁止主城填塞窄口','只保留短驻留、通行、引导，不集中全域仓储','高通行，低覆盖'),('connector 后低地与西北岸；连向中央台地与北高台','主聚落混合使用；不填岸扩为码头园区','最高'),('中部高位台地；向北高台和内谷转换','工匠居民紧凑院落；陡坡禁止规则街区','次级紧凑'),('较宽高位缓地及东界接入；北岸为陡坎','交换居民镇；不因相对平坦而推平到岸缘','次级紧凑'),('内谷缓地连接南岸渡运候选；西岸狭陡','谷地常住与路边生产；南岸只条件性渡运','谷地集中 / 岸坡低强度')]
subareas=[]
for c,(name,relation) in enumerate(zip(subnames,relations),1):
    mask=labels==c;subareas.append({'id':f'P{c}','name':name,'geometry':rle(mask),'terrain':summary(mask),'water_movement_relation':relation[0],'suitable_and_unsuitable':relation[1],'intensity':relation[2],'method':'accepted connector exact geometry; other subareas terrain-cost service catchments from human-selected anchors, planning seams not natural/political absolutes','secondary_component_note':'7-column disconnected remnant: reserve only, no settlement' if c==4 else None})
write('subareas.json',{'schema':'md-planning-subareas/1','status':STATUS,'subareas':subareas})

# 全中域规划覆盖：水岸、陡坡、人工痕迹与零碎缓冲不是空白，也不等于城市扩张地。
near_water=shore.copy()
for _ in range(6):
    d=near_water.copy();near_water[1:]|=d[:-1];near_water[:-1]|=d[1:];near_water[:,1:]|=d[:,:-1];near_water[:,:-1]|=d[:,1:]
reserve=m&(near_water|(slope>1.25)|(relief>40)|(~np.isfinite(slope))|artificial|secondary)
eligible=m&~reserve&~connector&(slope<=.75)&(relief<=24)&(step<=3)
claimed=np.zeros(m.shape,bool);node_masks=[];parents={};distances={}
for k,n in enumerate(nodes):
    dist,_,parent=dijkstra([(*n['point'],1)],True);parents[n['id']]=parent;distances[n['id']]=dist
    zz,xx=np.indices(m.shape);rad=140 if k in (0,2) else 110
    compact=(xx+X0-n['point'][0])**2+(zz+Z0-n['point'][1])**2<=rad**2
    can=eligible&~claimed&(labels==k+2)&(dist<=600)&compact
    idx=np.flatnonzero(can);idx=idx[np.argsort(dist.ravel()[idx],kind='stable')][:n['target_envelope']]
    mask=np.zeros(H*W,bool);mask[idx]=True;mask=mask.reshape(H,W)
    # 按核心连通部分保留聚落候选面；不把散落单格承诺为可建设街区。
    start=(n['point'][1]-Z0,n['point'][0]-X0);connected=np.zeros(m.shape,bool);q=[start];connected[start]=True
    for z,x in q:
        for dz,dx in ((0,1),(0,-1),(1,0),(-1,0)):
            zz,xx=z+dz,x+dx
            if 0<=zz<H and 0<=xx<W and mask[zz,xx] and not connected[zz,xx]:connected[zz,xx]=True;q.append((zz,xx))
    mask &= connected;claimed|=mask;node_masks.append(mask)
    n['envelope']=rle(mask);n['terrain']=summary(mask);n['envelope_area']=int(mask.sum());n['capacity_note']='gross mixed-use planning envelope; includes courtyards, lanes, loading, water/fire access; not building footprint'

def path_from(source,target):
    x,z=target;i=(z-Z0)*W+x-X0;p=parents[source];assert np.isfinite(distances[source].ravel()[i]);result=[]
    while i>=0:
        zz,xx=divmod(i,W);result.append([xx+X0,zz+Z0,int(y[zz,xx])]);i=int(p[i])
    return result[::-1]
routes=[]
specs=[('R1','N1',[89,1750],'Commons connector ↔ 主镇','principal_pack_and_resident','I-C'),('R2','N1',nodes[1]['point'],'主镇 ↔ 中台工匠节点','principal_pack_and_resident','N2'),('R3','N1',nodes[2]['point'],'主镇 ↔ 北高台交换镇','principal_exchange','N3'),('R4','N2',nodes[3]['point'],'中台 ↔ 内谷居民节点','secondary_foothill','N4'),('R5','N2',[598,1894],'中台 ↔ accepted East 接口','mountain_exchange_reservation','I-E1'),('R6','N4',[326,2326],'内谷 ↔ 南岸渡运候选','conditional_foot_pack','I-W1')]
for rid,src,target,name,role,dst in specs:
    path=path_from(src,target);dy=np.diff(np.array(path)[:,2]);routes.append({'id':rid,'name':name,'from':src,'to':dst,'status':'PROPOSED_CORRIDOR_RESERVATION / NOT EXISTING ROAD','role':role,'path':path,'reservation_halfwidth_blocks':6 if rid in ('R1','R2','R3') else 4,'length_blocks':len(path)-1,'ascent':int(dy[dy>0].sum()),'descent':int(-dy[dy<0].sum()),'max_surface_step':int(abs(dy).max()),'cart_access':'UNVERIFIED: steep sections initially pack/foot; future switchbacks/ramps subject to local site checks','source':'new derivation from accepted R1; node anchors authored by MD-001P; WB-003R formula reused'})
# 北高台的边界接口从真实 Middle/East 邻边选取，不能把地图上的方向箭头当接口。
east_edges=[]
for z,x in zip(*np.where(m)):
    for dz,dx in ((0,1),(0,-1),(1,0),(-1,0)):
        zz,xx=z+dz,x+dx
        if 0<=zz<H and 0<=xx<W and a[zz,xx]==3:east_edges.append((int(x)+X0,int(z)+Z0,int(xx)+X0,int(zz)+Z0))
point=min(east_edges,key=lambda q:abs(q[0]-900)+abs(q[1]-1800));path=path_from('N3',point[:2]);dy=np.diff(np.array(path)[:,2]);routes.append({'id':'R7','name':'北高台 ↔ 东域北接口','from':'N3','to':'I-E2','status':'PROPOSED_CORRIDOR_RESERVATION / NOT EXISTING ROAD','role':'secondary_exchange_reservation','path':path,'reservation_halfwidth_blocks':4,'length_blocks':len(path)-1,'ascent':int(dy[dy>0].sum()),'descent':int(-dy[dy<0].sum()),'max_surface_step':int(abs(dy).max()),'cart_access':'UNVERIFIED','source':'Middle-only terrain-cost path to exact shared political edge'})
route_mask=np.zeros(m.shape,bool)
for rt in routes:
    rr=rt['reservation_halfwidth_blocks']
    for x,z,_ in rt['path']:
        for dz in range(-rr,rr+1):
            rem=rr-abs(dz);zz=z-Z0+dz
            if 0<=zz<H:route_mask[zz,max(0,x-X0-rem):min(W,x-X0+rem+1)]=True
route_mask&=m
crossings=read(ROOT/'research/human-geography/southern-island/WB-003R/profile/crossing-profile.json')
water=[]
for c in crossings['candidates']:
    ep=c['east'];wp=c['west'];x,z=ep['x'],ep['z'];code=int(full[z-1376,x+800])
    water.append({'id':c['id'],'middle_endpoint':code==2,'endpoint_territory_index':code,'east_endpoint':[x,z],'west_endpoint':[wp['x'],wp['z']],'gap_blocks':c['edge_to_edge_gap_blocks'],'source_status':c['status'],'planning_status':'I-W1 / conditional south ferry interface; no major town at cliff backshore' if code==2 and c['status']!='REJECTED_AS_CLEAR_STRAIGHT_CROSSING' else 'CONTEXT_ONLY / not a Middle landing; rejected evidence remains rejected'})
commons_interface={'id':'I-C','middle_point':[89,1750],'commons_point':[88,1750],'accepted_plane_x':89,'accepted_shared_unit_edges':48,'connector_area':13661,'allocation':'transit, small welcome/notice/refuge pockets only; principal market in N1; no Commons expansion','future_options':['界石与共享告示','小型迎候/接驳点'],'not_authorized':['关卡施工','独占收费','Commons 城市扩张']}
interfaces=[{'id':'I-E1','middle_point':[598,1894],'east_point':[598,1895],'evidence':'WB-003R C-01/C-02/C-03 last Middle column under accepted revision 154','function':'pack cargo handover, tools/metal/stone exchange; no mine or road existence claim'}, {'id':'I-E2','middle_point':list(point[:2]),'east_point':list(point[2:]),'evidence':'exact shared edge; northern secondary reservation','function':'north terrace exchange link; East-side extension outside this plan'}]
for it in interfaces:
    x,z=it['middle_point'];xx,zz=it['east_point'];assert full[z-1376,x+800]==2 and full[zz-1376,xx+800]==3
write('movement-network.json',{'status':STATUS,'coordinate_system':'Minecraft x,z; path includes cached surface y','roads_existing':False,'directionality':'bidirectional exchange; stored path order only sets ascent/descent reporting direction','cost_formula':'mean(1+2*slope8+relief32/16+0.5*step1) + 4*abs(dy)^2; NaN slope uses explicit unknown penalty 1','routes':routes,'water_interfaces':water,'commons_interface':commons_interface,'east_interfaces':interfaces,'distinction':['WB-003R terrain evidence','MD-001P proposed corridor reservation','future road/dock only after local Site Gate'],'water_policy':'X-03 geometric water-gap proxy only; water depth, landing operation and navigation unverified'})

# 完整土地使用表：所有中域列恰好一类；混合用途节点内部不再画现代功能单区。
landuse=np.full(m.shape,0,np.uint8);landuse[m]=1;landuse[reserve]=2;landuse[connector]=3;landuse[route_mask&~reserve&~connector]=4
for i,mask in enumerate(node_masks):landuse[mask]=5+i
defs=[(1,'生产性开放地与渐变缓冲','家庭菜园/果木/饲料小地、林下利用、排水、堆料季节轮用；需现场确认土壤水源，非大片农牧替代 West'),(2,'地形/岸线/现有痕迹保护','当前 no-building envelope；仅经新局部任务验证后可能有步道/岸点，不推平或填谷'),(3,'connector 通行公用带','政治接口与通过性优先；紧凑小服务点，禁止成为全域主仓城'),(4,'交通与沿线服务预留','未来主次路径及必要装卸/避让/维护，预留宽度不是施工道路宽度'),(5,'主镇紧凑混合街院','商住、仓院、市场、小作坊、旅宿、公共/宗教、生活供应交织'),(6,'中台紧凑工匠社区','修造与轻加工院、工匠家庭、粮食铺、货物整备、地方服务混合'),(7,'北高台混合交换社区','仓储、东域货物交换、日常居民、旅宿、畜力服务及公共服务混合'),(8,'内谷紧凑居民社区','常住家庭、家庭手工业、小市场、工具修理、食物供应及南路中继')]
landzones=[{'id':f'L{c}','code':c,'name':name,'program':program,'area':int((landuse==c).sum()),'geometry':rle(landuse==c)} for c,name,program in defs]
open_programs=['通过性、政治接口与岸线保护；不承担主城外溢','临镇菜园/小供给、季节性交易维护、结构性树木与排水；不铺现代草坪','台地之间林坡/排水与生产维护；小作业空隙，不以平整大院贯通陡坡','高台居民食物/饲料补充、季节周转与植被；不把全域加工堆在街巷','谷地小生产、家庭供给与南路维护；狭岸和坡壁不冒充城市备用平地']
for i,sub in enumerate(subareas,1):
    sub['land_use_budget']={f'L{c}':int(((labels==i)&(landuse==c)).sum()) for c,_,_ in defs}
    sub['open_land_program']=open_programs[i-1]
write('subareas.json',{'schema':'md-planning-subareas/1','status':STATUS,'subareas':subareas})
write('land-use.json',{'status':STATUS,'exclusive_partition':True,'total_middle_area':391002,'zones':landzones,'no_build_current_planning_codes':['L2'],'not_build_authorization':True})
intensity=np.zeros(m.shape,np.uint8);intensity[m]=1;intensity[reserve]=0;intensity[connector|((landuse==4))]=2
for i,mask in enumerate(node_masks):intensity[mask]=4 if i==0 else 3
intdefs=[(0,'保护/不建','禁止以提高密度为由推平或填满'),(1,'低覆盖、有用途开放地','小生产、植被、排水、地形与居民服务背景'),(2,'低建筑覆盖、高通行/周转','connector 和主次交通带'),(3,'次级紧凑混合节点','密集院落与多层使用，低于主核；不等于稀疏孤立建筑'),(4,'最高强度主核','窄街、上住下作、共享院落与公共服务近邻')]
capacity=[]
for n in nodes:
    lo,hi=n['density'];capacity.append({'node':n['id'],'gross_envelope_area':n['envelope_area'],'indicative_footprint_ratio':[lo,hi],'footprint_capacity':[round(n['envelope_area']*lo),round(n['envelope_area']*hi)],'meaning':'mature planning range, not current buildings, no exact building count or population'})
cover=[sum(c['footprint_capacity'][i] for c in capacity)/391002 for i in (0,1)]
write('human-use-intensity.json',{'status':STATUS,'owner_rule':'territory-wide Middle > West > East; local exceptions allowed','comparison_status':'D-025 design constraint, NOT measured existing cross-domain building coverage; West/East masterplans not authored here','zones':[{'id':f'H{c}','code':c,'name':name,'meaning':meaning,'area':int(((intensity==c)&m).sum()),'geometry':rle((intensity==c)&m)} for c,name,meaning in intdefs],'capacity':capacity,'middle_indicative_territory_footprint_ratio':cover,'density_qa':'principal ratio exceeds secondary ratios; preserve open terrain; future West/East aggregate scenarios must remain below accepted Middle scenario, not every local town','multilevel_use':'principally 2–3 storeys at N1; secondary predominantly 1–2/2; no modern high-rise'})
activity_specs=[('A1','日常市场/秤验/记录/纠纷协商重心',[308,1639]),('A2','共用仓院/装卸/车马寄存重心',[270,1690]),('A3','家庭生活/小供给/清洁取水储备重心',[340,1610]),('A4','轻修理/商住/旅宿混合重心',[350,1660])]
activity=[]
zz,xx=np.where(node_masks[0])
for aid,name,desired in activity_specs:
    j=int(np.argmin((xx+X0-desired[0])**2+(zz+Z0-desired[1])**2));x,z=int(xx[j])+X0,int(zz[j])+Z0
    activity.append({'id':aid,'name':name,'point':[x,z],'cached_y':int(y[z-Z0,x-X0]),'role':'activity focus inside shared mixed-use envelope; not exclusive zoning or building footprint'})
nodes[0]['activity_centres']=activity
write('principal-hub-structure.json',{'status':STATUS,'node':'N1','activity_centres':activity,'connections':[{'from':'A1','to':'A2','use':'daytime freight access and shared yard; loading kept out of domestic alleys'},{'from':'A1','to':'A3','use':'daily walk to food, public notice, worship/care services; no segregated housing tract'},{'from':'A1','to':'A4','use':'mixed shop/work/inn street; evening resident access maintained'}],'street_policy':'future main lanes 3–5 block order, pedestrian alleys 2–3; wider turning only at shared yards; widths are planning ranges, not frozen design','tenure_growth':'shared access easements and varied household/workshop yards; no repeated rectangular parcels'})
write('settlement-nodes.json',{'status':STATUS,'nodes':nodes,'minor_places':[{'id':'W1','point':[326,2326],'type':'conditional landing/seasonal handling point','permanent_town':False,'reason':'WB-003R X-03 water gap, steep backshore prevents unsupported compact town assumption'}],'secondary_remnant':{'columns':7,'geometry':rle(secondary),'role':'terrain reserve only'}})
first={'recommended_type':'混合街市公共秤验与小仓院','node':'N1','role':'货物称验/短存、街市纠纷记录与居民日常交易共享；院边可有经营者生活和小修理使用','scale':'中等规模，建筑及必需院落合计数百 block-column 量级；不冻结长宽、层数或 footprint','first_gate':'Local Site Gate inside N1 after masterplan acceptance; no fixed building coordinate','alternatives':[{'type':'工匠合作修造院','node':'N2','condition':'台地地方社区为先且上山通道局部复核通过'},{'type':'居民粮食与日用品合作仓','node':'N4','condition':'内谷饮水/排水及南路生活供给优先'}],'why_not_forced_inn':'first choice follows mixed daily economy and public exchange, not prior inn assumption','world_write_authorized':False}
write('MASTERPLAN.json',{'schema':'middle-masterplan/1','status':STATUS,'source_territory_revision':154,'source_territory_path':territory.relative_to(ROOT).as_posix(),'source_territory_sha256':sha(territory),'middle_exact_area':391002,'main_component_area':390995,'secondary_area':7,'D025_density_principle':'Middle > West > East territory-wide; mixed compact Middle, broad agrarian West, dispersed mountain East; local exceptions','subareas':[{'id':s['id'],'name':s['name'],'area':s['terrain']['area'],'geometry_file':'subareas.json'} for s in subareas],'settlement_hierarchy':[{'id':n['id'],'rank':n['rank'],'point':n['point'],'envelope_area':n['envelope_area']} for n in nodes],'proposed_corridors':{'file':'movement-network.json','ids':[r['id'] for r in routes]},'land_use_zones':{'file':'land-use.json','ids':[z['id'] for z in landzones]},'human_use_intensity_zones':{'file':'human-use-intensity.json','codes':[0,1,2,3,4]},'water_interfaces':water,'commons_interface':commons_interface,'east_interfaces':interfaces,'reserved_no_build_terrain':{'file':'land-use.json','code':'L2','area':int((landuse==2).sum())},'resident_life_system':{'file':'resident-life-system.json','systems':['food','water','waste','fire','mobility','public','tenure']},'principal_hub_internal_structure':{'file':'principal-hub-structure.json','activity_centres':['A1','A2','A3','A4']},'first_build_recommendation':first,'world_write_authorized':False,'new_world_block_reads':0,'broad_rescan':0,'freshness':'ACCEPTED CACHE EPOCH ONLY; future Local Site Gate must check current visible conditions','phasing':[{'id':'F0','scope':'masterplan review and water/access/artificial-content checks; no build'},{'id':'F1','scope':'only recommended single building Site Gate then separate design/authorization; no town batch'},{'id':'F2','scope':'N1 daily mixed neighborhood plus essential connections, each bounded task'},{'id':'F3','scope':'N2/N3 secondary compact communities and East interfaces as demand grows'},{'id':'F4','scope':'N4 living services; X-03 only after shore/navigation checks; retain terrain reserves'}]})

write('validation/planning-geometry.json',{'status':'PASS','middle_area':int(m.sum()),'subarea_area_sum':sum(s['terrain']['area'] for s in subareas),'subareas_cover_middle':bool(np.array_equal(labels>0,m)),'land_use_cover_middle':bool(np.array_equal(landuse>0,m)),'settlement_envelopes_disjoint':int(sum(mask.sum() for mask in node_masks))==int(claimed.sum()),'node_envelope_areas':[n['envelope_area'] for n in nodes],'no_envelope_in_reserve':not bool((claimed&reserve).any()),'no_envelope_in_commons_or_east':bool(m[claimed].all()),'all_paths_dry_middle':all(all(m[z-Z0,x-X0] for x,z,_ in rt['path']) for rt in routes),'secondary_7_reserved':bool((landuse[secondary]==2).all()),'world_writes':0})
print('nodes',[(n['id'],n['envelope_area']) for n in nodes], 'capacity',cover,flush=True)
print('routes',[(r['id'],r['length_blocks'],r['max_surface_step']) for r in routes],flush=True)

# 七张固定比例地图；背景 includes 邻域，但所有填色规划成员仅限 Middle。
OUT.joinpath('visual').mkdir(exist_ok=True);font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',18);small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',14)
pal=np.array([[25,39,50],[126,161,120],[65,83,86],[199,173,111],[118,163,187],[228,167,99],[184,145,187],[122,173,178],[170,173,119]],np.uint8)
basev=np.clip((y-60)/130,0,1);base_rgb=np.stack((80+basev*140,165-basev*80,140-basev*75),axis=2).astype(np.uint8);base_rgb[~m]=(base_rgb[~m]*.25).astype(np.uint8);base_rgb[a==255]=[20,43,62];base_rgb[a==0]=[155,132,67]
titles=['terrain-base','planning-subareas','settlement-hierarchy','movement-exchange','land-use-masterplan','human-use-density','phasing-first-build']
cn=['地形规划底图','自然骨架与规划子区','聚落层级与居民节点','交通与交换预留','混合土地使用总体图','使用强度与密度梯度','分期与首栋规划出口']
for kind,title in zip(titles,cn):
    rgb=base_rgb.copy()
    if kind=='planning-subareas':rgb[m]=(pal[labels[m]]*.65+base_rgb[m]*.35).astype(np.uint8)
    if kind=='land-use-masterplan':rgb[m]=(pal[landuse[m]]*.8+base_rgb[m]*.2).astype(np.uint8)
    if kind=='human-use-density':
        density_palette=np.array([[68,86,84],[119,145,119],[191,174,126],[193,138,83],[241,98,69]],np.uint8);rgb[m]=density_palette[intensity[m]]
    if kind in ('settlement-hierarchy','phasing-first-build'):
        for i,mask in enumerate(node_masks):rgb[mask]=pal[6 if kind=='phasing-first-build' and i in (1,2) else 5+i]
    im=Image.new('RGB',(1970,1100),(18,29,40));im.paste(Image.fromarray(rgb),(45,65));dr=ImageDraw.Draw(im)
    dr.text((25,12),'MD-001P · '+title+' · PLANNING PROPOSAL',font=font,fill='white')
    # accepted exact Middle outline at unit-column scale
    boundary=m&(~np.roll(m,1,0)|~np.roll(m,-1,0)|~np.roll(m,1,1)|~np.roll(m,-1,1))
    zz,xx=np.where(boundary)
    for z,x in zip(zz,xx):dr.point((45+int(x),65+int(z)),fill='#fff2c5')
    if kind in ('movement-exchange','land-use-masterplan','settlement-hierarchy','phasing-first-build'):
        for rt in routes:
            pts=[(45+x-X0,65+z-Z0) for x,z,_ in rt['path']];
            for j in range(0,len(pts)-1,12):dr.line(pts[j:j+8],fill='#6bdbe7',width=2)
            p=pts[len(pts)//2];dr.text(p,rt['id'],font=small,fill='white')
    for i,n in enumerate(nodes):
        x,z=n['point'];p=(45+x-X0,65+z-Z0);dr.ellipse((p[0]-5,p[1]-5,p[0]+5,p[1]+5),fill='#ffffff');dr.text((p[0]+8,p[1]-24),n['id'],font=font,fill='white')
    for it in [commons_interface,*interfaces,{'id':'I-W1','middle_point':[326,2326]}]:
        x,z=it['middle_point'];dr.text((45+x-X0+4,65+z-Z0+5),it['id'],font=small,fill='#a7ecf2')
    for x in range(-300,1201,100):dr.text((45+x-X0,43),str(x),font=small,fill='#d5e1e8')
    for z in range(1500,2400,100):dr.text((0,65+z-Z0),str(z),font=small,fill='#d5e1e8')
    dr.text((1670,65),'北 ↑  东 →\n等比例 1 px = 1 block\n浅线：revision 154 中域\n金底：Commons 邻域\n暗底：其他政治空间\n青虚线：预留，不是道路',font=small,fill='white',spacing=9)
    if kind=='planning-subareas':legend=[s['id']+' '+s['name'] for s in subareas]
    elif kind=='human-use-density':legend=[f'H{i} '+n+'\n'+d for i,n,d in intdefs]
    elif kind=='land-use-masterplan':legend=[f'L{i} '+n for i,n,_ in defs]
    elif kind=='phasing-first-build':legend=['F0 审核与 Local Site Gate','F1 N1 秤验与小仓院','F2 N1 混合生活街院','F3 N2 / N3 紧凑次节点','F4 N4 与南岸条件接口','所有阶段均需单独授权']
    else:legend=[n['id']+' '+n['name']+'\n'+str(n['envelope_area'])+' 格混合候选面' for n in nodes]+['I-W1 南岸候选：背岸陡','7格 secondary 仅保留']
    if kind=='terrain-base':dr.text((1670,230),'高程底色：Y60 绿 → Y190+ 棕红',font=small,fill='white')
    for i,line in enumerate(legend):
        yy=275+i*65;dr.rectangle((1670,yy,1683,yy+12),fill=tuple(density_palette[i] if kind=='human-use-density' else pal[min(i+1,8)] if kind in ('planning-subareas','land-use-masterplan') else ([90,100,110] if i in (0,5) else pal[5] if i in (1,2) else pal[6] if i==3 else pal[8]) if kind=='phasing-first-build' else pal[min(i+5,8)]));
        wrapped=[]
        for part in line.split('\n'):
            acc=''
            for char in part:
                if dr.textlength(acc+char,font=small)>265:wrapped.append(acc);acc=char
                else:acc+=char
            wrapped.append(acc)
        dr.text((1690,yy-3),'\n'.join(wrapped),font=small,fill='white',spacing=2)
    dr.line((65,1050,165,1050),fill='white',width=3);dr.text((65,1060),'100 blocks',font=small,fill='white');dr.text((250,1050),'缓存 epoch · 规划候选 ≠ 施工范围 · world writes = 0',font=font,fill='white')
    im.save(OUT/'visual'/(kind+'.png'))
write('validation/map-contract.json',{'pixel_size':[1970,1100],'map_origin_pixel':[45,65],'world_origin':[X0,Z0],'map_extent_exclusive':[X0,Z0,X1,Z1],'pixels_per_block_x':1,'pixels_per_block_z':1,'all_middle_columns_included':int(m.sum())==391002,'note':'circles are node symbols only; actual envelope membership is RLE, not circle radius'})
print('masterplan machine data and seven maps complete',flush=True)
