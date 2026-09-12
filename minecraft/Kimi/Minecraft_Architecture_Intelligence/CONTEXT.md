# CONTEXT.md — 共享工程上下文（所有子任务必读）

> 本文件是 Minecraft Architecture Intelligence System（项目代号 H）各阶段子任务的统一事实来源。
> 任何脚本/文档任务开始前先读本文件，避免重复探索。

## 0. 铁律（来自任务书，必须遵守）

1. **只读参考库**：`D:\Games\Minecraft\` 下一切文件只读。不得修改/覆盖/删除任何已有文件。
2. **正式世界零写入**：不启动 Minecraft，不调用任何世界写入。
3. **所有产出写入工作区**：`D:\AI\kimi\kimi\workspace\Minecraft 建筑设计\Minecraft_Architecture_Intelligence\`（下称 `$OUT`）。
4. **UNKNOWN 纪律**：每个特征/规则标注 OBSERVED / HEURISTIC / INFERRED / UNKNOWN。数据不足写 UNKNOWN，不得猜测。
5. **脚本工程化**：模块化、路径走 CLI 参数或 config、不硬编码 123 个 REF ID、不依赖单一绝对路径、带 README/usage、关键算法有注释。
6. **不重复 V6 工作**：不重写 parser、不重做归一化、不重命名 REF ID、不动 Litematica 原件。

## 1. 真实工程路径（已审计确认）

任务书中的 `D:\AI\Minecraft-AI-Fabric-26.2-Test`、`D:\Games\Minecraft\AI-Preview` **不存在**。真实根：

```
工程根:        D:\Games\Minecraft\AI工程
参考库根:      D:\Games\Minecraft\AI工程\AI-Blueprints\references
原始蓝图:      D:\Games\Minecraft\.minecraft\versions\26.2-Fabric 0.19.5\schematics\  (123 个 .litematic, 只读!)
REF 映射:      references\catalog\reference-id-map.json   (123 条: reference_id / original_filename / original_absolute_path / file_hash)
主目录清单:    references\catalog\catalog.json / catalog.csv  (123 条 × 60+ 字段)
分类 V2:       references\catalog\classification-v2\catalog-v2.json, catalog-final.json
分类规则说明:  references\catalog\classification-rules.md
受控词表:      references\catalog\controlled-vocabulary.json
倒排索引:      references\indexes\inverted-index.json
```

## 2. Canonical Blueprint IR（核心数据格式，schema_version=1）

每张参考蓝图已有解析产物，**离线可用，无需碰 .litematic**：

```
references\derived\REF-0001 … REF-0123\
├── blueprint.json          # Canonical IR
├── metadata.json
├── preview-metadata.json
├── analysis.md
├── normalized\
│   ├── normalized-blueprint.json    # 归一化到 DataVersion 4903 的 IR（分析应优先用它）
│   ├── normalization-report.json    # original_data_version / compatibility / palette_changes / unresolved / state_checks
│   └── original-blueprint.json
└── proxy\                  # 四视图 PNG + LOD npz + palette.json
```

**blueprint.json 顶层结构**：
```json
{
  "schema_version": 1,
  "metadata": {"litematica": {"format_version", "minecraft_data_version", "regions": [...], ...}},
  "origin": [x,y,z],
  "dimensions": {"x":…,"y":…,"z":…},
  "rotation":…, "mirror":…,
  "palette": ["minecraft:oak_stairs[facing=north,half=bottom,shape=straight]", ...],
  "blocks": [[x,y,z,palette_index], ...]
}
```
- blocks 为扁平 `[x,y,z,palette_index]` 四元组；坐标为蓝图局部坐标。
- palette 项是完整 block state 字符串（含 `[...]` 属性）。air 可能是 `minecraft:air`/`cave_air` 或不在 blocks 中（需实测确认并记录）。
- 样例：`references\derived\REF-0001\blueprint.json`（3150 blocks）。

**分析一律优先读 `normalized\normalized-blueprint.json`**（全库已归一化到 DataVersion 4903，unresolved=0）；缺失时回退 `blueprint.json` 并记录。

## 3. 归一化状态（OBSERVED 事实）

- 123 张全部已归一化：LEGACY_SAFE 67 / MIGRATED 55 / CURRENT_NATIVE 1（REF-0123）
- DataVersion 分布：2975×2, 3105×1, 3120×1, 3465×58, 3700×1, 3953×12, 4189×14, 4438×33
- Region：单 Region 122 张，双 Region 1 张（REF-0123 京町家修复）
- 损坏文件：0（V6B 报告 PARSE_FAILED:0 / POSSIBLE_CORRUPT:0）
- 证据：`AI-Test\Legacy-Normalization-V6C1\evidence\data-version-audit.json`、`AI-Test\Reference-Library-V6B\evidence\summary.md`

## 4. catalog.json 已有字段（Metadata DB 可复用/连接）

`name / schematic_name / dimensions{x,y,z} / block_count / occupied_block_count / palette_size / primary_use(含置信度与证据) / styles[{tag,confidence,evidence}] / scale / settlement_roles / terrain_fit / material_profile / dominant_materials / block_entity_count / entity_count / technical_status / compatibility / blueprint_path / normalized_blueprint_path` 等 60+ 字段。
→ 我们的 Metadata DB 以 ref_id 关联 catalog，**增量计算几何/连通性字段**，不复制粘贴已有字段（可在文档中引用）。

## 5. V4 A/B/C 历史样本（Phase 8 评测用）

```
AI-Test\Architecture-V4\
├── A-blueprint.json                # 自由生成
├── B-blueprint.json + B-design.md  # 规则约束（Macro/Meso/Micro）
├── C-blueprint-before.json / C-blueprint-final.json / C-critique.md / C-design.md
├── summary.md / benchmark.json     # V4 对比报告
└── evidence\C-revision-diff.json
```
蓝图同样是 Canonical IR JSON，可直接喂给 Validator。

## 6. 运行时环境

- 托管 Python：`python`（Bash 内直接可用），含 numpy/pandas；**无 nbtlib**——如需解析原始 .litematic，vendored nbtlib 在 `AI-Blueprints\参考入库\第三方\nbtlib`（sys.path 注入）。但默认根本不需要碰原始文件。
- Node 24 可用（工程内 interop-test / AI-Preview 是 Node 项目），新增代码默认用 **Python**。
- Windows 路径含空格与中文，脚本内用 `pathlib`，命令行注意引号。

## 7. 已知工程限制（来自 interop-test/旧版归一化 README）

- 各边最大 128、包络 ≤1,000,000、预览 ≤50,000 显式方块、施工上限 20,000
- block entities / entities / scheduled ticks 不支持
- Mod 方块保留 unresolved（归一化后已归零）

## 8. 排除规则

- 统计/扫描时排除 `迁移记录\` 目录（2026-09-09 迁移前旧副本，会重复计数）。
- `AI-Blueprints\references\originals\REF-0123\` 是入库拷贝，原始主库在 schematics 目录。

## 9. 阶段优先级（资源不足时按此裁剪）

P0 环境审计 → P1 Metadata DB → P2 Walkability+Validator → P3 Taxonomy+Grammar → P4 Benchmark → P5 Rulepack → P6 B/C Evaluation → P7 Final Report
