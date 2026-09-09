"""将已完成调查复制到成果仓库；SQLite 使用可验证的确定性 gzip，不读取游戏世界。"""
import argparse
import gzip
import hashlib
import json
import shutil
from pathlib import Path

def digest(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()

def archive(source,destination):
    source=source.resolve();destination=destination.resolve()
    if source==destination or source in destination.parents or destination in source.parents:
        raise ValueError('来源与发布目录必须独立')
    target=destination/'World-Survey'/source.name
    copied=[]
    for path in sorted(source.rglob('*')):
        if not path.is_file() or '__pycache__' in path.parts or path.name.endswith(('.sqlite','.sqlite-journal','.sqlite-wal','.sqlite-shm','.pyc')):
            continue
        relative=path.relative_to(source);output=target/relative
        output.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(path,output)
        if digest(path)!=digest(output):raise ValueError('复制哈希不一致')
        copied.append({'path':output.relative_to(destination).as_posix(),'sha256':digest(output)})
    database=source/'raw'/'geography.sqlite';packed=target/'raw'/'geography.sqlite.gz'
    packed.parent.mkdir(parents=True,exist_ok=True)
    original=digest(database)
    with database.open('rb') as inp,packed.open('wb') as out:
        with gzip.GzipFile(filename='',mode='wb',fileobj=out,mtime=0,compresslevel=9) as stream:
            shutil.copyfileobj(inp,stream)
    with gzip.open(packed,'rb') as restored:
        restored_hash=hashlib.file_digest(restored,'sha256').hexdigest()
    if restored_hash!=original or digest(database)!=original:
        raise ValueError('数据库归档一致性验证失败')
    if packed.stat().st_size>=100*1024*1024:
        raise ValueError('压缩后仍超过 GitHub 单文件限制')
    record={'source_directory':str(source),'database':{'path':'World-Survey/'+source.name+'/raw/geography.sqlite','bytes':database.stat().st_size,'sha256':original},'archive':{'path':packed.relative_to(destination).as_posix(),'bytes':packed.stat().st_size,'sha256':digest(packed)},'decompressed_sha256_matches':True,'copied_files':copied}
    (destination/'发布归档.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'copied_files':len(copied),'database_bytes':database.stat().st_size,'archive_bytes':packed.stat().st_size,'decompressed_sha256_matches':True}))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('source',type=Path)
    parser.add_argument('destination',type=Path)
    args=parser.parse_args();archive(args.source,args.destination)
