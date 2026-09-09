# Asset Family Workspace Rules

本文件补充仓库根 `AGENTS.md`，适用于 `资产族/`。

## Workspace boundary

资产族目录按完整作品聚合创作、审核、版本与交付关系，但不拥有第二份正式资产正文。

```text
资产族 index / blueprint / matrix
→ 引用
世界包 / 人物卡 / 拓展包 canonical files
```

## 整族任务

当任务要求审核、迁移或更新“整个资产族”时，必须至少检查：

- 当前 family blueprint / index；
- World Pack；
- 全部 Character Cards；
- 专用 Expansions；
- 被消费的通用 Expansions；
- dependency / owner / version matrix；
- 跨文件 refs 与 supersession；
- 当前 bundle / release lock（若已授权存在）。

不得只修改命中的一两个文件后声称整族完成。

## Change delivery

Canonical 正文修改发生在 `世界包/人物卡/拓展包`。同一 delivery 同步更新：

- family index；
- version matrix；
- dependency / reference map；
- audit result；
- old current archive。

## Sequencing

优先完成共享 Core 与通用机制，再建设高耦合专用资产。发现第二个消费者时，重新评估是否应上提到通用资产库，避免多份临时机制。
