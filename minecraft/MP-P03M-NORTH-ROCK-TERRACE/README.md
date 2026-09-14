# MP-P03M｜北岩台长期聚落专项复核

`minecraft-planner v0.4` · `SETTLEMENT` · `HANDOFF_READY` · 等待 GPT + Owner 审核。

结论：有条件的长期交割、修理、共储聚落仍合理；全年供水、有效驮运和供给/权利尚未证实。保留父包12–24户 / 3,500–8,000格²条件区间，首段12–16户 / 3,500–5,000格²须先满足启动条件。没有自行判断回归结果。

- [Completion Report](Completion%20Report.md)：完整逻辑、主要约束、规模、成长与交接。
- [assessment-data.json](assessment-data.json)：机器可读判断、适应链、行动者、供给节奏、分支和DISTRICT交接。
- [Critic and Gates](Critic%20and%20Gates.md)：本轮自检与状态边界。
- [约束与分阶段空间](maps/约束与分阶段空间.png)、[剖面](maps/地形与浅层剖面.png)：实际XZ坐标底图。
- [来源](sources/input-register.json)、[校验](validation.json)、[文件哈希](manifest.json)。

地图复现：在安装NumPy、Pillow并具有`C:/Windows/Fonts/msyh.ttc`的Python环境运行 `python 证据与制图.py`。归档已含压缩逐列事实，重建不必读取存档或MP-P03旧规划。

原始事实恢复：用Python `gzip.decompress` 解压 `evidence/surface.json.gz`。解压SHA256应为 `d11f036d8baac7fabcfa7c4ed9ba804dd4862f55fc3d1ec2ce25cec68d6eb7f2`。这是一份调查数据，不是Minecraft存档。

`python 归档校验.py` 附加核对当前机器相关源文件哈希，需原项目仍在既定位置；只写本归档。若以后源文件变化，哈希断言失败应记录新证据，不能覆盖原结论或伪造一致。

`world writes = 0`。本归档不会自动升级为Canon，也不授权Builder施工。
