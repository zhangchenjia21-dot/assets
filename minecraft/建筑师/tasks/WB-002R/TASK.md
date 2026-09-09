# WB-002R｜Southern Island Regional Reconnaissance

状态：**AUTHORIZED / DISPATCH READY**

Owner 授权日期：2026-09-09

授权决策：`../../decisions/D-008_WB-002R南部大岛区域精查授权.md`

目标：对 Current Natural Atlas 的南部大岛 `NGEO-009` 及其直接自然环境做一次**当前、只读、区域级高分辨率精查**，形成可长期被 GPT / Codex 查询的 **Regional Natural Profile**。

本任务是文明设计前置研究，不是 Civilization Design，不是 World Canon，不是 Architecture / Build。

---

# 0. 必读入口

执行前最小读取顺序：

1. `minecraft/建筑师/AGENTS.md`
2. `minecraft/建筑师/current/项目状态.md`
3. `minecraft/建筑师/current/世界构建原则.md`
4. `minecraft/建筑师/decisions/D-007_文明设定必须经过区域实地考察.md`
5. `minecraft/建筑师/decisions/D-008_WB-002R南部大岛区域精查授权.md`
6. `minecraft/建筑师/research/human-geography/southern-island/Owner实地考察_2026-09-09.md`
7. `minecraft/建筑师/architecture/地理事实层与空间ID契约.md`
8. `minecraft/建筑师/research/natural-geography/NG-3/tooling/查询与更新契约.md`
9. `minecraft/建筑师/research/natural-geography/NG-3/atlas/objects.jsonl` 中 `NGEO-009 / NFEAT-003 / NHYD-019`
10. `minecraft/建筑师/research/natural-geography/NG-2/assessments/SITE-003.json`
11. 本 Task Packet

V1 / NG-2 / NG-3 为 immutable accepted evidence。不得修改其 SQLite、JSON/JSONL、manifest、validation、script、review 或其它 artifact。

---

# 1. 研究问题

本任务必须客观回答：

1. 南部大岛当前真实 biome 构成是什么？
2. 岛内 elevation / relief / slope 如何分布？
3. 低起伏平地与缓坡实际集中在哪里、规模多大、是否连续？
4. Owner 观察的“总体西低东高”是否得到数据支持？支持强度如何？
5. Owner 所称“西侧两个岛屿 / 岛片”在真实水陆拓扑上究竟是什么：独立岛、半岛、陆桥连接片、低地分区，还是其它结构？
6. 岛内 / 周边水体、岸线和内部池塘的真实表层拓扑是什么？
7. 岛内是否存在 2～5 个自然条件显著不同、可长期作为 Human Geography 推导基础的**自然区域**？
8. Owner 的“三个潜在部族区域”假设得到怎样的自然地理支持：`SUPPORTED / PLAUSIBLE / WEAK / CONTRADICTED / INSUFFICIENT`？
9. “温带 / 枯树环境”“多山少平原”这些真人印象，哪些可以被 biome / vegetation / terrain 事实量化，哪些仍只能保留为视觉解释？

不得预设答案必须为三个分区。

---

# 2. 严格边界

## 2.1 Minecraft 世界只读

**world writes = 0**

禁止：

- 放置 / 删除 / 替换方块；
- 修改 region / chunk / NBT / entity / player / level.dat；
- WorldEdit 写入；
- 启动会保存世界的 Minecraft / Bridge / executor 来获取证据；
- 安装 / 升级 / 恢复 Observation 环境；
- 放置调查标志。

只能离线只读当前真实 world 数据。

读取期间必须使用不弱于 NG-2 / NG-3 的源文件保护与前后指纹核验。

## 2.2 不创造人文事实

禁止：

- 创建 CIV / species / tribe / nation / religion；
- 给自然区域起正式世界内地名；
- 把自然区直接叫“第一部族区 / 第二部族区”；
- 判断“适合精灵 / 矮人 / 人类 / 蒸汽族”；
- 规划城市、村落、城堡、神殿、道路；
- 推导人口容量、农业产能、矿产、港口、航运能力；
- 创建 Architecture Grammar 或 Blueprint。

本轮只产出自然条件和 Human Geography 可用的前置约束。

---

# 3. Current-world freshness gate

开始前重新核对当前 `建筑师` 存档。

至少记录：

- LevelName / DataVersion；
- 当前 Overworld region inventory；
- 与 Current Natural Atlas / NG-2 对应 source snapshot 的 relevant-region 差异；
- `regional_snapshot_status`：
  - `CURRENT_MATCH`
  - `REGION_CHANGED_SINCE_ATLAS`
  - `UNVERIFIABLE`

