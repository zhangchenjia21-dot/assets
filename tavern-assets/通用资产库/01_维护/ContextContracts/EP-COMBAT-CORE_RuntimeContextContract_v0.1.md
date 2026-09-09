---
title: EP-COMBAT-CORE｜Runtime Context Contract
version: 0.1
status: current-binding-sidecar
created: 2026-08-18
updated: 2026-08-18
applies_to_asset: EP-COMBAT-CORE
applies_to_version: 0.1
canonical_asset: 战斗核心_Expansion_Pack_v0.1.md
contract_role: runtime-context-binding
canonical_domain_ownership: none
pattern: 通用资产库_RuntimeContextContract模式_v0.2
asset_spec_binding: pending-g9
---

# EP-COMBAT-CORE｜Runtime Context Contract v0.1

> [!abstract]
> 本 Sidecar 为 `EP-COMBAT-CORE v0.1` 提供有界 Runtime Context Contract；Combat Context / Relative Range / LOS / Cover / Stance / Pressure / Reaction / Martial Outcome / Physical Impact 等 Domain Semantics 仍只由正式 Combat Core 正文拥有。

---

# 1. Routing Profile

```text
ID: EP-COMBAT-CORE
Name: 战斗核心
Scope: Character-scale 直接战斗、攻击/防御/反应/撤退/制服、战斗距离/视线/掩体、战斗态势与直接战斗结果语义
Typical semantics: 攻击 / 格挡 / 闪避 / 招架 / 射击 / 擒抱 / 追击 / 撤退 / 投降 / 战斗反应 / 直接交战
```

争吵、政治冲突、宏观战争不因“有敌意”自动路由到 Combat。

---

# 2. Immediate Activation

- 玩家输入是可以产生即时直接战斗后果的 Action / Threat；
- 玩家主动攻击、防御、反应、追击、撤退、投降、制服、保护或抢夺；
- 当前输入直接查询 Combat Range / LOS / Cover / Reaction Window / Stance / Pressure；
- 当前目标是改变 Character-scale direct combat state。

---

# 3. State-mandatory Activation

**Active Combat Context** 是正式 state-mandatory 条件。

即使 Router 对一句省略输入只识别 Movement / Character Intent，例如：

> “我继续后退，绕到柱子后面。”

Program 根据 authoritative Active Combat State 可补充 Combat。

但只补充当前局部 Combat Projection，不加载全部 Combat Core 正文或全部战斗历史。

---

# 4. Downstream Activation

Combat 后果不要在第一轮 Router 里展开全部 Domain：

```text
Combat Formal Outcome
├─ Physical Impact → Health
├─ public combat Event → Reputation candidate
├─ Item consequence → Item owner
└─ Position consequence → World OS / Position owner
```

Health / Reputation 等后续 Domain 在正式结果形成后通过 Handoff 激活。

---

# 5. No-load Conditions

通常不加载 Combat：

- 普通争吵、威胁或敌意但没有即时战斗行为；
- 战后治疗；
- 纯 Relationship / Reputation / ORG 互动；
- 宏观 War Campaign / Formation 命令；
- 单纯移动且没有 Active Combat Context；
- 非战斗 Ritual / Magic interaction。

---

# 6. Minimal Read Set

当前 Combat 只读取：

- 当前 active combatants /直接相关参与者；
- 当前 Combat Objective；
- 当前 Relative Range / LOS / Cover；
- Stance / Pressure / Tempo；
- 当前 Reaction Window；
- Character Core 提供的**相关** Capability Projection；
- 直接相关 Weapon / Armor Combat Profile；
- 当前身体限制的 bounded Health Functional Projection（仅在确实影响动作时）；
- 必要 Scene / Position projection。

禁止加载：

- 全人物 Capability Profile；
- 全 Inventory；
- 全地图；
- 全 Health State；
- 全 Combat history；
- 全部下游 Reputation / Law / Relationship 规则。

---

# 7. Model-needed Semantics

模型主要负责：

- 把自由语言战斗表达映射为 Combat Intent / Action Candidate；
- 识别非标准攻击、防御、控制、撤退目标；
- 在有歧义时识别 target / objective / reaction candidate；
- 结合当前局部 Combat Context 产生合法语义 Candidate；
- Program Outcome 已确定后生成不改变结果的战斗叙事。

---

# 8. Program-owned Logic

Program / Runtime 负责：

- Active Combat Context authority；
- Ref / combatant / target validation；
- Range / LOS / Cover 的正式当前值；
- action legality / permission 的确定性边界；
- Resolution Plan；
- RNG / Dice；
- Program Judge；
- Martial / Formal Outcome；
- Physical Impact 的正式生成；
- Atomic Commit；
- Save / Restore。

模型不得把自己的“精彩叙述”反向升级为正式命中、伤害、死亡或状态变化。

---

# 9. Output Candidate

模型最多提出：

- candidate combat intent / action；
- candidate target / objective；
- candidate stance / reaction intent；
- candidate non-standard combat interpretation；
- clarification need。

不得直接给出 Formal Hit / Miss / Damage / Death / Commit。

---

# 10. Handoff / Information Boundary

## Incoming

- Character Core → relevant capability projection；
- Item → relevant weapon / armor profile；
- Position / Scene → local combat spatial projection；
- Health → current relevant functional limitation；
- Magic / Divine / Martial Theme → combat-specific contribution / action candidate。

## Outgoing

- Physical Impact → Health；
- public battle Event → Reputation downstream candidate；
- Item consequence → Item owner；
- movement / placement consequence → Position owner。

## Information Boundary

隐藏敌方 Skill、未发现 Weapon property、看不到的 Position / ambush truth 不自动进入 player-safe Combat Context。

---

# 11. Context Cost / Bounded Strategy

```text
Enabled Combat
!= Combat always in model context
```

```text
Active Combat
!= full world / full character / full health context
```

```text
Hard Dependency Character
!= full Character Core prompt inclusion
```

战斗参与者和历史规模扩大时，单次 Combat Working Set 仍围绕当前 direct engagement 局部化。

---

# 12. G8 / G9 Boundary

当前只冻结 Semantic Context Contract；不提前设计 Action Intent machine schema、Combat Context DTO 或 asset-spec compiler。G9 必须在 G8 Host / Controlled Multi-action 上游完成后再映射机器协议。
