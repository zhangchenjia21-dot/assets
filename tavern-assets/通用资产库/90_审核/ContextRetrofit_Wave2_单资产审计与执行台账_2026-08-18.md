---
title: Context Retrofit Wave 2｜单资产审计与执行台账
status: pass
version: 1.0
date: 2026-08-18
wave: 2
assets:
  - EP-SURVIVAL v0.2
  - EP-TRAVELER-SYSTEM v0.2
pattern_candidate: 通用资产库_RuntimeContextContract模式_v0.3
---

# Context Retrofit Wave 2｜单资产审计与执行台账

> [!success] 结论
> `EP-SURVIVAL v0.2` 与 `EP-TRAVELER-SYSTEM v0.2` 的 Canonical Domain Semantics 均保持 PASS；两者缺口主要是 Runtime Context Binding，因此正文版本不变，采用唯一 Sidecar Retrofit。
>
> 本轮新增两条跨资产稳定模式：
> 1. `Background deterministic progression != Model Activation`；
> 2. `Package Included != Feature Enabled != Module Enabled != Runtime Relevant != Model Visible`。

---

# 1. EP-SURVIVAL v0.2

## Canonical Ownership

正文已经清晰区分：

- Survival Own：Need / Routine Automation / Survival Load / Environmental Exposure Process；
- Health Own：持续身体 Condition / HP / Consciousness；
- Resource / Item / Economy Own：真实库存；
- World Own：环境事实。

结果：**PASS**。

## Program Authority

正文已经明确模型不拥有 HP、RNG、Formal Outcome、Atomic Commit；日常自动化真实消费 Resource。

结果：**PASS**。

## Context Gap

需要补充：

- Routine Need / Exposure 可以在后台 Program progression；
- 后台 tick 不需要模型；
- 只有玩家输入、warning / decision context 或开放式 Survival Strategy 才进入 Model Visible；
- Health 通过 threshold handoff downstream 激活。

分类：**WORKSPACE / METADATA ONLY → sidecar**。

---

# 2. EP-TRAVELER-SYSTEM v0.2

## Canonical Ownership

正文已经成熟表达 Traveler / System 双 Feature、Module Permission、Module Conditional Dependency，并拒绝第二 Character / Health / Relationship / Task / Position owner。

结果：**PASS**。

## Context Gap

需要把已有 Feature / Module 架构正式传播到 Context Orchestration：

```text
Package Included
!= Feature Enabled
!= Module Enabled
!= Runtime Relevant
!= Model Visible
```

并要求 Router Directory 只暴露当前 Game 已启用 Feature / Module，而不是整个 Package 的理论能力全集。

分类：**WORKSPACE / METADATA ONLY → sidecar**。

---

# 3. Pattern Change Assessment

上述两条不是只对 Survival / Traveler 有效：

- 任何长期 Need / cooldown / timer / routine automation 都可能需要后台 Program progression 而无需模型；
- 任何带 Feature / Module 的 Expansion 都可能出现“Package Enabled = 全部 Module 进入 Router”的 context explosion。

因此：

> **升级 Context Pattern v0.2 → v0.3，并升级 tavern-asset v0.8.0 → v0.8.1。**

同时作为 G9-02 Runtime Context Orchestration 的正式上游增量，更新项目第 15 号核心裁定。

---

# 4. G8 / G9 Gate

当前最新项目事实：WEB-04 Host prerequisite 已 PASS；G9 仍被 G8 Exit Gate 阻塞。

本轮只冻结 Semantic Runtime Profile / Context Contract，不实现 Router API / Context Compiler / Schema，因此不违反 Host-before-protocol。

结果：**PASS**。