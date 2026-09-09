# WB-002R Completion

**PASS-CANDIDATE / READY FOR INDEPENDENT REVIEW**。实施完成，停止于 Research；等待 GPT 独立审核。

## 执行与交付

- Execution base：`77c6086b369176dcacb635946377a817b452de64`，执行开始时的 `assets/main`。
- 提交前正常 fast-forward 保留并行 `f1103fb38a81f027209660f50255bd331c1072c8`（T01 独立审核），不修改该项目。
- Final commit：承载本 Completion 的提交，主题 `WB-002R: publish current southern island reconnaissance`。精确 SHA 以 `git log -1 --format=%H -- minecraft/建筑师/tasks/WB-002R/COMPLETION.md` 解析，推送后交接消息提供并核对远端 HEAD；不预填尚未产生的自身 hash。
- Research 入口：[WB-002R README](../../research/human-geography/southern-island/WB-002R/README.md)。全部新证据在任务指定目录，另仅机械更新 current 状态。

## Current world 与 immutable evidence

LevelName 建筑师 / DataVersion 4903。最小 study ROI：X=-800..415，Z=1376..2655；扩展 **0 格**。12 个相关 region 中9个与 NG-2 / NG-3 source snapshot 的 hash 不同，故 `regional_snapshot_status=REGION_CHANGED_SINCE_ATLAS`。本画像直接读取当前世界，旧 Atlas 仅作为宏观/历史 lineage。

本任务有两个读取窗口。第一次受保护读取结束后，独立核验发现源又发生外部变化（例：r.-1.4.mca 的 hash、某叶方块 distance 属性改变）。已暂停，Owner 明确确认退出存档后，保留首轮快照并重新完整读取。禁止掩盖此事实：`world_unchanged_since_start=false`；刷新后的 current epoch 与最终 seal 一致，`world_unchanged_since_current_epoch=true`。V1 / NG-2 / NG-3 从最初基线至封口始终 immutable。

**world writes = 0**。只读窗口持全部现有 world/evidence 文件的 `GENERIC_READ / FILE_SHARE_READ` 句柄并核对完整 inventory/hash/size/mtime；未启动 Minecraft / Bridge / executor，未写 NBT、区块、玩家或实体，未安装 Observation 环境。窗口间外部 actor 未由本任务判定；原变化、两份基线与首轮压缩观测完整保留。

证据：[source-audit.json](../../research/human-geography/southern-island/WB-002R/validation/source-audit.json)、`manifest/source-before.json`、`current-source-before.json`、`epoch-transition.json`、`raw-or-queryable/first-epoch/`。刷新读取起点为 2026-09-09 09:48:31 UTC，最终 seal 时间见 audit。

## 机器层与主要结果

1,556,480 根真实 1-block 水平柱，6,080 source chunks，97,280 个 4-block 植被样点。保留 raw surface / filtered surface、两种 surface biome lookup、真实水区间、材料状态/类别、source chunk/region hash。Biome 为原生 4×4×4 单元逐柱查值，不伪称原生体素精度为1。

SQLite schema：`southern-island-profile/1.0`。主查询库 `regional-profile.sqlite`，原始观测 `observed.sqlite`；因主库超过 GitHub 单文件限制，发布可验证的无损 gzip。使用 `tooling/Bootstrap/区域归档命令.py restore` 恢复两个标准文件名。SHA256、尺寸、round-trip 和 integrity 均见 [store.json](../../research/human-geography/southern-island/WB-002R/manifest/store.json)，没有上传完整世界或 Mods。

指定主岛的当前实际干陆面积 **575,363 blocks²**，bounds [-718,1419,280,2518]。median Y66、p90 Y71、max Y79；少量洞口低至 Y14。操作性 LOW_RELIEF_FLAT **67.65%**，GENTLE_SLOPE **15.49%**；更严格 relief32≤2 阈值仍有 **54.13%**。这不是 buildable land / 农业或人口容量判断。

主要 biome 为 savanna 311,664 柱、arid_highlands 149,229 柱、beach 112,694 柱。主岛植被样点含叶率10.89%、含 log/wood 率0.80%；palette 不足以证明枯树占优或现实生态物种。

