# Natural Geography Survey V1｜归档入口

状态：**ACCEPTED BASELINE / SURVEY ARTIFACT PARTIAL**

原始 Codex 提交：`dcd208cbd2fe6a120369a5df11edf0431066be55`（2026-09-09，`归档建筑师自然地理调查 V1 及验证证据`）。

## 内容

- `survey/`：原 `World-Survey/建筑师/` 整体调查成果，使用原 tree / blob 内容迁移，保留原始字节与验证材料；
- `packaging/`：第一次 push 时位于仓库根的归档脚本、requirements 与发布归档记录；
- `独立审核.md`：GPT 对 V1 任务的独立审核结论。

## Relocation note

第一次 Codex push 时，成果位于仓库根 `World-Survey/建筑师/`，并把 `Bootstrap/`、`requirements.txt`、`发布归档.json` 放在根目录。

2026-09-09 按 Owner 指令统一归入：

`minecraft/建筑师/research/natural-geography/V1/`

`packaging/发布归档.json` 是**第一次发布时的原始证据**，其中记录的 `World-Survey/建筑师/...` 路径仍指向旧布局；不要为了让路径“好看”而改写该历史证据。数据库与调查文件的 blob 内容 / SHA 证据保持不变。

当前项目导航和未来任务必须使用新路径。
