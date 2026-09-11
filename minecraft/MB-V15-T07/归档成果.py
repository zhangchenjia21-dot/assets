"""仅归档本轮输出，不复制游戏存档、备份、模组或其它测试。"""
from pathlib import Path
import json,zipfile,hashlib,shutil,html
R=Path(__file__).resolve().parent;dest=R.parent/'发布/assets/minecraft/MB-V15-T07';dest.mkdir(parents=True,exist_ok=True)
(dest/'.gitattributes').write_bytes(b'* -text\n')
def digest(b):return hashlib.sha256(b).hexdigest()
stages=['01-Macro','02-Meso','03-Micro','04-Repair','05-Water']
packed={}
for s in stages:
    root=R/'蓝图'/s;manifest=json.loads((root/'清单.json').read_text());files=[root/'清单.json']+[root/f for f in manifest['files']]
    files += [R/f'方案-{s}.npz',R/f'证据/{s}-实存方块.u16']
    for f in files:packed[f.relative_to(R).as_posix()]=f.read_bytes()
packed['设计地面.npy']=(R/'设计地面.npy').read_bytes()
hashes={k:digest(b) for k,b in packed.items()}
with zipfile.ZipFile(dest/'现场与蓝图.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for k,b in packed.items():z.writestr(k,b)
    z.writestr('压缩包内容SHA256.json',json.dumps(hashes,ensure_ascii=False,indent=2))
with zipfile.ZipFile(dest/'现场与蓝图.zip') as z:
    assert z.testzip() is None
    for k,h in hashes.items():assert digest(z.read(k))==h,k
for f in R.iterdir():
    if f.is_file() and f.suffix in ['.md','.py','.mjs','.json']:shutil.copy2(f,dest/f.name)
(dest/'研究').mkdir(exist_ok=True);shutil.copy2(R/'研究/技能原文-SKILL.md',dest/'研究/技能原文-SKILL.md')
(dest/'证据').mkdir(exist_ok=True)
for f in (R/'证据').iterdir():
    if f.suffix=='.json' or (f.suffix=='.png' and not f.name.startswith('04-Repair')):shutil.copy2(f,dest/'证据'/f.name)
images=['东南总览','西北总览','南来道路','门前抵达','院落回望','西侧水荫','田间步行','北脊剖望','俯视','剖面Z108']
for n in images:assert (dest/f'证据/05-Water-{n}.png').exists(),n
body=''.join(f'<section><h2>{n}</h2><img src="证据/05-Water-{n}.png" alt="{n}"></section>' for n in images)
page='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>T07 实存空间审计</title><style>body{background:#22251f;color:#eee;font:16px sans-serif;max-width:1200px;margin:30px auto;padding:20px}img{width:100%;height:auto}section{margin:40px 0}a{color:#b4d69d}p{line-height:1.7}</style><h1>T07 绿洲驿站 · 实存空间审计</h1><p>实际存档体素渲染，非 Minecraft 客户端截图；原生复杂形状与光照简化，流体运行未验证。<a href="Completion%20Report.md">Completion Report</a> 记录来源、阶段修订、坐标与限制。</p>'+body+'</html>'
(dest/'证据索引.html').write_text(page,encoding='utf8');(R/'证据索引.html').write_text(page,encoding='utf8')
out={'archive':str(dest),'compressed_files':len(hashes),'uncompressed_bytes':sum(map(len,packed.values())),'archive_bytes':(dest/'现场与蓝图.zip').stat().st_size,'roundtrip_hash_match':True,'full_world_uploaded':False}
(dest/'归档核验.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
for f in dest.rglob('*'):
    if f.is_file() and f.suffix in ['.md','.py','.mjs','.json','.html']:
        f.write_bytes(f.read_bytes().replace(b'\r\n',b'\n'))
manifest={f.relative_to(dest).as_posix():digest(f.read_bytes()) for f in sorted(dest.rglob('*')) if f.is_file() and f.name!='SHA256SUMS.json'}
(dest/'SHA256SUMS.json').write_bytes(json.dumps(manifest,ensure_ascii=False,indent=2).encode('utf8'));print(json.dumps(out,ensure_ascii=False))
