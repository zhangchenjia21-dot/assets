"""固定本轮观测重建全部派生指标/关系/SQLite，核心不含运行时间戳。"""
import hashlib,json,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
def hashes():
    paths=[ROOT/'raw-or-queryable/regional-profile.sqlite',*sorted((ROOT/'profile').glob('*.json')),*sorted((ROOT/'profile').glob('*.jsonl'))]
    return {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
if __name__=='__main__':
    before=hashes()
    for cmd in ('derive','relations','build'):
        subprocess.run([sys.executable,str(ROOT/'tooling/Bootstrap/区域命令.py'),cmd],check=True,capture_output=True)
    after=hashes();assert before==after,{k for k in before if before[k]!=after[k]}
    (ROOT/'validation/rebuild.json').write_text(json.dumps({'status':'PASS','method':'Full derive + relations + build from frozen observed.sqlite; all profile JSON/JSONL and final SQLite byte-identical','before':before,'after':after},indent=2)+'\n',encoding='utf-8',newline='\n');print('full deterministic rebuild PASS',flush=True)
