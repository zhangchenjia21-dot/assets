# TT-002R｜Completion

**REFINED_DRAFT / AWAITING GPT + OWNER ACCEPTANCE**

以 assets/main `bb3ca11ca0844112ea7aefa4bfd39c4792e958a4` 为执行起点，使用 Owner 指定附件 `D:/Download/TT-002R-owner-draft-rev153.json`。schema、revision 153、source.id 和六类面积全部匹配；原样复制到任务要求的 input 路径，没有再次应用 66 格 cleanup。

## 成果

入口：[TT-002R README](../../research/human-geography/southern-island/territory-refinement/TT-002R/README.md)。

任务包要求的 baseline-owner-draft.json、refined-draft.json、boundary-delta.json、八段解释报告、四张比较图、summary / geometry / source-audit 均已完成。另有独立 RLE 校验、地形与通达性对照、确定性重建哈希和复现脚本。完整 raw 与中间诊断数组保留本地。

仅在 Z1895–2090 内谷东缘有证据支持的三段移动边界，其余五段保持 Owner 原线。候选仅在原切口 ±48 格搜索，使用东西高差、slope8、relief32 和偏移惩罚；近似同分优先原线附近。无数学平滑、单一等高线、面积均衡或全三域自动重分。

- Middle → East：**4,142 列**；East → Middle：**0**。
- Middle：395,144 → **391,002**；East：1,194,016 → **1,198,158**。
- 新主线相对 Owner 边界最大欧氏位移：**30.9233 格**；>64 格段为空。
- Commons：**92,124** 不变；accepted connector：**13,661** 不变；West：**575,397** 不变。
- 全部有效陆地 **2,256,681** 守恒，无未分配或争议洞。
- Middle / East 分量数仍为 **2 / 2,088**，次级分量完全不变，未新增飞地。

## 验证与边界

逐列验证覆盖唯一性与守恒、锁定成员、改动条带和非主边界不变；独立脚本不导入生成器。生成结果及四张 PNG 重建字节一致；459 个前序 research / World Canon / architecture 文件前后哈希一致。四图已目视检查。

**world writes = 0；new world block reads = 0；broad rescan = 0。** 使用既有 cache epoch，不宣称当前运行世界同步。无聚落、道路、建筑设计，无 Canon 替换；current 状态仅机械回写为等待审核。

研究阶段曾拒绝会触碰内湖岸线并分裂主接壤线的候选，最终版本加入近岸保护和非有限值拒绝。参数、分段、短接回边和局部阶梯仍需 GPT / Owner 审核，技术检查不等于接受。

baseline 与成果按任务目录正常 commit + push 到 assets/main；推送后核对远端 HEAD。完成后停止，不进入 MD-001P 或 Build。
