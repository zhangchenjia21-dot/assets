# CRITIC_RULEPACK — 评审侧规则包（项目代号 H · P5）

> 配套机读文件：`critic_rules.json`（20 条，由 `build_rulepacks.py` 生成）。
> 上游来源：grammar 统计（量化阈值）、VALIDATION_SPEC 盲区声明、V4 B/C 只读参考（评审维度组织方式）。

## 0. 职责分工（显式声明，任务书第 16 节）

| 角色 | 回答的问题 | 性质 | 规则 |
|---|---|---|---|
| **Validator** | 有没有客观错误？ | 确定性（HEURISTIC 但可程序化） | V001–V012，HARD_FAIL/WARNING/INFO |
| **Critic** | 即使可用，设计是否合理？ | 判断性 | 本包 10 个维度 20 条 |

**明确禁止：**
1. **Critic 不重复 Validator 的客观错误检查。** V001–V012 的触发项直接进 Revision 流程，
   Critic 评审时不再裁决"入口是否存在""楼梯是否堵死"——那是 Validator 已经回答的问题。
2. **Critic 不评"丑"。** 不输出"难看""缺乏美感"这类无操作性的审美贬损；每条批评必须落到
   可执行的修改建议模板。审美终裁归人工（CR-VF-02，沿用 V4 纪律"规则满足不等于美观自动通过"）。
3. Critic 不改 UNKNOWN 维度的结论：凡 grammar 标 UNKNOWN 的维度（窗节奏、屋顶形制等），
   Critic 只能以 LLM_ONLY 方式给建议，且必须注明"无数据背书"。

## 1. 检查方法分级

| kind | 含义 | 示例 |
|---|---|---|
| HEURISTIC | 可程序化检查，给量化指标与阈值；阈值引自 grammar 真实 IQR/频率 | CR-CQ-01、CR-PR-01 |
| LLM_ONLY | 只能由模型从蓝图/预览判断，不给阈值 | CR-SH-02、CR-RP-01 |
| HUMAN_REVIEW | 必须人工裁决 | CR-VF-02 |

severity：`suggestion`（可权衡）/ `important`（强烈建议修改）/ `critical`。
本包**无 critical 条目**——凡"接近必须修改"的客观项都属于 Validator HARD_FAIL，职责不越界。

## 2. 十个维度 × 20 条规则

### spatial hierarchy（空间层级）
- **CR-SH-01**（HEURISTIC, suggestion）：单盒包络（footprint_ratio≈1）且无可识别次级体量 → 提示缺乏主次。
  修改模板：拆分/附加次级体量（侧翼/门廊/塔），参考 V4 B 的 L 形主次体量。
- **CR-SH-02**（LLM_ONLY, important）：主入口在接近方向上应可辨认（门廊/踏步/灯光/凹口）。
  参考 V4 C "Minecraft readability"：玩家从庭院接近时分不清主门与侧门 → 加偏心罩棚+双灯+连续踏步。

### circulation quality（动线质量）
- **CR-CQ-01**（HEURISTIC, suggestion）：`dead_end_ratio > 功能类 p75` → 动线碎片化。
  阈值按 `FUNC.{function}.circulation_constraints.dead_end_ratio` 取值。
- **CR-CQ-02**（LLM_ONLY, important）：语义动线——图上连通 ≠ 合理（穿卧室到厨房、出后门再进侧门）。
  Validator 明确不判此类（V003 盲区），Critic 负责补上。

### function coherence（功能一致性）
- **CR-FC-01**（HEURISTIC, important）：`usable_floor_area < 功能类 p25` → 功能容量不足。
- **CR-FC-02**（LLM_ONLY, suggestion）：功能分区语义。grammar 不识别房间语义，公私分层为 INFERRED，
  Critic 只能给"公共首层/私密上层"这类常识性建议并标注依据等级。

