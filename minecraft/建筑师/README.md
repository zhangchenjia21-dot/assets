# 建筑师｜Minecraft Fantasy World Build

本目录是存档 **`建筑师`** 的长期项目工作区与事实入口。

项目不是“随机让 AI 在地图上造漂亮建筑”，而是先理解已经存在的世界地形，再建立够建造使用的奇幻世界 Canon、文明建筑语言和聚落逻辑，最后让每次建造成为同一个世界的一部分。

## Current Stage

```text
Project placement / governance = PASS
NG-1 Coarse Survey = ACCEPTED BASELINE / ARTIFACT PARTIAL
NG-2 Local Refinement = PASS_WITH_NOTES / EVIDENCE ACCEPTED
NG-3 Natural Atlas = PASS_WITH_NOTES
Current Natural Atlas planning baseline = ACCEPTED @ 57d392d
Safe in-game visual review = BLOCKED_BY_SAFE_ENVIRONMENT
WB-001 Fantasy Foundation = OWNER APPROVED / CANON ESTABLISHED
WB-002 First Civilization Pilot = ACTIVE DESIGN
CIV-001 Southern Island Woodland Long-lived Civilization = OWNER-APPROVED PILOT ANCHOR
Architecture Bible = NOT STARTED / NOT AUTHORIZED
Build planning = HOLD
```

Natural Geography 主线已经达到当前可用停点。项目现已进入 **CIV-001 第一个文明设计**。

## Current Natural Atlas

Accepted snapshot：

`57d392dcb6f3052fc72be039748529c4df3e6cf9`

主查询层：

`research/natural-geography/NG-3/raw-or-queryable/atlas.sqlite`

当前对象：35 `NGEO` / 20 `NHYD` / 4 `NFEAT` / 8 `NSITE`。

原则：

> **宏观用 Atlas，落点再精查。**

Natural Atlas 是规划底图，不是精确施工边界、水文导航图、World Canon 或 build authorization。

## Current World Canon

全局基础：

`world/global/Fantasy-Foundation.md`

第一文明：

`world/civilizations/CIV-001/README.md`

当前已批准：

- 古老中魔多文明世界；
- 魔法真实但有约束；
- 神祇 / 神圣存在真实但不直接持续统治凡人社会；
- 主体技术约中世纪盛期～晚期；
- 存在局部幻想蒸汽工业；
- 人类 / 林地长生种 / 山地地下种 / 第四蒸汽关联种族槽位；
- CIV-001 位于南部大岛 `NGEO-009`，主要智慧种为林地长生种。

其余文明细节继续采用 Just-in-time Worldbuilding，不提前写完整百科。

## AI Start here

1. 读仓库根 `AGENTS.md`；
2. 读本目录 `AGENTS.md`；
3. 读 `current/README.md`；
4. 读 `current/项目状态.md`；
5. 按任务读取 `current/开发路线.md`、相关 `decisions/`、`world/`、`architecture/`、`research/`；
6. 自然地理优先使用 Current Natural Atlas，并保留 lineage / uncertainty；
7. 只有 Owner-approved 世界设定才能写入 `world/`；
8. 具体落地项目进入 `builds/`；
9. 无明确 world-write 授权不得修改 `建筑师` 存档。

## Repository map

| 路径 | 角色 | Authority |
|---|---|---|
| `current/` | 当前目标、状态、原则与高层路线 | **当前项目入口** |
| `tasks/` | 已授权 executable Task Packet / Completion | Active execution scope |
| `decisions/` | Owner 明确裁定 | Decision Authority |
| `architecture/` | 数据契约、Atlas / 建筑规则与未来系统协议 | Architecture Authority |
| `research/` | 自然地理、参考资料、校准与技术验证 | Evidence / planning baseline；不自动成为 Canon |
| `world/` | Owner 批准后的世界 / 文明 Canon | World Canon Authority |
| `builds/` | 已规划 / 已实施建筑与聚落记录 | Build Record |
| `99_归档/` | superseded / historical | 历史证据 |

## 当前核心边界

> **先读世界，再写世界。**

> **只写够 Minecraft 建造使用的设定。**

> **Natural Atlas 不等于 World Canon；World Canon 不等于 world-write authorization。**

## Next Action

继续设计 `CIV-001`，只收敛足够进入第一套 Architecture Grammar 的内容：

- 社会气质；
- 必要的种族生理 / 寿命；
- 自然 / 魔法关系；
- 生产与生活方式；
- 材料与技术倾向；
- 聚落与建筑空间特征。
