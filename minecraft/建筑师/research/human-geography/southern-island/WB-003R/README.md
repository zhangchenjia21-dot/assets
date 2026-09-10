# WB-003R｜Economic & Accessibility Substrate Reconnaissance

**IMPLEMENTATION COMPLETED / AWAITING INDEPENDENT REVIEW**。研究结论未升格为 Canon；world writes = 0。

这是 WB-002R-R1 缓存的有限补充，不是新一轮区域扫描。入口见 [review/index.json](review/index.json)，结论见 [经济与通达性前置画像](reports/经济与通达性前置画像.md)。阅读顺序：source-fingerprint → sampling-design → profiles → geometry-sampling / rebuild / source-audit → hypotheses。X-02 的离散抽样误判完整保留，精确几何检查与拒绝状态优先。

## 口径

- 范围沿用 R1：X=-800..2463、Z=1376..3487。逐柱地表、植被抽样、地形、水陆拓扑全部复用，未重新读取全域 NBT。
- W=西岛全部干陆；M=东岛且 X<640、exposed_y≤120；E=东岛且 X≥640、exposed_y≥140。它们是三类可复现研究样区，**不是已确定的人文边界**。547,618 个陆柱为未分配过渡地带、海岸或卫星陆块，占全部陆柱约24.26%，没有被当成海水；不能把本表当作三域完整领土统计。
- 土壤名集合见 L0 契约。低平土壤 proxy 为该集合与 R1 FLAT/GENTLE 的交集，未将苔藓、packed_mud、dirt_path 自动视作耕地。FLAT: relief32≤4、slope8≤0.125、step1≤1；GENTLE: 非FLAT且relief32≤8、slope8≤0.25、step1≤2。biome沿用R1原始表层查询；其原生分辨率为4×4×4，并非1格生物群系观测。
- 内水为 R1 已封闭的表层水体；Manhattan距离可穿越任何栅格，仅是几何接近程度。没有验证水质、补给、灌溉。
- 植被是 R1 每4格的柱样本；有≥75%柱属于某样区的chunk才分配其命名植被计数。混合chunk另计。不能换算森林面积、树数或木材产能。材料表保留所有实测名称，包括waystone等；不能宣称所有记录均为自然原生材料。
- 新采样固定seed=3003，X/Z模64等于32的格点；各样区按高程排序分3层，每层16柱，共144柱，Y=-60至该柱R1 exposed_y，25,176个方块位置。每区48柱；W/M/E面积不同，故横向密度不同（每万陆柱约0.834/1.915/0.544根）。不是区域无偏储量估计。只分类8类常见ore，其他名称仍保留于本地trace/近表层palette；非穷尽所有模组矿物。
- 矿物按共同绝对Y带分母比较。深部出现不等于可开采；未见只表示样本范围未见。近表层=各样本最上16个位置，包含空气、流体与植被，不等于16格实心岩层。
- 跨岛间距为真实岸柱单位方格的欧氏边到边距离，另存中心距；精确闭方格相交检查覆盖整段（触角也保守纳入）。X-02不满足清晰直线水面条件。低坡岸要求8格向陆直线逐步≤1且relief16≤8；endpoint另列16格延伸诊断，后8格可能更陡。
- 东岛1格、四邻接干陆Dijkstra；水为障碍，slope8、relief32、step1和实际边高差计入成本。详细公式与完整基线/敏感性折线见movement-corridors。坡坎权重4/16是研究参数，不是实测运输耗时。端点取研究掩膜质心附近实柱，不是聚落选址。当前六条折线单步≤1仍未检查人物净空、碰撞、危险方块、牲畜/车辆通过性。

## 本地缓存与复现

完整新trace与冻结源清单在 `D:/Games/Minecraft/AI工程/研究缓存/建筑师/WB-003R`，不在Git。SHA256、大小、epoch、保留策略在 [raw-cache.json](manifest/raw-cache.json)。复用R1的observed.sqlite、regional-profile.sqlite、derived.npz，不复制它们。缓存缺失必须报 `MISSING_LOCAL_CACHE`，不能假装轻量包包含完整raw。

Python3.12、NumPy2.3.5、Pillow12.3.0、nbtlib（仅重新定点读世界需要）。从本目录执行：

```powershell
python tooling/Bootstrap/基底命令.py derive
python tooling/tests/证据核验.py
python tooling/tests/汇总核验.py
python tooling/Bootstrap/基底命令.py seal
```

derive只读缓存并重建六个事实profile和地图，不修改人工解释。`seal`需原本地source-before.json及当前世界，比较全文件名/hash/size/mtime；它不能替代历史执行记录。使用默认机器之外的路径时指定 `--cache` / `--world`；R1缓存应置于相邻R1标准路径，原始SQLite可按R1恢复说明由其历史归档恢复并核对hash。

只有缓存确实缺失且世界仍匹配同一epoch，才能在**新的空缓存目录**依次 `init --cache <新目录>`、`sample --cache <新目录>`；不得覆盖原缓存。它会重新读取同样144柱，非全域扫描；世界已变则停止，不将新源冒充旧证据。manifest指向的旧raw应长期保留。

精确查询：本地 `mineral-columns.json` 按id或x/z查柱，`blocks[y+60]`即方块名。地表/地形任意柱继续使用R1的只读SQLite查询入口。GitHub可直接查询profile中的样区统计、sample-id阳性见证、跨岛端点和corridor折线；无需下载全量世界。

## 交付边界

源epoch与全部前序immutable目录在任务开始和结束均核对；完整世界清单只留本地。tooling遵循L3→L2→L1→L0；Bootstrap与tests在层外，没有跨模块内部代码依赖。地理缓存属于显式数据契约。地图只是阅读视图，坐标与事实以JSON为准；Owner“中心岛”仍为 **OWNER_REFERENT / COORDINATE_TBD**。
