"""外围证据汇编：候选语义由研究者明确给定，程序只计算缓存中的几何与统计。

不调用世界加载器；只读前序公开数据文件，不import前序内部模块。
矩形是比较窗口，必须和真实陆柱求交，不能冒充独立岛或建设边界。
"""
import sys,json,sqlite3,math
from pathlib import Path
from collections import Counter,deque
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.dont_write_bytecode=True
from 源快照保护器 import write_json,digest
out=Path(__file__).resolve().parents[1];project=out.parents[3];r1=project/'research/human-geography/southern-island/WB-002R-R1';wb=project/'research/human-geography/southern-island/WB-003R'
# 此处固定研究窗口以避免按设计偏好挑地；最终选址必须由Owner确认。
definitions=[{'id':'A','parent':2,'window':[-380,1664,240,2000],'label':'湾内东岛西伸低地','meaning':'C形低岛怀抱内视觉居中的西伸陆体','why_possible':'在低岛内湾正中显眼，远景容易称为中心岛。','why_not':'它连接东部山地主岛，不是独立岛，也不属于西部C形低岛陆连通分量。','mapping_confidence':'MEDIUM: visual match plausible; Owner identity unconfirmed'},
 {'id':'B','parent':1,'window':[-480,2000,128,2352],'label':'西部C形低岛内侧中部','meaning':'将中心岛理解为西部低岛本体及其内侧中央低地','why_possible':'确实属于西部平岛，面对内湾与A，保留西域空间语义。','why_not':'是C形岛本体的连续局部，不存在独立中心小岛；中心含义较弱。','mapping_confidence':'LOW: alternate literal-west reading, not equally strong'}]
cx0,cz0,cx1,cz1=-800,1376,1200,2655;shape=(cz1-cz0+1,cx1-cx0+1)
db=sqlite3.connect((r1/'raw-or-queryable/observed.sqlite').as_uri()+'?mode=ro',uri=True)
fields=['x','z','exposed_y','surface_y','water_y','water_bottom','exposed_state','artificial_material']
rows=np.asarray(db.execute('SELECT '+','.join(fields)+' FROM samples WHERE x BETWEEN ? AND ? AND z BETWEEN ? AND ? ORDER BY z,x',(cx0,cx1,cz0,cz1)).fetchall(),dtype=np.int32)
assert len(rows)==shape[0]*shape[1];a={k:rows[:,i].reshape(shape) for i,k in enumerate(fields)}
states={k:json.loads(v)['Name'] for k,v in db.execute('SELECT * FROM states')}
with np.load(r1/'raw-or-queryable/derived.npz') as f:
    m={k:f[k][:shape[0],:shape[1]] for k in ('land_component','water_component','slope8','relief32','step1','terrain_class','shoreline')}
def distribution(v):
    v=np.asarray(v);v=v[np.isfinite(v)];return dict(zip(('min','median','p90','max'),map(float,np.percentile(v,[0,50,90,100])))) if len(v) else None
def bounds(mask):
    z,x=np.where(mask);return [int(x.min()+cx0),int(z.min()+cz0),int(x.max()+cx0),int(z.max()+cz0)]
def rle(mask):
    runs=[]
    for z,row in enumerate(mask):
        changes=np.flatnonzero(np.diff(np.r_[False,row,False].astype(np.int8)))
        runs.extend([[z+cz0,int(x+cx0),int(y+cx0-1)] for x,y in zip(changes[::2],changes[1::2])])
    return runs
def largest_component(mask):
    seen=np.zeros(mask.shape,bool);best=[];width=mask.shape[1]
    for z,x in zip(*np.where(mask)):
        if seen[z,x]:continue
        q=deque([(int(z),int(x))]);seen[z,x]=True;part=[]
        while q:
            zz,xx=q.popleft();part.append((zz,xx))
            for nz,nx in ((zz-1,xx),(zz+1,xx),(zz,xx-1),(zz,xx+1)):
                if 0<=nz<mask.shape[0] and 0<=nx<width and mask[nz,nx] and not seen[nz,nx]:seen[nz,nx]=True;q.append((nz,nx))
        if len(part)>len(best):best=part
    result=np.zeros(mask.shape,bool)
    if best:z,x=np.array(best).T;result[z,x]=True
    return result
