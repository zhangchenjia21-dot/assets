# MB-V110-T12

先读 [Completion Report](Completion%20Report.md)，再打开 [同机位物理审计](同机位物理审计.html)。GitHub 不直接显示 HTML，可下载本目录后本地打开。物理 Gate 为 UNVERIFIED，不是 PASS；不包含本轮回归最终判断。

`修复蓝图与实存.zip` 解压至本目录可恢复各阶段实存 u16、Repair npz 和差量 Canonical Blueprint；ZIP CRC 及逐文件内容已验证。实存为 little-endian uint16，YZX=(36,96,56)，世界原点=(0,10,0)，配套调色板在同名 `*-实存.json`。归档 SHA256 见 SHA256.json。

只读复核依赖 Python/NumPy/Pillow：`物理完整性扫描.py reload`、`关联完整性核验.py reload`。后者检查实际差量是否严格符合账本和原生静态接触。`物理剖面证据.py 01-Repair`、`审计视图.py 01-Repair` 可重绘证据；默认使用 Windows 微软雅黑字体。

原生碰撞形状.java 是本轮的无世界读取器，编译/运行依赖既有 Minecraft 26.2 原生 classpath；不是安装 Mod。归档保留查询结果，可不重跑 Java 直接复核。形状默认上下文不能替代客户端输入、姿态、物理 tick 和真实碰撞。

世界作业依赖本机 AI-Offline L3 接口、已验证运行环境与硬编码 T12 路径，不可直接迁移去正式存档。建立副本.mjs/继续资格验证.mjs 保留首次尝试记录：Node 配置复制中途退出，最小配置资格验证又因缺数据包被拒绝；实际成功流程使用 PowerShell 完整复制 T11 来源实例 Mods/config 后，公开 qualifyExistingWorld 两次加载验证通过。不要盲目重新运行创建脚本；新副本来源与状态必须重新核对。

源存档完整逐文件哈希索引只留本机（含玩家文件名，不公开上传）；公开交付核验保留数量、索引摘要与全部文件不变结论。完整存档、备份、资格验证副本、运行时 Mods/config、玩家文件和编译缓存不归档。交付核验.py 的源世界检查依赖本机私有哈希索引；归档读者可以运行上述几何复核，但不能据此声称独立验证了不存在于归档内的整个世界。
