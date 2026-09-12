# MD-001P-R1｜P1 Gateway Settlement Revision

状态：**AUTHORIZED / DISPATCH READY**
日期：2026-09-12

## 0. 任务定位

对已完成的 `MD-001P` 做一次**定向总体规划修订**。

这不是重做整个中域总规，也不是建筑设计任务。

唯一核心问题：

> 原方案是否低估了 P1 connector 的聚落价值？如何把它升级为有常住生活的门户聚落，同时不堵塞政治/交通接口、不侵入 Commons、也不削弱 N1 主镇？

`world writes = 0`。

正式决策：

`minecraft/建筑师/decisions/D-026_P1连接带升级为中域门户聚落并修订MD-001P.md`

---

## 1. 必读

至少读取：

1. `minecraft/建筑师/current/项目状态.md`
2. `minecraft/建筑师/decisions/D-026_P1连接带升级为中域门户聚落并修订MD-001P.md`
3. `minecraft/建筑师/decisions/D-025_三域聚落密度与土地利用梯度.md`
4. `minecraft/建筑师/planning/CIV-001/MIDDLE/MD-001P/MASTERPLAN.md`
5. `minecraft/建筑师/planning/CIV-001/MIDDLE/MD-001P/subareas.json`
6. `minecraft/建筑师/planning/CIV-001/MIDDLE/MD-001P/settlement-nodes.json`
7. `minecraft/建筑师/planning/CIV-001/MIDDLE/MD-001P/human-use-intensity.json`
8. `minecraft/建筑师/planning/CIV-001/MIDDLE/MD-001P/land-use.json`
9. `minecraft/建筑师/planning/CIV-001/MIDDLE/MD-001P/movement-network.json`
10. `minecraft/建筑师/planning/CIV-001/MIDDLE/MD-001P/resident-life-system.json`
11. `minecraft/建筑师/planning/CIV-001/MIDDLE/MD-001P/first-build-recommendation.md`
12. `minecraft/建筑师/planning/CIV-001/MIDDLE/MD-001P/独立审核.md`
13. TT-002R revision 154 territory baseline。

---

## 2. Locked Baseline

以下保持不变：

- Middle total = 391,002 blocks²；
- revision 154 political geometry；
- Alliance Commons = 92,124；
- accepted connector P1 geometry = 13,661；
- P2–P5 基本地形分区；
- N1 principal hub 的存在；
- N2 / N3 / N4 的大体角色；
- East interfaces 的政治位置；
- `world writes = 0`。

不得为了给 P1 腾位置修改领土边界。

---

## 3. P1 Evidence

当前 P1：

```text
area = 13,661
bounds = X 89..240, Z 1664..1841
median Y = 64
median slope8 = 0.0625
median relief32 = 3
FLAT/GENTLE = 10,123 columns (~74%)
shore columns = 399
```

原 MD-001P 把全部 P1 作为 `connector 通行公用带`，并定义为“高通行、低覆盖”。

Owner 已明确认为该处理过于保守。

---

## 4. 必须重新规划 P1 内部

P1 不应被整体视作一种 land-use。

必须在真实地形上至少区分：

### A. Interface Threshold / 政治与通行阈值

靠近 X=89 accepted cut 的直接界面。

目标：

- 保持通行；
- 视线 / 避让 / 集散；
- 不用建筑把最窄政治接口堵死；
- 可有界石、告示、迎候等未来可能性，但不要自动创造收费关卡制度。

### B. Gateway Settlement / 门户街市与常住社区

在 P1 向东扩宽、真实平缓且不冲突的地带，规划一个**紧凑、有居民的门户节点**。

至少考虑：

- 短途交易；
- 小仓 / 临时周转；
- 车马 / 驮运停驻；
- 修理；
- 旅宿 / 饮食；
- 日用品；
- 向导 / 消息 / 告示；
- 常住经营者及家庭；
- 地方性小公共服务。

必须表现为真实社区，不是物流设施带。

### C. Shore / Drainage / Open Structure

保留必要岸线、排水、结构性植被、维护与地形缓冲。

---

## 5. P1 与 N1 的双节点关系

必须回答：

> 为什么 P1 门户节点和 N1 主镇都存在，而不是二选一？

原则：

- P1 = immediate gateway economy / short stay / short storage / transport turnover / portal life；
- N1 = deeper market / larger storage / processing / public life / long-term commercial network / denser urban community。

两者应形成：

> **Gateway → Principal Hub**

的连续城市化关系。

不得：

