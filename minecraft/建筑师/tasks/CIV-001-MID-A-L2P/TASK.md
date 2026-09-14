# CIV-001-MID-A-L2P｜MID-A Settlement Causal Plan

状态：**AUTHORIZED / DISPATCH READY**

日期：2026-09-14

## 0. 任务定位

这是 `minecraft-planner v0.5` 在 CIV-001 Middle 的第一次 L2 `SETTLEMENT` 规划。

目标：

> **把 MID-A 作为一座完整、高密、成熟的城市重新规划，解释它为什么长在这里、怎样从门户与低地交换逐步形成城市、内部为什么出现不同片区，并生成 L3 recursive packages。**

本任务不设计具体建筑，不调用 Builder，不 world-write。

`world writes = 0`。

---

## 1. Baseline

必须使用：

- `minecraft-planner v0.5`
- accepted `CIV-001-L0P-r1`
- accepted `CIV-001-MID-L1P-r1`
- `D-032_MiddleL1接受并确认MID-A为联盟最高密度城市进入L2.md`
- `minecraft/建筑师/tasks/CIV-001-MID-A-L2P/AUTHORITY-MATRIX.md`

直接父包：

`minecraft/建筑师/planning/CIV-001/MIDDLE/CIV-001-MID-L1P/handoff/L2-MID-A.md`

---

## 2. Owner Direction｜必须正确实现

MID-A 是：

> **整个 CIV-001 联盟建筑密度最高、土地利用率最高的城市区域。**

但高密不等于把所有格子铺满。

应体现：

- 高比例的有效建成与使用空间；
- 更连续的街道 frontage；
- 商住仓储/轻加工/旅宿/公共服务高度混合；
- 多层建筑需求更强；
- 院落、后场、装卸、服务缝和公共空间都承担明确功能；
- 很少存在“只是空着”的低效城市余地；
- 防火、排水、公共通行、市场空间、水与维护仍必须有真实空间；
- 不为追求密度大面积推平地形。

### Gateway

Alliance Commons 东侧 gateway / connector：

- 属于 MID-A 城市内部；
- 不是独立 G1 聚落；
- 因政治访问、商旅、即时交换与地理接口而非常繁华；
- 可形成 MID-A 内部最强的门户商业 / 服务片区之一；
- 不自动成为唯一城市核心；
- 不获得海关、关卡、强制收费或强制贸易权；
- 大宗长期仓储、高外部性加工不应全部堵在 Commons 接口。

---

## 3. Primary Questions

必须回答：

1. MID-A 的**真实城市范围**应该落在哪里？城市边缘为什么在那里停止？
2. 城市到底是“门户即核心”，还是“门户繁华但主市场 / 综合核心稍向东”，或形成多核心连续城市？
3. 最初 Anchor 是什么：Commons 接口、低地本地居民、湾内交换、市场、道路交汇、供水，还是其组合？
4. MID-A 的 Growth Sequence 如何形成？必须区分：
   - 联盟成立前的地方生活；
   - 跨域交换强化；
   - Commons 稳定后门户繁荣；
   - 成熟城市阶段的高密填充、分化与扩展。
5. 城市内部主要 movement skeleton 为什么这样形成？
6. 哪些 district / quarter 应该出现，为什么出现，为什么彼此邻接？
7. 门户区、主市场/综合核心、居民混合区、仓储/装卸、工坊/加工、旅宿/服务等功能应如何混合与分化，避免现代 zoning？
8. MID-A 作为联盟最高密城市，如何在 whole-settlement 尺度实现高土地利用而仍保持可生活性？
9. 水、污物、消防、排水、货运、维护、季节峰值如何约束高密城市？
10. 城市应如何与 Commons、MID-B、West 输入和 Middle 其它聚落建立接口？
11. 哪些部分应下放给 L3 `DISTRICT`，而不是 L2 直接画死？

---

## 4. Current-world Evidence Gate

本轮从区域规划进入 settlement 定址，必须刷新必要的 current-world evidence。

要求：

- 先用 accepted L1 S-W 与地形/通达证据生成少量候选 settlement envelope / core hypotheses；
- 对 materially affected 范围做只读 current-world 检查；
- 至少关注表层高程/坡度、水、植被、现有人造内容、主要障碍和必要浅层地下；
- 可以分阶段缩小读取范围，不 broad rescan 全世界；
- 明确 freshness、读取时间、覆盖体积和限制；
- 若发现现有可见 fabric，与历史演化逻辑一起处理，不得当成空白绿地。

---

## 5. Anti-Anchoring Firewall

Primary L2 solution freeze 前不得读取：

- 旧 N1 / G1 的规划几何和角色拆分；
- P1–P5；
- MD-001P / R1；
- MD-001S1 的 Site 推荐；
- MD-001U1 微街区；
- Middle Kit v0.1；
- 旧 first-build / corridor / building program。

先独立完成 MID-A L2 Primary 并冻结。

Freeze 后才允许做 Legacy A/B：

- 可以判断旧 G1/N1 是否在新城市内部自然重现为 district / subcenter；
- 可以复用时间绑定且范围明确的旧观测事实；
- 不得回填冻结主案；
- 不得因为已有建筑设计投入而保留旧片区。

---

## 6. Required Outputs

建议输出目录：

`minecraft/建筑师/planning/CIV-001/MIDDLE/MID-A/CIV-001-MID-A-L2P/`

至少包含：

- `README.md`
- `OWNER-SUMMARY.md`
- `L2-SETTLEMENT-PLAN.md/json`
- `SETTLEMENT-EXTENT.md/json`
- `ANCHOR-HIERARCHY.md/json`
- `GROWTH-PATH-DEPENDENCE.md`
- `MOVEMENT-PUBLIC-SPACE-SKELETON.md/json`
- `DISTRICT-FORMATION.md/json`
- `DENSITY-LAND-USE.md/json`
- `BUILDING-DEMAND.md/json`
- `SETTLEMENT-SERVICES.md/json`
- `ARCHITECTURE-KIT-REQUIREMENTS.md/json`
- `RESILIENCE-DEPENDENCIES.md`
- `evidence/`
- `validation/PRIMARY-FREEZE.json`
- `validation/PLANNER-CRITIC.md`
- `LEGACY-COMPARISON.md`（Freeze 后）
- 地图 / 图示：城市范围候选、Anchor/生长、movement/public space、district formation、密度/功能关系等

### L3 handoff

为需要继续规划的 district / quarter 输出 L3 recursive packages。

不得直接创建 Builder Design Package。

---

## 7. Planning Quality Gate

提交前至少检查：

- 门户繁华是否来自因果关系，而不是 Owner 标签机械涂色；
- MID-A 整体是否真的表现为联盟最高城市密度，而不是只有一个高密点；
- 高密是否仍保留供水、消防、排水、装卸、维护与公共生活；
- 是否避免现代单功能 zoning；
- district 是否来自历史、movement、rights、externalities 与地形；
- 是否真正解释“为什么这里是城市核心”；
- 是否让 gateway 属于一座城市而不是偷偷重新制造 G1；
- 是否没有越级画 parcel / building；
- 是否保留 L3 足够设计自由度；
- `world writes = 0`。

---

## 8. Stop Rule

完成后：

1. Primary Freeze；
2. Freeze 后做 Legacy comparison；
3. commit + push `assets/main`；
4. 核对远端 HEAD；
5. 停止交 GPT + Owner 审核。

不得自动执行任何 L3，不调用 Builder，不施工。
