# CIV-001-L0P｜Authority Matrix

状态：**ACTIVE INPUT BASELINE**

本文件定义第一次正式 `minecraft-planner v0.5` L0 重编译时，哪些资料属于事实 / Canon / Owner Constraint，哪些旧成果必须降级为 Legacy。

> 核心原则：**先独立推导，再看旧答案。**

---

## A. `OWNER_CONSTRAINT / APPROVED_CANON`｜必须继承

|对象|Authority|Planner 处理|
|---|---|---|
|CIV-001 为人类三域联盟|APPROVED_CANON|固定，不重写文明基本身份|
|前现代松散联盟 / 邦联式共同体；无王；三席议会|APPROVED_CANON|固定政治骨架，可推导空间后果|
|强地方自治；联盟主要处理战争、跨域争端、共同工程、重大交换规则与外交|APPROVED_CANON|固定制度边界，可推导 Actor / rights / flows|
|共同文化：务实、重承诺/契约/协商/履责|APPROVED_CANON|作为空间行为背景，不机械转成建筑风格|
|宗教中等可见；神圣真实但非神权国家|APPROVED_CANON|固定，具体空间表达按尺度 Just-in-time 推导|
|魔法低普及、中影响，不能廉价替代普通工程|APPROVED_CANON|固定 capability boundary|
|成熟前现代石木、桥梁、水利、矿山、冶炼、手工业工程能力|APPROVED_CANON|固定 broad capability；具体工程由下层解决|
|West broad role：低平生产 / 农牧 / 人口 / 市场基础|APPROVED_CANON|固定 broad regional role；具体聚落网络重推|
|Middle broad role：接驳 / 仓储 / 商贸 / 加工 / 低地—山地转换|APPROVED_CANON|固定 broad regional role；具体节点重推|
|East broad role：富矿山地 / 冶金 / 石工 / 山地生产|APPROVED_CANON|固定 broad regional role；具体矿点/聚落重推|
|三域互补是联盟长期存在的重要结构性原因|APPROVED_CANON|必须进入 L0 causal model|
|Alliance Commons 是联盟共同政治中心地|APPROVED_CANON|固定；不是第四个主权域|
|Alliance Commons = 92,124|OWNER_CONSTRAINT / ACCEPTED GEOMETRY|锁定|
|West = 575,397|OWNER_CONSTRAINT / ACCEPTED GEOMETRY|锁定|
|Middle = 391,002|OWNER_CONSTRAINT / ACCEPTED GEOMETRY|锁定|
|East = 1,198,158|OWNER_CONSTRAINT / ACCEPTED GEOMETRY|锁定|
|revision 154 exact territory geometry|OWNER_CONSTRAINT / ACCEPTED GEOMETRY|锁定，不为规划便利改线|
|D-025 density / land-use gradient|OWNER_CONSTRAINT|必须继承：Middle > West > East territory-wide average density；West productive openness strongest；East dispersed mountain settlement + terrain engineering strongest|
|Just-in-time Worldbuilding|OWNER_CONSTRAINT / PROJECT RULE|只补足改变当前空间推导的设定|
|world writes = 0|PROJECT RULE|全 Planner 阶段锁定|

Primary Canon source：

`minecraft/建筑师/world/civilizations/CIV-001/README.md`

关键 decisions 至少包括：

- `D-011_CIV-001人类三域联盟与三席议会方向批准.md`
- `D-013_可见世界约束与隐性设定可创作原则.md`
- `D-014_CIV-001最小文明Canon收敛与AB-001进入.md`
- `D-018_CouncilCenterland联盟公地与中域交割.md`
- `D-020_AB-001P1R联盟公地精确边界接受.md`
- `D-024_TT-002R中域东域精修边界接受并进入MD-001P.md`
- `D-025_三域聚落密度与土地利用梯度.md`
- `D-030_启用MinecraftPlanner并从CIV-001联盟L0重新编译.md`

---

## B. `OBSERVED / DERIVED EVIDENCE`｜可重新解释，不得篡改

### Natural / geographic evidence

优先复用：

- `minecraft/建筑师/research/human-geography/southern-island/WB-002R-R1/`
- `minecraft/建筑师/research/human-geography/southern-island/WB-003R/`
- accepted Natural Atlas / NG evidence as referenced by current project records
- `minecraft/建筑师/research/human-geography/southern-island/territory-refinement/TT-002R/refined-draft.json`