Owner 曾进入世界真人考察，因此不要假设 region hash 必然完全不变。

若相关 region 发生变化：

- 不要停止并猜测；
- 直接以**当前 world 的只读数据**作为本 Regional Profile 的事实源；
- 明确列出哪些 region 与旧 Atlas snapshot 不同；
- NG-3 继续作为历史 / 宏观 lineage，不得伪装为当前精确事实。

最终必须 seal 并证明本任务执行期间 world 未被本任务修改。

---

# 4. Study Area

主研究对象：

- `NGEO-009`
- `NFEAT-003`
- `NHYD-019`

NG-2 已验证岛体 bounds 约：

`X=-718..280, Z=1419..2518`

原 NG-2 source ROI：

`X=-800..415, Z=1376..2655`

本轮默认以该 source ROI 为**最小 study area**，保证包含岛体、外围水体和内部池塘。

若为了解释 Owner 所称“西侧两个岛屿 / 岛片”或自然分区，需要扩出 ROI：

- 允许每个方向最多再扩 256 blocks；
- 必须记录扩展原因；
- 不得无界扩扫整个世界。

---

# 5. 读取分辨率

本区域只有约百万级 columns，不应继续套用全世界 64-block 粗采样。

## 5.1 Terrain / water / biome 主层

默认目标：**1-block horizontal column coverage** 覆盖 study area，至少读取：

- filtered surface Y；
- raw top-surface / filtered-surface distinction；
- surface biome；
- land / surface-water mask；
- water interval / surface-water connectivity 所需信息；
- surface material category；
- source chunk / region provenance。

若某字段必须采用更低采样率，必须说明原因并明确标记 resolution。

## 5.2 Vegetation structural profile

为了验证 Owner 的“温带 / 枯树环境”印象，不要求复制整片 3D 世界，但必须形成足够的植被结构证据。

至少：

- biome composition；
- 在 4-block 或更细采样上统计 tree trunk / leaf canopy / major vegetation block categories；
- 记录 canopy / trunk density 的区域差异；
- 对“枯树 / dead-tree”只在 biome 名称、block palette 或实际结构明确支持时使用该语义，否则写成 `Owner visual interpretation`。

不得因树木 block palette 推导生态学物种事实。

---

# 6. Terrain metrics

形成整岛可查询 terrain metrics，至少包括：

- elevation min / median / quantiles / max；
- local slope / step；
- relief at useful windows（例如 16 / 32 / 64 blocks；可自行选择但必须说明）；
- ridge / highland / lowland proxy；
- coastline / inland-water adjacency；
- connected low-relief patches。

## 6.1 “平地”不要直接叫 buildable land

定义至少两级操作性地形类，例如：

- `LOW_RELIEF_FLAT`
- `GENTLE_SLOPE`

阈值必须公开、可查询、可重建。

输出其：

- connected component；
- area；
- bounds；
- elevation range；
- biome composition；
- edge / water contact；
- uncertainty。

这些只是自然地形形态，不得标记为 settlement suitability。

## 6.2 验证“西低东高”

不得只报东西两点。

至少使用：

- longitudinal elevation bands；
- median / quantile trend；
- 一个明确的整体相关 / regression 指标；
- 地图 / profile。

最终给出 `SUPPORTED / PARTIAL / NOT_SUPPORTED` 并解释局部反例。

---

# 7. Land / water topology

使用真实 1-block surface topology 区分：

- 主岛；
- 独立外围小岛；
- 半岛；
- 陆桥；
- 内部池塘 / 内水；
- narrow channels；
- shoreline。

重点审计 Owner 所称“西侧两个岛屿 / 岛片”：

> 不接受语言先验。必须由真实 4-neighbor surface land/water topology 判定它们究竟是什么。

允许结论为：Owner 视觉上形成两个独立空间，但拓扑上仍属于同一陆体。

不要推导：

- navigability；
- tidal behavior；
- upstream / downstream；
- natural harbor。

---

# 8. Regional Natural Zoning

这是本任务最重要的派生层。

目标是从真实自然条件识别**研究用自然分区**，而不是政治 / 部族区域。

至少综合：

- elevation；
- relief / slope；
- biome；
- major vegetation structure；
- water / shoreline barrier；
- low-relief patch distribution；
- land connectivity；
- obvious transition zones。

## 8.1 不强制 3 区

至少比较 2～5 区的合理性，或用其它可解释方法判断自然区数量。

最终自然分区可以是：

- 2 区；
- 3 区；
- 4～5 区；
- 或“没有足够清晰的离散分区，主要是连续梯度”。

研究 ID 使用例如：

`SIRZ-001...`

其中 `SIRZ = Southern Island Research Zone`。

