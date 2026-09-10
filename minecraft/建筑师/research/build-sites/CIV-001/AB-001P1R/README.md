# AB-001P1R｜Council Commons East-Connector Boundary Fit

**IMPLEMENTATION COMPLETED / AWAITING INDEPENDENT REVIEW**。

首选政治切口：**方块列X=88与X=89之间，物理边界平面X=89，Z=1726..1774**。48条单位陆地边构成该接口，没有删除一列方块或开挖水道。

- Alliance Commons：**92,124 blocks²**，A内X≤88的全部实际陆地。
- East connector：**13,661 blocks²**，A内X≥89的全部实际陆地。
- 合计：**105,785 blocks²**，恰好覆盖原A；两侧各1个连续分量，无遗漏、重叠或飞地。

这实现Owner的“A主体减东侧连接带”规则，没有内部小椭圆，没有目标面积/百分比。前序A外的陆地和水域不在此次面积计算内。

[边界报告](reports/联盟公地边界拟合.md) · [地图](visual/commons-connector-boundary.png) · [机器边界](commons-boundary.json)

## Geometry contract

`commons-geometry.json`、`connector-geometry.json`使用紧凑RLE：每条`[z,x_start,x_end]`包含首尾列。坐标是Minecraft方块索引；方块(x,z)占用[x,x+1)×[z,z+1)。`outline_segments`是精确方块边界合并线段`[x0,z0,x1,z1]`，含内水洞，未平滑；线段未按环排序，不应当作单一有序polygon顶点表。

外岸最窄列X88的48格与更东侧水洞截面的39个干陆位置不同。后一处外岸仍宽50格，因此不能把“干陆计数最小”自动当成主体自然收束的唯一答案。逐列、16列分带及±1列敏感性完整保留。选择由研究解释给定，程序不裁决政治语义。

## Reproduce

Python3.12、NumPy2.3.5、Pillow12.3.0，中文地图使用Windows微软雅黑。研究外围脚本只读前序数据契约；不导入前序业务内部模块，不创建空四层。

```powershell
python tooling/公地边界汇编.py
python tooling/边界独立核验.py snapshot
python tooling/公地边界汇编.py
python tooling/边界独立核验.py
python tooling/源证据核验.py seal
python tooling/交付封口.py
```

`snapshot`保存本地重建比较哈希；不是源world epoch。`源证据核验.py init`仅用于首次冻结任务源，拒绝覆盖，不得为了重建重置epoch。缓存缺失则恢复原R1缓存并核对hash，不重新扫描整个世界。完整初始源清单保留本地`D:/Games/Minecraft/AI工程/研究缓存/建筑师/AB-001P1R/source-before.json`，LOCAL_ONLY / PRESERVE_LOCAL；登记见validation/lineage.json。

新world block reads=0，broad rescan=0，world writes=0。Canon、Grammar、Capacity文档及前序evidence保持原样。GPT接受边界后自行重算Program/Capacity，AB-001P2继续HOLD；本包不包含建筑或道路方案。
