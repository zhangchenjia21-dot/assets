"""从SQLite成员矩形生成派生图；颜色表达类别/状态，不能暗示更高采样精度。"""
import json,sqlite3
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

def render_maps(out):
    db=sqlite3.connect((out/'raw-or-queryable/atlas.sqlite').as_uri()+'?mode=ro',uri=True)
    objects={id:json.loads(raw) for id,raw in db.execute('SELECT id,details FROM atlas_objects ORDER BY id')}
    runs={}
    for gid,z0,z1,x0,x1 in db.execute('SELECT * FROM geometry_runs ORDER BY geometry_id,z0,x0'):runs.setdefault(gid,[]).append((x0,z0,x1,z1))
    bounds=json.loads(db.execute('SELECT value FROM meta WHERE key=?',('world_coverage_bounds',)).fetchone()[0]);x0,z0,x1,z1=bounds
    scale=960/(x1-x0+1);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13);title=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    def point(x,z):return 50+(x-x0)*scale,110+(z-z0)*scale
    def color(id):
        n=int(id.split('-')[1]);return ((n*67)%180+55,(n*109)%170+65,(n*37)%175+60)
    def base(name,subtitle):
        im=Image.new('RGB',(1460,1160),(23,28,34));d=ImageDraw.Draw(im)
        d.text((30,12),name+' | PROPOSED',font=title,fill='white');d.text((30,42),f'X [{x0},{x1}] Z [{z0},{z1}] | North -Z up; East +X right',font=font,fill='white')
        d.text((30,64),subtitle,font=font,fill='white');d.text((30,86),'Display only; 960 px = 10032 blocks. Colours do not imply precision. Source: atlas.sqlite / geometry_runs',font=font,fill='white')
        d.rectangle((50,110,1010,1070),fill=(42,48,53))
        return im,d
    def draw_object(d,o,fill):
        for a,b,c,e in runs[o['geometry']['id']]:
            px,pz=point(a,b);qx,qz=point(c+1,e+1);d.rectangle((px,pz,qx,qz),fill=fill)
    def finish(im,d,name):
        for x in (-6144,-4096,-2048,0,2048,3776):
            px,_=point(x,z0);d.line((px,1070,px,1078),fill='white');d.text((px-20,1080),str(x),font=font,fill='white')
        for z in (-6144,-4096,-2048,0,2048,3456):
            _,pz=point(x0,z);d.text((2,pz-7),str(z),font=font,fill='white')
        d.line((50,1120,50+1024*scale,1120),fill='white',width=3);d.text((50,1130),'1024 blocks',font=font,fill='white');im.save(out/'visual'/name)
    for family,name in [('NGEO','NGEO-consolidated.png'),('NHYD','NHYD-water-relations.png')]:
        im,d=base(family+' consolidated membership','64-block regional approximation; exact NG-2 local masks retained in query store; grey = no selected object')
        if family=='NHYD':
            for o in objects.values():
                if o['family']=='NGEO':draw_object(d,o,(65,70,62))
        group=[o for o in objects.values() if o['family']==family]
        for o in group:draw_object(d,o,color(o['id']))
        for i,o in enumerate(group):
            x,z=point(o['representative']['x'],o['representative']['z']);d.text((x-8,z-6),o['id'][-3:],font=font,fill='white')
            label=o['id']+' '+o['type']
            if d.textlength(label,font=font)>420:label=o['id']+' verified branching channel (local)'
            d.text((1030,115+i*23),label,font=font,fill=color(o['id']))
        d.text((1030,980),'Map numbers carry the '+family+' prefix.',font=font,fill='white')
        if family=='NHYD':
            for s,t,kind,status in db.execute('SELECT source,target,kind,evidence_status FROM relations WHERE source LIKE ? AND target LIKE ? ORDER BY source,target',('NHYD-%','NHYD-%')):
                if kind!='overlaps':continue
                a=objects[s]['representative'];b=objects[t]['representative'];d.line((*point(a['x'],a['z']),*point(b['x'],b['z'])),fill='white',width=1)
            d.text((1030,1005),'White links: overlap associations only.',font=font,fill='white');d.text((1030,1028),'No global real-water connected_to claim.',font=font,fill='white')
        finish(im,d,name)
    im,d=base('Evidence status / uncertainty','Green=SUPPORTED identity/local fact; amber=PROVISIONAL; grey=unresolved/unassigned patches')
    for o in objects.values():
        if o['family'] in ('NGEO','NHYD'):draw_object(d,o,(64,155,114) if o['evidence_status']=='SUPPORTED' else (180,144,70))
    for i,text in enumerate(['18 SUPPORTED objects / 49 PROVISIONAL','248 small land cells left unresolved','676 small water cells left unresolved','65 objects require further refinement','Supported massif identity does NOT','mean an exact regional boundary.','Water outside exact local ROIs stays','topologically unresolved.','V1 coarse water can miss narrow links.','All IDs remain PROPOSED.']):d.text((1030,130+i*27),text,font=font,fill='white')
    for o in objects.values():
        if o['family']=='NGEO':x,z=point(**o['representative']);d.text((x,z),o['id'][-3:],font=font,fill='white')
    finish(im,d,'evidence-uncertainty.png')
    im,d=base('NFEAT / NSITE observation overview','NFEAT and NSITE are natural evidence / observation anchors; no building or settlement selection')
    for o in objects.values():
        if o['family']=='NGEO':draw_object(d,o,(66,80,69))
        elif o['family']=='NHYD':draw_object(d,o,(44,80,118))
    for i,o in enumerate(o for o in objects.values() if o['family'] in ('NFEAT','NSITE')):
        x,z=point(**o['representative']);c=(245,125,221) if o['family']=='NFEAT' else (246,211,96)
        d.ellipse((x-4,z-4,x+4,z+4),fill=c);d.text((x+7,z-18 if o['family']=='NFEAT' else z+4),o['id'],font=font,fill=c)
        d.text((1030,120+i*52),o['id']+' '+str(o['representative']),font=font,fill=c);d.text((1030,140+i*52),o['type'][:51],font=font,fill='white')
    finish(im,d,'features-sites.png')
    # 对照包括GEO原水域：不将1264个混合GEO和35个纯陆NGEO误作一一对应。
    compare=Image.new('RGB',(1480,850),(23,28,34));d=ImageDraw.Draw(compare)
    d.text((25,15),'V1 GEO -> Consolidated Atlas | categorical comparison, not an accuracy map',font=title,fill='white')
    d.text((25,45),f'X [{x0},{x1}], Z [{z0},{z1}]; North -Z up / East +X right; 700 px = 10032 blocks',font=font,fill='white')
    for gx,gz,gid in db.execute('SELECT gx,gz,v1_geo FROM cell_index'):
        if not gid:continue
        ax=max(gx*64,x0);bz=max(gz*64,z0);cx=min(gx*64+63,x1);dz=min(gz*64+63,z1)
        d.rectangle((25+(ax-x0)*700/10032,100+(bz-z0)*700/10032,25+(cx-x0+1)*700/10032,100+(dz-z0+1)*700/10032),fill=color(gid))
    for o in objects.values():
        if o['family'] not in ('NGEO','NHYD'):continue
        for ax,bz,cx,dz in runs[o['geometry']['id']]:d.rectangle((755+(ax-x0)*700/10032,100+(bz-z0)*700/10032,755+(cx-x0+1)*700/10032,100+(dz-z0+1)*700/10032),fill=color(o['id']))
    d.text((25,78),'V1: 1264 GEO (987 land candidates + 277 water)',font=font,fill='white');d.text((755,78),'Atlas: 35 NGEO + 20 NHYD; 4 NFEAT / 8 NSITE separate',font=font,fill='white')
    d.text((25,820),'Unassigned small patches and uncertain boundaries are retained; there is no one-to-one promotion.',font=font,fill='white')
    compare.save(out/'visual/V1-atlas-comparison.png');db.close()
