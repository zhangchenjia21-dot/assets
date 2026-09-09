---
title: EP-SURVIVAL｜Runtime Context Contract
version: 0.1
status: current-context-sidecar
created: 2026-08-18
updated: 2026-08-18
asset_id: EP-SURVIVAL
asset_version: 0.2
asset_title: 生存需求与环境
contract_location: sidecar
canonical_domain_ownership: none
pattern: 通用资产库_RuntimeContextContract模式_v0.3
skill: tavern-asset v0.8.1
asset_spec_binding: pending-g9
---

# EP-SURVIVAL｜Runtime Context Contract v0.1

> [!abstract]
> 本 Sidecar 只补齐 `EP-SURVIVAL v0.2` 的 Runtime Context Binding，不改变 Survival 的 Canonical Domain Semantics。
>
> Survival 正文继续拥有 Nutrition / Hydration / Sleep Need、Routine Survival Automation、Survival Load 与 Environmental Exposure Process；Health 继续拥有持续身体 Condition / HP / Consciousness。
>
> 本 Contract 重点冻结：**后台生存进度可以由 Program deterministic 持续推进，但这种后台推进本身不等于模型必须被激活。**

---

# 1. Routing Profile

```text
ID: EP-SURVIVAL
Name: 生存需求与环境
Scope: 营养、饮水、睡眠等生存需求，日常生存自动化，资源真实消费，环境暴露过程与 Survival Load
Typical semantics: 饿 / 渴 / 睡眠不足 / 熬夜 / 休息 / 进食 / 饮水 / 露营 / 严寒酷热暴露 / 长时间赶路劳动 / 生存资源是否够用
```

Routing Profile 只用于第一轮语义路由，不把完整 Survival 规则注入 Router。

---

# 2. Immediate Activation

典型 immediate activation：

- 玩家询问自己或目标角色当前 Hunger / Hydration / Sleep 等生存状态；
- 玩家主动决定进食、饮水、睡觉、熬夜、禁食、强行赶路、露营或寻找庇护；
- 玩家直接询问环境是否会构成持续生存风险；
- 当前行为的主要问题是“日常生存条件能否满足”，而不是已经形成的 Health Condition；
- 玩家覆盖 Routine Survival Automation；
- 当前行动需要选择具体 Survival Resource / Shelter / Protection strategy。

不因为“这个角色当然每天要吃饭喝水睡觉”就让 Survival 常驻模型上下文。

---

# 3. State-mandatory / Background Runtime Activation

Survival 必须区分：

```text
Runtime Background Progression
!=
Model Activation
```

当 World Time 推进时，Program 可以在后台 deterministic 更新：

- Nutrition / Hydration / Sleep deficit；
- Routine Automation eligibility；
- 已授权的日常 Resource Consumption；
- Survival Load accumulation；
- Environmental Exposure duration / accumulation；
- threshold / handoff condition。

这些后台计算属于 Runtime Relevant，但**默认不进入 Model Visible Working Set**。

模型仅在以下情况下需要加入：

- 玩家输入直接涉及 Survival；
- 当前需要开放式解释 /选择某种生存策略；
- 阈值已经产生需要玩家理解的 warning / decision context；
- 需要生成 player-safe 的生存状态解释。

若只是一次完全 deterministic 的后台 tick，不进行模型调用。

---

# 4. Downstream Activation

Survival 不要求 Router 第一轮预判所有身体后果。

正确链：

```text
World Time / Environment / Resource State
↓
Survival Need / Exposure / Load progression
↓ threshold
Survival Handoff
↓
EP-HEALTH-CORE downstream activation
```

Health 决定：Dehydration、Physical Fatigue、Weakness、Hypothermia 等持续身体事实。

反方向读取：Health 的当前 Functional Effect 可以作为 Survival 决策 Context，但 Survival 不复制 Health State。

---

# 5. No-load Conditions

以下场景通常不加载 Survival 模型 Context：

- 普通私人聊天，且不存在生存决策；
- 普通 Combat action resolution，且无需处理脱水 /疲劳等相关 bounded effect；
- 纯 Relationship / ORG / Reputation 操作；
- 一次正常且 deterministic 的 Routine Meal / Water / Sleep automation；
- 仅有后台 deficit accumulation，但没有达到玩家需要处理的 threshold；
- 仅需读取“当前是否明显疲惫 / 是否缺水”等一个确定性 projection 的其它 Domain。

---

# 6. Minimal Read Set

根据当前 Intent，只读取：

- 当前相关 Character / Actor；
- 本次相关 Need（Nutrition / Hydration / Sleep）或 Exposure / Load；
- 相关当前 deficit / semantic band；
- 必要 World Time delta；
- 当前相关 Resource / Shelter / Protection availability 摘要；
- Player Override / Routine Automation state；
- 当前直接相关 Health Functional Effect（只读，若有）；
- 必要的 player-safe warning state。

禁止为一个“我现在渴不渴”的问题加载：

- 全部角色 Survival State；
- 完整历史饮食记录；
- 全地图天气；
- 全 Inventory；
- 完整 Health history。

---

# 7. Model-needed Semantics

模型主要用于：

- 理解玩家自由语言中的生存意图与 Override；
- 解释开放式 Survival Strategy，例如“找背风处搭临时营地”；
- 在多个可用生存方案之间形成语义 Candidate；
- 把 bounded Survival State 转成玩家可理解但不泄漏隐藏数值的反馈；
- 解释非常规环境条件对 Survival Process 的语义影响候选。

模型不负责持续时间累积、资源扣减、Need 数值推进或 Health Condition 判定。

---

# 8. Program-owned Logic

Program / authoritative Runtime 负责：

- World Time 驱动的 Need / Exposure / Load progression；
- Routine Survival Automation 是否满足 deterministic 条件；
- 真实 Resource existence / consumption commit；
- Player Override persistence；
- deterministic threshold / warning checks；
- Need → Health Handoff trigger；
- State persistence / Save / Restore；
- Formal Outcome / Atomic Commit；
- ID / Ref validation。

**后台 deterministic progression 不应为了“保持世界活着”而持续消耗模型调用。**

---

# 9. Output Candidate

模型最多提出：

- survival intent；
- candidate player override；
- candidate survival strategy；
- candidate resource / shelter choice；
- candidate warning / explanation；
- clarification need。

模型不得直接写 Need State、扣减库存、生成 Health Condition 或提交时间推进。

---

# 10. Handoff / Information Boundary

## Incoming

- World / Environment → 当前环境与时间 Context；
- Item / Resource / Economy → 可访问资源、庇护与防护 Context；
- Character → 相关 Capability projection（Optional）；
- Health → 当前相关 Functional Effect（只读）。

## Outgoing

- Health → Need / Exposure / Load 已达到具有身体意义的 Cause；
- Narrative / UI → player-safe survival warning / status projection；
- Resource Owner → routine / explicit consumption request。

隐藏 deficit 数值、NPC 未知身体风险、后台资源真相不能因为 Survival 被启用就全部进入 Router / Narrative / Player Context。

---

# 11. Context Cost / Bounded Strategy

```text
Enabled Survival != Survival always in model context
Background Survival Progression != model call
All Need History != Current Need Projection
All Environment State != Current Exposure Slice
```

Character 数量、历史时长和 World Time 增长 5–10 倍时，普通无关 Turn 仍只发生 Program-side progression；模型成本不应跟着生存时间线性增长。

当前不冻结 token budget；G9-02 / G11 用真实 Provider 验证。