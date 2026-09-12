# STYLE_GRAMMARS — 风格语法

> 生成：`scripts/build_grammar.py`。样本纪律：n≥8 SUPPORTED（可 STRONG）、4–7 PROVISIONAL（最高 SOFT）、<4 OBSERVATION ONLY（不出规则）。Style 维度无 HARD（HARD=功能必需，见任务书第 20 节）。Other 为异质集合不出规则；Unknown（56 张）不是类别。
> basis：OBSERVED=元数据/审核分类直接统计；HEURISTIC=明确算法近似（算法与盲区见文末附录）。


## Medieval（sample_n=19，SUPPORTED）

| 维度 | 规则 | 类型 | basis | 统计 | 置信 |
|---|---|---|---|---|---|
| footprint_ratio | Medieval 平面长宽比 = max(x,z)/min(x,z)，1.0=方形 | STRONG | OBSERVED | n=19 median=1.0909 IQR[1.0461,1.2288] | high |
| height_ratio | Medieval 高宽比 = size_y/max(size_x,size_z) | SOFT | OBSERVED | n=19 median=0.8293 IQR[0.5921,1.254] | high |
| floor_count | Medieval 楼层数（楼板密度启发式） | STRONG | HEURISTIC | n=15 median=1.0 IQR[1.0,1.5] | medium |
| roof_height_ratio | Medieval 屋顶高度占比 = 上部 stair+slab 最长连续带高 / size_y | SOFT | HEURISTIC | n=19 median=0.0612 IQR[0.029,0.0996] | medium |
| roof_material_share_top3 | Medieval 顶部 1/3 区域 stair+slab 材料占比（屋顶材料信号） | SOFT | HEURISTIC | n=19 median=0.2794 IQR[0.1173,0.4824] | medium |
| roof_overhang | Medieval 屋顶出檐：顶部1/3 脚印超出中部1/3 >5% 的样本频率 | OPTIONAL | HEURISTIC | freq=0.3684 | medium |
| roof_overhang_ratio | Medieval 出檐比例分布 | SOFT | HEURISTIC | n=19 median=0.0177 IQR[0.0013,0.0669] | medium |
| vertical_rhythm | Medieval 竖向节奏 = 5 等分质量分布归一化熵（1=均匀，低=质量集中） | STRONG | OBSERVED | n=19 median=0.7779 IQR[0.5568,0.8448] | high |
| symmetry | Medieval 对称性 = max(symmetry_x, symmetry_z) | SOFT | OBSERVED | n=19 median=0.7115 IQR[0.4854,0.9186] | high |
| symmetry_high | Medieval 高对称（≥0.9）样本频率 | OPTIONAL | OBSERVED | freq=0.3158 | high |
| window_density | Medieval 窗密度 = 玻璃体素数/暴露面估计（窗面积代理） | SOFT | HEURISTIC | n=19 median=0.0031 IQR[0.0004,0.0161] | medium |
| palette_wood_ratio | Medieval wood 材料占比 | SOFT | OBSERVED | n=19 median=0.1647 IQR[0.1101,0.2328] | high |
| palette_stone_ratio | Medieval stone 材料占比 | STRONG | OBSERVED | n=19 median=0.5888 IQR[0.3893,0.6245] | high |
| palette_glass_ratio | Medieval glass 材料占比 | SOFT | OBSERVED | n=19 median=0.0029 IQR[0.0005,0.0282] | high |
| palette_decorative_ratio | Medieval decorative 材料占比 | SOFT | OBSERVED | n=19 median=0.03 IQR[0.0224,0.0734] | high |
| palette_top_blocks | Medieval 高频方块 Top（类内聚合） | SOFT | OBSERVED | tuff 37%, cobbled_deepslate 13%, cyan_terracotta 10%, smooth_basalt 5%, water 4% | high |
| material_transition | Medieval 底/中/顶主导材料族模式众数：stone→stone→stone | SOFT | HEURISTIC | freq=0.4211 | medium |
| wall_thickness | Medieval 墙厚估计 = 中部1/3 层水平扫描线实体段中位数 | SOFT | HEURISTIC | n=19 median=1.0 IQR[1.0,2.0] | medium |
| cantilever_frequency | Medieval 二层出挑（second_floor_overhang）频率 | OPTIONAL | OBSERVED | freq=0.1053 | high |
| chimney_frequency | Medieval 烟囱候选频率（高出柱顶 P90 的孤立细柱） | SOFT | HEURISTIC | freq=0.5789 | medium |
| foundation_stone_base | Medieval 石质基座（stone_base，底部20% 石≥55%）频率 | OPTIONAL | OBSERVED | freq=0.2105 | high |
| foundation_bottom_family | Medieval 底部 1/3 主导材料族众数：stone | STRONG | HEURISTIC | freq=0.8947 | medium |

