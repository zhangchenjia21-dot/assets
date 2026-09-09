# WB-002R-R1｜Southern Island Group Scope Completion

**IMPLEMENTATION COMPLETED / AWAITING INDEPENDENT REVIEW**。这不是 Stage PASS 或后续人文/建筑授权。

东侧主陆体已闭合：`CLOSED_WITHIN_STUDY`，`scope_complete=true`，`east_mountain_landmass_touches_study_boundary=false`。研究矩形 X=-800..2463、Z=1376..3487，真实水平1格覆盖 6,893,568 柱。完整东岛面积1,674,373 blocks²，bounds [-349,1453,2091,3214]；西岛面积575,363，两者表层不连通。

旧西部6,080区块与 WB-002R current epoch 的12个region哈希匹配，直接复用；增量读取20,848区块。完整研究有26,928区块和430,848个四格植被样点。全域统计含所有小岛礁，未将主岛外成员静默排除。`world writes = 0`；前序 V1 / NG-2 / NG-3 / WB-002R 不变。

主要结果：完整干陆中位Y128、最高Y300，平地21.70%；西岛平地67.65%，东岛5.99%。全域西低东高 Pearson r约0.643。自然区保留两个边界明确的研究参考单元和内部连续梯度；比较k2～5，但不确认恰好三区。

全范围 H-01～H-05 依次为 **PARTIALLY_SUPPORTED / SUPPORTED / SUPPORTED / PARTIALLY_SUPPORTED / INSUFFICIENT**。旧局部 verdict 原样保留，不能与全范围判断互换。

## 阅读和查询

- [完整区域画像](reports/南部岛屿群完整区域画像.md)
- [范围修正与复用说明](reports/WB-002R范围修正说明.md)
- `profile/scope-completion.json`：闭合硬门、范围与source region哈希。
- `profile/regional-summary.json`：全干陆、西岛、东岛对照。
- `profile/owner-hypothesis-evaluation.json`：前序局部和本轮全域 verdict。
- `validation/`：原始柱、独立拓扑、查询、重建和源封口。

主查询层为 `raw-or-queryable/regional-profile.sqlite`。Git 中存储无损gzip；先在本目录恢复：

```powershell
python tooling/Bootstrap/归档命令.py restore
python -S tooling/Bootstrap/查询命令.py coordinate --x 1500 --z 2300
python -S tooling/Bootstrap/查询命令.py coordinate --x -248 --z 2056
python -S tooling/Bootstrap/查询命令.py zone --id SIRZ-R1-002
python -S tooling/Bootstrap/查询命令.py low-relief --x 400 --z 1800 --radius 64
python -S tooling/Bootstrap/查询命令.py context --x 400 --z 1800 --radius 64
python -S tooling/Bootstrap/查询命令.py hypotheses
```

只用Python标准库即可查询。coordinate 返回真实柱、材料、两种biome、地形、zone、source chunk/region和邻近patch；near按实际RLE成员距离，不以bounds代替。范围外明确返回OUTSIDE_STUDY_AREA，未知ID和负radius报错。`profiles`表保存全部JSON，`objects`与`geometry_runs`保存实际成员；satellite组件没有主岛SIRZ归属，但仍可查询。

## 复现

Python3.12、numpy2.3.5、Pillow12.3.0、nbtlib2.0.4；地图使用Windows Arial。源文件保护依赖Windows只读共享句柄。Bootstrap中的nbtlib路径指向本机已有第三方依赖，可按环境显式调整；不得为此改世界或安装游戏组件。

本目录使用`.gitattributes`关闭Git自动换行转换，保留已核验文件的原始字节。重建字节一致性针对上述Windows环境；不能让检出时的换行改写破坏保存的证据哈希。

```powershell
python tooling/Bootstrap/画像命令.py
python tooling/Bootstrap/假说导出命令.py
python tooling/Bootstrap/汇编命令.py
python tooling/Bootstrap/地图命令.py
python tooling/测试/完整查询验证.py
python tooling/测试/区域拓扑独立验证.py
python tooling/测试/完整重建验证.py
python tooling/Bootstrap/归档命令.py archive
```

固定observed重建不依赖原世界，执行时间不进入核心profile事实文件。假说导出脚本只是装配模型已明确选定的解释和事实，不能自动裁定自然区语义。模型决定保存在`profile/zoning-decision.json`，改变它就是新的解释revision。

原世界重取不是日常复现步骤。`范围命令.py <world>`只允许新建基线，拒绝覆盖已有初始指纹；以旧observed库的稳定ID为起点，按哈希决定复用/refresh。`余带命令.py <world>`补齐可读取子矩形，使用本次已验证的full-chunk南界Z3487；该值是此次快照的约束，不能当未来世界的永久边界。边界探测失败与续读见范围修正说明。不要删除现有基线来重复运行。`封口命令.py <world>`核对从开始至最终的完整源指纹。

工具是前序公开成果的本轮独立版本；不修改或import历史模块内层。L0保留材料/字段契约，L1解码/保护/计算/查询/地图，L2增量读取与派生汇编，L3公开入口；Bootstrap与测试为外围。未上传完整存档、备份、凭据或Mods。

地图是等比例派生缩略图；biome原生4×4×4采样、水区间、过滤器、窗口边缘未知等限制见报告。所有成果停留在Research，不创建文明、种族、部族、国家或政治边界，不进入Architecture/Build。
