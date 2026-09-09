---
title: EP-MAGIC-CORE｜Runtime Context Contract
version: 0.1
status: current-context-sidecar
created: 2026-08-18
updated: 2026-08-18
asset_id: EP-MAGIC-CORE
asset_version: 0.3
asset_title: 魔法基础
canonical_asset_path: 拓展包/通用拓展包/魔法族/魔法基础_Expansion_Pack_v0.3.md
canonical_domain_ownership: none
pattern: 通用资产库_RuntimeContextContract模式_v0.4
generic_identity_status: normalized-workspace-binding
asset_spec_binding: pending-g9
---

# EP-MAGIC-CORE｜Runtime Context Contract v0.1

> [!abstract]
> 本 Sidecar 只为 `EP-MAGIC-CORE｜魔法基础 v0.3` 补充 Runtime Context Binding。
>
> Canonical Spell Magic Domain、Spell Grammar、Magic Aptitude、Spell Mastery、Casting Load、Magic Strain、Countermagic 与 Theme Extension Point 仍全部由正式资产正文拥有。
>
> 本文件不新增 Spell、不修改 Gameplay Outcome、不获得任何 Domain Ownership。

---

# 1. Routing Profile

```text
ID: EP-MAGIC-CORE
Name: 魔法基础
Scope: 法术型魔法的学习、掌握、施展、变体、维持、中断、反制/驱散、仪式与 Magic Strain
Typical semantics: 施法 / 学法术 / 教授法术 / 变体施法 / 维持法术 / 中断施法 / 反魔法 / 驱散 / Ritual / Magic Strain
```

Routing Profile 只表示 Spell Magic Domain 可能与当前输入有关，不携带 36 个基础 Spell Definition，也不展开所有 Theme Spell。

---

# 2. Immediate Activation

典型 immediate activation：

- 玩家明确尝试施展某个 Spell；
- 玩家以自由语言描述一个可能属于已知 Spell / 合法变体的施法意图；
- 学习、教授、训练或回忆具体 Spell；
- 识别、打断、Counter、Dispel、Suppress、Protect 某个 Spell；
- 主动绳持、取消或改变当前 Spell；
- 协同施法 / Ritual 的当前语义处理；
- 当前问题明确涉及 Magic Aptitude、Spell Mastery、Casting Load 或 Magic Strain。

普通 Combat 不能因为角色“会魔法”就自动激活 Magic。

---

# 3. State-mandatory Activation

以下 authoritative active state 可以使 Magic 成为 Runtime Relevant，即使玩家使用省略表达：

- 当前存在尚未完成的 active Casting Process；
- 当前存在玩家正在维持、修改或取消的 active Spell；
- 当前处于尚未完成的 Ritual / Cooperative Casting Process；
- 当前 Formal Action 明确引用一个 active Spell Ref / Countermagic interaction。

但：

> **Runtime Relevant != Model Visible。**

例如 Spell Duration、Magic Strain 恢复、确定性 maintenance bookkeeping 可以由 Program 继续推进而不调用模型。

---

# 4. Downstream Activation

Router 不负责提前预测所有 Spell 后果。

推荐链：

```text
Combat / Player Intent
→ Magic immediate semantic resolution
→ Program Formal Outcome
→ Spell Effect / Backlash Event
→ Health / Item / Position / World Owner downstream activation
```

以及：

```text
Combat Reaction Window
→ bounded Spell interaction request
→ Magic Counter / Dispel semantics
```

Health 不因为“法术可能受伤”而在施法第一轮全量进入 Prompt；只有真实 Health-relevant Effect / Backlash 形成后再 Handoff。

---

# 5. No-load Conditions

通常不加载 Magic 详细 Context：

- 角色拥有 Spell，但当前没有使用、学习、讨论或受 active Spell 影响；
- 完全不涉及魔法的私人闲聊；
- 普通武技 Combat；
- 已经由 Health 接管的身体后果，仅剩 Health progression；
- World Pack 的魔法历史 / 学院 /法律讨论，只需要 World / Knowledge facts 而不需要 Spell Mechanism；
- 后台 Magic Strain 恢复、Spell duration / cooldown 等 deterministic bookkeeping。

---

# 6. Minimal Read Set

一旦激活，只读取当前职责所需的最小充分集合：

- 当前 caster / target refs；
- **当前选中或候选的少量 Spell Definition projection**；
- caster 当前相关 Magic Aptitude / Magic-domain Skill；
- 当前 Spell Mastery；
- 当前 Magic Strain；
- 与选中 Spell 真正相关的 Requirement / Focus / Material / target / reach / duration / variability；
- 当前 active Spell / Ritual state（如有）；
- 必要 scene / environment facts；
- 若处于直接战斗，只读取 Combat 提供的 bounded Range / LOS / Cover / Reaction / Pressure projection；
- 若身体状态实际限制施法，只读取 Health 提供的 relevant Functional Effect。

不得默认读取：

- 全部 36 个基础 Spell；
- 所有已启用 Theme Spell；
- 角色完整六层 Character Profile；
- 完整 Combat / Health 正文；
- 完整 Spell history。

---

# 7. Model-needed Semantics

模型适合处理：

- 玩家自由语言中的施法意图与目标表达；
- 在已知 Spell Grammar 内识别可能的 Canonical Spell / 合法变体；
- 对 Spell 可变轴进行开放式语义解释；
- 非标准 Ritual / cooperative casting 的结构化 Candidate；
- Countermagic / Dispel 的语义意图；
- 当前选中 Spell 的 player-safe 解释与 Narrative realization。

