"""限定 T04 成果复制与无损压缩；拒绝覆盖归档目录，不上传完整存档。"""
from pathlib import Path
import gzip,hashlib,json,shutil
R=Path(__file__).parent;A=R.parent/'发布/assets/minecraft/MB-V13-T04';assert not A.exists(),'归档已存在，拒绝覆盖';A.mkdir(parents=True)
restored=[]
for p in R.rglob('*'):
 if not p.is_file():continue
 rel=p.relative_to(R)
 if p.name.startswith('临时') or p.suffix=='.ppm':continue
 if rel.parts[0]=='证据' and (p.suffix=='.npy' or p.name.startswith('设计')):continue
 target=A/rel;target.parent.mkdir(parents=True,exist_ok=True)
 if p.suffix in ['.bin','.npy']:
  raw=p.read_bytes();target=target.with_suffix(target.suffix+'.gz');target.write_bytes(gzip.compress(raw,mtime=0));assert gzip.decompress(target.read_bytes())==raw
  sha=hashlib.sha256(raw).hexdigest();restored.append({'file':target.relative_to(A).as_posix(),'uncompressed_sha256':sha,'uncompressed_bytes':len(raw)})
  if p.suffix=='.bin':assert sha==json.loads(p.with_suffix('.json').read_text(encoding='utf8'))['sha256']
 elif rel.parts[0]!='来源' and p.suffix in ['.py','.mjs','.md','.json']:
  target.write_bytes((p.read_text(encoding='utf-8-sig').replace('\r\n','\n').rstrip()+'\n').encode('utf8'))
 else:shutil.copyfile(p,target)
(A/'无损恢复清单.json').write_bytes(json.dumps(restored,ensure_ascii=False,indent=2).encode('utf8'))
(A/'.gitattributes').write_bytes('* -text\n来源/** -diff\n'.encode('utf8'))
files=sorted(p for p in A.rglob('*') if p.is_file());(A/'SHA256SUMS').write_bytes(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(A).as_posix()+'\n' for p in files).encode('utf8'))
print(json.dumps({'files':len(files)+1,'bytes':sum(p.stat().st_size for p in files),'largest_bytes':max(p.stat().st_size for p in files)},ensure_ascii=False))
