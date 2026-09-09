# 建筑师｜Minecraft Fantasy World Build

本目录是存档 **`建筑师`** 的长期项目工作区与事实入口。

项目不是“随机让 AI 在地图上造漂亮建筑”，而是先理解真实 Minecraft 世界，再让文明、建筑和历史从实际自然条件中逐步生长出来。

## Current Stage

```text
NG-1 Coarse Survey = ACCEPTED
NG-2 Local Refinement = PASS_WITH_NOTES
NG-3 Current Natural Atlas = ACCEPTED @ 57d392d
WB-001 Fantasy Foundation = OWNER APPROVED / CANON
D-007 Region-first Civilization Rule = ACTIVE
WB-002R Western low-island evidence = ACCEPTED PARTIAL
WB-002R-R1 Whole Southern Island-group Profile = PASS_WITH_NOTES / ACCEPTED @ 5c6bffe
WB-003 Civilization Hypotheses = READY FOR OWNER DISCUSSION / NOT CANON
CIV-001 species / region assignment = TBD
D-010 Large Scan Lightweight GitHub Delivery = ACTIVE
Architecture Bible = HOLD
Build planning = HOLD
```

当前没有需要自动执行的 Codex Civilization Task。下一步先由 GPT + Owner 讨论 `WB-003`。

## 核心方法

> **先读世界，再写世界。**

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

## Current Southern Island-group Profile

R1 implementation：

`5c6bffe8efbb0a5b0f53d8dfe036e012294b9c96`

Independent Review：

`research/human-geography/southern-island/WB-002R-R1/独立审核.md`

状态：**PASS_WITH_NOTES / CURRENT HUMAN-GEOGRAPHY PLANNING EVIDENCE ACCEPTED**。

关键事实：

- final study：X=-800..2463, Z=1376..3487；
- 西部 C 形低岛：575,363 blocks²，median Y66，flat≈67.65%；
- 东部山地主岛：1,674,373 blocks²，median Y149，max Y300，flat≈5.99%；
- 东岛完整表层边界已闭合，与西岛表层不连通；
- whole dry land flat≈21.70%；
- 总体 west-low / east-high 得到支持；
- 没有证据证明唯一、稳定、恰好三分的自然硬边界。

当前只保留两个 Research reference units，不是部族 / 国家 / World Canon。

## Current Natural Atlas

Accepted snapshot：`57d392dcb6f3052fc72be039748529c4df3e6cf9`

主查询层：`research/natural-geography/NG-3/raw-or-queryable/atlas.sqlite`

Natural Atlas 不是精确施工边界、水文导航图、World Canon 或 build authorization。

## Current World Canon

全局基础：`world/global/Fantasy-Foundation.md`

已批准：

- 古老中魔多文明世界；
- 魔法真实但有约束；
- 神祇 / 神圣存在真实但不直接持续统治凡人；
- 主体技术约中世纪盛期～晚期；
- 存在局部幻想蒸汽工业；
- 人类 / 林地长生种 / 山地地下种 / 第四蒸汽关联种族槽位；
- Just-in-time Worldbuilding。

`CIV-001` 仍只是首个文明 Pilot 工作 ID，species / region assignment = TBD。

## Large Scan Delivery

Owner 已批准大型扫描交付轻量化：

- `decisions/D-010_大型扫描证据GitHub轻量化.md`
- `architecture/大型扫描数据交付与审核契约.md`

以后默认：

```text
Minecraft World
→ Local Raw Cache
→ Lightweight Review Bundle
→ GitHub
```

单次 GitHub scan delivery 目标 `<=15 MiB`；超过 25 MiB 默认需要例外授权。完整 per-column DB / dense arrays 默认不再进入 main Git history。

## AI Start here

1. 读仓库根 `AGENTS.md`；
2. 读本目录 `AGENTS.md`；
3. 读 `current/项目状态.md`；
4. 读 `current/世界构建原则.md`；
5. 读 `current/开发路线.md`；
6. 若存在 Active Task，读取对应 `tasks/<ID>/TASK.md`；
7. 文明空间分配必须经过完整 Regional Reconnaissance；
8. 大型扫描必须遵守 D-010 / Large Scan Delivery Contract；
9. 只有 Owner-approved 世界设定才能写入 `world/`；
10. 无明确 world-write 授权不得修改 `建筑师` 存档。

## Repository map

| 路径 | 角色 | Authority |
|---|---|---|
| `current/` | 当前目标、状态、原则与路线 | 当前项目入口 |
| `tasks/` | 已授权 executable Task Packet / Completion | Active execution scope |
| `decisions/` | Owner / governance 决策 | Decision Authority |
| `architecture/` | 数据、空间与交付契约 | Architecture Authority |
| `research/` | 自然地理、区域考察、参考资料与验证 | Evidence / planning baseline |
| `world/` | Owner 批准后的世界 / 文明 Canon | World Canon Authority |
| `builds/` | 已规划 / 已实施建筑记录 | Build Record |
| `99_归档/` | superseded / historical | 历史证据 |

## Next Action

> **WB-003｜Civilization Hypotheses from Region**

基于已经接受的完整南部岛屿群区域事实，由 GPT + Owner 先讨论 2～4 个受自然条件约束的文明 / 部族适应方案。未测资源只作为 hypothesis；Owner 明确批准前不进入 Canon。
