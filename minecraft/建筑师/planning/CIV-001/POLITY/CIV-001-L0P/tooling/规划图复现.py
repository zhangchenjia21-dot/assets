"""仅从冻结R1缓存与revision154绘制L0阅读图；不解析或写入Minecraft世界。

规划关系由已保存JSON提供；此脚本不选择城址、不自动评判因果或授予通行权。
输出必须为独立目录，避免复现时覆盖Primary Freeze。
"""
from pathlib import Path
import argparse, hashlib, json, sqlite3, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

PLAN=Path(__file__).resolve().parents[1]
PROJECT=PLAN.parents[3]
RESEARCH=PROJECT/'research/human-geography/southern-island'
X0,Z0,X1,Z1=-800,1376,2463,3487
COLORS=[(146,99,187),(181,166,71),(210,111,60),(72,139,126)]
NAMES=['联盟公地','西域','中域','东域']
def read(path): return json.loads(path.read_text('utf-8-sig'))
def digest(path):
    with path.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
def derive(raw):
    expected={'observed.sqlite':'01d115d6c686cc6d59772cfc68e1cbd50a5816045eeaa7f48fa8a4a8d4a791b7','derived.npz':'575861ecd5b791ffd0e0c32614c5dc63de7563de477ee963994103f44024beff'}
    for name,h in expected.items():
        if digest(raw/name)!=h: raise ValueError('CACHE_HASH_MISMATCH '+name)
    terrpath=RESEARCH/'territory-refinement/TT-002R/refined-draft.json'
    plan=read(PLAN/'L0-POLITY-PLAN.json')
    if digest(terrpath)!=plan['territory_ref']['sha256']: raise ValueError('TERRITORY_HASH_MISMATCH')
    t=read(terrpath); assert t['revision']==154 and t['schema']=='civ-territories/1'
    a=np.load(raw/'derived.npz'); m=np.full(a['whole_group'].shape,-1,np.int8)
    for z,x0,x1,k in t['runs']:
        assert np.all(m[z-Z0,x0-X0:x1-X0+1]==-1)
        m[z-Z0,x0-X0:x1-X0+1]=k
    assert np.array_equal(m>=0,a['whole_group'])
    assert [int(np.sum(m==i)) for i in range(6)]==[92124,575397,391002,1198158,0,0]
    y=np.full(m.shape,-32768,np.int16); st=np.zeros(m.shape,np.int16)
    db=sqlite3.connect((raw/'observed.sqlite').as_uri()+'?mode=ro',uri=True)
    states={i:json.loads(v) for i,v in db.execute('select * from states')}
    # 按行读取已存在快照，限内存；不调用历史扫描器，也不访问世界文件。
    for z, in db.execute('select distinct z from samples'):
        rows=np.array(db.execute('select x,exposed_y,exposed_state from samples where z=? order by x',(z,)).fetchall())
        y[z-Z0,rows[:,0]-X0]=rows[:,1]; st[z-Z0,rows[:,0]-X0]=rows[:,2]
    db.close()
    summary=[]
    for k,cat in enumerate(t['categories'][:4]):
        mask=m==k; yy,xx=np.where(mask); ids,counts=np.unique(st[mask],return_counts=True)
        summary.append(dict(category=cat,area=int(mask.sum()),bounds=[int(xx.min()+X0),int(yy.min()+Z0),int(xx.max()+X0),int(yy.max()+Z0)],height_percentiles=np.percentile(y[mask],[10,50,90]).tolist(),height_max=int(y[mask].max()),terrain_counts={str(int(i)):int(n) for i,n in zip(*np.unique(a['terrain_class'][mask],return_counts=True))},surface_top=sorted([(states[int(i)],int(n)) for i,n in zip(ids,counts)],key=lambda v:-v[1])[:6]))
    expected_summary=read(PLAN/'evidence/territory-terrain-summary.json')['categories']
    assert json.loads(json.dumps(summary))==expected_summary
    return m,y,a['terrain_class'],a['shoreline']

