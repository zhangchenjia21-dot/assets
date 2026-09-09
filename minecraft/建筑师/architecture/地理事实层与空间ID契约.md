# 地理事实层与空间 ID 契约

## 1. Source of Truth

自然地理原始事实源：Minecraft 存档 `建筑师`。

仓库中的 Survey / Refinement / Atlas 是对某个 terrain snapshot 的结构化证据与索引。存档发生变化后，旧成果仍是历史证据，但不能自动代表最新世界状态。

当前已接受 coarse baseline：

`../research/natural-geography/V1/survey/raw/geography.sqlite.gz`

当前已接受 local calibration evidence：

`../research/natural-geography/NG-2/`

当前已接受 **Current Natural Atlas planning baseline**：

`../research/natural-geography/NG-3/raw-or-queryable/atlas.sqlite`

Accepted NG-3 snapshot：

`57d392dcb6f3052fc72be039748529c4df3e6cf9`

Independent Review：

`../research/natural-geography/NG-3/独立审核.md`

以后宏观自然地理查询默认优先使用 Current Natural Atlas；需要验证来源、局部精度或最新世界状态时，再沿 lineage 回溯 NG-2、V1 或原世界。

## 2. Evidence Levels

### Observed

直接来自 world / region / chunk / block / biome / heightmap 的观测与 provenance。

### Derived

基于 Observed 的 cell、slope、roughness、terrain class、连通分量、adjacency 等。

### Interpretive

SITE / terrain potential / local morphology interpretation 等规划线索。

### Consolidated Atlas

由已接受 Observed / Derived / calibrated Interpretive evidence 收敛出的长期自然地理索引。

Current Natural Atlas 回答：

> “当前已接受的自然地理证据，在声明尺度与 uncertainty 下支持什么？”

它不回答：

- 世界内的人如何给这些地方命名；
- 属于哪个国家 / 文明；
- 发生过什么历史；
- 是否应该在此建城 / 建堡；
- 精确施工边界在哪里。

因此 **Consolidated Atlas 不是 World Canon，也不是 Build Authority**。

任何查询结果必须保留 evidence status / uncertainty / lineage，禁止把 Consolidated interpretation 伪装成 Observed。

## 3. Survey Spatial IDs

V1 历史 ID：

- `GEO-xxx`：自然地形连通候选区；
- `HYD-xxx`：水体 / 水系候选；
- `FEAT-xxx`：特殊自然地貌候选；
- `SITE-xxx`：值得局部复核的规划候选点。

这些是**历史 survey identity**，不是地名，也不承担长期 Atlas identity。

V1 增量算法会在同类对象成员 Jaccard overlap ≥ 0.35 时尽量复用 ID；旧对象可 inactive，号码不回收。跨算法 / 跨采样精度升级不保证所有 ID 永久稳定，因此重大后续事实不得只绑定未经验证的 V1 provisional ID。

## 4. Consolidated Natural Atlas IDs

Current Atlas 使用：

- `NGEO-xxx`：Consolidated natural geographic region；
- `NHYD-xxx`：Consolidated surface-water / hydrologic object；
- `NFEAT-xxx`：Consolidated discrete natural feature；
- `NSITE-xxx`：terrain observation / planning candidate；仍不是 build authorization。

规则：

1. Survey ID 与 Atlas ID 永久区分；
2. Atlas object 必须保存 lineage 到 V1 / NG-2 / 后续 targeted evidence；
3. 一个 Atlas object 可以聚合多个 Survey object；Survey object 也可以只作为 evidence 而不被 promotion；
4. retired / superseded Atlas ID 不回收；
5. 更新 Atlas 时必须基于 membership overlap、lineage 与语义连续性明确判断 identity continuity，不得因排序变化整批重编号；
6. 拆分 / 合并使用新 ID，并保存 predecessor / successor lineage；
7. 当前工具遇到 geometry drift / retired reuse 会停止，未来迁移需要独立授权与审核。

### 4.1 Pre-review artifact status 与 Current Authority

NG-003 交付时 67 个对象内部均保存 `status=PROPOSED`。独立审核后，`57d392d...` 整体快照已被接受为 **Current Natural Atlas planning baseline**。

为保持已验证的 SQLite / JSONL / ID ledger 和 byte-identical rebuild 证据，本项目不原位重写这批 artifact state。

因此必须区分：

- `status=PROPOSED`：该对象在 NG-003 交付生成时的历史 artifact state；
- `evidence_status=SUPPORTED / PROVISIONAL`：对象当前仍有效的证据等级；
- `current authority`：由 `current/项目状态.md`、本 architecture contract 与独立审核声明整个 `57d392d...` snapshot 是否为当前规划基线。

