# NG-002｜Representative Local Refinement

状态：**AUTHORIZED / DISPATCH READY**

Owner 授权日期：2026-09-09

目标：在不修改 Minecraft 存档的前提下，对 Natural Geography Survey V1 的八类代表性候选地点做局部高分辨率精查，验证或推翻 V1 粗粒度地貌识别，为 NG-3 Natural Atlas Consolidation 提供可靠证据。

## 0. 必读入口

执行前最小读取顺序：

1. `minecraft/建筑师/AGENTS.md`
2. `minecraft/建筑师/current/项目状态.md`
3. `minecraft/建筑师/current/开发路线.md`
4. `minecraft/建筑师/architecture/地理事实层与空间ID契约.md`
5. `minecraft/建筑师/research/natural-geography/V1/README.md`
6. `minecraft/建筑师/research/natural-geography/V1/survey/sites/SITE.jsonl`
7. 本任务包

V1 是 immutable evidence baseline。本任务不得原位改写 `research/natural-geography/V1/` 的调查文件、脚本、manifest、SQLite 归档、JSONL 或 validation evidence。

---

# 1. 核心边界

## 严格只读

本任务：

**world writes = 0**

禁止：

- 放置/删除方块；
- 修改实体、玩家数据、区块、NBT、region、level.dat；
- WorldEdit 写入；
- 为观察而自动保存世界；
- 在游戏内放置标记柱或其它调查标识；
- 安装、升级、替换 Mod / Bridge / Observation 环境来强行满足视觉复核。

继续使用 V1 级别或更强的只读保护与前后指纹验证。若无法保证源世界不被写入，停止并报告 BLOCKED。

## 不进入世界观与建筑规划

本轮只回答“这些自然地貌候选实际上是什么”。

禁止：

- 创建国家、文明、宗教、历史、地名、政治边界；
- 把 biome 映射成种族/文化；
- 选择首都、堡垒、城市、港口；
- 生成建筑设计或蓝图；
- 把 SITE potential 当作建造授权。

---

# 2. 固定精查对象

本轮固定精查以下八个 V1 SITE。它们只是待验证假说，不是已确认地貌：

| Target | V1 type | Representative | 本轮主要验证问题 |
|---|---|---|---|
| `SITE-002` | mountain_pass_candidate | X=-5688, Y≈614, Z=-1592 | 是否真的存在可定义为山口/鞍部的低通道，而非单点高差假象 |
| `SITE-005` | broad_valley_candidate | X=-3000, Y≈101, Z=-5496 | 是否存在连续宽谷、谷壁和纵向通道 |
| `SITE-015` | plains_candidate | X=-824, Y≈63, Z=-3384 | 平坦区的真实面积、坡度、边缘与水体关系 |
| `SITE-014` | plateau_candidate | X=-4792, Y≈192, Z=-952 | 是否为有连续台面和明显边缘的高原/台地 |
| `SITE-017` | mountains_candidate | X=2760, Y≈329, Z=-1848 | 是否属于连续山体/山地，而非阈值造成的碎片分类 |
| `SITE-019` | inland_water_body_candidate | X=1096, Y≈62, Z=-1208 | 水体真实形状、连通性，以及是否应重分类为河道/湖泊/其它 |
| `SITE-003` | island_candidate | X=-248, Y≈72, Z=2056 | 是否存在被连续水域包围的真实岛体，以及岛体尺度/岸线 |
| `SITE-011` | coastal_bay_candidate | X=-312, Y≈62, Z=-4024 | 是否存在真实海湾凹入形态及与外海的连续连接 |

除非发现某个目标因世界数据缺失、边界截断或明显已被人工改造而无法判断，不要替换目标。无法判断时保留该 target，并输出 `INSUFFICIENT` 及证据。

---

# 3. 调查方法

不要简单把 V1 的 64 格采样缩成另一个固定网格后宣布完成。

采用 **局部多分辨率 / adaptive refinement**：

