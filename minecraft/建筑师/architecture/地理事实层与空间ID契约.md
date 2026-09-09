# 地理事实层与空间 ID 契约

## 1. Source of Truth

自然地理原始事实源：Minecraft 存档 `建筑师`。

仓库中的 Survey SQLite 是某次已接受调查对该世界的结构化快照 / 索引。存档发生变化后，旧 Survey 仍是历史证据，但不能自动代表最新世界状态。

当前已接受 baseline：

`../research/natural-geography/V1/survey/raw/geography.sqlite.gz`

解压后 SQLite 是 V1 的主要查询层；`atlas/*.jsonl`、`sites/*.jsonl`、`reports/*`、`visual/*` 为派生或导出视图。

## 2. Evidence Levels

### Observed

直接来自世界 / region / chunk / block / biome / heightmap 的观测与 provenance。

### Derived

基于 Observed 的 cell、slope、roughness、terrain class、连通分量、adjacency 等。

### Interpretive

SITE / terrain potential 等规划线索。

任何查询结果都应尽可能保留证据层级，禁止把 Interpretive 伪装成 Observed。

## 3. Current Spatial IDs

V1 已使用：

- `GEO-xxx`：自然地形连通候选区；
- `HYD-xxx`：水体 / 水系候选；
- `FEAT-xxx`：特殊自然地貌候选；
- `SITE-xxx`：值得局部复核的规划候选点。

这些 ID 是机器索引，不是地名。

V1 增量算法会在同类对象成员 Jaccard overlap ≥ 0.35 时尽量复用 ID；旧对象可 inactive，号码不回收。跨算法 / 跨采样精度升级不保证所有 ID 永久稳定，因此在局部复核前不要把重大 World Canon 永久绑定到未经验证的 provisional ID。

未来人文地理 / 聚落 / 建筑 ID 在相应阶段再正式定义，不提前制造空 Canon。

## 4. Coordinate Contract

- 坐标使用 Overworld block X / Y / Z；
- bounds 为闭区间；
- 64-block cell 的 gx / gz 使用数学 floor；
- 非矩形对象必须读取 members，不得用 bounds 假装完整覆盖；
- representative coordinate 是观察入口，不等于对象唯一中心或最佳建筑点。

## 5. Query Rule for Planning

大尺度问题可以使用 V1 coarse baseline。

具体规划必须逐步缩小：

```text
world / GEO query
→ candidate FEAT / SITE
→ local high-resolution terrain query
→ safe visual / scene observation
→ design decision
```

不得从 `SITE potential` 一步跳到 world write。
