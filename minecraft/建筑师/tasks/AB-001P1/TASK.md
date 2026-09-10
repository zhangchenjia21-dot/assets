# AB-001P1｜Three-seat Council Center-island Site Gate

状态：**AUTHORIZED / DISPATCH READY**

授权：`../../decisions/D-015_AB-001P1三席议会中心岛SiteGate授权.md`

## 0. 任务定位

本任务只负责把 Owner 所称 **“西部平岛的中心岛”** 转换成可靠的机器空间对应，并形成足够支持三席议事大厅设计的局部 Site Context。

不是建筑设计任务，不是施工任务。

`world writes = 0`。

---

## 1. 必读

至少读取：

1. `minecraft/建筑师/AGENTS.md`
2. `minecraft/建筑师/current/项目状态.md`
3. `minecraft/建筑师/current/建造原则.md`
4. `minecraft/建筑师/decisions/D-014_CIV-001最小文明Canon收敛与AB-001进入.md`
5. `minecraft/建筑师/decisions/D-015_AB-001P1三席议会中心岛SiteGate授权.md`
6. `minecraft/建筑师/world/civilizations/CIV-001/README.md`
7. `minecraft/建筑师/architecture/civilizations/CIV-001/Architecture-Grammar.md`
8. `minecraft/建筑师/research/human-geography/southern-island/WB-002R-R1/README.md`
9. `minecraft/建筑师/research/human-geography/southern-island/WB-003R/README.md`
10. 本 Task Packet

如调用通用 Minecraft 设计 Skill，使用 `Vibe-Coding/skill/codex/minecraft-builder/SKILL.md` 当前版本；但本轮只做 Site Gate，不进入建筑方案。

---

## 2. Owner Referent

Owner 原话语义：

> 三席议会相关建筑优先安排在 **西部平岛的中心岛**。

当前治理状态：

`OWNER_REFERENT / COORDINATE_TBD`

不得把历史研究中的某个 component / SIRZ / crossing endpoint 自动视为答案。

先利用现有地图与 topology 判断这个称呼最可能对应什么空间对象；必要时再对少量候选做 current-world read-only 局部核验。

---

## 3. Mapping Strategy

优先顺序：

```text
existing R1 topology / maps
→ WB-003R spatial context
→ spatial interpretation of "west flat island / center island"
→ bounded current-world local verification
```

禁止重新扫描整个南部岛屿群。

### 3.1 候选识别

候选必须记录：

- candidate ID；
- actual bounds / geometry reference；
- component / parent-landmass relation；
- 与西部 C 形低岛、东岛西伸低地、附近水面的关系；
- 为什么可能对应 Owner 的“中心岛”；
- 为什么可能不是；
- mapping confidence。

如果存在多个合理候选，不得通过主观偏好静默选一个。

### 3.2 Mapping Verdict

最终只允许：

- `UNIQUE_MAPPING_SUPPORTED`
- `OWNER_SELECTION_REQUIRED`
- `INSUFFICIENT_EVIDENCE`

---

## 4. Site Context

如果存在唯一高置信 mapping，或对每个候选都可低成本生成 Site Context，则至少整理：

### Terrain

- local bounds；
- elevation min / median / max；
- relief / slope；
-主要平缓区；
- 不得把“平缓区”直接变成整地授权。

### Shore / Water

- 岸线方向；
- 邻近水体；
- 岸边高差；
- 可到达水岸 proxy；
- 不宣称港口 / 航运能力。

### Scale

- 连续可用空间的大致尺度；
- 适合单座三席议事大厅还是未来建筑群的空间余量；
- 不要求把整个岛都变成政治中心。

### Access

- 当前自然进入方向候选；
- 与西域主体、跨岛方向的几何关系；
- 不规划正式道路 / 桥 / 渡口。

### Views / Skyline

至少识别：

- 主要外部视线方向；
- 从水面 / 对岸 / 岛内进入时的潜在视觉关系；
- 东部山地主岛是否可成为背景；
- 未来建筑天际线可能受哪些地形约束。

### Existing Surface

- vegetation structure；
-已有人工 block / path / structure / waystone 等；
- 是否存在需要保留或未来清理的显著对象。

不要为此修改世界。

---

## 5. Design-readiness Assessment

对唯一 Site 或每个候选输出：

- `SITE_DESIGN_READY`
- `READY_WITH_LIMITATIONS`
- `NOT_READY`

并说明：

1. 是否足够开始三席议事大厅 Plan / Section / Sequence；
2. 最大设计约束；
3. 哪些问题应在建筑设计中解决；
4. 哪些问题必须在 world-write 前再次确认。

这不是选出“最好地块”的打分比赛，而是判断 Owner referent 是否被可靠识别、是否可进入设计。

---

## 6. Deliverables

放到：

`minecraft/建筑师/research/build-sites/CIV-001/AB-001P1/`

建议：

```text
README.md
site-mapping.json
site-context.json              # UNIQUE 时
site-candidates.json           # 多候选时
reports/中心岛SiteGate.md
visual/site-context.png        # 轻量等比例图，若有帮助
validation/source-audit.json
review/index.json
```

可按真实结果删减 / 合并。

若需要本地大数据，遵守 D-010；但本任务原则上应主要复用既有轻量事实，不应产生大包。

---

## 7. Validation

至少检查：

- current world freshness；
- R1 / WB-003R evidence lineage；
- candidate geometry 与 existing topology 一致；
- bounds / elevation / water / vegetation 关键值可追溯；
- 若做 current-world targeted read，记录 source provenance；
- task 期间 world unchanged；
- `world writes = 0`；
- 前序 evidence / World Canon / Architecture Grammar immutable。

---

## 8. Strict Prohibitions

不得：

- world write；
- 开始建三席议事大厅；
- 推平场地；
- 清除植被；
- 创建道路 / 桥 / 码头；
- 修改 CIV-001 Canon；
- 修改 AB-001 Grammar；
- 把候选 Site 自动提升为 Build authorization；
- 设计整个联盟政治中心。

---

## 9. Completion / Stop

完成后：

- `minecraft/建筑师/tasks/AB-001P1/COMPLETION.md`
- `minecraft/建筑师/research/build-sites/CIV-001/AB-001P1/`
- current 机械更新为 implementation completed / awaiting review；
- commit + push `assets/main`；
- 核对远端 HEAD；
- 停止交 GPT 独立审核 / Owner mapping confirmation。

如果 verdict = `OWNER_SELECTION_REQUIRED`，必须停止等待 Owner 选择，不自行进入 Architecture Design。
