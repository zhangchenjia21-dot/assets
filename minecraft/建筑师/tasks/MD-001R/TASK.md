# MD-001R｜Middle Domain Regional Planning Reconnaissance

状态：**AUTHORIZED / DISPATCH READY**

授权：`../../decisions/D-021_先完成中域区域调查与总体规划再进入首栋建筑.md`

## 0. 任务定位

这是 CIV-001 **中域总体规划之前的规划级区域调查**。

目标不是设计第一栋建筑，也不是绘制最终城镇总图，而是建立足够让 GPT + Owner 正确规划中域的空间事实层。

当前路线：

```text
MD-001R Regional Planning Reconnaissance
→ GPT independent review
→ MD-001P Middle Domain Master Planning
→ first building type / site
→ local Site Gate
→ architecture design
→ bounded world-write
```

`world writes = 0`。

---

## 1. 必读

至少读取：

1. `minecraft/建筑师/AGENTS.md`
2. `minecraft/建筑师/current/项目状态.md`
3. `minecraft/建筑师/current/世界构建原则.md`
4. `minecraft/建筑师/current/建造原则.md`
5. `minecraft/建筑师/decisions/D-007_文明设定必须经过区域实地考察.md`
6. `minecraft/建筑师/decisions/D-010_大型扫描证据GitHub轻量化.md`
7. `minecraft/建筑师/decisions/D-013_可见世界约束与隐性设定可创作原则.md`
8. `minecraft/建筑师/decisions/D-021_先完成中域区域调查与总体规划再进入首栋建筑.md`
9. `minecraft/建筑师/world/civilizations/CIV-001/README.md`
10. `minecraft/建筑师/architecture/civilizations/CIV-001/Architecture-Grammar.md`
11. `minecraft/建筑师/research/human-geography/southern-island/WB-002R-R1/README.md`
12. `minecraft/建筑师/research/human-geography/southern-island/WB-003R/README.md`
13. `minecraft/建筑师/research/build-sites/CIV-001/AB-001P1R/README.md`
14. 本 Task Packet

---

## 2. 已知中域 Canon / Evidence

### Human Geography Canon

中域当前定位：

> **东部主岛西侧低地 / 坡麓过渡枢纽**

长期文明功能方向：

- 跨岛 / 水陆接驳；
- 仓储；
- 商贸；
- 加工；
- 低地与山地之间的人员 / 货物转换。

这些是 World Canon 的功能方向，不等于现实世界里已经存在码头、道路、城镇或仓库。

### Existing evidence

可以复用：

- WB-002R-R1：东岛完整 topology / terrain / biome / water / vegetation regional evidence；
- WB-003R：M research mask、low-relief substrate、water / landing proxy、inter-island crossings、M→E terrain-cost corridor；
- AB-001P1R：Alliance Commons 与中域的精确 connector 分界；A 内中域 connector = **13,661 blocks²**, `X>=89` 的 A actual geometry；
- R1 Local Raw Cache / lightweight query evidence。

WB-003R 的 `M` 掩膜只是研究掩膜，不是正式中域行政边界。本轮不得直接把 `M = 中域领土`。

---

## 3. 调查核心问题

本轮必须为“中域总体规划”回答以下问题。

### 3.1 Planning study area / spatial extent

建立一个**中域规划调查范围**，但不要自动冻结政治边界。

应从：

- Alliance Commons 东侧 connector；
- 东岛西部低地；
- 低地向坡麓 / 山地过渡；
- 既有 M→E movement evidence；

共同确定调查 envelope。

输出至少区分：

- `MIDDLE_CORE_PLANNING_AREA`：高度符合中域功能的低地 / 坡麓；
- `TRANSITION_FRINGE`：可能属于中域或东域的过渡带；
- `NOT_MIDDLE_PLANNING_AREA`：明显属于东部山地核心或无关区域。

这些是 planning classes，不是 World Canon 行政边界。

### 3.2 Terrain / usable-space structure

结构化：

- elevation / relief / slope；
- 大型连续 FLAT / GENTLE patches；
- 岸线与低岸；
- 内水；
- 坡麓 / 谷地 / 台地；
- 明显难以开发的陡坡、悬崖或破碎区；
- 从海岸 / connector 向山地抬升的 section logic。

不能只给平均值，要让总体规划能知道“哪里平、哪里陡、哪里形成自然分隔”。

### 3.3 Water / shoreline / landing structure

基于既有 water topology 与必要的 targeted refinement，标出：

- 面向西域 / Alliance Commons 的主要岸线；
- 可形成未来水陆接驳的 `LANDING_ACCESS_PROXY` 区段；
- 不适合大规模岸线开发的区段；
- 内水 / 湿地 / 水洞等规划约束；
- 现有 crossing X-00 / X-01 / X-03 与中域规划结构的关系。

禁止直接命名为“港口 / 航线”。

### 3.4 Movement / corridor structure

分析中域内部以及：

```text
Alliance Commons / 海峡方向
→ 中域低地
→ 坡麓
→ 东域山地核心
```

的自然移动结构。

至少识别：