## Rustic（sample_n=20，SUPPORTED）

| 维度 | 规则 | 类型 | basis | 统计 | 置信 |
|---|---|---|---|---|---|
| footprint_ratio | Rustic 平面长宽比 = max(x,z)/min(x,z)，1.0=方形 | STRONG | OBSERVED | n=20 median=1.1847 IQR[1.0964,1.3965] | high |
| height_ratio | Rustic 高宽比 = size_y/max(size_x,size_z) | STRONG | OBSERVED | n=20 median=0.8231 IQR[0.741,0.9641] | high |
| floor_count | Rustic 楼层数（楼板密度启发式） | STRONG | HEURISTIC | n=18 median=2.0 IQR[1.0,2.0] | medium |
| floor_height | Rustic 层高中位数（相邻楼面高差） | SOFT | HEURISTIC | n=12 median=6.0 IQR[4.875,9.5] | medium |
| roof_height_ratio | Rustic 屋顶高度占比 = 上部 stair+slab 最长连续带高 / size_y | SOFT | HEURISTIC | n=20 median=0.0751 IQR[0.0544,0.154] | medium |
| roof_material_share_top3 | Rustic 顶部 1/3 区域 stair+slab 材料占比（屋顶材料信号） | SOFT | HEURISTIC | n=20 median=0.306 IQR[0.163,0.4353] | medium |
| roof_overhang | Rustic 屋顶出檐：顶部1/3 脚印超出中部1/3 >5% 的样本频率 | OPTIONAL | HEURISTIC | freq=0.35 | medium |
| roof_overhang_ratio | Rustic 出檐比例分布 | SOFT | HEURISTIC | n=20 median=0.0166 IQR[0.0,0.0587] | medium |
| vertical_rhythm | Rustic 竖向节奏 = 5 等分质量分布归一化熵（1=均匀，低=质量集中） | STRONG | OBSERVED | n=20 median=0.8179 IQR[0.7597,0.8418] | high |
| symmetry | Rustic 对称性 = max(symmetry_x, symmetry_z) | SOFT | OBSERVED | n=20 median=0.4377 IQR[0.2947,0.5317] | high |
| symmetry_high | Rustic 高对称（≥0.9）样本频率 | OPTIONAL | OBSERVED | freq=0.0 | high |
| window_density | Rustic 窗密度 = 玻璃体素数/暴露面估计（窗面积代理） | SOFT | HEURISTIC | n=20 median=0.0031 IQR[0.0,0.015] | medium |
| palette_wood_ratio | Rustic wood 材料占比 | SOFT | OBSERVED | n=20 median=0.1949 IQR[0.1711,0.3007] | high |
| palette_stone_ratio | Rustic stone 材料占比 | STRONG | OBSERVED | n=20 median=0.3802 IQR[0.2825,0.4459] | high |
| palette_glass_ratio | Rustic glass 材料占比 | SOFT | OBSERVED | n=20 median=0.005 IQR[0.0,0.0264] | high |
| palette_decorative_ratio | Rustic decorative 材料占比 | SOFT | OBSERVED | n=20 median=0.0672 IQR[0.0302,0.1248] | high |
| palette_top_blocks | Rustic 高频方块 Top（类内聚合） | SOFT | OBSERVED | oak_leaves 3%, cyan_terracotta 2%, spruce_planks 2%, oak_log 2%, grass_block 2% | high |
| material_transition | Rustic 底/中/顶主导材料族模式众数：stone→functional→stone | OPTIONAL | HEURISTIC | freq=0.2 | medium |
| wall_thickness | Rustic 墙厚估计 = 中部1/3 层水平扫描线实体段中位数 | STRONG | HEURISTIC | n=20 median=2.0 IQR[1.75,2.0] | medium |
| cantilever_frequency | Rustic 二层出挑（second_floor_overhang）频率 | OPTIONAL | OBSERVED | freq=0.0 | high |
| chimney_frequency | Rustic 烟囱候选频率（高出柱顶 P90 的孤立细柱） | OPTIONAL | HEURISTIC | freq=0.25 | medium |
| foundation_stone_base | Rustic 石质基座（stone_base，底部20% 石≥55%）频率 | OPTIONAL | OBSERVED | freq=0.1 | high |
| foundation_bottom_family | Rustic 底部 1/3 主导材料族众数：stone | SOFT | HEURISTIC | freq=0.6 | medium |

