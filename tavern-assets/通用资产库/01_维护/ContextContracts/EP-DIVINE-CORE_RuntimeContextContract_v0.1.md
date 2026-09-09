---
title: EP-DIVINE-CORE｜Runtime Context Contract
version: 0.1
status: current-context-sidecar
created: 2026-08-18
updated: 2026-08-18
asset_id: EP-DIVINE-CORE
asset_version: 0.2.1
asset_title: 神术与信仰
canonical_asset_path: 拓展包/通用拓展包/魔法族/神术与信仰_Expansion_Pack_v0.2.1.md
canonical_domain_ownership: none
pattern: 通用资产库_RuntimeContextContract模式_v0.4
generic_identity_status: normalized-workspace-binding
asset_spec_binding: pending-g9
---

# EP-DIVINE-CORE｜Runtime Context Contract v0.1

> [!abstract]
> 本 Sidecar 只为 `EP-DIVINE-CORE｜神术与信仰 v0.2.1` 补充 Runtime Context Binding。
>
> Divine Covenant、Authority Scope、Invocation、Channel Strain、Anchor、Audience、Miracle、Sovereign Divine Authority 与 Spell↔Divine Interaction 的 Domain Semantics 仍由正式资产正文拥有。
>
> 本文件不获得 Divine Domain Ownership，也不把 Divine Actor 降级成确定性资源池。

---

# 1. Routing Profile

```text
ID: EP-DIVINE-CORE
Name: 神术与信仰
Scope: Divine Covenant、授权范围、神术调用、Channel Strain、神性锚点、Divine Audience、Miracle Request 与神性主权边界
Typical semantics: 神契 / 神授权限 / 祈祷 / 神术 / 圣礼 / 神性锚点 / 觐见 / 神迹请求 / 断契 / 授权变化 / Channel Strain
```

Router 不需要展开全部 Invocation Library，也不把“宗教话题”一律等价为 Divine Mechanism。

---

# 2. Immediate Activation

典型 immediate activation：

- 当前玩家明确调用 / 尝试某个 Divine Invocation；
- 祈祷、请求、谈判或进入 Divine Audience；
- 建立、修改、深化、紧张、断绝 Divine Covenant；
- 查询 / 使用当前 Authority Scope；
- 当前行为明确依赖 Personal / Sanctuary / Faith Anchor；
- 当前问题涉及 Invocation Mastery / Channel Strain；
- Spell 与 Divine Effect 当前发生显式 interaction；
- Miracle Request 或 Divine Actor direct intervention 的当前语义处理。

普通教会职位、宗教文化、神学知识讨论若不涉及真实 Covenant / Authorization / Invocation，可由 ORG / World / Knowledge 处理，不自动加载 Divine Core。

---

# 3. State-mandatory Activation

以下 authoritative active state 可使 Divine 成为 Runtime Relevant：

- 当前处于尚未结束的 Divine Audience Process；
- 当前存在 active Invocation / Ritual / Channeling Process；
- 当前 formal action 引用一条 active Covenant operation；
- 当前正在处理一个已正式建立的 Miracle Request / Divine Response process；
- 当前有明确 Spell↔Divine sovereign / authority-bound interaction。

但 covenant 存在本身、角色有宗教信仰本身，都不会让 Divine 永久进入 Model Context。

---

# 4. Downstream Activation

推荐链：

```text
Player Prayer / Invocation Intent
→ Divine semantic candidate
→ Program / Divine Actor adjudication
→ Formal Divine Event
→ Health / Combat / Item / Position / Relationship / ORG / World downstream Handoff
```

以及：

```text
Magic Effect
→ explicit Spell↔Divine Interaction Profile
→ bounded Divine activation
```

Router 不要求提前把所有可能受到神术影响的 Domain 同时加载。

---

# 5. No-load Conditions

通常不加载 Divine 详细 Context：

- 普通宗教文化 /历史 / 教义讨论，只需 World / Knowledge；
- 教会 Membership / Office 但不涉及 Divine Covenant / Authorization；
- 与神术无关的私人闲聊、Combat、Health；
- 角色拥有 Covenant / Invocation，但当前没有使用或处理；
- Channel Strain 的确定性时间恢复；
- 已经由 Health / Combat 等 Owner 接管的后续状态更新。

---

# 6. Minimal Read Set

根据当前职责只读取：

- 当前 mortal / Divine Actor refs；
- 当前相关 Covenant；
- 当前 relevant obligations / permissions；
- 当前 Authority Scope；
- **当前选中或候选的少量 Invocation Definition projection**；
- 相关 Invocation Mastery；
- 当前 Channel Strain；
- 当前真正相关 Anchor；
- 必要 World Sovereign / Divine Authority boundary；
- target / scene facts；
- Divine Audience 时的 purpose-built Divine Actor / covenant / request / relevant-history projection。

不得默认读取：

- 全部 Covenant；
- 全部 Divine Actor；
- 全部 **84 个 Invocation Definition**；
- 完整神学 /世界宗教历史；
- Divine Actor 全部 private goals / knowledge；
- 完整 Magic / Combat / Health 资产正文。

---

# 7. Model-needed Semantics

模型适合处理：

- 自由语言 Prayer / Invocation / Audience request；
- Covenant negotiation / obligation ambiguity 的开放式语义 Candidate；
- Divine Actor 作为自主 Actor 的回应 Candidate；
- 神的沉默、拒绝、谈判、条件性回应等非确定性角色语义；
- player-safe Divine response / narrative realization；
- 复杂 Miracle Request 的结构化意图。

模型不拥有 Covenant / Authorization / Miracle 的直接 State Mutation 权。

