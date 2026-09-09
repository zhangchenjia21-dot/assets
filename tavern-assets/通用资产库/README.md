# 通用资产库｜Generic Asset Library Workspace

本目录管理跨 World Pack 可复用 Expansion 的库级 Blueprint、Version、Ownership、Dependency、Consumer、Runtime Context Contract、维护规范与审核资料。

正式 Expansion 正文仍只保存在：`../拓展包/通用拓展包/`。本目录不是 Bundle，也不复制 Expansion 正文。

## Current

- Existing Reusable Expansion：**13**
- Stable Semantic Baseline：**10**
- Generic Supernatural Candidate：**3**
- Context Contract Coverage：**13 / 13 PASS**
- Existing Expansion Retrofit：**CLOSED**
- Generic Library Context Convergence：**PASS / CLOSED**
- `EP-KINSHIP-CORE｜家族与亲缘核心 v0.1`：**PASS / AUDITED CURRENT**
- `EP-POLITICS-CORE｜政治与公共权力核心 v0.1`：**PASS / AUDITED CURRENT**
- Han Politics Migration Plan：**COMPLETE / NOT YET EXECUTED**

当前维护源：

- `通用拓展包资产库总蓝图_v1.0`
- `通用资产库_当前版本矩阵_v0.9`
- `通用资产库_RuntimeContextContract模式_v0.6`
- `通用资产库_RuntimeContextContract索引_v0.6`
- `通用资产库_维护规范_v0.8`
- `通用资产库_Shared_Foundation架构规划_v0.9`
- `通用资产库_后续发展路线_v0.9`
- `tavern-asset v1.0`

## Politics 关键结论

```text
Regime / Political Order != Government Organization
Role Holding != Public Authority
Claim != Recognition != Control != Occupation != Jurisdiction
Public Reputation != Political Recognition
Kinship != Succession Outcome
Political Agreement != Commitment Promise Lifecycle
```

Politics 不建立通用 loyalty / legitimacy / stability / control score。

## Large Relation Graph

Kinship + Politics 已形成两份独立证据，正式提升为通用 Context Rule：

```text
Large Relation Graph
→ canonical primary relations / source facts
→ Program deterministic current-relevant path / subgraph
→ owner-safe + player-safe bounded projection
→ Model only for open semantic work
```

```text
Whole Relation Graph != Model Prompt
Derived Pairwise Projection != Canonical Truth
```

## Current Next

资产语义维护线自身仍可继续执行已计划的真实消费者迁移：

> **汉末三国《政争与势力》对 `EP-POLITICS-CORE` / ORG / Kinship 的迁移。**

迁移收口后：Economy → War → Shared Foundation Convergence。

这条资产维护路线与游戏项目 Creator / Library Product 开发并行但不可混淆：资产正文仍是 canonical semantic source；产品层必须消费已冻结的统一资产协议，不得反向改写资产语义 owner。

## Archive

同一维护文档族 superseded 版本进入：`99_归档/版本历史/`。`90_审核/` 保留历史审核证据，不与 current 事实源竞争。

## Game / G9

当前游戏项目权威状态以 `Vibe-Coding/main/sillytavern/` 为准；本段只做资产工作台导航同步。

```text
G9-02                         PASS / CLOSED
G9-03 Unified Protocol       PASS / CLOSED
G9-04 Adapter / Compiler     PASS / CLOSED
G9-05A Creator Foundation    PASS / FROZEN
G9-05B Creator Core          PASS / CLOSED
G9-05C World Creator         PASS / CLOSED
G9-05D Character Creator     PASS / CLOSED
G9-05E Use My Assets Game Creation
                              PASS / CLOSED
G9-05F Expansion Creator     PASS / CLOSED
G9-05G0 Real EP-CHAR Runtime Binding
                              PASS / CLOSED
G9-05G Primary Asset E2E Closure
                              PASS / CLOSED
Primary Asset End-to-End Closure Gate
                              PASS / CLOSED

Library Product Increment    AUTHORIZED / NEXT
```

当前 Creator / Asset authority：