全 ROI：17 个干陆分量、64 个真实水区间连通分量。主岛内部52个水分量、1,207个水柱。C 形北、南翼是同一连通岛；中部似岛陆片通过陆颈连到另一个触东边界的陆体。两条实际干陆路径分别879/529柱，只作拓扑见证，不作角色通行或道路依据。东侧另一个陆体在 ROI 内 max Y168，完整范围受边界截断，不能与主岛混算。

东西趋势为温和正相关：Pearson r=0.3372、R²约0.114、OLS +0.491Y/100X；西/东半部 median Y65/Y67，有局部反例。经度带与分位数全部保存。

## 分区与 Owner 五项假说

比较 k=2～5 的数值候选，综合地形、biome、植被、水陆阻隔和平缓面积，随后独立作模型解释。候选主要是岸线、南侧稍高地与植被/biome主题差异，碎片多、边界随 k 改变；本轮选择 Task 允许的“没有足够清晰的离散分区、主要是连续梯度”。

因此保存 **1 个 SIRZ-001 研究参考单元，0 个已建立的离散内部自然区界**。SIRZ 是当前主岛实际成员，不代表均质条件，不是 REG / tribe / political ID。2～5 候选图与指标全部保留供审核，没有为了满足“三个区域”预设而强切。

| 假说 | Verdict |
|---|---|
| H-01 温带 / 枯树环境 | PARTIALLY_SUPPORTED：非高密雨林/稀疏冠层有支持，温带与枯树占优未建立 |
| H-02 多山少平原 | NOT_SUPPORTED：对指定主岛；不能外推到东侧较大陆体 |
| H-03 西低东高 | PARTIALLY_SUPPORTED；地形趋势枚举为 PARTIAL |
| H-04 西侧两个岛片集中平地 | PARTIALLY_SUPPORTED：西半更平缓，独立两岛表述不成立，Owner具体参照未定位 |
| H-05 三个潜在部族区域 | NOT_SUPPORTED；自然 substrate 支持为 WEAK，不建立部族 |

机器 evaluation 与两份中文报告区分 Owner observation、machine observation、derived metric 和 interpretation。Owner 未给出具体视点，研究范围与其更广空间感受可能不一致，此限制必须进入独立审核。

## 验证

- **311** 个独立 scalar NBT raw-column cross-check 通过，覆盖边缘/四角、低地、起伏区、水岸、小内水、西侧与植被格点；独立反扫 raw top 并核对 material properties / biome / water interval，不调用生产向量解码器。
- 独立 union-find 对全 ROI 干陆/实际水区间图复算，与生产 BFS 分量双射一致。
- SQLite integrity、完整 source provenance、全部实际 RLE 成员重建、94 个有 bbox gap 的 flat patches、SIRZ 无重叠/悬空、JSON/JSONL 与 SQLite、负坐标/ROI外/error path、五类查询 CLI 的 `python -S` 确定性均通过。细目见 `validation/automated.json`，其断言数含逐run检查，不是独立测试案例数。
- 固定 observed 输入完整 derive + relations + build 后，核心 SQLite 与所有 profile JSON/JSONL byte-identical；运行时间不进入可变核心结果。
- 原始/主查询库和首轮旧快照 gzip 均通过 SHA256 / lossless round-trip / integrity。
- 离线图逐张目视自检：方向、岛片/水域关系、东侧高地与低岛对照、分区候选和图例对应合理；图不是事实源。不为截图启动游戏。
- 四层向下依赖/语法检查通过；L0 领域阈值、L1 解码/保护/指标/查询、L2 用例、L3 公开边界，Bootstrap/tests 为外围。历史代码只作为独立版本来源，没有修改或 import NG-2/NG-3 内层。

## 停止点

没有创建文明、种族、部族、国家、宗教或政治边界，没有进入 Architecture Bible / Build；没有从平地、水体或高地推导农业、人口、矿产、港口或航运。未修改 World Canon、原 Task Packet 或历史 evidence。

下一步仅交 GPT 独立审核，重点复核对象范围、连续梯度解释与 Owner 视点对应。任何进一步区域扩扫或人文候选均需后续决策，不由本 Completion 授权。
