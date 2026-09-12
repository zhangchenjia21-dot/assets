# ARCHITECTURE_TAXONOMY — 建筑分类体系（P3 任务 1）

> 两条独立 taxonomy：**Style**（像什么）与 **Function**（怎么用）。
> 主信号：V6C2 人工+规则审核分类（`references/classification-v2/catalog-final.json`，只读）；
> 交叉验证：P1 元数据几何/材料字段。落标脚本：`scripts/build_labels.py`，
> 全量标签表见 `LABELING_NOTES.md`（123 行完整）与 `labels.jsonl`。
> 机器可读定义：`style_taxonomy.json` / `function_taxonomy.json`。

## 1. 与 V6C2 分类的继承关系

V6C2（catalog-v2/catalog-final）词表比任务书候选类更细：style 有 24 个词（含 cottage、east_asian、
european、fortified、desert、classical 等），用途分 primary_use（14 类）+ secondary_use（46 词）两层。
本 taxonomy 是**收敛映射**而非重新分类：

- **Style**：取每张蓝图 V6C2 `styles[]` 中置信度最高的 tag，按下表映射；top 置信度 < 0.55 或几何
  强冲突 → Unknown（纪律，见任务书 8.2「不确定写 UNKNOWN」）。
- **Function**：按 `primary_use` + `secondary_use` 规则映射（`build_labels.py: map_function`）。
- V6C2 的 `scale`（tiny/small/medium/large/monumental）原样保留为 size_class，供缺口矩阵使用；
  `features[]`（timber_frame/stone_base/multi_story 等几何特征）作为 style 交叉验证信号。

置信度继承 V6C2 数值：high ≥0.70 / medium 0.55–0.70 / low <0.55；几何弱支持时下调一档。
`label_basis`：existing metadata（直接继承）/ mixed（几何交叉验证参与）/ filename / geometry /
manual signal；本库未发生后三者单独提拔（V6C2 已吸收 filename 与人工复核证据）。

## 2. Style Taxonomy（7 类，含 Unknown）

| 类别 | n | 支持级别 | 定义 | 主要判定信号 | V6C2 来源 |
|---|---:|---|---|---|---|
| Rustic | 20 | SUPPORTED | 乡村/田园质朴：小尺度木屋农庄，自然材料 | top=rustic @0.8；木石主导 | rustic×20 |
| Medieval | 19 | SUPPORTED | 欧洲中世纪/防御性：木框架、石基座、坡顶 | top=medieval @0.6 或 fortified @0.8；timber_frame/stone_base | medieval×14 + fortified×5 |
| Fantasy | 10 | SUPPORTED | 奇幻：夸张体量/飞艇/非常规结构 | top=fantasy @0.7–0.9；无确定性几何校验器 | fantasy×10 |
| Japanese | 7 | PROVISIONAL | 日式：曲线屋顶、木构 | top=japanese；stair_count≥20 | japanese×7 |
| Chinese | 4 | PROVISIONAL | 中式：坡屋顶、木构 | top=chinese @0.7（0.5×3 已降级 Unknown） | chinese×7→4 |
| Other | 7 | OBSERVATION ONLY（异质集合） | european/desert/classical 零散集合，不做 grammar 泛化 | top=european/desert/classical | 4+2+1 |
| Unknown | 56 | —（非类别） | V6C2 判 unknown（51）或低置信降级（5）；景观/雕塑居多 | — | unknown×51 + 降级×5 |

**候选类中未建立**（0 样本，不硬建）：Modern / Industrial / Gothic / Victorian / Nordic。

降级记录（5 条，均 style）：chinese@0.5 ×3、japanese@0.5 ×1、desert@0.5 ×1 → Unknown。
明细见 `LABELING_NOTES.md` 降级记录表。

## 3. Function Taxonomy（15 类，含 Unknown）

| 类别 | n | 支持级别 | 定义 | V6C2 来源 |
|---|---:|---|---|---|
| Residential | 23 | SUPPORTED | 居住：house/manor/treehouse | residential×23 |
| Decoration | 22 | SUPPORTED | 景观与纪念物（树/园/亭/雕像/传送门/陵墓） | landscape×14 + landmark(statue/portal/mausoleum)×8 |
| Castle | 14 | SUPPORTED | 城堡/大型纪念建筑群（palace 并入，记录在案） | military castle/keep×8 + palace×6 |
| Tower | 13 | SUPPORTED | 塔（height_ratio≥1.65 交叉验证） | landmark tower×11 + military tower×2 |
| Religious | 10 | SUPPORTED | 宗教：church/cathedral/monastery | religious×10 |
| Workshop | 7 | PROVISIONAL | 生产/商业作坊（shop/market 零售并入，记录在案） | industrial×4 + commercial shop/market×3 |
| Vehicle | 7 | PROVISIONAL | **新增类**：载具/运输构筑（候选表无，样本支持） | transport：airship×4/ship×1/dock×2 |
| Inn | 5 | PROVISIONAL | 旅馆/酒馆 | commercial tavern×5 |
| Civic | 4 | PROVISIONAL | 公共/市政（town_hall/guildhall/school/arena） | civic×4 |
| Gate | 3 | OBSERVATION ONLY | 门楼/城墙 | military gatehouse×3 |
| Blacksmith | 3 | OBSERVATION ONLY | 铁匠铺 | blacksmith×3 |
| Farm | 3 | OBSERVATION ONLY | 农场 | agricultural farm×3 |
| Mixed-use | 2 | OBSERVATION ONLY | 混合用途 | mixed_use×2 |
| Warehouse | 1 | OBSERVATION ONLY | 仓库 | warehouse×1 |
| Unknown | 6 | —（非类别） | primary_use=unknown | unknown×6 |

**候选类中未建立**（0 样本，不硬建）：Bridge。
**新增类**：Vehicle（transport 的 ship/airship/dock 无法归入任何候选功能类，n=7 达到 PROVISIONAL，
按「样本支持的类可建」原则新增并记录；若后续并入候选体系可再映射）。

## 4. 交叉验证与 UNKNOWN 纪律

- 交叉验证只做**校验/下调**，从不从几何单独提拔标签（V6C2 为主信号）。
- Residential 校验：door_count≥1 且 estimated_floor_count≥1；Tower：size_y/max(size_x,size_z)≥1.65
  （与 V6C2 tower 规则同阈值）；Castle：stone_ratio≥0.3；Farm：decorative_ratio≥0.3；
  Medieval/Rustic：timber_frame/stone_base/steep_gable 特征或 wood+stone≥0.4；
  Japanese/Chinese：stair_count≥20（屋顶构件信号）。
- 弱支持 → 保留标签、置信度降一档、notes 记录；强冲突 → Unknown 并记录（本次全库未发生强冲突）。
- Style Unknown 56 张是纪律结果：V6C2 自身对 51 张（多为树木/雕塑/景观）给出 unknown@0.2，
  不从文件名或材料臆造风格。