1. 先确定每个 target 足以覆盖其周边地貌关系的 ROI；
2. 对 ROI 做较密集地形、水体、biome 与表面材料读取；
3. 关键地貌边界、鞍部、岸线、谷底、台地边缘等区域继续细化；
4. 最终关键判定的有效采样间距原则上不得粗于 8 blocks；必要时使用 4 blocks 或逐列/逐块拓扑检查；
5. 对水体拓扑、岛屿包围关系、海湾开口、山口鞍部等不能靠插值猜测的对象，应读取足够的真实 chunk/block 数据确认。

ROI 尺寸由实际地貌决定，不强行固定 512/768/1024。必须记录每个 ROI bounds、分辨率层级、实际读取量与为何足以支持结论。

## 3.1 山口

至少验证：

- 鞍部是否真实存在；
- 两侧/相对方向是否存在更高地形；
- 低通道是否具有连续可穿越走廊，而不是一个孤立低点；
- 地形断面至少包含沿通道与横跨山脊的代表性 profile。

## 3.2 宽谷

至少验证：

- 谷底连续性；
- 两侧高地/谷壁关系；
- 谷底宽度变化；
- 是否存在河流/水体伴生；
- 纵向与横向 profile。

## 3.3 平原

至少验证：

- 连续低坡区域真实面积；
- relief / slope 分布；
- 周边丘陵、山地、水岸等边界；
- V1 单 cell 是否代表更大平坦区。

## 3.4 高原/台地

至少验证：

- 台面是否连续；
- 台面内部坡度；
- 相对周边高差；
- 是否存在明显 plateau edge / escarpment。

## 3.5 山地

至少验证：

- 是否形成连续山体/山带；
- 主峰/山脊/谷槽的大致结构；
- V1 `mountains_candidate` 的空间连续性是否可信。

## 3.6 内陆水体

至少验证：

- 实际水方块连通性；
- 岸线；
- 是否闭合；
- 是否与更大水系连接；
- `river` biome 与实际水体形态必须分开判断；
- 不推断流向，除非存在足够 block-level 证据。

## 3.7 岛屿

必须用真实水/陆拓扑确认“被水包围”，不能只依赖 64 格邻接或 biome。

记录：

- 岛体边界；
- 面积/尺度；
- 最高点；
- 岸线主要形态；
- 周围水体类型与开阔程度。

## 3.8 海湾

至少验证：

- 岸线是否真实向陆地凹入；
- 是否与外海连续；
- 开口方向和大致宽度；
- 湾内与湾口地形关系。

不要把“单个海水 cell 三面邻陆”直接等价为海湾。

---

# 4. 人工改造污染

`建筑师` 是实际游戏存档，不得假设地表完全自然。

局部精查时对每个 target 增加：

`anthropogenic_contamination = none / possible / likely / confirmed`

并记录证据。

如果发现建筑、道路、挖填方等可能改变自然地形：

- 不要自动删除或忽略；
- 不要把人工表面当成原始自然地貌；
- 若无法恢复自然地形含义，结论应降级或标记 `INSUFFICIENT`。

本轮不建立完整人工设施地图。

---

# 5. 结构化成果

所有新成果进入：

`minecraft/建筑师/research/natural-geography/NG-2/`

建议结构：

```text
NG-2/
├─ README.md
├─ manifest/
├─ raw-or-queryable/
├─ assessments/
├─ profiles/
├─ visual/
├─ validation/
└─ tooling/
```

可根据实现调整，但必须满足：

> **机器可查询事实层优先，Markdown / PNG 是派生阅读视图。**

不得把主要结果只保存成八篇 Markdown。

## Target Assessment Contract

每个 target 至少输出机器可读字段：

```text
target_id
v1_type
v1_source_object
roi_bounds
sampling_method
resolution_levels
observed_evidence
refined_metrics
water_topology
anthropogenic_contamination
verdict
refined_type
confidence
limitations
provenance
```

`verdict` 只能使用：

- `CONFIRMED`
- `RECLASSIFIED`
- `REJECTED`
- `INSUFFICIENT`

其中：

- CONFIRMED = V1 类型在局部高分辨率下成立；
- RECLASSIFIED = 有明确更合适的自然地貌类型；
- REJECTED = V1 候选由粗采样/阈值造成，不成立；
- INSUFFICIENT = 当前只读数据仍不足以可靠判断。

不要为了提高“通过率”避免 REJECTED。

