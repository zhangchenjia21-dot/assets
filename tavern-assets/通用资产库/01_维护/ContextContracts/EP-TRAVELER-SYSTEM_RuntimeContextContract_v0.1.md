---
title: EP-TRAVELER-SYSTEM｜Runtime Context Contract
version: 0.1
status: current-context-sidecar
created: 2026-08-18
updated: 2026-08-18
asset_id: EP-TRAVELER-SYSTEM
asset_version: 0.2
asset_title: 穿越与系统
contract_location: sidecar
canonical_domain_ownership: none
pattern: 通用资产库_RuntimeContextContract模式_v0.3
skill: tavern-asset v0.8.1
asset_spec_binding: pending-g9
---

# EP-TRAVELER-SYSTEM｜Runtime Context Contract v0.1

> [!abstract]
> 本 Sidecar 不改变 `EP-TRAVELER-SYSTEM v0.2` 的 Traveler / System Domain Semantics。
>
> 本 Contract 重点验证多级可选资产的 Context Hierarchy：**Package 被当前 Game 包含，不代表 Traveler Feature / System Feature 都启用；System Feature 启用也不代表所有 Module 启用；启用 Feature / Module 也不代表当前 Turn 必须进入模型上下文。**

---

# 1. Activation Hierarchy

正式冻结：

```text
Asset Library / Installed
!= Game Package Included
!= Feature Enabled
!= Module Enabled
!= Current Runtime Relevant
!= Current Model Visible
```

对本资产：

```text
EP-TRAVELER-SYSTEM included
├─ Traveler Feature ON / OFF
└─ System Feature ON / OFF
      └─ enabled Modules only
```

如果 System OFF：System Currency / Quest / Shop / Lottery / Surface / Module routing 都不存在于当前运行实例。

如果某 Module OFF：该 Module 不进入 Router Directory，也不产生 Conditional Dependency。

---

# 2. Routing Profiles

## Package-level summary

```text
ID: EP-TRAVELER-SYSTEM
Name: 穿越与系统
Scope: 异世界来客身份与可配置系统玩法框架；Traveler / System 两个 Feature 独立启停，System 由明确 Module 授权能力
```

## Feature / Module pruning

Router Directory 应按当前 Game 配置只暴露**已启用的 Feature / Module Routing Profiles**。

示例：

```text
Traveler ON
System ON
Enabled Modules = Appraisal + Shop

Router sees:
- Traveler identity / origin scope
- System framework scope
- Appraisal scope
- Shop scope

Router does NOT see:
- Healing
- Relationship Assistance
- Lottery
- Teleport
- Resurrection
```

避免“Package 理论上支持很多能力”导致 Router Prompt 与 Conditional Dependency 一起膨胀。

---

# 3. Immediate Activation

### Traveler Feature

- 玩家询问 / 使用 Traveler Identity、Origin World / Era、穿越背景、Disclosure；
- 玩家处理 Host Memory / Host Identity Integration 等穿越语义；
- 当前行动明确依赖 Otherworld Knowledge provenance。

### System Feature / Module

- 玩家打开、询问或使用已启用 System 能力；
- 玩家接受 /拒绝 System Quest Offer；
- 玩家使用 Shop / Storage / Appraisal / Teleport / Enhancement / Healing 等已启用 Module；
- 玩家修改合法的 System Feature / Module configuration（若当前产品允许）。

“玩家是穿越者”这一持续身份本身，不让 Traveler Context 永久常驻每个 Turn。

---

# 4. State-mandatory Activation

只有 authoritative active operation 会使相关 Feature / Module 成为 Runtime Relevant，例如：

- 正在执行一个已正式开始的 System module operation；
- 当前正在处理 System Quest offer / reward contract；
- Teleport / Storage / Lottery 等 formal operation 尚处于当前原子流程；
- 当前 Host Integration operation 尚未完成。

即使如此，Program 可以 deterministic 处理的 cooldown、currency、permission、module enabled state 等不自动进入 Model Visible Set。

---

# 5. Downstream Activation / Conditional Dependency

Module Conditional Dependency 只在**对应 Module Enabled 且当前操作真实需要 Provider**时成立。

示例：

```text
Healing Module enabled + user invokes healing
→ System module immediate relevant
→ bounded Health provider projection / mutation interface
→ Health owns final bodily state
```