## Fantasy（sample_n=10，SUPPORTED）

| 维度 | 规则 | 类型 | basis | 统计 | 置信 |
|---|---|---|---|---|---|
| footprint_ratio | Fantasy 平面长宽比 = max(x,z)/min(x,z)，1.0=方形 | STRONG | OBSERVED | n=10 median=1.1417 IQR[1.0045,1.5343] | high |
| height_ratio | Fantasy 高宽比 = size_y/max(size_x,size_z) | SOFT | OBSERVED | n=10 median=0.8185 IQR[0.7169,1.2293] | high |
| floor_count | Fantasy 楼层数（楼板密度启发式） | STRONG | HEURISTIC | n=8 median=1.0 IQR[1.0,1.25] | medium |
| roof_height_ratio | Fantasy 屋顶高度占比 = 上部 stair+slab 最长连续带高 / size_y | SOFT | HEURISTIC | n=10 median=0.0415 IQR[0.0091,0.0576] | medium |
| roof_material_share_top3 | Fantasy 顶部 1/3 区域 stair+slab 材料占比（屋顶材料信号） | SOFT | HEURISTIC | n=10 median=0.1015 IQR[0.0038,0.2644] | medium |
| roof_overhang | Fantasy 屋顶出檐：顶部1/3 脚印超出中部1/3 >5% 的样本频率 | SOFT | HEURISTIC | freq=0.6 | medium |
| roof_overhang_ratio | Fantasy 出檐比例分布 | SOFT | HEURISTIC | n=10 median=0.0864 IQR[0.0248,0.309] | medium |
| vertical_rhythm | Fantasy 竖向节奏 = 5 等分质量分布归一化熵（1=均匀，低=质量集中） | STRONG | OBSERVED | n=10 median=0.7419 IQR[0.6331,0.8789] | high |
| symmetry | Fantasy 对称性 = max(symmetry_x, symmetry_z) | SOFT | OBSERVED | n=10 median=0.6747 IQR[0.4081,0.8519] | high |
| symmetry_high | Fantasy 高对称（≥0.9）样本频率 | OPTIONAL | OBSERVED | freq=0.2 | high |
| window_density | Fantasy 窗密度 = 玻璃体素数/暴露面估计（窗面积代理） | SOFT | HEURISTIC | n=10 median=0.0022 IQR[0.0,0.0065] | medium |
| palette_wood_ratio | Fantasy wood 材料占比 | SOFT | OBSERVED | n=10 median=0.0553 IQR[0.0194,0.1755] | high |
| palette_stone_ratio | Fantasy stone 材料占比 | STRONG | OBSERVED | n=10 median=0.6981 IQR[0.4834,0.7554] | high |
| palette_glass_ratio | Fantasy glass 材料占比 | SOFT | OBSERVED | n=10 median=0.0043 IQR[0.0,0.0137] | high |
| palette_decorative_ratio | Fantasy decorative 材料占比 | SOFT | OBSERVED | n=10 median=0.1058 IQR[0.0495,0.1557] | high |
| palette_top_blocks | Fantasy 高频方块 Top（类内聚合） | SOFT | OBSERVED | stone 11%, brown_terracotta 9%, dirt 7%, grass_block 6%, gray_terracotta 5% | high |
| material_transition | Fantasy 底/中/顶主导材料族模式众数：stone→stone→stone | SOFT | HEURISTIC | freq=0.5 | medium |
| wall_thickness | Fantasy 墙厚估计 = 中部1/3 层水平扫描线实体段中位数 | SOFT | HEURISTIC | n=10 median=1.0 IQR[1.0,2.0] | medium |
| cantilever_frequency | Fantasy 二层出挑（second_floor_overhang）频率 | OPTIONAL | OBSERVED | freq=0.0 | high |
| chimney_frequency | Fantasy 烟囱候选频率（高出柱顶 P90 的孤立细柱） | OPTIONAL | HEURISTIC | freq=0.2 | medium |
| foundation_stone_base | Fantasy 石质基座（stone_base，底部20% 石≥55%）频率 | OPTIONAL | OBSERVED | freq=0.2 | high |
| foundation_bottom_family | Fantasy 底部 1/3 主导材料族众数：stone | SOFT | HEURISTIC | freq=0.7 | medium |

