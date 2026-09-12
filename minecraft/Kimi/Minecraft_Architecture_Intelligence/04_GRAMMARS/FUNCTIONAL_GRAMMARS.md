# FUNCTIONAL_GRAMMARS — 功能语法

> 生成：`scripts/build_grammar.py`。样本纪律同上。**房间语义无法自动识别**：所有 zone 均为 walkable connected region（可走连通分量），不声称识别 bedroom/kitchen；public/private 等语义推断标 INFERRED。Decoration/Vehicle 多为非建筑样本，其「规则」多为负向特征（无门/无室内），这本身就是功能画像。


## Residential（sample_n=23，SUPPORTED）

| 维度 | 规则 | 类型 | basis | 统计 | 置信 |
|---|---|---|---|---|---|
| required_zones.enclosed_interior | Residential 存在围合室内（interior_air_ratio≥0.01）频率 0.39 | OPTIONAL | HEURISTIC | freq=0.3913 | medium |
| required_zones.exterior_door | Residential 至少 1 扇外部门频率 0.78（door_count≠entrance_count，此处为外部门候选） | STRONG | HEURISTIC | freq=0.7826 | medium |
| optional_zones.upper_floor | Residential ≥2 层频率 0.37（上层作为可选 zone） | OPTIONAL | HEURISTIC | freq=0.3684 | medium |
| optional_zones.courtyard | Residential 院落（courtyard 特征）频率 0.00 | OPTIONAL | OBSERVED | freq=0.0 | high |
| zone_adjacency.largest_component | Residential 最大可走分量占比中位 0.36（高=各区连通好） | SOFT | HEURISTIC | n=23 median=0.3599 IQR[0.2761,0.4778] | medium |
| zone_adjacency.isolated_spaces | Residential 孤立空间数（≥8 体素非主分量）中位 32.0 | SOFT | HEURISTIC | n=23 median=32.0 IQR[21.0,46.5] | medium |
| public_private_separation | Residential 公私分区不可从 IR 直接判定；弱代理：≥2 层频率 0.37（上层私密假设为 INFERRED） | OPTIONAL | INFERRED | freq=0.3684 | medium |
| vertical_access.presence | Residential 存在垂直交通（楼梯簇/梯柱≥1）频率 1.00 | STRONG | HEURISTIC | freq=1.0 | medium |
| vertical_access.multifloor_requires | Residential 多层 ⇒ 有垂直交通：条件频率 1.00（n_multi=7） | SOFT | HEURISTIC | freq=1.0 | low |
| vertical_access.means | Residential 垂直交通方式：楼梯簇中位 116、梯柱中位 1 | SOFT | OBSERVED | stair_cluster_median=116.0, ladder_column_median=1.0 | high |
| entrance_relation.exterior_door_count | Residential 外部门候选数中位 2 | SOFT | HEURISTIC | n=23 median=2.0 IQR[1.0,3.5] | medium |
| circulation_constraints.dead_end_ratio | Residential 死端比例（度1站位/总站位）中位 0.13 | SOFT | HEURISTIC | n=23 median=0.1334 IQR[0.0843,0.1851] | medium |
| circulation_constraints.usable_floor_area | Residential 可用楼面面积中位 1342 格 | SOFT | HEURISTIC | n=19 median=1342.0 IQR[926.0,1948.0] | medium |

## Decoration（sample_n=22，SUPPORTED）

