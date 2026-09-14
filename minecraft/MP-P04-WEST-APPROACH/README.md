# MP-P04｜西接坡交割与修理前沿

`minecraft-planner v0.4` · DISTRICT · HANDOFF_READY · 等待GPT + Owner审核。

四处家庭混合用地、一处共同短储、两处共享空间、四条通路，组成西首卸—东轻载街区。当前4户条件分支，并集1,457 blocks²；不把上游不确定性改成既有事实。

- [Completion Report](Completion%20Report.md)：完整逻辑与边界。
- [planning-data](planning-data.json)：block、parcel、frontage、lane、shared space、约束与面积。
- [growth-and-demand](growth-and-demand.json)：行动者、节奏、演化与反馈。
- [L4交接包](implementation-packages.json)。
- [主图](maps/街区地块与通行.png)、[剖面](maps/通路与高差剖面.png)、[阶段01](maps/阶段01-交割起因.png)、[阶段02](maps/阶段02-条件常住.png)。
- [自检/Gates](Critic%20and%20Gates.md)、[来源](sources/source-register.json)、[校验](validation.json)、[文件哈希](manifest.json)。

`python 街区规划与制图.py` 可凭本归档重建JSON与图；依赖NumPy、Pillow和微软雅黑字体。不要在未审阅代码与来源前覆盖本轮已归档结果。

`街区只读调查.mjs` 是本轮调查复现入口，仅在原只读快照与源世界指纹一致时读取；不运行游戏。通常无需重跑，`evidence/near-ground.json.gz`已保留全部4543列×29层状态。`surface-crop.json.gz`是地表裁剪事实，不是世界存档。

`world writes = 0`，不修改Canon、Skill、既有规划或Minecraft存档；未判断Skill回归PASS/FAIL。
