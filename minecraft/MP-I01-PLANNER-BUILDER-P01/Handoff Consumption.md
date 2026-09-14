# Planner → Builder handoff consumption

实际读取：builder-design-packages.json仅BDP-00、BDP-01；未读取BDP-02，也未打开MP-P05 Planning Packet、Critic and Gates、Independent Review或MP-P04/更上游完整规划。此任务的对话上下文含上一轮资料，但不将其作为补充设计输入。场地只取压缩方块事实及其world-read provenance，不读取Planner的区域分配mask或规划图。

| 实际消费字段 | 用法 / 权限 |
|---|---|
| BDP-01 why、program_requirements、upstream_anchors_flows | 修理/值守+一户完整生活；顾客西来手提流，仅作为方向关系，不虚构公共路坐标 |
| spatial_envelope、envelope_semantic | 151列地块候选边界，不当作房屋轮廓；Builder生成82列体量 |
| required_access TH-01/02 search_line、observed_nearest_ground_y、height_rule | 限定营业与家庭入口候选段；实测事实复核后选地坪顶132/133；不是冻结门洞 |
| required_adjacency | 工作近接单、家庭通私院、不借另一户私域；Z1/Z2只作为关系名，未从外部补读mask |
| capacity | 一户，55–85列为非强制设计预算；两名居民是Builder假设 |
| planner_fixed | 公共通行、独立家庭空间、不扩界/增户、普通分段适应和现状保护作为固定关系 |
| builder_adaptable | 自主选择体量、层数、平剖面、结构、屋面、窗口、材料与院内线路 |
| architecture_kit_requirements | 编译为东域石基/木楼层/贴坡经营家庭，不复制相邻建筑 |
| known_uncertainty、dependencies、upstream_issue_protocol | 保留权利/供给/基底/通行条件；区分本户能力与P02事项，不替邻户验证 |
| BDP-00 scope、spatial_envelope_refs、planner_fixed、implementation_note | 接口联审在建筑冻结前；名义2/3格宽不当作实测路线；不生成整片公院 |

Builder自主设计包括：一户两人、低工作翼与高两层主屋、82列占地、两入口、北侧单格直梯、北西折转小院、石木结构、南北双坡屋面、两铺和日需/修理体积。所有这些均为本轮设计提案，不改Canon或Planner归档。

## Upstream planning issue：INCOMPLETE_HANDOFF

**HI-01｜公共接口无法定量联审。** BDP-00给出LANE-04与LANE-02接点编号、名义宽度，却没有线位、地面/路面高程、有效宽度范围、可调整边界、TH-01/02对接断面与接口版本。BDP-01入口搜索段与地表Y不能代替整条公共路径。这使“门前不侵占公共通行”和“先接口联审再冻结”无法同时完成证实。

已考虑的有界适应：门位选在搜索段内、门前落脚尽量收进本户、两体量顺不同高程、向内开门、不生成公共道路。这些保护措施仍不能证明未知公共路的连续性，因此不能静默认定联审完成。

最小补充：TH-01/02附近公共通行带的坐标/断面/设计高程与可协调范围；与相邻包共用的版本和谁负责协同。不要求读完整MP-P04或修改上游规模。

**HI-02｜地界离散化和排水接口。** BDP-01提供连续斜边多边形，却没有明确整格方块跨边界的容差；本轮遵循与151列面积一致的列中心核算，两个超界中心列已退掉，仍不能声称每个方块体积都严格在连续界内。需确认列中心用地还是全体积退让规则。公共侧雨水出口也未在BDP-00中给定，本轮保留需协同出口，不假定把水直接排到公共路合理。

**非阻断缺项**：Z1-FLEX_BUILDING_SEARCH / Z1-PRIVATE_YARD没有形状；因Builder有内部占地与院落重划权限，本轮按语义自主设计，不回读补形。C-SUPPLY、C-RIGHTS是明确继承的待证条件，不假装缺失已解决。P02的容量与私院不是本轮要完成的工作。

结果：建筑方案和设计模型已经形成；设计冻结保留接口HOLD。不是判断规划本身必然失败，也不是集成测试PASS/FAIL。
