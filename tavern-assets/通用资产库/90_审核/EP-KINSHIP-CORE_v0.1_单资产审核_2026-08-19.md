---
title: EP-KINSHIP-CORE v0.1｜单资产审核
status: pass
date: 2026-08-19
asset: EP-KINSHIP-CORE
asset_version: 0.1
skill: tavern-asset v0.9
---

# EP-KINSHIP-CORE v0.1｜单资产审核

> [!success] 结论
> **PASS / AUDITED CURRENT。** `家族与亲缘核心 v0.1` 可以进入通用资产库稳定语义基线；当前无需要阻断的 Owner、依赖、信息边界、上下文或跨世界复用问题。

## 1. 资产身份

- 名称：家族与亲缘核心；
- 稳定 ID：`EP-KINSHIP-CORE`；
- 类型：跨世界通用 Core；
- Hard Dependency：无；
- Runtime Context Contract：正文内建；
- Creator / machine binding：等待 G9-03。

结果：**PASS。**

## 2. Canonical Ownership

本 Core 唯一拥有：

- Family / Lineage Identity；
- 生物亲本 / 后代结构；
- 收养亲本 / 后代结构；
- 正式认定亲缘；
- 人物—家系关联；
- 家系分支 / 来源；
- 谱系主张与证据引用边界；
- 亲缘图的 authoritative structure / bounded projection。

明确不拥有：Relationship 情感、ORG Role/Membership、Reputation 评价、Politics 权力 /继承结果、Law 合法性、遗传能力、生育模拟、Program Outcome。

结果：**PASS。无 duplicate owner。**

## 3. 源关系优先 / 派生关系

正式冻结：长期保存产生结构的源边，兄弟姐妹、祖孙、堂表、姻亲称谓、世代距离、共同祖先等优先程序推导。

收益：

- 避免 O(n²) pairwise 关系膨胀；
- 修正亲本事实时不需要同步大量冗余边；
- 大谱系可保持可维护。

结果：**PASS。**

## 4. 家族对象

Family Entity 为可选长期世界对象，不要求每个小家庭自动生成。Family 只负责家系身份 /谱系结构；组织职位、内部权限、财富、政治权力等仍在其它 Owner。

结果：**PASS。**

## 5. 多家系与跨文化

- 不使用单一 `family_id` 产品语义；
- 姓氏 != 家系；
- 亲本关系不写死父+母二元模型；
- 父系 /母系 /长幼只作结构描述；
- 嫡庶、长子继承、绝嗣、血统纯度不作为通用默认规则。

结果：**PASS。跨世界复用成立。**

## 6. Relationship 接缝

婚姻仍由 Relationship 拥有；Kinship 只消费已成立婚姻作为姻亲结构来源，不双写 `married=true`。

收养亲缘由 Kinship 拥有，收养双方的亲密 /疏远仍由 Relationship。

结果：**PASS。**

## 7. Truth / Claim / Knowledge

明确区分：

```text
真实亲缘结构
!= 谱系主张
!= 法律承认
!= 社会传闻 / 公共认知
!= 个人知识
```

允许真实亲缘当前未知 /存在候选 /争议，不要求系统伪造全知答案。

结果：**PASS。**

## 8. Open Attempt / Agency

认亲、收养、断亲、调查身世、否认谱系等自由尝试均允许；声明不自动成为亲缘事实。

“断绝父子关系”不能删除生物亲缘。

结果：**PASS。**

## 9. Definition / Instance / Materialization

未知父亲可作为未解析谱系位置；具体可持续互动亲属必须先成为稳定人物，再绑定亲缘。

运行中生成失散亲属时必须经过人物 materialization + Program 校验 + commit，不能由 Narrative 直接制造永久 NPC。

结果：**PASS。与当前 G9 Game-local foundation 一致。**

## 10. Program Authority

确定性谱系图查询、共同祖先、世代距离、结构校验、Formal Outcome、Commit、Save / Restore 均由 Program / Runtime 负责。

模型只承担开放语义、争议解释、候选与自然语言表达。

结果：**PASS。**

## 11. Runtime Context Contract

18 项已全部内建。

重点通过：

```text
Whole Kinship Graph != Model Prompt
Family Members ↑↑↑ → unrelated Turn context ≈ stable
Genealogy Depth ↑↑↑ → local query context ≈ bounded by relevant path
```

模型不会为两个角色的亲缘查询读取整个 2000 人家谱。

结果：**PASS。**

## 12. UI / Creator

资产只声明人物详情 /家族详情 /未来谱系视图所需语义，不抢占当前产品一级 Surface。

Creator 只需作者化重要锚点、近亲、关键家系、谱系约束和秘密 /争议；不要求预填整个世界家谱。

结果：**PASS WITH G9-03 FUTURE BINDING。非阻塞。**

## 13. Future Explosion Review

假设：

- 2000 人家系；
- 30 代历史；
- 多次改姓、收养、分支；
- 100+ 谱系主张；
- Politics / Law / Reputation 同时消费。

要求仍成立：

- 源边而非 pairwise 冗余；
- 当前查询局部图；
- 下游只拿 bounded projection；
- 不共享整个 state；
- 不把潜在继承 /法律 /声望后果提前加载。

结果：**PASS。**

## 14. 最终裁定

| Gate | 结果 |
|---|---|
| Generic Identity | PASS |
| Canonical Owner | PASS |
| Dependency | PASS |
| Relationship Boundary | PASS |
| ORG Boundary | PASS |
| Politics / Law Boundary | PASS |
| Open Attempt | PASS |
| Program Authority | PASS |
| Information Boundary | PASS |
| Definition / Instance | PASS |
| Runtime Context 18 项 | PASS |
| Future Explosion | PASS |
| Creator Authorability | PASS WITH FUTURE G9-03 BINDING |

> **最终结果：PASS / AUDITED CURRENT。**
