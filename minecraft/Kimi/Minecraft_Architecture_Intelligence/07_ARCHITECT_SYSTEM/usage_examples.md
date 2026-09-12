# usage_examples — 下游消费者使用示例（项目代号 H · P5）

> 面向 Codex / ChatGPT 等下游模型：给定一条 brief，演示如何查 rulepack、生成时的注意点、
> 提交前 validator_precheck 自检、以及 Critic 评审话术模板。
> 三个示例覆盖三种典型情形：① SUPPORTED×SUPPORTED；② PROVISIONAL×PROVISIONAL（回退）；
> ③ 零样本风格（无 grammar 背书）。
> 所有数值均引自 `architect_rules.json` 对应规则条目，可现场核对。

---

## 示例 1：Medieval 住宅（SUPPORTED 风格 × SUPPORTED 功能）

### Brief

> "建一座中世纪风格的两层住宅，中型体量。"

### 第一步：查 rulepack

1. **风格检索**（SS-001/SS-002）：style=Medieval，n=19，SUPPORTED → 正常使用
   `architect_rules.json` 中 `applies_to.style=["Medieval"]` 的全部条目。
2. **功能检索**：function=Residential，n=23，SUPPORTED → 使用 `FUNC.Residential.*` 条目。

关键数值（抽查可追溯）：

| 决策点 | 取值 | source |
|---|---|---|
| 平面长宽比 | median 1.09，IQR[1.05,1.23] | STYLE.Medieval.footprint_ratio |
| 高宽比 | median 0.83，IQR[0.59,1.25] | STYLE.Medieval.height_ratio |
| 楼层数 | median 1，IQR[1,1.5]（brief 要求 2 层，偏离类内常态但在 max=2 内，可接受） | STYLE.Medieval.floor_count |
| stone 占比 | median 0.59，IQR[0.39,0.62] | STYLE.Medieval.palette_stone_ratio |
| wood 占比 | median 0.16，IQR[0.11,0.23] | STYLE.Medieval.palette_wood_ratio |
| 底部材料族 | 众数 stone（频率 0.89） | STYLE.Medieval.foundation_bottom_family |
| 屋顶高度占比 | median 0.06，IQR[0.03,0.10] | STYLE.Medieval.roof_height_ratio |
| 外部门候选数 | median 2，IQR[1,3.5] | FUNC.Residential.entrance_relation.exterior_door_count |
| ≥2 层频率 | 0.37（两层住宅在类内是少数但合法） | FUNC.Residential.optional_zones.upper_floor |
| 多层⇒垂直交通 | 条件频率 1.00 | FUNC.Residential.vertical_access.multifloor_requires |
| 死端比例 | median 0.13，IQR[0.08,0.19] | FUNC.Residential.circulation_constraints.dead_end_ratio |

UNKNOWN 维度（不查规则，自由发挥）：层高（floor_height，Medieval UNKNOWN）、窗洞节奏、
入口方位、屋顶形制。

### 第二步：生成注意点

- 包络 ≤128 边（GA-001）；先定平面（长宽比≈1.1），两层，石基座+木石墙身。
- **先做垂直交通再补房间**：楼梯位置先定，底部留进入站位（VA-G-01），**顶部先放落点平台
  再接梯段**（VA-G-02，"楼梯尽头是墙"的预防），顶部出口不要用关闭的活板门（VA-G-03）。
- 主入口直通主厅（CIR-G-01）；窗洞全部装玻璃（GA-008）；屋顶完整覆盖内部（GA-009）。
- 层数=2 ⇒ 必须有有效楼梯（FUNC.Residential.vertical_access.multifloor_requires，条件频率 1.00）。

### 第三步：提交前 validator_precheck

按 PC-V001…PC-V012 逐项自问（重点项）：