## Japanese（sample_n=7，PROVISIONAL）

| 维度 | 规则 | 类型 | basis | 统计 | 置信 |
|---|---|---|---|---|---|
| footprint_ratio | Japanese 平面长宽比 = max(x,z)/min(x,z)，1.0=方形 | SOFT | OBSERVED | n=7 median=1.2 IQR[1.0613,2.1043] | medium |
| height_ratio | Japanese 高宽比 = size_y/max(size_x,size_z) | SOFT | OBSERVED | n=7 median=0.75 IQR[0.5301,0.7952] | medium |
| floor_count | Japanese 楼层数（楼板密度启发式） | SOFT | HEURISTIC | n=6 median=2.5 IQR[1.25,3.0] | low |
| floor_height | Japanese 层高中位数（相邻楼面高差） | SOFT | HEURISTIC | n=4 median=8.0 IQR[4.25,12.25] | low |
| roof_height_ratio | Japanese 屋顶高度占比 = 上部 stair+slab 最长连续带高 / size_y | SOFT | HEURISTIC | n=7 median=0.1892 IQR[0.0892,0.2535] | low |
| roof_material_share_top3 | Japanese 顶部 1/3 区域 stair+slab 材料占比（屋顶材料信号） | SOFT | HEURISTIC | n=7 median=0.4073 IQR[0.3013,0.4264] | low |
| roof_overhang | Japanese 屋顶出檐：顶部1/3 脚印超出中部1/3 >5% 的样本频率 | OPTIONAL | HEURISTIC | freq=0.2857 | low |
| roof_overhang_ratio | Japanese 出檐比例分布 | SOFT | HEURISTIC | n=7 median=0.0 IQR[0.0,0.0299] | low |
| vertical_rhythm | Japanese 竖向节奏 = 5 等分质量分布归一化熵（1=均匀，低=质量集中） | SOFT | OBSERVED | n=7 median=0.7878 IQR[0.6967,0.8386] | medium |
| symmetry | Japanese 对称性 = max(symmetry_x, symmetry_z) | SOFT | OBSERVED | n=7 median=0.5786 IQR[0.3964,0.6554] | medium |
| symmetry_high | Japanese 高对称（≥0.9）样本频率 | OPTIONAL | OBSERVED | freq=0.0 | medium |
| window_density | Japanese 窗密度 = 玻璃体素数/暴露面估计（窗面积代理） | SOFT | HEURISTIC | n=7 median=0.0006 IQR[0.0001,0.0018] | low |
| palette_wood_ratio | Japanese wood 材料占比 | SOFT | OBSERVED | n=7 median=0.2539 IQR[0.2267,0.2948] | medium |
| palette_stone_ratio | Japanese stone 材料占比 | SOFT | OBSERVED | n=7 median=0.5174 IQR[0.2685,0.6222] | medium |
| palette_glass_ratio | Japanese glass 材料占比 | SOFT | OBSERVED | n=7 median=0.0009 IQR[0.0001,0.0033] | medium |
| palette_decorative_ratio | Japanese decorative 材料占比 | SOFT | OBSERVED | n=7 median=0.0429 IQR[0.0184,0.0662] | medium |
| palette_top_blocks | Japanese 高频方块 Top（类内聚合） | SOFT | OBSERVED | dirt 10%, oak_planks 9%, cobblestone 8%, stone_bricks 4%, cracked_stone_bricks 4% | medium |
| material_transition | Japanese 底/中/顶主导材料族模式众数：stone→wood→stone | OPTIONAL | HEURISTIC | freq=0.2857 | low |
| wall_thickness | Japanese 墙厚估计 = 中部1/3 层水平扫描线实体段中位数 | SOFT | HEURISTIC | n=7 median=2.0 IQR[1.0,2.0] | low |
| cantilever_frequency | Japanese 二层出挑（second_floor_overhang）频率 | OPTIONAL | OBSERVED | freq=0.1429 | medium |
| chimney_frequency | Japanese 烟囱候选频率（高出柱顶 P90 的孤立细柱） | OPTIONAL | HEURISTIC | freq=0.1429 | low |
| foundation_stone_base | Japanese 石质基座（stone_base，底部20% 石≥55%）频率 | OPTIONAL | OBSERVED | freq=0.2857 | medium |
| foundation_bottom_family | Japanese 底部 1/3 主导材料族众数：stone | SOFT | HEURISTIC | freq=0.7143 | low |

