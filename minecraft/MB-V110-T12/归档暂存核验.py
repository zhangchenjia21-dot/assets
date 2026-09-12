"""核验 Git index 字节与发布哈希，防止换行自动转换破坏证据。"""
from pathlib import Path
import subprocess,json,hashlib
from PIL import Image
root=Path('D:/Games/Minecraft/AI工程/发布/assets');D=root/'minecraft/MB-V110-T12'
m=json.loads((D/'SHA256.json').read_text(encoding='utf8'));paths=list(m)+['SHA256.json']
inputs=''.join(':minecraft/MB-V110-T12/'+p+'\n' for p in paths).encode('utf8')
data=subprocess.run(['git','cat-file','--batch'],cwd=root,input=inputs,capture_output=True,check=True).stdout;off=0
for p in paths:
 end=data.index(b'\n',off);header=data[off:end].split();assert header[1]==b'blob',header
 size=int(header[2]);blob=data[end+1:end+1+size];off=end+size+2
 assert blob==(D/p).read_bytes(),p
 if p in m:assert hashlib.sha256(blob).hexdigest()==m[p]['sha256'],p
 if p.endswith('.png'):
  with Image.open(D/p) as im:im.verify()
print(f'{len(paths)} staged files byte-identical; SHA256 and PNG decoding verified')
