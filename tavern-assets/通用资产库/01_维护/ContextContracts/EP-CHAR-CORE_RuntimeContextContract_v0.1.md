---
title: EP-CHAR-CORE｜Runtime Context Contract
version: 0.1
status: current-binding-sidecar
created: 2026-08-18
updated: 2026-08-18
applies_to_asset: EP-CHAR-CORE
applies_to_version: 0.1.5
canonical_asset: 人物能力与技艺_Expansion_Pack_v0.1.5.md
contract_role: runtime-context-binding
canonical_domain_ownership: none
pattern: 通用资产库_RuntimeContextContract模式_v0.2
asset_spec_binding: pending-g9
---

# EP-CHAR-CORE｜Runtime Context Contract v0.1

> [!abstract]
> 本文件是 `EP-CHAR-CORE｜人物能力与技艺 v0.1.5` 的 **Runtime Context Binding Sidecar**。
>
> 它不复制、不覆盖 Character Capability 的 Canonical Semantics，也不成为第二份 Expansion 正文；它只冻结 G9 前“何时激活、最少读取什么、模型看什么、Program 自己处理什么”的语义绑定。
>
> 若本 Sidecar 与正式 Expansion 正文发生语义冲突：**正文的 Canonical Domain Semantics 优先；Sidecar 必须修订，不能反向改写 Owner。**

---

# 1. Routing Profile

```text
ID: EP-CHAR-CORE
Name: 人物能力与技艺
Scope: 人物长期能力、属性、技能、经历、专长、执行风格、信条、学习训练与能力成长
Typical semantics: 会不会 / 擅长什么 / 用什么技能 / 训练 / 学习 / 熟练度 / 专长 / 经历带来的能力 / 长期执行风格 / 能力成长
```

Routing Profile 不是动作白名单；未命中 Skill Definition 仍允许 Open Attempt。

---

# 2. Immediate Activation

当前输入的核心问题直接涉及以下内容时，Character Capability Domain 参与：

- 玩家明确尝试一个需要读取长期能力证据的行动；
- 询问、比较或展示某人物已知的 Skill / Attribute / Specialty / Experience；
- 学习、训练、长期实践、能力成长或退化；
- 玩家主动采用某种已形成的 Specialty / Style；
- 当前语义理解需要判断“这个行动主要消费哪一种长期 Capability”。

仅仅“场景中存在人物”不能触发本 Core。

---

# 3. State-mandatory Activation

本 Core 没有“人物存在即常驻”的 state-mandatory 条件。

但如果某个已激活 Domain / Program Resolution 明确请求：

> `relevant character capability evidence`

则 Character Core 成为 **Runtime Relevant Provider**。

此时 Program 优先提供最小 Capability Projection；**Runtime Relevant 不等于 Character Core 全文进入模型。**

例如：

```text
Active Combat
→ requests relevant melee capability
→ Character Core provides bounded capability projection
→ no full Character Capability profile load
```

---

# 4. Downstream Activation

以下场景优先由其它 Domain 先处理，再通过 Provider / Handoff 请求 Character Capability：

- Combat → 请求与当前 Combat Action 直接相关的技能 / 属性 / Specialty；
- Magic / Divine → 请求对应领域 Capability；
- Politics / Economy / Governance / War 等未来 Domain → 请求特定领域 Skill Definition 对应的当前能力证据。

Router 不需要因为玩家“可能最终会用到某种能力”而预加载整个 Character Core。

---

# 5. No-load Conditions

以下场景通常不应因为本局启用了 Character Core 就把其详细语义加入 Model Working Set：

- 普通私人闲聊，且不涉及能力判断；
- 单纯 Relationship / Romance 互动；
- 只讨论 Public Reputation；
- ORG Membership / Role / Rank 的确定性查询；
- 单纯 Health 状态推进；
- 已由 Program 可确定完成的 Ref / Skill Registry lookup；
- 一个 Character 仅仅出现在当前 Scene。

**Character Definition / Personality != Character Capability Core。**

NPC 个性化对话需要人格事实时，不应因此加载六层能力机制全文。

---

# 6. Minimal Read Set

激活后只读取当前行动直接相关的：

- Actor；
- 1–2 个主要 Attribute；
- 当前相关 Skill；
- 必要 Specialty；
- 只有确实改变解释时才读取相关 Experience / Style / Creed；
- 当前能力状态的必要 provenance / training context；
- 当前模型职责允许看到的 player-safe / npc-safe projection。

禁止为了一个“开锁 / 骑马 / 剑术”行动加载：

- 人物完整六层 Profile；
- 全 Skill Registry；
- 全部 Experiences；
- 全部 Specialties；
- 全世界 Character Capability 状态。

---

# 7. Model-needed Semantics

模型主要负责：

- 从自由语言行动中识别可能相关的 Capability / Skill；
- 在多个合理 Skill / Attribute 都可能相关时提出语义 Candidate；
- 解释开放式训练、学习、实践是否可能形成成长 Candidate；
- 结合 Experience / Specialty / Style 对某次非标准行动提供语义解释；
- 在 player-safe context 中自然总结“这个人已知擅长什么”。

模型不负责最终能力判定结果。

---

# 8. Program-owned Logic

Program / Runtime 负责：

- Character / Skill / Definition Ref validation；
- 当前 Capability State 读取与持久化；
- 已掌握 / 未掌握 / 当前等级等确定性事实；
- Skill Registry identity；
- deterministic prerequisite / legality；
- Formal Resolution；
- RNG / Dice；
- Formal Outcome；
- growth state 的最终提交；
- Atomic Commit；
- Save / Restore；
- player-safe projection authorization。

如果一次行动只需要确定性 Skill lookup，优先 Program 处理，不为此调用模型阅读 Character Core 规则。

---

# 9. Output Candidate

模型最多提出：

- candidate relevant skill / attribute；
- candidate specialty / experience applicability；
- candidate capability interpretation；
- candidate learning / training / growth event；
- clarification need。

不得直接：

- 写 Skill State；
- 提升 Attribute；
- 授予 Specialty；
- 决定 Formal Outcome。

---

# 10. Handoff / Information Boundary

## Incoming

- Character Card / World Definition → bootstrap capability definition / evidence；
- Event / training / long-term practice → growth candidate；
- Domain Consumer → bounded capability evidence request。

## Outgoing

Character Core 向 Combat / Health / Magic / Divine / Politics / Economy / War 等消费者提供：

> **当前任务直接相关的 Capability Projection。**

消费者不得复制第二套 Character Capability State。

## Information Boundary

```text
Authoritative Character Capability
!= Player Knowledge of NPC Capability
!= NPC Knowledge of another Character Capability
```

NPC 隐藏技能、未见过的 Specialty、真实能力上限不自动进入 Router / Narrative / Player Context。

---

# 11. Context Cost / Bounded Strategy

```text
Enabled Character Core
!= Character Core always in model context
```

```text
Full Character Capability Profile
!= Current Action Capability Projection
```

```text
All Skills / Experiences / Specialties
!= Relevant Capability Evidence
```

人物数量、Skill Registry、长期成长历史扩大 5–10 倍时，普通无关 Turn 的模型上下文仍应基本稳定。

当前不冻结 token budget；G9 / G11 用真实 Provider 做 Context Composition Benchmark。

---

# 12. G8 / G9 Boundary

当前冻结 Semantic Context Contract。

G8 尚在 Final Host Convergence；G9 machine contract / compiler / Context Router 实现必须等待 G8 Exit Gate。当前 Sidecar 不声明最终 Schema、Router API、state path、selector 或任意数据访问 DSL。
