"""离线地图保持 X/Z 等比例，颜色仅表达公开数值，不定义自然区。"""
import json,colorsys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from L1_器件层 import 区域指标计算器 as metrics

def render(out):
    bounds=json.loads((out/'profile/scope-completion.json').read_text(encoding='utf-8'))['bounds'];metrics.BOUNDS=tuple(bounds)
    a,biomes,_=metrics.load_observed(out/'raw-or-queryable/observed.sqlite');m=np.load(out/'raw-or-queryable/derived.npz');wet=a['water_y']!=-32768
    palette=[(122,171,88),(207,173,89),(145,118,169),(225,204,159),(176,94,66),(120,176,185),(225,149,145),(165,150,80),(154,168,178),(190,220,225),(140,80,90),(100,140,170)]
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    def cat(values):
        rgb=np.full((*wet.shape,3),(37,77,110),np.uint8)
        for id in np.unique(values):
            if id:rgb[values==id]=palette[(int(id)-1)%len(palette)]
        return rgb
    def save(rgb,title,name,lines):
        scale=min(1400/rgb.shape[1],1000/rgb.shape[0]);size=(round(rgb.shape[1]*scale),round(rgb.shape[0]*scale))
        im=Image.new('RGB',(size[0]+450,size[1]+100),(23,28,34));d=ImageDraw.Draw(im)
        d.text((16,12),title+' | RESEARCH / NOT WORLD CANON',font=font,fill='white')
        d.text((16,38),f'X {bounds[0]}..{bounds[2]} / Z {bounds[1]}..{bounds[3]} | North -Z up / East +X right',font=font,fill='white')
        im.paste(Image.fromarray(rgb).resize(size,Image.Resampling.NEAREST),(16,80))
        for i,line in enumerate(lines):d.text((size[0]+30,80+i*25),line,font=font,fill='white')
        im.save(out/'visual'/name)
    biome_colors={i:tuple(round(v*255) for v in colorsys.hsv_to_rgb(j/max(len(biomes),1),0.45+0.25*(j%2),0.75+0.2*(j%3==0))) for j,i in enumerate(sorted(biomes))}
    rgb=np.zeros((*wet.shape,3),np.uint8)
    for i,color in biome_colors.items():rgb[a['filtered_biome']==i]=color
    lines=[f'{i+1}: {name}' for i,name in sorted(biomes.items())]
    save(rgb,'Filtered-surface biome','full-biome-map.png',lines)
    p=out/'visual/full-biome-map.png';im=Image.open(p);d=ImageDraw.Draw(im)
    for j,(i,name) in enumerate(sorted(biomes.items())):d.rectangle((im.width-20,82+j*25,im.width-5,96+j*25),fill=biome_colors[i])
    im.save(p)
    v=np.clip((a['exposed_y']-60)/240,0,1);rgb=np.stack((70+175*v,165-105*v,100-55*v),axis=2).astype(np.uint8);rgb[wet]=(37,77,110)
    save(rgb,'Elevation','full-elevation-map.png',['Green Y60 -> brown Y300','Water blue; cave openings retained'])
    v=np.clip(m['relief32']/32,0,1);rgb=np.stack((75+180*v,180-145*v,135-105*v),axis=2).astype(np.uint8);rgb[wet]=(37,77,110)
    save(rgb,'33 x 33 land relief','full-relief-slope-map.png',['Green 0 -> red >=32','Slope8 / step1 in query store'])
    v=np.nan_to_num(np.clip(m['slope8'],0,2),nan=0)/2;rgb=np.stack((75+180*v,180-145*v,135-105*v),axis=2).astype(np.uint8);rgb[wet]=(37,77,110);rgb[(~wet)&~np.isfinite(m['slope8'])]=(100,100,100)
    save(rgb,'Slope8 rise/run','full-slope-map.png',['Green 0 -> red >=2','Grey: missing dry endpoints','No gameplay traversability claim'])
    rgb=cat(m['terrain_class']);rgb[(~wet)&(m['terrain_class']==0)]=(90,90,90)
    save(rgb,'Low-relief morphology','full-low-relief-map.png',['Green: FLAT','Gold: GENTLE (excludes FLAT)','Grey: other / unknown slope','Not buildability'])
    save(cat(m['land_component']),'4-neighbor land topology','full-water-land-topology.png',['Blue: actual surface water','Land colours: components','No water navigation inference'])
    for k in range(2,6):save(cat(m['k'+str(k)]),f'Attribute alternative k={k}','full-zoning-k'+str(k)+'.png',['All dry land, including satellites','16-block features / actual land mask','Numerical candidate only'])
    if 'zones' in m.files:
        rgb=cat(m['zones']);rgb[(~wet)&(m['zones']==0)]=(110,110,110)
        save(rgb,'Research natural units','full-natural-zones-candidate.png',['Green: SIRZ-R1-001 west low island','Gold: SIRZ-R1-002 east main island','Grey: separately indexed satellites','Blue: surface water','Internal gradients remain queryable','No political boundaries'])
