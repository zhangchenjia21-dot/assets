"""L1 因果规划对象与真实坐标图册；规划决定由文档解释，计算只作证据。"""
from pathlib import Path
import json,math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent;CACHE=ROOT.parents[3]/'MP-P02-cache'
P=np.load(CACHE/'regional-natural.npz');h=P['height'];l=P['land'];s=P['slope'];rel=P['relief'];art=P['artificial']
terrain=json.loads((ROOT/'evidence/terrain-patches.json').read_text(encoding='utf8'))['patches']
models=json.loads((ROOT/'evidence/corridor-models.json').read_text(encoding='utf8'))
def dump(n,v):(ROOT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
N=[]
def node(id,name,pt,radius,cap,hh,allow,shared,tid,parent,role,morph,why,catch,activation):
 x,z=pt;a=(slice(z-1440-radius,z-1440+radius+1),slice(x-256-radius,x-256+radius+1));m=l[a]==2
 N.append(dict(id=id,name=name,authority='DESIGN_PROPOSAL',scale='REGIONAL_SYSTEM',type='SETTLEMENT_CANDIDATE' if id!='NODE-04' else 'SERVICE_NODE_CANDIDATE',parent_ref=parent,
  location_search_envelope={'type':'bbox_search_only','bounds':[x-radius,z-radius,x+radius,z+radius],'representative_xz':pt,'point_ground_y':int(h[z-1440,x-256])},
  built_fabric_capacity={'area_range_blocks2':cap,'confidence':'LOW','status':'CONDITIONAL_TARGET_NOT_EXISTING','household_pressure_range':hh,'household_land_allowance_range':allow,'shared_land_range':shared,'arithmetic':[hh[j]*allow[j]+shared[j] for j in (0,1)],'includes':'内部通行/小院/共享服务','excludes':'完整矿场、燃料林、供水保护地、农业腹地','morphology':morph,'current_area':'UNVERIFIED','activation':activation},
  functional_hinterland={'type':'RELATIONAL','description':catch},role=role,why=why,terrain_ref=tid,
  witness={'search_land_columns':int(m.sum()),'low_resistance_columns':int((m&(s[a]<=.2)&(rel[a]<=12)).sum()),'artificial_flag_columns':int((m&(art[a]>0)).sum()),'height_percentiles':np.percentile(h[a][m],[10,50,90]).tolist(),'not_buildable_capacity':True},
  source_refs=['SRC-CANON','SRC-PARENT','SRC-OBS','SRC-DERIVED'],uncertainty=['资源/供水/现有人文实存未证','地形口袋不是建筑许可','本轮调查快照不是当前世界认证']))
node('NODE-01','北台地交换共同体',[812,1636],110,[4000,8000],[18,32],[130,160],[1660,2880],'TERRAIN-004','MP-P01R:NODE-05',
 {'population':'北组团主要常住服务','economic':'食物/工具交换、维修和分段储运','political':'东席地方共同体之一，非唯一首府','network':'北部内部集散','symbolic':'地方守约与共同会集'},
 '台地内紧凑生活/交换簇，向同高地适配而非整坡推平',
 ['上游北山服务角色','较大的连续低阻力口袋','较南侧生产台地低约41格'],
 '北部共同体和可服务资源；经 INTERFACE-01 接中域；不宣称覆盖整个东岛',
 '水源、实存、当期生计至少成立才可常住；否则缩为周期交换')
node('NODE-02','内侧生产共同体',[620,1948],90,[2000,5000],[10,22],[120,150],[800,1700],'TERRAIN-006','MP-P01R:NODE-05',
 {'population':'较小常住工作群','economic':'实际资源邻近的日常生产/维护，矿种未定','political':'地方自治，与北台地共享区域事务','network':'北组团内段而非全域货运终点','symbolic':'地方山地/祖先活动'},
 '较小台地簇，工作与居住有近邻关系但取水和污染分离',
 ['多个共同体约束','内侧低阻力口袋与北台地分离','两节点模型路距约456格而非大矿都单核'],
 '附近实际生产点/劳动者，不按圆形半径划矿权',
 '仅在附近资源或其它持续生计成立时常住；可退为北组团季节工作点')
node('NODE-03','东南条件共同体',[1652,2588],100,[3000,6000],[8,16],[150,200],[1800,2800],'TERRAIN-007','MP-P01R:NODE-06',
 {'population':'小量或零常住','economic':'远端实际生产就近支持','political':'东席地方共同体间接代表','network':'条件性末端，非已证稳定重货链','symbolic':'地方性'},
 '口袋内分散小簇，避开坡缘；不使用旧代表点所在高地中央',
 ['上游允许迁移远端节点','TERRAIN-007 位于原搜索窗内','长途严坡模型失败，应抑制规模'],
 '东南实际活动，不假定整片山体已开矿',
 '默认不批准常住开发；水/资源/运输与供给通过后才启用，未通过=0')
node('NODE-04','东侧暂歇服务点',[1188,1988],65,[500,1000],[0,0],[0,0],[500,1000],'TERRAIN-011','MP-P01R:ROUTE-06',
 {'population':'无独立常住目标','economic':'条件支线临时停留/缓存/事故支持','political':'通行服务协作，不设新自治领地','network':'仅服务已证远端流','symbolic':'无预设宏大象征'},
 '极小服务地，可嵌入已有活动，不默认独立聚落',
 ['长线路若成立需分段','候选口袋有位置但无需求证据','不得用有平地作为设镇理由'],
 'CORRIDOR-03/04 上实际使用者；没有流就无服务点',
 '随 NODE-03 启用；没有重复停留需求则为0；计入远端网络总容量')

rejected=N.pop();rejected['status']='REJECTED_AFTER_DETOUR_TEST';rejected['rejection_reason']='经此固定服务点多绕820格，无独立需求，撤销。';rejected['former_capacity_hypothesis']=rejected['built_fabric_capacity'];rejected['built_fabric_capacity']={'area_range_blocks2':[0,0],'status':'WITHDRAWN_NOT_FOR_HANDOFF','confidence':'NOT_APPLICABLE'}
routes=[]
purposes=[('食物/工具上山、产品下山、代表外出','PERIODIC_REGIONAL','北部与中域衔接；要求对端接收能力，不设计 Middle 聚落'),('居民/维修/产品内段交换','DAILY_LOCAL_AND_PERIODIC','多个共同体分享服务，避免制造等距节点'),('条件远端通行与少量缓存','CONDITIONAL_SEASONAL','撤销绕行暂歇点，保留直接条件支线而非已证干线'),('远端人员与减量产品','CONDITIONAL_LOW','严格地形模型失败，不设固定高吞吐')]
for m,(flow,intensity,why) in zip(models['corridors'][:3],purposes):
 selected=0 if m['models'][0]['status']=='DERIVED_CORRIDOR_ONLY' else 1
 routes.append(dict(id=m['id'],authority='DESIGN_PROPOSAL',from_id=m['from_id'],to_id=m['to_id'],flow=flow,intensity=intensity,frequency='日常局部/周期' if len(routes)<2 else '条件/季节',geometry={'type':'derived_search_alignment','model_ref':f"evidence/corridor-models.json#{m['id']}/models/{selected}",'xz':m['models'][selected]['xz'],'corridor_search_halfwidth_blocks':48,'not_right_of_way':True},why=why,confidence='LOW',usable_route='UNVERIFIED',source_refs=['SRC-OBS','SRC-DERIVED'],activation='L2 实际道路/净空/供给和跨包接口验证；远端段不能用数学连通代替承载'))
interface=dict(id='INTERFACE-01',authority='UPSTREAM_PLANNING_INPUT_NOT_CANON',parent_ref='MP-P01R:NODE-04',xz=[350,1600],role='中域接收端坐标，仅接口不设计对端',required_contract=['接受食物/工具输入需求并确认容量','核实交换产品接收与运力','公众访问不得依赖未经证实的专属通道'],status='UNCONFIRMED_CROSS_PACKAGE_INTERFACE')
demands=[]
for i,(driver,users,mag,freq,dep,ext,response) in enumerate([
 ('山地生产依赖日常生活和食物工具','居民、工匠、运输者','北组团28–54户压力假设','日常/周期',['NODE-01','NODE-02','INTERFACE-01'],'库存腐损、动物拥挤','共同体内部生活与周期交换分工，不每日全部下山'),
 ('多个地方共同体保有权利','地方成员、东席代表','低常设/周期高峰','周期',['NODE-01','NODE-02'],'公共访问被生产流挤占','共享事务附着可达节点而不设置全域矿都'),
 ('矿产丰富不等于任何位置都可开采','劳动者与工艺人员','具体产量UNRESOLVED','生产周期',['NODE-02','NODE-03'],'矿害、烟、耗水耗林','先证资源与燃料再决定加工链；保护取水'),
 ('长坡运输造成驻留和事故成本','远端队伍','小量/可能为0','条件季节',['NODE-03'],'缓存腐损、过度扩张','服务节点仅随真实流出现，嵌入优先'),
 ('专业魔法不能取代基本供给','所有常住与访问者','饮水/食物证据待补','每日',['NODE-01','NODE-02','NODE-03'],'污染与供给中断','各候选先水源和实存确认，未证不得升级为建设包')]):
  demands.append(dict(id=f'DEMAND-{i+1:02d}',authority='DESIGN_PROPOSAL',driver=driver,users=users,magnitude=mag,frequency=freq,maturity='MATURE_HYPOTHESIS / CONDITIONAL_REMOTE',dependencies=dep,externalities=ext,possible_response=response,priority='CORE' if i<3 else 'ESSENTIAL_SUPPORT'))
growth=[dict(id='GROWTH-01',authority='PLANNING_ASSUMPTION',driver='当期生计或资源使用',response='当地有水、有活动的生活工作簇',new_constraint='地方使用权与原有通路形成惯性',next_pressure='重复交换与修理',viability='没有未来远端开发仍须可自理；节点坐标不被宣称为古迹'),
dict(id='GROWTH-02',authority='PLANNING_ASSUMPTION',driver='北部交换重复且跨坡昂贵',response='北台地集中一部分服务，内侧保留工作生活',new_constraint='两台地间活动强化，对外需要中域接口',next_pressure='协作维护与供给缓冲',viability='无全域矿都也能运作；不为未来道路预留大轴线'),
dict(id='GROWTH-03',authority='PLANNING_ASSUMPTION',driver='地方之间的事务与共用工程',response='周期协商和代表外出分享交换通路',new_constraint='公共访问和地方权利不能被货运垄断',next_pressure='只在远端产生真实剩余时向外延伸',viability='停在北组团仍是成立的区域系统'),
dict(id='GROWTH-04',authority='PLANNING_ASSUMPTION',driver='远端资源/水/路/供给都证明',response='东南小共同体与必要暂歇服务',new_constraint='高运输损耗与维护负担',next_pressure='可能季节化、撤退或改线',viability='没有证据则不发生，不用未来收益正当化当前常住')]
spaces=[dict(id='SPACE-01',authority='DESIGN_PROPOSAL',scope=['NODE-01','NODE-02','NODE-03'],type='water_and_slope_reserve_search',controller='各地方共同体，跨节点影响协商',users='下游用水与边坡受益者',purpose='先查供水、侵蚀与污染隔离',when='持续',why_unbuilt='维持生活和坡地稳定比填满候选窗优先',geometry='UNRESOLVED，不据未知风向水流画硬边界'),dict(id='SPACE-02',authority='DESIGN_PROPOSAL',scope=['NODE-01','NODE-02'],type='shared_service_and_access',controller='参与共同体',users='居民与访问者',purpose='交易、协商、通行及工作交接',when='日常与周期',why_unbuilt='共享使用和访问权，不作为剩余地出售',geometry='L2 refine; capacity included, not extra area')]
anchors=[dict(id=f'ANCHOR-{i+1:02d}',node=n['id'],scale='Regional',authority='DESIGN_PROPOSAL',role=['GROWTH_ANCHOR','ORIGIN_ANCHOR','ORIGIN_ANCHOR','GROWTH_ANCHOR'][i],why=n['why'],when='GROWTH-02' if i==0 else ('GROWTH-01' if i==1 else 'GROWTH-04'),attracts=n['role']['economic'],repels='损害饮水、安全或公共访问的活动',morphology=n['built_fabric_capacity']['morphology'],removal_effect=['服务分散回各共同体，对外货压下降','北台地居民/工作需求减少，内部通道退为低量','远端支线与暂歇需求一起取消','若无需驻留则取消，不影响地方政治 Canon'][i]) for i,n in enumerate(N)]
packages=[]
for i,(ns,name) in enumerate([(['NODE-01'],'北台地交换聚落'),(['NODE-02'],'内侧生产聚落'),(['NODE-03'],'东南条件聚落')]):
 parent=ns[0];packages.append(dict(id=f'PACKAGE-{i+1:02d}',authority='DESIGN_PROPOSAL_PENDING_REVIEW',parent_plan='MP-P02-EAST',parent_revision='r1',parent_scale='REGIONAL_SYSTEM',child_scale='SETTLEMENT',recipient='minecraft-planner',scope=ns,name=name,why='落实区域分工并验证常住成立条件，未授权建筑设计',scope_search_geometry=[{'node':n['id'],'search':n['location_search_envelope']} for n in N if n['id'] in ns],
 UPSTREAM_FIXED=['多个共同体而非全域单核矿都','矿产是区域 Canon 不能虚构指定矿脉','不得以搜索窗清空现有实存']+(['远端支线必须满足启用条件；固定 NODE-04 已撤销'] if i==2 else ['北组团生活/交换分工；与其它节点可用通道及公共访问兼容']),
 DOWNSTREAM_TO_RESOLVE=['现有方块体积/路/建筑/地权及人工材料标记，先观察再拟形态','饮水可靠性、食物和燃料来源、具体生产依据','通道实际坡道/净空/跨越/实存冲突','内部主要活动、服务接续、规模与密度、开放地','L2 anchors / sequence / settlement morphology，再交 L3'],
 DOWNSTREAM_ADAPTABLE=['在本轮搜索逻辑内迁移并保留主要依赖','共享或嵌入服务、内部容量分配','缩小/分簇或季节化；条件远端可为0'],
 REVISION_TRIGGER=['没有水或生计且附近无法替代','承载不足迫使区域关系/规模数量级改变','通道或已有实存使跨节点关系无法局部调整'],revision_protocol='报 UPSTREAM_PLANNING_ISSUE，列证据及最小受影响 node/flow/capacity；父案新增 revision 并使关联 child stale，不改 Canon 或直接覆盖上游。',
 capacity_hypothesis=[{'node':n['id'],'built_fabric_capacity':n['built_fabric_capacity'],'functional_hinterland':n['functional_hinterland']} for n in N if n['id'] in ns],upstream_flow_refs=[r['id'] for r in routes if r['from_id'] in ns or r['to_id'] in ns],cross_package_dependencies=[f'PACKAGE-{j:02d}' for j in range(1,4) if j!=i+1],external_interface='INTERFACE-01 需对端验证，本包不能设计或批准 Middle',source_refs=['SRC-PARENT','SRC-CANON','SRC-OBS','SRC-DERIVED'],expected_outputs=['实存/自然证据与版本','供给/通达的明确结论或有界分支','SETTLEMENT Plan 与容量图','L3 DISTRICT 包，非直接 Builder 包'],world_write_authorization=False,builder_ready=False,execution_precondition='父案关系用于本 regression；未自动升级 World Canon。可先进行无写入的 L2 调查；常住/建设不得跳过证据条件。'))
context=dict(plan_id='MP-P02-EAST',revision='r1',scale='REGIONAL_SYSTEM',state='HANDOFF_READY',review_status='AWAITING_GPT_OWNER',parent_package='MP-P01R-CIV001/r1/PACKAGE-03',parent_authority='USER_SELECTED_REGRESSION_INPUT_NOT_WORLD_CANON',skill='minecraft-planner v0.2',world_writes=0,fabric_observation_state='EXISTING_FABRIC_UNVERIFIED',fabric_note='仅见原调查人工材料标记；不是结构实存识别或清空授权',evolution_logic='EXISTING_EVOLUTION',maturity='北组团成熟工作假设；远端条件',bounds=[256,1440,2175,3263],bounds_semantics='analysis extent, not political border')
dump('planning-objects.json',dict(context=context,nodes=N,rejected_candidates=[rejected],corridors=routes,interfaces=[interface],anchors=anchors,spaces=spaces))
dump('demand-model.json',demands);dump('growth-sequence.json',growth);dump('implementation-packages.json',packages)
dump('building-program.json',[dict(id=f'PROGRAM-{i+1:02d}',demand=d['id'],functions=d['possible_response'],magnitude=d['magnitude'],adjacency=d['dependencies'],maturity=d['maturity'],externality=d['externalities'],shared_embedded_dedicated='共享/嵌入优先，专用量级须L2证明',uncertainty='不规定建筑数量/平剖面',recipient='SETTLEMENT Planner') for i,d in enumerate(demands)])
dump('settlement-capacity.json',dict(nodes=[{'id':n['id'],'capacity':n['built_fabric_capacity']} for n in N],north_total=[6000,13000],parent_north=[6000,14000],remote_total_if_activated=[3000,6000],remote_if_not_activated=0,parent_remote=[3000,9000],total_if_both_activated=[9000,19000],note='远端内部服务已计入N03；固定NODE-04已撤销，不重复计户。没有全区域人口/粮食自给认证。'))
dump('parent-delta.json',dict(parent='MP-P01R PACKAGE-03',authority='REGRESSION_PARENT_NOT_CANON',changes=[{'parent':'NODE-05','children':['NODE-01','NODE-02'],'action':'split capacity and location within original search','old_area':[6000,14000],'new_area':[6000,13000],'reason':'两个分离地形口袋与日常/区域服务分工'}, {'parent':'NODE-06','children':['NODE-03'],'action':'move primary within search; reject fixed relay after detour test','old_area':[3000,9000],'new_area_if_activated':[3000,6000],'reason':'通道严格模型失败，资源/供给未证，不提高容量'}, {'parent':'ROUTE-05/06','action':'replace conceptual lines with bounded resistance alternatives, no construction guarantee'}],fixed_relations_preserved=True,upstream_planning_issue='NONE_ESTABLISHED; strict-model failure alone is not proof all routes impossible',parent_files_modified=False))

# 地图：实际比例，彩圆只作面积符号，地形口袋另为绿色成员。
(ROOT/'maps').mkdir(exist_ok=True)
fontpath='C:/Windows/Fonts/msyh.ttc'
def f(n):return ImageFont.truetype(fontpath,n)
tt=np.clip((h-63)/237,0,1);rgb=np.stack([190-65*tt,205-104*tt,162-70*tt],axis=-1);gy,gx=np.gradient(h.astype(float));rgb=np.uint8(np.clip(rgb*np.clip(1+.025*(gx+gy),.7,1.1)[:,:,None],0,255));rgb[l!=2]=[129,174,190]
base=Image.fromarray(rgb)
colors=['#b85b2a','#885bb1','#27728d','#b07720']
specs=[('01','区域系统与通道',[256,1440,2176,3264],['NODE-01','NODE-02','NODE-03'],'network'),('02','北组团：位置、规模、地形',[352,1440,1152,2080],['NODE-01','NODE-02'],'capacity'),('03','东南条件网络：位置与规模',[1000,1840,2120,3008],['NODE-03'],'capacity'),('04','条件生长与服务关系',[256,1440,2176,3264],['NODE-01','NODE-02','NODE-03'],'growth')]
for num,title,bounds,shown,mode in specs:
 xmin,zmin,xmax,zmax=bounds;scale=min(1400/(xmax-xmin),1170/(zmax-zmin));mw=int((xmax-xmin)*scale);mh=int((zmax-zmin)*scale);ox=85;oy=130
 im=Image.new('RGB',(2180,1510),'#f5f1e8');im.paste(base.crop((xmin-256,zmin-1440,xmax-256,zmax-1440)).resize((mw,mh)),(ox,oy));d=ImageDraw.Draw(im)
 def xy(p):return(ox+(p[0]-xmin)*scale,oy+(p[1]-zmin)*scale)
 d.text((85,25),'MP-P02 · 东域山地共同体  |  '+title,font=f(30),fill='#263d40');d.text((85,76),'L1 REGIONAL_SYSTEM · r1 · 提案待审 · 北 ↑ (-Z) · world writes = 0',font=f(22),fill='#4f6063')
 for x in range(math.ceil(xmin/200)*200,xmax,200):
  u,v=xy([x,zmin]);d.line((u,oy,u,oy+mh),fill='#cdd4c9');d.text((u-18,oy+mh+7),str(x),font=f(18),fill='#304a4d')
 for z in range(math.ceil(zmin/200)*200,zmax,200):
  u,v=xy([xmin,z]);d.line((ox,v,ox+mw,v),fill='#cdd4c9');d.text((8,v),str(z),font=f(18),fill='#304a4d')
 # 自然低阻力口袋只在局部规模图显出，不作为拟建轮廓。
 if mode=='capacity':
  for patch in terrain:
   for zz,xx in patch['cells']:
    x=256+xx*8;z=1440+zz*8
    if xmin<=x<xmax and zmin<=z<zmax:
     a=xy([x,z]);b=xy([x+8,z+8]);d.rectangle((*a,*b),outline='#78966d',width=1)
 for i,c in enumerate(routes):
  pts=c['geometry']['xz'];col=('#85663c' if i<2 else '#9e5c65') if mode!='growth' else ('#bd7935' if i<2 else '#858080')
  for j,(a,b) in enumerate(zip(pts,pts[1:])):
   if xmin<=a[0]<xmax and zmin<=a[1]<zmax and xmin<=b[0]<xmax and zmin<=b[1]<zmax:
    if i<2 or j%4<2:d.line([xy(a),xy(b)],fill=col,width=3)
  labelpt=pts[len(pts)//2]
  if xmin<=labelpt[0]<xmax and zmin<=labelpt[1]<zmax:
   uu,vv=xy(labelpt);d.text((uu+6,vv+6),f'C{i+1:02d}',font=f(19),fill=col,stroke_width=2,stroke_fill='#f5f1e8')
 if xmin<=350<xmax and zmin<=1600<zmax:
  u,v=xy([350,1600]);d.rectangle((u-6,v-6,u+6,v+6),fill='#325b69');d.text((u+10,v),'I01 中域接口',font=f(18),fill='#325b69')
 for i,n in enumerate(N):
  if n['id'] not in shown:continue
  x,z=n['location_search_envelope']['representative_xz'];u,v=xy([x,z]);lo,hi=n['built_fabric_capacity']['area_range_blocks2'];rlo=math.sqrt(lo/math.pi)*scale;rhi=math.sqrt(hi/math.pi)*scale
  if mode=='capacity':
   b=n['location_search_envelope']['bounds'];a=xy(b[:2]);bb=xy(b[2:]);
   for aa,bbb in [((a[0],a[1]),(bb[0],a[1])),((bb[0],a[1]),(bb[0],bb[1])),((bb[0],bb[1]),(a[0],bb[1])),((a[0],bb[1]),(a[0],a[1]))]:
    leng=math.dist(aa,bbb)
    for step in range(0,int(leng),14):d.line((aa[0]+(bbb[0]-aa[0])*step/leng,aa[1]+(bbb[1]-aa[1])*step/leng,aa[0]+(bbb[0]-aa[0])*min(step+7,leng)/leng,aa[1]+(bbb[1]-aa[1])*min(step+7,leng)/leng),fill='#5c6e77',width=2)
  overlay=Image.new('RGBA',im.size);dd=ImageDraw.Draw(overlay);c=tuple(int(colors[i][k:k+2],16) for k in [1,3,5]);dd.ellipse((u-rhi,v-rhi,u+rhi,v+rhi),fill=c+(40,),outline=c+(255,),width=2);dd.ellipse((u-rlo,v-rlo,u+rlo,v+rlo),fill=c+(100,));im=Image.alpha_composite(im.convert('RGBA'),overlay).convert('RGB');d=ImageDraw.Draw(im);d.text((u+9,v-31),n['id'].replace('NODE-','N'),font=f(23),fill=colors[i],stroke_width=2,stroke_fill='white')
 panel=1530;py=140
 lines=['底图：R1 地面高程；蓝 = 水','C01 粮食/工具入山，产品出山','C02 居民与日常/工作交换','C03 远端小量条件流（虚线）','线是阻力搜索，不是道路或路权','绿色小格：派生低阻力地形口袋','虚线框：搜索；内圆/外环：面积','圆非实际城界；腹地为交叠关系','棕线较严、红线较宽松地形模型'] if mode!='growth' else ['G1 当地生计/资源使用形成共同体','G2 北部交换与生活工作分工','G3 公共访问分享北部服务链','G4 仅在水/资源/路/供给成立后','     出现远端活动与暂歇需求','灰线与 N03 可整体不发生','政治权力仍来自多个共同体','不是四阶段都必须发生的年表']
 for t in lines:d.text((panel,py),t,font=f(21),fill='#3f5558');py+=33
 py+=20
 for i,n in enumerate(N):
  lo,hi=n['built_fabric_capacity']['area_range_blocks2'];x,z=n['location_search_envelope']['representative_xz'];d.text((panel,py),n['id'].replace('NODE-','N')+' '+n['name'],font=f(22),fill=colors[i]);py+=34;d.text((panel,py),f'{lo/1000:g}–{hi/1000:g} 千格² · LOW'+(' / 或0' if i>1 else ''),font=f(21),fill='#354b4e');py+=32;d.text((panel,py),f'X{x}, Z{z} · Y{n["location_search_envelope"]["point_ground_y"]}',font=f(19),fill='#526368');py+=48
 d.text((panel,py+5),'北组团合计 6–13 千格²\n远端若启用合计 3–6 千格²\n供水、生计、实存和通行仍待证。\n固定暂歇点已撤销，不为平地设点。',font=f(21),fill='#354b4e',spacing=8)
 d.line((85,1380,85+200*scale,1380),fill='#243d42',width=4);d.text((85,1395),'200 blocks',font=f(20),fill='#354b4e')
 d.text((440,1350),'Source: WB-002R-R1 / base bc96aa5；X向右，Z向下。\nParent: MP-P01R PACKAGE-03（本轮 regression 输入，不是 World Canon）\n没有当前存档 freshness、建筑实存或人口承载认证。',font=f(20),fill='#53686b',spacing=7)
 im.save(ROOT/'maps'/f'{num}.png')
# 比较剖面使用地面均值，不画虚假的路面设计高程。
im=Image.new('RGB',(1900,1280),'#f5f1e8');d=ImageDraw.Draw(im);d.text((65,20),'MP-P02 · 阻力通道剖面比较（地形均值，不是道路纵断设计）',font=f(30),fill='#2d474a')
for i,m in enumerate(models['corridors'][:4]):
 ox=95;oy=130+i*265;d.text((ox,oy-42),m['id']+' '+m['from_id']+' → '+m['to_id'],font=f(22),fill='#354b4e')
 maxlen=max(v.get('length_blocks',1) for v in m['models']);d.rectangle((ox,oy,ox+1140,oy+180),outline='#a5b0ad')
 for j,v in enumerate(m['models']):
  if 'xz' not in v:d.text((1280,oy+j*65),'grade≤0.25：该模型无路',font=f(20),fill='#9b4b4b');continue
  pts=v['xz'];dist=[0.]
  for a,b in zip(pts,pts[1:]):dist.append(dist[-1]+math.dist(a,b))
  points=[(ox+x/maxlen*1140,oy+180-(y-40)/260*180) for x,y in zip(dist,v['height_profile'])];color=['#895f29','#a05b71'][j];d.line(points,fill=color,width=3)
  d.text((1280,oy+j*65),f'grade≤{v["grade_cap"]}: {v["length_blocks"]}格\n累计上升 {v["cumulative_ascent"]}格；逐格最大阶差 {v["max_fine_surface_step"]}',font=f(19),fill=color,spacing=5)
 d.text((ox,oy+183),f'横轴 0—{maxlen} 格；纵轴 Y40—300',font=f(17),fill='#53656b')
d.text((95,1210),'8格平均地面模型；严格/宽松阈值是分析假设。路存在不等于可驮运；无路不等于工程绝对不可行。',font=f(21),fill='#53656b');im.save(ROOT/'maps/05.png')
html='<!doctype html><meta charset="utf-8"><title>MP-P02 东域区域图册</title><style>body{font:18px system-ui;background:#f5f1e8;color:#30494d;margin:24px}img{width:100%}button{padding:10px;margin:5px}</style><h1>MP-P02 东域山地共同体系统</h1><p>REGIONAL_SYSTEM · HANDOFF_READY / 待审 · world writes = 0</p><p>先看区域关系，再看两个局部规模图。面积圆是尺度符号，非建设边界；条件节点可不发生。</p>'
for num,name in [('01','区域网络'),('02','北组团规模'),('03','东南条件规模'),('04','条件生长'),('05','通道剖面')]:html+=f'<button onclick="document.getElementById(\'map\').src=\'maps/{num}.png\'">{name}</button>'
html+='<p><a href="区域规划方案.md">完整区域规划</a> · <a href="implementation-packages.json">SETTLEMENT Planner 包</a></p><img id="map" src="maps/01.png">'
(ROOT/'区域图册.html').write_text(html,encoding='utf8');print('3 active nodes / 3 corridors / 3 SETTLEMENT packages / 5 maps generated')
