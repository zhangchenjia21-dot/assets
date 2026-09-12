# REVISION_PROTOCOL — 修订协议（项目代号 H · P5）

> 强化 V4 C 路线（`AI-Test/Architecture-V4/C-critique.md`，只读参考），
> 衔接 ARCHITECT_RULEPACK / Spatial Validator / CRITIC_RULEPACK 三者。
> 机读状态机见文末附录 A（JSON）。

## 1. 流程

```text
Architect（按 ARCHITECT_RULEPACK 生成）
↓
Hard Validator（V001–V012，确定性）
↓        ├─ 任一 HARD_FAIL → 直接进 Revision（Critic 不评审带病稿件）
Critic（10 维度，判断性）
↓
Revision（按优先级修订，重生成蓝图，不只是改说明文字）
↓
Hard Validator Recheck（修订后必须复检）
↓
Final（附评审与修订记录交付，Owner 做审美终裁）
```

## 2. 硬性规则

1. **Validator fail 必须修。** 任一 HARD_FAIL 未消除不得进入 Final；WARNING 可保留但须在交付说明中
   逐条给出理由（含"歧义阳性"情形：密封装饰空腔、天井等，引 known_limitations 对应条目）。
2. **Critic suggestion 可权衡。** severity=suggestion 的条目允许 KEEP 并写明理由；
   important 默认应改，不改需更强理由；critic 无 critical（客观必须项归 Validator）。
3. **迭代上限 ≤3 轮。** 一轮 = Critic 评审 + Revision + Validator Recheck。3 轮后仍存 important 未决项，
   停止迭代，把未决项与理由移交人工（HUMAN_REVIEW），不得无限循环。
4. **先治病再选美。** Validator 有 HARD_FAIL 的稿件不进入 Critic——评审一个客观上走不通的建筑是浪费。

## 3. 收敛判据（防止 Critic 把建筑改成完全不同的东西）

### 3.1 锚点（anchors）——修订不得改变

以下三项在首轮 Critic 前冻结，作为本次设计的身份：

| 锚点 | 定义 | 来源 |
|---|---|---|
| footprint 锚 | 包络 (x,z) 与主入口所在立面方向；允许 ±10% 的尺寸微调 | 初稿蓝图包络 |
| 风格标签锚 | brief 指定或 SS-005 声明的风格标签 | ARCHITECT_RULEPACK style_selection_rules |
| 功能分区锚 | 功能 grammar 要求的 zones 清单（围合室内有无/外部门/上层/院落）及主入口→主空间连通结构 | functional_rules.json 对应类 |

修订若需要改变任一锚点（如 Critic 建议"把住宅改成塔楼""L 形改成回字形"），**视为新设计而非修订**：
终止本轮协议，回到 Architect 重新生成（并保留原稿备查）。

### 3.2 差异阈值与回退

- 每轮 Revision 必须产出逐坐标 diff（added/removed/changed + SHA256，沿用 V4 `evidence/C-revision-diff.json` 的先例）。
- **相邻两版差异 > 30%（changed+added+removed 体素 / 前版实体体素）→ 触发回退检查**：
  评审该 diff 是否仍服务本轮 Critic 意见；若偏离（借修订之名行重设计之实），回退到前一版，
  并把超限改动拆成显式提案逐条表决（KEEP/CHANGE/ADD/REMOVE）。
- 阈值 30% 为 HEURISTIC（V4 C 的实际修订规模远低于此：降塔 3 格、退廊 1 格、局部换窗），
  无全库统计背书，可由人工按项目规模调整。

### 3.3 收敛信号

满足任一即收敛进入 Final：
1. Critic 连续一轮无 important 及以上新增意见；
2. 达到迭代上限 3 轮（未决项转人工）；
3. 相邻两版 diff < 5% 且剩余意见全部 KEEP。

## 4. 各角色交接物

