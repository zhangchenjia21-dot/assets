"""比较两次完整汇编的字节结果，覆盖数据库页顺序与稳定身份。"""
import hashlib,json,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
root=Path(__file__).resolve().parents[2]
paths=['raw-or-queryable/atlas.sqlite','atlas/id-registry.json','atlas/objects.jsonl','atlas/relations.jsonl']
def hashes():return {p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths}
def build():subprocess.run([sys.executable,str(root/'tooling/Bootstrap/图册命令.py'),'build'],check=True,capture_output=True)
if __name__=='__main__':
    identity_before=hashes()['atlas/id-registry.json']
    build();before=hashes();build();after=hashes()
    assert before==after,'full rebuild byte drift'
    assert before['atlas/id-registry.json']==identity_before,'identity drift'
    report={'status':'PASS','before':before,'after':after,'identity_before':identity_before,'method':'Two full builds; SQLite, ledger, object and relation JSONL byte-identical','initial_issue_resolved':'Identity registry rows now inserted in canonical ID order, independent of first-build versus loaded-ledger order.'}
    (root/'validation/rebuild.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('Rebuild PASS: SQLite, stable IDs, exports identical')