- `Vibe-Coding/main/sillytavern/G9-03_UnifiedAssetReferenceProtocol规格_v1.0_2026-08-20.md`
- `Vibe-Coding/main/sillytavern/G9-03A_RuntimeModuleBinding与TypedConfig增量裁定_v1.0_2026-08-20.md`
- `Vibe-Coding/main/sillytavern/G9-04_LegacyMarkdownAdapterCompilerBinding规格_v1.0_2026-08-20.md`
- `Vibe-Coding/main/sillytavern/G9-04_IndependentReview_最终收口_v1.0_2026-08-20.md`
- `Vibe-Coding/main/sillytavern/G9-05A_Creator基础模型与创作稿导入产品架构裁定_v1.0_2026-08-20.md`
- `Vibe-Coding/main/sillytavern/G9-05B_CreatorCore草稿导入发布内部合同规格_v1.0_2026-08-20.md`
- `Vibe-Coding/main/sillytavern/G9-05B_IndependentReview_最终收口_v1.0_2026-08-20.md`
- `Vibe-Coding/main/sillytavern/G9-05C_WorldCreator产品纵向规格_v1.0_2026-08-20.md`
- `Vibe-Coding/main/sillytavern/G9-05C_IndependentReview_最终收口_v1.0_2026-08-21.md`
- `Vibe-Coding/main/sillytavern/G9-05D0_CharacterProfileFields增量裁定_v1.0_2026-08-21.md`
- `Vibe-Coding/main/sillytavern/G9-05D_CharacterCreator产品纵向规格_v1.0_2026-08-21.md`
- `Vibe-Coding/main/sillytavern/G9-05D_IndependentReview_最终收口_v1.0_2026-08-21.md`
- `Vibe-Coding/main/sillytavern/G9-05E_使用我的资产库创建游戏产品与内部合同规格_v1.0_2026-08-21.md`
- `Vibe-Coding/main/sillytavern/G9-05E_IndependentReview_最终收口_v1.0_2026-08-22.md`
- `Vibe-Coding/main/sillytavern/G9-05F0_ExpansionImport与HostPublishGate增量裁定_v1.0_2026-08-22.md`
- `Vibe-Coding/main/sillytavern/G9-05F_ExpansionCreator产品纵向规格_v1.0_2026-08-22.md`
- `Vibe-Coding/main/sillytavern/G9-05F_IndependentReview_最终收口_v1.0_2026-08-22.md`
- `Vibe-Coding/main/sillytavern/G9-05G0_EP-CHAR-CORE真实RuntimeBinding增量裁定_v1.0_2026-08-22.md`
- `Vibe-Coding/main/sillytavern/G9-05G_PrimaryAssetEndToEndClosure规格_v1.0_2026-08-22.md`
- `Vibe-Coding/main/sillytavern/G9-05G_IndependentReview_最终收口_v1.0_2026-08-22.md`
- `Vibe-Coding/main/sillytavern/G9-05G_阶段收口与NextGate状态覆盖_v1.0_2026-08-22.md`

G9-04 已证明本仓库真实 World Pack / Character Card / Expansion Pack 可以通过确定性适配器转成 `TavernAssetV1`，再通过精确 Manifest 进入 G9-02 本局绑定与存档恢复轨道。

G9-05B 已建立共享 Creator Core：Creator Draft 与正式 Source Asset 分离、revision/CAS、外部 `.md/.txt` 创作稿 evidence、任务级 AI 授权、复杂 Provider operation 运行时解析、ChangeSet/Undo、正式 Source Asset Library、确定性发布与崩溃恢复。

G9-05C 已证明第一个真实 World Creator 产品纵向：四入口、三种创作起点、结构化 World workspace、完整 composition/dependency 编辑、exact AI scope、导入证据/未决/冲突继续创作定位、显式发布、Source 版本历史，以及发布后的合法 World dependency 可通过 G9-03 `validateAssetCatalog()`。

G9-05D 已证明 Character Creator 复用共享 Creator Core，并保持 `playerCharacterSupported` 只是 Source capability、No-Phantom、三态字段、referenceSources/dependency、exact AI scope、发布/版本历史与 Runtime 隔离。

G9-05E 已证明正式 Source Asset 可以经【使用我的资产库】按 exact snapshot 选择后进入本局：hard dependency 只由 selected exact target 满足，Character role 显式区分 `bound_only/opening_character/player_character`，复用 G9-04 binding，Final Create exactly-once，并走通 Session / Save / Restore。多版本 World / Character / Expansion 的产品选择身份均以 `assetRef + assetType + version + contentHash` 为准，不按 stable ref 自动继承 sibling version。

G9-05F 已证明 Expansion Creator 复用共享 Creator Core，并通过 Program-owned Capability Catalog、Host Publish Gate、typed feature/module/dependency/UI declarations、AI identity protection、source revision 与显式 Publish 形成正式 Source 纵向；Publish 不等于当前游戏 Runtime activation。

G9-05G 已证明真实汉末三国 World + 刘备 Character + `EP-CHAR-CORE` Expansion 可以从真实 Markdown / Creator source revision 形成 exact published Source，进入【使用我的资产库】建局，完成 production Runtime module binding、bounded capability projection、正式回合、Save/Restore、Crash/Resume/Recovery 与 Source version isolation。`EP-CHAR-CORE@0.1.5` 历史 proof snapshot 保持 immutable，production `0.1.6` 使用新的 exact Source identity；Expansion Publish 的 candidate/current Host 与 historical Source catalog 已分层，并关闭 append-after-durable / finalize-before-durable 的 exactly-once recovery crash window。

现有 Semantic Assets 不需要手工改写为 JSON；G9-04 Adapter 继续承担 legacy authoring format → canonical machine object，Creator 则直接从结构化 Draft 确定性发布同一种 `TavernAssetV1`。

下一阶段 Library Product 必须先冻结其产品定位与 Authority：Library Source、Creator Reference、Runtime retrieval、Model context、player-safe reference 的边界不得混淆。不得因为主资产 E2E 已通过就自动恢复 arbitrary Runtime Library retrieval、relation query DSL 或 hidden-state browsing。
