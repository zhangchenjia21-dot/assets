# MP-I01R-PLANNER-BUILDER-P01

**仅设计：CONCEPT_DESIGN_WITH_INTERFACE_HOLD。等待 GPT + Owner 审核；集成回归 PASS / FAIL 未裁定。**

Builder v1.11；shared contract v1.0；共同源提交 `fc6371361685e2eeaefdef5a513f21dbe64c6696`。正式输入仅为 MP-P05R2 的 BDP-01 r1 及其允许直接依赖。

`world writes = 0`。未改 Planner、Canon、任何 Skill/shared contract 或存档。

- [建筑意图、功能、平剖面、结构和转译](建筑设计.md)
- [Handoff consumption record](handoff-consumption-record.md)
- [预览入口](设计预览.html)（下载本目录后浏览器打开；无依赖、无世界执行）
- [体量轴测](体量轴测.svg)、[作坊平面](平面-作坊.svg)、[首层平面](平面-下层.svg)、[上层平面](平面-上层.svg)
- [横剖面](剖面-家庭横向.svg)、[楼梯剖面](剖面-楼梯.svg)、[剖切轴测](剖切轴测.svg)
- [体素设计](设计体素.json)、[几何盒](设计几何.json)、[设计核验与限制](设计核验.json)、[待闭合事项](issues.json)
- [输入版本与SHA256](inputs/来源与读取记录.json)

在 Node.js 24 上，从本目录依次运行 `node 设计生成.mjs` 与 `node 制图与核验.mjs` 可离线重建模型与图纸。`输入提取.mjs` 是本机一次性输入边界审计脚本，需要原始允许路径；归档复现不需要再次读取 Planner。没有依赖安装或 Minecraft 执行步骤。

方案为低肩单坡修理作坊＋高肩双层双坡住屋，保留独立家庭廊、原24格apron和等面积移位18格小院。未闭合项包含公共接触标高/雨水受纳、基础工程判断、真实家庭规模、门扇/护栏/烟道与雨水细部，以及运行时碰撞和服务运营。

本轮仅形成可审核设计，不宣称 DESIGN_READY、建成或集成回归成功。
