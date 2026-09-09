# NG-003 Completion

状态：**PASS-CANDIDATE / READY FOR INDEPENDENT REVIEW**。Implementation completed，等待 GPT 独立审核；不宣告 NG-3 Stage PASS。

## 执行与交付

- Execution base：`166515fe12ac7f5edd2dd04bccefa49f4e8b0951`，当时的 `assets/main`。
- 提交前已核对 main 前进至 `9f04e8947b38ed0001471d98efc9b791e9f9e310`，保留江南水园并行提交（`0214f6e`、`62ebb1e`、`9f04e89`）。本任务不改该项目。
- Final implementation commit：承载本报告的提交，主题 `NG-003: consolidate proposed natural atlas and query evidence`；精确 SHA 由 `git log -1 --format=%H -- minecraft/建筑师/tasks/NG-003/COMPLETION.md` 查询，推送后在交接消息提供并与远端 HEAD 核对。报告不预填尚未生成的自身 commit hash。
- 成果入口：[NG-3 README](../../research/natural-geography/NG-3/README.md)；主查询层 [atlas.sqlite](../../research/natural-geography/NG-3/raw-or-queryable/atlas.sqlite)。仅机械更新 current 状态，未更新 top-level Atlas authority。

## Freshness 与只读边界

`CURRENT_MATCH`，LevelName 建筑师，DataVersion 4903。552 个 Overworld region 与 V1 / NG-2 的 inventory 和 SHA256 相同；新增、删除、变化均为 0。

初始检查 2026-09-09 06:48:14 UTC；最终封口 07:31:35 UTC。最终结果 `V1_NG2_immutable=true`、`world_unchanged_since_start=true`、`world_inventory_before_after_equal=true`。完整世界、V1、NG-2（含忽略的本地 SQLite）均纳入指纹；核验期间持 Win32 只读共享句柄。证据见 [final-source-audit.json](../../research/natural-geography/NG-3/validation/final-source-audit.json) 及 manifest 初始清单。

**world writes = 0**。没有启动 Minecraft / executor / Bridge，没有修改 region、NBT、实体、玩家、level.dat，没有安装或恢复 Observation 环境。安全游戏内视觉审核仍是既有 `BLOCKED_BY_SAFE_ENVIRONMENT`，本轮地图是离线派生视图。

## Atlas 内容

| family | 数量 |
|---|---:|
| NGEO | 35 |
| NHYD | 20 |
| NFEAT | 4 |
| NSITE | 8 |

全部 67 个 ID 为 PROPOSED。18 SUPPORTED、49 PROVISIONAL，65 个 requires_refinement。未归并 248 个陆地 cells + 676 个水域 cells；没有把这些碎片伪装成边界明确的新对象。UNRESOLVED 对象数为 0，但未知通过 cell 标志与每对象 boundary/topology/semantic 字段保存。

宏观骨架为东西山体、两侧山前高地与中北部低地镶嵌体；35 个区域是高程/起伏、水域阻隔、连续性数值候选加显式模型解释的结果，不按 terrain 字符串直接合并。边界仍是 64 格近似；已核实南部岛屿改用 NG-2 实际成员。

Schema `natural-atlas/1.0`，算法 `ng3-consolidation/1.0`。SQLite 5,664,768 bytes，13,565 geometry runs；不复制 NG-2 500 万根柱。单文件远低于 GitHub 限制，直接发布 SQLite，无压缩归档，archive round-trip 不适用；SHA256 与 integrity check 已核验。V1 解压缓存仅在 NG-3 忽略目录。

稳定 ID 采用 stable_key + geometry_signature ledger；相同输入重建保留 ID，形状漂移与退休 ID 重用拒绝。未来 matching 使用成员重叠和 evidence lineage 作为证据，再明确裁定身份延续或拆并；不自动重编号。拆并须新 ID / predecessor lineage，退休 ID 不回收，详见 [查询与更新契约](../../research/natural-geography/NG-3/tooling/查询与更新契约.md)。

## 校准与保留未知

八条 NG-2 calibration 均进入机器层及 context。SITE-005 保持山前缓坡重分类；SITE-019 建立真实开放分支水道 NHYD-015，不重升为湖。SITE-002 仅局部浅鞍部；SITE-011 仅多出口 embayment 点，不推断天然港。没有用 6/8 推算全局 detector 准确率。

17 个粗水域维持 PROVISIONAL；3 个真实水面分量仅在 NG-2 ROI 内有支持。`connected_to` 类型可用但本轮不建立全局真实连通边；粗邻接与局部 overlap 明确不是水道连通。所有 NHYD `flow_direction=unknown`；没有流域、上下游、流量等生成字段。NSITE 均需继续观察和另行 world-write 授权。

Targeted refinement **0 / 12**。现有数据足以形成保留未知的宏观骨架；未确认的全球水域/岛屿/山口没有被晋升，因此未额外扫世界。最大未知仍为全球真实水系连通、精确分区边界与未归并小斑块。

## 验证

- [automated.json](../../research/natural-geography/NG-3/validation/automated.json)：681 项断言通过。覆盖 5 个 CLI（含 `python -S` 标准库运行）、确定 JSON、错误路径、150 个固定种子随机坐标、负坐标/范围边界/水点、NG-2 独立 NPZ 水陆掩膜与 bbox 内间隙、context 实际成员距离。
- 对象/lineage/evidence_status、JSONL 与数据库一致、关系无悬空、ID/key 唯一、漂移/退休回收拒绝、两处重分类及语义限制、SQLite integrity 和 SHA256 均通过。
- [rebuild.json](../../research/natural-geography/NG-3/validation/rebuild.json)：两次完整汇编的 SQLite、ID ledger、对象及关系导出字节一致。初次复核发现 ledger 插入顺序使 SQLite 页顺序变化，已固定按 ID 排序后通过。
- Python AST 语法/向下依赖检查通过；本工具模块无跨 NG-2 内层引用。公开 L3 入口有契约说明，中文业务文件与注释；Bootstrap/tests 属工程外围。
- 五张最终地图人工检查，修复水域长标签与 overlap 线显示；范围、X/Z 方向、PROPOSED ID 与精度警告可见。抽查山体、岛屿、分支水道、浅鞍部、海湾的地图/导出与机器层一致。该执行者自检不代替 GPT 独立审核。

## 停止点

没有进入 World Canon、Architecture Bible、建筑规划或 Build；没有写入 `world/` / `builds/`。后续仅建议 GPT 独立审核 Proposed Atlas，尤其关注宏观区域解释和未知水域拓扑的保留是否充分；不自行授权下一阶段。
