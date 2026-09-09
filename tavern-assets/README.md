# sillytavern-assets

个人使用的 SillyTavern 资产创作与维护仓库。

## AI 入口

任何 GPT、Codex、Grok、Kimi 或其它 Agent 开始资产任务前，先读 [`AGENTS.md`](./AGENTS.md)，再读目标工作区最近的局部 `AGENTS.md`。

正式资产正文只保留一份；完整正文留在仓库中，不重复复制进长 Agent Prompt。

## 仓库结构

本仓库同时提供三种互补视图，但正式资产正文只保留一份。

```text
世界包/        # Canonical World Pack Store
人物卡/        # Canonical Character Card Store
拓展包/        # Canonical Expansion Pack Store
资产族/        # Asset Family Workspace：按完整作品聚合创作、审核与版本管理
通用资产库/    # Generic Asset Library Workspace：跨世界通用机制的治理与维护
```

### 1. 按资产类型

`世界包 / 人物卡 / 拓展包` 是正式资产正文的唯一事实源，适合 Creator 的单资产浏览、编辑、导入、版本化与验证。

### 2. 按资产族

`资产族/` 按完整作品聚合 World Pack、Character Cards、专用 Expansion、所消费的通用 Expansion，以及蓝图、版本矩阵、创作规范和审核资料。

资产族目录只保存索引和管理资料，**不得复制第二份正式资产正文**。

### 3. 通用资产库

`通用资产库/` 管理跨多个 World Pack 复用的 Expansion，包括总蓝图、版本矩阵、Owner / Dependency 关系、维护规范和后续路线。

真正的通用 Expansion 正文仍位于：

`拓展包/通用拓展包/`

## 四个概念

```text
世界包 / 人物卡 / 拓展包
= 资产是什么

资产族
= 哪些资产共同组成一部作品

通用资产库
= 哪些机制可以被多个作品复用

Bundle
= 某个资产族在某一版本锁下的交付物
```

## 当前项目阶段导航

项目 current source：`zhangchenjia21-dot/Vibe-Coding/main/sillytavern/酒馆游戏项目开发核心总纲_CURRENT.md`。

截至 2026-08-22：

```text
G9-03 Unified Asset Protocol              PASS / CLOSED
G9-04 Adapter / Compiler / Binding        PASS / CLOSED
G9-05B Shared Creator Core                PASS / CLOSED
G9-05C World Creator                      PASS / CLOSED
G9-05D Character Creator                  PASS / CLOSED
G9-05E Use My Assets Game Creation        PASS / CLOSED
G9-05F Expansion Creator                  PASS / CLOSED
三类主资产完整组合建局与游玩闭环          AUTHORIZED / NEXT
```

当前实现主线：

```text
zhangchenjia21-dot/sillytavern main
26d23d47c5f5ac42d3e1029654a64eda831c4db1
```

本资产仓库的 G9-04 真实语义样本冻结证据基线仍为：

```text
968175e6c3fb3545b7c2907b65089c7e1dbb40a0
```

后续本仓库导航提交不改变该冻结语义证据，也不应为了同步项目阶段而改写正式资产正文。

下一阶段不是继续增加 Creator 类型，而是使用真实 published World + Character + Expansion exact snapshots，完成三类主资产组合建局、Feature/Module Runtime binding、可玩 Session、Save / Continue / Restore / Crash-Recovery 的端到端闭环。