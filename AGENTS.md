# AGENTS.md｜assets 仓库读写协议

本仓库是多项目资产 / 事实 / 证据仓库，不把项目专属内容长期堆在仓库根。

## 1. 项目定位

处理某个项目时：

```text
仓库根 AGENTS.md
→ 对应项目 README.md
→ 对应项目 AGENTS.md
→ 项目 current/README.md
→ 项目 current/项目状态.md
→ 与任务直接相关的 Authority / Evidence
```

当前 Minecraft `建筑师` 项目唯一主路径：

`minecraft/建筑师/`

## 2. 写入边界

Owner 已于 2026-09-09 授权：`建筑师` Minecraft AI Build 项目的后续任务，在完成并验证后，默认把该任务应持久化的成果 commit / push 到本仓库，无需每次重复询问是否 push。

但必须：

- 写入 `minecraft/建筑师/` 下正确的事实类型目录；
- 不把项目专属文件重新散落到仓库根；
- 不自动上传原始 Minecraft 存档、完整备份、凭据、账户数据或无关 Mods；
- 保持真实验收状态，`PARTIAL` 不得包装为 `PASS`；
- 大文件必须满足 GitHub 限制，并保存恢复方式与哈希证据；
- 并发更新先确认远端 HEAD，正常 fast-forward / merge，不 force-push；
- 提交前检查差异与文件清单，推送后核对远端 HEAD。

## 3. Authority 原则

项目自己的 `AGENTS.md` 决定该项目内 Canon / Evidence / Decision / Current Status 的所有权。

一般规则：

```text
Owner 当前明确指令
> 项目 current / Owner-approved Canon / decisions
> 可验证的结构化事实与世界数据证据
> architecture contracts
> research evidence
> discussion / archive
> Agent 推测
```

研究结果不能因为被写入 GitHub 就自动升级成 Canon。

## 4. 不做隐式世界写入

任何会修改 Minecraft 世界的任务，必须有当前任务的明确 world-write 授权和边界。

只读调查、文档整理、数据分析不得为了方便而顺带写世界。
