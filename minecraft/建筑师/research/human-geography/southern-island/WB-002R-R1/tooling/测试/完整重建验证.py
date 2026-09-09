"""固定 observed 输入完整重算，比较核心 SQLite 和所有 profile 导出字节。"""
import sys,json,hashlib,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tooling'))
from L1_器件层.源快照保护器 import digest,write_json
def hashes():
    paths=sorted((ROOT/'profile').glob('*.json'))+sorted((ROOT/'profile').glob('*.jsonl'))+[ROOT/'raw-or-queryable/regional-profile.sqlite']
    return {p.relative_to(ROOT).as_posix():digest(p) for p in paths}
before=hashes()
for name in ('画像命令.py','汇编命令.py'):subprocess.run([sys.executable,str(ROOT/'tooling/Bootstrap'/name)],check=True)
after=hashes();write_json(ROOT/'validation/rebuild.json',{'status':'PASS' if before==after else 'FAIL','fixed_input_observed_sha256':digest(ROOT/'raw-or-queryable/observed.sqlite'),'before':before,'after':after,'byte_identical':before==after});assert before==after
print('complete rebuild byte-identical PASS')
