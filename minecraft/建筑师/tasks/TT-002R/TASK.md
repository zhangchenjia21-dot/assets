# TT-002R｜Middle–East Terrain-Assisted Boundary Refinement

状态：**AUTHORIZED / DISPATCH READY**

决策依据：

- `../../decisions/D-023_中域东域手绘边界地形辅助精修.md`
- `../../decisions/D-020_AB-001P1R联盟公地精确边界接受.md`

## 0. 任务目标

对 Owner 已完成的三域手工分区草稿做一次**仅限 Middle ↔ East 主边界的 terrain-assisted refinement**。

目标不是重新自动分区，而是：

> 保留 Owner 的政治空间意图，用真实 elevation / relief / slope / valley / ridge structure 把手绘边界贴合到更合理的地貌过渡上。

`world writes = 0`。

---

## 1. Owner Draft Baseline

必须使用这一次 Owner 手绘草稿，而不是旧 territory 文件。

识别信息：

```text
schema = civ-territories/1
revision = 153
sourceId = 94fc4687358a9fd5dd542997538822bfdba7b83bd76c4825fd84bd0116ea3d21
```

GPT obvious-artifact cleanup 后面积：

```text
ALLIANCE_COMMONS = 92,124
WEST_DOMAIN      = 575,397
MIDDLE_DOMAIN    = 395,144
EAST_DOMAIN      = 1,194,016
UNASSIGNED       = 0
DISPUTED         = 0
```

GPT cleanup only：

- 删除一条 `WEST_DOMAIN` 误涂斜线：X=335..397, Z=2348..2390，共 63 格；
- 将 `(349,2139..2141)` 的 3 格孤立 `EAST_DOMAIN` 恢复为 Middle；
- **没有移动 Middle ↔ East 主边界**。

### Source discovery

优先在当前本地工程 / territory tool workspace 中寻找与上述 `sourceId + revision` 匹配的 `current.json` 或 Owner export。

可搜索：

- `minecraft/建筑师/tools/territory-delineation/**`
- repo working tree 中 `territories-draft*.zip`
- `data/territories/current.json`
- 当前工程相邻的 Owner export 目录

如果找到的是 cleanup 前版本，只能先应用上述 66 格确定性 cleanup，再进入 refinement。

如果无法找到**精确匹配**的 Owner draft，立即停止并报告：

> `OWNER_DRAFT_NOT_FOUND`

不得拿旧 territory 文件近似替代。

---

## 2. 必读 Evidence

至少复用：

1. `minecraft/建筑师/research/human-geography/southern-island/WB-002R-R1/`
2. `minecraft/建筑师/research/human-geography/southern-island/WB-003R/`
3. `minecraft/建筑师/research/build-sites/CIV-001/AB-001P1R/`
4. `minecraft/建筑师/world/civilizations/CIV-001/README.md`
5. `minecraft/建筑师/current/世界构建原则.md`
6. D-023

重点数据：

- elevation；
- slope8；
- relief32；
- low-relief components；
- shoreline / topology；
- terrain-cost / movement evidence；
- accepted Commons / connector geometry。

默认：

- `new world block reads = 0`
- `broad rescan = 0`

仅当现有 evidence 对某个局部段明确不足时，才允许极小范围 read-only 补查，并必须单独记录原因。

---

## 3. Locked Geometry｜绝对禁止改动

本轮必须 geometry-identical 保持：

- `ALLIANCE_COMMONS` accepted 92,124；
- Commons ↔ Middle connector 的 accepted cut；
- West Domain 主体；
- Middle / East 主边界以外的大范围 Owner assignment。

不要因为 QA 显示 East 有大量小岛/碎片，就把天然离岛或 disconnected land 自动删除、并入或重分。

---

## 4. Refinement Band

先从 Owner draft 提取 Middle ↔ East 的共享边界 edges。

仅在以下范围允许改变分类：

- **core editable band：距 Owner Middle–East boundary ≤64 blocks**；
- **diagnostic band：≤128 blocks**。

一般 refinement 应控制在 64 格内。

若某段边界偏移 >64 格：

- 必须给出连续 valley / ridge / steep break / foothill transition 的可复核 evidence；
- 在 delta report 中单独列出。

