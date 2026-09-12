# MD-001P｜中域详细总体规划

**MASTERPLAN PROPOSAL / AWAITING GPT + OWNER REVIEW**

入口：[完整总体规划](MASTERPLAN.md) · [第一座建筑规划推荐](first-build-recommendation.md) · [内部 Critic](validation/PLANNER-CRITIC.md)。

本方案覆盖 revision154 的整个 Middle Domain：**391,002** block-column。主体 390,995 列、离散 7 列均保留；后者仅作地形保留。采用 D-024 接受边界与 D-025 密度梯度，不修改 Canon / Grammar，不设计或施工单体。

## 等比例图

|图|用途|
|---|---|
|[terrain-base.png](visual/terrain-base.png)|真实地形、领土与政治邻域|
|[planning-subareas.png](visual/planning-subareas.png)|五个地形关联规划子区|
|[settlement-hierarchy.png](visual/settlement-hierarchy.png)|1 主 + 3 次聚落候选面|
|[movement-exchange.png](visual/movement-exchange.png)|七条陆地走廊预留、Commons / East / 南岸接口|
|[land-use-masterplan.png](visual/land-use-masterplan.png)|完整互斥土地使用安排|
|[human-use-density.png](visual/human-use-density.png)|最高主核、紧凑次节点、周转带与开放/保护地|
|[phasing-first-build.png](visual/phasing-first-build.png)|分期与首栋规划出口|
|[principal-life-structure.png](visual/principal-life-structure.png)|主镇混合生活活动重心；无建筑 footprint|

七张全域图的有效地图原点像素 `(45,65)` 对应世界 `(-400,1440)`，X/Z 均为 **1 px/block**。主镇图 X/Z 均为 **3 px/block**，独立坐标框见 `validation/principal-map-contract.json`。比例不因展示窗口缩放改变原 PNG 内的坐标关系。地图圆点仅为符号，候选面成员以 RLE 为准；虚线不是施工街线。

## 机器入口

`MASTERPLAN.json` 汇总 source revision/hash、面积、密度原则、各层引用、接口、保留地、首栋推荐及 `world_write_authorized=false`。

- `subareas.json`：五区精确 RLE、地形 / biome / 岸线 / 缓地、功能预算与开放地职责。
- `settlement-nodes.json`：四个规划节点、经缓存核对的点、实际候选面、密度区间和离散 7 格保留。
- `movement-network.json`：逐柱路径、最大表层步高、累计升降、政治接口、既有水岸证据及未验证项。
- `land-use.json`：L1–L8 对全中域无重叠、无遗漏覆盖。
- `human-use-intensity.json`：H0–H4 对全中域完整覆盖，成熟期容量计算与 D-025 条件。
- `principal-hub-structure.json`：A1–A4 活动重心、共享巷院与使用关系。
- `resident-life-system.json`：居民职业、食物/水/污物/消防/通行/公共/土地使用关系。

RLE 每项 `[z,x0,x1]` 两端包含；是逐 block-column 的规划成员，不是 bounds 矩形。block(x,z) 占据 `[x,x+1) × [z,z+1)`。土地用途 / 强度文件的 `geometry` 是互斥分区；不同专题图层可以叠合。比如保留地上的走廊仍需要未来局部判断，不获得自动施工优先权。

## 密度与限制

修订后的四个混合面合计 **72,609** 列；主镇占地意向比例最高。成熟期节点建筑 footprint 合计约占中域 **7.0%–9.5%**，不是现在的建筑数量或人口。中域最高平均密度是 D-025 规划硬输入；West/East 尚未总规，不伪造两域实测覆盖率来证明数字排序。

采用 accepted cache epoch；`world writes = 0`、`new world block reads = 0`、`broad rescan = 0`。饮水、当前地物、地下人工内容、车辆通行、南岸水深/航行等须在具体 Site Gate 解决。生物群系和地形参数不自动裁决土地用途；本次人物/活动与节点选择为待接受的规划判断。

## 复现

Python 3.12、numpy 2.3.5、Pillow 12.3.0、Windows 微软雅黑；仅使用既有 R1 / WB-003R / P1R / TT-002R 数据，不需游戏运行、网络或插件。

```text
python -X utf8 tooling/总体规划汇编.py
python -X utf8 tooling/主镇生活关系图.py
python -X utf8 tooling/规划独立核验.py
```

依赖 R1 已按原说明恢复的 `raw-or-queryable/observed.sqlite` 与 `derived.npz`。代码检查来源 SHA256；不以缺缓存为理由重扫。开始时源清单与诊断 NPZ 位于 `D:/Games/Minecraft/AI工程/研究缓存/建筑师/MD-001P`，完整 raw / 中间数组不上传。历史 source-before 缺失时，不能伪造本轮封口；几何重建仍可用原证据独立运行。

脚本属于规划外围，用标准文件数据契约读取前序证据，不导入其内部模块，没有为形式创建四层空包装。规则参数只汇编已经解释的本轮规划判断，不是通用自动城镇生成器。

完成提交后停止，等待 GPT + Owner 审核；首栋 Local Site Gate 尚未开始。
