---
title: EP-MAGIC-COMBAT｜Runtime Context Contract
version: 0.1
status: current-context-sidecar
created: 2026-08-18
updated: 2026-08-18
asset_id: EP-MAGIC-COMBAT
asset_version: 0.3
asset_title: 战斗魔法
canonical_asset_path: 拓展包/通用拓展包/魔法族/战斗魔法_Expansion_Pack_v0.3.md
canonical_domain_ownership: none
pattern: 通用资产库_RuntimeContextContract模式_v0.5
generic_identity_status: normalized-workspace-binding
reference_world_consumer: 埃瑟维亚_诸界余辉
asset_spec_binding: pending-g9
---

# EP-MAGIC-COMBAT｜Runtime Context Contract v0.1

> [!abstract]
> 本 Sidecar 只为 `EP-MAGIC-COMBAT｜战斗魔法 v0.3` 补充 Runtime Context Binding。
>
> Canonical Combat Spell Definitions、战斗施法 Skill Contribution、Combat Style、Spell-specific Martial Coupling 与 Combat Countermagic Theme Semantics 仍全部由正式资产正文拥有。
>
> 本文件不获得 Character / Magic / Combat 的上游 Domain Ownership，不修改 52 个 Combat Spell，不改变 Formal Outcome，也不把诸界余辉变成 Generic Owner。

---

# 1. Routing Profile

```text
ID: EP-MAGIC-COMBAT
Name: 战斗魔法
Scope: 把 Spell Magic 以武器、投射物、移动、Reaction、Martial Coupling 与战斗化 Countermagic 方式用于个人/小队直接交战
Typical semantics: 战斗施法 / 魔剑士 / 魔弓手 / 魔猎者 / 影行者 / 敌法者 / 断法斩 / 截咒 / 破障 / Reaction Counter / Martial Coupling
```

Routing Profile 不枚举 52 个 Combat Spell，也不复制 Magic Core / Combat Core 规则。

---

# 2. Immediate Activation

典型 immediate activation：

- 玩家明确施展、学习、教授、浏览或讨论 `EP-MAGIC-COMBAT` 提供的 Combat Spell；
- 玩家描述“把法术和武器攻击 / 投射攻击 / 战斗移动 / Reaction 结合”的当前动作；
- 当前输入明确涉及 Combat Style：魔剑士、魔弓手、魔猎者、影行者、敌法者；
- 当前动作明确是战斗化 Countermagic，例如截咒、断法、破障、护卫式反制；
- 已选中的 Spell Definition provenance 指向 `EP-MAGIC-COMBAT`；
- 玩家当前要求浏览 / 搜索 Combat Spell Library。

以下情况不因为 Hard Dependency 存在就自动 immediate：

- 普通非魔法 Combat；
- 普通 Spell Magic 但 selected Spell 不属于 Combat Magic；
- Character 会战斗魔法但当前只在社交 /旅行 /休息。

---

# 3. State-mandatory Activation

以下 authoritative state 可使 Combat Magic 成为 Runtime Relevant：

- 当前存在由 Combat Magic Definition 创建且仍需本 Theme 解释的 active Spell Effect / Mark / Suppression Field；
- 当前 Formal Action 已绑定一个 Combat Magic Spell Ref，尚处于未完成 Coupling / Countermagic continuation；
- 当前正在处理一个已正式成立的 Combat Reaction Window，且合法候选 Reaction Spell 属于 Combat Magic；
- 当前 selected Definition / effect provenance 指向 `EP-MAGIC-COMBAT`，并且本步需要读取其 Theme-specific condition。

但：

```text
Active Combat
!= Combat Magic state-mandatory
```

角色在战斗中、角色拥有 Combat Spell、Magic Core 与 Combat Core 同时 Enabled，都不能让 Combat Magic 永久常驻 Working Set。

---

# 4. Downstream Activation

本 Theme 特别依赖 **Outcome-gated continuation**。

例如 `CBT-040｜断法斩`：

```text
Player Intent: 断法斩
→ Combat Core resolves approach / attack / effective_contact
→ miss / no contact
   → no Countermagic continuation
→ effective_contact
   → EP-MAGIC-COMBAT Coupling Condition becomes relevant
   → EP-MAGIC-CORE Countermagic resolution
   → Program Formal Composite Outcome
```

因此：

> **Potential downstream capability != preloaded downstream context。**

同理：

- Reaction Spell 只有在真实 Reaction Window 成立后继续；
- Barrier / maintained Spell / casting process 只有在成为真实 interaction target 后加载对应 bounded Magic projection；
- Health 只有真实身体后果形成后通过 Handoff 激活；
- Divine 只有真实 Spell↔Divine interaction target 存在时读取 bounded Divine Interaction Profile。

