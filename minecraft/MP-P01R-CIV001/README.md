# MP-P01R｜CIV-001 国家尺度规划

状态：`HANDOFF_READY / AWAITING GPT + OWNER REVIEW`。`world writes = 0`。

- [国家级规划方案](国家级规划方案.md)：可独立阅读的完整因果逻辑、规模、分支和下层边界。
- [规划图册](规划图册.html)：五张真实坐标图；可切换与打开原图。
- [领土结构](maps/01.png) · [流与通道](maps/02.png) · [建成规模](maps/03.png) · [服务腹地](maps/04.png) · [逻辑生长](maps/05.png)
- `planning-objects.json`：地区、六个节点、六条概念通道、公地与 anchors。
- `settlement-capacity.json`：建成面积、户压力计算、LOW 置信度；不等于现存人口或城界。
- `demand-model.json`、`growth-sequence.json`、`building-program.json`：需求与生长及下游功能接口。
- `implementation-packages.json`：四个 L1 Planner 合同，没有 Builder 授权。
- [Planner Critic](Planner%20Critic.md)、`validation.json`、`source-register.json`：自检、证据、来源与哈希。
- [Completion Report](Completion%20Report.md)：交付与限制。

## 复现

依赖 Python 3、NumPy、Pillow 和 Windows 微软雅黑字体；从 assets 检出执行：

```powershell
python minecraft/MP-P01R-CIV001/地理证据提取.py
python minecraft/MP-P01R-CIV001/规划产物生成.py
python minecraft/MP-P01R-CIV001/归档验证.py
```

原始源位于现有 R1 归档，见 source-register；不重复上传 245 MB 数据库。脚本将原始 gzip 解压到工程下新的 `MP-P01R-cache`，以只读 SQLite 模式查询自然数据。没有 Minecraft 存档访问代码。`自然底图.png` 为同一原始快照复算。最终图与数据重复生成逐字节一致。

本包只写当前任务目录和该独立临时缓存。不要将本轮图中的搜索窗或等面积圆直接拿去施工；先进入 L1 调查实存、饮水、资源、通道与容量。旧规划及评审不属于本包输入。
