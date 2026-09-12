"""仅归档本轮证据与复现输入，不读取或复制游戏存档。"""
from pathlib import Path
import shutil, zipfile, hashlib
src=Path(__file__).resolve().parent
dst=src.parent/'发布/assets/minecraft/MB-V17-T09'
dst.mkdir(parents=True,exist_ok=True)
for p in list(src.glob('*.py'))+list(src.glob('*.mjs'))+list(src.glob('*.md'))+[src/'调色板.json']+list((src/'证据').glob('*.json'))+list((src/'证据').glob('*.png'))+list((src/'证据').glob('*.md'))+[src/'研究/技能原文-SKILL.md']:
    q=dst/p.relative_to(src);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
with zipfile.ZipFile(dst/'蓝图与实存数据.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(list((src/'蓝图').rglob('*.json'))+list(src.glob('*.npz'))+list((src/'证据').glob('*.u16'))):z.write(p,p.relative_to(src).as_posix())
with zipfile.ZipFile(dst/'蓝图与实存数据.zip') as z:assert z.testzip() is None
(dst/'.gitattributes').write_text('* -text\n',encoding='utf8')
(dst/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(dst).as_posix()+'\n' for p in sorted(dst.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt'),encoding='utf8')
print(f'archived {len(list(dst.rglob("*")))} entries; zip verified')