## Chinese（sample_n=4，PROVISIONAL）

| 维度 | 规则 | 类型 | basis | 统计 | 置信 |
|---|---|---|---|---|---|
| footprint_ratio | Chinese 平面长宽比 = max(x,z)/min(x,z)，1.0=方形 | SOFT | OBSERVED | n=4 median=1.0826 IQR[1.0435,1.2909] | medium |
| height_ratio | Chinese 高宽比 = size_y/max(size_x,size_z) | SOFT | OBSERVED | n=4 median=0.7515 IQR[0.5442,1.282] | medium |
| roof_height_ratio | Chinese 屋顶高度占比 = 上部 stair+slab 最长连续带高 / size_y | SOFT | HEURISTIC | n=4 median=0.1612 IQR[0.1102,0.3012] | low |
| roof_material_share_top3 | Chinese 顶部 1/3 区域 stair+slab 材料占比（屋顶材料信号） | SOFT | HEURISTIC | n=4 median=0.5613 IQR[0.4333,0.6132] | low |
| roof_overhang | Chinese 屋顶出檐：顶部1/3 脚印超出中部1/3 >5% 的样本频率 | OPTIONAL | HEURISTIC | freq=0.25 | low |
| roof_overhang_ratio | Chinese 出檐比例分布 | SOFT | HEURISTIC | n=4 median=0.0197 IQR[0.0,0.0491] | low |
| vertical_rhythm | Chinese 竖向节奏 = 5 等分质量分布归一化熵（1=均匀，低=质量集中） | SOFT | OBSERVED | n=4 median=0.7934 IQR[0.7705,0.8428] | medium |
| symmetry | Chinese 对称性 = max(symmetry_x, symmetry_z) | SOFT | OBSERVED | n=4 median=0.5971 IQR[0.406,0.7736] | medium |
| symmetry_high | Chinese 高对称（≥0.9）样本频率 | OPTIONAL | OBSERVED | freq=0.25 | medium |
| window_density | Chinese 窗密度 = 玻璃体素数/暴露面估计（窗面积代理） | SOFT | HEURISTIC | n=4 median=0.0018 IQR[0.0,0.009] | low |
| palette_wood_ratio | Chinese wood 材料占比 | SOFT | OBSERVED | n=4 median=0.2164 IQR[0.186,0.2217] | medium |
| palette_stone_ratio | Chinese stone 材料占比 | SOFT | OBSERVED | n=4 median=0.5352 IQR[0.4777,0.6151] | medium |
| palette_glass_ratio | Chinese glass 材料占比 | SOFT | OBSERVED | n=4 median=0.0041 IQR[0.0,0.018] | medium |
| palette_decorative_ratio | Chinese decorative 材料占比 | SOFT | OBSERVED | n=4 median=0.0045 IQR[0.0013,0.0269] | medium |
| palette_top_blocks | Chinese 高频方块 Top（类内聚合） | SOFT | OBSERVED | stone_bricks 29%, spruce_slab 7%, smooth_stone_slab 6%, stone 4%, oak_planks 3% | medium |
| material_transition | Chinese 底/中/顶主导材料族模式众数：stone→stone→stone | SOFT | HEURISTIC | freq=0.5 | low |
| wall_thickness | Chinese 墙厚估计 = 中部1/3 层水平扫描线实体段中位数 | SOFT | HEURISTIC | n=4 median=1.0 IQR[1.0,1.25] | low |
| cantilever_frequency | Chinese 二层出挑（second_floor_overhang）频率 | OPTIONAL | OBSERVED | freq=0.0 | medium |
| chimney_frequency | Chinese 烟囱候选频率（高出柱顶 P90 的孤立细柱） | OPTIONAL | HEURISTIC | freq=0.25 | low |
| foundation_stone_base | Chinese 石质基座（stone_base，底部20% 石≥55%）频率 | SOFT | OBSERVED | freq=0.5 | medium |
| foundation_bottom_family | Chinese 底部 1/3 主导材料族众数：stone | SOFT | HEURISTIC | freq=1.0 | low |