---

# 8. Program-owned Logic

Program / authoritative Runtime 负责：

- Covenant / Divine Actor Ref validation；
- Covenant current state；
- Authority Scope eligibility；
- Invocation known/mastery；
- Anchor existence / current applicability 的可确定事实；
- Channel Strain authoritative state / deterministic recovery；
- Sovereign boundary / permission 的确定性 Gate；
- RNG / Dice；
- Program Judge；
- Formal Outcome；
- Covenant / Authorization / Miracle Event commit；
- Save / Restore。

Divine Actor 的开放式自主判断可以由模型提出 Candidate，但只有 Runtime 才能形成正式 Covenant / Authorization / Miracle / World State。

---

# 9. Output Candidate

模型最多提出：

- `divine_intent`；
- `candidate_invocation_ref`；
- `candidate_audience_request`；
- `candidate_divine_response`；
- `candidate_covenant_change`；
- `candidate_authority_change`；
- `candidate_miracle_request` / response；
- `clarification_need`。

---

# 10. Handoff / Information Boundary

Incoming：

- Character → relevant capability projection；
- World → actual Divine Actor / religion / sovereign boundary facts；
- Magic → explicit interaction request；
- ORG → church office / organization facts（只作 Context）；
- Combat → reaction / target / opposition projection（如需）。

Outgoing：

- Health → healing / bodily effect candidate；
- Combat → divine combat effect candidate；
- ORG → covenant-related event context，不写 Church Office；
- Relationship / Reputation → public / interpersonal consequence event；
- World → Miracle / sovereign world-effect candidate。

Information Boundary：

- Divine Actor private knowledge / motive != player knowledge；
- 未被角色知道的 Covenant truth / hidden divine agenda 不进入 player-safe Context；
- “神存在”不等于玩家知道其全部属性；
- Narrative 不得把未正式发生的 Miracle / Covenant change 写成事实。

---

# 11. Context Cost / Bounded Strategy

冻结：

```text
Divine Enabled
!= Divine always visible
```

```text
Divine Runtime Relevant
!= All 84 Invocation Definitions visible
```

```text
All Covenants / Divine Actors
!= Current Divine Projection
```

Invocation Library、神明数量、Covenant 数量扩大 5–10 倍时，普通无关 Turn 和单 Invocation Turn 的模型 Context 应保持 bounded。

---

# 12. Feature / Covenant Activation Hierarchy

Divine Core 不把每条 Covenant 或 Invocation 变成独立 Expansion。

Context Selection 应逐层裁剪：

```text
Divine Core Enabled
→ relevant mortal
→ relevant Covenant
→ relevant Authority Scope
→ relevant known/authorized Invocation candidates
→ selected Invocation / Audience Process
→ Model
```

Multi-Covenant 只读取与当前请求相关的 Covenant；若真实冲突发生，再加入必要冲突方，不默认加载全部。

---

# 13. Background Program Progression

可 Program-only：

- Channel Strain 时间恢复；
- Invocation / Ritual duration bookkeeping；
- deterministic cooldown / expiry；
- 已正式确定的持续神术效果 tick；
- Covenant 状态的纯时间 bookkeeping（若具体定义存在）。

Covenant 不做“每日 Faith +1/-1”式模型 tick；真实关系变化由 Event / Actor decision 触发。

---

# 14. Definition Registry / Library Projection

Invocation Library 是 Definition Registry，不是 Prompt。

```text
Enabled Invocation Definitions
→ current Covenant / Authority compatible subset
→ actor-known / accessible subset
→ intent-relevant candidate retrieval
→ selected Definition Projection
→ Model
```

第一轮 Router 只需要 `EP-DIVINE-CORE` Domain profile；不要把 84 个 Invocation 名称塞进 Capability Directory。

---

# 15. Bounded Sufficiency｜Bounded != Starved

普通 Invocation 需要 selected Definition + Covenant / Authority / caster / target 的最小充分上下文。

**Divine Audience 特别禁止过度裁剪。**

若模型要代表自主 Divine Actor 产生回应 Candidate，至少需要当前职责真正相关的：

- player-safe / role-appropriate Divine Actor profile；
- current Covenant / Authority；
- 当前 request；
- relevant obligations / prior covenant events；
- 当前 world / sovereign boundary；
- 参与者身份与当前场景。

不能只提供 `godRef + covenantState` 然后期待模型生成有个性、因果连续的神性回应。

```text
Bounded
!= Starved
```

---

# 16. Narrative Affordance / Runtime Referent

若 Divine Audience / Miracle 让一个具体 Divine manifestation、avatar、messenger 或其他可持续交互对象对玩家可见：

> **player-visible durable/interactable affordance 必须拥有 authoritative Runtime referent。**

纯一次性的语气、光影、声音等 Ephemeral Narrative Realization 可以不成为长期实体，但不得伪装成之后可持续互动的具体对象。

---

# 17. Open Attempt

未授权 Invocation / Prayer / Miracle Request 仍可作为 Attempt。

Authorization 决定 Formal Effect，不删除表达本身。Router miss 或 Invocation Registry 未命中也不能自动判定玩家不能祈祷 / 请求 / 尝试。

---

# 18. G8 / G9 Boundary

本 Sidecar 是 G9-02 handwritten semantic requirement。

当前 G8 Engineering Gate 为 historical PASS；Stage UAT 已 FAIL 并正式 REOPEN G8；Current Next = G8-UAT-01 v1.1，G9 NOT AUTHORIZED。

不冻结 final Invocation registry schema、Divine Actor API、Router API、retrieval algorithm、token budget 或 Creator machine fields。