模型不负责把自然语言即兴写成新的永久 Canonical Spell。

---

# 8. Program-owned Logic

Program / authoritative state 负责：

- Spell Ref / Definition identity；
- 当前角苲是否真正掌握某 Spell；
- Mastery / Aptitude / Magic Strain authoritative read；
- Requirement / Focus / resource availability；
- deterministic duration / maintenance / strain recovery；
- permission / target eligibility 的可确定部分；
- RNG / Dice；
- Program Judge；
- Formal Outcome；
- active Spell lifecycle；
- Atomic Commit / Save / Restore。

模型不得直接写 Spell Mastery、Magic Strain、active Spell State 或 World State。

---

# 9. Output Candidate

模型最多输出：

- `spell_intent`；
- `candidate_spell_ref` / small ranked candidate set；
- `candidate_variation`；
- `candidate_target`；
- `candidate_countermagic_action`；
- `candidate_ritual_interpretation`；
- `clarification_need`。

这些都是 Candidate，不是 Formal Mutation。

---

# 10. Handoff / Information Boundary

Incoming：

- Character → relevant capability / skill projection；
- Combat → current reaction / range / opposition projection；
- World / Item → environment / focus / material facts；
- Theme Expansion → selected Spell Definition contribution。

Outgoing：

- Health → bodily effect / backlash；
- Combat → spell-in-combat internal result / interaction candidate；
- Item / Position / World → corresponding effect candidate；
- Narrative → player-safe spell result only after Formal Outcome。

Information Boundary：

- NPC 未公开的 Spell Library、Mastery、Magic Strain、秘密 Ritual 不自动进入玩家 Context；
- “某 Spell 存在”不等于玩家角色知道它；
- Theme Library 全量不进入 Router / Narrative。

---

# 11. Context Cost / Bounded Strategy

冻结：

```text
Magic Enabled
!= Full Magic Core in every prompt
```

```text
Magic Runtime Relevant
!= All Spell Definitions visible
```

```text
Known Spell Set
!= Current Model Visible Spell Set
```

Magic Core 当前正文已有 **36 个基础 Spell Definition**；未来 Theme Library 可以扩展到数百 / 数千条，但普通 Turn 与单 Spell Turn 的 Model Working Set 不应随总 Library 大小线性增长。

---

# 12. Feature / Theme Activation Hierarchy

Magic Core 是 Spell Magic Domain Core；Theme Expansion 通过 Contribution 扩展 Spell Registry。

因此：

```text
Magic Core Enabled
!= Every Magic Theme Enabled
!= Every Theme Spell Visible
```

Runtime 只允许当前 Game 已启用 Theme 的 Spell Definition 进入可检索 Registry；未启用 Theme 不提供 routing / spell candidates。

---

# 13. Background Program Progression

可 deterministic 后台处理：

- Magic Strain 的时间恢复；
- active Spell duration bookkeeping；
- deterministic maintenance / expiry；
- cooldown / fixed timer（若某 Spell Definition 声明）；
- 已确认 Formal Effect 的持续 tick bookkeeping。

```text
Background Magic Progression
!= Model Activation
```

只有出现新的自由语言决策、开放式变体、Counter interaction、warning / threshold decision 或新的跨域 Handoff 时才按需调用模型。

---

# 14. Definition Registry / Library Projection

Spell Registry 是 Runtime / Asset Definition Registry，不是 Prompt。

推荐语义链：

```text
Enabled Spell Definitions
→ actor-accessible / actor-known subset
→ intent-relevant candidate retrieval
→ selected Definition Projection
→ Model
```

Router 第一轮只需要 `EP-MAGIC-CORE` 的 Domain Routing Profile；不需要把 36 个 Spell 名称作为 Capability Directory 展开。

若玩家直接引用已知 Spell 名称 / ID，Runtime 可以直接定位 Definition；若玩家自由描述，先由 Magic routing 识别 Domain，再对 actor-accessible Spell subset 做 bounded candidate retrieval。

---

# 15. Bounded Sufficiency｜Bounded != Starved

目标不是把 Context 压到“只剩 Spell 名称”。

模型真正需要解释当前 Spell 时，Projection 至少应保留该 Spell 当前职责所需的核心效果、合法变体轴、关键 Requirement、目标 / Reach / Duration / Interaction 边界，以及与当前 caster / target 真正相关的状态。

```text
Bounded Context
= minimum sufficient high-signal context
!= minimum possible tokens
```

过度裁剪导致模型无法区分 Spell、忽略关键限制或只能泛化回答，同样属于 Context Failure。

---

# 16. Open Attempt

Spell Definition / Spell Registry 不是玩家动作白名单。

玩家可以描述未精确匹配预定义 Spell 的魔法尝试；Router 仍可将其路由到 Magic，之后由已知能力、Spell Grammar、World Rule 与 Program Judge 判断能否形成合法 Effect。

---

# 17. G8 / G9 Boundary

本 Sidecar 是 G9-02 handwritten semantic requirement，不是最终 machine schema。

当前不冻结：

- Runtime selector / retrieval algorithm；
- Spell registry machine field；
- Router API；
- token budget；
- asset-spec field；
- Creator machine UI。

当前 Stage UAT 已 FAIL 并正式 REOPEN G8；Current Next = G8-UAT-01 v1.1，G9 NOT AUTHORIZED。
