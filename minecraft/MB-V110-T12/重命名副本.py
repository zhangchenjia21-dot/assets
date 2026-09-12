"""仅修改新副本 level.dat 的 Data.LevelName 字符串；不写 region/POI/entity。"""
from pathlib import Path
import gzip,struct,json,hashlib
R=Path(__file__).resolve().parent
W=Path('D:/Games/Minecraft/.minecraft/versions/MB-V110-T12-隔离实例/saves/MB-V110-T12-京町家修复')
assert W.resolve()==W and W.name=='MB-V110-T12-京町家修复'
p=W/'level.dat';raw=p.read_bytes();b=gzip.decompress(raw);i=0;found=[]
def u16():
 global i
 n=struct.unpack_from('>H',b,i)[0];i+=2;return n
def string():
 global i
 n=u16();v=b[i:i+n].decode('utf8');i+=n;return v
def payload(t,path):
 global i
 if t in [1,2,3,4,5,6]:i+={1:1,2:2,3:4,4:8,5:4,6:8}[t]
 elif t==8:
  a=i;v=string()
  if path==['','Data','LevelName']:found.append((a,i,v))
 elif t in [7,11,12]:
  n=struct.unpack_from('>i',b,i)[0];i+=4+n*{7:1,11:4,12:8}[t]
 elif t==9:
  k=b[i];n=struct.unpack_from('>i',b,i+1)[0];i+=5
  for _ in range(n):payload(k,path+['[]'])
 elif t==10:
  while True:
   k=b[i];i+=1
   if not k:break
   name=string();payload(k,path+[name])
 else:raise ValueError(t)
t=b[i];i+=1;name=string();payload(t,[name]);assert i==len(b)
assert len(found)==1 and found[0][2]=='MB-V19-T11-京町家',found
a,z,old=found[0];v=W.name.encode('utf8');after=b[:a]+struct.pack('>H',len(v))+v+b[z:]
p.write_bytes(gzip.compress(after,mtime=0))
(R/'证据/副本更名.json').write_text(json.dumps({'old':old,'new':W.name,'only_tag':'Data.LevelName','source_level_sha256':hashlib.sha256(raw).hexdigest(),'destination_level_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'region_writes':0},ensure_ascii=False,indent=2),encoding='utf8')