这些 ID：

- 仅 Research；
- 不是 World Canon；
- 不是未来 REG / tribe / political ID。

每个 zone 必须记录：

- actual member geometry；
- natural characteristics；
- dominant biome；
- elevation / relief；
- flatland/gentle-slope share；
- water relationship；
- vegetation structure；
- boundary confidence；
- transition / overlap limitations。

---

# 9. Owner hypothesis evaluation

必须单独输出一份机器 + 人类可读的 hypothesis evaluation。

逐项检验：

1. `H-01 温带 / 枯树环境为主`
2. `H-02 多山少平原`
3. `H-03 总体西低东高`
4. `H-04 低起伏平地主要集中在西侧两个岛屿 / 岛片`
5. `H-05 可自然分成三个潜在部族区域`

每项 verdict：

- `SUPPORTED`
- `PARTIALLY_SUPPORTED`
- `NOT_SUPPORTED`
- `INSUFFICIENT`

必须区分：

- Owner observation；
- machine observation；
- derived metric；
- interpretation。

H-05 即使 `SUPPORTED`，也只能写：

> `three natural zones are a plausible Human Geography substrate`

不得直接升级成“三部族”。

---

# 10. Required Deliverables

成果统一放到：

`minecraft/建筑师/research/human-geography/southern-island/WB-002R/`

至少包含：

```text
README.md
raw-or-queryable/
  regional-profile.sqlite
profile/
  regional-summary.json
  biome-profile.json
  terrain-profile.json
  vegetation-profile.json
  water-topology.json
  low-relief-components.jsonl
  natural-zones.jsonl
  owner-hypothesis-evaluation.json
reports/
  区域自然画像.md
  Owner观察核验.md
visual/
  biome-map.png
  elevation-map.png
  relief-slope-map.png
  low-relief-map.png
  water-land-topology.png
  natural-zones-candidate.png
validation/
  automated.json
  source-audit.json
  rebuild.json
manifest/
  profile.json
  store.json
tooling/
  ...
```

文件名可在不降低清晰度的前提下合理调整。

## 10.1 Machine query layer

`regional-profile.sqlite` 是主要机器查询层。

至少支持未来回答：

- 一个坐标属于哪个 SIRZ；
- 该点 biome / elevation / slope / relief；
- 附近低起伏 patch；
- 附近水体 / 岸线关系；
- zone 的自然统计；
- Owner hypothesis evidence。

可以提供轻量 CLI，例如：

```text
coordinate x z
zone SIRZ-xxx
low-relief ...
context x z radius
```

不要把这做成服务或大型基础设施。

---

# 11. Validation

至少完成：

1. SQLite `integrity_check = ok`；
2. study area source chunk / region provenance 完整；
3. 至少 200 个独立 raw-column cross-check，覆盖：
   - 四角 / 边缘；
   - 高地；
   - 低地；
   - 水岸；
   - 内池塘；
   - Owner 关注的西侧区域；
4. land / water mask 拓扑 cross-check；
5. low-relief component member / bbox gap 检查；
6. SIRZ geometry 无 dangling / impossible overlap；
7. JSON/JSONL 与 SQLite 一致；
8. query layer 负坐标 / world-bound / error path；
9. deterministic rebuild：关键 SQLite / zone / profile exports 在固定输入下 byte-identical，或明确说明不能 byte-identical 的字段并把时间戳移出核心事实文件；
10. world source before / after inventory + hash / size / mtime 审计；
11. V1 / NG-2 / NG-3 immutable；
12. `world writes = 0`。

离线地图必须做人工目视自检，至少确认：

- 方向无翻转；
- 主岛与周边水陆关系合理；
- 高程图没有明显读取错误；
- natural zone candidate 与 terrain / biome / water evidence 大致对应。

Owner 已经提供真人游戏内考察，因此本任务**不要求为了补截图启动 Minecraft**。

---

# 12. Completion / stopping rule

完成后：

1. 写入：
   `minecraft/建筑师/tasks/WB-002R/COMPLETION.md`
2. 只可机械更新 `current/项目状态.md` 为：
   `WB-002R IMPLEMENTATION COMPLETED / AWAITING INDEPENDENT REVIEW`
3. 不得修改 World Canon 来分配任何 civilization / species；
4. 不得进入 AB-001 / Build；
5. commit + push 到 `zhangchenjia21-dot/assets/main`；
6. 保留其它并行项目提交；
7. 核对远端 HEAD；
8. 停止并交 GPT 独立审核。

任务完成后预期下一决策不是“开始建造”，而是：

> GPT + Owner 基于 Regional Natural Profile 提出并比较文明 / 部族候选。
