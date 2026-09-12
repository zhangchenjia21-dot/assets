"""仅发布本轮说明、脚本和审计证据，不复制存档、runtime、模组或备份。"""
from pathlib import Path
import shutil,zipfile,hashlib
R=Path(__file__).resolve().parent;D=R.parent/'发布/assets/minecraft/MB-V18-T10';D.mkdir(parents=True,exist_ok=True)
files=list(R.glob('*.py'))+list(R.glob('*.mjs'))+list(R.glob('*.md'))+list(R.glob('*.html'))
for folder in ['证据','研究','上游']:
 files += [p for p in (R/folder).rglob('*') if p.is_file() and p.suffix in ['.md','.json','.png']]
for p in files:
 q=D/p.relative_to(R);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
with zipfile.ZipFile(D/'蓝图与实存数据.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(list((R/'蓝图').rglob('*.json'))+list(R.glob('*.npz'))+list((R/'证据').glob('*.u16'))):z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(D/'蓝图与实存数据.zip') as z:assert z.testzip() is None
(D/'.gitattributes').write_text('* -text\n',encoding='utf8')
(D/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(D).as_posix()+'\n' for p in sorted(D.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt'),encoding='utf8');print('Scoped archive complete; ZIP CRC verified')
