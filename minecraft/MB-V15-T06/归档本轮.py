"""仅复制本轮授权成果；不包含完整世界、备份或其它回归样本。"""
from pathlib import Path
import gzip,hashlib,json
R=Path(__file__).resolve().parent;D=R.parent/'发布/assets/minecraft/MB-V15-T06';D.mkdir(parents=True,exist_ok=False)
for p in R.rglob('*'):
 if not p.is_file():continue
 rel=p.relative_to(R)
 if '__pycache__' in rel.parts or p.name.startswith(('临时','设计')) or p.name.endswith(('-步行.npy','.ppm')):continue
 if rel.parts[0] not in ['来源','蓝图','作业','证据'] and p.suffix not in ['.py','.mjs','.md','.json','.npy']:continue
 data=p.read_bytes()
 if p.suffix in ['.bin','.npy']:rel=Path(str(rel)+'.gz');data=gzip.compress(data,compresslevel=9,mtime=0)
 elif rel.parts[0]!='来源' and p.suffix in ['.py','.mjs','.md','.json']:data=data.replace(b'\r\n',b'\n')
 out=D/rel;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data)
(D/'.gitattributes').write_bytes(('* -text\n来源/** -diff\n').encode('utf8'))
files=sorted(p for p in D.rglob('*') if p.is_file());lines=[hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(D).as_posix() for p in files];(D/'SHA256SUMS').write_bytes(('\n'.join(lines)+'\n').encode('utf8'));print(json.dumps({'files':len(files)+1,'bytes':sum(p.stat().st_size for p in files),'largest':max(p.stat().st_size for p in files)}))
