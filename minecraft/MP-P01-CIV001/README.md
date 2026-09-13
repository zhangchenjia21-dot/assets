# MP-P01｜CIV-001 国家尺度规划

**DESIGN_PROPOSAL / HANDOFF_READY（L0→L1）/ 等待 GPT + Owner 审核。**

- [直观规划图入口](index.html)：结构、流、关系腹地与四阶段生长。
- [完整方案](settlement-plan.md)：因果逻辑、地形、需求、层级、分支与下游边界。
- [Planner Critic](planner-critic.md)：实际修订、反事实和Gate。
- `planning-objects.json`、`growth-sequence.json`、`building-program.json`、`implementation-packages.json`：machine-readable交接。
- `source-register.json`：当前Skill、Canon入口、Natural Atlas与R1来源及隔离说明。
- `validation.json` / `SHA256.json`：坐标、引用、来源哈希与图像核验。

本轮未访问/写入世界，未修改Canon、Skill或既有规划。独立回归不自行裁定PASS/FAIL。共享会话中此前出现过项目状态摘要，本轮未作为规划输入；不声称新会话级盲测。

可复现数据准备：`生成规划.py`从既有R1 observed.sqlite.gz解压到本机缓存并核对固定SHA256，只读 samples 的标高、derived.npz的land_component/slope8，不读其人文假设表。运行顺序：生成规划.py → 整理规划包.py → 补充腹地图.py → 验证交付.py。文字方案与Critic是本轮判断的原始产物，不由算法自动裁定。

完整调查数据库沿用原仓库来源，不重复上传。地图的8格抽样不降低原调查分辨率；它仅用于国家尺度表达，不能用于建筑落位、桥址或船道判定。