## 附录：IR 衍生 HEURISTIC 算法与盲区

1. **roof_height_ratio**：在 y≥0.4·size_y 范围找"本层 (stair+slab)/实体 ≥0.25 且本层实体≥3"的最长连续层带，带高 / size_y；**不从最顶层起算**（尖顶/装饰帽常为非楼梯方块，从顶起算会立即断裂——调试实测：世界之塔顶部 8 层 share=0）。盲区：平屋顶带长≈0–1；上部立面/基座装饰楼梯成带会高估；植被顶不成带（→0）。配套信号 **roof_material_share_top3** =顶部 1/3 区域 (stair+slab)/实体（任务书 9.1 建议的屋顶材料信号）。二者均为材料信号，不是屋面几何重建。
2. **roof_overhang_ratio**：顶部 1/3 脚印超出中部 1/3 的比例。盲区：三层皆错位的塔/雕塑会得到非零值，不等于真正屋檐。
3. **material_transition**：底/中/顶三段体素多数材料族（palette_dictionary 族表）。盲区：段内混合时只取多数族；装饰族（树叶）在顶部常胜出，可能掩盖屋面瓦材料。
4. **wall_thickness**：中部 1/3 层水平扫描线，两侧为空气的实体段（≤8 格）中位数。盲区：含室内隔断墙；露天构件（栅栏/树干）短段拉低中位数；实心肌体长段被排除。
5. **chimney_candidate**：柱顶高出全图柱顶 P90 ≥3 格且四邻柱顶低 ≥2 格的孤立细柱。盲区：尖顶/塔尖/树梢/旗杆同样触发——仅作频率倾向。V6C2 chimney 特征检测全库 0 次，故此处为唯一烟囱信号，可靠性低。
6. **window_rhythm 规律性 / entrance_placement 方位**：元数据不足，按纪律 UNKNOWN。
