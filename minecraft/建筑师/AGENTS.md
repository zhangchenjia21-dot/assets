# AGENTS.md｜建筑师项目读写协议

本文件适用于 `assets/minecraft/建筑师/`。

## 1. 最小读取顺序

```text
assets/AGENTS.md
→ minecraft/建筑师/README.md
→ minecraft/建筑师/AGENTS.md
→ current/README.md
→ current/项目状态.md
→ 与当前问题直接相关的 current / decision / architecture / research / world / build
```

禁止用“把整个仓库全部读一遍”替代定位唯一事实源。

## 2. Canonical Owner

- 项目目的、协作模型、长期边界：`current/项目总纲.md`
- Current Stage / Status / Blocker / Next Action：`current/项目状态.md`
- 世界构建方法与 Canon Promotion 原则：`current/世界构建原则.md`
- 建筑与聚落设计 / 施工原则：`current/建造原则.md`
- 高层阶段顺序：`current/开发路线.md`
- Owner 正式裁定：`decisions/`
- 地理事实层、空间 ID、证据层级契约：`architecture/`
- 客观调查 / 参考 / validation：`research/`
- Owner 明确批准后的世界设定：`world/`
- site-specific 设计、蓝图、world-write 与验收记录：`builds/`
- superseded / historical：`99_归档/`

## 3. 自然地理 Authority

原始自然地理最高事实源始终是目标 Minecraft 存档本身。

GitHub 中已接受的 Survey 数据是该存档在特定时间、特定算法下的**可查询快照 / 索引**，不是永远不会过期的替代世界。

证据层级必须保持：

```text
Observed
→ 直接读取世界的数据

Derived
→ 从 Observed 算出的地形类别 / 连通关系 / 聚类

Interpretive
→ SITE potential 等规划线索

World Canon
→ Owner 明确批准的人文 / 历史 / 世界设定
```

禁止：

- 把 GEO / HYD / FEAT / SITE 的候选名称直接当成世界 Canon；
- 用 biome 一对一决定文明或种族；
- 因为某个 SITE 分数高就直接授权建造；
- 用粗分辨率 bounds 代替真实成员关系；
- 隐瞒 confidence / limitation。

## 4. World Canon Promotion

新的国家、文明、宗教、历史、地名、边界、首都、贸易路线等，默认先在聊天中讨论。

只有 Owner 明确批准后，才允许进入 `world/` 并成为后续任务依赖的 Canon。

Research / terrain hypothesis / GPT 建议即使保存，也只能进入 `research/` 或 Owner 明确要求的 `discussion/`。

## 5. Build Promotion

具体建造默认流程：

```text
定位 SITE / 区域
→ 现场 / 局部地形复核
→ 必要的真实历史 / 建筑参考研究
→ 单目标设计
→ Critique / Revision
→ Preview（需要时）
→ Owner / 当前任务 world-write 授权
→ Build
→ 验收
→ builds/ 登记
```

无明确 world-write 授权时，`world writes = 0`。

## 6. 任务成果归档

Owner 已授权本项目后续已完成、已验证任务默认 push 到 `zhangchenjia21-dot/assets`。

归档时：

- 研究证据进入 `research/`；
- current 长期事实只更新唯一 Owner 文件，不创建 `FINAL_v2` / `最新版2`；
- 正式决定进入 `decisions/`；
- Canon 进入 `world/`；
- 建造记录进入 `builds/`；
- 失效内容进入 `99_归档/`；
- 不把任务产物写到仓库根。

## 7. 冲突处理

用户当前明确指令 > Owner-approved current / world / decisions > 可验证世界 / 结构化事实 > architecture > research > discussion / archive > Agent 推测。

如果世界实际状态与既有 Canon / build record 冲突，不得静默拼接；先判断是世界后来被修改、记录过期，还是 Canon 需要重新裁定。
