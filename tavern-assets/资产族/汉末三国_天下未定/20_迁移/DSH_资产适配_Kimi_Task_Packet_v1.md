# Kimi Task Packet｜汉末三国 DSH-native 资产适配 v1

## Task

在 `zhangchenjia21-dot/sillytavern-assets` 的 `dsh-adaptation-kimi-v1` 分支上，把指定的第二版 SillyTavern 资产改成适合当前 **The World on DeepSeek Harness (DSH)** 的 Source Assets。

这是内容/语义适配，不是 Runtime 重构。

## Branch / Base

- repo: `zhangchenjia21-dot/sillytavern-assets`
- branch: `dsh-adaptation-kimi-v1`
- base before this task packet: `30f5b7dde26639740a5069f15135562aa8a2f3b8`
- do not modify `main`
- do not modify `zhangchenjia21-dot/the-world`

## Read First

1. repository root `AGENTS.md`
2. `资产族/AGENTS.md`
3. this task packet
4. `资产族/汉末三国_天下未定/00_资产成员索引.md`
5. `资产族/汉末三国_天下未定/01_资产组合总蓝图.md`
6. target canonical assets listed below

Do not treat old Vibe-Coding / Creator / asset-spec architecture as the target architecture. The target is DSH-native The World.

## Target Architecture Semantics

Assume:

```text
DeepSeek Harness
+
World Core RPG Game Mode
+
Persistent game workspace
+
Source Assets / optional RPG Expansions
```

Important boundaries:

- Source assets = reusable pre-game material.
- `games/<game-id>/` = live, evolving game reality.
- Game-local changes never rewrite Source.
- World Core already owns new-game composition, recovery, durable maintenance, knowledge boundary, protagonist control mode, pacing guidance and choice scaffolding.
- `GM / Source / System knows X != NPC knows X`.
- T0 前已经发生的历史可以是过去；T0 后未来必须开放，game-local reality beats original history.
- Optional Expansion only activates after explicit player choice.
- Do not assume Creator, asset-spec, Resolver, Bootstrap, World OS, Atomic Commit, typed Event, compiler, unified machine Owner Registry or UI binding exists.
- Markdown-first. Strong model reasoning is expected. Prefer semantic guidance over workflow machinery.

## Files To Adapt

### World Pack

1. `世界包/汉末三国_天下未定_World_Pack_v0.2.3.md`

### Character Cards

2. `人物卡/汉末三国/CC-BATCH-01/刘备__Character_Card__v0.1.2.md`
3. `人物卡/汉末三国/CC-BATCH-01/曹操__Character_Card__v0.1.2.md`
4. `人物卡/汉末三国/CC-BATCH-01/关羽__Character_Card__v0.1.2.md`
5. `人物卡/汉末三国/CC-BATCH-02/张飞__Character_Card__v0.1.1.md`
6. `人物卡/汉末三国/CC-BATCH-01/袁绍__Character_Card__v0.1.2.md`

### Expansions

7. `拓展包/汉末三国/汉末三国_历史参照与分歧_Expansion_Pack_v0.2.md`
8. `拓展包/汉末三国/汉末三国_政争与势力_Expansion_Pack_v0.2.1.md`
9. `拓展包/通用拓展包/人物能力与技艺_Expansion_Pack_v0.1.5.md`
10. `拓展包/通用拓展包/关系与恋爱核心_Expansion_Pack_v0.2.md`
11. `拓展包/通用拓展包/穿越与系统_Expansion_Pack_v0.2.md`
12. `拓展包/通用拓展包/生存需求与环境_Expansion_Pack_v0.2.md`

## Adaptation Direction

### A. Overall

Rewrite these assets so that an excellent Chinese-language GM model can read them directly and use them naturally in a long-running RPG.

Prefer:

- what this asset means;
- what gameplay value it adds;
- what facts/ideas it provides;
- what it should influence;
- what it must not assume;
- how it interacts with other assets in natural language;
- what changes should become durable game facts.

Reduce/remove:

- machine protocol language;
- old Runtime workflows;
- Resolver / Bootstrap / World OS references;
- Creator / asset-spec binding status;
- UI routing / Feature / Module binding;
- typed mutation / event / owner plumbing;
- compiler-oriented repetition;
- preventive guardrail machinery that does not itself add gameplay value.

If an old engineering concept contains useful gameplay semantics, keep the semantics but rewrite it as GM-facing guidance.

### B. World Pack

The World Pack should primarily tell the GM:

- what the Han-end / Three Kingdoms world is;
- historical scope and source mode;
- selectable start eras and what is already past at each start;
- geography, society, institutions, technology, communications, religion and material life;
- identity space for player characters;
- public facts vs GM-only/source facts;
- history inertia without history correction force;
- T0 boundary;
- natural compatibility with optional expansions.

Remove wording like “Runtime must instantiate / Resolver restores / Owner is X”.

Do not delete rich historical or social content just because the old file is long. Delete system-engineering baggage, not world depth.

### C. Character Cards

Each character card should feel like a reusable historical person Source, not an input packet for a Resolver.

Keep and strengthen:

- stable identity;
- personality;
- contradictions;
- motivations;
- decision tendencies;
- capability semantics and limitations;
- relationship style;
- speech / social behavior;
- knowledge provenance;
- what changes with start year;
- what is historical past vs open future.