---

# 5. No-load Conditions

通常不加载 Combat Magic 详细 Context：

- 无关闲聊、旅行、组织、关系、名望等普通 Turn；
- 普通武器战斗，当前没有 Combat Spell / Countermagic / Coupling；
- Magic Domain 当前活跃，但 selected Spell 来自 Magic Core 或其他 Theme；
- Combat Magic Effect 已经结束，只剩 Health / World 等下游 Owner 的持续状态；
- 角色知道很多 Combat Spell，但当前没有浏览、学习、选择或施展它们；
- Combat / Magic 后台 deterministic bookkeeping。

---

# 6. Minimal Read Set

Combat Magic 激活后构建 **Owner-preserving bounded join**：

```text
Character minimal projection
+
Magic minimal projection
+
Combat minimal projection
+
selected Combat Magic Definition projection
(+ optional bounded provider projection only when truly relevant)
```

典型只读取：

### Character Provider
- 当前 actor ref；
- 相关 Combat / Magic capability；
- `战斗施法` 与真正相关的武器 / 远程 /移动 /感知 Skill；
- 不读取完整 Character Profile。

### Magic Provider
- 当前 Spell access / Mastery；
- Magic Strain / Casting Load 所需投影；
- Countermagic / Dispel 当前相关 interaction profile；
- 不读取完整 Magic Core / Spell Registry。

### Combat Provider
- 当前 Range / LOS / Cover / Pressure；
- 当前 Martial Outcome；
- `effective_contact` / Reaction Window / Interruption Trigger 等本步必要事实；
- 不读取完整 Combat Core。

### Combat Magic
- **selected Spell Definition**；
- 或极少量 intent-relevant candidate definitions；
- Theme-specific Coupling / Style semantics。

### Optional Providers
- Divine：仅 selected target 真正需要时读取 bounded Divine Interaction Profile；
- Health：仅身体限制/后果真正在当前职责需要时读取 relevant functional effect。

禁止：

```text
EP-MAGIC-COMBAT active
→ Character full context + Magic full context + Combat full context
```

---

# 7. Model-needed Semantics

模型适合：

- 解释玩家自由语言中的 combatized spell intent；
- 在当前 actor-accessible Combat Spell subset 中识别 selected / candidate Spell；
- 解释开放式 Spell↔Martial coupling intent；
- 在信息边界内解释 Countermagic target / tactic；
- Style Profile 的开放式战术语义；
- selected Definition 的 player-safe semantic realization。

模型不负责判定真实命中、Reaction Window 是否成立、Counter 是否成功或正式伤害/状态变化。

---

# 8. Program-owned Logic

Program / authoritative Owners 负责：

- Hard Dependency enablement；
- actor 是否真正掌握 Spell / Skill；
- Definition Ref / provenance；
- Range / LOS / Cover / movement legality；
- Martial hit / effective_contact / defense outcome；
- Reaction Window / action order / interruption timing；
- Casting Load / Magic Strain authoritative state；
- Countermagic / Dispel deterministic gates + RNG / Dice；
- Barrier / Focus / Casting Process authoritative refs；
- Formal Composite Outcome；
- Effect Instance lifecycle；
- Atomic Commit / Save / Restore / Recovery。

Theme 不成为上述事实的第二 Owner。

---

# 9. Output Candidate

模型最多提出：

- `combat_magic_intent`；
- `candidate_combat_spell_ref` / small ranked set；
- `candidate_martial_coupling`；
- `candidate_countermagic_intent`；
- `candidate_reaction_spell`；
- `candidate_target`；
- `clarification_need`。

Candidate 不等于 Martial Outcome / Counter Success / State Mutation。

---

# 10. Handoff / Information Boundary

Incoming：

- Character → relevant capability / skill projection；
- Combat → current Martial Outcome / Reaction / range / opposition projection；
- Magic → selected Spell / Countermagic interaction / Magic Strain projection；
- Divine → bounded Divine Interaction Profile（仅相关时）；
- Health → current functional limitation（仅相关时）。

Outgoing：

- Magic → Spell / Countermagic continuation；
- Combat → spell-in-combat interaction candidate / effect requested by current action；
- Health → bodily consequence only after formal effect；
- World / Item → corresponding formal effect / target handoff；
- Narrative → only player-safe committed result and durable refs。

Information Boundary：

- 敌法者不自动读取对手完整 Spell List / Mastery / hidden Strain；
- `识式瞬读`只给本步已合法获得的有限信息；
- hidden Divine authority / covenant truth 不因 anti-magic 进入 Context；
- selected Definition 可见不等于整个 Theme Library 可见。

