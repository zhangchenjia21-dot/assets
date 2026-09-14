# MP-P05R2｜北侧两户混合前沿

对象：MP-P04-WEST-APPROACH / r1 / PACKAGE-01。尺度：URBAN_ENSEMBLE。全新独立 L4 规划，未读取已有 L4 / Builder 答案。

交付状态：**规划与概念设计交接成果已生成，等待 GPT + Owner 审核**。本轮不判定回归 PASS / FAIL，不执行 Builder Architecture Design。`world writes = 0`。

## Owner 阅读入口

1. [组团与地形图](maps/01-组团与地形.png)：两户、家庭小院、门前、公院和东出口。
2. [完整规划说明](URBAN-ENSEMBLE.md)：为什么形成这些空间，以及仍需闭合什么。
3. [门前与公共接口图](maps/02-门前与公共接口.png)及[剖面](maps/03-地形与门前剖面.png)。
4. [交付与审核说明](交付说明.md)：自检证据、限制与审核边界。

## Builder 读取入口

读取 [builder-design-packages.json](builder-design-packages.json) 中目标 BDP-01 或 BDP-02。每包已嵌入该户地块列、空间程序、因果背景、公共接口、服务责任和未决项；无需回读完整 MP-P04，也无需读取另一户 BDP。

直接依赖为 [interface-baselines.json](interface-baselines.json)、[external-service-interfaces.json](external-service-interfaces.json) 和本目录的地表/浅层事实切片。文件 SHA256 写在 BDP 的 dependencies 内；全量交付校验见 `manifest.json`。

两个包均为 `CONCEPT_DESIGN_READY`。公共接触标高及雨水受纳等仍有设计冻结 HOLD，未声称 `DESIGN_FREEZE_READY`。此 readiness 只说明可进行何种下游工作，不是本轮回归评判或施工许可。

## Provenance

- 实际加载：minecraft-planner **v0.5**，GitHub 固定提交读取，非本地安装 Skill。
- Skill source commit：`fc6371361685e2eeaefdef5a513f21dbe64c6696`，仓库 `zhangchenjia21-dot/Vibe-Coding`。
- shared contract：**Minecraft Planner–Builder Contract v1.0**，同一提交，`skill/codex/shared/minecraft-planner-builder-contract.md`。
- 详细记录：[provenance.json](provenance.json)；参考加载清单：`sources/Skill参考加载.json`。

## 复现

Node.js 运行本目录下脚本：

```powershell
node .\规划编译.mjs
node .\规划制图.mjs
node .\交付校验.mjs
```

前三者只读本目录的白名单提取资料、写本目录派生成果。`证据提取.mjs` 是可选的原始来源复核步骤，依赖原目录及存档路径；它只读 PACKAGE-01 与公共直接对象、Canon 和世界哈希，不运行游戏、不写存档。若世界哈希不匹配，它停止而不悄悄换用新事实。

PNG 是 SVG 的栅格预览，使用本机 bundled `sharp` 转换。标准 Node 不自带 sharp；SVG 无第三方依赖即可重建和浏览。制图及检查不表示游戏内移动或建筑工程验证。

所有成果只归档在此同级新目录。既有规划、Canon、Skill 和存档均未修改。
