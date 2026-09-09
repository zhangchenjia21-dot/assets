# NG-003｜Natural Atlas Consolidation

状态：**AUTHORIZED / DISPATCH READY**

Owner 授权日期：2026-09-09

授权决策：`../../decisions/D-004_NG-3自然地理图册收敛授权.md`

目标：将 Natural Geography V1 的全局粗粒度事实层、NG-2 的局部高分辨率校准与反例，以及本轮少量必要的 targeted refinement，收敛成一套**稳定、机器可查询、可追溯、适合 Codex 后续世界规划使用的 Consolidated Natural Atlas**。

本任务不是 World Building，也不是建筑规划。

---

# 0. 必读入口

执行前最小读取顺序：

1. `minecraft/建筑师/AGENTS.md`
2. `minecraft/建筑师/current/项目状态.md`
3. `minecraft/建筑师/current/开发路线.md`
4. `minecraft/建筑师/architecture/地理事实层与空间ID契约.md`
5. `minecraft/建筑师/decisions/D-004_NG-3自然地理图册收敛授权.md`
6. `minecraft/建筑师/research/natural-geography/V1/README.md`
7. `minecraft/建筑师/research/natural-geography/NG-2/README.md`
8. `minecraft/建筑师/research/natural-geography/NG-2/独立审核.md`
9. 本 Task Packet

V1 与 NG-2 都是 immutable evidence。不得原位修改其任何调查、assessment、SQLite 归档、脚本、manifest、JSON/JSONL、validation 或 review 文件。

---

# 1. 核心目标

NG-3 要解决的是 V1 目前存在的结构性问题：

- V1 有 1,264 个 GEO、412 个 HYD、1,343 个 FEAT，主要是粗阈值 + 64-block 连通分量，过于碎片化，不适合作为长期世界规划对象；
- V1 的对象 ID 是 survey identity，不应直接被未来几十次建筑规划当成永久 Canonical Geography ID；
- NG-2 已证明不同 detector 的可靠性不相同：有些粗分类在局部成立，有些需要重分类；
- 后续 Codex 需要的是“这个坐标处于什么自然区域、周围是什么、与哪些水体/地貌相邻、这个判断有多可靠、证据来自哪里”，而不是再次阅读海量调查文件。

因此 NG-3 应建立：

> **Global coarse evidence → calibrated interpretation → consolidated geography objects → stable query layer**

最终成果必须优先服务后续 Codex 查询与规划，而不是人类阅读。

---

# 2. 严格边界

## 2.1 只读 Minecraft 世界

本任务：

**world writes = 0**

禁止：

- 放置、删除或替换方块；
- 修改区块、实体、玩家、NBT、region、level.dat；
- WorldEdit 写入；
- 为观察启动会保存世界的 Minecraft / executor / Bridge；
- 为完成任务安装、升级或恢复游戏 Observation 环境；
- 在世界中放置调查标记。

如果需要新增 targeted refinement，只允许离线、只读读取真实 world 数据，并必须使用不弱于 NG-2 的只读保护与前后地理源文件指纹校验。

## 2.2 不进入 World Canon

禁止：

- 创造国家、文明、种族分布、宗教、历史、政治边界；
- 给自然地理对象创造正式世界内地名；
- 用 biome 一对一推导文化；
- 规划首都、城堡、港口、村庄或道路；
- 生成建筑设计、蓝图或 world-write task。

自然 Atlas 中允许使用机器描述标签，例如 `western_high_mountain_massif`、`low_relief_coastal_plain`，但这些是**描述性 machine label**，不是 World Canon 地名。

---

# 3. Current-world freshness / provenance gate

在生成 Atlas 前，先检查当前 `建筑师` 存档与已接受调查快照的关系。

重点比较自然地理真正依赖的 Overworld region 数据，而不是把玩家位置、游戏时间等无关元数据变化误判为地形失效。

至少记录：

- 当前 LevelName / DataVersion；
- `dimensions/minecraft/overworld/region/` inventory；
- region 文件 hash 与 NG-2/V1 已保存 snapshot 的一致性；
- 是否存在新增、删除或改变的 Overworld region；
- `geography_snapshot_status`：
  - `CURRENT_MATCH`
  - `TERRAIN_CHANGED`
  - `UNVERIFIABLE`

若地形 region 已变化：

- 不得静默把旧 V1/NG-2 当成当前事实；
- 可以输出 historical/proposed atlas，但必须明确标记 stale；
- 不得宣称得到 current Natural Atlas；
- Completion 应返回需要重新 survey / targeted refresh 的证据。

若一致，则继续。

---