| 交接 | 内容 |
|---|---|
| Architect → Validator | Canonical IR blueprint.json（schema_version=1） |
| Validator → Critic | validation_status / hard_fail_count / rules_triggered / 三个 score / diagnostics |
| Critic → Revision | 按 CRITIC_RULEPACK §3 模板的触发清单，每条带处置（CHANGE/KEEP/ADD/REMOVE） |
| Revision → Validator Recheck | 新蓝图 + revision-diff.json（含 SHA256）+ 锚点不变声明 |
| Final → Owner | 蓝图 + 验证报告 + 评审记录 + 未决项清单（若有） |

## 5. 与 V4 C 的差异说明

V4 C 是单次人工 PASS（Critic 一轮 + Revision 一轮 + MCP validate）。本协议把它制度化：
锚点冻结、diff 阈值、迭代上限、状态机均为新增；Critic 维度表沿用 V4 C 的表格习惯但映射到
CRITIC_RULEPACK 的 10 个标准维度。

## 附录 A：机读状态机（revision_protocol.statemachine.json 内嵌）

```json
{
  "version": "P5-1.0",
  "states": ["BRIEF", "ARCHITECT", "VALIDATE", "CRITIQUE", "REVISE", "REVALIDATE", "FINAL", "ESCALATE_HUMAN"],
  "initial": "BRIEF",
  "transitions": [
    {"from": "BRIEF", "to": "ARCHITECT", "guard": "style/function 标签已确认或声明（SS-005）"},
    {"from": "ARCHITECT", "to": "VALIDATE", "guard": "blueprint.json 已产出且通过 validator_precheck 自检"},
    {"from": "VALIDATE", "to": "REVISE", "guard": "hard_fail_count > 0", "note": "Validator fail 必须修，跳过 Critic"},
    {"from": "VALIDATE", "to": "CRITIQUE", "guard": "hard_fail_count == 0"},
    {"from": "CRITIQUE", "to": "FINAL", "guard": "无 important 未决项 且 suggestion 已全部 KEEP/CHANGE 表决"},
    {"from": "CRITIQUE", "to": "REVISE", "guard": "存在 CHANGE/ADD/REMOVE 处置项 且 iteration < 3"},
    {"from": "CRITIQUE", "to": "ESCALATE_HUMAN", "guard": "iteration >= 3 且仍有 important 未决项"},
    {"from": "CRITIQUE", "to": "ARCHITECT", "guard": "修订需改变锚点（footprint/风格标签/功能分区）→ 视为新设计"},
    {"from": "REVISE", "to": "REVALIDATE", "guard": "revision-diff.json 已产出（含 SHA256）且锚点不变声明成立"},
    {"from": "REVISE", "to": "REVISE", "guard": "diff_ratio > 0.30 → 回退到前一版并拆分提案", "note": "回退检查"},
    {"from": "REVALIDATE", "to": "CRITIQUE", "guard": "hard_fail_count == 0 且 iteration+1"},
    {"from": "REVALIDATE", "to": "REVISE", "guard": "hard_fail_count > 0（修订引入了新客观错误）"},
    {"from": "ESCALATE_HUMAN", "to": "FINAL", "guard": "人工裁决完成"},
    {"from": "ESCALATE_HUMAN", "to": "ARCHITECT", "guard": "人工决定重设计"}
  ],
  "anchors": {
    "footprint": {"freeze_at": "first CRITIQUE", "tolerance": "包络 (x,z) 尺寸 ±10%，主入口立面方向不变"},
    "style_label": {"freeze_at": "first CRITIQUE", "tolerance": "不可变"},
    "function_zoning": {"freeze_at": "first CRITIQUE", "tolerance": "zones 清单与主入口→主空间连通结构不可变"}
  },
  "iteration_cap": 3,
  "diff_thresholds": {"rollback_check": 0.30, "converged": 0.05},
  "threshold_basis": "HEURISTIC（无全库统计背书，可按项目调整）"
}
```
