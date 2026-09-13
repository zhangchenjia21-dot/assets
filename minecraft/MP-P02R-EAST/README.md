# MP-P02R-CIV001 EAST

东域山地共同体系统，`REGIONAL_SYSTEM`，`minecraft-planner v0.3`。

状态：`HANDOFF_READY / AWAITING GPT + OWNER REVIEW`。这里的成熟度指可以进入下一层调查规划，不代表候选地已可建设。`world writes = 0`。

建议先看：

1. [区域规划](区域规划.md)：完整因果逻辑、地表影响、需求、容量与边界。
2. [地表与规模图](maps/地表差异与候选规模.png)、[候选同范围比较](maps/候选区域同范围比较.png)。
3. [规划数据](planning-data.json)、[三个SETTLEMENT交接包](implementation-packages.json)。
4. [Critic与Gate](Critic与Gate.md)、[Completion Report](Completion%20Report.md)。

地图目录另有地形、植被采样和关系线地形探针。双圆是等面积规模上下限，不是建成轮廓；框是搜索窗；虚线不是已证道路；南部03/04互斥且未启动可为0。

## 复现与审计

- sources/skill 是实际读取的冻结 v0.3 与必要references副本，来源文件未修改。
- sources/parent-package.json 是唯一父规划的必要摘取；sources/natural-atlas-subset.jsonl 只含相交NGEO/NHYD自然对象。
- sources/source-register.json 记录输入SHA256、仓库revision、权限与使用范围；artifact-sha256.json记录本轮产物。
- 在当前assets检出目录布局下，用Python（NumPy、Pillow、Windows微软雅黑）依次运行 `地表证据分析.py`、`规划产物生成.py`、`产物验证.py`。第一次脚本将获准R1 gzip解压到工程MP-P02R-cache，SHA不符立即退出；不上传重复原始DB。
- 原始R1数据在同仓库 `minecraft/建筑师/research/human-geography/southern-island/WB-002R-R1/raw-or-queryable/`。缓存不是证据authority，必须由登记的原始来源生成。
- 没有打开Minecraft存档或调用世界写入工具。脚本只读取归档调查，写本任务目录与独立缓存。
- 程序只做统计、制图、引用/算术/确定性验证，不判定规划语义质量或回归PASS/FAIL。

当前游戏实存、土层、稳定饮水、矿点、产能与连续可用路线未验证。输入为已接受自然调查快照，不冒充今日实时实机观测。完成后停止，不执行下一层Planner。
