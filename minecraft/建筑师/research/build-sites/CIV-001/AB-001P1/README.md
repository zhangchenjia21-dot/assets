# AB-001P1｜Three-seat Council Center-island Site Gate

**IMPLEMENTATION COMPLETED / AWAITING INDEPENDENT REVIEW / OWNER_SELECTION_REQUIRED**。

尚未选定Site；A/B设计进入状态均NOT_READY。world writes = 0。不包含三席议事大厅方案或施工。

- [中心岛SiteGate报告](reports/中心岛SiteGate.md)
- [候选对比图](visual/site-candidates.png)
- [Mapping verdict](site-mapping.json)
- [两候选局部Context](site-candidates.json)
- [审核入口](review/index.json)

A是内湾里视觉居中的东岛西伸低地，真实连接东岛；B是西部C形低岛内侧中部，仍属西岛本体。两者都不是独立中心小岛，不能靠地形评分替Owner决定称呼。两者的比较框是人为观察窗口，实际成员以`geometry/*-land-runs.json`为准。

复用R1 observed.sqlite/derived.npz及WB-003R crossing-profile，未重新扫描世界。本轮查询的缓存上下文X=-800..1200、Z=1376..2655；候选统计只取各窗口与父陆体成员交集。R1原生4格植被样本、坡度/地形分类及表层材料过滤限制均继承；表层flag不替代人工结构调查。射线只说明地形后景，不保证游戏可视性或建筑高度。

Python3.12、NumPy2.3.5、Pillow12.3.0；本机中文图使用msyh.ttc。脚本是研究复现/验证外围入口，未创建业务模块或空四层，也不引用前序内部Python代码。源保护器为WB-003R已公开机制的独立副本；其余只读SQLite/NPZ/JSON数据契约。

```powershell
python tooling/候选证据汇编.py
python tooling/候选证据核验.py
python tooling/源证据核验.py seal
```

`init`只用于首次冻结任务源清单，拒绝覆盖；不要为了复现而重新初始化epoch。seal需要本地原清单及当前世界，世界变化应报告变化，不覆盖历史证据。复现候选统计/地图不需要打开游戏或读NBT；R1本地缓存缺失须按R1恢复说明恢复并核对SHA256，不能把轻量包当作完整raw。候选语义与mapping verdict是人工解释，不由代码决定。

完整源清单保留在 `D:/Games/Minecraft/AI工程/研究缓存/建筑师/AB-001P1/source-before.json`，`LOCAL_ONLY / PRESERVE_LOCAL`；登记见validation/lineage.json。新输出限定本目录，前序目录、Canon、Grammar不变。重建哈希与最终payload见validation。