已接受的大尺度事实包括但不限于：

- 西部 C 形低岛低平，West 空间基础强；
- 东部主岛整体高而山地化，内部有连续垂直梯度；
- 东岛西部存在低地 / 坡麓过渡；
- 自然地理本身没有证明唯一的三域政治边界；
- 三域政治边界属于 Human Geography / Owner territorial baseline。

Planner 可以重新解释 terrain / accessibility / surface / flows 的规划意义，但不能把 proxy 写成 observed resource / road / settlement。

### Current-world evidence

如 L0 不需要新鲜逐块事实，优先复用 accepted evidence，不做 broad rescan。

若出现会 materially 改变 L0 判断的 evidence gap：

- 只允许 Just-in-time、read-only、比例相称的补查；
- 记录 necessity / scope / freshness；
- 不得以“能扫描”为理由重新扫描整个世界。

---

## C. `LEGACY / REFERENCE_ONLY`｜主推导前禁止读取

以下内容在 **Primary L0 solution freeze 之前不得读取**：

- `minecraft/建筑师/planning/CIV-001/MIDDLE/MD-001P/`
- `minecraft/建筑师/planning/CIV-001/MIDDLE/G1/MD-001U1/`
- `minecraft/建筑师/research/build-sites/CIV-001/MD-001S1/`
- `minecraft/建筑师/tasks/MD-001P/`
- `minecraft/建筑师/tasks/MD-001P-R1/`
- `minecraft/建筑师/tasks/MD-001S1/`
- `minecraft/建筑师/tasks/MD-001U1/`
- `minecraft/建筑师/architecture/civilizations/CIV-001/kits/MIDDLE/v0.1/`
- D-026 / D-027 中涉及 P1/G1/旧 Middle Masterplan 的下游规划结论
- 旧 P1–P5、N1–N4、G1、旧 corridor、旧 building program、旧 first-build recommendation

`AB-001 Architecture Grammar`：

- 其 broad technology / regional-family内容已被 CIV-001 Canon 摘要覆盖；
- 精确 Architecture Grammar 在 L0 仅可视为 downstream design reference，不能用来反推国家/区域聚落结构；
- L0 不输出建筑形式。

### Legacy comparison phase

Primary L0 solution 冻结后，必须单独输出 `LEGACY-COMPARISON.md`：

- 哪些旧结论被新 Planner 独立重现；
- 哪些被否定 / 重构；
- 哪些因为尺度不足仍不能判断；
- 不得以 Legacy 本身作为新结论的证据。

---

## D. `TO_REDERIVE`｜本轮必须重新求解

L0 必须从 Authority + Evidence 独立推导：

- 三域 + Alliance Commons 在联盟整体系统中的空间角色；
- major Actor / rights / cooperation relations when spatially consequential；
- food / ore / timber / trade / people / authority / defense 等跨域 flows；
- strategic gateways / chokepoints / cross-domain interfaces；
- polity-wide settlement hierarchy 的粗粒度层级；
- regional center / specialized node / frontier / commons 等角色需求；
- approximate settlement capacity / built-fabric scale classes；
- long-distance movement / exchange skeleton at L0 granularity；
- hinterland / catchment / supply / buffer / resilience dependencies；
- major historical / causal growth phases only where they materially explain present polity structure；
- West / Middle / East（以及 Commons 的适当下游形式）L1 recursive Planning Packages。

L0 不得重新求解成具体：

- 镇内街道；
- district boundaries；
- parcels；
- building list / exact building demand；
- exact Architecture Kit；
- exact bridge / harbor / well geometry；
- Minecraft block-level masks except accepted political boundary references。

---

## E. Stable Skill / Contract Baseline

本任务使用：

- `minecraft-planner v0.5`
- `minecraft-builder v1.11`（本轮不调用 Builder，只作为未来 recipient）
- `Minecraft Planner–Builder Contract v1.0`

Vibe-Coding stable regression record：

`skill/codex/REGRESSION-BASELINE.md`

固定稳定源提交（该记录所列）：

`fc6371361685e2eeaefdef5a513f21dbe64c6696`

Planner → Planner recursion 以 `recursive-planning-handoff.md` 为准。
