# NG-2｜Representative Local Refinement

状态：**implementation completed / awaiting independent review**。本轮为 NG-002 的离线只读研究交付，不是 Stage PASS，不进入 NG-3、World Canon 或建筑规划。

基线：`assets/main@4b9b1f7e600708ff67e1ef2f844a9d3de0ba2242`。目标存档 `建筑师`，DataVersion 4903。完整任务契约见 [TASK.md](../../../tasks/NG-002/TASK.md)。

## 结果索引

| Target / V1 source | 本轮判断 | 限定结论 | 入库柱数 |
|---|---|---|---:|
| [SITE-002](assessments/SITE-002.json) / FEAT-657 | CONFIRMED | 邻近局部浅鞍部；不等于整条区域山口 | 116,570 |
| [SITE-005](assessments/SITE-005.json) / FEAT-001 | RECLASSIFIED | 山前缓坡及伴生河流低地；未建立双壁宽谷 | 39,546 |
| [SITE-015](assessments/SITE-015.json) / GEO-566 | CONFIRMED | 水岸低起伏平原片段，面积有采样/截断限制 | 40,972 |
| [SITE-014](assessments/SITE-014.json) / GEO-729 | CONFIRMED | 山侧连续台地片段，区域边界仍开放 | 26,708 |
| [SITE-017](assessments/SITE-017.json) / GEO-534 | CONFIRMED | 连续山体及山肩，不是阈值碎片 | 156,398 |
| [SITE-019](assessments/SITE-019.json) / HYD-003 | RECLASSIFIED | 有局部展宽的连通分支水道，不是封闭独立湖体 | 2,162,688 |
| [SITE-003](assessments/SITE-003.json) / FEAT-618 | CONFIRMED | 实际外水环包围的低岛，含内池塘 | 1,556,480 |
| [SITE-011](assessments/SITE-011.json) / HYD-142 | CONFIRMED | 多出口沿海凹入水域，开口位置为解释性断面 | 917,504 |

合计 5,016,866 条 target-column 关联，去重后 5,007,380 根柱，44,108 个源区块。全部结论保留原 SITE 与 source ID；没有重编号或改写 V1。

6 个 CONFIRMED、2 个 RECLASSIFIED 是本次证据结果，不是通过率目标。山口和海湾只在明示局部尺度成立；其语义和限制需要独立审核。

## 事实与派生视图

- **可查询事实层**：[SQLite schema / 查询例](raw-or-queryable/SCHEMA.md)、压缩分片、states/biomes/chunks/samples/target_samples；[归档索引](manifest/archive.json)。恢复后可查询所有柱及源 region。
- **解释层**：八份 `assessments/SITE-xxx.json` 同时入库 `assessments`；原始解释输入 `interpretations.json` 保留，指标算法不自行决定 verdict。每份 `*-metrics.json` 有观测、面积、坡度、方块实体、分量及四向断面统计。
- **关键形态**：山口 1 格核心的路径/溢出高程见 `SITE-002-metrics.json#/critical_depression_test`；海湾验证锚点与指定开口断面见 `SITE-011.json#/refined_metrics/opening_evidence`；河道延伸断面见 `SITE-019.json`。
- **阅读视图**：[八目标总览](visual/eight-target-comparison.png)，每目标 context（含四条断面）、slope-boundary，三个水目标逐列水岸图，山口逐列核心等高线/路径图。全部北向 -Z、东向 +X，标注 ROI、比例、真实采样分辨率与 V1 点/cell。
- **可复核断面**：`profiles/SITE-xxx.json` 与 SQLite `profiles`。东西、南北逐列；对角每次 X/Z 各走1，水平间距 √2。图是派生视图，数据库和源快照优先。

## 方法与限制

先按目标关系确定不同 ROI，以8格真实点网获取背景。坡度 rise/run≥0.25、水岸变化或目标96格半径触发整个16×16区块的4格细化；所有目标读取四条逐列断面，三个水目标全ROI逐列，山口增加256×256逐列核心。ROI 和每一细化 patch 位于 `manifest/`，入库阶段表示首次插入，不是唯一读取阶段。

宽谷向东扩512格核查另一侧地形；内陆水体向西扩512格追踪真实连接。后者最终向北/南触边，已经足以否定封闭独立湖体，未继续扩展成完整流域调查。岛体外陆界不触边，内池塘与外围水环分开判断。

