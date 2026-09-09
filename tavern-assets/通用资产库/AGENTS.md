# Generic Asset Library Rules

本文件补充仓库根 `AGENTS.md`，适用于 `通用资产库/`。

## Canonical boundary

通用资产库负责跨世界机制的治理、蓝图、Owner、依赖、版本与消费者矩阵。真正的通用 Expansion 正文仍位于：

`拓展包/通用拓展包/`

不得在本目录复制第二份正文。

## Core-first

通用机制默认按以下顺序维护：

```text
Domain / capability survey
→ shared primitive
→ canonical owner
→ semantic contract
→ real asset-family consumers
→ convergence audit
→ downstream specializations
```

专用资产不得反向成为通用机制的隐性 Owner。

## 修改通用资产时

必须检查：

- canonical Expansion path / version；
- owner 与 semantic namespace；
- hard / optional / handoff / feature-conditional dependencies；
- 所有已登记 consumer asset families；
- Runtime Context Contract 与 player/private boundary；
- breaking semantic change 与 migration；
- blueprint / version matrix / maintenance roadmap；
- superseded current 的归档。

若改动影响消费者，正文与 consumer references 应在同一 delivery 同步；不能只更新总蓝图而留下漂移的 canonical assets。

## Stage boundary

External machine schema、Creator binding、Validator 与 Bundle protocol 只有项目 current source 正式授权后才建立。通用库可以先冻结语义和依赖，不得抢跑并反向定义 Host / Runtime。
