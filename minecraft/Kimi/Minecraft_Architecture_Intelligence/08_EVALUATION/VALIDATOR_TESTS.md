# VALIDATOR_TESTS — Spatial Validator 回归测试报告（项目代号 H · P2/P6）

> 测试套件：`tests/test_walkability.py`（11 例）+ `tests/test_validator.py`（19 例），合计 30 例。
> 本报告由 P6（Phase 8 第一部分）重跑确认并整理覆盖矩阵。

## 1. 最近一次运行

- 命令：`py -3 -m unittest tests.test_walkability tests.test_validator -v`（工作目录 = `$OUT` 根；环境 `PYTHONPATH=D:\AI\kimi\daimon-share\daimon\runtime\python\.venv\Lib\site-packages`）
- 时间：2026-09-13 02:58:16（本地时间）
- 结果：**Ran 30 tests — OK（30/30 通过，0 失败，0.051s）**

## 2. 规则 × 正例/负例覆盖矩阵（test_validator.py，19 例）

夹具：`tests/fixtures/*.json`（合成 Canonical IR，由 `generate_fixtures.py` 程序化生成，缺失时测试启动自动重建）。

| 规则 | 正例夹具（断言不触发/无 HARD_FAIL） | 负例夹具（断言触发 + 严重级） | 覆盖断言 |
|---|---|---|---|
| V001 No Exterior Entrance | correct_entrance | no_exterior_entrance | `test_v001_positive` / `test_v001_negative`（HARD_FAIL） |
| V002 Main Entrance Blocked | correct_entrance | blocked_entrance | `test_v002_positive` / `test_v002_negative`（HARD_FAIL） |
| V003 Major Interior Unreachable | correct_entrance | blocked_entrance（内部整体不可达） | `test_v003_positive` / `test_v003_negative` |
| V004 Isolated Room / Space | correct_entrance | isolated_room | `test_v004_positive` / `test_v004_negative`（HARD_FAIL） |
| V005 Stair Bottom Blocked | correct_stair | stair_bottom_blocked | `test_v005_positive` / `test_v005_negative`（HARD_FAIL） |
| V006 Stair Top Blocked（"楼梯尽头是墙"） | correct_stair | stair_top_blocked | `test_v006_positive` / `test_v006_negative`（HARD_FAIL，必现回归锁） |
| V007 Vertical Circulation Broken | correct_multifloor | broken_vertical_access | `test_v007_positive` / `test_v007_negative`（HARD_FAIL） |
| V008–V012（WARNING/INFO 级） | —（无独立负例夹具） | —（无独立负例夹具） | 仅由 `test_all_rules_present` 保证 12 条规则结果全部输出 |

结构性断言（3 例）：
- `test_all_rules_present`：每张蓝图输出 V001–V012 全部规则结果 + 任务书 §11 全部输出字段。
- `test_correct_entrance_no_hard_fail` / `test_correct_stair_no_hard_fail` / `test_correct_multifloor_no_hard_fail`：三个正例蓝图均不得有任何 HARD_FAIL。

专项回归锁（1 例）：
- `test_rooftop_component_not_counted_as_isolated_room`：正例蓝图屋顶露天站位形成独立连通分量（`walkable_components ≥ 2`），但 V004 不得触发——锁定 P1 教训（露天分量不计入孤立房间，否则全库误报）。

任务书 §12 要求"每条 Hard Rule 至少有正例和负例测试"：V001–V007 七条 HARD 规则全部满足 ✅。

## 3. walkability 模型覆盖（test_walkability.py，11 例）

| # | 场景 | 验证点 |
|---|---|---|
| 1 | 平地可走 | 5×5 石板地面 → 25 站位、1 分量 |
| 2 | 2 格高墙挡人 | 墙两侧站位分属不同分量 |
| 3 | 半砖可站上 | bottom 半砖 0.5 步高连通 |
| 4 | 楼梯连通上下层 | 3 级楼梯从地面升到 3 格高平台 |
| 5 | 敞门可过 | open 橡木门两侧同分量 |
| 6 | 木关门可过 / 铁关门阻挡 | 可交互构件语义（非铁质=可开启） |
| 7 | 栅栏挡人 | 碰撞 1.5 格，两侧不同分量 |
| 8 | 梯子垂直连通 | 地面→梯柱→3 格高平台同分量 |
| 9 | 净高不足不可站 | 1 格压顶板 → 地板站位非法 |
| 10 | 未知方块统计 | UNKNOWN 计入统计、保守视为阻挡 |
| 11 | 死端检测 | 1 格宽走廊封死 → 存在死端节点 |

## 4. 已知覆盖缺口（诚实声明）

1. **V008–V012 无独立负例夹具**：WARNING/INFO 级规则只有输出存在性断言，没有"必触发"回归锁。这些规则的阈值行为依赖 P2 全库校准（见 `05_SPATIAL_VALIDATOR/REFERENCE_SET_VALIDATION.md`，校准后全库 hard_fail_rate=0.496）而非单元负例。
2. **分级降级路径未单测**：V003/V004 的"隔离环含可交互构件 → 降 WARNING"机制感知分级在 P6 历史样本（C-before）上首次真实出现并被人工核对（见 `B_VS_C_PIPELINE.md`），但无合成夹具锁定。
3. **舱口（hatch）入口、交替梯子竖井**等低频路径无夹具；盲区见 `05_SPATIAL_VALIDATOR/known_limitations.md`。
