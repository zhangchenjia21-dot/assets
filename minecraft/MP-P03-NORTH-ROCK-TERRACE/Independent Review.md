# MP-P03 Independent Review｜minecraft-planner v0.3

日期：2026-09-14  
审核对象：`minecraft/MP-P03-NORTH-ROCK-TERRACE/`  
实现提交：`33684a9a214537fd46014bd2ece77c50c50c80f5`  
测试：`MP-P03｜北岩台集散候选 / SETTLEMENT`

## Verdict

> **PASS_WITH_NOTES — L2 SETTLEMENT 规划成立；国家→区域→聚落的递归链已经被实际验证。当前未发现需要再次修改 `minecraft-planner v0.3` 的 foundational SKILL_GAP。**

本轮已经不再停留于“节点 + 容量”层，而是形成了具有内部因果结构的完整聚落提案：西侧先卸载 / 修理，内台承担共享交割、保管与洁净接水关系，东上台形成更小的日常 / 寄宿簇。该结构由重货流、岩台高差、地表差异、共享治理、浅层空隙和常住供给条件共同约束，不是把三个功能标签平铺在场地上。

状态 `HANDOFF_READY` 只能按本案自己的限定解释为 **conditional planning handoff**。持续饮水仍未闭合，因此该状态不等于永久聚落可行、不等于 Owner 接受、更不等于 Builder-ready。

---

## 1. Positive Evidence

### 1.1 L2 读取了真正足以改变聚落形态的当前场地证据

本轮没有继续只依赖 R1 / Atlas 粗证据。Codex 在客户端退出、无 Java 进程时，只读复制 `level.dat` 和两个 Overworld region，通过现有 RegionReader 查询当前场地；读取前后源文件 SHA256 保持一致，`world writes = 0`。

这使 `Fabric Observation` 从上游 `UNVERIFIED` 提升为 `EXISTING_FABRIC_PARTIAL`，但没有误称“已完整调查现状”。这是正确的尺度深化。

### 1.2 Surface / Substrate v0.3 不再是装饰层

父候选本身以裸岩为主；本轮进一步调查 92,160 列当前表面，并把岩面、草土、砂砾、水、熔岩及少量其它表面带入内部布局。聚落没有因为岩台较平就连续铺满：北 / 南 / 东边缘被保留，草土小斑块没有自动城市化，砂砾带没有被自动解释成道路。

更重要的是，本轮把浅层状态继续向下读。8 格初查发现空气后，追加对核心 13,677 列逐柱向下 16 格复核，得到 603 个含浅层空气的列。初稿 `FRONTAGE-06` 被撤销，东侧前沿和背路缩短，`R03` 不再为了闭合图形跨到东台，`S04` 北边界也退让。

这说明：

> **surface / shallow substrate evidence materially changed morphology and capacity.**

不是“地图上多画一层紫色”。

### 1.3 聚落内部结构具有清晰因果，而不是现代 zoning

最终三个 District role：

- `D01 西接坡`：重货先卸载、修理、轮候，照看家庭就近嵌入；
- `D02 内台`：共享交接、保管、值守、洁净接收形成核心；
- `D03 东上台`：更远离入口牲畜干扰，承担较小的日常 / 寄宿混合簇。

这是 `flow + externality + terrain + shared-space governance` 生成的空间梯度。每个 District 仍允许混合生活 / 工作，不是住宅 / 商业 / 仓储三区切块。

### 1.4 Capacity 会被下层证据收敛，而不是机械继承父包上限

父包 NODE-01 的工作范围为约 `3,500–8,000 blocks²`；本轮在当前地表、浅层空隙、公共通行和共享空间约束后收敛为：

- 总建成压力 `3,500–4,600 blocks²`；
- `12–17` 户压力；
- 三个 District 分账为 `1,200–1,600 / 1,500–2,000 / 800–1,000 blocks²`。

District relation envelope 总几何面积约 5,688 blocks²，并未被冒充为建成面积。共享场院和本地通行已经包含在总压力内，没有重复加总。

### 1.5 对浅层空隙的处理保持规划纪律

最终全部 7 条有效 frontage、4 个 commons / service spaces 和 4 条 route relation 对已知浅层空气投影均为 `0 overlap`。`FRONTAGE-03` 仍有 6 个草土列，文件没有把它隐藏掉，而是明确留给 L3 核查 / 退让。

同时 Codex 没有把“空气层”称为地质危险的最终判定，也没有填洞、挖洞或生成地下室。它只把已知空隙作为当前规划避让证据。

### 1.6 Growth / Branch logic 比静态 masterplan 更成熟

本案不是默认聚落一定永久成立，而是明确三分支：

