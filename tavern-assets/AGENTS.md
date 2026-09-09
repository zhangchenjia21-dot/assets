# sillytavern-assets｜Repository Agent Rules

状态：current  
适用范围：本仓库全部世界包、人物卡、拓展包、资产族与通用资产库

## 1. 仓库定位

本仓库是 SillyTavern **语义资产内容**的当前事实源。

```text
世界包/        Canonical World Pack Store
人物卡/        Canonical Character Card Store
拓展包/        Canonical Expansion Pack Store
资产族/        按作品聚合的创作、审核、依赖与版本工作区
通用资产库/    跨世界通用 Expansion 的治理与维护工作区
```

产品 Runtime、Creator、机器 Schema 与阶段裁定不由本仓库决定：

```text
项目产品 / 架构 / Stage
→ zhangchenjia21-dot/Vibe-Coding/main/sillytavern/

资产创作与维护 Skill
→ zhangchenjia21-dot/Vibe-Coding/main/skill/gpt/tavern-asset/SKILL.md

正式 Agent 指令
→ zhangchenjia21-dot/Vibe-Coding/main/skill/gpt/agent-task-packet/SKILL.md
```

## 2. Canonical Ownership

正式资产正文只保存一份：

- World Pack 正文 → `世界包/`；
- Character Card 正文 → `人物卡/`；
- Expansion 正文 → `拓展包/`。

`资产族/` 与 `通用资产库/` 只能保存：

- index；
- blueprint；
- dependency / owner matrix；
- version lock；
- audit / migration / maintenance material；
- 对 canonical 文件的引用。

禁止把第二份正式资产正文复制进治理工作区。

## 3. Freshness 与 Current-only

正式任务开始时：

1. 获取 `main` 当前 HEAD；
2. 读取本文件与目标目录最近的 `AGENTS.md`；
3. 读取 `Vibe-Coding/skill/` 下相关 Skill current；
4. 定位资产族或通用资产库 current index；
5. 再读取被引用的 canonical assets；
6. 检查 `status / version / supersedes / archive`。

同一资产或治理文档族在 active 目录只保留一个 current。历史进入 `99_归档/`、明确 archive 目录或 Git history，不让 Agent 靠文件名猜最新版。

正式写回前重新检查 HEAD；不得用旧 Base 覆盖并行更新。

## 4. 最小充分工作集

单资产任务默认初始读取：

```text
AGENTS.md
→ 目标资产
→ 所属资产族 / 通用库 index
→ 直接依赖或被依赖资产
→ 相关审计 / 测试规则
```

不要无差别读取整个资产仓库。

当任务明确针对“整个资产族”“整个通用库”“依赖迁移”时，必须扩大到所有受影响成员和引用，不能只修改命中的单文件。

```text
Repository Total Assets
!= Initial Agent Working Set
```

## 5. Asset Change Propagation

修改 canonical asset 后，必须检查：

- asset id / version / filename；
- `depends_on / optional / handoff / consumes`；
- owner 与 semantic namespace；
- World Pack / Character Card / Expansion 的引用；
- 资产族 blueprint / version matrix / release lock；
- 通用资产库 consumer matrix；
- 旧版本是否需要归档；
- bundle / manifest 是否属于当前授权范围。

正文、索引、版本与依赖更新应在同一 delivery 中闭环。

## 6. Core-first 与依赖纪律

多个资产共享同一机制时，优先：

```text
shared domain survey
→ generic core / canonical owner
→ typed semantic contract
→ real consumer audit
→ downstream world-specific assets
```

禁止先为多个专用资产复制临时机制，再事后反向抽取 Core。

依赖必须区分 hard、optional、handoff、feature-conditional 与 read-only reference；依赖关系不自动等于 Runtime Prompt inclusion。

## 7. Semantic Asset 阶段边界

当前机器 Manifest、Bundle Schema、Validator、Creator Binding 与 external asset-spec 只有在 `Vibe-Coding` 当前项目阶段正式授权后才能建立。

在未授权前：

- 允许完善语义正文、owner、dependency、identity、context contract 与迁移计划；
- 不把临时 frontmatter 冒充已冻结机器协议；
- 不让资产仓库反向定义尚未证明的 Runtime / Host capability。

## 8. 质量与安全

- source / owner identity 穿过 adapter / assembly 引用时不得丢失；
- private / hidden / player-safe 内容边界必须明确；
- 不使用 display name 或自然语言相似度临时猜 owner / identity；
- 不破坏稳定 asset id 与跨文件引用；
- 不用批量替换掩盖逐资产语义差异；
- 不执行 destructive Git 操作覆盖未知工作树。

## 9. 正式 Agent 指令

GPT 为 Codex、Grok 或其它 Agent 生成资产任务时，使用 `Vibe-Coding/skill/gpt/agent-task-packet`，至少说明：

- repo / branch / base HEAD；
- current Skill 与资产事实源；
- 目标资产族 / canonical assets；
- Read First；
- Allowed / Prohibited；
- INV / AC / NON；
- 依赖与引用传播范围；
- Git 与 final report。

完整资产正文留在仓库，不复制进长 Prompt；执行 Agent 无法读取仓库时才提供必要摘要或附件。

## 10. Final Report

正式任务结束时报告：

```markdown
## Result
PASS | PARTIAL | BLOCKED

## Canonical Assets Changed
- path / old version / new version

## Governance Synced
- family index / generic matrix / refs / archive

## Evidence
- searches / audits / validation

## Git
- base HEAD / final HEAD / commit / push / final status

## Remaining
- unresolved dependencies / migration / next gate
```