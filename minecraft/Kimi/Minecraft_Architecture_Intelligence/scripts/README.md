# scripts/ README — 模块与用法

> 项目代号 H · P0+P1 脚本集。所有脚本路径参数化，无硬编码绝对路径；
> 对参考库 `D:\Games\...` 全程只读，产出只写 `$OUT`。

## 运行环境

本机托管 venv（`daimon\runtime\python\.venv`）的基础解释器路径已失效（health.json 有记录）。
可用方式（只读挂载其 site-packages，依赖 numpy 2.4 / pandas 3.0 / scipy）：

```bash
export PYTHONPATH="D:\AI\kimi\daimon-share\daimon\runtime\python\.venv\Lib\site-packages"
py -3 <script> ...
```

## 模块一览

| 文件 | 职责 |
|---|---|
| `blueprint_io.py` | Canonical IR 加载（normalized 优先、canonical 回退并记录）、block state 字符串解析、numpy 体素化（坐标归零、显式/隐式 air 统一） |
| `walkability.py` | **核心共享模块**：Minecraft 玩家可通行近似模型。站位+净高判定、数据驱动方块分类表（BLOCK_CLASS_RULES / KNOWN_FULL_KEYWORDS）、连通图与连通分量指标。P2 Validator 复用 |
| `extract_blueprint_metadata.py` | 批量提取 6.1–6.6 全部字段 → jsonl + csv + extraction_summary.json |
| `build_manifest.py` | 从 catalog.json 生成 01_INVENTORY/BLUEPRINT_MANIFEST.md |
| `audit_scan.py` | P0 只读验证扫描 → 01_INVENTORY/audit_scan_results.json |
| `build_labels.py` | **P3 任务1**：V6C2 分类（catalog-final.json）+ P1 元数据交叉验证 → 03_TAXONOMY 标签表（labels.jsonl 123 行 / LABELING_NOTES.md / label_summary.json）。映射表为脚本内显式常量 |
| `build_grammar.py` | **P3 任务2**：Style/Functional Grammar 构建 → 04_GRAMMARS（style_rules.json / functional_rules.json / 两份 .md / grammar_confidence_report.md / data_gap_matrix.json / ir_features.jsonl）。样本纪律 n≥8 SUPPORTED、4–7 PROVISIONAL、<4 OBSERVATION ONLY，按规则自身 sample_n 执行 |
| `build_benchmark.py` | **P4**：Design Brief Benchmark 生成器 → 06_BENCHMARK（design_briefs.jsonl 100 条 / zone_catalog.json / coverage_stats.json / benchmark_split.json）。数值锚定 grammar 实测区间；targets_gap 断言命中 data_gap_matrix P0 cell；固定种子可复跑 |
| `validate_benchmark.py` | **P4 验收**：独立于生成器的 11 项全量自洽检查（层高×楼层≤限高、zone 容量、邻接引用闭合、gap size_class 边界等）+ 10 条抽查明细。全 PASS 退出码 0 |
| `generate_blueprint.py` | **P6b**：参数化参考生成器（programmatic reference generator, rule-driven，**非 LLM**）。brief + architect_rules/style_grammar 数值区间 → Canonical IR（地基/外墙/楼板/直跑或折返楼梯/隔墙分区/门窗/梯形坡顶/阳台平台/材料族拟合 + 围护洪泛密闭自检）。CLI：`--briefs 06_BENCHMARK/design_briefs.jsonl --brief-id <id> --out <路径>` |
| `revise_blueprint.py` | **P6b**：C 路线程序化修复器（REVISION_PROTOCOL 落地）。V002–V011 触发 → 体素级 patch（门接近清理/楼梯堵点开翼/孤立房间开门洞/泄漏填实/屋面补盖）或 overrides 重生成（阳台门移位/材料拟合/分区线平移）；逐坐标 diff + SHA256 + 锚点校验 |
| `score_generated.py` | **P6b**：生成样本 rubric 机器评分（口径同 score_v4_samples.py；brief 机器可读故 S03/S04/S07、M01、E01–E03、F01/F02/F03/F06 升级为机器评，F05 维持 LLM_ONLY） |
| `run_benchmark.py` | **P6b 主管线**：12 条 dev brief × B/C 两路线 → `08_EVALUATION/generated/`（B/C IR + `_traces` 逐轮中间结果）+ `evaluation_data.jsonl` 追加 + `p6b_summary.json`。CLI：`--only <brief_id>` 单跑 |

## 用法示例

