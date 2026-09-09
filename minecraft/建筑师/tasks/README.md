# Tasks｜建筑师

本目录保存已经获得 Owner 授权、可直接交给 Codex 执行的任务包。

规则：

- `current/项目状态.md` 决定当前哪一个任务处于 ACTIVE / AUTHORIZED；
- `TASK.md` 只冻结本轮执行范围、交付物、验收与禁止事项，不复制整个项目背景；
- Codex 完成后在对应任务目录补 `COMPLETION.md`，并把实际成果归入 `research/`、`world/`、`builds/` 等 canonical 目录；
- Task Packet 不是 World Canon，也不能自行修改长期项目原则；
- 完成任务默认 commit + push 到 `zhangchenjia21-dot/assets/main`，随后由 GPT 独立审核。

## 大型扫描 Task 额外要求

凡预计产生百万级 columns、完整 SQLite、dense NPZ、大规模 geometry / cross-check 等高体积机器证据，Task Packet 必须遵守：

- `../decisions/D-010_大型扫描证据GitHub轻量化.md`
- `../architecture/大型扫描数据交付与审核契约.md`

默认使用：

```text
Local Raw Cache
→ Lightweight Review Bundle
→ GitHub
```

Task 必须明确：local raw cache、GitHub review bundle、source fingerprint、raw-cache manifest、predecessor reuse / delta、size budget 与 cold-archive 条件。

单次 GitHub delivery 默认目标 `<=15 MiB`；超过 25 MiB 必须在 Task 中获得明确例外授权，不能只因压缩后可 push 就自动提交完整 raw database。
