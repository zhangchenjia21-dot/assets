"""MP-P01：读取白名单自然栅格，计算候选阻力走廊，输出当前尺度提案；不访问世界。"""
from pathlib import Path
import numpy as np,sqlite3,json,hashlib,heapq,math,html,subprocess,gzip
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent;REPO=R.parents[1];G=R.parent/'建筑师/research';SRC=G/'human-geography/southern-island/WB-002R-R1'
def save(name,data):p=R/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
db=Path('D:/Games/Minecraft/AI工程/MP-P01-cache/observed.sqlite')
if not db.exists():
 db.parent.mkdir(parents=True,exist_ok=True);db.write_bytes(gzip.decompress((SRC/'raw-or-queryable/observed.sqlite.gz').read_bytes()))
assert sha(db)=='01d115d6c686cc6d59772cfc68e1cbd50a5816045eeaa7f48fa8a4a8d4a791b7'
c=sqlite3.connect('file:'+db.as_posix()+'?mode=ro',uri=True)
H=np.full((264,408),-999,dtype=np.int16)
for x,z,y in c.execute('select x,z,exposed_y from samples where (x+800)%8=4 and (z-1376)%8=4'):H[(z-1376)//8,(x+800)//8]=y
assert not (H==-999).any()
derived=np.load(SRC/'raw-or-queryable/derived.npz');L=derived['land_component'][4::8,4::8];S=derived['slope8'][4::8,4::8]
np.savez_compressed(R/'terrain-sample.npz',elevation=H,land_component=L,slope=S,x0=-796,z0=1380,step=8)
def cell(x,z):return (round((z-1380)/8),round((x+796)/8))
def coord(p):return [-796+p[1]*8,1380+p[0]*8]
def nearest(x,z,land):
 p=cell(x,z);candidates=[(math.hypot(i-p[0],j-p[1]),(i,j)) for i in range(max(0,p[0]-12),min(264,p[0]+13)) for j in range(max(0,p[1]-12),min(408,p[1]+13)) if L[i,j]==land];assert candidates;return min(candidates)[1]
# 位置由本轮地形及因果判断提出；算法只把代表点约束到对应自然陆块，不生成社会判断。
specs=[
('01','西部腹地集市',-410,2160,1,'regional_center','GROWTH-01','西域居民、农牧与常见手工业的日常中心','低地粮食/牲畜与家庭加工先可自立；丰余交换使腹地节点先于联盟出现','高常住、周期来客；服务西岛南部腹地','粮食季节性集散；不得吞噬连续生产地'),
('02','北弧次级集市',-200,1510,1,'secondary_market','GROWTH-01','西岛北弧家庭与牧用地','C 形陆路绕行成本使北弧不必每日依赖南部中心','中低常住、地方集市；与01竞争北西接壤腹地','保留分散生产，不铺成连续城带'),
('03','西岸内湾接驳候选',-440,1790,1,'gateway','GROWTH-02','跨水粮运、旅人和议事代表','接近公地的内湾岸段减少陆运绕行，但岸坡和航道尚待核实','少量常住、季节性高吞吐；不是人口首位城','装卸与候渡共用到达走廊，候渡不阻日常通行'),
('04','联盟公地代表点',-120,1790,2,'institutional_center','GROWTH-03','三席、裁决、共同誓约与公共工程协商','共同主权降低地方主城独占议会的制度成本','低常住但高政治位阶；不等同经济首都','准确边界只引用 Canon，点不是公地面域'),
('05','坡麓转换中心候选',276,1764,2,'regional_gateway','GROWTH-02','跨岛交换、仓储、加工和山地驮运','低地进入山坡的成本转换使货物分批、换载和结算集中','中等常住、跨域吞吐高；不垄断全部外贸','重货停在低处，居民和洁净补给避污染物流'),
('06','北山共同体服务候选',644,1756,2,'mountain_service','GROWTH-01','多个山地地方共同体','适度高地停留面连接周边生产点；具体矿口未定，不能先造矿城','中低常住、山地多点服务；东席不集中为单王城','矿口与水源发现后可在搜索窗内迁移；禁止默认露天矿'),
('07','东北坡地交换候选',1116,2108,2,'specialized_exchange','GROWTH-04','东岛东北坡地与北山支线','山脊以东的侧向联系避免所有货物翻越主峰','条件性中低常住；与06分担山地服务','须核实连续缓坡和清洁水；未满足不升级常年中心'),
('08','东南共同体服务候选',1900,2660,2,'mountain_service','GROWTH-04','远离北侧接口的东南地方共同体','狭长岛体使远端地方服务有理由独立，不必日常进公地','条件性低常住、地方补给与季节集散','未有可持续水/粮/燃料方案时只保留季节节点'),
('09','南岸海运替代候选',1420,3188,2,'conditional_gateway','GROWTH-04','远端矿产/石材批量外运与返程粮食','若重货足够且航行可靠，绕岛海运可替代跨脊重车','可选低人口高货流；需求不足不成立','不宣称天然港，不预设外部贸易伙伴')]
nodes=[];lookup={}
for no,name,x,z,land,role,stage,users,why,catchment,note in specs:
 p=nearest(x,z,land);x,z=coord(p);ident='SETTLEMENT-'+no;lookup[ident]=p
 nodes.append({'id':ident,'name':name,'type':'settlement_search_anchor','scale':'POLITY_TERRITORY','authority':'DESIGN_PROPOSAL','geometry':{'type':'Point','coordinates':[x,z],'coordinate_system':'Minecraft overworld X,Z; north=-Z','meaning':'搜索窗代表点，不是城址/码头/建筑定位','search_halfwidth_blocks':96},'observed_at_sample':{'exposed_y':int(H[p]),'land_component':land,'slope8':float(S[p])},'role':role,'historical_stage':stage,'users':users,'why':why,'catchment':catchment,'downstream_implication':note,'source_refs':['E-CANON','E-R1','E-ATLAS'],'uncertainty':['实址须 L1/L2 核实水、可用台地和出入接口'],'population_role':catchment,'political_role':'三席共同主权' if no=='04' else '地方自治下的功能节点','symbolic_role':'共同誓约' if no=='04' else '地方身份，不自动赋予圣地资格'})
def pathfind(a,b,mode):
 dist={a:0.};prev={};queue=[(0.,a)];landid=int(L[a]);end=b
 while queue:
  cost,p=heapq.heappop(queue)
  if cost!=dist[p]:continue
  if p==end:break
  for di,dj in [(0,1),(1,0),(0,-1),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]:
   q=(p[0]+di,p[1]+dj)
   if not(0<=q[0]<264 and 0<=q[1]<408):continue
   if mode=='land' and (L[q]!=landid or (di and dj and (L[p[0]+di,p[1]]!=landid or L[p[0],p[1]+dj]!=landid))):continue
   length=8*math.hypot(di,dj);rise=abs(float(H[q])-float(H[p]));
   if mode=='land' and rise/length>.75:continue
   weight=(1+6*rise/length+3*max(0,float(S[q]))) if mode=='land' else (1 if L[q]==0 else 50)
   new=cost+length*weight
   if new<dist.get(q,1e99):dist[q]=new;prev[q]=p;heapq.heappush(queue,(new,q))
 assert end in dist,(a,b,mode)
 chain=[end]
 while chain[-1]!=a:chain.append(prev[chain[-1]])
 chain.reverse();return chain,dist[end]
route_specs=[('01','01','03','land','粮食、日常市场与赴会合流','REGIONAL','GROWTH-02'),('02','02','03','land','北弧居民与低地产品','REGIONAL','GROWTH-02'),('03','03','04','water','代表/旅人及轻货候选渡运','STRATEGIC','GROWTH-03'),('04','04','05','land','公地与中域政治连接，重货不强制穿公地','STRATEGIC','GROWTH-03'),('05','05','06','land','粮食上山、制品下山、驮运接续','REGIONAL','GROWTH-02'),('06','06','07','land','山地侧向共同体联系','REGIONAL','GROWTH-04'),('07','07','08','land','分段驮运与信息支线，不假定连续重车道','LOW','GROWTH-04'),('08','08','09','land','条件性货物集运到南岸','REGIONAL_CONDITIONAL','GROWTH-04'),('09','03','05','water','商业货物直达中域，分离议事流','REGIONAL','GROWTH-02'),('10','09','05','water','条件性绕島海运：批量货物与返程粮食','REGIONAL_CONDITIONAL','GROWTH-04')]
routes=[]
for no,aa,bb,mode,flow,mag,stage in route_specs:
 aa='SETTLEMENT-'+aa;bb='SETTLEMENT-'+bb;chain,cost=pathfind(lookup[aa],lookup[bb],mode);length=sum(math.dist(coord(p),coord(q)) for p,q in zip(chain,chain[1:]));rise=sum(abs(float(H[q])-float(H[p])) for p,q in zip(chain,chain[1:]))
 routes.append({'id':'ROUTE-'+no,'authority':'DESIGN_PROPOSAL','from':aa,'to':bb,'mode':mode,'flow':flow,'magnitude':mag,'historical_stage':stage,'geometry':{'type':'LineString','coordinates':[coord(p) for p in chain],'meaning':'8格抽样阻力候选线；非道路中心线施工许可'},'sampled_length_blocks':round(length),'sampled_absolute_rise':round(rise),'resistance_cost':round(cost),'max_sample_grade':max(abs(float(H[q])-float(H[p]))/math.dist(coord(p),coord(q)) for p,q in zip(chain,chain[1:])),'status':'CANDIDATE_REQUIRES_LOCAL_SURVEY','limitations':['8格采样可能漏窄沟、崖、人工物；不验证净空/碰撞/驮队通行','水线包含岸端接入，不是已验证船道；未知水深流向/风浪'] if mode=='water' else ['线为区域走廊见证，不证明连续可用路线；重货须另行纵断和转运设计'],'source_refs':['E-R1','A-TRANSPORT']})
save('planning-objects.json',{'plan_id':'MP-P01','revision':1,'state':'HANDOFF_READY','scale':'POLITY_TERRITORY','context_modifier':'GREENFIELD','context_note':'实际人文现状未查询；仅在未建关系规划意义采用 GREENFIELD，任何已存在对象须下游保护，历史序列是提案而非实存。','bounds':[-800,1376,2463,3487],'authority':'DESIGN_PROPOSAL','world_writes':0,'nodes':nodes,'routes':routes,'canon_constraints':[{'id':'CANON-COMMONS','authority':'APPROVED_CANON','geometry':{'type':'source_reference','definition':'A ∩ X<=88；connector A∩X>=89；接口 Z1726..1774','exact_mask_not_loaded':True},'area_blocks2':92124,'note':'不把代表点/矩形当作精确公地轮廓，不读取后续规划面域。'}]})
save('route-diagnostics.json',[{k:v for k,v in r.items() if k!='geometry'} for r in routes])
colors=np.zeros((*H.shape,3),np.uint8);colors[:]=[64,112,139]
for lo,hi,col in [(0,80,(198,203,155)),(80,120,(154,174,123)),(120,180,(146,148,114)),(180,240,(140,119,105)),(240,400,(205,199,189))]:colors[(L>0)&(H>=lo)&(H<hi)]=col
Image.fromarray(colors).resize((1632,1056)).save(R/'maps/terrain-base.png')
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',18);small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',15);titlefont=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',30)
def px(p):return (70+(p[0]+800)/2,110+(p[1]-1376)/2)
def drawmap(name,title,stage=4,flows=True):
 im=Image.new('RGB',(1780,1340),(240,239,228));im.paste(Image.open(R/'maps/terrain-base.png'),(70,110));d=ImageDraw.Draw(im);d.text((70,22),title,font=titlefont,fill='#223331');d.text((70,65),'POLITY_TERRITORY · MP-P01 r1 · 底图=实测抽样 / 节点及走廊=设计提案',font=font,fill='#30423d')
 for x in range(-800,2464,400):p=px((x,1376));d.line((p[0],110,p[0],1166),fill='#a1b4b0');d.text((p[0],90),str(x),font=small,fill='black')
 for z in range(1400,3488,200):p=px((-800,z));d.line((70,p[1],1702,p[1]),fill='#a1b4b0');d.text((13,p[1]),str(z),font=small,fill='black')
 if flows:
  for r in routes:
   if int(r['historical_stage'][-2:])>stage:continue
   points=[px(v) for v in r['geometry']['coordinates']];col='#ffe47c' if r['mode']=='land' else '#7de5ff'
   d.line(points,fill=col,width=5)
   mid=points[len(points)//2];d.text(mid,r['id'][-2:],font=small,fill='black',stroke_width=2,stroke_fill='white')
 for n in nodes:
  if int(n['historical_stage'][-2:])>stage:continue
  p=px(n['geometry']['coordinates']);r=11 if n['id'] in ('SETTLEMENT-01','SETTLEMENT-04','SETTLEMENT-05') else 7;d.ellipse((p[0]-r,p[1]-r,p[0]+r,p[1]+r),fill='#cd734a',outline='white',width=2);offset={'SETTLEMENT-03':(-175,18),'SETTLEMENT-04':(-50,-48),'SETTLEMENT-05':(13,18)}.get(n['id'],(13,-24));d.text((p[0]+offset[0],p[1]+offset[1]),n['id'][-2:]+' '+n['name'],font=font,fill='#10212a',stroke_width=2,stroke_fill='#eeeede')
 p=px((89,1726));q=px((89,1774));
 if stage>=3:d.line([p,q],fill='#ce2e72',width=6)
 d.text((1360,135),'N ↑（-Z）  E →（+X）',font=font,fill='white');d.line((1400,1125,1650,1125),fill='white',width=4);d.text((1410,1130),'500 blocks',font=font,fill='white')
 for i,text in enumerate(['浅绿 <Y80；绿 Y80–119；灰绿 Y120–179；棕 Y180–239；浅灰 ≥Y240；蓝为水面/非陆块。','橙点=搜索代表点（非城址）；黄线=陆运候选；青线=渡运候选；粉线=Canon 公地东侧接口。','节点编号对应 planning-objects.json；连线不是施工线，山区优先驮运；未验证桥址、船道、水源或矿口。','坐标范围 X[-800,2463] Z[1376,3487]；R1 1格实测→8格抽样。snapshot bc96aa5 lineage；2026-09-13 制图。','岛形不是政治区界；Commons 精确面域仅引用 Canon，未用图上点或包络代替。']):d.text((70,1190+i*26),text,font=small,fill='#263a3a')
 im.save(R/f'maps/{name}.png')
drawmap('territory','整体结构｜低岛生产腹地—转换接口—多点山地共同体',flows=False)
drawmap('flows','长期流通｜陆运候选与分流渡运，山地主脊不是重货直通道')
for stage in [1,2,3,4]:drawmap('growth-'+str(stage),f'假设性生长阶段 {stage}｜每阶段独立可运作；不是既有历史事实',stage)
save('map-register.json',{'coordinate_system':'Minecraft X,Z; units=blocks; north=-Z','sampling':{'step':8,'origin':[-796,1380],'shape':[264,408],'no_missing_samples':True},'maps':['territory','flows','growth-1','growth-2','growth-3','growth-4'],'proposal_nodes':len(nodes),'proposal_routes':len(routes),'freshness':'Accepted snapshot, not live world verification','source_refs':['E-R1','E-ATLAS','E-CANON']})
print(json.dumps({'nodes':[(n['id'],n['geometry']['coordinates'],n['observed_at_sample']) for n in nodes],'routes':[(r['id'],r['sampled_length_blocks'],round(r['max_sample_grade'],2)) for r in routes]},ensure_ascii=False))