# 4. Evidence calibration：必须吸收 NG-2，而不是只读取 V1

建立明确的 `calibration` 数据层，至少把 NG-2 八个结果转化为对 V1 detector / semantics 的使用规则。

不得把“6/8 confirmed”解释成全局 75% 准确率。

至少保留以下已审核边界：

- **mountain / continuous massif**：大型连续高地在宏观尺度可作为较强 regional evidence；但 Y 阈值不等于最终山地边界；
- **mountain_pass_candidate**：只能作为“值得局部验证的 saddle/pass hypothesis”，不得从 V1 直接 promotion；
- **broad_valley_candidate**：已有明确 false-positive / reclassification 证据，不能仅凭 V1 valley threshold 直接建立 consolidated valley；
- **plains_candidate**：可用于寻找低起伏区，但代表点可能位于岸线或边缘，必须以更大连片关系理解；
- **plateau_candidate**：可支持局部 bench/tableland hypothesis，但完整边界可能开放；
- **inland_water_body_candidate**：粗网格可能把展宽河道误判成独立湖体；封闭性必须谨慎；
- **island_candidate**：只有真实水陆拓扑证据才能 promotion 为 confirmed island；
- **coastal_bay_candidate**：可以形成 coastal embayment，但不得自动推导 natural harbor、唯一湾口或可航行性。

输出机器可读 calibration rules / warnings，供后续 Atlas update 与 Codex 查询显示。

---

# 5. Consolidated Atlas identity

V1 历史 ID：

`GEO-xxx / HYD-xxx / FEAT-xxx / SITE-xxx`

必须保持不变，作为 evidence lineage。

NG-3 使用新的 PROPOSED Consolidated Atlas ID：

- `NGEO-001...`：consolidated natural geographic region；
- `NHYD-001...`：consolidated surface-water / hydrologic object；
- `NFEAT-001...`：consolidated discrete natural feature；
- `NSITE-001...`：terrain observation/planning candidate；仍不是 build authorization。

## ID 原则

1. ID 与 World Canon 地名分离；
2. 所有 Atlas ID 必须有 lineage；
3. 不要求与 V1 一对一对应；一个 NGEO 可聚合多个 V1 GEO；一个 V1 对象也可被拆分/降级/仅作为 evidence；
4. rejected / superseded ID 不回收；
5. Atlas 更新必须设计稳定 matching / lineage strategy，避免每次运行全部重编号；
6. 本轮在独立审核前所有新 ID 状态均为 `PROPOSED`。

---

# 6. NGEO｜宏观自然地理区域收敛

目标是把 V1 过度碎片化的 terrain cells / GEO component 收敛成适合长期理解的**宏观 physiographic regions**。

例如可以形成：

- mountain massif / mountain belt sector；
- highland / plateau system；
- low-relief plain；
- basin / broad depression；
- major valley corridor（仅证据充分时）；
- coastal lowland / coastal upland；
- island / archipelago region；
- 其它由真实地图支持的自然大区。

不要预设世界必须包含这些类型。

## 收敛依据

可综合使用：

- V1 cells 的 elevation / slope / relief / roughness / terrain；
- V1 members / adjacency；
- 水体作为自然边界；
- biome 作为环境 context，而不是单独分区器；
- NG-2 calibration；
- 大尺度形状 / continuity；
- 少量 targeted refinement（必要时）。

不得只以 `terrain` 字符串相同就机械合并。

## 粒度要求

最终 NGEO 应显著减少 V1 的碎片化。

不要为了达到一个固定数量而强行合并；但结果应处于“几十个可理解宏观区域”的量级，而不是继续保留上千个细碎对象。若地图真实结构导致更多对象，必须说明。

允许存在：

- `SUPPORTED`
- `PROVISIONAL`
- `UNRESOLVED`

不要为了让整张地图看起来完整而伪造明确边界。

---

# 7. NHYD｜水体与水系收敛

目标不是建立现实水文学模型，而是提供未来规划足够可靠的表层水体关系。

可以建立：

- major ocean/coastal water domain；
- large lake / inland water body（证据充分时）；
- major connected river/channel system（不强行区分河流流向）；
- strait / channel / embayment 等已支持结构；
- unresolved water relation。

必须继续保持：

- `flow_direction = unknown`，除非有直接充分证据；
- 不自动推导 watershed / upstream / downstream / discharge；
- ocean/river biome 不能代替真实水体连通；
- natural harbor 不在本阶段自动建立。

对于是否闭合、是否为岛屿外围水环、是否为重大连通水道等 Atlas-critical 关系，如果 V1 粗证据不足，可以触发 targeted refinement。