山口点 Y=614 本身是微凹点；邻近东西步进路径最高Y=621。南北64格的高地与东西较低地形支持局部浅鞍部，但算法没有证明游戏实体通行或整座山脉两侧路线。海湾东北指定断面宽42柱，西南指定断面主水段宽444柱；这是可复查轴向宽度，不是唯一湾口/航道宽度。

平原619,136、台面193,088、山地高地2,459,328 blocks²是8格点网掩膜的面积估计，不是逐列精确地貌面积。平原目标在岸边，最近低坡分量seed距离16格；文件明确记录这种选择。岛体575,385 blocks²为逐列陆柱计数；外围水面和其它触边分量的面积仅限ROI。不要用mask外包矩形或分量面积替代未定义的完整对象面积。

WORLD_SURFACE 与过滤后表面分开存储。洞口极低值、树冠、冰及水柱均保留；高度代理不是原始裸地。水拓扑基于真实方块水区间四邻相交，biome 单列，未推断流向。规则范围和哨兵值详见 schema。

八目标均记录 `anthropogenic_contamination=possible`：存在 Waystone 等非纯地质对象及部分候选材料，生成/玩家来源未能确定。Terralith 明示天然 stone_slab 与 dirt_path 规则，不能以这些材料直接认定人类改造；也不能反过来证明全部自然。保留其位置及原始表面，未发现足以推翻宏观形态判断的大范围改造证据；小规模或天然材料修改仍可能漏检。地下 chest/spawner 和 sculk 另行保留，不自动称作人类建筑。

## 只读与验证

[world-write-audit](validation/world-write-audit.json)、[最终独立读取审计](validation/final-read-audit.json)：**world writes = 0**。目标世界1,524个文件、6,658,996,007 bytes，完整 inventory / SHA256 / size / mtime 在首次、追加和最终审计间一致。V1的47个文件也完全一致，并检查与基线 Git 内容无差异。

读取期间对所有已有源文件持有 Win32 `GENERIC_READ / FILE_SHARE_READ` 句柄，拒绝写入与删除；前后全清单补充检测文件新增/删除。没有加载Minecraft、执行器、Bridge或修改正式环境。最终独立复核178柱（随机、水、冰、最低/最高），使用独立单索引palette解码及自顶向下竖扫，验证表面、过滤后高度、实际水顶/完整水区间和biome。

[delivery-checks](validation/delivery-checks.json) 验证数据库完整性、八个assessment、字典/区块/样本引用、分辨率与数组坐标、逐列ROI覆盖。8个解码/拓扑单元测试包含跨long填充、signed long、对角水、不同水位、冰下水、单柱干桥、岛内池塘与开放凹岸。

`in_game_visual_review = BLOCKED_BY_SAFE_ENVIRONMENT`。正式离线执行器会保存世界，退役 LIVE/Observation 路径未恢复；没有安全游戏内截图，不宣称完成该条件项。PNG均为离线数据派生图。

## 恢复与复现

Python 3.12.14、numpy 2.3.5、Pillow 12.3.0、nbtlib 2.0.4（实际版本见 validation/runtime-and-scope.json）。不随成果上传Mod或原始世界。运行前在自己的环境提供依赖；本轮没有安装/升级依赖。

从此NG-2目录运行（`python` 替换为可用解释器）：

```powershell
python -B tooling/Bootstrap/归档命令.py restore
python -B tooling/Bootstrap/精查命令.py views
python -B tooling/测试/精查解码拓扑测试.py
```

恢复按 manifest 指定次序二进制拼接 gzip 分片，校验分片/gzip/SQLite SHA256并运行 integrity_check；已存在数据库则拒绝覆盖。归档前已做完整恢复回环，不仅测试压缩包能打开。

仅在持有同一原始快照且可以取得只读锁时，才可重跑源审计：

```powershell
python -B tooling/Bootstrap/精查命令.py audit --world 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/建筑师'
```

完整重采样顺序为 `scan --world ...` → `derive` → `audit --world ...` → `finalize` → `views` → `归档命令.py pack`。`derive/finalize` 会重建本轮派生成果，不能对已接受证据原位运行并当作新版本。`scan` 会拒绝源世界/V1与首轮指纹不一致。Windows只读保护和默认字体路径是已知宿主约束；Bootstrap中的本机 nbtlib 备用路径不是依赖锁，优先使用调用环境依赖。

工具内部 L3 → L2 → L1 → L0；Bootstrap和测试为工程外围。后续独立审核入口为 [COMPLETION.md](../../../tasks/NG-002/COMPLETION.md)。
