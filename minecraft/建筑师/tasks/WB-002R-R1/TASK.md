# WB-002R-R1｜Southern Island Group Scope Completion

状态：**AUTHORIZED / DISPATCH READY**

授权决策：`../../decisions/D-009_WB-002R-R1南部岛屿群范围补全授权.md`

前序独立审核：`../../research/human-geography/southern-island/WB-002R/独立审核.md`

## 0. 任务定位

本任务是 WB-002R 的**范围补全修正**，不是全新文明设计任务。

WB-002R 已经对西侧低海拔 `NGEO-009` 区域形成可信的 1-block evidence，但其固定 ROI 没有完整覆盖 Owner 真人考察语境中的右侧更大山地陆体，因此整片“南部岛屿群”仍未形成完整 Regional Natural Profile。

本轮目标：

> **保留可复用的 west / low-island evidence，补齐 east / mountainous landmass，并统一重建整个南部岛屿群的区域自然画像。**

不创建文明，不进入 Architecture / Build。

---

# 1. 必读

执行前至少读取：

1. `minecraft/建筑师/AGENTS.md`
2. `minecraft/建筑师/current/项目状态.md`
3. `minecraft/建筑师/current/世界构建原则.md`
4. `minecraft/建筑师/decisions/D-007_文明设定必须经过区域实地考察.md`
5. `minecraft/建筑师/decisions/D-009_WB-002R-R1南部岛屿群范围补全授权.md`
6. `minecraft/建筑师/tasks/WB-002R/TASK.md`
7. `minecraft/建筑师/tasks/WB-002R/COMPLETION.md`
8. `minecraft/建筑师/research/human-geography/southern-island/WB-002R/README.md`
9. `minecraft/建筑师/research/human-geography/southern-island/WB-002R/独立审核.md`
10. `minecraft/建筑师/research/human-geography/southern-island/Owner实地考察_2026-09-09.md`
11. 本 Task Packet

V1 / NG-2 / NG-3 / WB-002R 已有交付全部 immutable。

---

# 2. 已知范围缺口

WB-002R 使用：

`X=-800..415, Z=1376..2655`

扩展 0 格。

其结果已经证明：

- 西侧低岛 `NGEO-009` 完整落在 ROI 内；
- ROI 东侧存在另一主要干陆体；
- 该东侧陆体局部最高达到约 Y168；
- 它触碰 east study boundary；
- 完整范围没有建立。

因此当前 R1 必须把这个 east-boundary land component 作为首要 scope-completion target。

---

# 3. Hard Scope Gate｜不得再次截断主要东部陆体

## 3.1 Adaptive expansion

以 WB-002R ROI 为起点，读取当前世界并识别所有触碰 study boundary 的主要 land component。

重点追踪东侧山地陆体。

扩展建议使用 256 或 512 block tile / band 逐轮推进，可根据 I/O 效率自行实现。

每轮扩展后重新判断：

- relevant land component 是否仍触碰 study boundary；
- 是否已经被 surface water 完整包围；
- 是否实际通过 land neck / broad connection 连向更大陆地；
- 是否触达当前 pregenerated full-world boundary。

## 3.2 Completion hard gate

最终不得同时满足：

> `east_mountain_landmass_touches_study_boundary = true`

且仍宣布 `scope_complete=true`。

必须得到以下之一：

### `CLOSED_WITHIN_STUDY`
相关山地陆体的表层水陆边界在 study area 内闭合，可判定其真实岛 / 半岛 / 其它拓扑身份。

### `CONNECTED_TO_LARGER_LAND`
证明该山地陆体继续连接到明显更大的陆地，不应被称为独立岛；此时无需无限追踪整个大陆，但必须划定一个足够覆盖 Owner 考察区域的 eastern mountain sector，并明确完整陆体范围不是本轮目标。

### `CENSORED_AT_WORLD_OR_SAFETY_BOUND`
到达 pregenerated world edge 或合理安全上限仍无法闭合。必须说明未闭合原因、当前范围和不能回答的问题。

禁止再次出现“明显被东边界截断，但仍按完整南部区域给最终自然分区结论”。

## 3.3 Bounded safety

默认允许从旧 ROI 自适应扩大到每方向额外约 2048 blocks 的量级；若更早闭合应立即停止，不为消灭所有未知继续扫。

如果 2048 仍不足，先判断是否实际上连接到大陆 / 大型连续陆体；不要机械继续数千格无限扩扫。

如确有证据表明只差少量范围即可闭合，可以合理超过默认值，但必须在 Completion 解释。

---

# 4. Current-world freshness / evidence reuse

Owner 和其它任务可能在两轮之间进入 Minecraft，不能假设 WB-002R west evidence 自动等于当前世界。

开始前：

1. 对所有 R1 relevant region 做 current freshness audit；
2. 将当前 region hash 与 WB-002R current-epoch snapshot 比较；
3. 对未变化的 west area，可以直接复用 WB-002R observed evidence；
4. 对已变化 region，只重读受影响范围；
5. 新扩展的 east area 必须从当前 world 只读读取；
6. 最终统一 profile 必须绑定一个明确 current epoch。

目标是**增量复用，不是无意义重扫，也不是混合不同 epoch 而不标注**。

`world writes = 0`。

