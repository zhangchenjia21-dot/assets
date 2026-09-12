"""归档正式 REF 及现有 registry 的精确变更快照；不上传世界、runtime、账户或历史测试数据。"""
from pathlib import Path
import json,hashlib,zipfile,shutil,gzip,html
R=Path(__file__).resolve().parent;B=R.parent;L=B/'AI-Blueprints/references';D=L/'derived/REF-0123';A=B/'发布/assets/minecraft/建筑师/builds/T12正式资产入库'
A.mkdir(parents=True,exist_ok=True)
(A/'.gitattributes').write_text('* -text\n',encoding='utf8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
meta=json.loads((D/'metadata.json').read_text(encoding='utf8'));validation=json.loads((R/'最终资产验证.json').read_text(encoding='utf8'))
report='''# REF-0123 · T12 町家正式入库

状态：正式参考库注册完成，交 GPT 审核。world writes = 0；没有 Canon SITE 放置授权。

## 正式资产

- REF ID：`REF-0123`；名称：**江户后期京都呉服商町家院落**。
- 本机库：`D:/Games/Minecraft/AI工程/AI-Blueprints/references/derived/REF-0123/`。
- Canonical Blueprint：上述目录 `normalized/normalized-blueprint.json`，schema_version=1；原点 `(0,0,0)`。
- Litematic：`D:/Games/Minecraft/AI工程/AI-Blueprints/references/originals/REF-0123/京町家修复.litematic`。
- 实存包络（含端点）：`X11..39 / Y15..34 / Z16..89`；尺寸 **29×20×74（X×Y×Z）**。
- 两个 Region：GroundInterface 28×2×72，local `(1,0,1)`；MachiyaCompound 29×18×74，local `(0,2,0)`。
- 42,660 个明确格位（含空气），12,188 个非空气方块；方块需求逐状态见 `block-requirements.json`。
- anchor：local `(13,2,1)`；主入口 local `(13,3,2)`，对应实存 `(24,18,18)`，朝北（-Z）。地面行走标高 local Y2，室内抬高地板行走面 Y3。
- 现有 taxonomy：`building / mixed_use / japanese / east_asian / large`；附属用途 `shop / house / townhouse / warehouse / garden`。江户后期约 1840 年、京都呉服商宅作为描述 metadata 保存，未扩充词表。

## 来源与批准

唯一提取源：`D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V110-T12-京町家修复`。

已读取上游 `Asset Approval.md`，来源提交 `c3c246a`，批准文件 SHA256 见 metadata。批准覆盖 T12 最终修复状态，且 Owner 已实机检查。T11 设计资料仅用于界定地界/接口，没有从 T11、baseline 或中间蓝图提取任何正式方块。

隔离 T12 副本与归档 reload 完全相同。游戏副本相对归档有 6 格 Y15 草方块变泥土，均位于已支承台阶下；正式资产忠实保留游戏副本的实际状态。全部 47 格 Repair 与归档账本逐格一致。提取前后以及注册后对来源文件哈希核对一致，原 T11 和正式“建筑师”存档均未进入或写入。

## Scope 与复用

包含完整临街商宅、二层/楼梯、居住与服务空间、前后庭、后仓库、厕间、院墙、阈槛、台阶与直接地基。地界内低两层保留为整体 ground interface；上部保留完整出檐与必要明确空气。排除北侧测试街路延伸、外部超平坦背景，资产中无 QA 脚本/辅助结构。

适合狭长城市平地，北侧接街。应放置两个完整 Region，预备地基和净空，接街另作现场设计。目标主地面行走标高减 2 为蓝图最小 Y。不要过滤必要空气或单独省略地基 Region。本轮未旋转、重新设计或写入任何 Canon 场地。

## 验证

- 从最终来源逐格重读正式 Blueprint：0 差异；47 格 Repair 全保留；Scope 外明确格位 0。
- Canonical → Litematic → Canonical：42,660 个明确格位、空气语义、坐标、origin、dimensions 和完整 block states，0 unintended diff。
- Litematic 二次导出语义比较：0 unintended diff。
- 26.2 / DataVersion 4903 原生 Litematica 文件解析：两个 Region、12,188 非空气方块，完整状态 0 差异；原生探针未打开世界。Litematica 0.28.8 / MaLiLib 0.29.6。
- 现有负坐标/负 Size 多 Region 夹具 24 格、building-states 夹具 61 格原生回读一致。V6A 10 项互通语义测试通过（使用隔离证据目录）。首次直接运行旧测试有 3 项因历史证据目录拒绝覆盖而报 EPERM；随后只重定向测试输出，未改互通实现。
- V6C identity normalization：`CURRENT_NATIVE`，无需旧版本替换，状态变更 0。固定 122 项历史批处理不用于本次增量入库。
- stable REF 延续现有 path/hash 映射，原 122 条记录内容不变；既有 catalog、CSV、V2 catalog 与倒排索引已追加。L3 `resolve_reference_blueprint`、`query_references` 和 V2 `read_reference_classification` 均返回 REF-0123。
- preview 从正式 Blueprint 重新绘制，源和图片 SHA256 已绑定；不是旧版本截图。五个标准视图已实际检查，并保留内部/楼梯等额外视图与剖面。

## 已知限制

10 个空容器/炉方块实体的默认 NBT 未导出；方块及完整状态保留，检查确认没有物品、非空组件、燃烧/烹饪进度或配方记录丢失。此项为明确的管线限制；NBT diff 不声称为 0。后续部署必须遵守现有基础实体策略。

预览是简化方块形状/光照的离线渲染，不是 Minecraft 截图；原生文件解析不等于新场地实装验证。本轮不进入世界测试放置。42,660 明确格位符合 V5 50k 预览上限，但超过单次 20k 施工上限；未来施工应由现有离线批次拆分，不得跳过现场审核。参考库 `REFERENCE_ONLY` 与正式入库状态并存，Owner 入库批准不是世界写入批准。

## 交付文件

- `REF-0123/`：便于审阅的 metadata、Litematic、Blueprint、预览和验证记录。
- `资产库变更快照.zip`：本机现有 references 相对路径下全部新增文件及本次修改的 registry/索引的字节一致快照；是交付归档，不是第二套运行 registry。
- `资产库快照SHA256.json`：包内每个文件哈希；原有条目保护验证另见 `最终资产验证.json`。
- `复现脚本/`：本轮执行脚本；注册脚本仅适用于注册前状态，已注册会拒绝。不得盲目重跑或覆盖其它已入库资产。

恢复时先解压到临时目录并核对 SHA256；同一工程根下，只有确认没有后续 REF/registry 更新后才能恢复对应路径。不要将旧 registry 快照覆盖更新的资产库。当前本机已完成注册，不需要再次安装。完整世界与 runtime 不在交付中。
'''
(R/'Completion Report.md').write_text(report,encoding='utf8');(A/'Completion Report.md').write_text(report,encoding='utf8');(D/'analysis.md').write_text(report,encoding='utf8')
intro='''# REF-0123 · 江户后期京都呉服商町家院落

已按 Owner 批准正式入库；保留 REFERENCE_ONLY / 无世界施工授权。

本目录 normalized/normalized-blueprint.json 为当前默认表示，metadata.json 为放置、依赖及 provenance 契约，proxy/ 为该正式蓝图的代表性视图。

精确体量、验证与限制见 analysis.md。不要只放置上部 Region 或从 T11 替代本资产。
'''
(D/'README.md').write_text(intro,encoding='utf8')
readme=L/'README.md';old=readme.read_text(encoding='utf8');prefix='''# 当前参考库增量

2026-09-12：已追加 **REF-0123 · 江户后期京都呉服商町家院落**，现有 123 个稳定 REF。T12 最终实存、Owner 批准、26.2 原生互通验证与完整 metadata 见 [REF-0123](derived/REF-0123/README.md)。资产状态 REFERENCE_ONLY 表示未获任何新场地施工授权。

下文保留原 V6B 122 项历史批次报告，其统计不代表新增批次。新增条目走既有 catalog / V2 / index；不要重跑固定 122 项历史任务覆盖增量。

---

'''
if not old.startswith('# 当前参考库增量'):readme.write_text(prefix+old,encoding='utf8')
registry=json.loads((R/'注册结果.json').read_text(encoding='utf8'))['registry_files'];files=[L/p for p in registry]+[L/'README.md']+list(D.rglob('*'))+list((L/'originals/REF-0123').rglob('*'));files=[p for p in files if p.is_file()]
manifest={str(p.relative_to(B)).replace('\\','/'):sha(p) for p in files};save(A/'资产库快照SHA256.json',manifest)
with zipfile.ZipFile(A/'资产库变更快照.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in files:z.write(p,p.relative_to(B).as_posix())
with zipfile.ZipFile(A/'资产库变更快照.zip') as z:
 assert z.testzip() is None
 for name,digest in manifest.items():assert hashlib.sha256(z.read(name)).hexdigest()==digest
public=A/'REF-0123';public.mkdir(exist_ok=True)
for name in ['metadata.json','placement.json','preview-metadata.json','block-requirements.json','extraction-validation.json','native-validation.json','Asset Approval.md','analysis.md','README.md']:shutil.copy2(D/name,public/name)
shutil.copy2(D/'normalized/normalized-blueprint.json',public/'blueprint.json');shutil.copy2(L/'originals/REF-0123/京町家修复.litematic',public/'京町家修复.litematic');shutil.copytree(D/'proxy',public/'proxy',dirs_exist_ok=True)
for name in ['来源核对.json','提取验证.json','原生回读验证.json','最终资产验证.json','REF查询验证.json','V2查询验证.json','注册结果.json','互通回归结果.txt']:shutil.copy2(R/name,A/name)
scripts=A/'复现脚本';scripts.mkdir(exist_ok=True)
for p in R.iterdir():
 if p.suffix in ['.py','.mjs','.java','.ps1']:shutil.copy2(p,scripts/p.name)
with gzip.open(A/'原生回读明细.json.gz','wb') as f:f.write((R/'native-litematica-load.json').read_bytes())
items=list((public/'proxy').glob('*.png'));gallery='<!doctype html><meta charset="utf-8"><title>REF-0123 正式资产</title><style>body{background:#202425;color:#eee;font:16px sans-serif;margin:24px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(400px,1fr));gap:16px}img{width:100%;image-rendering:auto}figcaption{padding:8px}</style><h1>REF-0123 · 正式町家资产</h1><p>所有图像来自本轮正式 Blueprint；简化离线渲染，非客户端截图。来源与视图 hash 见 metadata。</p><main>'
for p in items:gallery+=f'<figure><img src="REF-0123/proxy/{html.escape(p.name)}"><figcaption>{html.escape(p.stem)}</figcaption></figure>'
gallery+='</main>'; (A/'preview.html').write_text(gallery,encoding='utf8')
save(A/'SHA256.json',{p.relative_to(A).as_posix():sha(p) for p in A.rglob('*') if p.is_file() and p.name!='SHA256.json'})
print(json.dumps({'archive':str(A),'files':len(list(A.rglob('*'))),'bytes':sum(p.stat().st_size for p in A.rglob('*') if p.is_file()),'zip_verified':True},ensure_ascii=False))
