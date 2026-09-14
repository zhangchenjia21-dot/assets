# D-030｜启用 minecraft-planner 并从 CIV-001 联盟 L0 重新编译

状态：**OWNER APPROVED WORKFLOW / ACTIVE**

日期：2026-09-14

## 1. 决策

`minecraft-planner v0.5`、`minecraft-builder v1.11` 与 `Minecraft Planner–Builder Contract v1.0` 已完成核心回归并形成稳定基线。

CIV-001 正式项目从现在起停止沿用旧的“先做 Middle 总规 / 再做单体或微街区”的聚落规划链，改为按 Planner 的五级递归尺度重新编译：

```text
L0 POLITY_TERRITORY
→ L1 REGIONAL_SYSTEM
→ L2 SETTLEMENT
→ L3 DISTRICT
→ L4 URBAN_ENSEMBLE
→ minecraft-builder
```

第一正式任务从 **CIV-001 三域联盟 L0 POLITY_TERRITORY** 开始。

L0 接受后，优先递归进入 **Middle L1 REGIONAL_SYSTEM**。West / East / Alliance Commons 的更细规划按依赖 Just-in-time 展开，不要求在进入 Middle 前全部完成。

## 2. 冻结并保留的上游事实

本轮不是重新创造领土或文明 Canon。以下继续作为 Planner 的高权威输入：

- 已接受 Natural Geography / current-world evidence；
- CIV-001 Minimal World Canon；
- 三域联盟、三席议会与强地方自治；
- Alliance Commons 的共同领土地位及精确边界；
- Owner 人工 West / Middle / East 分区；
- TT-002R revision 154 正式领土；
- D-025 三域空间梯度；
- 世界技术、魔法、宗教与文化等已批准 Canon。

正式领土：

```text
ALLIANCE_COMMONS = 92,124
WEST_DOMAIN      = 575,397
MIDDLE_DOMAIN    = 391,002
EAST_DOMAIN      = 1,198,158
UNASSIGNED       = 0
DISPUTED         = 0
TOTAL            = 2,256,681
```

Planner 默认无权为了规划便利修改上述政治边界。若出现真正的 `UPSTREAM_PLANNING_ISSUE`，必须上报 GPT + Owner，不能静默改线。

## 3. Owner 级空间方向继续有效

```text
Middle = territory-wide 平均建筑 / 聚落密度最高、土地利用最紧
West   = 大面积农牧生产景观最强、聚落节点化集中
East   = territory-wide 平均密度最低、聚落最分散嵌山、地形工程最强
```

这是 `OWNER_CONSTRAINT`，不是旧规划结果。

Broad Canon 继续有效：

- West：低平生产 / 农牧 / 人口 / 市场基础；
- Middle：接驳 / 仓储 / 商贸 / 加工 / 低地—山地转换；
- East：富矿山地 / 冶金 / 石工 / 山地生产；
- 三域互补是联盟长期存在的重要结构性原因；
- Alliance Commons 是联盟共同政治中心地，不是第四个主权域。

## 4. 必须重新推导的内容

以下旧结论全部降级为 `LEGACY / REFERENCE_ONLY`，不得直接继承为新 Planner 的答案：

- P1–P5 planning subareas；
- N1 / N2 / N3 / N4 / G1 settlement hierarchy；
- 旧 movement corridors；
- 旧 land-use / building program；
- gateway / anchor 的具体落点与层级；
- Growth Sequence；
- District / block / parcel morphology；
- MD-001S1 单建筑 Site 解释；
- MD-001U1 微街区 envelope 与 5 栋 building program；
- Middle Architecture Kit v0.1 的 typology / module 结论。

旧成果不删除，保留为 lineage / regression / A-B evidence。

## 5. Anti-Anchoring｜旧规划读取顺序

为避免新版 Planner 被旧答案锚定：

1. 主 L0 因果规划阶段不得读取旧 Middle 聚落规划与 MD-001U1 设计包；
2. 先使用冻结事实、Canon、Owner Constraint 与自然 / 人文地理 evidence 完成独立 L0 解；
3. 主解冻结后，才允许读取 Legacy 规划做 A/B comparison；
4. Legacy comparison 不得无证据地反向污染已经形成的独立推导；
5. 若旧结论与新推导巧合一致，应说明独立因果链，而不是以“之前就是这样”为理由。

## 6. 尺度纪律

L0 负责：

- 联盟领土结构与三域关系；
- settlement hierarchy 的粗层级；
- regional center / gateway / frontier / political commons 等角色；
- 跨域 food / ore / trade / people / authority / defense flows；
- major corridors / chokepoints / cross-region interfaces；
- catchment / hinterland / resilience；
- 粗粒度 settlement capacity 与 built-fabric scale classes；
- 向 L1 递归的 Planning Packages。

L0 不得：

- 画具体街道；
- 决定具体地块；
- 复刻 N1 / G1 等旧节点；
- 设计建筑；
- 生成 block palette；
- 进入 world-write。

## 7. World-write

Planner 全阶段默认：

`world writes = 0`

任何 Planner acceptance 都不自动构成 Builder 或施工授权。
