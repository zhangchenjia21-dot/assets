# CIV-001-MID-L1P｜Middle Regional System Recompile

状态：**AUTHORIZED / DISPATCH READY**
日期：2026-09-14

## 0. 任务定位

这是已接受 `CIV-001-L0P-r1` 之后，对 Middle 的第一次正式 `L1 REGIONAL_SYSTEM` 重编译。

目标：

> **在不继承旧 N1/G1/P1–P5 等答案的前提下，使用 minecraft-planner v0.5，从中域真实领土、地形、联盟级 flows / rights / access / density constraints 出发，重新推导中域完整的区域聚落网络、中心层级、主要交换关系、容量与生长逻辑，并生成向 L2 递归的 Planning Packages。**

本任务不是城市详细总规，不设计街区、地块或建筑。

`world writes = 0`。

---

## 1. Skill / Parent Baseline

必须使用：

- `minecraft-planner v0.5`
- `recursive-planning-handoff.md`
- Planner 执行中实际需要的 references

首先读取：

1. `minecraft/建筑师/tasks/CIV-001-MID-L1P/AUTHORITY-MATRIX.md`
2. `minecraft/建筑师/decisions/D-031_CIV-001-L0P接受并进入MiddleL1区域规划.md`
3. `minecraft/建筑师/planning/CIV-001/POLITY/CIV-001-L0P/handoff/L1-MIDDLE.md`
4. `minecraft/建筑师/planning/CIV-001/POLITY/CIV-001-L0P/L0-POLITY-PLAN.md`
5. L0 Primary 中与 Middle 直接相关的 flows / movement / actors / capacity / growth / resilience artifacts
6. accepted CIV-001 Canon、D-025、revision154 与相关 natural geography evidence

### Legacy Firewall

Primary L1 Freeze 前严格遵守 Authority Matrix D 类禁读规则。

不得通过 Git search、全文搜索、目录遍历等方式提前看到旧 Middle / G1 答案。

---

## 2. 本轮必须回答的 Owner 级问题

最终成果必须让非程序员 Owner 能直接回答：

1. **中域到底应该有几个主要聚落 / 中心？**
2. **为什么是这些中心，而不是更多或更少？**
3. **其中有没有一个真正的“主中心”？如果有，为什么；如果没有，为什么？**
4. **联盟公地东侧连接地带是否自然形成门户聚落？若形成，它和中域其它中心是什么关系？**
5. **西域来的粮食 / 生活品与东域来的矿料 / 金属，应该在哪里、以什么方式完成换装 / 存留 / 加工？**
6. **政治访问和商业货流需要共用节点，还是应该部分分离？**
7. **哪些地方主要承担居民日常生活，哪些地方承担市场、加工、仓储、旅宿、专业服务？为什么？**
8. **Middle > West > East 的平均密度梯度，具体在中域区域网络上怎样体现，而不是靠把所有平地塞满建筑？**
9. **中域从早期交换到成熟区域网络，大致怎样历史性生长出来？**
10. **下一步应该优先挑哪个 settlement 做 L2，为什么？**

单独输出：

`OWNER-SUMMARY.md`

要求用普通中文，不用 Skill 术语堆砌。

---

## 3. Regional Premise / Actors / Rights

在 Middle L1 尺度重新整理：

- 中席代表的地方共同体、商贸 / 接驳权力与居民；
- West / East 使用者对 Middle 的需求，但不赋予其直接土地控制权；
- Commons 共同政治访问与 Middle 地方土地权的接口；
- 运输者、货主、工匠、居民、旅客的利益与冲突；
- 地方地权、水权、岸线 / 通行权中哪些已知、哪些未决；
- 谁承担公共工程 / 等待 / 拥堵 / 外部性成本。

不得默认：

- 中域可以对联盟流量无限收费；
- 中域必须免费承担全部货运；
- 一条最短路线自动拥有通行权；
- Commons 或 East/West 可以单方决定中域内部土地。

---

## 4. Middle Regional Terrain / Surface / Access Interpretation

使用完整 391,002 Middle territory。

应在 L1 尺度识别真实有意义的：

