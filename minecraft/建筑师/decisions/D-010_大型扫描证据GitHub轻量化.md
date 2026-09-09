# D-010｜大型扫描证据 GitHub 轻量化

状态：**OWNER DIRECTION / ACTIVE DECISION**

日期：2026-09-09

## 背景

WB-002R / WB-002R-R1 的区域高分辨率扫描产生了百万级 column、完整 SQLite / NPZ / 大型 geometry JSON 等高体积证据。本轮 R1 push 约 112MB，造成：

- Codex 归档与 push 耗时明显增加；
- GPT 独立审核面对大量并不需要逐行读取的原始数据；
- Git history 快速膨胀；
- predecessor / revision 容易重复提交相同 raw evidence。

Owner 明确要求：本轮完成并审核后，优化后续扫描类任务的 push 与审核数据负担。

## 决策

### 1. GitHub 不再默认承担完整 raw-scan 仓库职责

项目事实源仍然是 Minecraft world。

后续大型调查默认分为：

```text
Minecraft World
→ LOCAL RAW CACHE
→ LIGHTWEIGHT REVIEW BUNDLE
→ GitHub Research / Governance
```

完整逐柱 / 逐体素 / 大型中间数组默认 `LOCAL_ONLY / REGENERABLE`，不因“证据完整”而自动 push Git history。

### 2. GitHub 默认保存可审核证据，不保存所有原始行

默认应 push：

- Task / Completion；
- scope / source fingerprint / freshness / lineage；
- schema / algorithm version；
- aggregated regional profiles；
- 重要对象 / zone / major component geometry；
- key metrics；
- hypothesis evaluation；
- stratified / boundary / topology witnesses；
- validation summary；
- deterministic rebuild / query / reproduce tooling；
- 适度分辨率的阅读地图；
- raw-cache manifest（hash / size / schema / source binding / rebuild command）。

默认不 push：

- 完整 per-column observed database；
- 大型 raw NPZ / dense arrays；
- 重复 predecessor raw snapshot；
- 数万 / 数十万条仅用于证明“所有微小 component 都存在”的展开 JSON；
- 完整 cross-check 明细（改为分层样本 + summary）；
- 可以从 local raw cache / world 稳定重建的大型中间产物。

### 3. 默认体积预算

扫描类单次 GitHub research delivery：

- **目标：≤ 15 MiB**；
- **超过 25 MiB：默认不得 push，除非 Task 明确给出必要性 / 例外授权**；
- 单个 raw / database artifact 若明显主导体积，应优先转 `LOCAL_ONLY`，而不是只靠 gzip 把它塞进 Git。

这是工程治理预算，不是科学精度限制。扫描仍可在本地使用 1-block / 高分辨率。

### 4. Revision 不复制 predecessor raw evidence

R1 / R2 等修正任务必须优先：

- lineage 指向 predecessor；
- hash 验证后复用；
- GitHub 只提交 revision delta + 新的统一轻量 profile；
- 不重复上传同一大型原始快照。

### 5. Raw cache 必须可追溯

任何未 push 的关键 raw cache 至少登记：

- `cache_id`；
- logical / local path（可为空或机器相关，不作为跨机器契约）；
- SHA256；
- byte size；
- schema / format version；
- source world fingerprint / epoch；
- generated_at；
- rebuild / refresh command；
- retention：`REGENERABLE` / `PRESERVE_LOCAL`。

GitHub 中的结论必须能知道自己依赖的是哪份 raw cache，而不是只写“本地有数据”。

### 6. 世界改变后不可重建的 snapshot

如果 Minecraft world 后续发生变化，使旧 raw snapshot 无法从当前 world 重建：

- 允许标记 `PRESERVE_LOCAL`；
- GitHub 仍只保存 manifest + hash + review bundle；
- 如确需远程长期冷备，另行授权 Git LFS / Release / object storage / archive；
- **不得默认把冷备塞进 main Git history。**

### 7. GPT 独立审核采用 Review Bundle

独立审核默认检查：

```text
scope completeness
+ source fingerprint / freshness
+ methodology / code
+ key metrics
+ stratified raw witnesses
+ boundary / topology witnesses
+ deterministic rebuild
+ maps / summaries
+ uncertainty / limitations
```

不把“GPT 逐行吞取百万级 raw observation”当成审核完整性的要求。

## 生效范围

本决策适用于后续：

- Natural Geography scan；
- Regional Reconnaissance；
- resource / accessibility survey；
- build-site high-resolution observation；
- 其它会产生大型可重建机器证据的任务。

WB-002R / WB-002R-R1 已经进入 Git history 的大型 artifact 保持历史证据，不通过 force-push / history rewrite 为本决策追溯瘦身。

具体交付契约见：

`../architecture/大型扫描数据交付与审核契约.md`
