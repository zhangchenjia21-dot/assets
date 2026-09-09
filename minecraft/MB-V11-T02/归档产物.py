"""仅复制 T02 产物，不上传存档、备份或临时渲染缓存。"""
from pathlib import Path
import shutil,hashlib,json,gzip
R=Path(__file__).parent;dest=R.parent/'发布/assets/minecraft/MB-V11-T02';dest.mkdir(parents=True,exist_ok=True)
include={'来源','蓝图','作业','证据','候选'};files=[]
for p in R.rglob('*'):
 if not p.is_file():continue
 rel=p.relative_to(R)
 if len(rel.parts)>1 and rel.parts[0] not in include:continue
 if p.suffix=='.npy' or p.suffix=='.bin' or p.name.startswith('临时') or p.suffix=='.ppm':continue
 if len(rel.parts)==1 and p.suffix not in ['.py','.mjs','.json','.md'] and p.name!='.gitattributes':continue
 target=dest/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
 if rel.parts[0]!='来源' and (p.suffix in ['.py','.mjs','.json','.md'] or p.name=='.gitattributes'):
  content='\n'.join(line.rstrip() for line in p.read_text(encoding='utf-8-sig').splitlines()).rstrip()+'\n'
  target.write_bytes(content.encode('utf8'))
 files.append(target)
for n in range(1,6):
 data=gzip.decompress((dest/f'证据/阶段{n}-实存.bin.gz').read_bytes());meta=json.loads((dest/f'证据/阶段{n}-实存.json').read_text(encoding='utf8'))
 assert hashlib.sha256(data).hexdigest()==meta['sha256']
manifest='\n'.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(dest).as_posix() for p in sorted(files))+'\n'
(dest/'SHA256SUMS.txt').write_bytes(manifest.encode('utf8'));print(json.dumps({'files':len(files)+1,'bytes':sum(p.stat().st_size for p in files),'destination':str(dest)},ensure_ascii=False))