- 把 P1 升成比 N1 更大的新主城；
- 让 P1 与 N1 功能完全重复；
- 让 P1 线性建筑连续堵满 connector；
- 让 N1 因 P1 存在而失去主镇逻辑。

---

## 6. Settlement Hierarchy 修订

建议新增专门节点 ID，例如：

- `G1` / `N0` / 其它清晰命名

但命名可由你选择。

它至少应标记为：

- `gateway settlement / portal quarter / secondary-specialized node`

需要给出：

- exact planning envelope；
- terrain metrics；
- intended building coverage range；
- resident roles；
- service roles；
-与 N1 的互补关系。

不要把整个 13,661 P1 当作 settlement envelope。

---

## 7. Density / Land-use 修订

必须重新计算：

- P1 内各 land-use 面积；
- 新门户节点对 Middle territory-wide mature footprint 的影响；
- Middle > West > East 的 D-025 逻辑是否更清楚；
- connector narrow threshold 仍然保持低覆盖；
- P1 widening 部分可以成为中高强度混合街区。

不要为了提高数字而机械加建筑。

---

## 8. Movement Network 修订

原 R1 `Commons connector ↔ N1` 不应再只是“穿过 P1 的单条 corridor”。

应重新表达为：

- Commons interface → Gateway settlement → N1 principal hub

但仍然：

- corridor ≠ existing road；
- 不冻结像素折线为街道；
- 不设计完整道路施工；
- 保留政治界面畅通。

如需要，可以把原 R1 拆成两个规划段或一个带节点的 corridor chain。

---

## 9. First-build Recommendation 必须重审

原推荐：

> N1 公共秤验与小仓院

P1 升级后，这个推荐**不能自动保留**。

必须重新比较：

- 在 P1 gateway 做首栋；
- 在 N1 做首栋；
- 两者各自作为 CIV-001 第一座地方建筑样板的优劣。

尤其考虑：

- 秤验 / 短仓是否更自然地靠近门户；
- 若太靠政治边界，会不会误读成 customs / toll house；
- 哪个 Site 更能同时表达“中域高密混合生活”而不是单一物流功能。

最终给 1 个推荐 + 最多 2 个备选，但不冻结建筑尺寸或 Site。

---

## 10. Required Deliverables

直接修订 MD-001P 正式成果，保留 lineage。

至少更新：

```text
planning/CIV-001/MIDDLE/MD-001P/MASTERPLAN.md
planning/CIV-001/MIDDLE/MD-001P/MASTERPLAN.json
planning/CIV-001/MIDDLE/MD-001P/subareas.json
planning/CIV-001/MIDDLE/MD-001P/settlement-nodes.json
planning/CIV-001/MIDDLE/MD-001P/human-use-intensity.json
planning/CIV-001/MIDDLE/MD-001P/land-use.json
planning/CIV-001/MIDDLE/MD-001P/movement-network.json
planning/CIV-001/MIDDLE/MD-001P/resident-life-system.json
planning/CIV-001/MIDDLE/MD-001P/first-build-recommendation.md
planning/CIV-001/MIDDLE/MD-001P/validation/*
planning/CIV-001/MIDDLE/MD-001P/visual/* relevant maps
```

新增：

```text
planning/CIV-001/MIDDLE/MD-001P/REVISION-R1.md
```

记录：

- 原问题；
- Owner correction；
- 改了什么；
- 哪些没改；
- 面积 / 密度变化；
- first-build recommendation 是否变化。

至少重做这些图：

- human-use-density.png
- land-use-masterplan.png
- settlement-hierarchy.png
- movement-exchange.png
- phasing-first-build.png

图上必须清楚标出 P1 gateway node，而不能只靠颜色暗示。

---

## 11. Critic

修订后检查：

- 是否从“低估 P1”走向“过度城市化 P1”；
- 是否保留政治接口与交通净空；
- 是否形成真实常住社区；
- P1 与 N1 是否互补；
- 是否仍符合 D-025；
- 是否把门户误做成现代收费站 / 物流园 / 边防城；
- 是否让示意图可以让 Owner 一眼看懂 P1 是重要规划地点。

---

## 12. 禁止

- `world writes > 0`
- 修改 territory revision 154
- 修改 Alliance Commons
- broad rescan
- 进入单体建筑设计
- 施工道路 / 聚落 / 建筑
- 自动授权 Local Site Gate

---

## 13. Completion

完成后：

- 写 `minecraft/建筑师/tasks/MD-001P-R1/COMPLETION.md`；
- commit + push `assets/main`；
- 核对远端 HEAD；
- 停止交 GPT + Owner 审核。
