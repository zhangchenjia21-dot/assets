# NG-2 可查询事实层

`refinement.sqlite` 是本轮派生快照。发布时以 gzip 分片保存，恢复命令见根 README；不是原始存档，也不包含完整区块 NBT。SQLite `user_version=1`。

| 表 | 主键 | 含义 |
|---|---|---|
| samples | x,z | 实际整数方块柱的表面、过滤后表面、水区间、材料及 biome |
| target_samples | target,x,z | ROI 成员及首次插入分辨率阶段；重叠目标共享 samples |
| chunks | cx,cz | 源 region 相对路径、sector、DataVersion、生成状态和方块实体位置 |
| states | id | 原始方块 Name / Properties 字典 |
| biomes | id | WORLD_SURFACE 顶柱位置的实际 biome ID |
| targets | id | V1 SITE 原记录与本轮 ROI 配置 |
| profiles | target,name,x,z | 横纵及两条对角实测断面，含距离、高度和水面 |
| assessments | target | 人工解释、判决、限制及证据引用，与导出 JSON 一致 |

坐标与 bounds 均为方块闭区间 `[xmin,zmin,xmax,zmax]`，北为 -Z，东为 +X。维度 `minecraft:overworld`，DataVersion 4903。所有高度单位为 blocks；面积为 blocks²。

`surface_y` 从实际 WORLD_SURFACE heightmap 解码。`exposed_y` 向下越过 L0 明示的植被/空气，仍可能落在冰、天然装饰、人工表面、洞口内或水面；它不是裸岩高程或原始地形恢复。`ocean_floor_y` 保留源 OCEAN_FLOOR 观测，不当作测得水深。`water_y` 与 `water_bottom` 是在过滤后表面或连续冰层下观察到的连续水方块区间，闭区间；不存在时为 -32768。水深为 top-bottom+1。水生植物、bubble_column 按实际含水状态类别纳入，任意 waterlogged 形状不纳入。没有穿透所有固体去调查地下河；海底洞口可造成很深的连续水柱。

`ice_covered=1` 表示实际冰下找到水，不是仅见冰便当成水。水连通为四邻柱实际水区间至少共享一个 Y；不靠 biome，不跨干桥或对角。冰山/雪盖下被固体隔开的水可分为多个表层可见区间分量；水面二维陆地分量不是三维洞穴/桥梁拓扑。

`artificial_material=1` 只是表面或过滤后材料匹配的候选旗标。Terralith 的自然石 slab、土径、苔藓 carpet 会命中；方块实体也可能来自世界生成。它不等于人工施工来源。具体来源不确定性由 assessment 的 `anthropogenic_contamination` 与说明承担。

8 格网格保存真实点值，4 格细化规则及 patch 清单见 manifest；三个水目标全 ROI 逐列，山口另有逐列核心。`target_samples.stage` 只表示首次写入阶段，不表示其它阶段没有再次读取。`chunks` 是读取过的区块数量，不等于每区块256柱都入库；Reader 解码整块并仅持久化被请求柱。

NPZ `grid8` 数组为 `[z,x]`，步长8；`topology1` 和 `critical1` 步长1。`height` 对应 exposed_y，`water_top/bottom` 同数据库。低坡度 mask 用中心差分 rise/run≤0.125；面积是采样柱数×64的局部估计，不是逐列精确面积。mask 若不包含 V1 网格点，则选最近符合点，指标显式记录 seed/距离；不得把这种结果称为 target 精确所在分量。边界触 ROI 表示空间截断。水目标的水陆面积为实际柱计数，但分量触边时仍不是完整地理对象面积。

```sql
-- 从任一assessment回溯具体柱、材料、源region/chunk。
SELECT t.target,s.x,s.z,s.surface_y,s.exposed_y,s.water_y,s.water_bottom,
       st.json,b.name,c.region,c.cx,c.cz,c.sector
FROM target_samples t JOIN samples s USING(x,z)
JOIN states st ON st.id=s.exposed_state JOIN biomes b ON b.id=s.biome
JOIN chunks c ON c.cx=(s.x >> 4) AND c.cz=(s.z >> 4)
WHERE t.target='SITE-003' AND s.x=-248 AND s.z=2056;
```

负坐标使用算术右移 / Python `//16`，不能用朝零截断除法计算 chunk。源文件 SHA256/size/mtime 位于 `manifest/world-before.json`。数据的有效性绑定该快照；不提供后来世界变化的自动拼接。
