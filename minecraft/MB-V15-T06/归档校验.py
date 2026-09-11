"""只读核对归档文件与压缩体素哈希，不访问游戏存档。"""
from pathlib import Path
import hashlib,gzip,json
R=Path(__file__).resolve().parent;count=0
for line in (R/'SHA256SUMS').read_text(encoding='utf8').splitlines():
 sha,name=line.split('  ',1);p=(R/name).resolve();assert p.is_relative_to(R);assert hashlib.sha256(p.read_bytes()).hexdigest()==sha,name;count+=1
for p in (R/'证据').glob('*.bin.gz'):
 b=gzip.decompress(p.read_bytes());m=json.loads(p.with_suffix('').with_suffix('.json').read_text(encoding='utf8'));assert hashlib.sha256(b).hexdigest()==m['sha256'],p.name
print('Verified',count,'files and all readback gzip hashes')
