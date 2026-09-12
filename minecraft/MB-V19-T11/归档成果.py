"""只归档 T11 报告、复现脚本与证据，不包含游戏存档及备份。"""
from pathlib import Path
import shutil,zipfile,hashlib,json
R=Path(__file__).resolve().parent;root=Path('D:/Games/Minecraft/AI工程/发布/assets').resolve();D=(root/'minecraft/MB-V19-T11').resolve()
assert D.is_relative_to(root) and D.name=='MB-V19-T11'
D.mkdir(parents=True,exist_ok=True)
files=[p for p in R.iterdir() if (p.suffix in ['.md','.mjs','.py','.html'] or p.name=='.gitattributes') and p.name!='视图校正.py']
files+=list((R/'证据').glob('*.json'))+list((R/'证据').glob('*.png'))+[(R/'研究/技能原文-SKILL.md')]
for p in files:
 q=D/p.relative_to(R);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);assert hashlib.sha256(p.read_bytes()).digest()==hashlib.sha256(q.read_bytes()).digest()
packed=list((R/'蓝图').rglob('*.json'))+list(R.glob('*.npz'))+list((R/'证据').glob('*.u16'))
with zipfile.ZipFile(D/'蓝图与实存.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in packed:z.write(p,str(p.relative_to(R)))
with zipfile.ZipFile(D/'蓝图与实存.zip') as z:
 assert z.testzip() is None
 for p in packed:assert z.read(str(p.relative_to(R)).replace('\\','/'))==p.read_bytes()
manifest={str(p.relative_to(D)).replace('\\','/'):{'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(D.rglob('*')) if p.is_file() and p.name!='SHA256.json'}
(D/'SHA256.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'files':len(manifest),'zip_members':len(packed),'bytes':sum(i['size'] for i in manifest.values()),'archive':str(D)},ensure_ascii=True))
