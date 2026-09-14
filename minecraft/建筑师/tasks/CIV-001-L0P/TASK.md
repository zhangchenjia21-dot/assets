# CIV-001-L0P｜CIV-001 Three-Domain Alliance L0 Polity/Territory Recompile

状态：**AUTHORIZED / DISPATCH READY**

日期：2026-09-14

## 0. 任务定位

这是 `minecraft-planner v0.5` 在正式 `建筑师` 项目中的第一次 L0 应用。

目标：

> **从已接受的世界事实、CIV-001 Canon、Owner 人工领土与 D-025 空间方向出发，独立重新推导 CIV-001 三域联盟在 `L0 POLITY_TERRITORY` 尺度上的因果空间结构，并生成向 L1 递归的 Planning Packages。**

本任务不是 Middle 总规，不设计城市、街区、地块或建筑。

`world writes = 0`。

---

## 1. Skill / Contract Baseline

必须使用稳定基线：

- `minecraft-planner v0.5`
- `minecraft-builder v1.11`（未来 recipient；本轮不执行 Builder）
- `Minecraft Planner–Builder Contract v1.0`

先读取：

- `Vibe-Coding/skill/codex/minecraft-planner/SKILL.md`
- `Vibe-Coding/skill/codex/minecraft-planner/references/recursive-planning-handoff.md`
- Planner 在执行中实际要求的其它 references
- `Vibe-Coding/skill/codex/shared/minecraft-planner-builder-contract.md` 仅用于理解后续接口边界
- `Vibe-Coding/skill/codex/REGRESSION-BASELINE.md`

稳定源基线以 regression record 所列 `fc6371361685e2eeaefdef5a513f21dbe64c6696` 为准。

---

## 2. Authority Baseline｜必须先读

先读：

`minecraft/建筑师/tasks/CIV-001-L0P/AUTHORITY-MATRIX.md`

该文件是本任务 Authority / Anti-Anchoring 的直接控制面。

然后读取高权威输入：

1. `minecraft/建筑师/current/项目状态.md`
2. `minecraft/建筑师/decisions/D-030_启用MinecraftPlanner并从CIV-001联盟L0重新编译.md`
3. `minecraft/建筑师/world/civilizations/CIV-001/README.md`
4. Authority Matrix 列出的相关 Canon decisions
5. `D-025_三域聚落密度与土地利用梯度.md`
6. accepted Natural / Human Geography evidence
7. revision154 territory geometry

### Input Firewall

在 **Primary L0 solution freeze** 前：

**禁止读取** Authority Matrix C 类列出的旧 Middle / G1 / MD-001S1 / MD-001U1 / Middle Kit v0.1 下游成果。

不要用 Git search 无意命中这些旧结果作为推导依据。

---

## 3. Project-specific Planning Context｜必须正确理解

CIV-001 是一个**历史上已经成熟存在的前现代文明 / 联盟**，不是新殖民绿地项目。

同时，Minecraft 当前正式世界中的许多可见人造聚落尚未被实际建入存档。

因此必须明确区分：

```text
Fictional / historical evolution = EXISTING_EVOLUTION
Minecraft visible built-fabric implementation = largely not yet implemented
```

**不要因为当前存档中没有城市方块，就把 CIV-001 历史写成 GREENFIELD_FORMATION。**

也不要伪造当前世界已经存在未观察到的建筑方块。

采用 D-013 的可见世界 / 隐性设定原则：

- 历史、制度、长期关系等可在 Canon / Planner 层形成；
- 可见建筑、道路、工程未来由 Builder / world-write 真实实现；
- 规划层必须标清 fictional-history / current-save observation 的差异。

---

## 4. L0 Scope｜本轮真正要解决什么

Planner 必须在 `POLITY_TERRITORY` 尺度回答：

### 4.1 Territorial / Political System

- 三域为何在这种地理条件下形成一个联盟而非单一王国或完全分裂体系；
- 三席议会与强地方自治如何影响空间网络；
- Alliance Commons 在整个联盟权力地理中的角色；
- West / Middle / East 的权利、自治与共同治理关系在空间上有哪些后果；
- 哪些联盟级公共工程 / 规则需要跨域合作。

不重新划领土。

### 4.2 Actors / Rights / Capability

仅在 materially consequential 时建立：

- West towns / estates / market powers；
- Middle transfer / trade / foothill communities；
- East clans / mountain communities；
- Three-seat Council / alliance-level institutions；
- relevant merchants / producers / travelers / military / ritual institutions；
- access / commons / local autonomy / cooperation / veto relations。