```text
PC-V001 有入口吗？            → 有，南向木门 1 扇
PC-V002 门内外各 1 格站位？   → 门外步道 2 格、门内门厅 1 格，高差 0 ✓
PC-V003 主厅可达率 ≥50%？     → 全部内部空间同分量 ✓
PC-V006 楼梯顶部有落点+净高？ → 顶格接二楼走廊平台，上方 2 格空气 ★
PC-V007 两层同分量？          → 楼梯连接 ✓
PC-V010 窗洞已填玻璃？        → 全部玻璃板 ✓
PC-V011 屋顶覆盖？            → 全坡顶 ✓
```

### 第四步：Critic 评审话术模板

```text
你是对上图纸的 Critic。Validator 已确认 hard_fail_count=0，你不再检查客观错误。
请仅按以下 10 个维度评审：spatial hierarchy / circulation quality / function coherence /
style coherence / proportion / facade rhythm / roof massing / material transition /
repetition / visual focal point。
每条意见按此格式输出：
[维度] severity=(suggestion|important) 观察 → 建议（CHANGE/KEEP/ADD/REMOVE + 坐标级说明）
约束：
- 量化项对照 Medieval IQR（如 height_ratio IQR[0.59,1.25]），超界才提；
- window_rhythm / 屋顶形制为 UNKNOWN 维度，给建议时注明"无数据背书"；
- 不评"丑"；审美争议项转人工。
- 锚点：footprint 南向主入口 / Medieval 风格标签 / 两层住宅分区，修订不得改变。
```

---

## 示例 2：Japanese 旅馆（PROVISIONAL × PROVISIONAL，回退策略演示）

### Brief

> "建一座日式温泉旅馆，带住宿上层。"

### 第一步：查 rulepack + 回退判断

1. style=Japanese，n=7，**PROVISIONAL**（SS-003）：所有风格数值只作咨询，目标落在 IQR 即可，
   交付说明必须标注"grammar 置信度低（PROVISIONAL）"。
2. function=Inn，n=5，**PROVISIONAL**（SS-007）：功能规则同样降格。

可用参考值（咨询性）：

| 决策点 | 取值 | source |
|---|---|---|
| 平面长宽比 | median 1.2，IQR[1.06,2.10] | STYLE.Japanese.footprint_ratio |
| 楼层数 | median 2.5，IQR[1.25,3] | STYLE.Japanese.floor_count |
| 层高 | median 8，IQR[4.25,12.25]（n=4，边缘可用） | STYLE.Japanese.floor_height |
| 屋顶高度占比 | median 0.19，IQR[0.09,0.25]（明显高于 Medieval 0.06） | STYLE.Japanese.roof_height_ratio |
| wood 占比 | median 0.25，IQR[0.23,0.29] | STYLE.Japanese.palette_wood_ratio |
| 外部门 | Inn 至少 1 扇外部门频率 1.00 | FUNC.Inn.required_zones.exterior_door |
| ≥2 层频率 | 0.60 | FUNC.Inn.optional_zones.upper_floor |
| 梯柱使用 | Inn 梯柱中位 10（类内常用梯子） | FUNC.Inn.vertical_access.means |

UNKNOWN 维度：窗洞节奏、入口方位（Japanese 全 UNKNOWN）；floor_height 仅 4 样本，谨慎。
**禁止**：把上述咨询值当 HARD 阈值执行；禁止编造"日式建筑必须出檐 X 格"这类无来源规则
（roof_overhang 频率仅 0.29，类内并非普遍）。

### 第二步：生成注意点

- 体量与材料参考上表；屋顶占比可明显高于西式（0.19 vs 0.06），形制自由发挥（UNKNOWN）。
- 功能上：≥1 外部门、上层住宿（"公共首层/私密上层"为 INFERRED 假设，可采纳但注明）、
  垂直交通必备（Inn 多层⇒垂直交通条件频率 1.00，n=3，OBSERVATION ONLY，按常识仍执行）。