| 维度 | 规则 | 类型 | basis | 统计 | 置信 |
|---|---|---|---|---|---|
| required_zones.enclosed_interior | Decoration 存在围合室内（interior_air_ratio≥0.01）频率 0.14 | OPTIONAL | HEURISTIC | freq=0.1364 | medium |
| required_zones.exterior_door | Decoration 至少 1 扇外部门频率 0.00（door_count≠entrance_count，此处为外部门候选） | OPTIONAL | HEURISTIC | freq=0.0 | medium |
| optional_zones.upper_floor | Decoration ≥2 层频率 0.42（上层作为可选 zone） | SOFT | HEURISTIC | freq=0.4211 | medium |
| optional_zones.courtyard | Decoration 院落（courtyard 特征）频率 0.00 | OPTIONAL | OBSERVED | freq=0.0 | high |
| zone_adjacency.largest_component | Decoration 最大可走分量占比中位 0.35（高=各区连通好） | SOFT | HEURISTIC | n=22 median=0.3465 IQR[0.1838,0.6355] | medium |
| zone_adjacency.isolated_spaces | Decoration 孤立空间数（≥8 体素非主分量）中位 2.0 | SOFT | HEURISTIC | n=22 median=2.0 IQR[0.0,16.75] | medium |
| public_private_separation | Decoration 公私分区不可从 IR 直接判定；弱代理：≥2 层频率 0.42（上层私密假设为 INFERRED） | OPTIONAL | INFERRED | freq=0.4211 | medium |
| vertical_access.presence | Decoration 存在垂直交通（楼梯簇/梯柱≥1）频率 0.50 | SOFT | HEURISTIC | freq=0.5 | medium |
| vertical_access.multifloor_requires | Decoration 多层 ⇒ 有垂直交通：条件频率 0.38（n_multi=8） | OPTIONAL | HEURISTIC | freq=0.375 | medium |
| vertical_access.means | Decoration 垂直交通方式：楼梯簇中位 0、梯柱中位 0 | SOFT | OBSERVED | stair_cluster_median=0.0, ladder_column_median=0.0 | high |
| entrance_relation.exterior_door_count | Decoration 外部门候选数中位 0 | STRONG | HEURISTIC | n=22 median=0.0 IQR[0.0,0.0] | medium |
| circulation_constraints.dead_end_ratio | Decoration 死端比例（度1站位/总站位）中位 0.16 | SOFT | HEURISTIC | n=22 median=0.1636 IQR[0.0715,0.2503] | medium |
| circulation_constraints.usable_floor_area | Decoration 可用楼面面积中位 267 格 | SOFT | HEURISTIC | n=19 median=267.0 IQR[76.5,1048.0] | medium |

## Castle（sample_n=14，SUPPORTED）

| 维度 | 规则 | 类型 | basis | 统计 | 置信 |
|---|---|---|---|---|---|
| required_zones.enclosed_interior | Castle 存在围合室内（interior_air_ratio≥0.01）频率 0.50 | SOFT | HEURISTIC | freq=0.5 | medium |
| required_zones.exterior_door | Castle 至少 1 扇外部门频率 0.71（door_count≠entrance_count，此处为外部门候选） | SOFT | HEURISTIC | freq=0.7143 | medium |
| optional_zones.upper_floor | Castle ≥2 层频率 0.45（上层作为可选 zone） | SOFT | HEURISTIC | freq=0.4545 | medium |
| optional_zones.courtyard | Castle 院落（courtyard 特征）频率 0.00 | OPTIONAL | OBSERVED | freq=0.0 | high |
| zone_adjacency.largest_component | Castle 最大可走分量占比中位 0.39（高=各区连通好） | SOFT | HEURISTIC | n=14 median=0.3876 IQR[0.2134,0.6077] | medium |
| zone_adjacency.isolated_spaces | Castle 孤立空间数（≥8 体素非主分量）中位 53.5 | SOFT | HEURISTIC | n=14 median=53.5 IQR[28.75,105.5] | medium |
| public_private_separation | Castle 公私分区不可从 IR 直接判定；弱代理：≥2 层频率 0.45（上层私密假设为 INFERRED） | OPTIONAL | INFERRED | freq=0.4545 | medium |
| vertical_access.presence | Castle 存在垂直交通（楼梯簇/梯柱≥1）频率 1.00 | STRONG | HEURISTIC | freq=1.0 | medium |
| vertical_access.multifloor_requires | Castle 多层 ⇒ 有垂直交通：条件频率 1.00（n_multi=5） | SOFT | HEURISTIC | freq=1.0 | low |
| vertical_access.means | Castle 垂直交通方式：楼梯簇中位 113、梯柱中位 4 | SOFT | OBSERVED | stair_cluster_median=113.0, ladder_column_median=3.5 | high |
| entrance_relation.exterior_door_count | Castle 外部门候选数中位 15 | SOFT | HEURISTIC | n=14 median=15.0 IQR[0.5,26.75] | medium |
| circulation_constraints.dead_end_ratio | Castle 死端比例（度1站位/总站位）中位 0.08 | SOFT | HEURISTIC | n=14 median=0.0762 IQR[0.0396,0.0944] | medium |
| circulation_constraints.usable_floor_area | Castle 可用楼面面积中位 2206 格 | SOFT | HEURISTIC | n=11 median=2206.0 IQR[1598.5,4729.0] | medium |

