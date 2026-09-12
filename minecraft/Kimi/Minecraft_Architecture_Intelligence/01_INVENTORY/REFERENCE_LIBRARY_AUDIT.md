# REFERENCE_LIBRARY_AUDIT — Phase 0 环境与参考库审计

> 项目代号 H · P0 产出。所有结论均为 OBSERVED（来自只读扫描），证据路径逐条给出。
> 扫描脚本：`scripts/audit_scan.py`；原始扫描结果：`01_INVENTORY/audit_scan_results.json`。
> 扫描时间基准：2026-09-12（本阶段执行日）。

## 审计字段清单（任务书第 5 节）

| 字段 | 结论 | 证据 |
|---|---|---|
| **Source directory** | 参考库根 `D:\Games\Minecraft\AI工程\AI-Blueprints\references`；原始 .litematic 主库 `D:\Games\Minecraft\.minecraft\versions\26.2-Fabric 0.19.5\schematics\`；REF 入库拷贝在 `references\originals\` | `references\README.md`；`references\catalog\reference-id-map.json` |
| **Blueprint count** | **123** 张参考蓝图（原始 .litematic 123 个） | `references\catalog\catalog.json`（list 长度 123）；`audit_scan_results.json` |
| **REF ID count** | **123** 个稳定 REF ID（REF-0001 … REF-0123），`derived\` 下 123 个 REF-* 目录 | `audit_scan_results.json` → `ref_dir_count: 123`；`reference-id-map.json`（123 条） |
| **Normalized count** | **123/123** 全部存在 `normalized\normalized-blueprint.json` 与 `normalization-report.json`，归一化目标 DataVersion 4903；compatibility 分布 LEGACY_SAFE 67 / MIGRATED 55 / CURRENT_NATIVE 1（REF-0123） | `audit_scan_results.json` → `coverage`、`compatibility_distribution` |
| **DataVersion distribution** | 原始 minecraft_data_version：2975×2, 3105×1, 3120×1, 3465×58, 3700×1, 3953×12, 4189×14, 4438×33, 4903×1（REF-0123，26.2 原生） | `audit_scan_results.json` → `data_version_distribution`（取自 catalog.json）；另见 `AI-Test\Legacy-Normalization-V6C1\evidence\data-version-audit.json` |
| **Region count distribution** | 单 Region 122 张；双 Region 1 张（REF-0123 江户后期京都呉服商町家院落） | `audit_scan_results.json` → `region_count_distribution`；`references\README.md` |
| **File format** | 原始资产：gzip 压缩 Java big-endian NBT 的 Litematica `.litematic`；派生 Canonical IR：JSON（`schema_version=1`）；归一化 IR 同格式 | `AI-Blueprints\interop-test\README.md`（坐标与数据契约节）；`references\derived\REF-0001\blueprint.json` |
| **Parser entrypoint** | CLI：`AI-Blueprints\interop-test\Bootstrap\投影命令.mjs`（`inspect-litematic` / `import-litematic` / `export-litematic` / `compare-litematic` / `preview-blueprint`）；公开 Node API：`interop-test\L3_外交层\投影互通公开接口.mjs`（Node 24，无第三方 npm 依赖） | `interop-test\README.md`（稳定入口节） |
| **Intermediate representation** | Canonical Blueprint IR JSON（`schema_version=1`）：顶层含 `metadata / origin / dimensions / rotation / mirror / palette / blocks`；blocks 为扁平 `[x,y,z,palette_index]` 四元组，坐标从包络最小角归零；**air 显式保存**（palette 含 `minecraft:air` 且在 blocks 中被引用，实测 123/123） | 抽查 `derived\REF-0001\blueprint.json`（3150 blocks）、`derived\REF-0123\blueprint.json`（42660 blocks）；`audit_scan_results.json` → `samples`、`air_explicit_in_blocks` |
| **Known corrupted files** | **0**。V6B 批次 PARSE_FAILED:0 / POSSIBLE_CORRUPT:0；本阶段 P1 提取（见 `02_BLUEPRINT_METADATA/feature_extraction_report.md`）逐文件重读全部 123 张，parse failure 0 | `references\README.md`（V6B 技术状态表）；`AI-Test\Reference-Library-V6B\evidence\batch-report.json` |
| **Known limitations** | 各边最大 128、包络 ≤1,000,000 格、预览 ≤50,000 显式方块、施工上限 20,000；block entities / entities / scheduled ticks 不支持（明确标记 `BLOCK_ENTITY_UNSUPPORTED` 等）；未实现跨 DataVersion 的 DataFixer 迁移（已由 V6C1 归一化离线完成）；全局 rotation/mirror 需预先烘焙 | `interop-test\README.md`；CONTEXT.md 第 7 节 |
| **Existing tests** | `interop-test` 下 `npm test`（类型/位流、states、signed/multi-region、冲突、实体保留、未知 Mod、稀疏 origin、拒绝覆盖、批准禁用、10k/50k 耗时）；`测试\验证原生加载.ps1`（真实 Litematica `LitematicaSchematic.createFromFile` 探针）；历史批次证据：`AI-Test\Litematica-V6A\evidence`、`Reference-Library-V6B\evidence`、`Legacy-Normalization-V6C1\evidence`、`Classification-V6C2` | `interop-test\README.md`（验证节）；上述 evidence 目录 |

## 任务书第 5 节 13 项确认点的补充回答

1. **Minecraft AI Build 实际目录**：`D:\Games\Minecraft\AI工程`（任务书中的 `D:\AI\Minecraft-AI-Fabric-26.2-Test`、`D:\Games\Minecraft\AI-Preview` 均不存在；实际副本 `AI-Test\Minecraft-AI-Fabric-26.2-Test` 与 `AI工程\AI-Preview`）。
2. **Git 状态**：`D:\Games\Minecraft\AI工程` 非 Git 工作区（版本管理靠 MB-Vxx 批次目录与 AI-Test 证据目录）；本产出工作区 `Minecraft_Architecture_Intelligence\` 同为非 Git 目录。
3–8. 见上表。
9. **旧建筑评测脚本**：未发现独立评测脚本；历史评测以批次报告形式存在（V4 A/B/C、V6B 分类批次）。
10. **A/B/C 设计实验结果**：存在，`AI-Test\Architecture-V4\`（A-blueprint.json / B-blueprint.json+B-design.md / C-blueprint-before/final.json+C-critique.md / summary.md / benchmark.json）。
11. **V4/V5/V6 报告与 UAT**：`AI-Test\` 下 `Blueprint-Preview-V5`、`Litematica-V6A`、`Reference-Library-V6B`、`Legacy-Normalization-V6C1`、`Classification-V6C2`、`Gallery-V6D`、`Deployable-Assets-V6E`、`Current-World-Direct-UAT` 等。
12. **3D Preview 数据结构**：`derived\REF-*\proxy\`（四视图 PNG + LOD npz + palette.json），123/123 存在；`preview-metadata.json` 123/123。
13. **离线解析可行性**：**可行**。全部 123 张均有 Canonical IR 与归一化 IR，P1 全程未触碰 .litematic 原件，未启动 Minecraft。

## 排除与边界说明

- 统计排除 `AI工程\迁移记录\`（2026-09-09 迁移前旧副本）与 `AI-Test\目录迁移原文件-20260909\`，避免重复计数。
- `references\originals\REF-0123\` 为入库拷贝；原始主库位于 schematics 目录。
- 本审计对 `D:\Games\Minecraft\` 全程只读；所有产出写入 `$OUT`。
