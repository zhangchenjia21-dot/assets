"""仅归档 T05 授权成果；排除临时渲染、步行缓存及完整世界。"""
from pathlib import Path
import gzip,hashlib,json
R=Path(__file__).resolve().parent;D=R.parent/'发布/assets/minecraft/MB-V14-T05'
D.mkdir(parents=True,exist_ok=False)
for p in R.rglob('*'):
 if not p.is_file():continue
 rel=p.relative_to(R)
 if '__pycache__' in rel.parts or p.name.startswith(('临时','设计')) or p.name.endswith(('-步行.npy','.ppm')):continue
 if rel.parts[0] not in ['来源','证据','蓝图','作业'] and p.suffix not in ['.py','.mjs','.md','.json','.npy']:continue
 data=p.read_bytes()
 if p.suffix in ['.bin','.npy']:rel=Path(str(rel)+'.gz');data=gzip.compress(data,compresslevel=9,mtime=0)
 elif rel.parts[0]!='来源' and p.suffix in ['.py','.mjs','.md','.json']:data=data.replace(b'\r\n',b'\n')
 out=D/rel;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data)
(D/'.gitattributes').write_bytes(b'* -text\n')
files=sorted(p for p in D.rglob('*') if p.is_file());lines=[hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(D).as_posix() for p in files]
(D/'SHA256SUMS').write_bytes(('\n'.join(lines)+'\n').encode('utf8'))
print(json.dumps({'files':len(files)+1,'bytes':sum(p.stat().st_size for p in D.rglob('*') if p.is_file()),'largest':max((p.stat().st_size,str(p.relative_to(D))) for p in files)},ensure_ascii=False))