- 全局 HARD 规则（GA-002…GA-005、VA-G-01…04）照常执行——回退只降风格/功能统计规则，
  不降客观合规。

### 第三步：validator_precheck

同示例 1 清单；额外注意 Inn 梯柱多 → PC-V006/VA-G-05：梯井出口留 1 格平台。

### 第四步：Critic 话术模板

同示例 1 模板，替换约束段为：

```text
- 本设计 style/function 均为 PROVISIONAL：量化阈值仅作参考，超出 IQR 不必然构成意见；
- window_rhythm / entrance_placement / 屋顶形制 UNKNOWN，注明"无数据背书"；
- 零样本禁忌：不得引入 Medieval 等其他风格的 IQR 作为依据。
```

---

## 示例 3：Modern 市政厅（零样本风格 × PROVISIONAL 功能）

### Brief

> "建一座现代风格的市政厅。"

### 第一步：查 rulepack + 回退判断

1. style=Modern → **全库 0 样本**（style_taxonomy.json `not_built_zero_sample`）。
   触发 SS-004：**无 style grammar 可用**。
   - 允许：global_architecture_rules + functional grammar + LLM 自由发挥；
   - 必须：交付说明标注"style grammar 无背书"；
   - **禁止**：编造 Modern 风格数值规则，或盗用其他风格 IQR 充当 Modern 依据。
2. function=Civic，n=4，PROVISIONAL（SS-007）：功能统计仅咨询。
   参考：外部门频率 0.75、可用楼面面积中位 5034 格（OBSERVATION ONLY）、死端比例中位 0.07。

### 第二步：生成注意点

- 风格完全由 LLM 依据"现代建筑"常识自由发挥（大玻璃幕墙、平屋顶、几何体量均可尝试），
  但每条风格决策在说明中标注依据为"LLM 常识，无本地 grammar"。
- 全局 HARD/STRONG 规则不变：入口、可达性、楼梯落点、围护、净高照常执行（GA/VA/CIR 全部适用）。
- Civic 注意：围合室内频率仅 0.25（类内多为开放/纪念性结构）——若设计为大堂+办公，属合理偏离，
  在说明中声明即可（对应 Critic 阶段的 KEEP 理由）。

### 第三步：validator_precheck

同示例 1 清单，逐条执行；风格自由不豁免任何 PC 项。

### 第四步：Critic 话术模板

```text
本设计 style=Modern 为零样本类别，无 grammar 背书：
- 所有 HEURISTIC 量化项（palette/height_ratio/roof_height_ratio 等）无风格 IQR 可对照，
  退化为只检查功能类（Civic, PROVISIONAL）相关项与全局一致性；
- style coherence / facade rhythm / roof massing 维度仅作 LLM 语义评审，必须注明"无数据背书"；
- function coherence 对照 FUNC.Civic.*（PROVISIONAL，咨询性）；
- 锚点：footprint / "Modern" 风格标签（用户指定）/ 市政厅功能分区，修订不得改变；
- 审美争议一律转人工（CR-VF-02）。
```

---

## 附：通用调用顺序（伪代码）

```python
brief = normalize(user_input)                      # 确认/声明 style + function（SS-005）
style_tier  = tier_of(brief.style)                 # SUPPORTED / PROVISIONAL / 零样本
func_tier   = tier_of(brief.function)
rules = select(architect_rules,
               style=brief.style, function=brief.function,
               tiers=(style_tier, func_tier))      # 含回退策略 SS-004/SS-007
blueprint = generate(brief, rules)                 # VA-G-02 先放楼梯落点
precheck(blueprint)                                # PC-V001…PC-V012 自检
report  = validator(blueprint)                     # V001–V012
if report.hard_fail_count: revise()                # 必须修
critique  = critic(blueprint, rules, anchors)      # 按 CRITIC_RULEPACK 话术
loop revision_protocol(max_iter=3, anchors=frozen) # 见 REVISION_PROTOCOL 状态机
```
