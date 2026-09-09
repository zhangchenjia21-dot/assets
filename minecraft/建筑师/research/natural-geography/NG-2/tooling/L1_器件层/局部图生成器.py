import json
import hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont

def render(db,out,configs,targets):
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',12)
    thumbs=[]
    for id,config in configs.items():
        raw=out/'raw-or-queryable'/f'{id}-grid8.npz'
        if not raw.exists():continue
        a=np.load(raw);h=a['height'].astype(float);lo,hi=h.min(),h.max();b=config['bounds'];p=targets[id]['representative']
        normalized=(h-lo)/max(1,hi-lo);rgb=np.stack((35+210*normalized,65+175*normalized,75+160*normalized),axis=-1).astype(np.uint8)
        water=a['water_top']!=-32768;rgb[water]=(40,115,206)
        w=680;hei=max(320,round(w*h.shape[0]/h.shape[1]));im=Image.fromarray(rgb).resize((w,hei),Image.Resampling.NEAREST)
        canvas=Image.new('RGB',(1100,max(680,hei+155)),(24,28,33));canvas.paste(im,(0,85));d=ImageDraw.Draw(canvas)
        d.text((12,8),f'{id} | observed-column terrain | Y {lo:.0f}..{hi:.0f}',fill='white',font=font)
        d.text((12,30),f'ROI X [{b[0]}, {b[2]}] Z [{b[1]}, {b[3]}] | North -Z up; East +X right',fill='white',font=font)
        d.text((12,53),'Map raster: 8-block actual samples; detailed raw store: 8 / adaptive 4 / profiles 1; blue = actual water',fill='white',font=small)
        def px(x,z):return ((x-b[0])/(b[2]-b[0]+1)*w,85+(z-b[1])/(b[3]-b[1]+1)*hei)
        x,z=px(p['x'],p['z']);d.line((x-8,z,x+8,z),fill='red',width=2);d.line((x,z-8,x,z+8),fill='red',width=2)
        cb=targets[id]['bounds'];a0,c0=px(cb['min_x'],cb['min_z']);a1,c1=px(cb['max_x']+1,cb['max_z']+1);d.rectangle((a0,c0,a1,c1),outline='yellow',width=2)
        d.text((w+15,88),'Red cross: V1 target',fill='white',font=small);d.text((w+15,110),'Yellow: V1 64-block cell',fill='yellow',font=small)
        d.text((w+15,134),'No interpolated heights.',fill='white',font=small)
        profiles={}
        for name,dist,y in db.execute('SELECT name,distance,elevation FROM profiles WHERE target=? ORDER BY name,distance',(id,)):profiles.setdefault(name,[]).append((dist,y))
        for i,(name,pts) in enumerate(profiles.items()):
            if i>=4:break
            left=w+18;top=175+i*120;pw=370;ph=78
            if top+ph>canvas.height-10:break
            xs=[v[0] for v in pts];ys=[v[1] for v in pts];xmin=min(xs);xmax=max(xs);ymin=min(ys);ymax=max(ys)
            d.text((left,top-22),f'{name}: Y {ymin}..{ymax}; 1-block columns',fill='white',font=small)
            pp=[(left+(v-xmin)/max(1,xmax-xmin)*pw,top+ph-(y-ymin)/max(1,ymax-ymin)*ph) for v,y in pts]
            d.rectangle((left,top,left+pw,top+ph),outline=(100,100,100));d.line(pp,fill=(235,196,89),width=2)
            d.text((left,top+ph+2),f'Distance from profile start: 0..{xmax:.0f} blocks',fill=(185,190,195),font=small)
        scale=128*w/(b[2]-b[0]+1);d.line((12,hei+107,12+scale,hei+107),fill='white',width=3);d.text((12,hei+119),'128 blocks',fill='white',font=small)
        d.text((170,hei+100),'Vegetation-filtered surface; observed 8-block raster.',fill='white',font=small)
        d.text((170,hei+119),'Water topology and refined boundaries are separate evidence.',fill='white',font=small)
        canvas.save(out/'visual'/f'{id}-context.png');thumbs.append(canvas.resize((550,round(canvas.height/2))))
        topo=out/'raw-or-queryable'/f'{id}-topology1.npz'
        if topo.exists():
            a=np.load(topo);wet=a['water_top']!=-32768;rgb=np.full((*wet.shape,3),(161,155,116),dtype=np.uint8);rgb[wet]=(35,109,198)
            mask=wet;shore=np.zeros(mask.shape,bool);shore[1:]|=mask[1:]!=mask[:-1];shore[:,1:]|=mask[:,1:]!=mask[:,:-1];rgb[shore]=(235,222,152)
            im=Image.fromarray(rgb);can=Image.new('RGB',(max(im.width,1050),im.height+105),(24,28,33));can.paste(im,(0,85));dd=ImageDraw.Draw(can)
            dd.text((12,8),f'{id}: exact water/land topology | 1 pixel = 1 block | North -Z up; East +X right',fill='white',font=font)
            dd.text((12,31),f'ROI X [{b[0]}, {b[2]}] Z [{b[1]}, {b[3]}] | blue: block water, including verified water below ice',fill='white',font=small)
            dd.text((12,52),'Tan: exposed non-water | pale line: refined shoreline | red: V1 point | yellow: V1 cell',fill='white',font=small)
            x=p['x']-b[0];z=p['z']-b[1]+85;dd.ellipse((x-5,z-5,x+5,z+5),fill='red');dd.rectangle((cb['min_x']-b[0],cb['min_z']-b[1]+85,cb['max_x']-b[0],cb['max_z']-b[1]+85),outline='yellow',width=2)
            if id=='SITE-011':
                for z,x0,x1 in [(-4100,-147,-106),(-3800,-707,-264)]:
                    py=z-b[1]+85;dd.line((x0-b[0],py,x1-b[0],py),fill='cyan',width=3);dd.text((x0-b[0],py+5),f'X {x0}..{x1}; {x1-x0+1} columns',font=small,fill='white')
                dd.rectangle((0-b[0],-4464-b[1]+85,176-b[0],-4145-b[1]+85),outline='cyan',width=2)
                dd.text((12,can.height-18),'Cyan: specified opening sections / open-water context box; no unique bay polygon is asserted.',font=small,fill='white')
            can.save(out/'visual'/f'{id}-water-topology.png')
    if thumbs:
        rh=max(t.height for t in thumbs);overview=Image.new('RGB',(1100,((len(thumbs)+1)//2)*rh),(24,28,33))
        for i,t in enumerate(thumbs):overview.paste(t,((i%2)*550,(i//2)*rh))
        overview.save(out/'visual'/'eight-target-comparison.png')

def detail_views(db,out,configs,targets):
    """派生边界为采样阈值掩膜；标注其分辨率，不把它当作完整地貌边界。"""
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
    for id,cfg in configs.items():
        a=np.load(out/'raw-or-queryable'/f'{id}-grid8.npz');b=cfg['bounds'];p=targets[id]['representative']
        feature='high_terrain_200' if id=='SITE-017' else 'target_elevation_band' if id=='SITE-014' else 'low_slope_land'
        slope=a['slope'];rgb=np.zeros((*slope.shape,3),np.uint8);v=np.clip(slope/0.5,0,1)
        rgb[:,:,0]=50+v*200;rgb[:,:,1]=170-v*100;rgb[:,:,2]=90-v*40
        rgb[a['water_top']!=-32768]=(35,109,198)
        mask=a[feature];edge=np.zeros(mask.shape,bool);edge[1:]|=mask[1:]!=mask[:-1];edge[:,1:]|=mask[:,1:]!=mask[:,:-1];rgb[edge]=(255,230,80)
        w=800;h=round(w*slope.shape[0]/slope.shape[1]);im=Image.new('RGB',(max(w,1100),h+110),(24,28,33));im.paste(Image.fromarray(rgb).resize((w,h),Image.Resampling.NEAREST),(0,100));d=ImageDraw.Draw(im)
        for i,text in enumerate([f'{id} slope and sampled boundary | 8-block actual grid; North -Z up, East +X right',f'X [{b[0]}, {b[2]}] Z [{b[1]}, {b[3]}] | 128 blocks = {128*w/(b[2]-b[0]+1):.1f} pixels',f'Green: slope 0; red: rise/run >=0.5; blue: water; yellow: {feature}', 'Red: V1 point; white rectangle: V1 cell. Mask boundary is sampled and may be ROI-censored.']):d.text((8,6+i*23),text,font=font,fill='white')
        def point(x,z):return ((x-b[0])*w/(b[2]-b[0]+1),100+(z-b[1])*h/(b[3]-b[1]+1))
        x,z=point(p['x'],p['z']);d.ellipse((x-4,z-4,x+4,z+4),fill='red');cb=targets[id]['bounds'];x0,z0=point(cb['min_x'],cb['min_z']);x1,z1=point(cb['max_x']+1,cb['max_z']+1);d.rectangle((x0,z0,x1,z1),outline='white',width=2)
        im.save(out/'visual'/f'{id}-slope-boundary.png')
    critical=out/'raw-or-queryable/SITE-002-critical1.npz'
    if critical.exists():
        a=np.load(critical);m=json.loads((out/'assessments/SITE-002-metrics.json').read_text(encoding='utf-8'))['critical_depression_test'];b=m['bounds'];h=a['height'];v=np.clip((h-h.min())/max(1,h.max()-h.min()),0,1)
        rgb=np.stack((40+180*v,60+150*v,70+130*v),axis=-1).astype(np.uint8);q=h//4;edge=np.zeros(q.shape,bool);edge[1:]|=q[1:]!=q[:-1];edge[:,1:]|=q[:,1:]!=q[:,:-1];rgb[edge]=(90,95,100)
        scale=3;im=Image.new('RGB',(1100,h.shape[0]*scale+110),(24,28,33));im.paste(Image.fromarray(rgb).resize((h.shape[1]*scale,h.shape[0]*scale),Image.Resampling.NEAREST),(0,100));d=ImageDraw.Draw(im)
        for i,t in enumerate(['SITE-002 critical core | 1-block actual columns; contours every 4 Y; 3 pixels/block',f'X [{b[0]}, {b[2]}] Z [{b[1]}, {b[3]}] | North -Z up; East +X right', 'Cyan: conservative E-W terrain-step route; magenta: N-S route (when found)', 'Red: V1 point. Step routes model integer heights, not full gameplay physics.']):d.text((8,6+23*i),t,font=font,fill='white')
        for name,color in [('east-west','cyan'),('north-south','magenta')]:
            pts=[((p['x']-b[0])*scale,100+(p['z']-b[1])*scale) for p in m['terrain_step_crossings'][name]['path']]
            if len(pts)>1:d.line(pts,fill=color,width=2)
        p=targets['SITE-002']['representative'];x=(p['x']-b[0])*scale;z=100+(p['z']-b[1])*scale;d.ellipse((x-5,z-5,x+5,z+5),fill='red')
        im.save(out/'visual/SITE-002-critical-contours.png')