---

# 6. V1 ID 与证据链

V1 的 `SITE-xxx / GEO-xxx / HYD-xxx / FEAT-xxx` 是历史 survey ID。

本轮：

- 不重新编号 V1 对象；
- 不原位修改 V1 JSONL；
- 所有精查结论以 `target_id` / `v1_source_object` 回链；
- NG-2 可以建立自己的内部 refinement object ID，但必须记录来源；
- NG-3 才决定哪些对象进入 consolidatd Natural Atlas。

因此 NG-2 的 CONFIRMED 仍不等于 World Canon。

---

# 7. 可视化

每个 target 至少生成足以人工检查的局部阅读视图，按地貌适配选择：

- high-resolution local heightmap；
- water / shoreline map；
- biome/context map；
- contour / slope / relief map；
- terrain profiles；
- target + V1 cell overlay；
- refined boundary overlay。

另外生成一份八个 target 的 comparison overview。

可视化必须标注：

- north / coordinate orientation；
- ROI bounds；
- scale / sampling resolution；
- V1 target point；
- refined feature boundary（若已建立）。

图片仍不是 Source of Truth。

---

# 8. 安全视觉复核

如果当前已有 Observation 能力能够在**不安装/更新 Mod、不修改世界、不触发保存、不改变正式环境**的条件下使用，可以对八个 target 中最关键的 3–5 个进行 scene / screenshot 视觉复核。

优先：

- mountain pass；
- broad valley；
- island / bay；
- 一个 plains 或 mountain target。

如果安全条件不满足：

- 不要为了完成任务强行恢复/替换 Observation；
- 记录 `in_game_visual_review = BLOCKED_BY_SAFE_ENVIRONMENT`；
- Offline local refinement 仍可独立完成；
- 不得谎称已做游戏内复核。

---

# 9. 验证要求

至少包括：

1. 对高分辨率样本做独立 raw chunk / vertical scan cross-check；
2. 水体判断必须来自真实 block state，不以 biome 代替；
3. queryable store 做 integrity check；
4. 所有 target 有 assessment；
5. 机器可读 assessment 能追溯到源 region / chunk / sample；
6. 图与结构化结果的 bounds / orientation 一致；
7. 任务前后目标世界全文件 inventory / SHA256 / size / mtime 一致，或使用等价且不弱于 V1 的强证明；
8. `world writes = 0`。

如果世界在调查期间被其它程序修改，不能继续使用前后不一致的数据宣布完成。

---

# 10. Completion / Push

完成后：

1. 在 `minecraft/建筑师/tasks/NG-002/COMPLETION.md` 写真实 Completion Report；
2. 新调查成果全部进入 `research/natural-geography/NG-2/`；
3. 不修改 `world/`、`builds/`；
4. 不自行进入 NG-3；
5. 更新任何 current 状态前，只能记录客观“NG-2 implementation completed / awaiting independent review”，不得自行宣布 Stage PASS；
6. commit + push 到 `zhangchenjia21-dot/assets/main`；
7. 推送后核对远端 commit；
8. 把 commit 与关键成果路径交给 Owner / GPT 独立审核。

---

# 11. Acceptance Matrix

NG-002 的核心完成条件：

- [ ] 八个固定 target 全部完成局部高分辨率调查；
- [ ] 每个 target 有机器可读 assessment 与明确 verdict；
- [ ] 关键判断有效分辨率 ≤ 8 blocks，拓扑问题在必要处使用更精细真实 block/chunk 读取；
- [ ] 山口/宽谷至少有纵横 profile；
- [ ] island / bay / inland water 使用真实水陆连通性验证；
- [ ] 人工改造污染有显式判断；
- [ ] queryable refinement store 可重新读取；
- [ ] 视觉派生图完整且有坐标/尺度；
- [ ] sample / biome / water / database 等验证通过；
- [ ] V1 evidence 未被改写；
- [ ] world writes = 0 且有可审计证据；
- [ ] Completion Report 与远端 push 完成；
- [ ] 未偷渡 World Canon、Architecture Bible 或 Build Planning。

游戏内视觉复核为条件性项：安全环境不可用时允许如实 BLOCKED，不因此伪造 PASS。