### style coherence（风格一致性）
- **CR-SC-01**（HEURISTIC, important）：wood/stone/glass/decorative 四项材料族占比 ≥2 项出 IQR → 风格漂移。
- **CR-SC-02**（LLM_ONLY, suggestion）：风格语汇混搭诊断；风格零样本（Modern 等）时不评此项。

### proportion（比例）
- **CR-PR-01**（HEURISTIC, suggestion）：`height_ratio` 出风格类 IQR。
- **CR-PR-02**（HEURISTIC, suggestion）：`footprint_ratio` 出风格类 IQR。
  塔楼等特殊功能可豁免，但需注明。

### facade rhythm（立面节奏）
- **CR-FR-01**（LLM_ONLY, suggestion）：窗洞位置节奏——grammar 全风格 UNKNOWN，**只作 LLM 判断，
  评审语中必须注明"无数据背书"**。
- **CR-FR-02**（HEURISTIC, suggestion）：`window_density` 出风格类 IQR。

### roof massing（屋顶体量）
- **CR-RM-01**（HEURISTIC, suggestion）：`roof_height_ratio` 出风格类 IQR。
- **CR-RM-02**（LLM_ONLY, suggestion）：屋顶形制与风格匹配——形制 grammar 未测量（UNKNOWN），
  仅 LLM 判断并注明。

### material transition（材料过渡）
- **CR-MT-01**（HEURISTIC, suggestion）：底部 1/3 主导材料族 ≠ 风格类众数（如 Medieval 众数 stone，频率 0.89）。
- **CR-MT-02**（LLM_ONLY, important）：材料层级是否成立（承重→结构→填充），还是随机噪声铺色。
  参考 V4 C "Material hierarchy：五个主要材料族职责明确，不新增随机点缀材料"。

### repetition（重复）
- **CR-RP-01**（LLM_ONLY, suggestion）：机械重复同一构件且立面无差异（V4 C 实测："庭院下层百叶等距重复"
  → 移除三组窗饰，中央改有识别度的入口）。
- **CR-RP-02**（HEURISTIC, suggestion）：对称性偏离风格类常态（如 Rustic 高对称频率 0.0，做成高对称即偏离）。

### visual focal point（视觉焦点）
- **CR-VF-01**（LLM_ONLY, suggestion）：全立面均质无焦点 → 增加/强化一个焦点构件；
  烟囱设置可参考 `STYLE.{style}.chimney_frequency`。
- **CR-VF-02**（HUMAN_REVIEW, suggestion）：审美终裁归 Owner，附修改前后对比说明。

## 3. 评审输出格式（建议模板）

每条触发按如下格式输出（对应 `revision_template` 字段）：

```text
[CR-XX-##] severity=important | dimension=proportion
观察：height_ratio=1.9，超出 Fantasy IQR[0.72,1.23]（n=10, PROVISIONAL）
建议：降低塔身高度或加宽基座，使高宽比回到 IQR 内；若为 Tower 功能可豁免，请注明。
依据：STYLE.Fantasy.height_ratio（grammar, SUPPORTED→规则自身 PROVISIONAL 时需注明）
处置：CHANGE / KEEP / ADD / REMOVE + 具体坐标级说明（沿用 V4 C 表格习惯）
```

## 4. 计数

| dimension | HEURISTIC | LLM_ONLY | HUMAN_REVIEW | 小计 |
|---|---:|---:|---:|---:|
| spatial_hierarchy | 1 | 1 | 0 | 2 |
| circulation_quality | 1 | 1 | 0 | 2 |
| function_coherence | 1 | 1 | 0 | 2 |
| style_coherence | 1 | 1 | 0 | 2 |
| proportion | 2 | 0 | 0 | 2 |
| facade_rhythm | 1 | 1 | 0 | 2 |
| roof_massing | 1 | 1 | 0 | 2 |
| material_transition | 1 | 1 | 0 | 2 |
| repetition | 1 | 1 | 0 | 2 |
| visual_focal_point | 0 | 1 | 1 | 2 |
| **合计** | **10** | **9** | **1** | **20** |