## Tower（sample_n=13，SUPPORTED）

| 维度 | 规则 | 类型 | basis | 统计 | 置信 |
|---|---|---|---|---|---|
| required_zones.enclosed_interior | Tower 存在围合室内（interior_air_ratio≥0.01）频率 0.31 | OPTIONAL | HEURISTIC | freq=0.3077 | medium |
| required_zones.exterior_door | Tower 至少 1 扇外部门频率 0.54（door_count≠entrance_count，此处为外部门候选） | SOFT | HEURISTIC | freq=0.5385 | medium |
| optional_zones.upper_floor | Tower ≥2 层频率 0.62（上层作为可选 zone） | SOFT | HEURISTIC | freq=0.6154 | medium |
| optional_zones.courtyard | Tower 院落（courtyard 特征）频率 0.00 | OPTIONAL | OBSERVED | freq=0.0 | high |
| zone_adjacency.largest_component | Tower 最大可走分量占比中位 0.43（高=各区连通好） | SOFT | HEURISTIC | n=13 median=0.435 IQR[0.2109,0.5194] | medium |
| zone_adjacency.isolated_spaces | Tower 孤立空间数（≥8 体素非主分量）中位 14.0 | SOFT | HEURISTIC | n=13 median=14.0 IQR[4.0,19.0] | medium |
| public_private_separation | Tower 公私分区不可从 IR 直接判定；弱代理：≥2 层频率 0.62（上层私密假设为 INFERRED） | OPTIONAL | INFERRED | freq=0.6154 | medium |
| vertical_access.presence | Tower 存在垂直交通（楼梯簇/梯柱≥1）频率 1.00 | STRONG | HEURISTIC | freq=1.0 | medium |
| vertical_access.multifloor_requires | Tower 多层 ⇒ 有垂直交通：条件频率 1.00（n_multi=8） | HARD | HEURISTIC | freq=1.0 | medium |
| vertical_access.means | Tower 垂直交通方式：楼梯簇中位 44、梯柱中位 1 | SOFT | OBSERVED | stair_cluster_median=44.0, ladder_column_median=1.0 | high |
| entrance_relation.exterior_door_count | Tower 外部门候选数中位 1 | SOFT | HEURISTIC | n=13 median=1.0 IQR[0.0,2.0] | medium |
| circulation_constraints.dead_end_ratio | Tower 死端比例（度1站位/总站位）中位 0.10 | SOFT | HEURISTIC | n=13 median=0.1016 IQR[0.061,0.1913] | medium |
| circulation_constraints.usable_floor_area | Tower 可用楼面面积中位 473 格 | SOFT | HEURISTIC | n=13 median=473.0 IQR[246.0,1925.0] | medium |

## Religious（sample_n=10，SUPPORTED）

