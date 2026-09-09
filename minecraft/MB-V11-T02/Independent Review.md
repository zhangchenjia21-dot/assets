# MB-V11-T02 Independent Review

Date: 2026-09-09

Test world: `MB-V11-T02-山地修道院`

Skill under test: `minecraft-builder v1.1`

Verdict: **PASS_WITH_MAJOR_FINDINGS**

## Positive evidence

- `T02-P01` — 山地、道路、建筑群之间形成了真实的三维因果关系；不是在平地上摆放修道院。
- `T02-P02` — 山脚 → 门楼 → 客舍 / 服务区 → 高台教堂 → 回廊 → 生产台地的移动序列成立，上山视野和空间开合表现良好。
- `T02-P03` — Plan / Section / Sequence 真实进入施工；多层台地、挡墙、楼梯和建筑标高之间关系清楚。
- `T02-P04` — Codex 在阶段审查中自行发现并修复主路撞墙、泉台观察点、楼板缺基础等问题，说明 staged self-check 有实际作用。

## Findings

### T02-F01 — 非预期悬空石质构件再次出现

Classification: `SKILL_GAP + MODEL_EXECUTION_FAILURE + QA_SCOPE`

Severity: High

Owner 在真实 Minecraft 客户端发现建筑侧面存在明显横向悬出的石质墙 / 构件，下方无合理支撑。该问题在 Codex 自己的软件透视中也可见，但未被其识别为异常。

生成逻辑与最终 QA 均说明现有检查主要覆盖：设计体素一致性、主要动线净空、建筑楼板基础接触；没有对墙体、岩石、台地边缘、植被等全局几何执行 unintended floating / isolated geometry 检查。

T01 已出现浮空石块，T02 再次复现。升级为 `minecraft-builder v1.2` 高优先级候选：加入 Construction Integrity Sweep。

### T02-F02 — Detail Vegetation 与 vanilla plant palette 仍明显不足

Classification: `MODEL_EXECUTION_FAILURE + SKILL_GAP`

Severity: High

除树冠、农作物、少量所谓“林下斑块”外，场景仍基本没有使用 Minecraft 原版丰富的花草、蕨类、苔藓等小尺度植被。林下斑块甚至主要使用 leaves 方块代替真正地被。

T01 已出现相同问题。说明 v1.1 虽然定义了 Detail Vegetation，但不足以促使 Codex主动建立 vanilla detail vegetation palette。

v1.2 应明确：适合题材时主动利用原版草、蕨、苔藓、花卉与其它小型植物；按生态、色彩和空间职责成组组织，禁止随机彩色撒点。

### T02-F03 — Structural Vegetation 仍偏“散点大树”

Classification: `MODEL_EXECUTION_FAILURE`

Severity: Medium

大型乔木尺度已有改善，但整体仍以离散坐标的单株树为主，没有充分形成树林、林缘、树带、疏密梯度和 canopy mass。v1.1 对 cluster / density gradient / irregular edge 已有明确要求，因此本轮主要归因于执行不足。

继续在森林类测试中观察。

### T02-F04 — 材质与表面语言过于单一

Classification: `MODEL_EXECUTION_FAILURE + SKILL_GAP`

Severity: High

主要建筑和地形长期依赖少数 stone / stone_bricks / cobblestone / smooth_sandstone / terracotta / gravel 等材料，大面积墙面、山体和屋面缺乏受控的层次与过渡。

T01 已存在相同趋势。升级为 v1.2 高优先级候选：建立 Controlled Material Language，而不是单纯增加方块数量或随机混材。

### T02-F05 — 参数化形态重复

Classification: `MODEL_EXECUTION_FAILURE + SKILL_GAP`

Severity: Medium-High

多个功能不同的建筑共享高度相似的矩形石墙 + 阶梯坡屋顶生成语法。代码复用本身没有问题，但实现层的 reusable generator 被隐性转化成了设计层的形态复制。

T01 的亭与树已经出现类似现象。升级为 v1.2 候选：reusable generator ≠ repeated morphology；功能、等级和环境角色显著不同的对象应形成合理的形态家族差异。

### T02-F06 — 山地适应成立，但局部过度规则切台

Classification: `MODEL_EXECUTION_FAILURE / TASK_SPECIFIC_JUDGMENT`

Severity: Medium

整体山地逻辑是成功的，但部分建筑通过较大的矩形 pad 切出台地，仍有“先切平台、再放建筑”的倾向。真实山地修道院允许台地，因此不能机械禁止；后续应观察是否经常过度平台化。

暂不写入通用 Skill 新规则。

### T02-F07 — 山体已有 Geometry，但 Surface Language 不足

Classification: `MODEL_EXECUTION_FAILURE`

Severity: Medium

高处山壁主要在 grass / andesite 等少数表面状态之间切换，缺少岩层、碎石坡、土石交界、裂隙、植被口袋等中尺度表面结构。

与 F04 有关联，但暂记为地形专项表现，不独立扩写 Skill。

### T02-F08 — 屋顶与立面 Minecraft 工艺仍粗糙

Classification: `MODEL_EXECUTION_FAILURE`

Severity: Medium

远观建筑体量成立，但屋顶明显呈整层方块阶梯，长墙面开口和构造节奏偏少。说明 v1.1 提升了空间设计，但没有同步显著提升 block vocabulary / building craft。

暂不将具体 stairs / slabs 用法硬编码进通用 Skill，避免过度工程化；先由 Controlled Material / Morphology Review 约束整体结果。

### T02-F09 — Perceptual QA 仍不足

Classification: `TOOLING_LIMITATION + MODEL_EXECUTION_FAILURE`

Severity: High

Codex 已生成软件体素透视，悬空构件在预览阶段具备可见性，但未被识别；同时软件透视不等于真实 Minecraft 客户端材质、透明度、光照与碰撞体验。

长期工具链应支持真实客户端玩家高度截图或自动观察点截图。Skill 可要求在可获得真实客户端证据时优先用于 Final Review，但不应把不存在的工具能力写成硬依赖。

## Cross-test escalation after T01 + T02

以下问题已经跨两个不同题材复现，不再视为单次偶发：

1. 非预期悬空 / 孤立几何未被可靠发现；
2. Detail Vegetation / 原版植物 palette 利用不足；
3. 材质与 surface language 单一；
4. 参数化生成导致形态重复。

Owner 已批准在 T03 前优先更新 Skill。后续测试从 `minecraft-builder v1.2` 开始，因此 T01 / T02 作为 v1.1 baseline 保留，不回写修改历史样本。