```bash
# P0 审计扫描
py -3 scripts/audit_scan.py \
  --references-root "D:\Games\Minecraft\AI工程\AI-Blueprints\references" \
  --output "01_INVENTORY\audit_scan_results.json"

# 单张蓝图 IR 自检
py -3 scripts/blueprint_io.py "D:\Games\...\derived\REF-0001" --info

# 单张蓝图 walkability 分析
py -3 scripts/walkability.py "D:\Games\...\derived\REF-0001"

# 全量元数据提取（P1 主命令）
py -3 scripts/extract_blueprint_metadata.py \
  --references-root "D:\Games\Minecraft\AI工程\AI-Blueprints\references" \
  --catalog "D:\Games\Minecraft\AI工程\AI-Blueprints\references\catalog\catalog.json" \
  --output "02_BLUEPRINT_METADATA"

# 单元测试（11 个合成场景）
py -3 -m unittest tests.test_walkability -v

# P3 任务1：Taxonomy 落标（V6C2 主信号 + 几何交叉验证）
py -3 scripts/build_labels.py \
  --catalog-final "D:\Games\Minecraft\AI工程\AI-Blueprints\references\classification-v2\catalog-final.json" \
  --metadata "02_BLUEPRINT_METADATA\blueprint_metadata.jsonl" \
  --output "03_TAXONOMY"

# P3 任务2：Grammar 构建（省略 --references-root 则 IR 衍生维度全 UNKNOWN）
py -3 scripts/build_grammar.py \
  --metadata "02_BLUEPRINT_METADATA\blueprint_metadata.jsonl" \
  --labels "03_TAXONOMY\labels.jsonl" \
  --output "04_GRAMMARS" \
  --references-root "D:\Games\Minecraft\AI工程\AI-Blueprints\references\derived" \
  --palette-dictionary "02_BLUEPRINT_METADATA\palette_dictionary.json"

# P4：生成 Benchmark（100 条 brief + split + 覆盖统计）
py -3 scripts/build_benchmark.py --root "<Minecraft_Architecture_Intelligence 根>"

# P4 验收：自洽性校验（11 项全量 + 10 条抽查）
py -3 scripts/validate_benchmark.py --root "<Minecraft_Architecture_Intelligence 根>"
```

## walkability.py 设计要点（Validator 复用前必读）

- **方块分类表数据驱动**：`BLOCK_CLASS_RULES`（有序子串规则）+ `KNOWN_FULL_KEYWORDS`；
  未知方块 → UNKNOWN，保守视为整格阻挡并计入 `unknown_block_types` 统计。
  类：AIR / FULL / SLAB / STAIR / DOOR / TRAPDOOR / FENCE / FENCE_GATE / WALL /
  GLASS_PANE / LADDER / CARPET / SNOW_LAYER / PRESSURE_PLATE / PLANT / NONSOLID /
  WATER / LAVA / UNKNOWN。
- **站位（stance）**锚定在支撑体素：full/top 类 surface=1.0，bottom 类 surface=0.5，
  薄件 ≈0.1，雪层 layers/8。
- **净高**：脚部+头部近似 1.8 格；v1 层要求 `solid_lo ≥ s+0.8`，v2 层在 s>0.2 时要求
  `solid_lo ≥ s−0.2`（向量化实现，公式见模块注释）。
- **边**：水平 4 邻 × 支撑层差 dy∈{-1,0,1}；|ΔE|≤0.5 可走；|ΔE|≤1.0 且任一端为楼梯可走；
  梯柱（同 x,z 连续梯子）把相邻站位按高程连通——**P2 修复：同高程组与相邻高程组间
  完全二部连接**（旧链式实现会漏接梯井两侧分属不同房间的同高站位）。
- **可交互构件语义**：非铁质的关门、关栅栏门视为"玩家可开启"→ 可过；铁质关门阻挡；
  关闭活板门仍为半格实体（舱口竖井由梯子边覆盖，交替竖井见 P2 known_limitations）。
- **图分析**：scipy.sparse.csgraph.connected_components；死端=度数 1 的站位。
- `analyze(..., return_labels=True)` 额外返回全包络分量标签与站位高程；
  `analyze(..., return_graph=True)`（P2 新增）额外返回站位图边数组
  `graph_src/graph_dst` 与 `stance_mask`，供 Validator 做邻接查询。

## 测试

`tests/test_walkability.py`：11 个合成场景——平地可走 / 2 格墙挡人 / 半砖可上 /
楼梯连通上下层 / 敞门可过 / 木关门可过·铁关门阻挡 / 栅栏挡人 / 梯子垂直连通 /
净高不足不可站 / 未知方块统计 / 死端检测。当前全绿（11/11）。

`tests/test_validator.py`（P2）：19 个用例，8+1 组合成 Canonical IR 夹具
（`tests/fixtures/`，`generate_fixtures.py` 生成）。每条 HARD 规则（V001–V007）
至少一个正例+一个负例断言；"楼梯尽头是墙"负例（V006）必现；含"屋顶露天分量不计
孤立房间"回归锁。当前全绿（19/19）。运行：`py -3 -m unittest tests.test_validator -v`