def square(mask):
    yy,xx=np.where(mask);z0,z1=yy.min(),yy.max();x0,x1=xx.min(),xx.max();crop=mask[z0:z1+1,x0:x1+1];prev=np.zeros(crop.shape[1]+1,np.int32);best=(0,0,0)
    for z,row in enumerate(crop):
        cur=np.zeros(len(prev),np.int32)
        for x,value in enumerate(row):
            if value:cur[x+1]=1+min(prev[x],prev[x+1],cur[x]);candidate=(int(cur[x+1]),z,x);best=max(best,candidate)
        prev=cur
    n,z,x=best;bb=[int(x+x0-n+1+cx0),int(z+z0-n+1+cz0),int(x+x0+cx0),int(z+z0+cz0)]
    return {'side_blocks':n,'bounds':bb,'interpretation':'largest axis-aligned all-FLAT square in comparison window; terrain diagnostic, not footprint or clear-space approval'}
records=[];masks={};witness=[]
for item in definitions:
    lo,top,hi,bottom=item['window'];mask=(m['land_component']==item['parent'])&(a['x']>=lo)&(a['x']<=hi)&(a['z']>=top)&(a['z']<=bottom);masks[item['id']]=mask
    flat=mask&(m['terrain_class']==1);patch=largest_component(flat);sq=square(flat);runs=rle(mask)
    write_json(out/f'geometry/{item["id"]}-land-runs.json',{'encoding':'inclusive [z,x0,x1] world-coordinate horizontal runs','parent_land_component':item['parent'],'comparison_window':item['window'],'runs':runs})
    write_json(out/f'geometry/{item["id"]}-flat-patch-runs.json',{'encoding':'inclusive [z,x0,x1]','runs':rle(patch)})
    surface=Counter(states[int(s)] for s in a['exposed_state'][mask]);flag=mask&(a['artificial_material']>0)
    special={name:n for name,n in surface.items() if ('waystone' in name or name.endswith(('dirt_path','stone_slab','cobblestone','planks')))}
    for name in sorted(set(special)|{n for n in surface if n in ('minecraft:lava','minecraft:fire','minecraft:pointed_dripstone')}):
        points=np.argwhere(mask&np.isin(a['exposed_state'],[i for i,v in states.items() if v==name]))
        for z,x in points[:6]:witness.append({'candidate':item['id'],'kind':'surface_name','block':name,'x':int(x+cx0),'z':int(z+cz0),'y':int(a['exposed_y'][z,x]),'source':'R1 observed.samples exposed_state'})
    veg=[]
    for x,z,leaf,trunk in db.execute('SELECT x,z,leaf,trunk FROM vegetation WHERE x BETWEEN ? AND ? AND z BETWEEN ? AND ?',(lo,hi,top,bottom)):
        if mask[z-cz0,x-cx0]:veg.append((leaf,trunk))
    vv=np.array(veg);shores={};waterids=Counter();contacts=[];outer=[]
    for direction,dz,dx in (('N',-1,0),('E',0,1),('S',1,0),('W',0,-1)):
        sh=mask&np.roll(a['water_y']!=-32768,(-dz,-dx),(0,1));points=np.argwhere(sh);steps=[];depth=[];good=0
        for z,x in points:
            nz,nx=z+dz,x+dx;steps.append(int(a['exposed_y'][z,x]-a['water_y'][nz,nx]));depth.append(int(a['water_y'][nz,nx]-a['water_bottom'][nz,nx]+1));waterids[int(m['water_component'][nz,nx])]+=1
            ys=[]
            for i in range(9):
                iz,ix=z-dz*i,x-dx*i
                if m['land_component'][iz,ix]!=item['parent']:break
                ys.append(int(a['exposed_y'][iz,ix]))
            if len(ys)==9 and max(abs(b-a) for a,b in zip(ys,ys[1:]))<=1:good+=1
        shores[direction]={'shore_edge_contacts':len(points),'land_minus_water_top':distribution(steps),'adjacent_water_depth':distribution(depth),'eight_step_inward_low_step_contacts':good}
        if len(points):
            z,x=points[len(points)//2];contacts.append({'direction':direction,'land':[int(x+cx0),int(z+cz0),int(a['exposed_y'][z,x])],'water':[int(x+dx+cx0),int(z+dz+cz0),int(a['water_y'][z+dz,x+dx])]})
        linked=mask&np.roll((m['land_component']==item['parent'])&~mask,(-dz,-dx),(0,1))
        if linked.any():
            z,x=np.argwhere(linked)[len(np.argwhere(linked))//2];outer.append({'direction':direction,'edge_count':int(linked.sum()),'inside':[int(x+cx0),int(z+cz0)],'outside':[int(x+dx+cx0),int(z+dz+cz0)]})
    yy,xx=np.where(mask);pick=np.argmin((xx-xx.mean())**2+(yy-yy.mean())**2);z,x=int(yy[pick]),int(xx[pick]);origin=[x+cx0,z+cz0,int(a['exposed_y'][z,x])+2];rays=[]
    # 地形天际线是观察而非建筑高度设计；8方位、4格采样不声称完整可视域。
    for label,dz,dx in (('N',-1,0),('NE',-1,1),('E',0,1),('SE',1,1),('S',1,0),('SW',1,-1),('W',0,-1),('NW',-1,-1)):
        samples=[]
        for d in range(4,1201,4):
            nz=round(z+dz*d/math.hypot(dz,dx));nx=round(x+dx*d/math.hypot(dz,dx))
            if not(0<=nz<shape[0] and 0<=nx<shape[1]):break
            height=max(int(a['exposed_y'][nz,nx]),int(a['water_y'][nz,nx]));samples.append((math.degrees(math.atan2(height-origin[2],d)),nx+cx0,nz+cz0,height,d))
        peak=max(samples);rays.append({'direction':label,'sampled_to_blocks':samples[-1][-1],'maximum_elevation_angle_degrees':peak[0],'horizon_sample_xzy':list(peak[1:4]),'horizon_distance':peak[4]})
    record=dict(item,actual_bounds=bounds(mask),geometry=f'geometry/{item["id"]}-land-runs.json',land_columns=int(mask.sum()),is_independent_island=False,parent_continuations=outer,terrain={'elevation':distribution(a['exposed_y'][mask]),'slope8':distribution(m['slope8'][mask]),'relief32':distribution(m['relief32'][mask]),'flat_columns':int(flat.sum()),'gentle_columns':int((mask&(m['terrain_class']==2)).sum()),'largest_connected_flat_patch':{'columns':int(patch.sum()),'bounds':bounds(patch),'geometry':f'geometry/{item["id"]}-flat-patch-runs.json'},'largest_all_flat_square':sq},shore_water={'directional_contacts':shores,'water_component_contacts':dict(waterids),'witnesses':contacts,'interpretation':'WATER_ACCESS_PROXY / LANDING_ACCESS_PROXY only; counts are shore edges not unique columns; depth from R1 contiguous surface water interval'},existing_surface={'surface_palette':dict(surface),'artificial_material_flag_columns':int(flag.sum()),'named_path_structure_signals':special,'vegetation_sample_columns':len(vv),'leaf_occupied_fraction':float(np.mean(vv[:,0]>0)),'trunk_occupied_fraction':float(np.mean(vv[:,1]>0)),'limitations':'sparse R1 4-block vegetation grid; flag/name is not structure attribution or underground protection survey'},views={'observer_xzy_eye':origin,'method':'8 rays, 4-block spacing, max1200 blocks or local context boundary; ground/water only, ignores canopy, weather and render distance','rays':rays},design_readiness='NOT_READY',readiness_reason='Owner referent unconfirmed; candidate context supports comparison only, no Plan/Section/Sequence design start')
    records.append(record)
    # RLE往返独立重建，并以SQLite条件聚合复核候选高程。
    rebuilt=np.zeros(mask.shape,bool)
    for zz,x0,x1 in runs:rebuilt[zz-cz0,x0-cx0:x1-cx0+1]=True
    assert np.array_equal(rebuilt,mask)
    assert all(m['land_component'][zz-cz0,x0-cx0:x1-cx0+1].min()==item['parent'] for zz,x0,x1 in runs)
    sb=sq['bounds'];roi=flat[sb[1]-cz0:sb[3]-cz0+1,sb[0]-cx0:sb[2]-cx0+1];assert roi.all() and roi.size==sq['side_blocks']**2
    print(item['id'],record['land_columns'],record['terrain'],flush=True)
components=json.loads((r1/'profile/land-components.json').read_text(encoding='utf-8'));near=[v for v in components if v['id']>2 and -480<=v['bounds'][0]<=280 and 1550<=v['bounds'][1]<=2050]
write_json(out/'site-candidates.json',{'schema':'site-candidates/1','verdict':'OWNER_SELECTION_REQUIRED','candidate_coordinates_are':'observed comparison areas; not selected site coordinates','candidates':records,'nearby_small_components':[{'id':v['id'],'area':v['area_blocks2'],'bounds':v['bounds']} for v in near],'candidate_selection':'human-authored two semantic readings, not program ranking; nearby tiny disconnected cells do not establish a council island'})
write_json(out/'review/surface-witnesses.json',{'witnesses':witness,'meaning':'surface signals to preserve/recheck; no demolition/clearance authorization'})
# 等比例比较图使用实际成员着色；非矩形整块填色，保留海水与连接陆体。
rgb=np.zeros((*shape,3),np.uint8);rgb[:]=(35,75,106);rgb[m['land_component']==1]=(112,150,107);rgb[m['land_component']==2]=(149,136,111);rgb[(m['land_component']>2)]=(200,190,150)
shade=np.clip((a['exposed_y']-62)/4,0,40).astype(np.uint8);land=m['land_component']>0;rgb[land]=np.maximum(rgb[land].astype(np.int16)-shade[land,None],0).astype(np.uint8)
for key,col in [('A',(239,185,65)),('B',(135,169,235))]:rgb[masks[key]]=col;rgb[masks[key]&(m['terrain_class']==1)]=np.minimum(np.array(col)+25,255)
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',20);small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',16)
canvas=Image.new('RGB',(1800,1470),'#f0eee7');draw=ImageDraw.Draw(canvas)
draw.text((26,12),'AB-001P1｜中心岛称呼待确认：两个空间解释，不是建筑方案',font=font,fill='#15222c')
overview=Image.fromarray(rgb).resize((1401,896));canvas.paste(overview,(20,60));draw=ImageDraw.Draw(canvas)
def mappt(x,z):return (20+(x-cx0)*.7,60+(z-cz0)*.7)
for r in records:
    lo,top,hi,bottom=r['window'];draw.rectangle((*mappt(lo,top),*mappt(hi,bottom)),outline='white',width=2);draw.text(mappt(lo,top-34),r['id']+' '+r['label'],font=small,fill='white')
draw.text((1440,80),'北 N ↑（-Z）\n东 E →（+X）\nX: -800..1200\nZ: 1376..2655\n总览：0.7像素/格\n观察窗白框非岛界\n\nA 金色：东岛西伸部\nB 蓝色：西岛内侧\n较浅色：R1 FLAT\n海水：蓝灰\n\n两者都不是\n独立的中心小岛。\n\nOwner未选择前\nNOT_READY\nworld writes = 0',font=small,fill='#17252e',spacing=10)
draw.line((1440,800,1580,800),fill='black',width=3);draw.text((1440,812),'200格比例尺',font=small,fill='black')
for i,r in enumerate(records):
    x0,z0,x1,z1=r['window'];crop=rgb[z0-cz0:z1-cz0+1,x0-cx0:x1-cx0+1];im=Image.fromarray(crop);canvas.paste(im,(25+i*875,1020));draw=ImageDraw.Draw(canvas)
    draw.text((25+i*875,980),r['id']+' 局部等比例（1像素/格）；框外陆连通未切断',font=small,fill='#17252e')
    draw.text((25+i*875,1390),f"陆柱 {r['land_columns']:,}；Y中位 {r['terrain']['elevation']['median']:g}；最大连续平缓方块诊断边长 {r['terrain']['largest_all_flat_square']['side_blocks']}格",font=small,fill='#17252e')
canvas.save(out/'visual/site-candidates.png')
db.close()
write_json(out/'validation/geometry-check.json',{'status':'PASS','candidate_geometry_rle_roundtrip':True,'parent_membership_exact':True,'flat_square_all_members_verified':True,'candidates_are_parent_subsets_not_islands':True,'new_world_block_reads':0,'cache_context_bounds':[cx0,cz0,cx1,cz1],'limitations':'no in-game rendering, tree collision, underground structures or complete viewshed; no unique Owner mapping'})