```text
Lottery Module enabled + user draws
→ Program RNG
→ Reward candidate / formal grant path
→ model does not invent random result
```

```text
System Quest accepted
→ World OS Task / Objective owns accepted task state
```

```text
Publicly visible System action
→ Formal Event
→ Reputation downstream activation if applicable
```

Router 不因为 System 理论上可以影响 Character / Health / Relationship / Magic / Divine / Combat，就预加载全部 Provider。

---

# 6. No-load Conditions

- Package included 但 Traveler OFF + System OFF；
- Traveler ON，但当前普通对话 / Combat /移动与 Traveler identity 无关；
- System ON，但当前 Turn 未使用 System；
- 某 Module OFF；
- System ON 且某 Module enabled，但当前只需 Program-side cooldown / currency / persistence 更新；
- 其它 Domain 只需要一个确定性 System fact，例如“当前是否拥有 Appraisal Module”。

OFF 必须是 fail-closed no-load，不允许模型偶尔“自己发系统任务”。

---

# 7. Minimal Read Set

按当前 Feature / Module 读取：

### Traveler

- current Traveler Identity / Origin summary；
- 当前相关 Host Integration policy；
- 与本次问题直接相关的 Otherworld Knowledge provenance；
- player-safe disclosure state。

### System

- System Profile 的必要摘要；
- 当前 relevant Module Definition + enabled state；
- 当前 Module permission / target eligibility；
- 当前相关 currency / cooldown / usage / reward contract 摘要；
- 必要目标 Owner bounded projection。

禁止默认读取：

- 全部 Module；
- 全部 Quest history；
- 全部 Shop catalog；
- 全部 Storage；
- 所有 Provider Core 正文；
- 所有 Character / Health / Relationship / Magic / Divine state。

---

# 8. Model-needed Semantics

模型主要用于：

- 理解玩家对 Traveler / System 的自由语言意图；
- 解释穿越身份、Host Memory、Otherworld Knowledge 等开放式语义；
- 解析非标准 System command / request；
- 生成明确权限范围内的 candidate quest text / system message / appraisal interpretation；
- 在 Ultimate / high-permission Module 中解释玩家想达成的语义目标，但不扩大 Permission Scope。

---

# 9. Program-owned Logic

Program 负责：

- Feature / Module enabled state；
- Conditional Dependency preflight；
- Module permission / target eligibility；
- Currency / cooldown / usage limit；
- Shop / Storage authoritative state；
- Lottery RNG；
- Reward grant validation；
- Accepted Task / Objective formal ownership handoff；
- cross-owner mutation interface；
- Formal Outcome / Atomic Commit；
- Save / Restore。

System 不因“像 GM”而获得未声明 Program Authority。

---

# 10. Output Candidate

模型最多提出：

- traveler / system intent；
- candidate module invocation parameters；
- candidate quest offer text / reward interpretation；
- candidate appraisal interpretation；
- candidate high-permission semantic request；
- clarification need。

模型不得：

- 自己打开未启用 Module；
- 自己扩大 Permission；
- 自己抽 Lottery；
- 直接写 Character / Health / Relationship / Magic / Divine / World State；
- 创建第二 Task / Inventory / Position owner。

---

# 11. Handoff / Information Boundary

### Incoming Provider

只按当前已启用且相关 Module 请求 Character / Health / Relationship / Survival / Magic / Divine / Combat / Item / Position 等 bounded facts。

### Outgoing

- Quest Offer / Reward Contract → World OS Task / Objective；
- Enhancement → Character Capability owner；
- Healing → Health owner；
- Relationship Assistance → Relationship owner；
- Teleport → Position owner；
- Reward / Generation → Item / Resource owner；
- public effects → Event / Reputation downstream。

Appraisal / Traveler knowledge 不允许绕过 Knowledge / player-safe disclosure boundary。

---

# 12. Context Cost / Bounded Strategy

```text
Package Included != every Feature visible
Feature Enabled != every Module visible
Module Enabled != every Turn relevant
Runtime Relevant != full Provider prompt
```

模块数量扩大 5–10 倍时，Router Directory 只增加**当前 Game 真正启用**的 Routing Profile；单个 Turn 只加载本次命中的 Module + bounded Provider projection。

因此 Package capability breadth 不应等价于普通 Turn context breadth。