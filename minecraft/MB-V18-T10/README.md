# MB-V18-T10

阅读 [Completion Report](Completion%20Report.md) 和 [前后同机位证据](证据索引.html)。本包为精修隔离的 Builder 自证，不是独立回归结论。

`上游/` 只保留获准读取的 T09 自产 Intent 和 Completion Report。`研究/技能原文-SKILL.md` 是本轮实际读取、按 Git blob 校验的 v1.8 原文。

`蓝图与实存数据.zip` 无损压缩各阶段 Canonical Blueprint、设计数组和实存 u16。解压到本目录即可恢复相对路径；归档文件 SHA256 见 `SHA256SUMS.txt`，ZIP 已执行 CRC 检查。未上传完整存档、临时资格副本、备份、模组或配置正文。

Python + NumPy + Pillow 可运行：

```text
python 空间核验.py 05-Restraint
python 阶段保护核验.py 05-Restraint
python 审计视图.py 05-Restraint
```

渲染字体依赖 Windows `msyh.ttc`。实存数组为小端 u16、YZX 顺序 `[56,144,144]`，世界原点 `[0,10,0]`，调色板在各阶段 `实存.json`。基准为 `00-Baseline`，最终为 `05-Restraint`，`reload` 为零施工重载。原生方块状态属性顺序不影响比较。

施工脚本依赖原工作区 AI-Offline 公共接口及已验证 runtime，不是通用导入工具。`准备隔离世界.mjs` 仅用于不存在目标时的新建副本；`验证隔离副本.mjs` 是本轮中断后核对副本并完成配置资格的续作入口。不得在已有成果上重复初始化，也不得手工伪造 runtime 登记。只读审计无需运行这两个脚本。

当前可游览存档位于原工作区的 `MB-V18-T10/实例/saves/MB-V18-T10-罗马浴场精修`，并不自动加入正式客户端 saves 列表。没有改动正式客户端或 `建筑师`。

初次 factory runtime 资格尝试失败，使用正确完整客户端配置后成功；细节见 Gate 与 Completion Report。工具工程记录中的 PASS 仅是执行器的保存/读回状态，不是 T10 回归判定。
