# MB-V11-T02 山地修道院

入口文档：[Completion Report](Completion%20Report.md)。本归档保留独立 T02 的原创蓝图、分阶段施工文件、研究来源、实存空间审计与候选资产。不包含完整游戏存档或备份，不给出回归 PASS / FAIL 判断。

## 证据恢复

`证据/阶段N-实存.bin.gz` 是本项目范围内的只读体素导出，不是 Minecraft region 文件。用标准 gzip 解压得到 `.bin`；对应 JSON 保存 SHA256、尺寸、Y 原点和完整方块状态表。

体素布局是 uint8、X→Y→Z（Z 最快），尺寸 `[240,104,220]`，坐标起点 `[0,63,0]`；索引 `(x*104+(y-63))*220+z`。对解压字节计算 SHA256，须与 JSON 中值相同。

在 Windows 安装 NumPy、Pillow、Node 后，可在保留本目录结构且解压数据的副本中运行 `python 空间审计.py 5` 重建最终透视、平面和剖面。该脚本只读取导出文件，不访问游戏存档。字体使用 Windows 微软雅黑。

## 蓝图与施工复现

`蓝图/` 每个 `.json.gz` 解压后是 schema_version=1 Canonical Blueprint，含绝对 origin、局部坐标、完整 palette。按 01—05 顺序应用。每个文件均通过现有蓝图公开接口核验；施工压缩操作与对应蓝图逐格一致。

施工脚本依赖原工作区 `AI-Offline`、`AI-Preview`、`AI-Blueprints` 的正式 L3 接口及已验证 Fabric 26.2 运行时，不能将本归档当作独立 Minecraft 执行器。原工作目录是 `D:/Games/Minecraft/AI工程/MB-V11-T02`。

原执行顺序：`生成修道院.py` → `执行与读回.mjs run 1/read 1` → `run 2/read 2` → `run 3/read 3` → `局部修订.py` → `run 4/read 4` → `基础修订.py` → `run 5/read 5` → `空间审计.py 5` → `最终核验.py`。Node 命令分别执行，`run/read` 表示两次调用。

脚本只允许名字和路径完全相符的测试世界；第一阶段拒绝覆盖已存在目录。复现需要经过明确授权的新目标或隔离环境，不能直接在已完成世界上重新执行第一阶段，也不能将目标改为真实存档。

`SHA256SUMS.txt` 列出归档文件哈希。本目录 Git 属性禁止隐式换行转换，避免破坏哈希；自产文本归档为 LF，外部来源快照按原文保留，不做空白清理。`候选/` 仅是本任务候选，不构成正式资产库登记。
