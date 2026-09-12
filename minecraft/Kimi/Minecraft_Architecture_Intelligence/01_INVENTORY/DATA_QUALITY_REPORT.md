# DATA_QUALITY_REPORT — 参考库数据质量报告

> 项目代号 H · P0 产出。除特别说明外均为 OBSERVED。
> 证据：`01_INVENTORY/audit_scan_results.json`（`scripts/audit_scan.py` 生成，只读扫描）。

## 1. 完整性总览

| 指标 | 结果 | 说明 |
|---|---:|---|
| REF 目录数 | 123/123 | `derived\REF-0001 … REF-0123` |
| 损坏文件 | **0** | V6B 批次 PARSE_FAILED:0 / POSSIBLE_CORRUPT:0（`references\README.md`）；P1 逐文件重读亦 0 失败 |
| unresolved blocks | **0**（归零） | 全部 123 份 `normalization-report.json` 的 `unresolved` 合计为 0；V6C1 归一化目标 DataVersion 4903 |
| catalog 条目 | 123/123 | 每条含 `reference_id / dimensions / block_count / compatibility / primary_use / styles` 等 60+ 字段 |

## 2. derived 产物覆盖率（脚本实测）

| 产物 | 覆盖 | 覆盖率 |
|---|---:|---:|
| `blueprint.json`（Canonical IR） | 123/123 | 100% |
| `normalized\normalized-blueprint.json` | 123/123 | 100% |
| `normalized\normalization-report.json` | 123/123 | 100% |
| `normalized\original-blueprint.json` | 123/123 | 100% |
| `proxy\`（四视图 PNG + LOD npz + palette.json） | 123/123 | 100% |
| `preview-metadata.json` | 123/123 | 100% |
| `metadata.json` | 123/123 | 100% |
| `analysis.md` | 123/123 | 100% |

结论：派生链完整，**P1+ 各阶段可完全离线工作于 normalized IR，无需触碰 .litematic 原件**。

## 3. air 表示方式实测结论（OBSERVED）

- 全部 123 份 `normalized-blueprint.json` 的 palette 均含 `minecraft:air` 条目；
- 全部 123 份的 `blocks` 数组**显式引用 air 的 palette 索引**（即 air 不是“缺省即空气”，而是显式体素；V6B 报告亦载 “air 显式保存”）；
- 未观察到 `minecraft:cave_air` / `void_air` 条目；
- 抽样验证：REF-0001（palette 15 项 / 3150 blocks，含 `minecraft:air`）、REF-0123（palette 51 项 / 42660 blocks，含 `minecraft:air`），顶层结构均为 `schema_version / metadata / origin / dimensions / rotation / mirror / palette / blocks`，origin 为 `{x:0,y:0,z:0}`（坐标已从包络最小角归零）。
- 工程含义：体素化时**必须尊重显式 air**——它携带“此处被有意留空”的语义；包络内未被 blocks 覆盖的坐标同样按 air 处理（Canonical 契约允许稀疏掩码，见 `interop-test\README.md`）。

## 4. 已知限制（沿用 V5/V6A 工程约束，OBSERVED）

| 限制 | 数值 |
|---|---|
| 各边最大 | 128 格 |
| 包络体积上限 | 1,000,000 格 |
| 预览显式方块上限 | 50,000（含 Region 内 air） |
| 施工上限 | 20,000 |
| block entities / entities / scheduled ticks | 不支持（明确标记 UNSUPPORTED，不静默丢弃语义） |
| 跨 DataVersion DataFixer | 未在互通层实现；旧蓝图经 V6C1 离线归一化到 4903，palette_changes 留痕于各 `normalization-report.json` |

## 5. 归一化与迁移记录说明

- compatibility 分布：LEGACY_SAFE 67 / MIGRATED 55 / CURRENT_NATIVE 1（REF-0123）。
- 旧 identifier（如 `minecraft:grass`、`minecraft:chain`）在归一化中完成映射，归一化后 unresolved=0；原始 IR（`blueprint.json` / `normalized\original-blueprint.json`）保留原样可供溯源。
- **排除规则**：本阶段一切统计排除 `AI工程\迁移记录\` 与 `AI-Test\目录迁移原文件-20260909\`（2026-09-09 迁移前旧副本，会重复计数）；`references\originals\REF-0123\` 为入库拷贝不重复计数。

## 6. 风险与残留问题

| 项 | 状态 | 影响 |
|---|---|---|
| 托管 Python venv 基础解释器路径失效 | 已绕过 | 本阶段以 `py -3` + `PYTHONPATH` 挂载 `daimon\runtime\python\.venv\Lib\site-packages`（只读）运行 numpy/pandas；详见 `scripts/README.md` |
| block entities 语义（箱子内容、告示牌文字等） | UNKNOWN（工程不解析） | 功能判读（如“厨房”）不能依赖容器内容 |
| 蓝图 rotation/mirror | 已烘焙为坐标与状态 | 提取特征按烘焙后坐标系计算，不代表放置到世界后的朝向 |
| `minecraft:air` 之外的特殊空气变体 | 未出现 | 若未来引入 cave_air/void_air，需扩展解析白名单 |
