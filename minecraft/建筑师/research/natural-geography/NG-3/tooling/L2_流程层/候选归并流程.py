import json,sqlite3,hashlib
from collections import Counter
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from L1_器件层.区域分段器 import segment
from L1_器件层.源快照保护器 import write_json

def candidates(out):
    if json.loads((out/'manifest/freshness.json').read_text(encoding='utf-8'))['geography_snapshot_status']!='CURRENT_MATCH':raise ValueError('freshness gate未通过')
    db=sqlite3.connect((out/'raw-or-queryable/input-cache/v1.sqlite').as_uri()+'?mode=ro',uri=True);db.row_factory=sqlite3.Row
    rows=[dict(r) for r in db.execute('SELECT * FROM cells ORDER BY gz,gx')];db.close();a=segment(rows);gx0,gz0=map(int,a['origin'])
    (out/'atlas').mkdir(exist_ok=True);(out/'visual').mkdir(exist_ok=True)
    np.savez_compressed(out/'raw-or-queryable/numeric-segmentation.npz',**a)
    candidates=[];lookup={(r['gx'],r['gz']):r for r in rows}
    for family,key in [('NGEO','land_units'),('NHYD','water_units')]:
        units=a[key];ids=sorted(i for i in np.unique(units) if i>0)
        rgb=np.full((*units.shape,3),(25,30,40),np.uint8);rgb[units==-1]=(100,100,100)
        for number,id in enumerate(ids,1):
            zz,xx=np.where(units==id);members=sorted((int(x+gx0),int(z+gz0)) for z,x in zip(zz,xx));data=[lookup[p] for p in members]
            centroid=(float(np.mean(xx)+gx0)*64+32,float(np.mean(zz)+gz0)*64+32)
            rp=min(data,key=lambda r:(r['x']-centroid[0])**2+(r['z']-centroid[1])**2)
            entry={'candidate':f'{family}-C{number:03d}','numeric_component':int(id),'cells':len(members),'member_hash':hashlib.sha256(json.dumps(members,separators=(',',':')).encode()).hexdigest(),'bounds':[min(p[0] for p in members)*64,min(p[1] for p in members)*64,max(p[0] for p in members)*64+63,max(p[1] for p in members)*64+63],'representative':[rp['x'],rp['z']],'mean_elevation':float(np.mean([r['elevation'] for r in data])),'min_elevation':min(r['elevation'] for r in data),'max_elevation':max(r['elevation'] for r in data),'mean_relief':float(np.mean([r['relief'] for r in data])),'mean_slope':float(np.mean([r['slope'] for r in data])),'terrain_counts':dict(Counter(r['terrain'] for r in data)),'top_biomes':Counter(r['biome'] for r in data).most_common(5),'numeric_band_counts':dict(Counter(str(int(a['numeric_bands'][z,x])) for z,x in zip(zz,xx))),'edge_censored':bool(min(xx)==0 or max(xx)==units.shape[1]-1 or min(zz)==0 or max(zz)==units.shape[0]-1)}
            candidates.append(entry);rgb[units==id]=((number*67)%190+50,(number*109)%180+50,(number*37)%180+50)
        im=Image.new('RGB',(1264,1110),(24,28,33));im.paste(Image.fromarray(rgb).resize((948,948),Image.Resampling.NEAREST),(0,90));draw=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13)
        draw.text((12,12),f'{family} numerical candidates only; no semantic promotion | North -Z up / East +X right',font=font,fill='white')
        draw.text((12,36),'64-block cells; 320-block land height/relief window; water barrier; grey=unresolved small patches',font=font,fill='white')
        draw.text((12,58),f'Grid X [{gx0*64},{(gx0+units.shape[1])*64-1}] Z [{gz0*64},{(gz0+units.shape[0])*64-1}]; numbers carry {family}-C prefix; 6 px = 64 blocks',font=font,fill='white')
        for c in candidates:
            if not c['candidate'].startswith(family):continue
            x,z=c['representative'];draw.text(((x/64-gx0)*6,90+(z/64-gz0)*6),c['candidate'][-3:],font=font,fill='white')
        im.save(out/'visual'/f'{family}-candidate-review.png')
    write_json(out/'atlas/numeric-candidates.json',candidates)
    print(json.dumps([{'candidate':c['candidate'],'cells':c['cells'],'representative':c['representative'],'mean_y':round(c['mean_elevation']),'relief':round(c['mean_relief']),'bands':c['numeric_band_counts']} for c in candidates]))
