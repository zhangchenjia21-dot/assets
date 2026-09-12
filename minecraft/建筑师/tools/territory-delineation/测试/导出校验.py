"""独立解压器验证 ZIP CRC、JSON 格网和 PNG 像素；只写本工具示例目录。"""
import io,json,zipfile
from pathlib import Path
from collections import Counter
from PIL import Image
root=Path(__file__).resolve().parents[1]
expected={'data/territories/'+s for s in ['current.json','preview.png','areas.md','adjacency.json','qa.md']}
colors=[(226,189,102,255),(92,189,152,255),(174,147,220,255),(232,142,105,255),(155,169,184,255),(239,110,152,255)]
for filename,status in [('example.zip','DRAFT'),('confirmed.zip','OWNER_CONFIRMED')]:
    with zipfile.ZipFile(root/'测试/临时'/filename) as z:
        assert set(z.namelist())==expected and z.testzip() is None
        doc=json.loads(z.read('data/territories/current.json'));assert doc['status']==status
        areas=Counter()
        for zz,a,b,c in doc['runs']:areas[c]+=b-a+1
        assert [areas[i] for i in range(6)]==[92124,0,13661,0,2150896,0]
        im=Image.open(io.BytesIO(z.read('data/territories/preview.png'))).convert('RGBA');assert im.size==(3264,2112)
        counts=Counter(im.getdata());assert [counts[c] for c in colors]==[areas[i] for i in range(6)]
        adj=json.loads(z.read('data/territories/adjacency.json'));assert adj['revision']==doc['revision']
        assert all(adj['matrix'][i][j]==adj['matrix'][j][i] for i in range(6) for j in range(6))
        if status=='DRAFT':
            for name in sorted(expected):
                p=root/'examples/initial-state'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(name))
(root/'validation/导出结果.json').write_text(json.dumps({'status':'PASS','checks':['ZIP CRC and five exact paths','draft and Owner-confirmed status','RLE area totals','PNG exact color counts and dimensions','revision linkage and adjacency symmetry'],'example':'initial geometry, DRAFT, no Owner authorization'},indent=2),encoding='utf-8')
print('export PASS')