读取与 seal 的保护不弱于 WB-002R。

---

# 5. Resolution

新增 / refresh 区域继续优先使用：

- 1-block horizontal terrain / biome / land-water coverage；
- 真实 surface-water interval / topology；
- provenance 到 chunk / region；
- 4-block 或更细 vegetation structural sampling。

如果新范围显著扩大导致某非关键派生层需要降低采样率，可以合理调整，但：

- land/water topology 不得因此退化为 64-block Atlas 猜测；
- terrain / biome 基础层应尽量保持与 WB-002R 可比较；
- resolution 必须字段化。

---

# 6. Unified Regional Profile

R1 必须重新建立一个针对**完整研究范围**的统一 profile，而不是只附一份 east supplement。

至少回答：

1. full study extent / scope status；
2. 主要 land components 及其真实拓扑身份；
3. west lowland group 与 east mountain landmass 的关系；
4. biome composition / spatial distribution；
5. elevation / slope / relief；
6. low-relief / gentle-slope components；
7. shoreline / internal water；
8. vegetation structural differences；
9. west-east terrain gradient；
10. 2～5 natural-zone candidates 或 continuous-gradient conclusion。

## 6.1 不预设“两个岛”或“三个区域”

Owner 的描述是观察入口，不是答案。

特别验证：

- “左侧两个平原低地岛”在真实 topology 上究竟是两个独立岛、同一 C 形岛的两翼、岛 + 半岛、还是其它结构；
- “右侧山地岛”究竟是不是独立岛；
- “三个部族区域”的视觉感是否对应 3 个明显自然区，或只是 west-low / east-high + transition 的连续结构。

---

# 7. Re-evaluate Owner hypotheses at correct scope

必须重新评估：

- `H-01 温带 / 枯树环境为主`
- `H-02 多山少平原`
- `H-03 总体西低东高`
- `H-04 平原主要集中在西侧两个岛屿 / 岛片`
- `H-05 可自然分成三个潜在部族区域`

旧 WB-002R verdict 必须保留为 predecessor/local verdict，但新的 whole-scope verdict 独立输出。

每项必须同时注明：

- scope；
- Owner observation；
- machine observation；
- derived evidence；
- interpretation；
- verdict。

H-05 即使获得支持，也只能说明 natural substrate，不得创建 tribe / political region。

---

# 8. Natural Zones

研究 ID 继续使用 Research-only namespace，可选择：

`SIRZ-R1-001...`

或设计清晰的 successor lineage。

每个 zone 必须有：

- actual member geometry；
- biome；
- elevation / slope / relief；
- flatland share；
- vegetation structure；
- water relation；
- boundary confidence；
- predecessor relation（如涉及 WB-002R SIRZ-001）；
- `NOT_WORLD_CANON`。

禁止为了贴合 Owner “三个部族区域”而强制 k=3。

---

# 9. Required Deliverables

统一放到：

`minecraft/建筑师/research/human-geography/southern-island/WB-002R-R1/`

至少包含：

```text
README.md
raw-or-queryable/
profile/
  scope-completion.json
  land-components.json
  regional-summary.json
  biome-profile.json
  terrain-profile.json
  vegetation-profile.json
  water-topology.json
  low-relief-components.jsonl
  natural-zones.jsonl
  owner-hypothesis-evaluation.json
reports/
  南部岛屿群完整区域画像.md
  WB-002R范围修正说明.md
visual/
  full-biome-map.png
  full-elevation-map.png
  full-relief-slope-map.png
  full-low-relief-map.png
  full-water-land-topology.png
  full-natural-zones-candidate.png
validation/
manifest/
tooling/
```

可以合理调整文件名，但不能降低机器可查询性。

主查询层必须能够查询 west + east 的统一当前 profile。

---

# 10. Validation

至少验证：

- source freshness / current epoch；
- task execution期间 source unchanged；
- `world writes = 0`；
- predecessor WB-002R immutable；
- current affected west regions refresh / reuse 正确；
- east expansion raw-column crosschecks；
- land/water topology independent crosscheck；
- query store integrity；
- deterministic rebuild / export；
- 无 dangling zone / component refs；
- **scope completion hard gate**；
- whole-scope H-01～H-05 verdict 与机器事实绑定。

地图需要人工离线目视检查，但仍不为补截图启动会写存档的游戏环境。

---

# 11. Strict prohibitions

本轮不得：

- 创建文明 / 种族 / 部族 / 国家 / 宗教；
- 把 SIRZ 写成部族边界；
- 推导矿产、农业产能、人口容量；
- 推导航运、港口、上下游；
- 创建 Architecture Grammar；
- 规划建筑 / 聚落；
- world write；
- 修改 WB-002R predecessor evidence；
- 修改 V1 / NG-2 / NG-3。

---

# 12. Completion / Stop

完成后：

- `minecraft/建筑师/tasks/WB-002R-R1/COMPLETION.md`
- `minecraft/建筑师/research/human-geography/southern-island/WB-002R-R1/`
- 仅机械更新 current 状态为 implementation completed / awaiting review；
- commit + push `assets/main`；
- 保留并行提交；
- 核对远端 HEAD；
- 停止交 GPT 独立审核。

R1 完成不自动授权 CIV-001、Architecture Bible 或 Build。
