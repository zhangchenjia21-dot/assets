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
WB-002 First Civilization Pilot = PAUSED / DESIGN RESET
WB-002R Western low-island evidence = ACCEPTED PARTIAL
WB-002R whole southern island-group profile = INCOMPLETE
WB-002R-R1 Scope Completion = AUTHORIZED / DISPATCH READY
CIV-001 species / region assignment = TBD
Architecture Bible = HOLD
Build planning = HOLD
```

当前 Active Task：

`tasks/WB-002R-R1/TASK.md`

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

## WB-002R Scope Correction

WB-002R implementation：`362b77e42e84ae7eee666b041a62f86a28c3559f`

Independent Review：

`research/human-geography/southern-island/WB-002R/独立审核.md`

其 1-block survey 对 `NGEO-009` 西侧低海拔岛体本身有效，但实现明确承认：东侧还有更高主要陆体，触碰 ROI 东边界且完整范围被截断。

因此现有调查只能作为 **western low-island partial evidence**，不能代表 Owner 真人考察中的整个南部岛屿群。

### R1

Decision：

`decisions/D-009_WB-002R-R1南部岛屿群范围补全授权.md`

Task：

`tasks/WB-002R-R1/TASK.md`

R1 将复用可用西部数据，并自适应向东补齐更大山地陆体。只要主要山地陆体仍触碰 study boundary，就不能宣告 scope complete。

## Current Natural Atlas

Accepted snapshot：`57d392dcb6f3052fc72be039748529c4df3e6cf9`

主查询层：`research/natural-geography/NG-3/raw-or-queryable/atlas.sqlite`

35 NGEO / 20 NHYD / 4 NFEAT / 8 NSITE。

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

## AI Start here

1. 读仓库根 `AGENTS.md`；
2. 读本目录 `AGENTS.md`；
3. 读 `current/项目状态.md`；
4. 读 `current/世界构建原则.md`；
5. 读 `current/开发路线.md`；
6. 若有 Active Task，读取对应 `tasks/<ID>/TASK.md`；
7. 文明空间分配必须经过完整 Regional Reconnaissance；
8. 只有 Owner-approved 世界设定才能写入 `world/`；
9. 无明确 world-write 授权不得修改 `建筑师` 存档。

## Repository map

| 路径 | 角色 | Authority |
|---|---|---|
| `current/` | 当前目标、状态、原则与路线 | 当前项目入口 |
| `tasks/` | 已授权 executable Task Packet / Completion | Active execution scope |
| `decisions/` | Owner / governance 决策 | Decision Authority |
| `architecture/` | 数据契约、Atlas / 建筑规则 | Architecture Authority |
| `research/` | 自然地理、区域考察、参考资料与验证 | Evidence / planning baseline |
| `world/` | Owner 批准后的世界 / 文明 Canon | World Canon Authority |
| `builds/` | 已规划 / 已实施建筑记录 | Build Record |
| `99_归档/` | superseded / historical | 历史证据 |

## Next Action

> **执行 WB-002R-R1。**

R1 完成并独立审核通过后，才进入 `WB-003｜Civilization Hypotheses from Region`。
