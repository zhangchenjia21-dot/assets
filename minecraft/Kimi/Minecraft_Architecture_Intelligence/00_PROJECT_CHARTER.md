# 00_PROJECT_CHARTER — Minecraft Architecture Intelligence System（项目代号 H）

> 版本：P7-1.0 ｜ 建立日期：2026-09-13 ｜ 状态：已完成（P0→P7 全阶段收尾）
> 本文件是项目章程：目标、边界、能力分层、信息纪律、安全规则与目录导航。
> 事实细节以各阶段报告为准；本文件只做定位与约束声明。

---

## 1. 项目目标

把目前依赖模型直觉的 Minecraft 建筑设计，尽可能转化成**可测量、可验证、可复用、可迭代**的建筑知识系统。

本项目不试图证明"122/123 张蓝图足以让 AI 学会建筑"，也不试图证明"加一些规则就能解决 AI 建筑"。
最优结果不是"所有问题都解决"，而是：**每个能力边界都被如实标注，每个数字都可回溯到真实产物。**

## 2. 边界

### 2.1 做什么（五层能力）

| 层 | 名称 | 产物位置 |
|---|---|---|
| A | Blueprint Intelligence Layer — 蓝图从"文件"升级为可查询建筑数据 | `01_INVENTORY/` `02_BLUEPRINT_METADATA/` |
| B | Architecture Grammar Layer — 风格/比例/材料/层高/屋顶/空间组织/功能分区规律 | `03_TAXONOMY/` `04_GRAMMARS/` |
| C | Spatial Quality Layer — 入口不可达/房间孤立/楼梯堵死/垂直断裂等自动发现 | `05_SPATIAL_VALIDATOR/` |
| D | Benchmark Layer — 统一测试不同 Architect Agent / Prompt 的任务集 | `06_BENCHMARK/` |
| E | Architect / Critic Rulepack — 研究成果转成模型可直接消费的规则 | `07_ARCHITECT_SYSTEM/` `08_EVALUATION/` |

### 2.2 不做什么

- 不重写 Direct World Bridge，不重构 Fabric mod 核心；
- **不修改正式 Minecraft 世界**（Formal world writes = 0）；
- 不删除/覆盖 123 张参考蓝图，不原地修改 Litematica 原件，不重命名稳定 REF ID；
- 不重做已 PASS 的 V6A/V6B/V6C 批次工作（parser、归一化、分类直接复用）；
- 不做模型微调；
- 不把无法可靠检测的审美问题硬编码进 Validator（审美终裁归人工）。

**默认对参考库和正式世界只读。** 一切产出写入本目录（`$OUT`）。

## 3. 信息状态纪律（全项目强制）

每个特征、每条规则必须标注来源性质：

| 标记 | 含义 | 示例 |
|---|---|---|
| **OBSERVED** | 从蓝图几何 / block state / catalog 直接读取或确定性计算 | 尺寸、材料占比、门计数 |
| **HEURISTIC** | 经明确算法近似，算法与盲区必须文档化 | 楼层检测、外部空气洪泛、walkability 模型 |
| **INFERRED** | 跨蓝图统计规律，必须带 sample_n 与统计区间 | grammar 的 IQR/频率规则 |
| **UNKNOWN** | 数据不足或算法无法稳定判断——**允许，不得猜测** | 主入口方位（全库 89.4% 不可判定）、窗节奏、屋顶形制 |

配套纪律：SUPPORTED（n≥8）/ PROVISIONAL（n=4–7）/ OBSERVATION ONLY（n<4）三级样本分级；
少样本不过度泛化；无法验证的改善不得虚构。

## 4. 安全规则（铁律）

