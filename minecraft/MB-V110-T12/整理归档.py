"""整理本轮审计与归档；不上传存档、资格验证副本、Mods、配置或玩家文件索引。"""
from pathlib import Path
import json,hashlib,shutil,zipfile,html
from PIL import Image
R=Path(__file__).resolve().parent;E=R/'证据';root=Path('D:/Games/Minecraft/AI工程/发布/assets').resolve();D=(root/'minecraft/MB-V110-T12').resolve();assert D.is_relative_to(root)
src=(R/'审计视图.py').read_text(encoding='utf8');v={};exec(src[src.index('views=['):src.index('def render')],{},v);views=v['views']
(E/'观察点.json').write_text(json.dumps([{'name':n,'eye':e,'target':t} for n,e,t in views],ensure_ascii=False,indent=2),encoding='utf8')
parts=['<!doctype html><meta charset="utf-8"><title>T12 物理修复证据</title><style>body{background:#f5f1e8;color:#26302d;font:16px sans-serif;margin:28px}p{line-height:1.7}section{margin:35px 0}.pair{display:flex;gap:12px}figure{width:50%;margin:0}img{width:100%}</style><h1>T12 自主物理完整性 Repair</h1><p>左 baseline，右 01-Repair。物理 Gate 最终 UNVERIFIED：已发现的静态失败消除，真实玩家移动未验证。所有透视来自实存体素，剖面来自原生静态碰撞形状；均非客户端截图。红框保持同位置，供比较原缺口/身体包络。先看五组物理剖面，再看完整25组同机位。</p>']
for name in ['东墙支承','入口台阶','仓库入口','楼梯中线','楼梯西侧']:
 parts.append('<section><h2>'+name+'</h2><div class="pair">')
 for s in ['baseline','01-Repair']:parts.append('<figure><img src="证据/'+s+'-剖面-'+name+'.png"><figcaption>'+s+'</figcaption></figure>')
 parts.append('</div></section>')
for n,e,t in views:
 parts.append('<section><h2>'+html.escape(n)+'</h2><p>眼位 '+str(e)+' → '+str(t)+'</p><div class="pair">')
 for s in ['baseline','01-Repair']:
  assert (E/f'{s}-{n}.png').exists();parts.append('<figure><img loading="lazy" src="证据/'+s+'-'+n+'.png"><figcaption>'+s+'</figcaption></figure>')
 parts.append('</div></section>')
(R/'同机位物理审计.html').write_text(''.join(parts),encoding='utf8')
logs=[]
for p in E.glob('*-执行.json'):
 d=json.loads(p.read_text(encoding='utf8'));f=Path(d['job_directory'])/'stdout.log';t=f.read_text(encoding='utf8',errors='replace')
 lines=[x for x in t.splitlines() if 'Saving chunks for level' in x or 'All dimensions are saved' in x or '/ERROR]' in x]
 logs.append({'stage':p.stem,'world_path':d['world_path'],'changed_blocks':d.get('changed_blocks'),'save_completed':d.get('save_completed'),'shutdown_verified':d.get('shutdown_verified'),'excerpt':lines})
(E/'执行日志摘要.json').write_text(json.dumps(logs,ensure_ascii=False,indent=2),encoding='utf8')
D.mkdir(parents=True,exist_ok=True)
files=[p for p in R.iterdir() if p.suffix in ['.md','.py','.mjs','.java','.html'] or p.name=='.gitattributes']+list((R/'研究').glob('*.md'))+[p for p in E.iterdir() if p.suffix in ['.json','.png'] and p.name!='来源世界文件哈希.json']
for p in files:
 q=D/p.relative_to(R);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);assert p.read_bytes()==q.read_bytes()
packed=list((R/'蓝图').rglob('*.json'))+list(R.glob('*.npz'))+list(E.glob('*.u16'))
with zipfile.ZipFile(D/'修复蓝图与实存.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in packed:z.write(p,str(p.relative_to(R)))
with zipfile.ZipFile(D/'修复蓝图与实存.zip') as z:
 assert z.testzip() is None
 for p in packed:assert z.read(str(p.relative_to(R)).replace('\\','/'))==p.read_bytes()
manifest={str(p.relative_to(D)).replace('\\','/'):{'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(D.rglob('*')) if p.is_file() and p.name!='SHA256.json'}
for p in D.rglob('*.png'):
 with Image.open(p) as im:im.verify()
(D/'SHA256.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8');print('archived files',len(manifest)+1,'ZIP members',len(packed),'paired views',len(views))