Rewrite/remove:

- `Historical Baseline Resolver Handoff`;
- `Capability Bootstrap Handoff`;
- machine interface language;
- fixed future-history implications;
- numeric conversion contracts.

Important: A character card does not grant the NPC access to all Source knowledge. The card should make it easy for the GM to ask “why would this person know this?”.

### D. Expansions

An Expansion should add a playable mechanism domain, not recreate a standalone Runtime.

For each Expansion, make it easy for the GM to understand:

1. what experience it adds;
2. what it pays attention to;
3. what causal logic it introduces;
4. how to adjudicate naturally;
5. what state is worth persisting in the game workspace;
6. how failure, success, progress or deterioration feel in play;
7. what it does NOT own;
8. what other packs can enrich it without becoming hidden hard dependencies.

Do not flatten mechanics into pure lore. Keep meaningful mechanical distinctions if they improve play.

## Specific Product Decisions To Preserve

### Historical reference

- Original history is a reference, not a future event queue.
- No “history correction force”.
- Do not create a mandatory divergence percentage.
- Future historical knowledge can lose relevance as conditions change.

### Politics

- Institutions, legitimacy, office, faction, influence and public authority matter.
- Do not turn politics into one universal score or deterministic state machine.
- NPC political behavior follows interests, identity, relationships, information and current conditions.

### Character capability

- Capabilities should matter and develop, but the model should not need a compiler-generated numeric profile to play.
- Avoid RPG-game-number fetish unless a number genuinely improves play.
- World-specific projections such as 三国五维 may exist as optional summaries, not canonical truth that overrides character reality.

### Relationships / romance

- Relationship state must come from shared history, treatment, trust, attraction, obligations, conflict and context.
- No automatic romance because a relationship score crosses a threshold.
- Not every relationship is romantic.
- NPC autonomy remains intact.

### Traveler / System

- “穿越者” and “有系统” are independent choices.
- A traveler may have no system.
- System knowledge/UI is private unless shared or observable.
- The System should add gameplay affordances, not silently make the whole world game-like or omniscient.

### Survival

- Hunger, thirst, sleep, exposure and travel conditions matter when relevant.
- Do not force bookkeeping every turn.
- Compress routine maintenance; surface consequences when meaningful.
- Durable injuries/disease belong to durable game reality; do not reset after a scene.

## Dependency Rules

Do not preserve old dependency graphs mechanically.

Use these rules:

- only call something a hard requirement if the asset literally cannot make sense without it;
- otherwise describe synergy in prose;
- optional packs remain independently selectable;
- World Pack may suggest useful expansions but never silently enable them;
- do not invent Required / Recommended / Optional machine metadata for the new DSH target.

## Chinese Writing Goal

Kimi should actively improve Chinese localization quality:

- natural contemporary Chinese for long-form reading;
- historical concepts use appropriate Chinese terminology;
- preserve era texture through titles, institutions, social relations, etiquette, material life and worldview;
- avoid pseudo-classical filler;
- reduce unnecessary English runtime jargon;
- write like high-quality material for an AI GM, not like backend protocol documentation.

## Experimental Branch Rule

This is a comparison branch, not a formal release.

For v1:

- modify the 12 existing files in place on `dsh-adaptation-kimi-v1`;
- do not rename files;
- do not bump asset versions yet;
- do not archive old files;
- do not synchronize the family version lock / release governance yet;
- do not touch non-target canonical files except when a broken direct reference inside a target file must be corrected;
- do not touch `main`.

Git history provides the old version for diff comparison.

## Acceptance Criteria

PASS only if all are true:

- [ ] assets no longer require the old SillyTavern Runtime architecture to be useful;
- [ ] DSH GM can understand how to use each file directly;
- [ ] World Pack remains rich world content rather than becoming a short prompt;
- [ ] Character Cards preserve distinctive personality and historical grounding;
- [ ] Expansions preserve actual gameplay mechanics, not only descriptions;
- [ ] Source truth vs game-local truth is clear;
- [ ] NPC knowledge provenance is clear;
- [ ] T0 past/open-future boundary is clear;
- [ ] optional expansions do not silently activate;
- [ ] `穿越者 != 带系统的穿越者` remains explicit;
- [ ] no new universal schema / manifest / validator / runtime is invented;
- [ ] Chinese prose is cleaner and more locally natural than the old version.

## Git Delivery

Commit the adaptation to `dsh-adaptation-kimi-v1` in logical groups. Suggested grouping:

1. World Pack
2. 5 Character Cards
3. 2 Han-specific Expansions
4. 4 Generic Expansions
5. final cross-asset consistency cleanup

Do not merge to main.

## Final Report

Return:

```markdown
## Result
PASS | PARTIAL | BLOCKED

## Files Adapted
- path

## Main Changes
- old-runtime assumptions removed
- gameplay semantics retained/strengthened
- Chinese localization improvements

## Cross-asset Decisions
- dependency changes
- knowledge-boundary changes
- T0/history changes

## Git
- base HEAD
- final HEAD
- commits

## Remaining
- unresolved questions for GPT review
```

After Kimi finishes, GPT will perform the diff / architecture review before anything is considered for The World.