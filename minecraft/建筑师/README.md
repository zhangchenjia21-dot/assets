# 建筑师｜Minecraft Fantasy World Build

本目录是存档 **`建筑师`** 的长期项目工作区与事实入口。

项目不是“随机让 AI 在地图上造漂亮建筑”，而是先理解真实 Minecraft 世界，再让文明、建筑和历史从实际自然条件中逐步生长出来。

## Current Stage

```text
NG-1 Coarse Survey = ACCEPTED
NG-2 Local Refinement = PASS_WITH_NOTES
NG-3 Current Natural Atlas = ACCEPTED @ 57d392d
WB-001 Fantasy Foundation = OWNER APPROVED / CANON
D-006 Southern Island Woodland Long-lived CIV-001 anchor = SUPERSEDED
D-007 Region-first Civilization Rule = ACTIVE
WB-002 First Civilization Pilot = PAUSED / DESIGN RESET
WB-002R Southern Island Regional Reconnaissance = AUTHORIZED / DISPATCH READY
CIV-001 species / region assignment = TBD
Architecture Bible = HOLD
Build planning = HOLD
```

当前 Active Task：

`tasks/WB-002R/TASK.md`

## 核心方法

> **先读世界，再写世界。**

当前正式流程：

```text
Current Natural Atlas
→ Regional Reconnaissance
→ Regional Natural Profile
→ civilization / species hypotheses
→ Owner approval
→ World Canon
→ Architecture Grammar
→ local Build site observation
→ authorized world write
```

Atlas 负责宏观筛选，不直接决定文明。

## Current Natural Atlas

Accepted snapshot：

`57d392dcb6f3052fc72be039748529c4df3e6cf9`

主查询层：

`research/natural-geography/NG-3/raw-or-queryable/atlas.sqlite`

当前对象：35 `NGEO` / 20 `NHYD` / 4 `NFEAT` / 8 `NSITE`。

Natural Atlas 不是精确施工边界、水文导航图、World Canon 或 build authorization。

## Current World Canon

全局基础：

`world/global/Fantasy-Foundation.md`

已批准：

- 古老中魔多文明世界；
- 魔法真实但有约束；
- 神祇 / 神圣存在真实但不直接持续统治凡人；
- 主体技术约中世纪盛期～晚期；
- 存在局部幻想蒸汽工业；
- 人类 / 林地长生种 / 山地地下种 / 第四蒸汽关联种族槽位；
- Just-in-time Worldbuilding。

### CIV-001

`world/civilizations/CIV-001/README.md`

`CIV-001` 保留为首个文明 Pilot 工作 ID，但原先“南部大岛 = 林地长生种文明”的指定已经被 `D-007` 撤销。

当前 species / region assignment 均为 TBD。

## WB-002R｜Southern Island Regional Reconnaissance

Authorization：

`decisions/D-008_WB-002R南部大岛区域精查授权.md`

Task：

`tasks/WB-002R/TASK.md`

Owner 实地证据：

`research/human-geography/southern-island/Owner实地考察_2026-09-09.md`

本轮让 Codex 只读结构化：

- biome；
- elevation / slope / relief；
- low-relief / gentle-slope；
- vegetation structure；
- land / water topology；
- internal natural zones；
- Owner 五项实地观察的独立核验。

不强制得出“三个区域”；不创建文明 / 部族 / 政治事实；`world writes = 0`。

## AI Start here

1. 读仓库根 `AGENTS.md`；
2. 读本目录 `AGENTS.md`；
3. 读 `current/项目状态.md`；
4. 读 `current/世界构建原则.md`；
5. 读 `current/开发路线.md`；
6. 若有 Active Task，读取对应 `tasks/<ID>/TASK.md`；
7. 按阶段读取相关 `decisions/`、`world/`、`architecture/`、`research/`；
8. 自然地理优先使用 Current Natural Atlas，并保留 lineage / uncertainty；
9. 文明空间分配必须经过 Regional Reconnaissance；
10. 只有 Owner-approved 世界设定才能写入 `world/`；
11. 无明确 world-write 授权不得修改 `建筑师` 存档。

## Repository map

| 路径 | 角色 | Authority |
|---|---|---|
| `current/` | 当前目标、状态、原则与高层路线 | **当前项目入口** |
| `tasks/` | 已授权 executable Task Packet / Completion | Active execution scope |
| `decisions/` | Owner 明确裁定 | Decision Authority |
| `architecture/` | 数据契约、Atlas / 建筑规则与未来系统协议 | Architecture Authority |
| `research/` | 自然地理、区域考察、参考资料、校准与技术验证 | Evidence / planning baseline |
| `world/` | Owner 批准后的世界 / 文明 Canon | World Canon Authority |
| `builds/` | 已规划 / 已实施建筑与聚落记录 | Build Record |
| `99_归档/` | superseded / historical | 历史证据 |

## Next Action

> **执行 WB-002R。**

Codex 完成后交 GPT 独立审核；Regional Profile 被接受后，才进入 `WB-003｜Civilization Hypotheses from Region`。
