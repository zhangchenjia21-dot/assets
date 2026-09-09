---
title: EP-RELATIONSHIP-ROMANCE-CORE｜Runtime Context Contract
version: 0.1
status: current-binding-sidecar
created: 2026-08-18
updated: 2026-08-18
applies_to_asset: EP-RELATIONSHIP-ROMANCE-CORE
applies_to_version: 0.2
canonical_asset: 关系与恋爱核心_Expansion_Pack_v0.2.md
contract_role: runtime-context-binding
canonical_domain_ownership: none
pattern: 通用资产库_RuntimeContextContract模式_v0.2
asset_spec_binding: pending-g9
---

# EP-RELATIONSHIP-ROMANCE-CORE｜Runtime Context Contract v0.1

> [!abstract]
> 本 Sidecar 只负责 `EP-RELATIONSHIP-ROMANCE-CORE v0.2` 的 Runtime Context Binding；Relationship / Romance Truth 继续只由正式 Expansion 正文拥有。

---

# 1. Routing Profile

```text
ID: EP-RELATIONSHIP-ROMANCE-CORE
Name: 关系与恋爱核心
Scope: 人与人之间的私人持续关系、单向情感/信任/尊重/依恋/关系承诺/浪漫吸引、共同关系、关系边界与关系记忆
Typical semantics: 喜欢 / 讨厌 / 信任 / 尊重 / 依恋 / 友情 / 师徒 / 仇敌 / 恋爱 / 求爱 / 分手 / 婚姻关系 / 关系边界 / 私人约定
```

Public Reputation、ORG Role、Political Recognition 不属于 Relationship Routing Profile。

---

# 2. Immediate Activation

- 玩家主动进行明确的人际关系互动，并且私人关系状态本身会影响当前语义；
- 询问、表达或挑战 Trust / Respect / Sentiment / Attachment 等私人关系事实；
- 求爱、表白、分手、和解、建立 / 调整 Relationship Agreement / Boundary；
- 当前输入直接讨论 Shared Bond：朋友、师徒、恋人、婚姻、私人仇敌等；
- 玩家询问自己已知的私人关系状态或历史。

普通 NPC 对话不自动要求加载完整 Relationship Core；只有当前互动需要私人关系语义时才参与。

---

# 3. State-mandatory Activation

不存在“只要两人认识就必须常驻”的 package-wide 条件。

若当前已经存在**明确激活中的 Relationship-specific interaction context**，例如正在处理某项 Relationship Agreement / Personal Boundary 的直接触发，则 Runtime 可以补充 Relationship 为 Relevant Domain。

仅有高 Trust / 低 Sentiment / 已婚等长期 State，本身不要求每 Turn 把 Relationship Core 放进 Model Working Set。

---

# 4. Downstream Activation

大量关系变化应该在事件发生后再处理：

```text
Combat / Rescue / Betrayal / Gift / Public Event / Promise outcome
↓ Formal Event
Relationship Interpretation Candidate
↓
Relationship downstream activation
```

第一轮 Router 不要求预测“这件事未来是否会提高信任 / 降低好感”。

Reputation 只提供公共评价 Context；它不能直接写 Relationship Respect / Trust。

---

# 5. No-load Conditions

通常不加载详细 Relationship Context：

- 普通移动 / 物品操作；
- 纯 Character Capability 使用；
- Combat 动作解析阶段，且私人关系不影响当前意图；
- 单纯 Health / Survival progression；
- ORG 任职 / Membership 确定性变化；
- 询问“江湖上大家怎么看某人”这类 Public Reputation；
- Character 仅仅同处一个 Scene。

---

# 6. Minimal Read Set

只读取当前人物对之间直接相关的：

- A → B 的必要 Directed Dimensions；
- 必要时 B → A；
- 当前 Shared Bond；
- 与本次互动直接相关的 Personal Boundary / Relationship Agreement；
- 少量最相关 Relationship Memory / Interpretation；
- 当前可见 / 可知的关系投影。

不得为了一次私人对话加载：

- 全人物关系图；
- 某人对所有 NPC 的关系；
- 全部 Relationship Memory 历史；
- 所有 Romance Preference；
- Public Reputation 全量状态。

---

# 7. Model-needed Semantics

模型适合：

- 理解自由语言中的复杂私人关系意图；
- 将 Formal Event 解释为“这个人物怎样理解它的关系意义”的 Candidate；
- 生成非对称、矛盾关系下的 NPC response candidate；
- 识别 Boundary / Agreement / Romance Attempt 中的开放式语义；
- 对 player-safe Relationship State 做自然语言摘要。

---

# 8. Program-owned Logic

Program / Runtime 负责：

- Character pair / Relationship Ref；
- 当前 Directed / Shared State 的权威存储；
- hidden quantitative representation；
- deterministic lifecycle / threshold bookkeeping；
- Relationship Agreement / Boundary 当前正式状态；
- Formal Outcome；
- Atomic Commit；
- Save / Restore；
- player-safe / npc-safe projection authorization。

模型不得直接写 Trust / Respect / Attraction 等正式状态。

---

# 9. Output Candidate

模型最多提出：

- candidate relationship intent；
- candidate event interpretation；
- candidate directed-dimension change；
- candidate Shared Bond / Agreement / Boundary change；
- candidate NPC relationship response；
- clarification need。

最终变化由 Runtime / Program Owner 决定。

---

# 10. Handoff / Information Boundary

## Incoming

- External Formal Event → Relationship Interpretation Candidate；
- Reputation → public perception context；
- ORG → role / membership context；
- Character Definition / Personality → NPC interpretation input；
- Health / Survival / Combat → relevant event context。

## Outgoing

Relationship 提供私人关系 projection 给：

- NPC response；
- Narrative；
- Character Detail；
- 需要私人关系 Context 的其他 Domain。

不得反写 Reputation / ORG / Politics / Law。

## Information Boundary

NPC 私人 Trust / Attraction / Attachment 等默认不等于玩家已知事实。

```text
Relationship Truth
!= Player Knowledge
!= NPC Knowledge of the other side
!= Public Reputation
```

---

# 11. Context Cost / Bounded Strategy

```text
Enabled Relationship
!= all relationship graph in prompt
```

```text
Full Relationship History
!= relevant relationship memory summary
```

```text
A knows B
!= Relationship Core always model-visible when A and B share a scene
```

人物关系网络增长 5–10 倍时，普通无关 Turn 只读取当前相关 pair / small local set。

---

# 12. G8 / G9 Boundary

当前只冻结语义 Binding；不冻结机器字段、relationship selector、query DSL 或 browser-side state access。G9 必须服从 G8 已验证 Host / projection capability。
