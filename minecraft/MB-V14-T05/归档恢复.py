"""校验本任务归档，或恢复到一个全新目录；不会进入或写入 Minecraft 存档。"""
from pathlib import Path
import hashlib,gzip,sys
R=Path(__file__).resolve().parent
def verify():
 entries=[]
 for line in (R/'SHA256SUMS').read_text(encoding='utf8').splitlines():
  sha,name=line.split('  ',1);p=(R/name).resolve()
  if not p.is_relative_to(R) or hashlib.sha256(p.read_bytes()).hexdigest()!=sha:raise ValueError('HASH_MISMATCH '+name)
  entries.append(p)
 print('Verified',len(entries),'files');return entries
if __name__=='__main__':
 files=verify()
 if len(sys.argv)>1 and sys.argv[1]=='restore':
  dest=Path(sys.argv[2]).resolve();dest.mkdir(parents=True,exist_ok=False)
  for p in files:
   rel=p.relative_to(R);raw=p.read_bytes()
   if p.name.endswith(('.bin.gz','.npy.gz')):rel=rel.with_suffix('');raw=gzip.decompress(raw)
   out=dest/rel;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw)
  print('Restored to',dest)