- 低地 / 岸侧；
- connector / Commons interface；
- 谷地；
- 坡麓；
- 高位缓地；
- Middle→East 的潜在跨界接近带；
- 水侧接驳可能；
- 地形阻力与普通时代工程可以改变的约束。

可以形成新的区域性 terrain/service sectors，但：

- 不继承旧 P1–P5；
- 不为了凑 3–6 块强行分区；
- sector 必须有真实 regional planning 意义；
- sector 不是政治边界或 settlement footprint。

---

## 5. Settlement Network Alternatives｜必须比较，不得一步定答案

至少提出并比较两种可信网络逻辑，例如但不限于：

### A. Consolidated / merged system

一个较强的主要转换中心承担多类流，辅以若干地方节点。

### B. Distributed / specialized system

Commons gateway、跨水货运、山地换装、居民市场等由多个互补中心承担。

如果证据支持第三种 hybrid，可加入。

比较维度至少包括：

- terrain / surface；
- effective access；
- rights / control；
- political access vs freight conflict；
- daily resident needs；
- storage / processing externalities；
- water / waste / fire pressure；
- seasonal peaks；
- resilience / single-point failure；
- D-025 density consequence；
- plausible historical growth。

最终必须选择一个推荐网络，或明确保留一个尚需证据才能二选一的 fork。

---

## 6. Settlement Roles / Hierarchy

根据本轮独立推导，定义 Middle 需要的 settlement / service node roles。

每个重要 node / node-family 至少说明：

- WHY；
- users；
- regional role；
- broad search envelope / search logic；
- upstream flows；
- downstream / neighboring dependencies；
- working built-fabric capacity range（若有足够依据）；
- maturity / growth role；
- major constraints；
- evidence confidence；
- what must be resolved at L2。

不要为了画图均匀撒节点。

不要提前冻结：

- exact settlement polygon；
- exact streets；
- exact district zoning；
- exact building count。

---

## 7. Movement / Exchange Network

L1 可以确定：

- regional corridor relationships；
- search corridors；
- crossing / interface alternatives；
- transport-mode expectations；
- major access dependencies；
- fallback relations。

但每条关系必须区分：

- physical access；
- legal / tenure access；
- political permission；
- security；
- seasonality；
- transport-mode compatibility。

不得把 terrain-cost path 直接当道路。

尤其重新研究：

- Commons → Middle；
- West → Middle direct exchange；
- Middle internal movement；
- Middle → East 多点关系。

---

## 8. Capacity / Density / Land-use Logic

必须给出 Middle 全域的区域量级判断，并检查 D-025。

至少明确：

- settlement built-fabric capacity hypotheses；
- open / protected / productive / transition ground 的区域角色；
- density 为什么集中在哪里；
- 为什么其它地方相对更低；
- 混合使用、共享设施、紧凑街区如何减少无意义占地；
- 哪些地形不能因为追求高密而推平。

如需要数字，必须区分：

- built fabric；
- building footprint；
- settlement envelope；
- catchment / productive hinterland。

不能混用。

---

## 9. Causal Growth / Path Dependence

建立 Middle 自己的区域生长模型。

至少说明：

- 最初哪些局部交换 / 居民 / 通行需求先存在；
- 哪些 repeated flows 促成稳定的接驳与服务节点；
- Commons 稳定后如何改变 Middle 的政治访问；
- 山地交换增长如何改变加工 / 仓储 /居民节点；
- 拥堵、地权、火险、缺水、坡地如何产生分流、次中心或专业化；
- 成熟网络为什么形成当前推荐结构。

这是历史形成模型，不是 Minecraft build phase。

除非 Owner 后续接受为 Canon，否则保持 `PLANNING_ASSUMPTION`。

---

## 10. Cross-Scope Interfaces

必须显式处理但不越级设计：

### Alliance Commons

只解析 Middle 侧所需的 shared institutional access / interface obligations。

若 Commons 内部细节不足以继续，输出：

`COMMONS_DEPENDENCY_REQUEST`

不要自行规划整个 Commons。

### West

只解析 Middle 所需的 R-WM / food / ordinary goods interfaces。

### East

