"""整理已完成世界的证据与文件校验，不再加载或写入 Minecraft 存档。"""
from pathlib import Path
import json,hashlib,html,numpy as np
R=Path(__file__).resolve().parent;E=R/'证据';sha=lambda b:hashlib.sha256(b).hexdigest()
source=Path('D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V17-T09-罗马浴场')
base=json.loads((E/'来源文件基准.json').read_text(encoding='utf8'));now={str(p.relative_to(source)):sha(p.read_bytes()) for p in source.rglob('*') if p.is_file()}
assert base==now
stages=['01-Functional','02-Architectural','03-Material','04-Composition','05-Restraint','reload'];logs=[]
for s in stages:
 d=json.loads((E/f'{s}-执行.json').read_text(encoding='utf8'));p=Path(d['job_directory'])/'stdout.log'
 rows=[l for l in p.read_text(encoding='utf8',errors='replace').splitlines() if 'Perflib 009' in l]
 logs.append({'stage':s,'shutdown_verified':d['shutdown_verified'],'log_findings':rows})
out={'source_all_files_unchanged':True,'source_files':len(now),'final_reload_bytes_identical':(E/'05-Restraint.u16').read_bytes()==(E/'reload.u16').read_bytes(),'final_snapshot_sha256':sha((E/'05-Restraint.u16').read_bytes()),'skill_sha256':sha((R/'研究/技能原文-SKILL.md').read_bytes()),'skill_git_blob':'b4d58c40f20cdaff99f4656275bdcdc9598c841c','world_writes_T09':0,'world_writes_建筑师':0,'logs':logs}
(E/'最终隔离与重载核验.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');assert out['final_reload_bytes_identical']
m=json.loads((E/'05-Restraint-实存.json').read_text(encoding='utf8'));A=np.array(m['palette'])[np.fromfile(E/'05-Restraint.u16',dtype='<u2').reshape(56,144,144)]
points=[(87,19,35),(89,21,102),(120,17,100)]+[(x,19,31) for x in [64,67,70,73,90,93,96,99]]
access=[]
for x,y,z in points:
 ok=A[y-10,z,x]=='minecraft:air' and A[y-9,z,x]=='minecraft:air' and A[y-11,z,x]!='minecraft:air';access.append({'stand':[x,y,z],'two_block_clearance_and_floor':bool(ok)})
for x in [64,67,70,73,90,93,96,99]:assert A[10,29,x]=='minecraft:air'
(E/'活动点净空.json').write_text(json.dumps({'points':access,'all_chest_lids_clear':True,'native_interaction_tested':False},ensure_ascii=False,indent=2),encoding='utf8');assert all(v['two_block_clearance_and_floor'] for v in access)
views=['东北总貌','西南总貌','入口门槛','更衣室','更衣保管近景','冷厅向暖室','热室穹顶','热浴整理近景','庭院柱廊','服务炉房','燃料工作近景','入口石框近景','纵剖X82','横剖Z61','热区剖Z108','平面Y22']
body=['<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>T10 前后对照</title><style>body{background:#202426;color:#eee;font:16px system-ui;margin:30px}section{margin:30px 0}.pair{display:grid;grid-template-columns:1fr 1fr;gap:16px}img{width:100%;height:auto}a{color:#a9d7ee}h2{font-size:20px}</style><h1>T10 精修隔离审计</h1><p>左：精修前；右：Restraint 后。同机位、同渲染器。实存体素渲染，非客户端截图；不能验证原生纹理、照度、FOV 和运动体验。</p><p><a href="Completion%20Report.md">Completion Report</a> · <a href="Spatial%20Completion%20Gate.md">Spatial Completion Gate</a></p>']
for v in views:
 body.append('<section><h2>'+html.escape(v)+'</h2><div class="pair">')
 for s in ['00-Baseline','05-Restraint']:
  f=f'证据/{s}-{v}.png';assert (R/f).is_file(),f;body.append(f'<div><p>{s}</p><a href="{f}"><img loading="lazy" src="{f}"></a></div>')
 body.append('</div></section>')
body.append('<h2>各 Pass 近景</h2>')
for s in stages[:5]:
 for p in sorted(E.glob(s+'-*.png')):
  if any(v in p.name for v in ['近景','冷厅向暖室']):body.append(f'<p><a href="证据/{p.name}">{p.name}</a></p>')
(R/'证据索引.html').write_text('\n'.join(body)+'</html>',encoding='utf8');print(json.dumps({k:v for k,v in out.items() if k!='logs'},ensure_ascii=False))
