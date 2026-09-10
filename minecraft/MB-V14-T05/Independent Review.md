# T05 Independent Review｜minecraft-builder v1.4

## Verdict

**FAIL_WITH_STRONG_POSITIVE_REGRESSION**

T05 在 Structural Vegetation 上出现显著跃迁：祖树与外围树群已经真正承担 canopy、围合、背景、路径与圣所身份，42 株结构树以自定义大树为主，不再依赖原版小树；草、蕨、苔地、腐殖土等近地层也明显改善。但中央水系作为 LANDSCAPE / MIXED_ENVIRONMENT 的一等系统存在 Minecraft 运行时有效性缺口，因此终态不能按完成品通过。

## Positive evidence

### T05-P01｜Structural Vegetation breakthrough

- 祖树约 48 格高、29 格冠幅级别，外围树群采用 20–32 格高的大型自定义树。
- 树群按场地边缘、开口、水体与交通 reserve 组织，而不是默认 Minecraft 小树散点。
- Owner 实机确认整体树形与“森林圣所”主题相符。

结论：v1.4 及此前 Structural Vegetation / scale 规则已经真正改变模型空间设计方式。

### T05-P02｜Ground / herb layer improvement

- 使用 moss、podzol、coarse dirt、short grass、fern 等形成林下与湿岸地表。
- 相比 T01–T04，近地层从“默认 grass block + 稀疏点缀”明显进步。

## Findings

### T05-F01｜Water geometry is not proven vanilla-fluid-stable

**Classification:** A `SKILL_GAP` + B `MODEL_EXECUTION_FAILURE` + C `TOOLING_LIMITATION`

**Severity:** Critical

Owner 在 Minecraft 客户端看到多级溪流/河道两侧缺少足以约束水体的河床与岸壁；按 Vanilla fluid 行为，侧边开放的 source/flowing water 在正常邻接更新后应向外蔓延，而当前几何呈现为静态体素水带。

生成器直接大量写入 `minecraft:water[level=0]`，并用人工分段水位制造 72→70→68→65→64→63 的跌水。现有 `水系核验.py` 只计算 water voxel 的六邻接分量，明确声明“连通不代表长时间流体模拟”。Completion Report 也承认未进行长期 fluid update 验证。

**Root issue:** 当前 QA 验证的是 `connected water voxels`，不是 `Minecraft-valid hydrology`。

**Required direction:** Skill 应增加 Water / Fluid Semantics：河床、岸壁、水位、溢流口、跌水、源水/流水状态必须在 Minecraft 实际 fluid rules 下成立。若工具可用，应触发/模拟必要 fluid updates 后复查；若工具不可用，应采用保守可稳定的河道截面，并明确不能把静态离线水体素视为完成验证。

### T05-F02｜Flowering layer remains visually under-corrected

**Classification:** A `SKILL_GAP` + B `MODEL_EXECUTION_FAILURE`

**Severity:** Major

v1.4 已使 Codex 从单一极低密度花点进步到 3 个花种（lily_of_the_valley / allium / blue_orchid）与 5 个显式 flower patch，但在 256×256 的“幻想森林圣所”中，Owner 实机仍感到花卉层明显不足。

当前规则仍反复强调 Flowers are accents / 不要过度，因此模型继续采用保守密度。对于 lush / enchanted / sacred grove / ornamental garden / spring meadow 等花卉本应成为显著视觉层的题材，需要更强的正向默认。

**Required direction:** 下一版允许有意“过校正”：在花卉主题合理的 lush 场景中，花卉应在玩家尺度上明显可见，形成多个 substantial patches / ribbons / clearing carpets / edge communities，而不是只有少数象征性斑块。仍禁止均匀撒点和机械集齐所有颜色；若后续出现过量，再基于新测试回调。

### T05-F03｜Tree crown family still somewhat repetitive

**Classification:** B `MODEL_EXECUTION_FAILURE`

**Severity:** Minor

Completion 自认树冠偏圆团且存在家族重复。与此前相比已经显著改善，不建议为此立即继续扩写 Skill；后续观察幻想森林之外题材是否重复。

### T05-F04｜Water QA produces false confidence

**Classification:** A `SKILL_GAP` + C `TOOLING_LIMITATION`

**Severity:** Major

`6407` 格水形成单一六邻接分量只能证明“几何连通”，不能证明水位合理、岸线封闭、流向正确或 tick 后不外溢。以后水系 QA 必须将 connectivity 与 fluid stability 分开报告，不能以单连通分量作为水系完成证据。

## Owner evidence incorporated

1. 客户端观察到河道/跌水边缘与 Minecraft 水流规则不一致，需要 Water Level / Channel / Fluid Stability 检验。
2. 大型自定义树形与森林圣所主题匹配，为本轮最明确的正向改进。
3. 花卉仍明显不足，Owner 要求下一轮对适宜题材做大幅度正向矫正，宁可先偏多再根据测试回调。

## Regression conclusion

T05 证明：

- Structural Vegetation / tree scale：**显著成功**；
- Ground herbaceous layer：**明显成功**；
- Flowering Community：**方向有效但力度不足**；
- Water：**出现新的 Minecraft runtime-semantics 缺口**。

下一版 Skill 优先补：

1. `Minecraft Water / Fluid Semantics & Stability`；
2. 更强的 theme-sensitive `Flower Abundance Bias`。

不要因为本轮水系错误否定树木与近地植被已经取得的正向回归证据。