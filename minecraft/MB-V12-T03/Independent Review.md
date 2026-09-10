# T03 Independent Review｜中世纪河谷村落

## Verdict

**FAIL**

T03 的 Macro / Meso 规划有明显正向进展：河谷、水系、桥梁、聚落、农田与高差关系成立，住宅和公共建筑也比前两轮更有功能差异；但最终实机出现道路穿入建筑、多个建筑 envelope 被破坏等核心完成性错误，因此不能作为可接受成品通过。

## Owner 实机证据

Owner 明确反馈：

1. 道路直接穿入房间；
2. 多处房屋结构不完整；
3. 高低差成立，但部分建筑通过强行抬高和大面积石台实现，观感不自然；
4. 已开始出现花草，但整体自然植被密度仍明显不足。

## Positive Evidence

- 河流、桥梁、坡地、条田与聚落建立了真实的整体空间骨架；
- 高差开始实际影响玩家视野与村落层次；
- v1.2 的 Vanilla Detail Vegetation 规则产生了真实行为变化：本轮开始使用 short grass、fern、oxeye daisy、poppy；
- Controlled Material Language 有改善，材料 palette 比 T01/T02 丰富；
- Anti-Parametric-Repetition 有改善，不同功能建筑开始采用不同体量和构造逻辑；
- Construction Integrity Sweep 被模型实际实现，不再只做方块写入成功检查。

## Findings

### T03-F01｜Road–Building Destructive Collision

**Classification:** `SKILL_GAP + MODEL_EXECUTION_FAILURE`  
**Severity:** Critical

道路生成逻辑会直接清除路径上方的方块以获得净空，但没有先检查建筑 envelope，因此后施工道路可以破坏已经完成的住宅。现有道路 QA 只验证道路是否净空，甚至可能把“道路已经把墙挖掉”错误判为通行成功。

**Action:** 在 Skill 中增加 `System Interface Integrity`：后施工系统不得无意破坏前序系统，重点检查 circulation ↔ architecture、terrain ↔ architecture、water ↔ architecture、vegetation ↔ circulation / architecture。

### T03-F02｜Building Envelope Regression

**Classification:** `SKILL_GAP + MODEL_EXECUTION_FAILURE`  
**Severity:** Critical

最终未重新验证主要建筑的 roof / exterior walls / floor / intended openings / entrances / vertical circulation，因此无法区分有意开敞与后续施工造成的破坏。

**Action:** Final Spatial Review 增加 `Building Envelope Integrity`。

### T03-F03｜Forced Elevation / Platformization

**Classification:** `SKILL_GAP + MODEL_EXECUTION_FAILURE`  
**Severity:** Major

模型通过为建筑硬编码不同标高、整块填石和清平矩形平台来满足 Anti-Flatness，产生“建筑架在人工石台上”的过度纠偏。此前 T02 已出现类似平台化倾向。

**Action:** 增加 `Anti-Forced-Elevation`：高差必须来自连续地形或明确功能因果，优先 fit building to terrain，而不是先定建筑标高再强迫地形服从。

### T03-F04｜Detail Vegetation Improved but Coverage Too Low

**Classification:** `MODEL_EXECUTION_FAILURE + SKILL_GAP`  
**Severity:** Major

v1.2 已成功促使模型使用原版花草，但整体环境仍是大片 grass block + 少量植物散点。野花不应成为唯一“丰富植被”手段。

**Action:** 将植被要求从“有树草花”提升为 `Layered Vegetation`：canopy / understory / herbaceous / groundcover / seasonal accents 按场景职责形成层级与覆盖。

### T03-F05｜Structural Vegetation Still Point-Based

**Classification:** `MODEL_EXECUTION_FAILURE`  
**Severity:** Major

乔木仍主要以离散坐标单株分布，没有充分形成林缘、树篱、河岸树群、密度梯度和树林背景。该问题已跨 T01–T03 重复出现。

**Action:** Skill 继续强化植被层级和密度变化，但不要引入固定间距或数量规则。

### T03-F06｜Road Engineering Overreach

**Classification:** `TASK_SPECIFIC_JUDGMENT / MODEL_EXECUTION_FAILURE`  
**Severity:** Moderate

部分道路采用过厚石基和完整 gravel 路面，产生强人工工程感。村落道路应有主路、土路、小径的层级，并尽量顺坡，仅在必要处 cut/fill。

**Action:** 暂不写入通用 Skill，继续观察其它题材。

### T03-F07｜River Edge Too Hard

**Classification:** `TASK_SPECIFIC_JUDGMENT`  
**Severity:** Moderate

河流整体布局成立，但部分岸线偏槽化、硬边化，缺少泥岸、砾滩、草岸、河岸植物和侵蚀过渡。

**Action:** 暂不写入通用 Skill。

### T03-F08｜Perceptual QA Gap Persists

**Classification:** `TOOLING_LIMITATION + MODEL_EXECUTION_FAILURE`  
**Severity:** Major

软件体素透视和几何 QA 没有充分暴露真实客户端里的道路穿房、屋顶材质权重和建筑破损观感。真实 Minecraft 客户端截图 / 玩家视角仍是不可替代的验收证据。

## v1.2 Regression Assessment

| v1.2 新规则 | T03 结果 |
|---|---|
| Vanilla Detail Vegetation | 有效，但覆盖不足 |
| Ground Plane | 部分有效 |
| Controlled Material Language | 明显改善 |
| Anti-Parametric-Repetition | 明显改善 |
| Construction Integrity Sweep | 已实施，但检测范围过窄，发生严重 false negative |

## Skill Update Decision

T03 后允许提前更新 Skill，因为本轮发现并非只重复旧问题，而是暴露了 v1.2 新规则执行后的系统性缺口。更新应保持 bounded，不加入村落专用细则。

纳入下一版的通用修订：

1. `System Interface Integrity`；
2. `Building Envelope Integrity`；
3. `Anti-Forced-Elevation`；
4. `Layered Vegetation`。

不纳入：固定植物数量、固定道路宽度、特定河岸做法、特定屋顶材料等题材性规则。
