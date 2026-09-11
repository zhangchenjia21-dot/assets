# T07 Independent Review｜绿洲商队驿站

## Verdict

**PASS_WITH_FINDINGS**

T07 未发现影响交付的道路穿模、建筑包络破坏、孤立重型几何、水体侧漏/缺底或重大可达性错误。作为 T01—T07 主回归的最终样本，本轮证明 minecraft-builder v1.5 已能在干旱题材中保留有意义的开放空间，并根据环境降低植被/花卉密度，而不是机械执行“填满空地”或 Flower Abundance Bias。

主要剩余问题已从 Macro/Meso 空间正确性转向建筑形态成熟度、真实客户端感知 QA 和局部自然地形完成度。

## Positive regression evidence

### T07-P01｜Meaningful openness 成立

沙漠外围与商路保留大面积空旷，绿洲、水源、棕榈、农田和驿站形成资源中心，没有因为 Space Use / Vegetation 规则而过度填充环境。

### T07-P02｜Flower Abundance Bias 未发生过度泛化

本轮主动采用低花量/低植被密度，与干旱生态和人工灌溉范围一致。说明 v1.5 的花卉强化至少在该题材中仍能被环境因果覆盖。

### T07-P03｜Terrain / Circulation / System Interface 稳定

道路生成没有使用大包络 clear 去切割已建对象；建筑未由无因果高台托起；北脊在 Macro 审核后增加冲蚀沟以打断连续等高层。后续施工发现树根修复截断暗渠后又进行最小范围水系恢复。

### T07-P04｜Water QA 表述更严谨

静态检查覆盖床岸、水位、连通和侧漏/缺底，但明确保留 `fluid stability unverified`，没有再把几何连通性冒充 Vanilla fluid update 证据。

### T07-P05｜Material vocabulary 较此前丰富

主驿站及附属设施使用 sandstone / cut sandstone / smooth sandstone / terracotta / brick / packed mud / wood / wool 等材料并按基础、开口、屋面、轻型棚架和道路分工；当前主要问题已经不是“没有 palette”。

## Findings

### T07-F01｜Box-dominant architectural massing

**Classification:** MODEL_EXECUTION_FAILURE + SKILL_GAP_WATCH  
**Severity:** Moderate

Owner 实机观察为“建筑全都是火柴盒”。代码证据支持这一感受：主驿站首先以四个长方体翼部形成主体，管理房和仓房也主要通过通用 `house()` 生成矩形实体。虽然 Meso 阶段加入桶拱屋顶、主伊万、尖拱门楼、内向拱廊、窗洞及市场棚架，局部截面语言已经不是纯立方体，但整体 silhouette / massing 仍然主要由矩形盒体决定。

这与历史 caravanserai 的正交围合原型并不冲突，因此不能简单禁止矩形体量。真正缺少的是“在合理正交原型内形成建筑层级”：门楼突出、伊万深度、角部/入口体量、不同翼高、拱顶与屋面轮廓、露台/女儿墙、服务建筑组合等没有充分进入整体天际线。

建议后续 Skill 候选补充 `Architectural Massing & Silhouette`：Facade Articulation 解决墙面近中距离问题，而 Massing 负责远中距离体量。建筑不应仅靠“box + facade details”完成；对题材允许的建筑，应利用功能和结构产生 volume hierarchy、recess/projection、roofline variation、tower/iwan/vault/courtyard edge 等三维轮廓。但不应把“非方盒”写成普遍硬要求，真实仓房、堡垒、商队驿站本就可高度正交。

### T07-F02｜Typological research authority 偏弱

**Classification:** TASK_SPECIFIC_JUDGMENT  
**Severity:** Minor

设计研究实际主要依赖 Wikipedia 的 Caravanserai / Qanat、FAO 椰枣资料和 Tabas 地理资料。事实提取总体合理，且明确区分了未读取的二手引用；但核心建筑类型缺少直接的遗产机构、建筑测绘、考古或平面资料支持。若未来 Canon Build 使用具体历史建筑语言，建议至少取得一项更高权威的平面/剖面/遗产资料作为主要形态依据。

### T07-F03｜自然岩脊仍有残余 heightfield / voxel terrace 感

**Classification:** MODEL_EXECUTION_FAILURE  
**Severity:** Minor

Codex 已在 Macro 审核后主动增加三条冲蚀沟并打断连续等高层，明显响应 Natural Terrain Morphology；Completion Report 仍承认北脊部分坡面存在方块层级。说明规则有效，但自然地貌建模仍未完全达到成熟水平。当前不建议继续扩写 Skill 微规则，更适合作为模型执行能力观察项。

### T07-F04｜真实客户端 Perceptual QA 仍缺失

**Classification:** TOOLING_LIMITATION  
**Severity:** Moderate / persistent

最终证据仍来自体素软件渲染，非 Minecraft 客户端实机截图；流体也没有受控 Vanilla tick。几何和系统 QA 已明显成熟，但材质、阴影、方块实际模型、视觉重复和玩家近距离审美仍主要依赖 Owner 实机发现。该问题不能继续通过增加 Skill 文本完全解决，未来更值得增强客户端截图/指定视点/流体更新等观察工具。

### T07-F05｜Micro finishing 仍属于基础层

**Classification:** TASK_SPECIFIC_JUDGMENT / FUTURE_FINISHER_SCOPE  
**Severity:** Minor

本轮已有货物、干草、坐席、照明、市场棚架、田间桥板等 Micro 内容，足以让空间功能可读，但距离展示级成品仍有明显余量。建议保持 Builder 的边界，不继续把大量家具、杂物、生活痕迹、细部装饰塞进 minecraft-builder；这些更适合未来独立 `minecraft-finisher` / `minecraft-detailer` 阶段。

## T07 summary

T07 的核心反向测试通过：

- 沙漠空旷可以被保留为有意义的环境尺度；
- 植被集中于水源和灌溉区；
- 花卉强化没有被机械泛化；
- 驿站、水源、农业、市场、商路及休息功能形成一个完整节点；
- 系统完整性和 QA 未出现前几轮的重大回归。

当前最明显的跨题材建筑问题已从“材料少/墙面空”进一步收敛为 **architectural massing / silhouette 仍偏基本盒体**。建议在 T01—T07 总审计后再决定是否将该项加入下一版本 Skill，而不是立即修改 v1.5。
