"""仅复制本任务公开成果，压缩读回体素并校验，保留所有原文件。"""
from pathlib import Path
import gzip,hashlib,json,shutil
R=Path(__file__).parent;A=R.parent/'发布/assets/minecraft/MB-V12-T03'
assert not A.exists(),'拒绝覆盖已有归档'
A.mkdir(parents=True)
for p in R.rglob('*'):
 if not p.is_file():continue
 rel=p.relative_to(R)
 if p.suffix in ['.npy','.ppm'] or p.name.startswith('临时'):continue
 if rel.parts[0]=='来源' and p.name not in ['minecraft-builder-v1.2.md','Wharram-history.html','Crowell-VCH.html']:continue
 if rel.parts[0]=='证据' and p.name.startswith('设计'):continue
 target=A/rel;target.parent.mkdir(parents=True,exist_ok=True)
 if p.suffix=='.bin':
  raw=p.read_bytes();target=target.with_suffix('.bin.gz');target.write_bytes(gzip.compress(raw,mtime=0));assert gzip.decompress(target.read_bytes())==raw
  m=json.loads(p.with_suffix('.json').read_text(encoding='utf8'));assert hashlib.sha256(raw).hexdigest()==m['sha256']
 elif p.suffix in ['.py','.mjs','.md','.json'] and rel.parts[0]!='来源':
  target.write_bytes(p.read_text(encoding='utf-8-sig').replace('\r\n','\n').encode('utf8'))
 else:shutil.copyfile(p,target)
(A/'.gitattributes').write_text('* -text\n来源/** -diff\n',encoding='utf8')
files=sorted(p for p in A.rglob('*') if p.is_file())
(A/'SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(A).as_posix()+'\n' for p in files),encoding='utf8')
print(json.dumps({'files':len(files)+1,'bytes':sum(p.stat().st_size for p in files),'largest':max((p.stat().st_size,str(p.relative_to(A))) for p in files)},ensure_ascii=False))