只解析 Middle 所需的 R-ME / mountain production / daily supply interfaces。

如 sibling L1 细节确实成为 blocker，记录最小 dependency request，不直接执行 West/East L1。

---

## 11. L2 Recursive Handoff Packages

对最终推荐网络中的重要 settlement / settlement-family，生成 L2 `SETTLEMENT` Planning Package。

每个包包含：

- WHY / role；
- search geometry / envelope；
- UPSTREAM_FIXED；
- DOWNSTREAM_TO_RESOLVE；
- DOWNSTREAM_ADAPTABLE；
- capacity hypothesis；
- access / water / rights / seasonal / resilience dependencies；
- revision triggers；
- expected L2 outputs；
- `world_write_authorization = false`。

L1 完成后**不得执行任何 L2 包**。

---

## 12. Primary Freeze + Legacy A/B

在独立 Middle L1 主方案完成后：

1. 生成 `validation/PRIMARY-FREEZE.json`；
2. 最好用独立 commit 固定 Primary；
3. 才允许读取 Authority Matrix D 类 Legacy；
4. 输出 `LEGACY-COMPARISON.md`。

比较：

- 新中心网络 vs 旧 N1/G1/N2/N3/N4；
- 新区域结构 vs 旧 P1–P5；
- 新 movement vs 旧 R1–R7；
- 新 growth logic vs 旧“总规后设计”流程；
- 哪些旧局部 current-world evidence 仍可复用；
- 哪些旧成果应继续淘汰。

**Legacy comparison 不得回填 Primary。**

---

## 13. Required Deliverables

建议目录：

`minecraft/建筑师/planning/CIV-001/MIDDLE/CIV-001-MID-L1P/`

至少包含：

- `README.md`
- `OWNER-SUMMARY.md`
- `L1-REGIONAL-PLAN.md/json`
- `ACTORS-RIGHTS.md`
- `REGIONAL-TERRAIN-SYSTEM.md/json`
- `SETTLEMENT-NETWORK-ALTERNATIVES.md`
- `SETTLEMENT-HIERARCHY.md/json`
- `MOVEMENT-ACCESS-NETWORK.md/json`
- `CAPACITY-DENSITY.md/json`
- `GROWTH-PATH-DEPENDENCE.md`
- `RESILIENCE-DEPENDENCIES.md`
- `handoff/L2-*.md/json`
- `validation/PRIMARY-FREEZE.json`
- `validation/PLANNER-CRITIC.md`
- `LEGACY-COMPARISON.md`（Freeze 后）
- `COMPLETION.md`

### Maps

输出对 Owner 有意义的等比例地图，至少让人一眼看懂：

1. Middle terrain / surface context；
2. 推荐 settlement network；
3. major flows / movement；
4. settlement hierarchy + approximate search areas；
5. density / built-fabric concentration logic；
6. growth / phase logic（如空间化有意义）。

图上必须区分：

- accepted boundary；
- observed / derived terrain；
- proposal；
- search area；
- relationship arrow；
- NOT_EXISTING_ROAD / NOT_BUILD_FOOTPRINT。

---

## 14. Planner Critic

至少检查：

- 是否只是把旧 N1/G1 换名字；
- 是否真的比较一个中心 vs 多中心；
- 是否把 Commons gateway 自动当成最大中心；
- 是否把所有货流强塞同一节点；
- 是否忽略常住居民生活；
- 是否把 Middle 高密误解为填满平地；
- 是否把 weighted path 当真实道路；
- 是否让地形、权利、水、季节和外部性真正改变网络；
- 是否出现现代 zoning；
- 是否越级画 district / parcel / building；
- L2 packages 是否保留真实问题与自由度；
- 是否把 Legacy 在 Freeze 前偷渡回来。

---

## 15. Stop Conditions

本轮结束时必须：

- `world writes = 0`；
- 不调用 `minecraft-builder`；
- 不进入 L2；
- 不设计建筑；
- 不修改 revision154 / Commons；
- 不执行 West / East / Commons sibling plan；
- commit + push `assets/main`；
- 核对远端 HEAD；
- 停止交 GPT + Owner 独立审核。