---

# 8. NFEAT｜离散自然地貌

仅 promotion 对后续世界理解有明显价值、且证据足够的离散 feature。

例如：

- verified / supported island；
- local saddle / mountain pass morphology；
- escarpment；
- coastal embayment；
- distinct plateau bench；
- dramatic headland / peninsula；
- 其它明显地貌。

不要把 V1 1,343 个 FEAT 全部照搬到 NFEAT。

每个 NFEAT 必须回答：

- 它为什么值得成为长期 Atlas 对象；
- 证据等级；
- 是否需要 future local verification；
- 与哪些 NGEO / NHYD 相关；
- lineage 到哪些 V1 / NG-2 evidence。

---

# 9. NSITE｜未来规划筛选入口

NSITE 只用于未来的“去哪里继续看”与 terrain suitability 初筛。

可以从：

- NG-2 已验证地点；
- Consolidated Atlas 中重要自然节点；
- V1 SITE 中仍有价值但未验证的候选；

建立少量长期稳定 NSITE。

每个 NSITE 必须明确：

- `evidence_status`；
- `planning_potential` 只是 terrain potential；
- `requires_local_observation`；
- `requires_world_write_authorization = true`；
- 不得写成“首都位置”“城堡位置”等世界设定结论。

---

# 10. Targeted refinement budget

NG-3 不是第二次 NG-2，也不是全世界高精扫。

只有遇到**会改变 Consolidated Atlas 大结构的 ambiguity**时，才允许新增 targeted refinement。

典型理由：

- 两个主要 NGEO 是否实际由山口/低地连通；
- 某 major water body 是封闭湖、展宽河道还是与海域连通；
- 某宏观 coastline / island relation 会改变 Atlas topology；
- 某巨大 V1 GEO fragmentation 是否只是采样噪音。

默认上限：**最多 12 个 targeted refinement targets**。

如果 12 个仍不足：

- 保留 `UNRESOLVED / PROVISIONAL`；
- 不继续无限扩扫；
- 在 Completion 中提出下一轮必要研究。

Targeted refinement 必须：

- 说明为什么 Atlas-critical；
- 记录 ROI / resolution /读取量；
- world writes = 0；
- 保存 raw/queryable evidence；
- 不覆盖 NG-2 数据。

允许 0 个 targeted refinement；如果现有 V1 + NG-2 已足够形成合理 Atlas，不要为了“做了更多工作”而强行读取。

---

# 11. 机器事实层 / Query Layer

所有新成果进入：

`minecraft/建筑师/research/natural-geography/NG-3/`

建议：

```text
NG-3/
├─ README.md
├─ manifest/
├─ calibration/
├─ raw-or-queryable/
├─ atlas/
├─ targeted-refinement/
├─ visual/
├─ validation/
└─ tooling/
```

可调整，但机器层必须是主成果。

## 11.1 推荐 Source of Truth

优先使用 SQLite 作为 Proposed Atlas 主要查询层；如果有更适合的结构可以采用，但必须说明为何更适合 Codex。

不得复制 NG-2 的 500 万根柱作为无意义重复数据。能通过 lineage 引用 V1 / NG-2 的事实应优先引用；仅存新增 targeted evidence 与 Consolidated Atlas 自己的索引/关系。

至少应表达：

### atlas_objects

- id
- family
- type
- status (`PROPOSED`)
- evidence_status
- machine_label
- summary
- bounds
- centroid / representative
- geometry / membership semantics
- confidence / confidence_semantics（如使用）

### atlas_members / cell_index

支持坐标落点查询；非矩形对象不能只用 bbox。

### relations

至少支持：

- adjacent_to
- contains / part_of（如果建立层级）
- connected_to
- associated_with
- overlaps（如需要）

### lineage

每个 Atlas 对象追溯：

- V1 GEO/HYD/FEAT/SITE；
- V1 cells / members；
- NG-2 assessment；
- NG-3 targeted evidence；
- 算法 / schema version。

### uncertainty

显式保存：

- boundary uncertainty；
- topology uncertainty；
- semantic uncertainty；
- requires_refinement。

### calibration

供以后更新与查询时解释 detector caveat。

---

# 12. Codex 查询接口

这是本任务关键交付，不要只提供 SQL 示例。

提供一个轻量、无服务依赖的查询入口，例如 Python CLI，至少支持：

```text
coordinate --x <x> --z <z>
```

返回：

- 所属/附近 NGEO；
- NHYD / NFEAT；
- 最近 NSITE；
- evidence status；
- uncertainty；
- lineage refs。

```text
object --id NGEO-xxx
```