偏移 >128 格：默认禁止；停止并交 GPT / Owner 重新授权。

---

## 5. Terrain Semantics

中域与东域不是由单一海拔阈值切开。

### Middle-preferred morphology

更倾向 Middle 的地貌：

- 连续低地；
- 谷底 / 宽谷；
- 山前缓坡；
- 低地—坡麓连续交通走廊；
- 能从 connector / 西部低地自然延续的 foothill terrain。

### East-preferred morphology

更倾向 East 的地貌：

- 连续高山核心；
- 强 relief；
- 陡坡 / 山脊；
- 大块连续 mountain mass；
- 与东部高地系统明显同属一体的 spur / ridge。

### Boundary behavior

优先：

- 沿明显坡折；
- 沿山脊 / 山前过渡；
- 绕开完整连续谷底；
- 保持 valley continuity；
- 保持 mountain-core continuity。

允许：

- 谷地让 Middle 局部向东伸；
- 山脊 / 山体支脉让 East 局部向西压。

禁止：

- 数学平滑；
- 单一等高线；
- 固定 X / Z 直线；
- 仅凭 biome 自动分类；
- 为了让面积“更均衡”移动边界。

---

## 6. Method

方法可自由实现，但必须把 Owner boundary 当作 prior。

如果使用 cost / seam / optimization 方法，至少解释：

- owner-line deviation penalty；
- elevation / slope / relief 如何进入评分；
- valley / ridge continuity 如何处理；
- 为什么不会让算法远离 Owner intent。

不得只输出结果，不解释算法。

---

## 7. Required Deliverables

写入：

`minecraft/建筑师/research/human-geography/southern-island/territory-refinement/TT-002R/`

至少：

```text
README.md
baseline-owner-draft.json
refined-draft.json
boundary-delta.json
reports/中域东域边界地形精修.md
visual/before.png
visual/after.png
visual/diff.png
visual/terrain-overlay.png
validation/summary.json
validation/geometry.json
validation/source-audit.json
```

其中：

### `boundary-delta.json`

至少记录：

- changed columns count；
- Middle → East count；
- East → Middle count；
- Middle / East before-after area；
- mean / median / p90 / max displacement from Owner boundary；
- >64 block displacement segments；
- unchanged locked-area hashes / counts。

### `terrain-overlay.png`

必须能让 Owner 一眼看到：

- 原手绘线；
- 精修线；
- elevation / relief / slope 中至少一种直观底图；
- 主要 valley / ridge / foothill rationale。

### 分段解释

报告应把主边界分成约 5–12 个可理解段落，每段说明：

- 保持原线 / 向 Middle 调整 / 向 East 调整；
- 调了多少；
- 地形原因。

---

## 8. Validation

至少验证：

- Commons geometry 100% unchanged；
- accepted connector geometry 100% unchanged；
- West 主体 unchanged；
- 所有变化都在 allowed refinement band；
- 没有 UNASSIGNED hole；
- Middle / East 主体连通关系不被无意义破坏；
- 不制造新的小型政治飞地；
- total valid land coverage 守恒；
- source evidence / predecessor immutable；
- `world writes = 0`。

另外比较 refinement 前后：

- Middle side terrain statistics；
- East side terrain statistics；
- boundary 附近高程 / relief / slope separation 是否更符合 CIV-001 的 Middle-lowland/foothill vs East-mountain-core 语义。

不要求所有指标都“最大化”；Owner intent 优先。

---

## 9. Result Status

输出只能标记：

> **REFINED_DRAFT / AWAITING GPT + OWNER ACCEPTANCE**

不得自动替换 World Canon 或正式 current territory boundary。

---

## 10. Next Stage

本任务完成后停止。

GPT 独立审核 + Owner 接受后，项目**直接进入**：

> `MD-001P｜Middle Domain Detailed Master Planning`

不再插入 broad reconnaissance。

如果 MD-001P 内出现局部 evidence gap，再 Just-in-time 做极小范围 read-only 补查。

---

## 11. Completion

完成后：

- 写 `minecraft/建筑师/tasks/TT-002R/COMPLETION.md`；
- commit + push `assets/main`；
- 保留并行提交；
- 核对远端 HEAD；
- 停止交 GPT 独立审核。

`world writes = 0`。
