---
title: EP-HEALTH-CORE｜Runtime Context Contract
version: 0.1
status: current-binding-sidecar
created: 2026-08-18
updated: 2026-08-18
applies_to_asset: EP-HEALTH-CORE
applies_to_version: 0.1
canonical_asset: 身体状态核心_Expansion_Pack_v0.1.md
contract_role: runtime-context-binding
canonical_domain_ownership: none
pattern: 通用资产库_RuntimeContextContract模式_v0.2
asset_spec_binding: pending-g9
---

# EP-HEALTH-CORE｜Runtime Context Contract v0.1

> [!abstract]
> 本 Sidecar 只声明 Health Domain 的 Runtime Relevance / Model Working Set 边界；HP、Condition、Consciousness、Functional Effect、Treatment / Recovery 等 Canonical Semantics 继续由 `EP-HEALTH-CORE v0.1` 正文拥有。

---

# 1. Routing Profile

```text
ID: EP-HEALTH-CORE
Name: 身体状态核心
Scope: 持续身体/生理状态、伤势、疾病、中毒、疼痛、身体疲劳、意识、治疗、稳定、康复与身体死亡事实
Typical semantics: 受伤 / 流血 / 骨折 / 生病 / 中毒 / 疼痛 / 昏迷 / 治疗 / 包扎 / 恢复 / 身体还能不能继续行动
```

Combat hit / Spell success 本身不属于 Health Router 主要职责；正式身体影响形成后再由 Health 接管。

---

# 2. Immediate Activation

- 玩家直接检查、诊断、治疗、稳定或恢复某个身体状态；
- 当前输入明确询问某个 Injury / Disease / Condition 对身体功能的影响；
- 玩家主动尝试带伤行动，且“当前身体限制如何影响这次尝试”是主要语义问题；
- 当前行为以治疗 /康复 /身体处置为主要目标。

---

# 3. State-mandatory Activation

若 authoritative Health State 已存在以下情况，Runtime 可以把 Health 加入 **Runtime Relevant Set**：

- 当前 Condition 的 Functional Effect 直接约束正在解析的行动；
- Critical / Dying / Consciousness State 必须影响当前处理；
- 当前有正式 Treatment / Progression / Recovery lifecycle 到达处理节点。

但其中可 deterministic 处理的 progression / HP / threshold 仍由 Program 完成；**State-mandatory Runtime Relevant != full Health semantics model-visible。**

---

# 4. Downstream Activation

典型链：

```text
Combat / Magic / Divine / Survival / World Cause
↓ Formal Impact / Treatment / Exposure Event
Health-relevant Handoff
↓
Health downstream activation
```

例如普通 Combat Action 解析阶段不要求 Router 预先加载 Health；只有 Physical Impact 成为正式 Handoff，或已有伤势直接限制动作时，Health 才参与。

---

# 5. No-load Conditions

通常不加载详细 Health Context：

- 未涉及身体影响的普通闲聊；
- Public Reputation / ORG / Politics 等社会事实；
- Combat “是否命中 / 当前 Range / Reaction”解析，且当前身体状态不构成相关限制；
- 单纯 Item / Position 操作；
- 只需要展示一个已授权 Health Summary 的 UI / Narrative 场景，可由 Runtime 直接提供 materialized safe projection。

---

# 6. Minimal Read Set

根据当前 Health intent，只读取：

- 当前 Target；
- 直接相关 Condition；
- Condition Severity / Trend；
- 相关 Functional Effect；
- 必要 Body / Physiology Facts；
- 当前 Consciousness / Critical state（若相关）；
- 当前 Treatment / Recovery context；
- 必要的 cause / provenance 摘要；
- player-safe / diagnosis-safe projection。

不得默认加载：

- Target 全部 Health 历史；
- 所有人物 Health State；
- 所有 source Events；
- 完整医学数据库；
- 精确隐藏 HP（除非某 Program-owned path 确实需要，且通常不进入模型）。

---

# 7. Model-needed Semantics

模型主要负责：

- 识别自由语言治疗 /身体处置意图；
- 对非标准身体影响提出 Condition / Functional Effect interpretation candidate；
- 对开放式 Treatment Attempt 提出语义 Candidate；
- 在已给定 Formal Health State 的前提下生成自然、player-safe 的身体表现 /叙述；
- 需要时提出 clarification。

模型不拥有 HP 数值或最终身体结果。

---

# 8. Program-owned Logic

Program / Runtime 负责：

- authoritative HP / Health Reserve；
- Condition State；
- deterministic Condition lifecycle；
- Health Burden / HP calculation；
- Critical / Dying threshold；
- Consciousness State；
- deterministic treatment / recovery bookkeeping；
- RNG / Dice；
- Program Judge；
- Formal Outcome；
- Bodily Death 的正式提交；
- Atomic Commit；
- Save / Restore；
- player-safe / diagnosis-safe projection authorization。

正文已经冻结：来源资产不能自行 `HP -X/+X`；本 Sidecar 继续保持这一 Program Authority Boundary。

---

# 9. Output Candidate

模型最多提出：

- candidate health intent；
- candidate Condition interpretation；
- candidate treatment / stabilization action；
- candidate Functional Effect interpretation；
- candidate clarification need。

不得直接：

- 改 HP；
- 创建正式 Condition；
- 宣告死亡；
- 提交 Recovery Outcome。

---

# 10. Handoff / Information Boundary

## Incoming

- Combat → Physical Impact；
- Survival → need / exposure consequence；
- Magic / Divine / World → Health-relevant effect / treatment；
- Character Capability → relevant bodily capability evidence（只读）。

## Outgoing

Health 向：

- Combat / Character Action Resolution → bounded Functional Effect projection；
- Relationship / Narrative → relevant visible bodily event context；
- Survival / downstream Health gameplay → current bodily condition projection。

## Information Boundary

```text
Health Truth
!= Player diagnosis
!= NPC diagnosis
!= Narrative-visible detail
```

精确 HP、隐藏 Disease、未发现 Poison、不可观察 Condition 不自动进入模型职责或 UI。

---

# 11. Context Cost / Bounded Strategy

```text
Enabled Health
!= Health rules always in model context
```

```text
All Conditions / Health History
!= Current Relevant Condition Projection
```

```text
Health Runtime Relevant
!= Health Model Visible
```

长期伤病历史与人物数量增长时，普通无关 Turn 的 Working Set 应保持稳定；需要身体影响时也只读取当前 Target 的局部状态。

---

# 12. G8 / G9 Boundary

当前 Sidecar 不定义最终 HP DTO、state selector、Context Compiler 或 UI data binding。G9 必须在 G8 Final Host Convergence 后把 bounded player-safe projection 映射到真实 Host capability。