| 维度 | 规则 | 类型 | basis | 统计 | 置信 |
|---|---|---|---|---|---|
| required_zones.enclosed_interior | Religious 存在围合室内（interior_air_ratio≥0.01）频率 0.30 | OPTIONAL | HEURISTIC | freq=0.3 | medium |
| required_zones.exterior_door | Religious 至少 1 扇外部门频率 0.50（door_count≠entrance_count，此处为外部门候选） | SOFT | HEURISTIC | freq=0.5 | medium |
| optional_zones.upper_floor | Religious ≥2 层频率 0.30（上层作为可选 zone） | OPTIONAL | HEURISTIC | freq=0.3 | medium |
| optional_zones.courtyard | Religious 院落（courtyard 特征）频率 0.00 | OPTIONAL | OBSERVED | freq=0.0 | high |
| zone_adjacency.largest_component | Religious 最大可走分量占比中位 0.38（高=各区连通好） | STRONG | HEURISTIC | n=10 median=0.3813 IQR[0.3296,0.4506] | medium |
| zone_adjacency.isolated_spaces | Religious 孤立空间数（≥8 体素非主分量）中位 27.5 | SOFT | HEURISTIC | n=10 median=27.5 IQR[18.25,55.0] | medium |
| public_private_separation | Religious 公私分区不可从 IR 直接判定；弱代理：≥2 层频率 0.30（上层私密假设为 INFERRED） | OPTIONAL | INFERRED | freq=0.3 | medium |
| vertical_access.presence | Religious 存在垂直交通（楼梯簇/梯柱≥1）频率 1.00 | STRONG | HEURISTIC | freq=1.0 | medium |
| vertical_access.multifloor_requires | Religious 多层 ⇒ 有垂直交通：条件频率 1.00（n_multi=3） | SOFT | HEURISTIC | freq=1.0 | low |
| vertical_access.means | Religious 垂直交通方式：楼梯簇中位 60、梯柱中位 0 | SOFT | OBSERVED | stair_cluster_median=60.0, ladder_column_median=0.0 | high |
| entrance_relation.exterior_door_count | Religious 外部门候选数中位 1 | SOFT | HEURISTIC | n=10 median=1.0 IQR[0.0,2.75] | medium |
| circulation_constraints.dead_end_ratio | Religious 死端比例（度1站位/总站位）中位 0.08 | SOFT | HEURISTIC | n=10 median=0.0778 IQR[0.0606,0.1048] | medium |
| circulation_constraints.usable_floor_area | Religious 可用楼面面积中位 1612 格 | SOFT | HEURISTIC | n=10 median=1611.5 IQR[776.75,3390.0] | medium |

## Workshop（sample_n=7，PROVISIONAL）

| 维度 | 规则 | 类型 | basis | 统计 | 置信 |
|---|---|---|---|---|---|
| required_zones.enclosed_interior | Workshop 存在围合室内（interior_air_ratio≥0.01）频率 0.43 | SOFT | HEURISTIC | freq=0.4286 | low |
| required_zones.exterior_door | Workshop 至少 1 扇外部门频率 0.71（door_count≠entrance_count，此处为外部门候选） | SOFT | HEURISTIC | freq=0.7143 | low |
| optional_zones.upper_floor | Workshop ≥2 层频率 0.67（上层作为可选 zone） | SOFT | HEURISTIC | freq=0.6667 | low |
| optional_zones.courtyard | Workshop 院落（courtyard 特征）频率 0.00 | OPTIONAL | OBSERVED | freq=0.0 | medium |
| zone_adjacency.largest_component | Workshop 最大可走分量占比中位 0.56（高=各区连通好） | SOFT | HEURISTIC | n=7 median=0.5615 IQR[0.4404,0.7568] | low |
| zone_adjacency.isolated_spaces | Workshop 孤立空间数（≥8 体素非主分量）中位 7.0 | SOFT | HEURISTIC | n=7 median=7.0 IQR[3.0,28.0] | low |
| public_private_separation | Workshop 公私分区不可从 IR 直接判定；弱代理：≥2 层频率 0.67（上层私密假设为 INFERRED） | OPTIONAL | INFERRED | freq=0.6667 | low |
| vertical_access.presence | Workshop 存在垂直交通（楼梯簇/梯柱≥1）频率 0.86 | SOFT | HEURISTIC | freq=0.8571 | low |
| vertical_access.multifloor_requires | Workshop 多层 ⇒ 有垂直交通：条件频率 0.75（n_multi=4） | SOFT | HEURISTIC | freq=0.75 | low |
| vertical_access.means | Workshop 垂直交通方式：楼梯簇中位 28、梯柱中位 5 | SOFT | OBSERVED | stair_cluster_median=28.0, ladder_column_median=5.0 | medium |
| entrance_relation.exterior_door_count | Workshop 外部门候选数中位 2 | SOFT | HEURISTIC | n=7 median=2.0 IQR[1.0,4.0] | low |
| circulation_constraints.dead_end_ratio | Workshop 死端比例（度1站位/总站位）中位 0.09 | SOFT | HEURISTIC | n=7 median=0.0859 IQR[0.0743,0.1488] | low |
| circulation_constraints.usable_floor_area | Workshop 可用楼面面积中位 570 格 | SOFT | HEURISTIC | n=6 median=570.5 IQR[293.25,772.75] | low |

