# MP-P02 Independent Review｜minecraft-planner v0.2

日期：2026-09-13  
审核对象：`minecraft/MP-P02-EAST/`  
实现提交：`62594edade83bb5dd2fd93793640d6e32972dbd5`  
测试：`MP-P02｜CIV-001 东域山地共同体系统 / REGIONAL_SYSTEM`

## Verdict

> **PASS_WITH_FINDINGS — L0→L1 recursive planning 成立，但暴露一个应在继续下钻前修复的 foundational SKILL_GAP：Surface / Substrate / Land-Cover 尚未成为一等规划证据。**

本轮足以证明 `minecraft-planner v0.2` 可以把国家层抽象关系继续下钻到区域层，而没有直接跳到建筑设计：上游东域“多共同体、分段服务、远端条件启动”的关系被进一步拆解为北部两个互相依赖的共同体、一个条件性东南共同体，并撤销了一个没有独立需求支撑的中转候选。输出继续交给 `SETTLEMENT` Planner，未伪装为 Builder-ready。

但是，Owner 指出北台地在真实世界中明显以裸露石质地表为主。独立复核本轮实际数据读取与脚本后确认：MP-P02 主要使用 `exposed_y / water_y / artificial_material / land_component / slope8 / relief32` 做地形口袋与阻力分析，没有读取或分类自然表层方块、土壤/裸岩、植被/地被等 surface character。因此 Planner 能知道“这里较平、较高、属于东岛陆地”，但不能真正知道“这里是一片裸岩台地，而不是草土台地”。

这会影响区域规划中的承载、生计、水土、聚落形态与地方 Architecture Kit requirements，不能简单推迟到 Builder 选材阶段。

---

## 1. Positive Evidence

### 1.1 Recursive planning contract 真正生效

MP-P02 把上游 `PACKAGE-03` 当作 parent planning proposal，而不是 Canon；允许移点、拆分、容量重估和撤销。结果没有机械保留父案全部节点，而是形成：

- N01 北台地交换共同体；
- N02 内侧生产共同体；
- N03 东南条件共同体；
- N04 原暂歇候选撤销。

撤销 N04 的理由不是“图不好看”，而是它缺乏独立需求，且会带来约 820 blocks / 46% 的额外绕行。这是有效的下层自主修订，而不是把上层 proposal 当不可更改事实。

### 1.2 Terrain resistance 真实改变了区域网络

本轮没有只看中心点距离。它重新分析低阻力地形口袋，并比较两种坡度容许模型；C01、C02、C03 的长度、累计上升和模型可达性明显不同。远端 N03 仍被保留为条件分支，而非因为地图需要“再放一个城市”而强行保留。

### 1.3 Capacity 有继续收敛，而非复制父级数字

上游北部总建成容量约 6–14k blocks²；本轮拆成两个不同角色的共同体，合计约 6–13k blocks²。东南保持 3–6k 或 0。说明 v0.2 的 built-fabric capacity 没有退化成固定模板数字。

### 1.4 Scale discipline 基本成立

本轮没有下钻到房屋平面、屋顶、palette 或具体街区 parcel；下游仍为三个 `SETTLEMENT` Planner 包。区域图、capacity 和 corridor 都保持搜索 / 假设语义，world writes = 0。

---

## 2. Foundational Finding — Surface / Substrate Blindness

### F01 — Geometry-aware, surface-blind terrain model

**Severity：Major / Foundational**  
**Class：SKILL_GAP**

本轮地形分析脚本读取：

```text
exposed_y
water_y
artificial_material
land_component
slope8
relief32
```

低阻力口袋条件主要是：

```text
land
+ slope threshold
+ relief threshold
```

这能回答：

> 哪些地方较平、较连续、上下移动成本较低？

但不能回答：

> 这块平地实际上是草土、裸岩、砂砾、泥地、雪地、林下还是其它地表？

因此 `TERRAIN-004 / N01 北台地` 被识别为较大的低阻力台地，却没有把 Owner 可见的“大面积石质裸露”作为一等 planning input。

### 为什么这不是 Builder 阶段的小问题

同样的 slope / relief，可以对应完全不同的人地关系：

- 草土缓台：更可能支持菜地、畜养、庭院和较低基础施工成本；
- 裸岩缓台：本地耕作/土壤活动可能受限，生活承载更依赖水土与外部补给，但石工、石基、贴岩建设机会更强；
- 沼泽平地：平但不代表宜居；
- 沙砾平地：排水、植被、农业与道路维护逻辑又不同。

因此：

> **Low slope is not equivalent to high settlement carrying capacity.**

Surface / substrate 应参与：

- settlement capacity sensitivity；
- livelihood / food-support assumptions；
- drainage / water-retention questions；
- erosion / fire / maintenance externalities；
- local construction opportunity；
- morphology / terrace / courtyard / productive-ground strategy；
- Architecture Kit Requirements。

但必须保持证据纪律：

- grass block ≠ fertile farmland；
- exposed stone ≠ approved quarry / ore deposit；
- forest cover ≠ sustainable timber yield；
- sand ≠ desert civilization；
- biome label ≠ soil model。

---

## 3. Skill implication

建议 `minecraft-planner v0.3` 增加一等模块：

> **Surface / Substrate / Land-Cover Character**

至少要求在当前尺度真正相关时读取或明确标记未知：

- exposed natural surface material / family；
- soil-bearing vs exposed rock；
- sand / gravel / mud / snow / barren character；
- vegetation / canopy / ground-cover character；
- wet / dry surface signals when supported；
- current cultivated / disturbed surface when actually observed。

并将其加入：

1. Terrain strategy；
2. Settlement Capacity；
3. Planning maps；
4. recursive handoff unresolved evidence；
5. Planner Critic / regression rubric。

如果现有 Survey 没有这一证据，Planner 不应猜；应输出 targeted evidence requirement。

---

## 4. Status

MP-P02 本身保持：

> **PASS_WITH_FINDINGS**

原因：本轮测试目标——L0→L1 recursive planning、区域 terrain resistance、capacity refinement、下游 SETTLEMENT handoff——已经成立。

但在继续把东域正式下钻到 L2 settlement planning 之前，应先完成 v0.3 的 Surface / Substrate / Land-Cover 补强，否则下一层可能在“几何适合、地表性质不适合”的错误前提上进一步精化。

本 Review 不批准任何 world-write，也不把 MP-P02 proposal 升级为 World Canon。
