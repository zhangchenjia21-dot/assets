# 自然地理初步探查 V1

状态：PARTIAL；world writes = 0（全存档前后 SHA256/大小/修改时间与文件清单一致）。

存档：`D:\Games\Minecraft\.minecraft\versions\26.2-Fabric 0.19.5\saves\建筑师`。Minecraft 26.2，DataVersion 4903。

完整生成方块范围：[-6224, -6544, 3807, 3487]；完整生成分量：[{'chunks': 393129, 'chunk_bounds': [-389, -409, 237, 217]}]；区块状态统计：{'minecraft:biomes': 2528, 'minecraft:carvers': 2520, 'minecraft:full': 393129, 'minecraft:initialize_light': 2512, 'minecraft:structure_starts': 20512}。Header 范围 [-6400, -6720, 3983, 3663] 不等于完成地形范围。

已采样 24964 个区块、124820 根柱，64 格网格；每个单元采样区块内五柱。

对象数量：{'GEO': 1264, 'HYD': 412, 'FEAT': 1343, 'SITE': 20}。GEO 是连通地形单元，不是命名山脉或行政区；小型碎片也保留。

## 地形统计（采样单元）

- water: 8711 单元，平均高度 62.3

- mountains_candidate: 6506 单元，平均高度 337.3

- plains_candidate: 4445 单元，平均高度 67.7

- hills_candidate: 3650 单元，平均高度 78.0

- valley_candidate: 847 单元，平均高度 80.7

- highlands_candidate: 711 单元，平均高度 149.5

- plateau_candidate: 88 单元，平均高度 230.8

- wetlands_candidate: 6 单元，平均高度 86.4

## 大尺度骨架

- GEO-534：mountains_candidate，范围 {'min_x': 896, 'max_x': 3839, 'min_z': -5056, 'max_z': 2431}，估计覆盖 12.44 百万方块平方，样本平均高度 344.4。

- GEO-535：mountains_candidate，范围 {'min_x': -6272, 'max_x': -3329, 'min_z': -5952, 'max_z': 1535}，估计覆盖 10.51 百万方块平方，样本平均高度 374.6。

- HYD-001：ocean_connected_water_candidate，范围 {'min_x': -6272, 'max_x': 3839, 'min_z': -6592, 'max_z': 3519}，估计覆盖 30.61 百万方块平方，样本平均高度 62.1。

## 下一步代表性观察地点

- SITE-017 / GEO-534：mountains_candidate，X=2760，Y≈329，Z=-1848，置信度 0.45。

- SITE-015 / GEO-566：plains_candidate，X=-824，Y≈63，Z=-3384，置信度 0.45。

- SITE-005 / FEAT-001：broad_valley_candidate，X=-3000，Y≈101，Z=-5496，置信度 0.45。

- SITE-001 / FEAT-656：mountain_pass_candidate，X=-6072，Y≈645，Z=-4024，置信度 0.35。

- SITE-003 / FEAT-618：island_candidate，X=-248，Y≈72，Z=2056，置信度 0.45。

- SITE-011 / HYD-142：coastal_bay_candidate，X=-312，Y≈62，Z=-4024，置信度 0.25。

- SITE-021 / GEO-728：plateau_candidate，X=2440，Y≈276，Z=-6456，置信度 0.45。

- SITE-019 / HYD-003：inland_water_body_candidate，X=1096，Y≈62，Z=-1208，置信度 0.45。

## 已知限制

- 64 格网格仅在每个单元的一个区块采五柱；跨格水体连通与狭窄地形可能漏检，面积为外推估计。

- GEO 是阈值分类的连通分区，存在碎片与类别交错，不等同于语义完整的山脉或流域。

- surface_y 包括树冠；exposed_y 只剥离显式植被，不能可靠消除所有植物、人工建筑、冰面或悬空地形。

- 河流、岛屿、半岛、谷地、山口等均是待复核候选；未证明真实河道连续性和流向。

- 汇流点、天然港口、瀑布、流域和高差水流转换没有可靠证据，保持 uncertain；海洋命名结合水方块与 biome，不依据 biome 独立判定。

- 边界触及对象是截断观测，不能判断世界外侧连通；全区块状态已审计，详细地形只解码采样区块。

- 未进行游戏内现场视觉复核：正式执行器会保存世界，退役 Observation/Bridge 不恢复；地图仅为离线派生证据。

- 对象 confidence 是启发式可信度标记，未经统计校准；局部规则阈值需在后续精查验证。

下一阶段建议：先针对山地、谷地、平原和水岸候选做 4–8 格局部只读精查，并在安全观察环境中复核；本轮停止，不进入文明设定或建筑规划。

工具分层：L0 编码契约；L1 文件读取/存储/推导/地图；L2 调查流程；L3 命令公开边界。无跨模块内部调用。