- 1–3 条主 corridor candidate；
- 横向 / 纵向 movement barriers；
- 可能成为道路骨架的自然低成本带；
- 哪些 corridor 只是模型敏感结果；
- 未来道路 / 聚落沿线开发时需要避开的地形问题。

这不是正式道路规划。

### 3.5 Existing surface / landscape constraints

至少整理：

- structural vegetation；
- exposed / near-surface material differences；
- lava / cave / cliff / hazardous signals；
- dirt_path / waystone / 人工方块 / 已知 structure signals；
- 需要在未来 Site task 中保护或复核的对象。

不要为了调查清树或修改世界。

### 3.6 Planning subareas

基于真实地理，在中域规划调查范围内提出 **2–5 个 planning subareas**。

每个 subarea 至少记录：

- ID；
- geometry / bounds；
- terrain character；
- water relation；
- access relation；
- expansion room；
- dominant constraints；
- `planning_fit`。

允许的 `planning_fit` 例如：

- exchange / transfer candidate；
- dense settlement candidate；
- warehouse / craft candidate；
- residential expansion candidate；
- foothill transition candidate；
- preserve / low-development candidate。

这些只是总体规划输入，不是建筑选址授权。

### 3.7 Planning nodes

从 subareas 中识别最多 **3–6 个 planning nodes**，用于后续 MD-001P 比较。

Node 不是一栋建筑的 Site，而是可能形成：

- 核心城镇；
- 渡运 / 交换聚落；
- 坡麓加工聚落；
- 次级居住 / 服务聚落；

等较大空间节点的位置。

每个 node 要明确为什么值得规划、为什么可能不适合高强度开发。

不得在本轮直接宣布“这里就是中域首府”。

---

## 4. 总体规划所需的 Section / Scale

为了后续不是只看俯视图，本轮至少提供：

- 1 条从西 / 海湾 → 中域 → 东部山地的代表性长剖面；
- 2–4 条关键局部剖面或 elevation profile；
- planning nodes 之间的大致距离量级；
- 中域整体可规划尺度与各 subarea 的面积量级。

不要求专业 CAD，但必须让 GPT + Owner 能判断城镇与交通结构是否在 Minecraft 玩家尺度上成立。

---

## 5. 数据策略｜禁止重复大扫描

严格复用 WB-002R-R1 / WB-003R / AB-001P1R。

默认：

```text
existing R1 / WB-003R caches
→ query / derived planning analysis
→ only targeted refinement where genuinely missing
→ Lightweight Review Bundle
```

禁止：

- 重新做整个南部岛群 full scan；
- 重新做整个东岛逐柱扫描；
- 重复上传 predecessor raw DB / NPZ；
- 为“以后可能有用”无限扩大调查。

如果需要新 current-world read，必须是 bounded targeted read，并在 Completion 中给出新增 columns / blocks 数量和原因。

遵守 D-010：

- GitHub research payload target `<=15 MiB`；
- `>25 MiB` 默认禁止 push；
- 完整 raw 默认 Local-only。

---

## 6. Deliverables

写入：

`minecraft/建筑师/research/human-geography/middle-domain/MD-001R/`

建议至少：

```text
README.md
planning-study-area.json
terrain-structure.json
water-access.json
movement-structure.json
planning-subareas.json
planning-nodes.json
reports/中域区域规划调查.md
visual/middle-domain-planning-base.png
visual/terrain-access.png
visual/section-profile.png
review/index.json
review/key-metrics.json
review/limitations.json
validation/summary.json
manifest/lineage.json
```

允许合理合并，但不能只交一篇散文。

### 规划底图要求

至少提供一张**等比例、带坐标 / 方向、可用于后续总体规划的中域规划底图**，清楚显示：

- Alliance Commons / connector；
- 海岸 / 水体；
- flat / gentle / steep structure；
- planning subareas；
- planning nodes；
- corridor candidates；
- 东域山地核心方向。

地图必须是 evidence / planning base，不得画成已经批准的城市设计图。

---

## 7. Interpretation contract

最终结论按：

- `OBSERVED / DERIVED`；
- `SUPPORTED_PLANNING_INFERENCE`；
- `PLAUSIBLE_BUT_UNVERIFIED`；
- `NOT_SUPPORTED`；

区分。

不得把总体规划潜力写成“现实中已经有某城市 / 港口 / 道路”。

---

## 8. Strict prohibitions

本轮不得：

- world write；
- 设计第一栋中域建筑；
- 决定建筑尺寸；
- 画最终道路 / 港口 / 城镇施工图；
- 自动确定中域首府；
- 修改 CIV-001 Canon；
- 修改 AB-001 Architecture Grammar；
- 修改 Alliance Commons boundary；
- 恢复三席议事大厅 AB-001P2；
- broad rescan。

`world writes = 0`。

---

## 9. Completion / Stop

完成后：

- 写 `minecraft/建筑师/tasks/MD-001R/COMPLETION.md`；
- current 只机械更新为 implementation completed / awaiting independent review；
- commit + push `assets/main`；
- 保留并行提交，不 force-push；
- 核对远端 HEAD；
- 停止交 GPT 独立审核。

审核通过后，下一步才是 **MD-001P｜Middle Domain Overall Master Planning**。
