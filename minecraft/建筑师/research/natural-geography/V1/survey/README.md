# 建筑师 · Natural Geography Survey V1

独立只读调查目录。事实源是既有存档；本目录的 SQLite 是调查事实与推导结果的权威存储。JSONL、地图和短报告均可由它重新生成，不要手工维护副本。

## 入口

- `manifest/survey.json`：当前运行的范围、版本、覆盖率、限制及状态。
- `raw/geography.sqlite`：可查询结构化事实层（schema 1）。
- `atlas/GEO.jsonl`、`HYD.jsonl`、`FEAT.jsonl`、`adjacency.jsonl`：派生语义索引。
- `sites/SITE.jsonl`：自然空间潜力候选，不是 Canon。
- `reports/summary.md`：派生短报告。
- `visual/`：北为 -Z、右为 +X 的总览图；不是事实源。
- `manifest/source-before.json`、`source-after.json`、`write-audit.json`：全存档内容哈希、大小、修改时间与文件清单证据。

## 运行

工作目录为本目录，使用现有 Python 与已安装 nbtlib 2.0.4 / numpy / Pillow，不安装或更改游戏环境。

```powershell
$surveyPython = 'C:\Users\MRVHREVO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $surveyPython -B scripts/Bootstrap/调查命令.py scan --world 'D:\Games\Minecraft\.minecraft\versions\26.2-Fabric 0.19.5\saves\建筑师'
& $surveyPython -B scripts/Bootstrap/调查命令.py views
& $surveyPython -B scripts/测试/存档解码测试.py
& $surveyPython -B scripts/测试/调查交付验证.py
```

`scan` 只接受已存在且 LevelName 正确的 DataVersion 4903 世界，不创建世界。Windows 只读共享句柄拒绝源文件写入/删除；不能取得时停止，不关停游戏。所有 Python 文件禁止字节码落到依赖目录。`views` 不访问世界。

增量扫描重新检查全部 header，并以 region SHA256 与算法版本决定是否复用原始采样。推导图谱重新生成；同类对象与旧成员集合 Jaccard 重叠 ≥0.35 时复用 ID，拆分/合并可能产生新 ID，旧对象保留 inactive，不重用号码。升级解码或采样规则时必须修改 ALGORITHM。V1 不保证跨精度升级自动保持所有 ID。

`reports/incremental-validation.json` 保存一次真实缓存重跑的样本、活动对象成员 ID 与邻接表一致性结果。`scripts/测试/增量复用测试.py capture` / `verify` 用于后续重复该检查。`manifest/toolchain.json` 保存工具源码哈希与实际运行依赖版本。

## 数据契约

所有坐标是主世界方块 X/Y/Z；bounds 闭区间。样本以绝对 X/Z 作主键；chunks 以有符号 chunk X/Z 作主键。64 格 cell 的 gx/gz 是数学 floor 除法，负数不可截断取整。cell 只代表抽样外推范围，不能据此声称整格已实测。

| 表 | 证据层级 | 用途 |
|---|---|---|
| regions | Observed | 来源地形 region 路径与 SHA256 |
| chunks | Observed + Derived component | header 存在性、扇区、时间戳、连通分量 |
| chunk_status | Observed | 所有 header 区块的真实 Status / DataVersion，full 与未完成生成状态分离 |
| samples | Observed + 显式植被过滤结果 | observed JSON 包含坐标、WORLD_SURFACE/OCEAN_FLOOR/MOTION_BLOCKING_NO_LEAVES、表面方块、biome、水面方块；exposed_y 是过滤结果 |
| cells | Derived | 五柱聚合、邻域高差、斜率代理、粗糙度、地形类别与 GEO |
| objects | Derived / Interpretive | GEO/HYD/FEAT/SITE，confidence 为启发式值，不是概率 |
| members | Derived | 精确的成员 cell，bounds 不能替代非矩形成员关系 |
| adjacency | Derived | GEO 间四邻域共享边，边无方向 |
| meta | Provenance | schema、算法、存档绑定、manifest |

`surface_y` 是 heightmap 的最高非空气方块 Y（存储值减一并加 min_y）。`ocean_floor_y` 是 Minecraft OCEAN_FLOOR，不是剥离所有树木的地质基岩。biome 是该柱 WORLD_SURFACE 高度的 4×4×4 biome 单元。`water` 由去显式植被后的方块名读取；不含冰、岩浆与隐藏洞穴水，waterlogged 非水方块未计入。

## 查询示例

推荐 `sqlite3.connect(Path(...).as_uri() + '?mode=ro', uri=True)`，结果中始终保留证据层级。图谱只覆盖已采样的主世界。

```sql
-- 给定坐标先在应用侧计算 cx=floor(x/16)、gx=floor(x/64)，z 同理。
SELECT * FROM chunks WHERE cx=:cx AND cz=:cz;
SELECT geo_id,terrain,elevation,observed FROM cells WHERE gx=:gx AND gz=:gz;
SELECT o.id,o.type,o.confidence,o.details FROM members m JOIN objects o USING(id)
WHERE m.gx=:gx AND m.gz=:gz AND o.active=1;
-- GEO 邻接
SELECT * FROM adjacency WHERE a=:geo OR b=:geo;
-- 平坦候选与显著高差
SELECT x,z,geo_id,slope,relief FROM cells WHERE terrain='plains_candidate' ORDER BY slope LIMIT 20;
SELECT x,z,geo_id,relief FROM cells ORDER BY relief DESC LIMIT 20;
-- 给定坐标最近的采样水格；距离只是平面欧氏距离，不代表可达性
SELECT x,z,(x-:x)*(x-:x)+(z-:z)*(z-:z) AS distance2 FROM cells
WHERE water>=0.6 ORDER BY distance2 LIMIT 10;
-- 地貌候选与 SITE
SELECT id,type,confidence,details FROM objects WHERE active=1 AND family='SITE';
SELECT id,type,details FROM objects WHERE active=1 AND type LIKE '%valley%';
```

## 工程边界与校验

L0：格式位数、palette 索引与空间规则。L1：只读存档解析、SQLite、地貌计算、派生地图。L2：持句柄、指纹、覆盖、采样、验证、分析、导出顺序。L3：输入/输出路径校验与公开接口。Bootstrap 负责现有第三方库路径注入，测试属于工程外围。没有引用其他业务模块内部；复用的是已安装第三方 nbtlib。

接受条件包括：源存档前后指纹一致、固定随机点及水面/高点独立竖向扫描核对高度、独立 biome 数组展开核对、全区块状态读取器与 nbtlib 对照、SQLite integrity_check、对象成员/分类检查与派生地图检查。仅程序运行成功不代表高级地貌已验证，因此可保持 PARTIAL。