## Vehicle（sample_n=7，PROVISIONAL）

| 维度 | 规则 | 类型 | basis | 统计 | 置信 |
|---|---|---|---|---|---|
| required_zones.enclosed_interior | Vehicle 存在围合室内（interior_air_ratio≥0.01）频率 0.43 | SOFT | HEURISTIC | freq=0.4286 | low |
| required_zones.exterior_door | Vehicle 至少 1 扇外部门频率 0.71（door_count≠entrance_count，此处为外部门候选） | SOFT | HEURISTIC | freq=0.7143 | low |
| optional_zones.upper_floor | Vehicle ≥2 层频率 0.20（上层作为可选 zone） | OPTIONAL | HEURISTIC | freq=0.2 | low |
| optional_zones.courtyard | Vehicle 院落（courtyard 特征）频率 0.00 | OPTIONAL | OBSERVED | freq=0.0 | medium |
| zone_adjacency.largest_component | Vehicle 最大可走分量占比中位 0.38（高=各区连通好） | SOFT | HEURISTIC | n=7 median=0.377 IQR[0.3183,0.5145] | low |
| zone_adjacency.isolated_spaces | Vehicle 孤立空间数（≥8 体素非主分量）中位 48.0 | SOFT | HEURISTIC | n=7 median=48.0 IQR[12.5,111.0] | low |
| public_private_separation | Vehicle 公私分区不可从 IR 直接判定；弱代理：≥2 层频率 0.20（上层私密假设为 INFERRED） | OPTIONAL | INFERRED | freq=0.2 | low |
| vertical_access.presence | Vehicle 存在垂直交通（楼梯簇/梯柱≥1）频率 1.00 | SOFT | HEURISTIC | freq=1.0 | low |
| vertical_access.multifloor_requires | Vehicle 多层 ⇒ 有垂直交通：条件频率 1.00（n_multi=1） | SOFT | HEURISTIC | freq=1.0 | low |
| vertical_access.means | Vehicle 垂直交通方式：楼梯簇中位 208、梯柱中位 2 | SOFT | OBSERVED | stair_cluster_median=208.0, ladder_column_median=2.0 | medium |
| entrance_relation.exterior_door_count | Vehicle 外部门候选数中位 3 | SOFT | HEURISTIC | n=7 median=3.0 IQR[1.0,7.0] | low |
| circulation_constraints.dead_end_ratio | Vehicle 死端比例（度1站位/总站位）中位 0.11 | SOFT | HEURISTIC | n=7 median=0.1065 IQR[0.096,0.197] | low |
| circulation_constraints.usable_floor_area | Vehicle 可用楼面面积中位 825 格 | SOFT | HEURISTIC | n=5 median=825.0 IQR[210.0,2504.0] | low |

## Inn（sample_n=5，PROVISIONAL）

