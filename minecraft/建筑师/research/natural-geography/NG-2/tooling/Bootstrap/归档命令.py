"""可查询快照无损分片与恢复；恢复目标已存在时拒绝覆盖。"""
import argparse,gzip,hashlib,json,shutil,sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
RAW=ROOT/'raw-or-queryable'
def digest(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def restore(dest,meta):
    compressed=RAW/'restore-temporary.gz'
    with compressed.open('xb') as f:
        for part in meta['parts']:
            p=RAW/part['name']
            if p.stat().st_size!=part['size'] or digest(p)!=part['sha256']:raise ValueError('分片校验失败')
            with p.open('rb') as src:shutil.copyfileobj(src,f)
    if digest(compressed)!=meta['gzip_sha256']:raise ValueError('gzip拼接校验失败')
    with gzip.open(compressed,'rb') as src,dest.open('xb') as f:shutil.copyfileobj(src,f)
    compressed.unlink()
    if digest(dest)!=meta['sqlite_sha256']:raise ValueError('数据库恢复哈希不符')
    db=sqlite3.connect('file:'+str(dest)+'?mode=ro',uri=True)
    if db.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise ValueError('恢复数据库损坏')
    db.close()
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['pack','restore']);args=parser.parse_args()
    manifest=ROOT/'manifest/archive.json'
    if args.command=='restore':
        restore(RAW/'refinement.sqlite',json.loads(manifest.read_text(encoding='utf-8')))
    else:
        source=RAW/'refinement.sqlite';tmp=RAW/'pack-temporary.gz'
        with source.open('rb') as src,tmp.open('wb') as target:
            with gzip.GzipFile(fileobj=target,mode='wb',compresslevel=6,mtime=0,filename='') as gz:shutil.copyfileobj(src,gz)
        parts=[]
        with tmp.open('rb') as f:
            while data:=f.read(64*1024*1024):
                p=RAW/f'refinement.sqlite.gz.part{len(parts)+1:03d}';p.write_bytes(data);parts.append({'name':p.name,'size':len(data),'sha256':digest(p)})
        meta={'format':'ordered binary concatenation -> gzip -> SQLite','sqlite_size':source.stat().st_size,'sqlite_sha256':digest(source),'gzip_size':tmp.stat().st_size,'gzip_sha256':digest(tmp),'parts':parts}
        manifest.write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8',newline='\n');tmp.unlink()
        check=RAW/'restored-check.sqlite';restore(check,meta);check.unlink()
        (ROOT/'validation/archive-roundtrip.json').write_text(json.dumps({'lossless_sha256_match':True,'restored_integrity_check':'ok','sqlite_sha256':meta['sqlite_sha256'],'parts':len(parts)},indent=2)+'\n',encoding='utf-8',newline='\n')
        print(json.dumps(meta))