回答：谁想推动、谁有权、谁承担成本、谁可能抵抗、什么能力使其成为可能。

### 4.3 Flows / Stocks / Rhythms / Externalities

至少重新推导并区分：

- food / livestock / ordinary goods；
- ore / metal / stone；
- timber / fuel only where evidence / Canon supports planning relevance；
- trade / merchants / travelers；
- authority / dispute resolution / alliance ritual；
- defense / mobilization；
- seasonal / buffer / storage dependencies where consequential。

不要把 broad Canon 方向误写成现代统一供应链或完全垄断。

### 4.4 Settlement Hierarchy｜粗粒度

推导联盟级需要哪些**角色类别和层级**，例如但不限于：

- alliance political center；
- regional centers；
- gateways / transfer nodes；
- production / market centers；
- mountain / mining / clan nodes；
- secondary towns / villages / hamlets；
- frontier / crossing / strategic nodes。

**不要默认旧 N1 / G1 等节点存在。**

如果 L0 能确定的是 role + search logic，而不能确定 exact site，这是正确结果。

### 4.5 Major Movement / Access Skeleton

推导：

- 跨岛 / 跨域主要交换关系；
- major land / water / pass / crossing search relations；
- chokepoints；
- physical access 与 political / tenure / security / seasonal access 的区别；
- 哪些 route 只是 search corridor / required relation，而不是 existing road。

不得把 WB-003R proxy path 改称现成道路。

### 4.6 Capacity / Built-fabric Scale

为重要区域角色 / settlement role 给出**粗粒度 capacity hypothesis / scale class**，而不是精确人口或精确占地。

必须把：

- location search envelope / logic；
- built-fabric capacity hypothesis；
- functional hinterland / catchment；

分开。

### 4.7 Causal Growth / Path Dependence

仅在解释现有 polity structure 有必要时，提出联盟级历史阶段 / path dependence：

例如：

- 哪些交换 / 防御 /制度关系可能先于联盟正式成立；
- 三席议会为何成为稳定制度；
- Commons 为什么成为共同政治中心；
- 哪些 major route / regional specialization 是因何逐步固化。

这是**联盟尺度因果历史**，不是给每个村庄写年表。

### 4.8 Resilience / Failure Dependencies

当后果重大时，识别：

- 单一 crossing / route / supply dependency；
- food / ore / authority network 的脆弱点；
- 需要 fallback / buffer 的关系。

不要求数值模拟。

---

## 5. Owner Constraints｜不得遗漏

必须显式保持：

```text
Middle territory-wide average built / settlement density > West > East
Middle land-use / spatial intensity highest
West large agrarian-pastoral productive landscape strongest
East settlement distribution most dispersed across territory
East terrain adaptation / terrain engineering strongest
```

注意：这是**territory-wide morphology**，不是每个局部统一密度。

Planner 必须解释这一梯度如何从：

- 地形；
- broad economic role；
- access / transfer；
- land pressure；
- social organization；

共同成立，而不是仅把 D-025 复述一遍。

---

## 6. 禁止事项｜Scale Discipline

本轮禁止：

- 重做 revision154；
- 修改 Alliance Commons 边界；
- 直接恢复旧 P1–P5 / N1–N4 / G1；
- 画 town street grid；
- 定 district / parcel；
- 精确决定一栋建筑在哪里；
- 设计 Council Hall；
- 生成 exact Architecture Kit；
- 生成 block palette；
- 调用 Builder 继续 Architecture Design；
- world-write；
- broad rescan。

L0 可以输出“Middle 需要一个或多个 transfer gateway / regional center”等 role / relation，但 exact settlement morphology 留给 L1/L2。

---

## 7. Expected Primary Outputs

输出目录：

`minecraft/建筑师/planning/CIV-001/POLITY/CIV-001-L0P/`

至少包含：

### Core

- `README.md`
- `L0-POLITY-PLAN.md`
- `L0-POLITY-PLAN.json`
- `AUTHORITY-TRACE.md`
- `ACTORS-RIGHTS.md`
- `FLOWS-SYSTEM.md`
- `flows-system.json`
- `SETTLEMENT-HIERARCHY.md`
- `settlement-hierarchy.json`
- `MOVEMENT-ACCESS-SKELETON.md`
- `movement-access-skeleton.json`
- `CAPACITY-SCALE.md`
- `capacity-scale.json`
- `GROWTH-PATH-DEPENDENCE.md`
- `RESILIENCE-DEPENDENCIES.md`

### Visual

至少输出可审核的等比例 / 可追踪地图：