- `BRANCH-01`：供给 / 权属成立 → 采用 3.5k–4.6k、12–17 户条件形态；
- `BRANCH-02`：只支持短时交割 → 缩到约 400–1,000 blocks² 日间服务、常住 0，D02/D03 不保留空壳；
- `BRANCH-03`：接近 / 权属等不能兼容 → 停止定址并回报 `UPSTREAM_PLANNING_ISSUE`。

因此“未来没有形成永久聚落”仍是合法结果，不存在为了让测试通过而强行保城。

### 1.7 L2 → L3 recursive handoff 成立

三个下游包均是：

`SETTLEMENT → DISTRICT → recipient = minecraft-planner`

并保留：

- `upstream_fixed`；
- `downstream_to_resolve`；
- `downstream_adaptable`；
- cross-package dependencies；
- capacity hypothesis；
- revision triggers / upstream issue protocol；
- `world_write_authorization = false`；
- `builder_ready = false`。

上层固定的是交割顺序、共享空间、主要通行、浅层空隙避让和常住前提，而不是 parcel 宽度、房间、屋顶或 palette。Scale Discipline 合格。

---

## 2. Notes / Remaining Boundaries

### N1｜持续供水仍是本案最大 blocker，但暂不构成 Skill failure

场地周边观察到水列，但水质、持续水量、季节稳定性、到高台的供给方式均未证实。Codex没有用“附近有水”替代供水闭合，并把常住分支明确依赖于此。

独立审核接受 `conditional HANDOFF_READY` 的原因是：本轮交付给下一层的是**继续调查 / 规划的 District package**，不是建设包；且水失败时存在明确 BRANCH-02 / BRANCH-03 回退。

如果后续多轮频繁出现“关键生存条件未闭合但仍称 HANDOFF_READY”而造成误解，再考虑为 Skill 正式增加 `CONDITIONAL_HANDOFF_READY` 状态。当前一例不足以再扩状态机。

### N2｜当前道路 / 权属 / 历史 fabric 仍未真正恢复

本轮 `EXISTING_FABRIC_PARTIAL` 主要来自当前物理表面、浅层状态和 block entity 读取。它没有证明：

- 哪些线是历史道路；
- 哪些地属于谁；
- 是否已有住民聚落；
- 人工材料 / 地下对象的具体历史来源。

三个 L3 package 都要求先查这些问题，处理正确。后续 District Planner 不得把本轮 polygons 当空地新城边界。

### N3｜Route 是 settlement alignment proposal，不是已证道路

`ROUTE-01` 等已经有逐格地形 profile，但 `usable_route` 仍明确是 `UNVERIFIED_PHYSICAL_MOVEMENT`。这点必须保持到 L3 / implementation evidence 真正检查净空、转折、坡道与连续步行 / 驮运。

### N4｜Owner 视觉审核仍必要

本次独立审核能够核对规划逻辑、几何 / 证据数据、交接结构与生成图资产存在；但 Owner 仍应重点看 `maps/01-内部结构与地表.png`：三层空间是否直观像一座因岩台、货运和共享生活逐渐形成的山地聚落，而不是过于工程化的功能关系图。

---

## 3. Regression Classification

- Authority / Evidence discipline：**PASS**
- Planning Context：**PASS**
- Premise：**PASS_WITH_NOTE（permanent water supply conditional）**
- Surface / Substrate Necessity：**PASS**
- Terrain Necessity：**PASS**
- Demand / Flow / Externality：**PASS**
- Anchor / Historical Validity：**PASS**
- Anti-Zoning：**PASS**
- Settlement Capacity：**PASS**
- Settlement Morphology：**PASS**
- Scale Discipline：**PASS**
- L2→L3 Recursive Handoff：**PASS**
- Planner→Builder boundary：**PASS**
- World-write safety：**PASS**

Finding classification：当前仅 `TASK_SPECIFIC_JUDGMENT / EVIDENCE_LIMITATION` notes；**没有新的 foundational `SKILL_GAP`。**

---

## 4. Decision

> **MP-P03 accepted as regression PASS_WITH_NOTES.**

> **`minecraft-planner v0.3` 保持不变。**

> **允许进入 P04 / DISTRICT 回归测试。**

P04 推荐优先选择 `PACKAGE-01 / DISTRICT-01 西接坡交割与修理前沿`。原因是它在三种分支中最稳定：即使永久常住供水最终失败，西侧日间交割 / 修理角色仍最有可能以缩减形式存在，因此适合作为 L3 测试，不需要预先假定 D02 / D03 永久成立。

P04 应测试：

- inherited / existing fabric 如何进入 block / parcel / frontage；
- 卸载、修理、家庭小院、共享空地如何生成细粒度 morphology；
- 浅层空隙 / 岩面 / 草土如何影响地块与巷道；
- L3 是否能形成真正的 `URBAN_ENSEMBLE` 交接，而不提前设计建筑。