1. `D:\Games\Minecraft\` 下一切文件只读；不得修改/覆盖/删除任何已有文件。
2. 正式世界零写入：不启动 Minecraft，不调用任何世界写入接口。
3. 所有产出写入 `$OUT`（本目录）。
4. 统计排除 `AI工程\迁移记录\` 与 `AI-Test\目录迁移原文件-20260909\`（2026-09-09 迁移前旧副本，防重复计数）。
5. 脚本工程化：路径走 CLI 参数或 config，不硬编码 123 个 REF ID，带 README/usage。

安全验收实测记录见 `COMPLETION_REPORT.md` Safety 节（2026-09-13 实测：三项全 0）。

## 5. 真实工程路径（P0 审计确认，OBSERVED）

```text
工程根:        D:\Games\Minecraft\AI工程
参考库根:      D:\Games\Minecraft\AI工程\AI-Blueprints\references
原始蓝图:      D:\Games\Minecraft\.minecraft\versions\26.2-Fabric 0.19.5\schematics\  (123 个 .litematic, 只读)
Canonical IR: references\derived\REF-0001 … REF-0123\  (blueprint.json + normalized\ + proxy\)
产出根($OUT): D:\AI\kimi\kimi\workspace\Minecraft 建筑设计\Minecraft_Architecture_Intelligence\
```

任务书中的 `D:\AI\Minecraft-AI-Fabric-26.2-Test`、`D:\Games\Minecraft\AI-Preview` 不存在（详见 `01_INVENTORY/REFERENCE_LIBRARY_AUDIT.md`）。
工程约束：各边最大 128、包络 ≤1,000,000 格、预览 ≤50,000 显式方块、施工上限 20,000；block entities/entities/scheduled ticks 不支持。

## 6. 目录导航

| 目录/文件 | 内容 | 关键产物 |
|---|---|---|
| `01_INVENTORY/` | P0 环境与参考库审计、数据质量 | `REFERENCE_LIBRARY_AUDIT.md`、`DATA_QUALITY_REPORT.md` |
| `02_BLUEPRINT_METADATA/` | P1 元数据 DB（123×50 字段 + _basis 标注） | `METADATA_SCHEMA.md`、`blueprint_metadata.jsonl/.csv`、`feature_extraction_report.md` |
| `03_TAXONOMY/` | P3 分类体系（Style 7 类 / Function 15 类） | `ARCHITECTURE_TAXONOMY.md`、`labels.jsonl`、`label_summary.json` |
| `04_GRAMMARS/` | P3 语法提取（style 111 条 / functional 117 条） | `STYLE_GRAMMARS.md`、`FUNCTIONAL_GRAMMARS.md`、`data_gap_matrix.json`（375 cell） |
| `05_SPATIAL_VALIDATOR/` | P2 空间校验器（V001–V012） | `VALIDATION_SPEC.md`、`validator_source/`、`REFERENCE_SET_VALIDATION.md`、`known_limitations.md` |
| `06_BENCHMARK/` | P4 设计任务基准（100 brief，dev30/test70） | `BENCHMARK_SPEC.md`、`design_briefs.jsonl`、`scoring_rubric.json`、`BASELINE_RESULTS.md` |
| `07_ARCHITECT_SYSTEM/` | P5 规则包与修订协议 | `ARCHITECT_RULEPACK.md`（218 条）、`CRITIC_RULEPACK.md`（20 条）、`REVISION_PROTOCOL.md` |
| `08_EVALUATION/` | P6 评测（V4 重评 + 12-brief B/C 离线实验） | `B_VS_C_PIPELINE.md`、`BASELINE_VS_RULED.md`、`B_VS_C_OFFLINE_RUN.md`、`VALIDATOR_TESTS.md` |
| `09_FINAL_REPORT/` | P7 最终报告（8 份） | `01_EXECUTIVE_SUMMARY.md` … `08_NEXT_STEPS.md` |
| `scripts/` | 全部脚本（审计/提取/语法/校验/基准/评测/生成） | `README.md`（环境约束与用法） |
| `tests/` | 回归测试 30 例（walkability 11 + validator 19） | `VALIDATOR_TESTS.md` 记录最近运行 30/30 绿 |
| `COMPLETION_REPORT.md` | 任务书 §30 结构的完成报告 | 含 Safety 实测验证 |

## 7. 阶段历程

P0 环境审计 → P1 Metadata DB → P2 Walkability+Validator → P3 Taxonomy+Grammar → P4 Benchmark → P5 Rulepack → P6 B/C Evaluation → P7 Final Report（本阶段）。

各阶段全部完成；阶段优先级裁剪未触发。最终结论见 `09_FINAL_REPORT/01_EXECUTIVE_SUMMARY.md`。
