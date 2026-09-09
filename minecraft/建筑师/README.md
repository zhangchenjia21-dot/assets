# 建筑师｜Minecraft Fantasy World Build

本目录是存档 **`建筑师`** 的长期项目工作区与事实入口。

项目不是“随机让 AI 在地图上造漂亮建筑”，而是先理解已经存在的世界地形，再建立奇幻世界 Canon、建筑语言和聚落逻辑，最后让每次建造成为同一个世界历史的一部分。

## Current Stage

```text
Project placement / governance = PASS
Natural Geography Survey V1 = ACCEPTED BASELINE
Survey Artifact Status = PARTIAL
Local high-resolution / safe visual review = NEXT, NOT AUTHORIZED
World Canon = NOT STARTED
Architecture Bible = NOT STARTED
Build planning = HOLD
```

V1 基础事实：Minecraft 26.2 / DataVersion 4903；主世界完整生成范围约 X=-6224～3807、Z=-6544～3487；393,129 个 `full` 区块形成连续矩形。V1 使用 64 格粗网格，24,964 个采样单元、124,820 根采样柱。高级地貌识别仍是候选，不是世界 Canon。

## AI Start here

1. 读仓库根 `AGENTS.md`；
2. 读本目录 `AGENTS.md`；
3. 读 `current/README.md`；
4. 读 `current/项目状态.md`；
5. 按任务再读取 `current/世界构建原则.md`、`current/建造原则.md`、`current/开发路线.md`；
6. 自然地理问题读取 `research/natural-geography/` 与 `architecture/地理事实层与空间ID契约.md`；
7. 只有 Owner-approved 世界设定才进入 `world/`；
8. 具体落地项目进入 `builds/`。

## Repository map

| 路径 | 角色 | Authority |
|---|---|---|
| `current/` | 当前目标、状态、原则与高层路线 | **当前项目入口** |
| `decisions/` | Owner 明确裁定 | Decision Authority |
| `architecture/` | 数据契约、空间事实层、未来工具/建造系统协议 | Architecture Authority |
| `research/` | 自然地理调查、历史/现实参考、技术验证 | Evidence；不自动成为 Canon |
| `discussion/` | Owner 明确要求保存的未批准草案 | 非 Authority |
| `world/` | Owner 批准后的世界 Canon / World Bible | World Canon Authority |
| `builds/` | 已规划 / 已实施建筑与聚落的 site-specific 记录 | Build Record |
| `99_归档/` | superseded / historical | 历史证据 |

## 核心边界

> **先读世界，再写世界。**

Minecraft 存档是自然地理原始事实源。粗扫描产生的算法分类是索引和候选，而不是自动生成的国家、历史或文明。

> **结构化事实层优先，Markdown / 地图是阅读视图。**

> **Research 不等于 Canon；Canon 必须经过 Owner 明确批准。**
