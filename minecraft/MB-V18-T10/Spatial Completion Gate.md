# T10 Spatial Completion Gate

Scope：T09 罗马浴场主体、运动庭院及既有服务设施；BUILDING；目标 FINISHED。继承 T09 Architectural Intent，不新增主体或重新规划城市。

实际基准来自独立复制世界 MB-V18-T10-罗马浴场精修的 RegionReader 只读采样。1,161,216 格与 T09 归档最终方块状态比较，只有 1,222 格 grass_block 变为 dirt；视为当前来源状态，不逆改。源存档的数据包也与旧施工 runtime 不同，因此最终采用其所属客户端完整 mods/config，并完成资格验证；初次不匹配尝试保留为失败记录。

| Gate 项 | 本轮观察与判断 |
|---|---|
| Spatial Logic | 更衣—冷厅—暖室—热室与运动庭院共同服务公共洗浴；东炉房和水箱独立。池体、休息边界和公共空地可用，中央不依赖家具定义。 |
| Circulation | 重跑 14 条局部预期连接检查，全部成立。透视检查更衣分流、冷暖抬升门槛、庭院通道；维护梯在既有独立服务边。没有发现需重新开门或重铺主路线的 Core 问题。 |
| Massing / Section | 三跨高冷厅、低暖室颈部、圆穹顶热室、低更衣和西柱廊各有剖面与功能依据。穹顶体素阶梯较粗，但不是需要家具掩盖的核心缺失。 |
| Structure / Environment | 0 孤立实体，1,138 水方块静态床岸封闭。既有高差容纳热风空腔。供热和水路为建筑表达，流体更新稳定性依旧未验证。 |
| Minecraft Usability | 静态两格净空及正确方向台阶检查未发现大量卡头、断层或错误门槛。尚无原生客户端行走验证，不将静态结果当成原生碰撞证明。 |
| Upstream Defect Test | 不增加家具和装饰，主要活动与空间身份已成立。当前工具证据下答案 YES；无需修改 Frozen 内容即可进入 Finishing。 |

结论：`SPATIAL_COMPLETE → FINISHING`。这是本 Scope 的施工入口判断，不是回归测试 PASS / FAIL。

## Phase Protection

冻结 Program / Space Graph、主体量、Plan / Section、主屋顶、主入口和主要交通、地形骨架、全部水方块与池体几何、skyline、空间序列与功能分区。不存在需要改动的 Structural Vegetation。

逐笔保留 Finishing 修改坐标、前后方块及活动/构造原因。禁止 Y24 及以上任何方块改动；禁止已有实体变空气（既有家具除外）、空气变实体超出已声明活动区。材料替换只作用既有实体表面，不改变其占位。

Allowed：实际储物、少量工作台/浴后用品、任务照明、门框表面、地面纹样、因果性烟熏与磨损。Restricted 仅后勤院外小片踏实地面材质，保持标高和通行语义。每阶段比较实存变化、门槛连接、水体及限制区，最终重看相同视点并执行 Restraint。
