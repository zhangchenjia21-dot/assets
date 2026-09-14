# 复现与核验

仅工程外围脚本，不建立业务模块或四层空壳。规划语义保存在主JSON/Markdown；脚本只验证数据、画图和封存，不选择城址，不代替模型Critic。业务脚本中文命名，注释说明只读与封存不变量。没有跨模块内部import、向上依赖、Builder调用或世界API。

环境：Python 3.12、NumPy、Pillow；字体Windows msyh.ttc。实际版本与字体哈希见validation/PRIMARY-CHECKS.json。R1 raw默认从原assets检出既存raw-or-queryable读取，只用mode=ro的SQLite和NPZ；缺失时按R1归档恢复到外部缓存并验证hash，不重新扫世界。

在本计划目录执行：

```powershell
python tooling/规划图复现.py --raw-cache '<R1 raw-or-queryable绝对路径>' --output '<独立输出目录>'
python tooling/封存核验.py verify
```

第一条会核验两份raw哈希、revision154、逐格无重叠完整覆盖及各域地形/表层汇总，再绘制五图。比较独立输出的visual文件SHA256与PRIMARY-FREEZE。字体或Pillow不同可能改变PNG字节，需披露；不得因此替换封存。

`check`只检查引用/字段/图规格，不代表语义PASS。`freeze`只用于首次Primary生成后，拒绝覆盖已有封存；日常审核不要调用freeze。后续Legacy比较、最终验证、COMPLETION不在主方案哈希集合中。git属性保持任务目录字节不改换行。

没有提供自动重写主文案命令：模型的选择与假说就是需要审核的源。原始缓存默认Local-only；Git只保存小汇总、图、引用、脚本与哈希。
