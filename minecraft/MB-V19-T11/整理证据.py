"""整理本轮实存对照和执行摘要；不读取其它测试资料、不复制存档。"""
from pathlib import Path
import json,hashlib,html,re,sys
import numpy as np
R=Path(__file__).resolve().parent;E=R/'证据'
last=sys.argv[1]
items=[]
for p in sorted(E.glob('*-执行.json')):
 d=json.loads(p.read_text(encoding='utf8'));log=Path(d['job_directory'])/'stdout.log';t=log.read_text(encoding='utf8',errors='replace') if log.exists() else ''
 # 仅保留本作业的保存结果及警告摘要，不复制运行时配置或凭据。
 lines=[l for l in t.splitlines() if ('Saving chunks for level' in l or 'All dimensions are saved' in l or '/WARN]' in l or '/ERROR]' in l)]
 items.append({'stage':p.name.removesuffix('-执行.json'),'world_path':d['world_path'],'changed_blocks':d.get('changed_blocks'),'save_completed':d.get('save_completed'),'shutdown_verified':d.get('shutdown_verified'),'native_mismatches':d.get('mismatches'),'block_entities_checked':d.get('block_entities_checked'),'log_excerpt':lines})
(E/'执行与日志摘要.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf8')
s=(R/'审计视图.py').read_text(encoding='utf8');a=s.index('views=[');b=s.index('def render',a);ns={};exec(s[a:b],{},ns);views=ns['views']
(E/'观察点.json').write_text(json.dumps([{'name':n,'eye':e,'target':t,'coordinate_system':'Minecraft X Y Z','kind':'saved voxel perspective, not client screenshot'} for n,e,t in views],ensure_ascii=False,indent=2),encoding='utf8')
parts=['<!doctype html><meta charset="utf-8"><title>T11 同机位空间审计</title><style>body{background:#eeeae1;color:#262c2c;font:16px sans-serif;margin:30px}section{margin:35px 0}.pair{display:flex;gap:12px}figure{margin:0;width:50%}img{width:100%}h1{font-size:26px}p{max-width:1050px;line-height:1.7}</style><h1>T11 京町家：精修前后同机位</h1><p>左：04-Base / SPATIAL_COMPLETE；右：'+last+'。全部来自保存关闭后的真实体素；非客户端截图。模型、纹理、光照及透明材质简化，不证明夜间照度、动态流体或真实移动碰撞。视点与目标坐标逐项列出，19 个视点不只选择局部陈设。各阶段原始采样、蓝图与核验另附。</p>']
for n,e,t in views:
 parts.append('<section><h2>'+html.escape(n)+'</h2><p>eye '+str(e)+' → '+str(t)+'</p><div class="pair">')
 for st in ['04-Base',last]:parts.append('<figure><img loading="lazy" src="证据/'+st+'-'+n+'.png"><figcaption>'+st+'</figcaption></figure>')
 parts.append('</div></section>')
parts.append('<h2>同位置平剖对照</h2>')
for n in ['纵剖X27','通庭剖X34','前店剖Z26','底层平面Y19','二层平面Y25']:
 parts.append('<section><h3>'+n+'</h3><div class="pair">')
 for st in ['04-Base',last]:parts.append('<figure><img src="证据/'+st+'-'+n+'.png"><figcaption>'+st+'</figcaption></figure>')
 parts.append('</div></section>')
(R/'同机位空间审计.html').write_text(''.join(parts),encoding='utf8')
skill=(R/'研究/技能原文-SKILL.md').read_bytes();blob=hashlib.sha1(b'blob '+str(len(skill)).encode()+b'\0'+skill).hexdigest()
assert blob=='5420c7cbbca25199e81ec1204dbc928b70abf73c'
(E/'Skill来源.json').write_text(json.dumps({'repo':'zhangchenjia21-dot/Vibe-Coding','path':'skill/codex/minecraft-builder/SKILL.md','version':'v1.9','git_blob':blob,'sha256':hashlib.sha256(skill).hexdigest(),'snapshot_unmodified':True},indent=2),encoding='utf8')
print('evidence index and exact Skill hash verified')
