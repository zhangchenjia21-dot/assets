"""离线派生图以1格事实层为来源；缩略图不得假装单像素精确。"""
import json
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from L0_公理层.区域契约 import BOUNDS
from L1_器件层.区域指标计算器 import load_observed

def render(out):
    a,biomes,states=load_observed(out/'raw-or-queryable/observed.sqlite');m=np.load(out/'raw-or-queryable/derived.npz');main=m['main_island'];wet=a['water_y']!=-32768
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13)
    palette=[(122,171,88),(207,173,89),(145,118,169),(225,204,159),(176,94,66),(120,176,185),(225,149,145),(165,150,80),(154,168,178)]
    def categorical(values):
        rgb=np.full((*values.shape,3),(31,47,63),np.uint8)
        for id in np.unique(values):
            if id:rgb[values==id]=palette[(int(id)-1)%len(palette)]
        return rgb
    def save(rgb,title,name,lines):
        im=Image.new('RGB',(1280,1010),(23,28,34));d=ImageDraw.Draw(im)
        d.text((25,12),title+' | RESEARCH ONLY',font=font,fill='white')
        d.text((25,38),f'X [{BOUNDS[0]},{BOUNDS[2]}], Z [{BOUNDS[1]},{BOUNDS[3]}]; North -Z up / East +X right',font=font,fill='white')
        d.text((25,62),'Source: current 1-block columns; derived views, no civilization/build authorization',font=small,fill='white')
        im.paste(Image.fromarray(rgb).resize((851,896),Image.Resampling.NEAREST),(25,90))
        for i,line in enumerate(lines):d.text((895,100+i*24),line,font=small,fill='white')
        im.save(out/'visual'/name)
    rgb=np.full((*main.shape,3),(37,77,110),np.uint8);lines=[]
    for i,b in enumerate(sorted(np.unique(a['filtered_biome']).tolist())):
        rgb[a['filtered_biome']==b]=palette[i%len(palette)]
        lines.append(f'{b}: {biomes[b]}')
    # 图例色块与native biome ID直接关联，水面仍显示其真实biome。
    save(rgb,'Filtered-surface biome (native 4x4x4 sampling)','biome-map.png',lines+['Not an ecological species/climate map.'])
    p=out/'visual/biome-map.png';im=Image.open(p);d=ImageDraw.Draw(im)
    for i,b in enumerate(sorted(np.unique(a['filtered_biome']).tolist())):d.rectangle((878,102+i*24,890,114+i*24),fill=palette[i%len(palette)])
    im.save(p)
    h=a['exposed_y'];land=~wet;v=np.clip((h-60)/100,0,1);rgb=np.stack((70+175*v,165-105*v,100-55*v),axis=2).astype(np.uint8);rgb[wet]=(37,77,110)
    save(rgb,'Filtered elevation; water blue','elevation-map.png',['Land colour: green Y60 -> brown Y160','Values above Y160 saturate.','NGEO-009 main island max Y79','Surrounding eastern land is separate.','Cave openings remain actual surface.'])
    v=np.clip(m['relief32']/16,0,1);rgb=np.stack((75+180*v,180-145*v,135-105*v),axis=2).astype(np.uint8);rgb[wet]=(37,77,110)
    save(rgb,'Land relief32 (33 x 33 window)','relief-slope-map.png',['Green: relief 0; red: relief >=16','Water excluded from window extrema.','slope8 and step1 are queryable.','At coast/ROI windows are censored.'])
    v=np.nan_to_num(np.clip(m['slope8'],0,1),nan=0);rgb=np.stack((70+185*v,180-150*v,110-80*v),axis=2).astype(np.uint8);rgb[wet]=(37,77,110);rgb[~wet&~np.isfinite(m['slope8'])]=(100,100,100)
    save(rgb,'Central8 slope (rise/run)','slope-map.png',['Green: 0; red: >=1.0 rise/run','Grey: missing land endpoints / ROI edge','Raw step1 separately queryable','No traversability inference'])
    rgb=np.full((*main.shape,3),(100,99,89),np.uint8);rgb[wet]=(37,77,110);rgb[m['terrain_class']==1]=(92,188,99);rgb[m['terrain_class']==2]=(215,185,90)
    save(rgb,'Operational flat / gentle masks','low-relief-map.png',['Green: LOW_RELIEF_FLAT','Yellow: GENTLE_SLOPE (excludes flat)','Grey: other / metric edge unknown','Not settlement suitability.','All component members are indexed.'])
    rgb=categorical(m['land_component']);rgb[wet]=(37,77,110)
    # 内部水分量和外侧水域不同着色；连通性另由真实水区间判断。
    edge_ids=np.unique(np.r_[m['water_component'][0],m['water_component'][-1],m['water_component'][:,0],m['water_component'][:,-1]])
    rgb[wet&~np.isin(m['water_component'],edge_ids)]=(83,185,205)
    save(rgb,'Current 4-neighbor land / water topology','water-land-topology.png',['Blue: ROI-edge water component','Cyan: water component not on ROI edge','Land colours = component identities','Not all non-edge water is an island pond.','Main island at (-248,2056)','Surface connection only; no navigation.'])
    im=Image.open(out/'visual/water-land-topology.png');d=ImageDraw.Draw(im)
    for id in np.unique(m['land_component']):
        zz,xx=np.where(m['land_component']==id)
        if id and len(xx)>500:
            n=len(xx)//2;d.text((25+xx[n]*.7,90+zz[n]*.7),f'L{id}',font=font,fill='white')
    im.save(out/'visual/water-land-topology.png')
    im=Image.new('RGB',(1280,1430),(23,28,34));d=ImageDraw.Draw(im)
    d.text((20,10),'Numerical zoning alternatives k=2..5; not semantic decisions; north up / east right',font=font,fill='white')
    d.text((20,35),f'Each panel: X {BOUNDS[0]}..{BOUNDS[2]}, Z {BOUNDS[1]}..{BOUNDS[3]}; 16-block attributes, main-island mask',font=small,fill='white')
    for k in range(2,6):
        x=20+((k-2)%2)*635;z=65+((k-2)//2)*680;d.text((x,z),f'k={k} (colours ordered by mean elevation)',font=font,fill='white');im.paste(Image.fromarray(categorical(m['k'+str(k)])).resize((608,640),Image.Resampling.NEAREST),(x,z+25))
    im.save(out/'visual/zoning-alternatives-2-to-5.png')
    if (out/'profile/zoning-decision.json').exists():
        dec=json.loads((out/'profile/zoning-decision.json').read_text(encoding='utf-8'));key=dec['membership_source'];rgb=categorical(m[key]);save(rgb,'Natural zone candidates | SIRZ research IDs','natural-zones-candidate.png',[f'SIRZ-{i:03d}: '+label for i,label in enumerate(dec['labels'],1)]+['1-block island outline','No discrete internal boundaries established','No political or tribal boundaries'])
    terrain=json.loads((out/'profile/terrain-profile.json').read_text(encoding='utf-8'));im=Image.new('RGB',(1050,480),(23,28,34));d=ImageDraw.Draw(im)
    d.text((20,12),'Main island longitude elevation profile: p10 / median / p90',font=font,fill='white')
    bands=terrain['longitude_bands']
    for i,b in enumerate(bands):
        x=70+i*105;e=b['elevation'];y=lambda h:400-(h-55)*10
        d.line((x,y(e['p10']),x,y(e['p90'])),fill=(130,170,230),width=3);d.ellipse((x-4,y(e['median'])-4,x+4,y(e['median'])+4),fill='yellow');d.text((x-35,425),str(b['x_bounds'][0]),font=small,fill='white')
    for h in (55,60,65,70,75,80):d.text((10,400-(h-55)*10),str(h),font=small,fill='white')
    d.text((20,455),f'Pearson r={terrain["pearson_x_elevation"]:.4f}; OLS +{terrain["OLS_Y_per_100_X"]:.3f} Y per 100 X; block columns not independent observations',font=small,fill='white');im.save(out/'visual/longitude-profile.png')
