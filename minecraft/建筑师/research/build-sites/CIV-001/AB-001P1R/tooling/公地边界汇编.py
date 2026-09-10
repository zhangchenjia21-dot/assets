"""研究外围脚本：实现已解释的东侧切口，不按目标面积反推、不拟合椭圆。

方块(x,z)占用[x,x+1)×[z,z+1)；列88/89之间的边界平面为X=89。
输入仅前序RLE、SQLite和NPZ；写入只限本轮研究目录，不加载世界。
"""
import sys,json,sqlite3
from pathlib import Path
from collections import deque,defaultdict
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.dont_write_bytecode=True
from 源快照保护器 import digest,write_json
out=Path(__file__).resolve().parents[1];p1=out.parent/'AB-001P1';project=out.parents[3];r1=project/'research/human-geography/southern-island/WB-002R-R1'
x0,z0,x1,z1=-380,1664,240,2000;shape=(z1-z0+1,x1-x0+1);cut=89
source=p1/'geometry/A-land-runs.json';g=json.loads(source.read_text(encoding='utf-8'));a=np.zeros(shape,bool)
for z,s,e in g['runs']:a[z-z0,s-x0:e-x0+1]=True
xx=np.arange(x0,x1+1)[None,:];commons=a&(xx<cut);connector=a&~commons
def compact(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
def runs(mask):
    result=[]
    for z,row in enumerate(mask):
        ends=np.flatnonzero(np.diff(np.r_[False,row,False].astype(np.int8)))
        result.extend([[z+z0,int(s+x0),int(e+x0-1)] for s,e in zip(ends[::2],ends[1::2])])
    return result
def bounds(mask):
    zz,xx=np.where(mask);return [int(xx.min()+x0),int(zz.min()+z0),int(xx.max()+x0),int(zz.max()+z0)]
def components(mask):
    seen=np.zeros(shape,bool);parts=[]
    for z,x in zip(*np.where(mask)):
        if seen[z,x]:continue
        seen[z,x]=True;q=deque([(int(z),int(x))]);part=[]
        while q:
            zz,xx=q.popleft();part.append((zz,xx))
            for nz,nx in ((zz-1,xx),(zz+1,xx),(zz,xx-1),(zz,xx+1)):
                if 0<=nz<shape[0] and 0<=nx<shape[1] and mask[nz,nx] and not seen[nz,nx]:seen[nz,nx]=True;q.append((nz,nx))
        parts.append(part)
    return sorted(parts,key=len,reverse=True)
def outline(mask):
    # 合并共线单位方块边；保留全部外岸与内水洞，不简化或平滑几何。
    lines=defaultdict(list)
    for z,x in zip(*np.where(mask)):
        for dz,dx,axis,line,pos in ((-1,0,'H',z+z0,x+x0),(1,0,'H',z+z0+1,x+x0),(0,-1,'V',x+x0,z+z0),(0,1,'V',x+x0+1,z+z0)):
            nz,nx=z+dz,x+dx
            if not(0<=nz<shape[0] and 0<=nx<shape[1]) or not mask[nz,nx]:lines[(axis,int(line))].append(int(pos))
    segments=[]
    for (axis,line),positions in sorted(lines.items()):
        positions=sorted(positions);start=last=positions[0]
        for pos in positions[1:]+[None]:
            if pos is not None and pos==last+1:last=pos;continue
            segments.append([start,line,last+1,line] if axis=='H' else [line,start,line,last+1])
            start=last=pos
    return segments
db=sqlite3.connect((r1/'raw-or-queryable/observed.sqlite').as_uri()+'?mode=ro',uri=True)
rows=np.array(db.execute('SELECT x,z,exposed_y FROM samples WHERE x BETWEEN ? AND ? AND z BETWEEN ? AND ? ORDER BY z,x',(x0,x1,z0,z1)).fetchall(),dtype=np.int32);heights=rows[:,2].reshape(shape)
with np.load(r1/'raw-or-queryable/derived.npz') as f:
    labels=f['land_component'];water=f['water_component'][z0-1376:z1-1376+1,x0+800:x1+801];relief=f['relief32'][z0-1376:z1-1376+1,x0+800:x1+801];slope=f['slope8'][z0-1376:z1-1376+1,x0+800:x1+801]
assert np.all(labels[z0-1376:z1-1376+1,x0+800:x1+801][a]==2)
sections=[]
for col in np.flatnonzero(a.any(axis=0)):
    zz=np.flatnonzero(a[:,col]);outer=int(zz[-1]-zz[0]+1);sections.append({'x':int(col+x0),'land_columns':len(zz),'north_z':int(zz[0]+z0),'south_z':int(zz[-1]+z0),'outer_span':outer,'internal_nonland_columns':outer-len(zz),'next_column_land_edges':int((a[:,col]&a[:,col+1]).sum()) if col+1<shape[1] else None,'median_y':float(np.median(heights[:,col][a[:,col]])),'median_relief32':float(np.median(relief[:,col][a[:,col]]))})
bands=[]
for start in range(-352,241,16):
    ss=[v for v in sections if start<=v['x']<start+16]
    if ss:bands.append({'x_inclusive':[start,start+15],'mean_land_width':float(np.mean([v['land_columns'] for v in ss])),'mean_outer_span':float(np.mean([v['outer_span'] for v in ss])),'median_north_z':float(np.median([v['north_z'] for v in ss])),'median_south_z':float(np.median([v['south_z'] for v in ss]))})
compact(out/'review/cross-sections.json',{'definition':'actual dry column count distinct from north-south outer span; units blocks','sections':sections,'bands16':bands})
summary={};parts={}
for name,mask in [('commons',commons),('connector',connector)]:
    parts[name]=components(mask);rr=runs(mask);geom={'schema':'block-land-rle/1','coordinate_convention':'block [x,x+1) x [z,z+1); runs [z,x_start,x_end] inclusive','area_blocks2':int(mask.sum()),'bounds':bounds(mask),'runs':rr,'outline_segments':outline(mask),'outline_convention':'exact block edges [x0,z0,x1,z1]; unordered merged segments including internal holes, not a smoothed polygon'};compact(out/f'{name}-geometry.json',geom)
    decoded=np.zeros(shape,bool)
    for z,s,e in rr:decoded[z-z0,s-x0:e-x0+1]=True
    assert np.array_equal(decoded,mask)
    valid_slope=slope[mask&np.isfinite(slope)]
    summary[name]={'area_blocks2':int(mask.sum()),'bounds':bounds(mask),'connected_components':[len(p) for p in parts[name]],'elevation_min_median_max':list(map(float,np.percentile(heights[mask],[0,50,100]))),'relief32_median_p90':list(map(float,np.percentile(relief[mask],[50,90]))),'slope8_median_p90':list(map(float,np.percentile(valid_slope,[50,90]))),'unknown_slope_columns':int((mask&~np.isfinite(slope)).sum()),'geometry':f'{name}-geometry.json'}
assert len(parts['commons'])==len(parts['connector'])==1
assert not (commons&connector).any() and np.array_equal(commons|connector,a)
contacts=[]
for z,x in parts['connector'][0]:
    for dz,dx in ((-1,0),(0,1),(1,0),(0,-1)):
        nz,nx=z+dz,x+dx
        if not(0<=nz<shape[0] and 0<=nx<shape[1]) and labels[nz+z0-1376,nx+x0+800]==2:contacts.append([[x+x0,z+z0],[nx+x0,nz+z0]])
assert any(p[1][0]==241 for p in contacts)
# 边界是相邻列之间的政治接口；不删除任何方块列。
edge_z=np.flatnonzero(a[:,cut-1-x0]&a[:,cut-x0]);interface=[[cut,int(z+z0),cut,int(z+z0+1)] for z in edge_z]
checks=[]
for k in (87,88,89,90,110):
    left=a&(xx<k);right=a&~left;checks.append({'plane_x':k,'commons_area':int(left.sum()),'connector_area':int(right.sum()),'commons_component_sizes':[len(p) for p in components(left)],'connector_component_sizes':[len(p) for p in components(right)]})
write_json(out/'commons-boundary.json',{'status':'PREFERRED_BOUNDARY_FIT / AWAITING INDEPENDENT REVIEW','owner_rule':'All A except east connector; no inner ellipse or area target','source_A':{'path':'../AB-001P1/geometry/A-land-runs.json','sha256':digest(source),'area_blocks2':int(a.sum())},'selected_cut':{'plane_x':cut,'column_partition':'Commons x<=88; connector x>=89; intersect both with A actual geometry','shore_to_shore_z_interval':[int(edge_z.min()+z0),int(edge_z.max()+z0+1)],'land_interface_edges':len(edge_z),'interface_unit_segments':interface},'method':'Human-selected shoreline neck: outer-span minimum at column88 after marked narrowing; full X cross-sections and connectedness checked; not ellipse fitting or program political scoring','commons':summary['commons'],'connector':summary['connector'],'parent_east_continuation':{'parent_component':2,'contacts_count':len(contacts),'witnesses':contacts[::max(1,len(contacts)//8)][:9]},'uncertainty':{'pixel_scale':'Plane88 and89 both have48 adjacent land edges; choose89 to keep the complete narrowest coast-to-coast column in Commons. +/-1 block sensitivity retained.','downstream_diagnostic':'Columns109/110 have39 dry cells but50-block outer span; internal nonland lowers dry count, not a second equally narrow external shoreline neck. Plane110 shown as diagnostic, not alternate selected boundary.','scope':'Only original A actual land partitioned; mainland beyond A, internal water rights, construction and future capacity not assigned.'},'sensitivity':checks,'world_writes':0,'new_world_block_reads':0,'broad_rescan':False})
write_json(out/'validation/geometry.json',{'status':'PASS','source_A_area':int(a.sum()),'union_equals_A':True,'intersection_empty':True,'omitted_A_land':0,'duplicate_A_land':0,'rle_roundtrip':True,'commons_components':len(parts['commons']),'connector_components':len(parts['connector']),'connector_parent_contacts':len(contacts),'parent_component':2,'new_world_block_reads':0})
# 等比例候选A与连接陆体上下文，颜色只分真实成员，不画椭圆或建筑。
context=labels[z0-1376:z1-1376+1,x0+800:401+800];rgb=np.zeros((*context.shape,3),np.uint8);rgb[:]=(35,76,109);rgb[context==1]=(99,134,96);rgb[context==2]=(153,143,125);rgb[context>2]=(176,177,151)
rgb[:,:shape[1]][commons]=(206,177,95);rgb[:,:shape[1]][connector]=(176,137,194)
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',22);small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',17)
canvas=Image.new('RGB',(1620,1220),'#f1eee5');canvas.paste(Image.fromarray(rgb).resize((1562,674),Image.Resampling.NEAREST),(28,96));draw=ImageDraw.Draw(canvas)
draw.text((28,15),'AB-001P1R｜联盟公地 = 全部 A 主体 − 东侧连接带',font=font,fill='#152431')
draw.text((28,51),'金色：联盟公地　紫色：A 内连接带　灰褐：A 外东岛续接　北↑ / 东→　2像素/格',font=small,fill='#152431')
px=28+(cut-x0)*2;za,zb=int(edge_z.min()+z0),int(edge_z.max()+z0+1)
draw.line((px,96+(za-z0)*2,px,96+(zb-z0)*2),fill='#d52326',width=5);draw.text((px-60,96+(za-z0)*2-34),'切口 X=89',font=font,fill='#b3191e')
draw.line((28+(241-x0)*2,96,28+(241-x0)*2,770),fill='white',width=2);draw.text((28+(241-x0)*2+8,110),'A原观察窗东界\n不是主岛终点',font=small,fill='white')
draw.text((28,790),f"公地 {summary['commons']['area_blocks2']:,} 格²  +  连接带 {summary['connector']['area_blocks2']:,} 格²  =  A {int(a.sum()):,} 格²；无遗漏，无内缩椭圆",font=font,fill='#152431')
draw.text((28,830),'下图：X逐列截面；蓝=外岸跨度，橙=实际干陆宽度。右侧水洞造成干陆数低谷。',font=small,fill='#152431')
left,top,width,height=60,900,1250,230
for widthvalue in (0,50,100,200,300):
    py=top+height-widthvalue/320*height;draw.line((left,py,left+width,py),fill='#c7c5bd');draw.text((12,py-10),str(widthvalue),font=small,fill='black')
for key,color in [('outer_span','#236795'),('land_columns','#dc7624')]:
    draw.line([(left+(r['x']+349)/589*width,top+height-r[key]/320*height) for r in sections],fill=color,width=2)
for x in (-349,-100,0,88,110,240):
    px=left+(x+349)/589*width;draw.line((px,top,px,top+height),fill='#b9b6ab',width=1);draw.text((px-14,1140),str(x),font=small,fill='black')
draw.text((1330,922),'X=88 外岸48格\nX=109 干陆39格\n但外岸仍50格\n\nworld writes = 0\n不包含建筑方案',font=small,fill='#152431',spacing=10)
canvas.save(out/'visual/commons-connector-boundary.png');db.close();print(json.dumps(summary,ensure_ascii=False),flush=True)