返回完整对象与 lineage。

```text
neighbors --id NGEO-xxx
```

返回邻接/连接对象。

```text
search --family ... --type ... --evidence-status ...
```

支持未来按地貌筛选。

```text
context --x <x> --z <z> --radius <r>
```

输出一份**机器 JSON context bundle**，面向以后 Codex 建筑/聚落规划，包含区域、相邻大地貌、水体、features、候选 site、限制与证据等级。

不得在 `context` 中生成文明/建筑设计；它只是自然地理上下文装配器。

查询入口必须有 deterministic JSON output，并带 schema version。

---

# 13. 可视化

生成派生阅读视图帮助 Owner / GPT 审核：

至少：

- Consolidated NGEO map；
- NHYD / surface-water relation map；
- NFEAT / NSITE overview；
- evidence-status / uncertainty map；
- V1 → Consolidated Atlas 对照图（可简化表达）。

要求：

- 标注 X/Z 方向；
- 显示地图范围；
- stable proposed IDs；
- 不用视觉颜色差异伪装数据精度；
- 图片不是 Source of Truth。

---

# 14. Human-readable summary

README / summary 只需要回答：

1. Consolidated Atlas 一共形成多少 NGEO / NHYD / NFEAT / NSITE；
2. 世界的大尺度自然骨架是什么；
3. 哪些结论 evidence 强，哪些仍 provisional；
4. NG-2 的两个 reclassification 如何改变 Atlas；
5. 是否新增 targeted refinement；为什么；
6. 当前最大自然地理未知是什么；
7. 未来 World Building 能安全依赖哪些自然地理层级，哪些不能。

不要把 Markdown 变成另一份 100 页世界百科。

---

# 15. Validation

至少验证：

1. V1 / NG-2 文件指纹未被修改；
2. 若读取 current world，Overworld region 前后无变化；
3. `world writes = 0`；
4. Proposed Atlas store integrity check；
5. 每个 Atlas object 有 lineage；
6. 每个 Atlas object 有 evidence_status；
7. 新 Stable ID 无重复、无回收；
8. coordinate lookup 对随机点 / 边界点 / 水体点返回一致结果；
9. relations 不出现不存在对象的 dangling reference；
10. cell/member mapping 不用 bbox 替代非矩形 membership；
11. NG-2 两个 RECLASSIFIED 不得被 V1 旧类别重新静默 promotion；
12. `SITE-002` 不被升级为战略山口；
13. `SITE-011` 不被升级为 natural harbor；
14. river flow / watershed 等未证实语义没有被悄悄生成；
15. query CLI 的 `coordinate/object/neighbors/search/context` 均有自动测试；
16. 如果存储采用压缩归档，做 lossless round-trip + SHA256 + integrity check。

抽样独立检查部分 Consolidated Atlas object，确保 summary / export / maps 与机器事实层一致。

---

# 16. 完成状态语义

允许：

- `PASS-CANDIDATE / READY FOR INDEPENDENT REVIEW`
- `PARTIAL`
- `BLOCKED`

Codex 不得自行宣布 NG-3 Stage PASS。

如果 Atlas 可以完整生成但某些区域仍 uncertain：

- 不必因此把整个任务标成失败；
- 应保留 uncertainty；
- Atlas 的价值之一就是明确知道“哪里还不知道”。

---

# 17. Completion / Push

完成后：

1. 在 `minecraft/建筑师/tasks/NG-003/COMPLETION.md` 写真实 Completion Report；
2. 新成果全部进入 `research/natural-geography/NG-3/`；
3. **不要写入 `world/` 或 `builds/`**；
4. 不自行创建/更新 top-level current Atlas authority；独立审核后由 GPT 决定 promotion；
5. 只做机械更新 `current/项目状态.md` 为 implementation completed / awaiting review；
6. commit + push 到 `zhangchenjia21-dot/assets/main`；
7. 不 force-push；保留其它并行项目提交；
8. 推送后核对远端 HEAD；
9. 停止，交回 GPT 独立审核。

---

# 18. Completion Report 最小内容

必须报告：

- execution base / final commit；
- geography snapshot freshness；
- NGEO / NHYD / NFEAT / NSITE 数量；
- Atlas schema / machine store；
- stable ID strategy；
- NG-2 calibration 如何被落实；
- targeted refinement 数量与原因；
- query CLI 验证；
- uncertainty / unresolved 数量；
- V1 / NG-2 immutable evidence；
- world writes；
- validation / archive round-trip；
- 明确说明没有进入 World Canon / Architecture Bible / Build；
- 下一阶段建议，但不得自行授权。