| 维度 | 规则 | 类型 | basis | 统计 | 置信 |
|---|---|---|---|---|---|
| required_zones.enclosed_interior | Inn 存在围合室内（interior_air_ratio≥0.01）频率 0.60 | SOFT | HEURISTIC | freq=0.6 | low |
| required_zones.exterior_door | Inn 至少 1 扇外部门频率 1.00（door_count≠entrance_count，此处为外部门候选） | SOFT | HEURISTIC | freq=1.0 | low |
| optional_zones.upper_floor | Inn ≥2 层频率 0.60（上层作为可选 zone） | SOFT | HEURISTIC | freq=0.6 | low |
| optional_zones.courtyard | Inn 院落（courtyard 特征）频率 0.00 | OPTIONAL | OBSERVED | freq=0.0 | medium |
| zone_adjacency.largest_component | Inn 最大可走分量占比中位 0.51（高=各区连通好） | SOFT | HEURISTIC | n=5 median=0.5125 IQR[0.5084,0.5487] | low |
| zone_adjacency.isolated_spaces | Inn 孤立空间数（≥8 体素非主分量）中位 44.0 | SOFT | HEURISTIC | n=5 median=44.0 IQR[20.0,63.0] | low |
| public_private_separation | Inn 公私分区不可从 IR 直接判定；弱代理：≥2 层频率 0.60（上层私密假设为 INFERRED） | OPTIONAL | INFERRED | freq=0.6 | low |
| vertical_access.presence | Inn 存在垂直交通（楼梯簇/梯柱≥1）频率 1.00 | SOFT | HEURISTIC | freq=1.0 | low |
| vertical_access.multifloor_requires | Inn 多层 ⇒ 有垂直交通：条件频率 1.00（n_multi=3） | SOFT | HEURISTIC | freq=1.0 | low |
| vertical_access.means | Inn 垂直交通方式：楼梯簇中位 118、梯柱中位 10 | SOFT | OBSERVED | stair_cluster_median=118.0, ladder_column_median=10.0 | medium |
| entrance_relation.exterior_door_count | Inn 外部门候选数中位 3 | SOFT | HEURISTIC | n=5 median=3.0 IQR[3.0,4.0] | low |
| circulation_constraints.dead_end_ratio | Inn 死端比例（度1站位/总站位）中位 0.09 | SOFT | HEURISTIC | n=5 median=0.0928 IQR[0.0714,0.1495] | low |
| circulation_constraints.usable_floor_area | Inn 可用楼面面积中位 1313 格 | SOFT | HEURISTIC | n=5 median=1313.0 IQR[980.0,3589.0] | low |

## Civic（sample_n=4，PROVISIONAL）

| 维度 | 规则 | 类型 | basis | 统计 | 置信 |
|---|---|---|---|---|---|
| required_zones.enclosed_interior | Civic 存在围合室内（interior_air_ratio≥0.01）频率 0.25 | OPTIONAL | HEURISTIC | freq=0.25 | low |
| required_zones.exterior_door | Civic 至少 1 扇外部门频率 0.75（door_count≠entrance_count，此处为外部门候选） | SOFT | HEURISTIC | freq=0.75 | low |
| optional_zones.upper_floor | Civic ≥2 层频率 0.67（上层作为可选 zone） | SOFT | HEURISTIC | freq=0.6667 | low |
| optional_zones.courtyard | Civic 院落（courtyard 特征）频率 0.25 | OPTIONAL | OBSERVED | freq=0.25 | medium |
| zone_adjacency.largest_component | Civic 最大可走分量占比中位 0.48（高=各区连通好） | SOFT | HEURISTIC | n=4 median=0.4812 IQR[0.4266,0.5522] | low |
| zone_adjacency.isolated_spaces | Civic 孤立空间数（≥8 体素非主分量）中位 37.5 | SOFT | HEURISTIC | n=4 median=37.5 IQR[33.5,72.0] | low |
| public_private_separation | Civic 公私分区不可从 IR 直接判定；弱代理：≥2 层频率 0.67（上层私密假设为 INFERRED） | OPTIONAL | INFERRED | freq=0.6667 | low |
| vertical_access.presence | Civic 存在垂直交通（楼梯簇/梯柱≥1）频率 1.00 | SOFT | HEURISTIC | freq=1.0 | low |
| vertical_access.multifloor_requires | Civic 多层 ⇒ 有垂直交通：条件频率 1.00（n_multi=2） | SOFT | HEURISTIC | freq=1.0 | low |
| vertical_access.means | Civic 垂直交通方式：楼梯簇中位 85、梯柱中位 1 | SOFT | OBSERVED | stair_cluster_median=85.0, ladder_column_median=1.0 | medium |
| entrance_relation.exterior_door_count | Civic 外部门候选数中位 2 | SOFT | HEURISTIC | n=4 median=2.5 IQR[0.75,5.5] | low |
| circulation_constraints.dead_end_ratio | Civic 死端比例（度1站位/总站位）中位 0.07 | SOFT | HEURISTIC | n=4 median=0.0705 IQR[0.0604,0.1081] | low |
| circulation_constraints.usable_floor_area | Civic 可用楼面面积中位 5034 格 | SOFT | HEURISTIC | n=3 median=5034.0 IQR[3855.0,6605.0] | low |
