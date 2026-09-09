# 地理事实层与空间 ID 契约

## 1. Source of Truth

自然地理原始事实源：Minecraft 存档 `建筑师`。

仓库中的 Survey SQLite 是某次已接受调查对该世界的结构化快照 / 索引。存档发生变化后，旧 Survey 仍是历史证据，但不能自动代表最新世界状态。

当前已接受 coarse baseline：

`../research/natural-geography/V1/survey/raw/geography.sqlite.gz`

解压后 SQLite 是 V1 的主要查询层；`atlas/*.jsonl`、`sites/*.jsonl`、`reports/*`、`visual/*` 为派生或导出视图。

当前已接受 local calibration evidence：

`../research/natural-geography/NG-2/`

NG-2 只证明八个固定 target 的局部事实，不把其结论外推成全世界 detector 准确率。

## 2. Evidence Levels

### Observed

直接来自世界 / region / chunk / block / biome / heightmap 的观测与 provenance。

### Derived

基于 Observed 的 cell、slope、roughness、terrain class、连通分量、adjacency 等。

### Interpretive

SITE / terrain potential 等规划线索。

### Consolidated Atlas

由已接受 Observed / Derived / calibrated Interpretive evidence 收敛出的长期自然地理索引。

Consolidated Atlas 仍然不是 World Canon：它回答“自然地理证据目前支持什么”，不回答“这个世界的人类称它什么、属于哪个国家、发生过什么历史”。

任何查询结果都应尽可能保留证据层级，禁止把 Interpretive 或 Consolidated interpretation 伪装成 Observed。

## 3. Survey Spatial IDs

V1 已使用：

- `GEO-xxx`：自然地形连通候选区；
- `HYD-xxx`：水体 / 水系候选；
- `FEAT-xxx`：特殊自然地貌候选；
- `SITE-xxx`：值得局部复核的规划候选点。

这些 ID 是**历史 survey identity**，不是地名，也不承担最终长期 Atlas identity。

V1 增量算法会在同类对象成员 Jaccard overlap ≥ 0.35 时尽量复用 ID；旧对象可 inactive，号码不回收。跨算法 / 跨采样精度升级不保证所有 ID 永久稳定，因此重大后续事实不得只绑定未经验证的 V1 provisional ID。

## 4. Consolidated Natural Atlas IDs

D-004 已为 NG-3 预留：

- `NGEO-xxx`：Consolidated natural geographic region；
- `NHYD-xxx`：Consolidated surface-water / hydrologic object；
- `NFEAT-xxx`：Consolidated discrete natural feature；
- `NSITE-xxx`：terrain observation / planning candidate；仍不是 build authorization。

规则：

1. Survey ID 与 Atlas ID 永久区分；
2. Atlas object 必须保存 lineage 到 V1 / NG-2 / 后续 targeted evidence；
3. 一个 Atlas object 可以聚合多个 Survey object；Survey object 也可以只作为 evidence 而不被 promotion；
4. rejected / superseded Atlas ID 不回收；
5. 更新 Atlas 时优先基于 membership overlap、lineage 与语义连续性保留 ID，不得因排序变化整批重编号；
6. NG-3 独立审核前，所有新 Atlas ID 都是 `PROPOSED`；审核接受后才可成为 current Natural Atlas 的稳定引用。

未来人文地理 / 聚落 / 建筑 ID 在相应阶段再定义，不提前制造空 Canon。

## 5. Coordinate Contract

- 坐标使用 Overworld block X / Y / Z；
- bounds 为闭区间；
- 64-block cell 的 gx / gz 使用数学 floor；
- 非矩形对象必须读取 members，不得用 bounds 假装完整覆盖；
- representative coordinate 是观察入口，不等于对象唯一中心或最佳建筑点；
- Consolidated Atlas 的 coordinate lookup 应显式返回 membership / nearby relation 与 uncertainty，不能只按 bbox 命中。

## 6. Query Rule for Planning

当前大尺度问题可以使用 V1 coarse baseline + NG-2 calibration。

NG-3 独立审核并 promotion 后，未来自然地理查询默认优先使用 Consolidated Atlas；需要验证来源、细节或最新世界状态时再回溯 Survey / world。

具体规划必须逐步缩小：

```text
Consolidated Natural Atlas / world-scale query
→ NGEO / NHYD / NFEAT / NSITE
→ lineage / evidence / uncertainty check
→ local high-resolution terrain query
→ safe visual / scene observation（条件允许时）
→ design decision
```

不得从 `NSITE planning_potential` 一步跳到 world write。

## 7. Freshness Rule

任何 Atlas 都绑定一个 Minecraft terrain snapshot。

如果当前 Overworld region inventory / hash 与 Atlas evidence snapshot 不再一致：

- 旧 Atlas 保留为历史证据；
- 不得静默宣称仍代表 current world；
- 应通过 targeted refresh / survey update 显式更新 provenance；
- 玩家位置、游戏时间等非 terrain 元数据变化不应被误当成地形变化。
