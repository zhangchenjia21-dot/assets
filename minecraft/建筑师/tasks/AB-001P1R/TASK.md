# AB-001P1R｜Council Commons East-Connector Boundary Fit

状态：**AUTHORIZED / DISPATCH READY**

授权：`../../decisions/D-019_AB-001P1R联盟公地东侧连接带边界拟合授权.md`

## 0. 任务定位

本任务只负责精确拟合 Candidate A 的：

```text
Alliance Commons 主体
↔
东侧连接主岛的 connector / neck
```

政治土地规则已经由 Owner 决定：

> **A 除东侧连接主岛部分外，其余主体全部为联盟公地。**

不得在 A 内再人为缩一个更小的椭圆公地。

本轮不设计建筑、不施工。

`world writes = 0`。

---

## 1. 必读

1. `minecraft/建筑师/AGENTS.md`
2. `minecraft/建筑师/current/项目状态.md`
3. `minecraft/建筑师/current/建造原则.md`
4. `minecraft/建筑师/decisions/D-018_CouncilCenterland联盟公地与中域交割.md`
5. `minecraft/建筑师/decisions/D-019_AB-001P1R联盟公地东侧连接带边界拟合授权.md`
6. `minecraft/建筑师/research/build-sites/CIV-001/AB-001P1/README.md`
7. `minecraft/建筑师/research/build-sites/CIV-001/AB-001P1/site-candidates.json`
8. `minecraft/建筑师/architecture/civilizations/CIV-001/Council-Centerland-Program-Capacity.md`
9. 本 Task Packet

---

## 2. Source / Reuse

优先直接复用：

- AB-001P1 Candidate A actual geometry；
- R1 terrain / topology cache；
- 已有 shoreline / parent-landmass evidence。

默认：

- `new world block reads = 0`
- `broad rescan = 0`

只有现有 geometry 明确不足以判断 cut line 时，才允许极小范围 read-only 补充；必须说明必要性。

---

## 3. Boundary-fit method

不要做“完美数学椭圆拟合”。

要寻找的是 A 主体自然形态中：

> **视觉中心陆体开始向右侧主岛拉成长连接带的位置。**

至少分析：

- X 方向逐带 land cross-section width；
- 北 / 南岸线收束；
- neck width 的局部极小值或明显台阶；
- 切割前后 connected components；
- terrain / elevation / relief 辅助变化；
- 从 AB-001P1 图上是否能清楚读出“主体 + 连接带”。

### 首选原则

优先选择：

1. 最小且自然的 land-neck cut；
2. cut 后西侧 Commons 保持一个大而连续的主体；
3. cut 后东侧 connector 与东部主岛保持连续；
4. 不把 A 主体边缘大块土地误切给中域；
5. 不产生细碎政治飞地。

若存在两个同样合理的 neck，只给最多 2 个候选，并明确差异；不要为了避免 Owner 选择而假装唯一。

---

## 4. Required outputs

写入：

`minecraft/建筑师/research/build-sites/CIV-001/AB-001P1R/`

至少：

```text
README.md
commons-boundary.json
commons-geometry.json        # 可用紧凑 RLE / runs
connector-geometry.json      # 可用紧凑 RLE / runs
reports/联盟公地边界拟合.md
visual/commons-connector-boundary.png
validation/summary.json
```

`commons-boundary.json` 至少记录：

- source A geometry；
- selected / candidate cut line；
- method；
- Commons area；
- Commons bounds；
- connector area；
- connector bounds；
- connectedness；
- uncertainty；
- `world_writes=0`。

---

## 5. Validation

至少检查：

- Commons ∪ connector = A actual geometry；
- Commons ∩ connector = empty；
- 无 A actual land 被遗漏；
- Commons 为单一主要连续主体；
- connector 真实接向 parent landmass 东侧 continuation；
- geometry round-trip / area count 一致；
- source hashes / lineage；
- predecessor evidence immutable；
- `world writes = 0`。

---

## 6. Strict prohibitions

不得：

- 重新决定 Owner 的政治规则；
- 在 A 内再创建第二层小椭圆公地；
- 设计三席议事大厅；
- 规划代表馆 / 广场 / 道路 / 码头；
- world write；
- 修改 CIV-001 Canon 或 AB-001 Grammar。

---

## 7. Completion / Stop

完成后：

- 写 `minecraft/建筑师/tasks/AB-001P1R/COMPLETION.md`；
- current 只机械回写 implementation completed / awaiting review；
- commit + push `assets/main`；
- 核对远端 HEAD；
- 停止交 GPT 独立审核。

P1R 完成后，GPT 先接受精确 Commons 面积并重算 Program / Capacity；AB-001P2 在此之前继续 HOLD。