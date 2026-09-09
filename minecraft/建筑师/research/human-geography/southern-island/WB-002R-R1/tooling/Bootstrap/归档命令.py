"""SQLite 无损压缩及逐文件哈希恢复；只写当前研究目录。"""
import gzip,hashlib,json,shutil,sqlite3,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def digest(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
mode=sys.argv[1] if len(sys.argv)>1 else 'archive';manifest=ROOT/'manifest/store.json'
if mode=='archive':
    entries=[]
    for name in ('observed.sqlite','regional-profile.sqlite'):
        src=ROOT/'raw-or-queryable'/name;archive=src.with_suffix('.sqlite.gz')
        with src.open('rb') as inp,archive.open('wb') as stream,gzip.GzipFile(filename='',mode='wb',fileobj=stream,mtime=0) as out:shutil.copyfileobj(inp,out)
        restore=src.with_suffix('.roundtrip.sqlite')
        with gzip.open(archive,'rb') as inp,restore.open('xb') as out:shutil.copyfileobj(inp,out)
        sha=digest(src);assert sha==digest(restore)
        db=sqlite3.connect(restore.as_uri()+'?mode=ro',uri=True);assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok';db.close();restore.unlink()
        entries.append({'name':name,'uncompressed_size':src.stat().st_size,'sha256':sha,'archive':archive.name,'archive_size':archive.stat().st_size,'archive_sha256':digest(archive),'roundtrip':'PASS','integrity_check':'ok'})
    manifest.write_text(json.dumps({'compression':'gzip lossless mtime=0','files':entries},indent=2)+'\n',encoding='utf-8');print('archive roundtrip PASS')
elif mode=='restore':
    for item in json.loads(manifest.read_text(encoding='utf-8'))['files']:
        dst=ROOT/'raw-or-queryable'/item['name'];src=ROOT/'raw-or-queryable'/item['archive'];assert digest(src)==item['archive_sha256']
        if dst.exists():assert digest(dst)==item['sha256'];continue
        with gzip.open(src,'rb') as inp,dst.open('xb') as out:shutil.copyfileobj(inp,out)
        assert digest(dst)==item['sha256']
    print('restore SHA256 PASS')
else:raise ValueError('archive or restore expected')
