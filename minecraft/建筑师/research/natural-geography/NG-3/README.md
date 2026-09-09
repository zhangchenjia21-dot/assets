# NG-3｜Consolidated Natural Atlas

**PASS-CANDIDATE / READY FOR INDEPENDENT REVIEW**。全部对象为 `PROPOSED`，不是已晋升的 Current Atlas authority。

主成果是 [atlas.sqlite](raw-or-queryable/atlas.sqlite)，schema `natural-atlas/1.0`。形成 **35 NGEO、20 NHYD、4 NFEAT、8 NSITE**：18 SUPPORTED、49 PROVISIONAL；65 个对象仍需进一步 refinement。0 个 UNRESOLVED 对象不代表没有未知：248 个小陆地 cells、676 个小水域 cells 保留为未归并斑块，另有全局水体拓扑及区域边界不确定性。

## 自然骨架与证据边界

东西两侧高山体（NGEO-034 / 035）、两侧山前高地（027 / 029），以及中部至北部低地镶嵌体（001）构成宏观骨架。001 不是整块平地，也不证明全域可通行。南部已核实岛体为 NGEO-009；其真实水陆掩膜与其他 64-block 近似区域明确分开。机器描述标签不是世界内地名。

数值候选使用高程、320-block 邻域平均/起伏、水体阻隔与四邻接，随后由模型结合高度图、候选图、NG-2 校准作显式解释，保存于 [semantic-decisions.json](atlas/semantic-decisions.json)。没有按 V1 `terrain` 字符串直接合并，也没有为凑数量跨水体拼接。高地阈值、平滑及小分量归并仍产生近似边界；SUPPORTED 山体身份不等于精确边界。

NG-2 八个局部结果进入 [calibration](calibration/detector-rules.json)，不能外推为全局准确率。SITE-005 保留山前缓坡解释，不建立粗阈值谷地；SITE-019 对应 NHYD-015 的真实分支水道与展宽段，不建立封闭湖。SITE-002 只形成局部浅鞍部点；SITE-011 是多出口海湾观察点，不推断天然港、唯一湾口或可航行性。

17 个粗水域对象仍为 PROVISIONAL；NHYD-015、019、020 使用 NG-2 已核实的局部真实水面分量。`connected_to` 在 schema 中受支持，但本轮没有全局真实水体连接边；粗邻接、局部重叠不能证明整个水域连通。全部 `flow_direction=unknown`，没有流域、上下游或流量推断。局部 ROI 边缘仍截断水域。

新增 targeted refinement **0 / 12**：已有证据足以建立带未知的宏观骨架，本轮不需要把未知湖体/水系强行晋升；理由见 [decision.json](targeted-refinement/decision.json)。没有复制 NG-2 的 500 万根原始柱。

## 使用入口

在 NG-3 目录运行，查询仅需 Python 3 标准库，无服务、无需世界存档：

```powershell
python tooling/Bootstrap/图册命令.py coordinate --x 1096 --z -1208
python tooling/Bootstrap/图册命令.py object --id NGEO-034
python tooling/Bootstrap/图册命令.py neighbors --id NGEO-009
python tooling/Bootstrap/图册命令.py search --family NHYD --evidence-status SUPPORTED
python tooling/Bootstrap/图册命令.py context --x -248 --z 2056 --radius 400
```

输出为带 schema version 的确定性 JSON，中文使用 JSON Unicode 转义。`snapshot.checked_at` 是离线 freshness 检查时间，查询本身不检查实时世界。完整使用与复现见 [查询与更新契约](tooling/查询与更新契约.md)。

世界范围 X=-6224～3807，Z=-6544～3487。粗 cell 索引边缘超出这个范围，实际几何已裁剪。点查询按 RLE 成员判断，不能把 bbox 或涉及的 cell 当作完整 footprint；context 按真实索引成员的最小距离筛选。NSITE 仅是下一次观察入口，全部仍需局部观察与独立 world-write 授权。

## 审核与后续依赖

五张主要派生地图位于 [visual](visual/)，数值候选审阅图另外保留；图像不是事实源，颜色不代表精度。681 项自动断言、完整重建字节一致性与存档/证据封口复核见 [validation](validation/)。直接 SQLite 约 5.7 MB，SHA256 见 [store.json](manifest/store.json)，无压缩归档无需 round-trip。

初始 freshness 为 `CURRENT_MATCH`：552 个 Overworld region 与 V1、NG-2 SHA256 一致；最终复核见 [final-source-audit.json](validation/final-source-audit.json)。V1 / NG-2 包括本地忽略文件的完整指纹保持不变，world writes = 0。没有启动游戏或执行器。

未来可将本 Proposed Atlas 用于定位宏观自然背景和选择继续调查的位置；不可依赖粗区域边界确定施工范围、把粗水域图当作通航网络、或从 biome 推导人文分布。最大未知是局部验证范围之外的真实水体连通、宏观分界的精确位置和零散未归并斑块。下一步仅为 GPT 独立审核；任何后续研究、World Canon、Architecture Bible 或建筑规划都不由本成果授权。