以后不可因为对象 JSON 中仍写 `PROPOSED` 就忽略 Current Atlas，也不可因为整个 Atlas 被接受就把 PROVISIONAL 对象当成精确事实。

未来人文地理 / 聚落 / 建筑 ID 在对应阶段再定义，不提前制造空 Canon。

## 5. Coordinate / Geometry Contract

- 坐标使用 Overworld block X / Y / Z；
- bounds 为闭区间；
- 64-block cell 的 gx / gz 使用数学 floor；
- 非矩形对象必须读取真实 indexed members / geometry runs，不得用 bounds 假装完整覆盖；
- representative coordinate 是观察入口，不等于对象唯一中心或最佳建筑点；
- coordinate lookup 必须显式区分 membership / nearby relation / uncertainty；
- `nearby` 不等于 `contains`；
- coarse 64-block regional footprint 与 NG-2 1-block / 8-block local mask 必须保留不同 geometry semantics。

Current Atlas 已验证 query layer 使用 geometry runs 的实际 indexed members 计算命中与距离，不使用 bbox / centroid 替代 footprint。

## 6. Evidence Status / Uncertainty Contract

Current Atlas 对象可使用：

- `SUPPORTED`
- `PROVISIONAL`
- 后续版本需要时可显式加入 `UNRESOLVED`

`SUPPORTED` 只表示：

> 在对象声明的尺度和语义上已有较强证据。

它**不表示**：

- 精确边界已逐块验证；
- object 内每一个位置都具有同样性质；
- 适合直接施工；
- 已成为 World Canon。

`requires_refinement=true` 必须被后续规划尊重。

Current NG-3 中 67 个对象有 18 SUPPORTED / 49 PROVISIONAL，65 个对象仍需 refinement；另保留 248 land cells + 676 water cells 未归并。`UNRESOLVED object count = 0` 不表示没有未知。

## 7. Hydrology Contract

当前 NHYD 只提供足以支持宏观规划的表层水域索引。

默认规则：

- `flow_direction = unknown`；
- watershed / upstream / downstream / discharge / source = unknown；
- biome 不能代替 water connectivity；
- coarse sampled water component 不自动等于真实完整连通水体；
- natural harbor / navigability 不自动建立；
- `connected_to` 关系只有存在直接足够 topology evidence 时才可建立。

Current Atlas 中大部分 NHYD 保持 PROVISIONAL；只有 NG-2 actual 1-block water component 在各自 ROI 内拥有更强 topology evidence。ROI 外 continuation 仍未知。

## 8. Query Rule for Planning

宏观查询默认：

```text
Current Natural Atlas
→ coordinate / context
→ NGEO / NHYD / NFEAT / NSITE
→ lineage / evidence_status / uncertainty
```

具体规划必须继续缩小：

```text
Current Natural Atlas / world-scale query
→ candidate region / feature / NSITE
→ local high-resolution terrain query
→ safe visual / scene observation（条件允许时）
→ Canon / Architecture context
→ design decision
```

不得从：

- `NSITE planning_potential`
- coarse NGEO boundary
- coarse NHYD relation

一步跳到 world write。

Current Atlas `context` 的设计契约必须保持：

- `world_write_authorized = false`
- `design_or_canon_generated = false`

## 9. Freshness Rule

任何 Atlas 都绑定一个 Minecraft terrain snapshot。

Current NG-3 最后 accepted freshness 状态：

`CURRENT_MATCH`

但它只代表 `checked_at` 时点。

如果当前 Overworld region inventory / SHA256 与 Atlas evidence snapshot 不再一致：

- 当前 Atlas 降为 historical/stale evidence；
- 不得静默宣称仍代表 current world；
- 通过 targeted refresh / survey update 显式更新 provenance；
- 需要时重新评估 geometry identity continuity；
- 玩家位置、游戏时间等非 terrain 元数据变化不应被误当成 terrain change。

## 10. World Building Boundary

Natural Atlas 独立验收完成后，才允许进入 Human Geography / World Building 的下一阶段讨论。

推荐顺序：

```text
Global / non-spatial Canon
→ Human Geography hypotheses informed by Current Natural Atlas
→ Owner review / approval
→ spatial World Canon
```

Atlas 可以约束文明发展的可能性，但不能自动生成文明结论。

例如允许：

> “该 NGEO 为高山主体，可能形成交通阻隔与山口依赖。”

不允许未经 Owner promotion 直接写：

> “这里就是矮人王国。”
