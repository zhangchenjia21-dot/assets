# AB-001P1R｜Completion

状态：**IMPLEMENTATION COMPLETED / AWAITING INDEPENDENT REVIEW**。

执行基线：`assets/main @ d83d155`。保留此前并行项目提交。日期：2026-09-10。

## 结果

首选切口：**X=88/89两列之间，物理边界平面X=89，Z=1726..1774**。48条单位陆地边构成政治接口；未开挖、未删除方块。

|分区|面积 blocks²|实际方块bounds|
|---|---:|---|
|Alliance Commons|**92,124**|[-349,1685,88,1982]|
|A内东侧connector|**13,661**|[89,1664,240,1841]|
|原A合计|**105,785**|[-349,1664,240,1982]|

**Commons∪connector=A；Commons∩connector为空。** 两侧各自单一连续；A无遗漏、无重复、无飞地。没有在A内部再缩一个小椭圆，没有裁掉连接带以外的自然主体边缘。

## 判定依据

全X逐列与16列分带记录显示，外岸宽度在主体东侧明显收束，X88为局部最窄外岸截面48格；更东的X109/110干陆数39格包含内部水洞效应，外岸跨度仍50格。选择最窄完整列东缘，保留A主体。

公开像素级不确定性：平面X88/89/90对应公地92,076 / 92,124 / 92,173格²；均保持两侧连续。下游X110另作诊断，不作为同等首选切口。政治拟合仍待GPT接受，工程测试不替代独立审核。

## 交付与验证

[研究包](../../research/build-sites/CIV-001/AB-001P1R/README.md) 含机器边界、两份紧凑RLE与精确轮廓、截面与地形辅助统计、轻量地图、报告和复现代码。

- 复用AB-001P1实际geometry与R1缓存，**new world block reads=0，broad rescan=0，world writes=0**。
- 集合面积守恒、RLE往返、轮廓边集合独立对照和四邻接连通核验通过。
- connector与父陆体有190条接出边；独立拓扑路径在不进入Commons的条件下到达X400主岛区域。该路径仅为连通见证，不是道路规划。
- 五项核心artifact新进程重建SHA256一致。
- 世界、V1/NG-2/NG-3、WB-002R/R1/WB-003R、AB-001P1、World Canon与architecture（含Grammar、Capacity）完整前后inventory/hash/size/mtime一致。
- 完整源清单LOCAL_ONLY / PRESERVE_LOCAL；新research payload见validation/payload.json，满足D-010目标。
- 脚本是研究外围复现流程，中文命名/语义注释，无前序内部业务模块直连、无空层或建筑设计。

## Stop

仅提交本研究包、此Completion与current机械状态。正常commit + push assets/main，核对远端HEAD后停止交GPT独立审核。

**AB-001P2继续HOLD。** GPT接受精确Commons边界后再重算Program/Capacity；本轮未修改Canon、Grammar或Capacity，未设计三席议事大厅及任何附属空间。
