# REF-0123 正式资产入库 Independent Review

## Verdict

**PASS_WITH_NOTES — 正式参考资产入库通过。**

本轮审核目标是确认 Owner 已批准的 T12 最终修复町家是否被正确提取、转换、注册为现有参考资产体系中的单一新条目，且没有把测试环境、旧版本或未经授权的 world-write 混入正式资产。

基于 commit `5354f82291c9196f94101fad06d7048725a15781` 中的提取脚本、Canonical Blueprint、metadata / placement、Litematic、查询结果、round-trip / native validation、registry 保护证据与变更快照，本轮正式入库满足要求。

---

## 1. Approved source / lineage：PASS

正式条目为 `REF-0123｜江户后期京都呉服商町家院落`，metadata 明确记录 Owner ingest approval、T11 → T12 47-cell bounded Repair lineage 与 `minecraft-builder v1.10`，并把 Canon world-write 保持为 false。

正式提取脚本只读 `MB-V110-T12-京町家修复`，使用 RegionReader 读取真实存档，提取前后冻结并复核来源文件哈希；脚本不调用 world execute / write 接口。

47 格 T12 Repair 在最终验证中全部保留；正式 Blueprint 相对实际提取源为 0 cell difference。

### Note — client copy 与归档 reload 的 6 格自然状态漂移

隔离归档 reload 与后来用于客户端验收 / 正式提取的同名游戏副本相比，有 6 格 Y15 `grass_block → dirt`，全部位于已支承台阶下。该差异已被显式记录，正式资产选择忠实保存 Owner 实机验收后的当前实际状态，而不是偷偷把旧状态补回。

这属于可接受的 Minecraft 被遮蔽草方块状态演化，不影响结构、范围或设计语义；但 provenance 中应继续保留这条记录。

---

## 2. Asset Scope / bounding / placement：PASS

正式资产尺寸为 **29×20×74（X×Y×Z）**，来源包络 `X11..39 / Y15..34 / Z16..89`。

资产分成两个 Region：

- `GroundInterface`：28×2×72，local `(1,0,1)`；
- `MachiyaCompound`：29×18×74，local `(0,2,0)`。

这种拆分与提取脚本一致：低两层只保留地界内的直接 ground interface，上部保留完整建筑、出檐与必要空气。北侧测试街路延伸和超平坦背景没有进入正式资产。

anchor / facing / ground level 均已明确：anchor `(13,2,1)`，主入口 local `(13,3,2)`，朝北；主地面行走标高 local Y2，抬高木地板行走面 Y3。

部署说明明确要求完整放置两 Region，并把街道接续留给新 SITE 现场设计。这一点正确，避免把测试道路当成资产的一部分。

---

## 3. Canonical Blueprint / Litematic interoperability：PASS

正式 Canonical Blueprint：schema_version=1，origin `(0,0,0)`，42,660 个显式格位，12,188 个非空气方块。

验证证据支持：

- 实际来源 → Canonical：0 difference；
- Canonical → Litematic → Canonical：0 unintended diff；
- 二次 Litematic 语义比较：0 unintended diff；
- Minecraft 26.2 / DataVersion 4903 原生 Litematic 解析：2 Region、12,188 non-air，完整 block state difference = 0；
- multi-region fixture 与 building-state fixture 继续通过；
- normalization 为 `CURRENT_NATIVE`，原始与 normalized Blueprint SHA256 相同，无替换状态。

因此本资产没有通过“重新设计 / 修形”进入库，而是对 T12 最终状态做 identity-style normalization 和格式注册。

---

## 4. Stable REF / existing registry protection：PASS

注册脚本沿用既有 REF 分配机制，从 122 个既有条目之后得到 `REF-0123`，并在写入前明确断言该 ID、目录不存在。

catalog / reference-id-map / inverted-index / classification-v2 registries 采用追加方式；验证脚本确认前 122 条旧记录保持不变。

正式查询结果：

- `resolve_reference_blueprint` 返回 `REF-0123` normalized Blueprint；
- `query_references` 返回唯一 `REF-0123`；
- V2 classification 查询成功；
- compatibility = `CURRENT_NATIVE`。