- `visual/01-territory-terrain-context.png`
- `visual/02-polity-regional-roles.png`
- `visual/03-major-flows.png`
- `visual/04-settlement-hierarchy-search-logic.png`
- `visual/05-movement-access-skeleton.png`

图上必须区分：

- accepted boundary；
- observed / derived terrain；
- Canon role；
- proposed search relation；
- existing-vs-proposed / observed-vs-authored。

不要用圆点图伪装 exact settlement sites。

### Recursive Planner Handoff

目录：

`handoff/`

至少生成：

- `L1-WEST.md/json`
- `L1-MIDDLE.md/json`
- `L1-EAST.md/json`

每个 package 按 `recursive-planning-handoff.md` 包含：

- Package ID / parent revision / scale；
- WHY / regional role；
- search geometry / territory ref；
- upstream anchors / flows；
- `UPSTREAM_FIXED`；
- `DOWNSTREAM_TO_RESOLVE`；
- `DOWNSTREAM_ADAPTABLE`；
- capacity hypothesis；
- Actor / rights / access / mitigation / stock / resilience dependencies where consequential；
- revision triggers；
- expected L1 outputs；
- `world_write_authorization = false`。

### Alliance Commons Handoff Decision

必须明确判断：

> Alliance Commons 应当在递归结构中作为怎样的下游 planning object？

可以是：

- 独立 special institutional/common-territory package；
- 跨多个 L1 package 的 shared object；
- 或 Planner 有更好且符合尺度纪律的表达。

但**不得把 Commons 自动升级成第四个主权域**。

将结论写入：

`handoff/COMMONS-HANDOFF-DECISION.md`

必要时生成 machine-readable package。

---

## 8. Planner Critic / Gates

输出：

`validation/PLANNER-CRITIC.md`

至少检查：

- 是否真正回答 WHY / WHO / HOW；
- 是否只是把三域 Canon 换词重述；
- Actors / rights 是否只在 consequential 时使用；
- 是否把物理可行误当社会许可；
- 是否把 Planner 知识误当历史行动者知识；
- 是否考虑 ordinary adaptation，而不是自然决定论；
- settlement hierarchy 是否来自 demand / flows / authority / terrain；
- D-025 是否有因果支撑；
- 是否把 proxy 当 road / resource；
- 是否过度设计 L1/L2；
- capacity 是否与 search envelope / catchment 分开；
- cross-region dependency / resilience 是否遗漏；
- recursive packages 是否给下层留下真实问题与适配空间；
- `world writes = 0`。

达到 Planner 的 L0 handoff readiness 才能进入 Primary Freeze。

---

## 9. Primary Freeze｜防旧答案污染

在读取任何 C 类 Legacy 资料之前：

1. 完成全部 Primary L0 outputs；
2. 运行 Critic；
3. 生成 `validation/PRIMARY-FREEZE.json`：
   - plan revision；
   - primary artifact list；
   - SHA256 / equivalent immutable hashes；
   - freeze timestamp；
   - statement：Legacy Middle planning not read before freeze；
4. 冻结主方案。

Primary Freeze 后不得因为看到 Legacy 而静默修改主方案。

如果 Legacy 暴露的是**此前遗漏的高权威事实**，只能记录为 potential upstream input issue，不能偷偷回填。

---

## 10. Legacy A/B Comparison｜Freeze 后才允许

Primary Freeze 完成后，才读取 Authority Matrix C 类旧成果。

输出：

`LEGACY-COMPARISON.md`

对比至少包括：

- 新 L0 是否独立支持旧的“Middle 转换枢纽”等 broad Canon；
- 旧 G1 / N1 等具体节点在 L0 是否根本无法判断；
- 哪些旧结构可能被未来 L1/L2 独立重现；
- 哪些旧规划明显属于过早冻结；
- MD-001U1 / Middle Kit v0.1 能为未来下游提供哪些实验性参考；
- 哪些 Legacy 不应传入 L1-MIDDLE 作为 fixed constraint。

不要给 Legacy 打“保留”仅因为它已经花了很多工作量。

---

## 11. Completion / Stop Rule

任务完成时：

- 输出 `minecraft/建筑师/tasks/CIV-001-L0P/COMPLETION.md`；
- 更新 `current/项目状态.md` 为 `IMPLEMENTATION COMPLETE / AWAITING GPT + OWNER REVIEW`；
- commit + push `assets/main`；
- 核对 remote HEAD；
- 停止。

**不得自动进入 Middle L1。**

必须先由 GPT + Owner 独立审核 L0 及三个 L1 handoff packages。

`world writes = 0`。