---

# 11. Context Cost / Bounded Strategy

冻结：

```text
Character + Magic + Combat = Hard Dependencies
!=
Character + Magic + Combat full prompt inclusion
```

```text
Combat Magic Enabled
!= 52 Combat Spell always visible
```

```text
Magic/Combat state grows
!= current Combat Magic join grows proportionally
```

Context 成本由当前选中 Spell、当前 actor、当前 Combat Outcome / Reaction、当前 target complexity 决定，而不是 Provider 正文大小或总 Definition 数量。

---

# 12. Feature / Theme Activation Hierarchy

Combat Magic 是 Magic 上的 Reusable Theme，同时依赖 Combat Core。

```text
Magic Enabled
+ Combat Enabled
!= Combat Magic Enabled

Combat Magic Enabled
!= every Combat Spell relevant
```

未启用 Combat Magic 时，其 52 个 Definitions 不进入当前 Game 的可检索 Theme Registry。

---

# 13. Background Program Progression

可由 Program 后台处理：

- active Combat Magic Effect duration / expiry；
- deterministic field / mark timer；
- Magic Strain recovery；
- 已提交持续效果的固定 bookkeeping。

后台 progression 不自动触发模型。

---

# 14. Definition Registry / Library Projection

Combat Magic 当前维护 **52 个 Combat Spell Definition**。

默认链：

```text
Combat Magic enabled registry
→ actor-known / actor-accessible Combat Spell subset
→ intent-relevant retrieval
→ selected Definition projection
→ Model / Program step
```

第一轮 Router 不需要看到 52 个 Spell 名称。

例外：玩家当前职责就是“浏览 /搜索 Combat Spell Library”时，可以分页 /分类 /搜索式检索较大的 player-safe subset，但仍不要求一次全文 Prompt。

---

# 15. Bounded Sufficiency / Context Completeness

为正确理解一个 Coupled Combat Spell，不能只给 `CBT-040` 的名字。

至少要保留当前职责真正需要的：

- selected Spell core effect / requirement / coupling boundary；
- 当前 Martial prerequisite / Outcome；
- actor relevant Mastery / Skill / Strain；
- target / range / reaction / information boundary。

`Bounded` 不能裁掉决定“是否可以继续 Coupling / Counter”所需的关键事实。

---

# 16. Narrative Affordance / Runtime Referent

以下 durable/interactable 内容必须先拥有 authoritative ref / Effect Instance，再由 Narrative 描述：

- 抑术场；
- 猎印 / 禁制印；
- 持续武器强化；
- 可被后续驱散/破坏的 Spell Effect；
- 当前可交互 Barrier / Focus / Casting Process；
- 由 Combat Magic 造成并承诺跨步持续的其他对象/状态。

纯瞬时光效、音效、动作表现可以 Narrative-only。

最新 G8 Semantic Materialization 进一步确认：generic label / placeholder 不能冒充 concrete durable referent。

---

# 17. Cross-Owner Projection Join

本 Theme 是多 Provider 组合资产的 Reference Case。

正式规则：

> **Theme / Composite Expansion 可以依赖多个 Canonical Provider，但模型 Working Set 必须是 current-purpose、owner-preserving 的 bounded projection join，而不是 transitive dependency expansion。**

每个 Provider 只提供自己拥有的当前事实；Combat Magic 不复制这些事实，也不在 Sidecar 中建立 mirror state。

---

# 18. Outcome-Gated Continuation Activation

对 Cross-Action / Reaction / Countermagic 等多阶段能力：

> **Potential continuation 不等于当前已激活 Context。**

只有正式上游 Outcome / Trigger 成立后，才把后续 Owner / Definition projection 加入 Current Relevant Set。

这既降低 Context，也避免模型提前假设“武器已经命中 / Reaction 已成立 / Barrier 可被驱散”。

---

# 19. Generic Identity Normalization

审计结论：`战斗魔法 v0.3` 正文的 Canonical Mechanism 已跨世界成立。

- `asset_family: 通用拓展包资产库`；
- World Pack 只决定社会解释 /教授方式 /禁令 /地方名称；
- 诸界余辉仅是 `reference_world_consumer`；
- 正文没有把埃瑟维亚专名写入 Combat Magic Canonical Mechanism。

历史 `skill: tavern-asset v0.5.2` / `blueprint v0.1` 解释为 authoring provenance；current binding 由 Generic Library current Matrix / Blueprint / Context Index / `tavern-asset v0.9` 决定。

因此本轮：**不改 62KB Canonical Asset Body Version；以 Sidecar + Workspace binding 完成 normalization。**
