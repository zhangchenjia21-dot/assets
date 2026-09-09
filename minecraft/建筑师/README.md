# 建筑师｜Minecraft Fantasy World Build

本目录是存档 **`建筑师`** 的长期项目工作区与事实入口。

项目不是“随机让 AI 在地图上造漂亮建筑”，而是先理解已经存在的世界地形，再建立奇幻世界 Canon、建筑语言和聚落逻辑，最后让每次建造成为同一个世界历史的一部分。

## Current Stage

```text
Project placement / governance = PASS
Natural Geography Survey V1 = ACCEPTED COARSE BASELINE / ARTIFACT PARTIAL
NG-2 Representative Local Refinement = PASS_WITH_NOTES / EVIDENCE ACCEPTED
NG-3 Natural Atlas Consolidation = PASS_WITH_NOTES
Current Natural Atlas planning baseline = ACCEPTED @ 57d392d
Safe in-game visual review = BLOCKED_BY_SAFE_ENVIRONMENT
WB-001 Global / Non-spatial Fantasy Canon = READY FOR OWNER AUTHORIZATION / NOT AUTHORIZED
World Canon = NOT STARTED / NOT AUTHORIZED
Architecture Bible = NOT STARTED / NOT AUTHORIZED
Build planning = HOLD
```

Natural Geography 主线已经达到当前可用停点。下一候选阶段不是继续全世界高精扫描，而是进入 **WB-001｜Global / Non-spatial Fantasy Canon**。

## Current Natural Atlas

Accepted snapshot：

`57d392dcb6f3052fc72be039748529c4df3e6cf9`

主查询层：

`research/natural-geography/NG-3/raw-or-queryable/atlas.sqlite`

当前对象：

- 35 `NGEO`
- 20 `NHYD`
- 4 `NFEAT`
- 8 `NSITE`

查询入口：

```text
coordinate
object
neighbors
search
context
```

以后宏观自然地理查询默认优先使用 Current Natural Atlas，再按 lineage / uncertainty 回溯 NG-2、V1 或原 Minecraft 世界。

注意：NG-3 交付 artifact 内部对象仍保存 `status=PROPOSED`，这是 pre-review 历史状态。独立审核已经把**整个 57d392d snapshot**接受为 Current Natural Atlas planning baseline；这不改变对象自身 `SUPPORTED / PROVISIONAL` 证据等级，也不代表 World Canon。

## Current Geography Limits

- 多数 NGEO / coarse NHYD boundary 仍是尺度化近似，不是精确施工边界；
- 全球水系 connectivity / flow direction / watershed 仍未建立；
- 65 个 Atlas object 仍需要按需 local refinement；
- safe in-game visual review 暂时不可用；
- Atlas freshness 只代表最后 gate / seal 时点，terrain region 变化后需要 refresh。

因此标准原则仍然是：

> **宏观用 Atlas，落点再精查。**

## AI Start here

1. 读仓库根 `AGENTS.md`；
2. 读本目录 `AGENTS.md`；
3. 读 `current/README.md`；
4. 读 `current/项目状态.md`；
5. 若有 Active Task，读取对应 `tasks/<ID>/TASK.md`；
6. 自然地理优先读取 `architecture/地理事实层与空间ID契约.md` 与 Current Natural Atlas；
7. 按任务再读取相关 `decisions/`、`research/`、`world/`、`builds/`；
8. 只有 Owner-approved 世界设定才进入 `world/`；
9. 具体落地项目进入 `builds/`。

## Repository map

| 路径 | 角色 | Authority |
|---|---|---|
| `current/` | 当前目标、状态、原则与高层路线 | **当前项目入口** |
| `tasks/` | 已授权 executable Task Packet / Completion | Active execution scope |
| `decisions/` | Owner 明确裁定 | Decision Authority |
| `architecture/` | 数据契约、空间事实层、Atlas / 未来建造系统协议 | Architecture Authority |
| `research/` | 自然地理调查、校准、Atlas、历史/现实参考、技术验证 | Evidence / accepted planning baseline；不自动成为 World Canon |
| `discussion/` | Owner 明确要求保存的未批准草案 | 非 Authority |
| `world/` | Owner 批准后的世界 Canon / World Bible | World Canon Authority |
| `builds/` | 已规划 / 已实施建筑与聚落的 site-specific 记录 | Build Record |
| `99_归档/` | superseded / historical | 历史证据 |

## 核心边界

> **先读世界，再写世界。**

Minecraft 存档是自然地理原始事实源。Survey、refinement 和 Consolidated Atlas 必须保留 provenance / freshness；不能自动生成国家、历史或文明。

> **结构化事实层优先，Markdown / 地图是阅读视图。**

> **Natural Atlas 不等于 World Canon；Canon 必须经过 Owner 明确批准。**

> **NSITE / terrain potential 不等于 build authorization。**

## Next Candidate Stage

`WB-001｜Global / Non-spatial Fantasy Canon`

先定义不绑定具体地图位置的：

- 世界气质；
- 宇宙观；
- 魔法规则；
- 神祇 / 宗教基线；
- 智慧种族；
- 技术与物质文化；
- 历史深度与灾变结构；
- 怪物 / 超自然生态；
- 历史知识可靠性。

随后再使用 Current Natural Atlas 推演 Human Geography hypotheses。

**WB-001 当前尚未授权。**
