# MP-P02｜CIV-001 东域区域规划

`REGIONAL_SYSTEM` · `HANDOFF_READY / AWAITING GPT + OWNER REVIEW` · `world writes = 0`

- [完整区域规划](区域规划方案.md)
- [可切换图册](区域图册.html)
- [区域网络](maps/01.png) · [北部规模](maps/02.png) · [东南条件规模](maps/03.png) · [条件生长](maps/04.png) · [通道剖面](maps/05.png)
- `planning-objects.json`、`settlement-capacity.json`：三个有效候选、通道、容量与撤销候选。
- `implementation-packages.json`：三个 SETTLEMENT Planner 包，非 Builder 包。
- `demand-model.json`、`growth-sequence.json`、`building-program.json`、`parent-delta.json`：因果与上游差异。
- `evidence/`：地形口袋、严格/宽松通道、撤点对比及自然 Atlas 子集。
- `source-register.json`、`validation.json`：[Completion Report](Completion%20Report.md)。

父包只作为本次 regression 上游，未升级 Canon。世界写入、既有规划和 Skill 修改均为零。

## 复现

依赖 Python、NumPy、Pillow 与 Windows 微软雅黑。脚本路径以当前 assets 检出为基准：

```powershell
python minecraft/MP-P02-EAST/区域地形分析.py
python minecraft/MP-P02-EAST/区域通道检验.py
python minecraft/MP-P02-EAST/区域规划生成.py
python minecraft/MP-P02-EAST/归档验证.py
```

原始数据引用现有 R1 归档，不重复上传。解压缓存位于 AI工程/MP-P02-cache，SQLite 只读连接。区域代码不访问 Minecraft 存档。

图中通道是阻力分析的搜索线，不是已建或工程可用道路；面积圆是量级符号，不是城界。实存、饮水、生计、资源与通达是 L2 的必需查证事项。