def render(m,y,terrain,shore,out,font):
    ft=lambda s:ImageFont.truetype(str(font),s)
    fonts={s:ft(s) for s in [17,20,22,25,29,40]}
    ox,oz=60,140
    def pos(x,z): return (ox+(x-X0)/2,oz+(z-Z0)/2)
    land=m>=0
    # 二倍缩略仅是阅读视图；所有统计和法定成员在原始一格数组上进行。
    v=np.clip((y.astype(float)-62)/238,0,1)
    rgb=np.zeros((*m.shape,3),dtype=np.uint8); rgb[:]=(193,220,230)
    low=np.array([225,222,177]); high=np.array([135,113,101])
    rgb[land]=(low+(high-low)*v[land,None]).astype(np.uint8)
    for k,c in enumerate(COLORS): rgb[m==k]=(rgb[m==k]*.7+np.array(c)*.3).astype(np.uint8)
    edges=np.zeros(m.shape,bool)
    edges[1:] |= (m[1:]!=m[:-1])&(m[1:]>=0)
    edges[:,1:] |= (m[:,1:]!=m[:,:-1])&(m[:,1:]>=0)
    rgb[edges]=(42,49,50)
    base=Image.fromarray(rgb).resize((1632,1056),Image.Resampling.LANCZOS)
    crosses=read(RESEARCH/'WB-003R/profile/crossing-profile.json')['candidates']
    corridors=read(RESEARCH/'WB-003R/profile/movement-corridors.json')['candidates']
    meta=dict(schema='l0-map-transform/1',world_bounds_inclusive=[X0,Z0,X1,Z1],world_cell_boundary_extent=[X0,Z0,X1+1,Z1+1],image_size=[2400,1320],map_origin_px=[ox,oz],pixels_per_block=.5,north='negative Z / top',accepted_geometry='revision154 exact members before downsample; no new political polygons',display_only_labels='Role label rectangles and arrow endpoints are page-layout annotations, NOT settlement sites or route geometry',source_refs=['evidence/source-register.json','evidence/territory-terrain-summary.json'],maps=[])
    titles=['领土与地形｜接受边界上的真实差异','联盟空间角色｜共同政治地与地方网络','主要流与缓冲｜需求关系，不是路线图','聚落层级与搜索｜角色确定，城址未定','通达搜索骨架｜几何见证与许可分开']
    names=['01-territory-terrain-context.png','02-polity-regional-roles.png','03-major-flows.png','04-settlement-hierarchy-search-logic.png','05-movement-access-skeleton.png']
    panels=[
      ['事实层：revision154 + R1快照','公地 92,124｜中位 Y69','西域 575,397｜中位 Y66','中域 391,002｜中位 Y122','东域 1,198,158｜中位 Y177','色调随高度加深，非宜居评分。','平地+缓坡：西83.1%、中20.2%、东6.6%。','低坡不是可建面积，也不证明肥力。','西草土与砂面；中草土/石/砂砾并存；东亦有草土。','两主岛表层不连通；公地与东部陆体连续。','X=89为公地—中域政治接口，不需筑墙或切断陆地。','原生biome 4格；图未将其当民族/农业分类。'],
      ['Canon：三席、地方自治、互补','西域：生产开敞 + 节点市场','中域：高周转 + 居民混合服务','东域：广域分散 + 近源专业节点','公地：共同政治中心，非第四域','提出的因果：','有限可达地竞争 → 中域紧凑。','生产地价值/地权 → 西域开敞。','山地/近源/自治 → 东域分散。','共同事务 → 公地多向访问。','政治权重 ≠ 人口或建筑最大。','本图不确定首城、村镇数量或建筑。'],
      ['虚线箭头 = 提出的需求方向','F-FOOD：西→中/东/公地','季节补入、日常消耗；多处缓冲。','F-METAL：东→中/西及近用','矿产为Canon；矿点/运量未知。','F-PEOPLE：多向生活/交换','F-AUTH：三域↔共同政治地','事件高峰不等于永久建满公地。','F-FUEL：各域近用+有条件交换','不证明西域木材或东域煤的垄断。','F-DEF：事件联络，不设敌国方向。','线端为域级说明位置；不是城址。'],
      ['色块内斜纹 = 区域搜索责任','不是城镇范围、已建区域或用地分区。','H-C 政治级：CAP-C 6k–16k','H-W 市场服务：CAP-W 9k–24k','H-M 转换服务：CAP-M 10k–26k','H-E 山地节点：CAP-E 3k–10k','H-L 地方支持：CAP-L 0.8k–4k','单位blocks²；每个角色工作量级。','LOW置信度；可合并、不重复累加。','搜索 ≠ 建成 ≠ 服务腹地。','H-X战略协调可叠合，不另造一镇。','节点数/城址/全域总量待L1。'],
      ['青线：WB地形代价实验轨迹','不代表现成道路；C-02/03敏感。','方框：已测跨水岸对（非渡址）','X-00/01到公地，X-03到中域。','X-02被精确相交检查拒绝。','R-WC：西—公地政治/交换','R-WM：南部直接货运比较分支','R-CM：公地—中域陆侧关系','R-ME：坡麓—山地多接近搜索','R-EE：东域全域内部服务联络','净空/模式/权利/安全/季节未证。','先普通适应，再判约束；不设计桥路。']]
    label_positions=[(-560,2130),(-240,1810),(370,1560),(1330,2590)]
    for i,(title,name) in enumerate(zip(titles,names)):
        img=Image.new('RGB',(2400,1320),(246,245,238)); d=ImageDraw.Draw(img)
        d.text((60,30),f'CIV-001 · L0 / {title}',font=fonts[40],fill=(34,47,53))
        d.text((60,91),'CIV-001-L0P-r1   |   POLITY_TERRITORY   |   HANDOFF_READY · 待 GPT + Owner 审核   |   world writes = 0',font=fonts[22],fill=(65,70,70))
        img.paste(base,(ox,oz))
        def text(x,z,txt):
            px,pz=pos(x,z); box=d.textbbox((px,pz),txt,font=fonts[22]); d.rectangle((box[0]-5,box[1]-3,box[2]+5,box[3]+3),fill=(250,249,242));d.text((px,pz),txt,font=fonts[22],fill=(28,37,40))
        def dashed(points,color,width=4,arrow=False):
            pp=[pos(*p) for p in points]
            for a,b in zip(pp,pp[1:]):
                dx,dy=b[0]-a[0],b[1]-a[1]; length=math.hypot(dx,dy)
                if not length: continue
                for s in np.arange(0,length,18):
                    end=min(s+10,length);d.line((a[0]+dx*s/length,a[1]+dy*s/length,a[0]+dx*end/length,a[1]+dy*end/length),fill=color,width=width)
            if arrow:
                a,b=pp[-2:];ang=math.atan2(b[1]-a[1],b[0]-a[0]);d.polygon([b,(b[0]-18*math.cos(ang-.5),b[1]-18*math.sin(ang-.5)),(b[0]-18*math.cos(ang+.5),b[1]-18*math.sin(ang+.5))],fill=color)
        if i==3:
            # 全域一致斜纹只标记搜索责任，不产生子域边界/城镇掩膜。
            zgrid,xgrid=np.indices(m.shape)
            stripes=land & (((xgrid+zgrid)%64)<3)
            hatch=Image.new('RGBA',(3264,2112));ha=np.zeros((2112,3264,4),np.uint8);ha[stripes]=[45,47,55,60]
            img.paste(Image.fromarray(ha).resize((1632,1056),Image.Resampling.LANCZOS),(ox,oz),Image.fromarray(ha).resize((1632,1056),Image.Resampling.LANCZOS))
        if i==2:
            dashed([(-410,2160),(400,2020),(1110,2350)],(166,103,28),5,True)
            dashed([(1250,2530),(470,2110),(-330,2250)],(99,68,122),5,True)
            dashed([(-430,1840),(-110,1840)],(151,65,118),4,True)
            dashed([(860,1950),(120,1810),(-110,1840)],(151,65,118),4,True)
            text(240,1980,'食物 / 普通品 →');text(520,2380,'← 材料 / 成品')
        if i==4:
            for c in corridors:
                path=c['path'];d.line([pos(p[0],p[1]) for p in path],fill=(40,113,155),width=3)
            for c in corridors:
                path=c['path']
                text(path[-1][0]+30,path[-1][1],c['id']+' probe')
            for c in crosses:
                if not c['exact_closed_cell_water_only']:continue
                ends=[(c[e]['x'],c[e]['z']) for e in ['west','east']]
                d.line([pos(*p) for p in ends],fill=(130,51,106),width=4)
                for p in ends:
                    x,z=pos(*p);d.rectangle((x-4,z-4,x+4,z+4),outline=(130,51,106),width=2)
                text(ends[0][0]-120,ends[0][1]-45,c['id'])
            dashed([(1050,2160),(1540,2490),(1370,2850)],(66,94,87),3,True)
            text(1470,2750,'R-EE 全域搜索责任')
        labels=[('西域',-620,2030),('联盟公地',-320,1860),('中域',400,1510),('东域',1400,2940)]
        if i in [1,3]: labels=[('H-W 市场/生产服务',-680,2150),('H-C 共同政治',-325,1830),('H-M 转换服务',320,1560),('H-E 山地共同体网络',1220,2880)]
        for txt,x,z in labels:text(x,z,txt)
        # 使用完整块边界范围的同一仿射变换；地图间比例始终一致。
        for x in range(-600,2401,400):
            px,_=pos(x,Z0);d.line((px,oz-7,px,oz),fill='black',width=1);d.text((px-24,oz-29),str(x),font=fonts[17],fill=(60,70,75))
        for z in range(1600,3401,400):
            _,pz=pos(X0,z);d.text((4,pz-9),str(z),font=fonts[17],fill=(60,70,75))
        d.rectangle((ox,oz,ox+1632,oz+1056),outline=(45,58,62),width=2)
        d.text((1570,160),'N / −Z ↑',font=fonts[22],fill=(30,40,45))
        d.line((90,1230,290,1230),fill=(35,45,50),width=5);d.text((90,1240),'400 blocks（横纵等比例）',font=fonts[20],fill=(40,50,60))
        d.text((470,1222),'实线边：accepted territory 154   |   水蓝：快照水域/非干陆背景',font=fonts[20],fill=(40,50,60))
        d.text((470,1252),'R1 cached epoch + WB-003R；未刷新当前存档。缩略图不供逐格施工。',font=fonts[20],fill=(40,50,60))
        panel_x=1740;py=154
        for k in range(4):
            d.rectangle((panel_x+(k%2)*300,py+(k//2)*40,panel_x+(k%2)*300+24,py+(k//2)*40+24),fill=COLORS[k])
            d.text((panel_x+(k%2)*300+35,py+(k//2)*40),NAMES[k],font=fonts[22],fill=(35,45,50))
        py=260
        for j,line in enumerate(panels[i]):
            # 按真实字体像素断行，不依赖中英文字符等宽假设。
            cur='';lines=[]
            for ch in line:
                if d.textlength(cur+ch,font=fonts[25])>600:lines.append(cur);cur=ch
                else:cur+=ch
            lines.append(cur)
            for s in lines:d.text((panel_x,py),s,font=fonts[25],fill=(39,55,62));py+=36
            py+=16
        d.text((1740,1210),'图层权威：事实 / Canon / 提案分开',font=fonts[22],fill=(110,65,48))
        d.text((1740,1247),'无城址圆点 · 无街区/建筑设计',font=fonts[22],fill=(110,65,48))
        (out/'visual').mkdir(parents=True,exist_ok=True);img.save(out/'visual'/name,optimize=True)
        meta['maps'].append(dict(file='visual/'+name,title=title,semantic='same-scale explanatory map; exact members from accepted RLE; annotations are proposals or labeled research witnesses'))
    (out/'visual/map-metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

def main():
    p=argparse.ArgumentParser();p.add_argument('--raw-cache',required=True,type=Path);p.add_argument('--output',required=True,type=Path);p.add_argument('--font',default='C:/Windows/Fonts/msyh.ttc',type=Path);a=p.parse_args()
    if a.output.resolve()==PLAN.resolve(): raise ValueError('Refuse to overwrite frozen primary directory; render to separate output and compare')
    a.output.mkdir(parents=True,exist_ok=True)
    arrays=derive(a.raw_cache);render(*arrays,a.output,a.font)
    print('Exact territory, source hashes and per-domain summary verified; five maps rendered. world writes = 0')
if __name__=='__main__':main()
