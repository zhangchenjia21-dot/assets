---
title: ORG + Reputation｜Context Cluster 收敛审核
status: pass
review_date: 2026-08-18
cluster:
  - EP-ORG-CORE v0.1.1
  - EP-REPUTATION-CORE v0.1
review_type:
  - cluster-convergence
  - ownership
  - runtime-context
  - future-explosion
skill: tavern-asset v0.8.0
---

# ORG + Reputation｜Context Cluster 收敛审核

> [!success] 结论
> **PASS。**
>
> ORG 与 Reputation 已形成第一组同时通过 Canonical Ownership 与 Runtime Context Contract 的社会结构 Shared Foundation Cluster。
>
> 本审核确认：`Role / Rank / Membership` 与 `Public Social Evaluation` 不重复；两资产同时 Enabled 不产生 Hard Dependency，也不要求共同常驻 Prompt；可以把本 Cluster 作为旧 Expansion Context Retrofit 的模式冻结依据。

---

# 1. Ownership Lattice

```text
Membership / Role / Rank / Internal Authority → EP-ORG-CORE
Public social evaluation / fame / infamy / epithet → EP-REPUTATION-CORE
Specific A→B Trust / Respect / Sentiment → Relationship Core
Public Political Authority / Recognition → Politics
Legal Status / Wanted / Judgment → Law
```

关键原则：**Formal institutional standing != socially perceived standing。**

---

# 2. 核心反例测试

## 2.1 高职位、低声望

某人是门派执法长老，但门中普遍认为其徇私：Role / Rank → ORG；“徇私”公共评价 → Reputation。无冲突。

## 2.2 无职位、高声望

某普通弟子无正式职位，但在年轻弟子中极具侠名：Membership / Rank → ORG；侠名 → Reputation。无冲突。

## 2.3 私人态度与公共评价相反

门中普遍认为某长老公正；掌门本人极不信任他：group reputation → Reputation；掌门→长老 Trust → Relationship。无冲突。

## 2.4 虚假自称掌门

玩家公开宣称“我就是掌门”。Router 可以 immediate route：ORG + Reputation / social interaction。

- ORG 验证当前 Role Holding 不成立；
- 玩家 Attempt 仍成立；
- 若传播并形成社会看法，再由 Reputation 接管；
- 不因为虚假 Role Claim 自动写入 ORG。

Open Attempt / Ownership 均正确。

---

# 3. Context Inclusion 审核

两资产 Package Hard Dependency 均无。Reputation 可以 Optional / Read-only 使用 ORG target / audience context，不形成 `ORG → Reputation → ORG` Hard Cycle。

正式冻结：

```text
ORG enabled + Reputation enabled
!= ORG context + Reputation context always loaded together
```

---

# 4. 场景级 Working Set 测试

## Scene A｜私人闲聊

Enabled：ORG + Reputation + Relationship。Input：与旧友叙旧。

期望：Reputation / ORG 均可不进入 Model Visible Set；仅当话题涉及公开身份 /名望时 JIT 激活。PASS。

## Scene B｜辞任职位

Input：“我辞去执法堂副堂主。” Immediate：ORG。

Reputation 不参与正式辞任；若公开辞任形成社会评价，等待 Event Handoff。PASS。

## Scene C｜问门派名声

Input：“这个门派在江南武林名声怎么样？” Immediate：Reputation。

Reputation 只需要 organization target ref + relevant Audience；不需要加载全部 Membership / Branch / Role state。PASS。

## Scene D｜利用职位威望压人

Input：“我是执法堂副堂主，让他们给我让路。” 可能 immediate：ORG + Reputation / social response。

ORG 只提供 Role / Authority bounded projection；Reputation 只提供相关 Audience 对该身份 /人物的公共评价。最终 NPC Response 仍由 Runtime / Relationship / Personality。PASS。

---

# 5. Handoff 边界

## ORG → Reputation

允许 Organization target reference、Role / Rank / membership context、public appointment / removal Event context。

禁止 Reputation 反向修改 Role / Rank，也不因“门望很高”自动任命职位。

## Reputation → ORG

默认只读 Context。如果某世界规则规定选举 /任命参考社会声望，最终任命仍由 ORG / Politics 正式流程决定。

---

# 6. Pairwise Integration Explosion 审核

本 Cluster 没有采用 `ORG special reputation system + Reputation special organization-state copy`，而采用 `Canonical Owner + bounded read projection + typed Handoff`。

因此未来新增 Politics / Law / War 时，不需要为每一对 Expansion 重建双向特殊状态。PASS。

---

# 7. Future Explosion Review

规模扩大 5–10 倍：100 个 Organization、数千 Membership、数百 Reputation Audience / Records，仍可通过 Target / Audience / current intent 的 bounded projection 工作。

潜在风险：

1. Audience Scope 若机器实现过于自由，可能形成查询爆炸；
2. Reputation spread 若尝试全图逐节点模拟，可能产生性能爆炸；
3. ORG / Reputation 如果下游复制摘要为 authoritative state，会重新产生 dual truth。

处理原则：G9 只提供受控 Audience / Projection Primitive；Spread 先语义化 /事件化，不预设全网格仿真；Derived Summary / cache 无写回权。

当前无 blocker。

---

# 8. Context Contract Pattern Freeze

基于 ORG v0.1.1 + Reputation v0.1，以下模式足够稳定，可用于旧 Expansion Retrofit：

1. Routing Profile；
2. Immediate Activation；
3. State-mandatory Activation（如适用）；
4. Downstream Activation；
5. No-load；
6. Minimal Read Set；
7. Model-needed Semantics；
8. Program-owned Logic；
9. Output Candidate；
10. Handoff / Information Boundary；
11. Context Cost / Bounded Strategy。

结论：**Context Contract Pattern v0.1 = FROZEN FOR RETROFIT。**

---

# 9. 下一步

暂停新 Core 生产；先执行 Existing Expansion Context Retrofit：

```text
Wave 1
Character → Relationship → Health → Combat → ORG recheck

Wave 2
Survival → Traveler/System

Wave 3
Magic → Divine

Wave 4
Combat Magic
```

Wave 1 后执行 Context Cluster Audit；全部完成后执行 Generic Library Context Convergence。
