# CIV-001-MID-A-QG-L3P｜Q-GATE Gateway Market District Planning

状态：**AUTHORIZED / DISPATCH READY**

日期：2026-09-20

## 0. 任务定位

这是 accepted MID-A 的第一项 L3 `DISTRICT` 规划。

目标：

> **把 Q-GATE 规划成 MID-A 面向 Alliance Commons 的极繁华、高密、混合生活门户街市片，并生成可进入 L4 Urban Ensemble 的街区 / 街坊 / 公共空间 / 地块关系。**

Q-GATE 是 MID-A 的内部片区，不是独立城市。

本轮不设计具体建筑，不调用 Builder，不 world-write。

## 1. Baseline

必须读取：

- `minecraft/建筑师/tasks/CIV-001-MID-A-QG-L3P/AUTHORITY-MATRIX.md`
- accepted MID-A L2 Primary；
- `handoff/L3-Q-GATE.md`
- D-033。

使用：

- `minecraft-planner v0.5`

## 2. 游戏体验目标

玩家从 Alliance Commons 进入中域时，应立刻感受到：

> **这里进入了整个联盟最繁忙、最紧凑、最城市化的地方。**

但不要用“巨型城门 / 关卡”制造繁华。

繁华应来自：

- 连续 frontage；
- 密集但有变化的商住建筑关系；
- 狭窄而有效的街巷；
- 店铺 / 饮食 / 旅宿 / 修理 / 短存 / 居住混合；
- 来往者与本地居民共存；
- 市场摊位 / 雨棚 / 小公共空间；
- 共享院落和后向使用；
- 去往 Q-MARKET 的城市连续性；
- visible infrastructure / street furniture / daily-life details。

## 3. 必须回答

1. 从 X=89 Commons 接口进入后，主要公共 movement 如何逐步展开，而不是一条直路贯穿？
2. 哪一段形成最强 frontage / 门户商业，为什么？
3. Q-GATE 内部应该形成几个 block / morphological unit？为什么这样分？
4. 主要 lane / secondary lane / service lane / shared courtyard 如何形成？
5. 公共、共用、半私有、私有空间怎样过渡？
6. 短交易、饮食旅宿、修理、短存和居民生活怎样混合，而不是 modern zoning？
7. 批次货物怎样转向后场 / Q-YARDS，而不堵住居民与 Commons 公共访问？
8. Q-GATE 怎样无缝进入 Q-MARKET，而不是出现“门户镇结束、主城开始”的断裂？
9. 历史上哪些地块先形成，哪些因分户 / 商业价值 / 后向利用后来细分？
10. 在高密下，visible water / drainage / fire / waste / maintenance 怎么表达？
11. 哪些 Urban Ensemble 应进入 L4，并推荐第一批实际建设的 package？

## 4. Infrastructure Simplification

遵循 D-033。

做到玩家可见 / 可读即可。

建议研究但不强制形式：

- 1–2个公共井 / 水槽 / 小蓄水点的规划位置关系；
- 街边明沟 / 檐沟 / 短盖沟；
- 消防水缸 / 水桶点；
- 有理由的小型开敞节点；
- 后巷清运 / 服务院。

不要设计：

- 地下管网；
- 现实城市污水系统；
- 水压 / 流量系统；
- 复杂消防系统。

这些具体造型属于 Builder。

## 5. Current-world Evidence

若父 L2 snapshot 对本片仍足够新鲜且覆盖完整，可明确复用。

只有在：

- 当前世界已变化；
- 精确 L3 street/block 关系需要更细局部证据；
- 旧快照范围不足；

时才做有界 read-only refresh。

不 broad rescan。

## 6. 输出

建议目录：

`minecraft/建筑师/planning/CIV-001/MIDDLE/MID-A/Q-GATE/CIV-001-MID-A-QG-L3P/`

至少包含：

- README / OWNER-SUMMARY；
- L3-DISTRICT-PLAN.md/json；
- MORPHOLOGY-BLOCKS.md/json；
- MOVEMENT-LANES.md/json；
- PUBLIC-SHARED-PRIVATE.md/json；
- PARCEL-EVOLUTION.md/json；
- GROWTH-PATH-DEPENDENCE.md；
- DENSITY-FRONTAGE.md/json；
- VISIBLE-SERVICES.md/json；
- BUILDING-DEMAND.md/json；
- ARCHITECTURE-KIT-REQUIREMENTS.md/json；
- L4 recursive packages；
- current evidence refs / refresh evidence；
- Primary Freeze；
- Planner Critic；
- Freeze 后 Legacy comparison；
- 至少 4–6 张可审核规划图。

## 7. L4 Handoff

L3 应把 Q-GATE 拆成若干**有因果关系的 Urban Ensemble / micro-district packages**。

每个 package 至少说明：

- WHY；
- users / flows；
- frontage / lane / courtyard relation；
- shared / service interfaces；
- growth stage；
- density character；
- planning-fixed relations；
- Builder adaptable freedom；
- visible service expectations。

同时给出：

> **recommended_first_build_package**

推荐理由优先考虑：

1. 玩家进入 MID-A 的第一视觉体验；
2. 能代表 MID-A Architecture Kit 的核心语言；
3. 能验证高密混合而非 prefab；
4. 后续可自然向 Q-MARKET 扩展；
5. 施工范围有界、可回退、可独立验收。

## 8. Quality Gate

检查：

- 不是现代网格 zoning；
- 不是一条主街两边复制同款房；
- 门户繁华但不堵公共进入；
- 居民真实存在，不是NPC商业布景；
- 地块 / 街坊有历史生长逻辑；
- 高密不消灭消防 / 排水 / 通行 / 后勤；
- 基础设施不过度工程化；
- Q-GATE 与 Q-MARKET 连续；
- 不偷用旧 G1/U1 几何；
- 不越级设计具体建筑；
- world writes = 0。

## 9. Stop Rule

完成：

1. Primary Freeze；
2. Freeze 后 Legacy comparison；
3. commit + push `assets/main`；
4. 核对远端 HEAD；
5. 停止交 GPT + Owner 审核。

不得自动执行 L4，不调用 Builder，不施工。
