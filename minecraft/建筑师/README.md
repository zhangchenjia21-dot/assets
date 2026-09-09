# 建筑师｜Minecraft Fantasy World Build

本目录是存档 **`建筑师`** 的长期项目工作区与事实入口。

项目不是“随机让 AI 在地图上造漂亮建筑”，而是先理解已经存在的世界地形，再建立奇幻世界 Canon、建筑语言和聚落逻辑，最后让每次建造成为同一个世界历史的一部分。

## Current Stage

```text
Project placement / governance = PASS
Natural Geography Survey V1 = ACCEPTED COARSE BASELINE / ARTIFACT PARTIAL
NG-2 Representative Local Refinement = PASS_WITH_NOTES / EVIDENCE ACCEPTED
Safe in-game visual review = BLOCKED_BY_SAFE_ENVIRONMENT
NG-3 Natural Atlas Consolidation = AUTHORIZED / DISPATCH READY
World Canon = NOT STARTED / NOT AUTHORIZED
Architecture Bible = NOT STARTED / NOT AUTHORIZED
Build planning = HOLD
```

当前 Active Task：

`tasks/NG-003/TASK.md`

NG-3 的目标是把 V1 global coarse evidence + NG-2 calibration/counterexamples 收敛成机器可查询的 Proposed Consolidated Natural Atlas。新 Atlas 使用 `NGEO / NHYD / NFEAT / NSITE` 稳定命名空间，并与历史 V1 `GEO / HYD / FEAT / SITE` survey ID 保持 lineage，而不是直接复用。

V1 基础事实：Minecraft 26.2 / DataVersion 4903；主世界完整生成范围约 X=-6224～3807、Z=-6544～3487；393,129 个 `full` 区块形成连续矩形。V1 使用 64 格粗网格，24,964 个采样单元、124,820 根采样柱。

NG-2 已对 8 类代表目标完成局部高分辨率校准：6 个局部 CONFIRMED、2 个 RECLASSIFIED；这些结果是 calibration evidence，不是 V1 全局 detector 准确率。

## AI Start here

1. 读仓库根 `AGENTS.md`；
2. 读本目录 `AGENTS.md`；
3. 读 `current/README.md`；
4. 读 `current/项目状态.md`；
5. 若有 Active Task，读取对应 `tasks/<ID>/TASK.md`；
6. 按任务再读取相关 `current/`、`decisions/`、`architecture/`、`research/`；
7. 只有 Owner-approved 世界设定才进入 `world/`；
8. 具体落地项目进入 `builds/`。

## Repository map

| 路径 | 角色 | Authority |
|---|---|---|
| `current/` | 当前目标、状态、原则与高层路线 | **当前项目入口** |
| `tasks/` | 已授权 executable Task Packet / Completion | Active execution scope |
| `decisions/` | Owner 明确裁定 | Decision Authority |
| `architecture/` | 数据契约、空间事实层、Atlas/未来建造系统协议 | Architecture Authority |
| `research/` | 自然地理调查、校准、Atlas proposal、历史/现实参考、技术验证 | Evidence；不自动成为 Canon |
| `discussion/` | Owner 明确要求保存的未批准草案 | 非 Authority |
| `world/` | Owner 批准后的世界 Canon / World Bible | World Canon Authority |
| `builds/` | 已规划 / 已实施建筑与聚落的 site-specific 记录 | Build Record |
| `99_归档/` | superseded / historical | 历史证据 |

## 核心边界

> **先读世界，再写世界。**

Minecraft 存档是自然地理原始事实源。Survey、refinement 和 Consolidated Atlas 都必须保留 provenance / freshness；不能自动生成国家、历史或文明。

> **结构化事实层优先，Markdown / 地图是阅读视图。**

> **Research / Natural Atlas 不等于 World Canon；Canon 必须经过 Owner 明确批准。**
