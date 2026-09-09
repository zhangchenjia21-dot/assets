# WB-002R-R1｜Completion

**IMPLEMENTATION COMPLETED / READY FOR INDEPENDENT REVIEW**。不自行宣布 Stage PASS，不授权文明、Architecture Bible 或 Build。

## 范围完成

执行起点为当前 main `bc96aa5`；保留期间并行项目提交 `44b7de0`，本轮提交接续其后。

范围从 [-800,1376,415,2655] 自适应扩展为 **[-800,1376,2463,3487]**，向东+2048、向南+832格。目标东部主陆体实际 bounds **[-349,1453,2091,3214]**，面积 **1,674,373 blocks²**，四边均不接触study boundary。

```text
scope_status = CLOSED_WITHIN_STUDY
scope_complete = true
east_mountain_landmass_touches_study_boundary = false
east_topological_identity = independent closed surface island
world writes = 0
```

东岛包含其西伸低地半岛，不连接更大陆地。西部 C 形两翼属于同一独立低岛；不能把两个低地视觉空间先验当成两个独立岛。小到单柱的外围陆体全部保留，不将2,102个干陆分量机械等同于2,102个地理学岛屿。

逐轮范围和接触记录见研究目录 `manifest/expansion-trace.json`。追加带发现一个 `initialize_light` 区块，读取器拒绝接受；利用实际 full 区块余带即已闭合目标。全过程未生成新区块。最后续读的238个区块是单次恢复量，完整新增量为20,848，差别在修正说明中明确保留。

## 增量与统一画像

交付目录：[`WB-002R-R1/`](../../research/human-geography/southern-island/WB-002R-R1/)

- 6,893,568根水平1格柱，26,928个source chunks，430,848个四格植被样点。
- 旧西部12个region哈希全部匹配WB-002R current epoch，直接复用1,556,480柱/6,080区块，无无意义重扫。
- 新增读取5,337,088柱/20,848区块，统一绑定本轮初始current epoch。最终source region哈希在scope与SQLite中可查。
- 全矩形全部干陆2,256,681 blocks²；其中两大主体2,249,736，外围细小成员6,945，均进入全范围统计及查询。
- 完整干陆中位Y128、最高Y300、平地21.70%；西岛中位Y66/平地67.65%，东岛中位Y149/平地5.99%。
- X/Y Pearson r=0.64295，OLS约+5.764Y/100X；存在东岸下降等局部反例。
- 2,102个干陆、739个真实水区间分量；493个平地、1,674个缓坡分量。西岛表层内水1,207柱，东岛8,894柱。

2～5类候选已比较。选择两个水陆边界明确的研究参考单元 `SIRZ-R1-001/002`，保留内部连续梯度；未确认恰好三区。每单元包含实际RLE成员、biome、高程/坡度/起伏、平地、植被、水关系、置信度和predecessor关系，均为`NOT_WORLD_CANON`。外围小岛礁单独索引，不伪分配到主岛。

## H-01～H-05

| 假说 | 正确全范围 verdict |
|---|---|
| H-01 温带 / 枯树为主 | PARTIALLY_SUPPORTED；稀疏叶冠与非雨林有支持，温带和枯树优势未建立 |
| H-02 多山少平原 | SUPPORTED；东部主体高起伏，全范围平地约21.7% |
| H-03 总体西低东高 | SUPPORTED；全域经度带和两主体高差共同支持 |
| H-04 西侧两个岛片集中平地 | PARTIALLY_SUPPORTED；西部集中成立，两个独立低岛表达不成立 |
| H-05 恰好三个潜在部族区域 | INSUFFICIENT；差异明确，但稳定三分区及其硬边界未建立 |

机器evaluation逐项区分scope、Owner observation、machine observation、derived evidence、interpretation与verdict；旧WB-002R局部evaluation原样嵌入保留。没有用旧低岛H-02/H-05否定完整岛群的Owner观察。

## 验证与交付方式

- **504根独立标量NBT原始柱核验通过**，含东扩区域、东岛轮廓极值和最高Y300点；不调用生产向量解码器。
- 独立union-find重建全矩形水陆图，与生产BFS分量双射一致。
- SQLite integrity、全source provenance、旧观测表复用一致性、全部RLE重建、对象/zone/内水引用、全范围H绑定、范围硬门均通过。
- 100个随机窗口中的31个干陆窗口独立检查relief/slope；其余为水柱，未冒充干陆验证样例。
- 7类标准库CLI用例确定性与2个错误路径通过；JSON/JSONL实际成员及profile与主库一致。CLI显式输出UTF-8。
- 固定observed输入完整derive+build后，**主SQLite与所有profile JSON/JSONL byte-identical**，见`validation/rebuild.json`。
- 两个SQLite均以无损gzip归档，SHA256、round-trip和integrity通过；恢复命令为`python tooling/Bootstrap/归档命令.py restore`，见`manifest/store.json`。未提交超限未压缩SQLite、完整存档或Mods。
- 11张离线地图已目视检查方向、比例、闭合轮廓、低地/山地差异和候选分区；未启动游戏补截图。
- 工具语法/四层向下依赖检查通过；历史工具仅作为独立版本来源，没有修改或直接import历史内层。

最终源封口时间 **2026-09-09 11:07:14 UTC**：`world_unchanged_since_start=true`，完整inventory/hash/size/mtime一致，V1 / NG-2 / NG-3 / WB-002R全部immutable。读取与seal均使用不弱于前序的GENERIC_READ / FILE_SHARE_READ保护。证据见`validation/source-audit.json`。

## 停止点

本轮只提交本Completion、R1研究目录及current机械状态回写。没有创建文明、种族、部族、国家、宗教或政治边界；没有进入Architecture/Build，也没有推导矿产、农业、人口、港口或航运。

提交并push到assets/main，核对远端HEAD后停止。下一步仅交GPT独立审核，尤其复核完整范围、自然参考单元与H-05解释；不自动恢复CIV-001。
