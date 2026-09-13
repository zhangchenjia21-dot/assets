# MP-P03｜北岩台集散候选

`minecraft-planner v0.3` · `SETTLEMENT` · r1

状态：**HANDOFF_READY（条件性规划交接） / 待 GPT + Owner 审核**。

推荐阅读：

1. [完整聚落规划](聚落规划.md)
2. [内部结构与地表](maps/01-内部结构与地表.png)、[同坐标地形图](maps/02-内部结构与地形.png)、[通行剖面](maps/03-主要通行地形剖面.png)
3. [规划数据](planning-data.json)与[三个DISTRICT交接包](implementation-packages.json)
4. [Critic/Gate和修订](Critic与Gate.md)、[Completion Report](Completion%20Report.md)

地图深灰为聚合前沿带，不是单栋footprint；米黄为通行和共有院；虚线为街区关系范围；紫色为逐柱观察到的地面下16格内空气投影。地图不能直接施工。完整常住分支仍待供水、日需与土地使用证据闭合。

## 证据与复现

- sources/skill：实际读取的当前v0.3及8个references；来源commit记录于skill-revision.txt和source-register.json。
- sources/parent-package.json：唯一父包及其必要节点、流引用，不读取独立审核。
- evidence/world-read-provenance.json：源世界身份、读取时间、触及文件前后SHA、只读接口与本地缓存指纹。
- evidence：表面统计、地形/地表观察图、浅层样柱及逐柱空隙见证、路/前沿/空隙叠置；不上传原始存档或完整92,160列缓存。
- 两个region与level.dat副本及原始查询结果仅位于本地 `D:/Games/Minecraft/AI工程/MP-P03-cache/`。
- 原始读取用项目既有L3 RegionReader，不启动Minecraft。不要改为会加载/保存区块的run-job。

在当前工程布局下，复现顺序：`node 现状只读调查.mjs` → Python `场地证据分析.py` → `node 浅层空隙复核.mjs` → Python `聚落规划生成.py` → Python `局部证据复核.py` → Python `归档验证.py`。Python需NumPy/Pillow和微软雅黑，Node使用现有工程接口。重读源世界要求客户端退出；若原文件指纹改变，这是新快照，不能冒充本轮源数据。

本轮写入范围只有MP-P03目录与独立缓存。`world writes = 0`；没有修改Canon、Skill、存档、已有规划，也没有执行下一层任务。几何/哈希检查不负责判定规划质量或回归PASS/FAIL。