这证明新资产已经进入现有 registry，而不是另造第二套资产目录或旁路 catalog。

---

## 5. Metadata / reuse contract：PASS_WITH_NOTE

metadata 对用途、风格、scale、terrain fit、features、settlement roles、dimensions、regions、provenance、Owner approval 和 placement contract 的记录足够支持后续检索与 SITE 级复用。

`asset_status = REFERENCE_ONLY` 与 `ingest_status = REGISTERED_OWNER_APPROVED` 同时存在是正确的：

- Owner 已批准 **入库**；
- 但没有自动获得任何 Canon SITE / world-write **放置授权**。

查询结果中 `approval = null` 因此不应被视为入库失败，而是维持“参考资产 ≠ 自动施工许可”的隔离边界。

### Note — classification evidence 较泛化

部分 V2 feature / reference-value evidence 使用同一条总体说明重复支撑多个字段。对于 Owner 自产并已明确知道身份的 REF-0123，这不影响注册正确性；未来如果资产分类被用于自动高风险选址 / 设计推理，可再考虑把具体 evidence 拆得更细。当前不需要返工。

---

## 6. Block entities：PASS_WITH_KNOWN_LIMITATION

来源范围内有 10 个 chest / barrel / furnace block entities。当前管线没有导出其默认 NBT，但验证确认：

- inventory = 0；
- custom components = 0；
- furnace 无燃烧 / 烹饪 / recipe progress；
- 对应方块及完整 block states 均保留。

因此没有实际内容丢失，但不能声称 NBT round-trip = 0。该限制已经进入 metadata / query warning，处理正确。

后续若某资产含有真实库存、自定义容器名、书本、告示牌、熔炉进度或其它有意义 block-entity 数据，当前基础实体策略不能直接沿用本次“空 NBT 可省略”的结论。

---

## 7. Preview / audit binding：PASS

preview 由正式 Blueprint 重新生成，而非复用 T11 / T12 旧截图；metadata 保存 source Blueprint SHA256 与五个标准视图 SHA256，最终验证确认 preview hashes match。

这保证视觉审阅对象与正式注册对象绑定一致。

---

## 8. World-write isolation：PASS

提取、转换、Litematic 原生解析和 registry 注册均记录 `world_writes = 0`。正式条目与 Approval 均继续声明：

> Reference asset registration does not authorize Canon placement.

本轮没有修改 `建筑师` 正式存档。

---

## Findings

### F01 — 6 个 grass→dirt 状态与归档 reload 不同

**Classification:** C `WORLD_STATE_EVOLUTION / PROVENANCE_NOTE`  
**Severity:** Minor.

已记录、范围明确、位于台阶支承下，正式资产忠实采用 Owner 客户端验收后的当前世界状态。无需返工。

### F02 — 10 个空 block entities 的默认 NBT 未导出

**Classification:** C `TOOLING_LIMITATION`  
**Severity:** Minor for REF-0123; potentially Major for future stateful assets.

本资产没有库存、自定义组件或炉状态，因此当前内容无实质丢失。保留 warning 即可。

### F03 — GitHub 审核对象是本地参考库的可复现快照 / 验证证据

**Classification:** C `EVIDENCE_BOUNDARY`  
**Severity:** Minor.

运行时 `AI-Blueprints/references` 位于本机工程目录，不直接由本仓库作为 live registry 使用；GitHub 保存了 REF-0123 镜像、registry 变更快照、SHA256、注册脚本与查询结果。当前证据足以审核本次入库，但第三方不能只靠 GitHub 直接调用用户本机 live registry。

---

## Release decision

**REF-0123 正式入库审核通过。**

当前可视为正式参考资产：

> `REF-0123｜江户后期京都呉服商町家院落`

保留 `REFERENCE_ONLY` 是正确状态；未来任何真实 SITE 使用仍必须经过当前建筑任务的场地设计、Preview / Gate 和 world-write 授权。

同时，结合 T11 Owner 审美验收、T12 物理修复闭环与本次正式资产入库验证，`minecraft-builder v1.10` 继续维持 **Production Pilot baseline**，无需因本次资产化再修改 Skill。
