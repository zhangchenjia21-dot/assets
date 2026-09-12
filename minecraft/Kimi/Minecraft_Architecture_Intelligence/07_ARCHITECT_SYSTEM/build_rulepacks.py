# -*- coding: utf-8 -*-
"""
build_rulepacks.py — P5 生成 Architect Rulepack 与 Critic Rulepack 的 JSON 产物。

设计原则（对应 CONTEXT.md 铁律 4 与任务书 15/16/20 节）：
- 每条规则的 source 必须可追溯到 $OUT 内真实产物：
  * 04_GRAMMARS/style_rules.json / functional_rules.json 的 rule_id
  * 05_SPATIAL_VALIDATOR/validator_rules.json 的 V001–V012（阈值原样引用）
  * 05_SPATIAL_VALIDATOR/known_limitations.md 的盲区条目
  * CONTEXT.md 的工程上限（§7）
  * 03_TAXONOMY/label_summary.json 的分级计数
- grammar 标 UNKNOWN 的维度不生成规则，只在 rulepack 的 unknown_dimensions 登记。
- 数值类规则直接拷贝 grammar 的 median/p25/p75/min/max/sample_n，脚本不做二次加工，
  保证"抽查能对上"。

用法：
    py -3 build_rulepacks.py            # 在 07_ARCHITECT_SYSTEM 目录下运行
产物：
    architect_rules.json / critic_rules.json
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent  # Minecraft_Architecture_Intelligence
STYLE_RULES = OUT / "04_GRAMMARS" / "style_rules.json"
FUNC_RULES = OUT / "04_GRAMMARS" / "functional_rules.json"
VALIDATOR_RULES = OUT / "05_SPATIAL_VALIDATOR" / "validator_rules.json"

GEN_STATEMENT = {
    # 维度 → 生成侧祈使句模板（{stats} 由脚本填入真实统计）
    "footprint_ratio": "平面长宽比 max(x,z)/min(x,z) 建议落在 {iqr}（中位 {median}，n={n}）。",
    "height_ratio": "高宽比 size_y/max(x,z) 建议落在 {iqr}（中位 {median}，n={n}）。",
    "floor_count": "楼层数建议落在 {iqr}（中位 {median}，n={n}；楼板密度启发式）。",
    "floor_height": "层高建议落在 {iqr}（中位 {median}，n={n}）。",
    "roof_height_ratio": "屋顶高度占比（上部 stair+slab 连续带高/size_y）建议落在 {iqr}（中位 {median}，n={n}）。",
    "roof_material_share_top3": "顶部 1/3 区域 stair+slab 材料占比建议落在 {iqr}（中位 {median}，n={n}）。",
    "roof_overhang": "屋顶出檐（顶部1/3 脚印超出中部1/3 >5%）在类内频率 {freq}，可自行取舍。",
    "roof_overhang_ratio": "出檐比例建议落在 {iqr}（中位 {median}，n={n}）。",
    "vertical_rhythm": "竖向节奏（5 等分质量分布归一化熵，1=均匀）建议落在 {iqr}（中位 {median}，n={n}）。",
    "symmetry": "对称性 max(sym_x, sym_z) 建议落在 {iqr}（中位 {median}，n={n}）。",
    "symmetry_high": "高对称（≥0.9）样本频率 {freq}。",
    "window_density": "窗密度（玻璃体素/暴露面估计）建议落在 {iqr}（中位 {median}，n={n}）。",
    "palette_wood_ratio": "wood 材料族占比建议落在 {iqr}（中位 {median}，n={n}）。",
    "palette_stone_ratio": "stone 材料族占比建议落在 {iqr}（中位 {median}，n={n}）。",
    "palette_glass_ratio": "glass 材料族占比建议落在 {iqr}（中位 {median}，n={n}）。",
    "palette_decorative_ratio": "decorative 材料族占比建议落在 {iqr}（中位 {median}，n={n}）。",
    "palette_top_blocks": "高频方块参考类内聚合 Top 列表（见 stats.value）。",
    "material_transition": "底/中/顶主导材料族模式参考众数（见原规则 statement；频率 {freq}）。",
    "wall_thickness": "墙厚估计建议落在 {iqr}（中位 {median}，n={n}）。",
    "cantilever_frequency": "二层出挑在类内频率 {freq}，可自行取舍。",
    "chimney_frequency": "烟囱候选在类内频率 {freq}，可自行取舍。",
    "foundation_stone_base": "石质基座（底部20% 石≥55%）在类内频率 {freq}。",
    "foundation_bottom_family": "底部 1/3 主导材料族参考众数（见原规则 statement；频率 {freq}）。",
}

ROOF_DIMS = ["roof_height_ratio", "roof_material_share_top3", "roof_overhang", "roof_overhang_ratio"]
PALETTE_DIMS = ["palette_wood_ratio", "palette_stone_ratio", "palette_glass_ratio",
                "palette_decorative_ratio", "palette_top_blocks", "material_transition",
                "foundation_bottom_family", "foundation_stone_base"]
FUNC_DIM_MAP = {  # functional 维度 → architect rulepack 类别
    "required_zones.enclosed_interior": "function_rules",
    "required_zones.exterior_door": "function_rules",
    "optional_zones.upper_floor": "function_rules",
    "optional_zones.courtyard": "function_rules",
    "public_private_separation": "function_rules",
    "entrance_relation.exterior_door_count": "function_rules",
    "vertical_access.presence": "function_rules",
    "vertical_access.means": "function_rules",
    "zone_adjacency.largest_component": "circulation_rules",
    "zone_adjacency.isolated_spaces": "circulation_rules",
    "circulation_constraints.dead_end_ratio": "circulation_rules",
    "circulation_constraints.usable_floor_area": "circulation_rules",
    "vertical_access.multifloor_requires": "vertical_access_rules",
}


def stats_str(r):
    n = r.get("sample_n")
    if "median" in r:
        iqr = "IQR[{:.4g},{:.4g}]".format(r.get("p25", float("nan")), r.get("p75", float("nan")))
        return {"iqr": iqr, "median": "{:.4g}".format(r["median"]), "n": n,
                "freq": "{:.2f}".format(r.get("frequency", 0.0))}
    return {"iqr": "—", "median": "—", "n": n, "freq": "{:.2f}".format(r.get("frequency", 0.0))}


def convert_grammar_rule(r, category, prefix):
    """把一条 grammar 规则转换成生成侧规则，数值原样保留。"""
    dim = r["dimension"]
    s = stats_str(r)
    tpl = GEN_STATEMENT.get(dim)
    statement = (tpl.format(**s) if tpl else r["statement"])
    stats = {k: r[k] for k in ("median", "p25", "p75", "min", "max", "frequency", "value") if k in r}
    stats["sample_n"] = r.get("sample_n")
    return {
        "id": f"{prefix}.{r['class']}.{dim}",
        "category": category,
        "type": r["rule_type"],
        "statement": f"[{r['class']}] {statement}",
        "source": {"dataset": str(Path(STYLE_RULES if prefix.startswith('STY') else FUNC_RULES).relative_to(OUT)),
                   "rule_id": r["rule_id"], "support": r["support"]},
        "confidence": r["confidence"],
        "basis": r["basis"],
        "applies_to": {"style": [r["class"]]} if prefix.startswith("STY") else {"function": [r["class"]]},
        "stats": stats,
        "original_statement": r["statement"],
    }


def vsrc(vid):
    return {"dataset": "05_SPATIAL_VALIDATOR/validator_rules.json", "rule_id": vid}


def hand_rule(rid, cat, rtype, statement, source, confidence, basis, applies_to, **extra):
    r = {"id": rid, "category": cat, "type": rtype, "statement": statement,
         "source": source, "confidence": confidence, "basis": basis, "applies_to": applies_to}
    r.update(extra)
    return r


def build_architect():
    style = json.loads(STYLE_RULES.read_text(encoding="utf-8"))
    func = json.loads(FUNC_RULES.read_text(encoding="utf-8"))
    val = json.loads(VALIDATOR_RULES.read_text(encoding="utf-8"))
    rules = []

    # ---------- 1. global_architecture_rules（生成即合规，映射 Validator） ----------
    g = "global_architecture_rules"
    rules += [
        hand_rule("GA-001", g, "HARD",
                  "包络约束：单边 ≤128、包络 ≤1,000,000 体素、施工上限 20,000 显式方块；超出则拆分或缩小体量。",
                  {"dataset": "CONTEXT.md", "rule_id": "CONTEXT.§7.engineering_limits"},
                  "high", "OBSERVED", {"all": True}),
        hand_rule("GA-002", g, "HARD",
                  "必须有至少一个 exterior→interior 入口（外部门 / 无门开口 / 梯子舱口之一）。"
                  "若内部为有意密封的装饰空腔，必须在提交说明中标注设计意图（Validator 无法判意图，见 known_limitations §1.3）。",
                  vsrc("V001"), "high", "HEURISTIC", {"all": True},
                  validator_params=val["V001"]["params"]),
        hand_rule("GA-003", g, "HARD",
                  "主入口门槛内外两侧各留 ≥1 格可站立接近位（净高 ≈2 格，脚部高程差 ≤1.0）；"
                  "门开在包络最底层（y=0）时按隐含地面放行，非底层悬空门会触发 V002。",
                  vsrc("V002"), "high", "HEURISTIC", {"all": True},
                  validator_params=val["V002"]["params"]),
        hand_rule("GA-004", g, "HARD",
                  "主要内部空间必须与主入口同一连通分量：主入口内侧分量应覆盖 ≥50% 内部站位；"
                  "多入口建筑须明确指定主入口（主入口选错会改变 V003 判定分子，见 VALIDATION_SPEC V003 盲区）。",
                  vsrc("V003"), "high", "HEURISTIC", {"all": True},
                  validator_params=val["V003"]["params"]),
        hand_rule("GA-005", g, "HARD",
                  "不留纯实体封闭的孤立内部空间：≥20 内部站位的封闭分量判 HARD_FAIL，9–19 判 WARNING；"
                  "隔离环上留门/活板门/梯子/栅栏门可降级为 WARNING。有意密封的空腔（墓室/树腔）需标注意图。",
                  vsrc("V004"), "high", "HEURISTIC", {"all": True},
                  validator_params=val["V004"]["params"]),
        hand_rule("GA-006", g, "HARD",
                  "门两侧沿通行轴都要有接近站位；不做贴墙假门（两侧皆实体的装饰门除外，但建议避免歧义）。",
                  vsrc("V008"), "medium", "HEURISTIC", {"all": True}),
        hand_rule("GA-007", g, "STRONG",
                  "主要通路净高 ≥2 格：低净高格（有支撑但站不直）≥12 且占内部站位 ≥35% 触发 V009 WARNING。"
                  "装饰性夹层/阁楼暗格无法与通道压抑区分，应有意控制规模。",
                  vsrc("V009"), "medium", "HEURISTIC", {"all": True},
                  validator_params=val["V009"]["params"]),
        hand_rule("GA-008", g, "STRONG",
                  "围护完整：内部空气与外部空气的 6 邻接泄漏（排除门/开口周边 1 格）≥10 格且 ≥2% 内部空气触发 V010。"
                  "无玻璃的开窗 = 真实泄漏，无法与设计性开口区分——窗洞应用玻璃/玻璃板/活板门填充，或接受 WARNING。",
                  vsrc("V010"), "medium", "HEURISTIC", {"all": True},
                  validator_params=val["V010"]["params"]),
        hand_rule("GA-009", g, "STRONG",
                  "内部空间上方要有屋顶覆盖：无屋顶柱 ≥12 且占内部柱 ≥20% 触发 V011。"
                  "天井/中庭是设计性露天室内，会触发——如属有意设计请在说明中标注。",
                  vsrc("V011"), "medium", "HEURISTIC", {"all": True},
                  validator_params=val["V011"]["params"]),
        hand_rule("GA-010", g, "SOFT",
                  "控制内部死端数量：度数为 1 的内部站位 ≥6 计 INFO、≥15 计 WARNING（V012）。"
                  "壁龛/房间尽头是合法死端，本规则只作统计提示。",
                  vsrc("V012"), "medium", "HEURISTIC", {"all": True},
                  validator_params=val["V012"]["params"]),
        hand_rule("GA-011", g, "STRONG",
                  "主要动线不要依赖红石机关：关闭的铁门 = 阻挡（即使有按钮/拉杆），关闭的非铁质活板门 = 半格实体，"
                  "Validator 不建模机关语义（known_limitations §1.4）。非铁质门与栅栏门视为可交互开启、可通过。",
                  {"dataset": "05_SPATIAL_VALIDATOR/known_limitations.md", "rule_id": "KL.§1.4"},
                  "high", "OBSERVED", {"all": True}),
        hand_rule("GA-012", g, "SOFT",
                  "蓝图不含地形：入口与楼梯底部尽量落在包络最底层（y=0，按隐含地面放行）或在下方提供支撑体；"
                  "悬在包络内半空的入口/梯底会真实触发 V002/V005（known_limitations §1.1）。",
                  {"dataset": "05_SPATIAL_VALIDATOR/known_limitations.md", "rule_id": "KL.§1.1"},
                  "high", "OBSERVED", {"all": True}),
        hand_rule("GA-013", g, "SOFT",
                  "不要依赖玩家跳跃/游泳/潜行通过主要动线：模型不认跳上 1 格、不认 1.5 格潜行通道（known_limitations §1.5）。"
                  "跑酷式设计会被判断裂。",
                  {"dataset": "05_SPATIAL_VALIDATOR/known_limitations.md", "rule_id": "KL.§1.5"},
                  "high", "OBSERVED", {"all": True}),
    ]

    # ---------- 2. style_selection_rules ----------
    c = "style_selection_rules"
    rules += [
        hand_rule("SS-001", c, "HARD",
                  "按 brief 的 style 标签检索 style_rules.json 对应 class 的规则块；样本纪律：n≥8 SUPPORTED，"
                  "4–7 PROVISIONAL，<4 OBSERVATION ONLY（不形成规则）。",
                  {"dataset": "04_GRAMMARS/style_rules.json", "rule_id": "sample_discipline"},
                  "high", "OBSERVED", {"all": True}),
        hand_rule("SS-002", c, "STRONG",
                  "SUPPORTED 风格（Medieval n=19 / Rustic n=20 / Fantasy n=10）：规则按标注的 STRONG/SOFT/OPTIONAL "
                  "与 confidence 使用，数值取 median 与 IQR[p25,p75]。",
                  {"dataset": "04_GRAMMARS/grammar_confidence_report.md", "rule_id": "GCR.§1.style"},
                  "high", "OBSERVED", {"style": ["Medieval", "Rustic", "Fantasy"]}),
        hand_rule("SS-003", c, "SOFT",
                  "PROVISIONAL 风格（Japanese n=7 / Chinese n=4）：全部规则按咨询性使用，输出必须标注 "
                  "'grammar 置信度低（PROVISIONAL）'，优先落在 IQR 内而非追求 median。",
                  {"dataset": "04_GRAMMARS/grammar_confidence_report.md", "rule_id": "GCR.§1.style"},
                  "medium", "OBSERVED", {"style": ["Japanese", "Chinese"]}),
        hand_rule("SS-004", c, "HARD",
                  "回退策略：brief 风格落在 Other（n=7 异质，仅观测）或零样本风格（Modern/Industrial/Gothic/"
                  "Victorian/Nordic 全库 0 样本）时，无 style grammar 可用——只用 global_architecture_rules + "
                  "functional grammar + LLM 自由发挥，并在交付说明中标注 'style grammar 无背书'，禁止编造风格数值规则。",
                  {"dataset": "03_TAXONOMY/style_taxonomy.json", "rule_id": "not_built_zero_sample"},
                  "high", "OBSERVED", {"style": ["Other", "Modern", "Industrial", "Gothic", "Victorian", "Nordic", "Unknown"]}),
        hand_rule("SS-005", c, "SOFT",
                  "brief 风格歧义时（参考库以 conf<0.55 降级为 Unknown 的判例存在）：先向需求方确认或显式声明所假设的"
                  "风格标签，再检索 grammar；不要把 Unknown 风格当类别检索（Unknown n=56 是非类别）。",
                  {"dataset": "03_TAXONOMY/label_summary.json", "rule_id": "thresholds.style_conf_floor"},
                  "medium", "OBSERVED", {"all": True}),
        hand_rule("SS-006", c, "HARD",
                  "UNKNOWN 维度不编规则：window_rhythm 规律性与 entrance_placement 对全部 5 个风格类均 UNKNOWN；"
                  "floor_height 对 Medieval/Fantasy/Chinese UNKNOWN；floor_count 对 Chinese UNKNOWN。"
                  "这些维度交给 LLM 自由发挥或人工判断，rulepack 不提供数值（见 unknown_dimensions 清单）。",
                  {"dataset": "04_GRAMMARS/grammar_confidence_report.md", "rule_id": "GCR.§2"},
                  "high", "OBSERVED", {"all": True}),
        hand_rule("SS-007", c, "STRONG",
                  "功能类别回退：Gate/Blacksmith/Farm/Mixed-use/Warehouse 样本 <4（OBSERVATION ONLY，0 条规则）；"
                  "Inn n=5、Civic n=4、Workshop n=7、Vehicle n=7 为 PROVISIONAL。功能 grammar 缺失时回退到 "
                  "global_architecture_rules + 同类 SUPPORTED 功能（Residential/Castle/Tower 等）作参考，并标注回退来源。",
                  {"dataset": "04_GRAMMARS/grammar_confidence_report.md", "rule_id": "GCR.§1.function"},
                  "high", "OBSERVED",
                  {"function": ["Gate", "Blacksmith", "Farm", "Mixed-use", "Warehouse", "Inn", "Civic", "Workshop", "Vehicle"]}),
    ]

    # ---------- 3~6. grammar 转换（roof / palette / function / circulation / vertical） ----------
    for r in style["rules"]:
        if r["dimension"] in ROOF_DIMS:
            rules.append(convert_grammar_rule(r, "roof_rules", "STY.ROOF"))
        elif r["dimension"] in PALETTE_DIMS:
            rules.append(convert_grammar_rule(r, "palette_rules", "STY.PAL"))
    # roof 形制 UNKNOWN 的显式登记（一条元规则，防编造）
    rules.append(hand_rule(
        "STY.ROOF.UNKNOWN.roof_form", "roof_rules", "HARD",
        "屋顶形制（坡顶/歇山/悬山/攒尖/平顶等）与坡度曲线未被 grammar 测量，全风格 UNKNOWN："
        "不得编造数值规则，交由 LLM 依据风格常识与参考蓝图预览自由发挥，或人工指定。",
        {"dataset": "04_GRAMMARS/grammar_confidence_report.md", "rule_id": "GCR.§2"},
        "high", "UNKNOWN", {"all": True}))

    for r in func["rules"]:
        cat = FUNC_DIM_MAP.get(r["dimension"])
        if cat:
            rules.append(convert_grammar_rule(r, cat, "FUNC"))

    # ---------- circulation / vertical 的生成侧补充（对齐 V001–V007/V012） ----------
    c = "circulation_rules"
    rules += [
        hand_rule("CIR-G-01", c, "HARD",
                  "主入口开门后应直接进入或经短门厅进入主要空间；不要把主入口开进与主空间断开的附属小房间"
                  "（图上虽连通但主分量占比会被拉低，触发 V003）。",
                  vsrc("V003"), "high", "HEURISTIC", {"all": True}),
        hand_rule("CIR-G-02", c, "STRONG",
                  "非设计性死路控制：走廊尽头应是房间/楼梯/门窗之一；内部死端站位 <15（V012 WARNING 阈值），"
                  "并参照功能类的 dead_end_ratio 中位数（见 circulation_rules 中 FUNC.*.dead_end_ratio 各条）。",
                  vsrc("V012"), "medium", "HEURISTIC", {"all": True},
                  validator_params=val["V012"]["params"]),
        hand_rule("CIR-G-03", c, "SOFT",
                  "'出后门绕行再进侧门' 在连通图上算连通（V003/V004 不判不可达），但语义上是劣质动线——"
                  "内部空间之间应有内部通道，绕行外廊只作补充（VALIDATION_SPEC V003 盲区，生成侧自律）。",
                  {"dataset": "05_SPATIAL_VALIDATOR/VALIDATION_SPEC.md", "rule_id": "V003.blind_spot"},
                  "medium", "HEURISTIC", {"all": True}),
    ]
    c = "vertical_access_rules"
    rules += [
        hand_rule("VA-G-01", c, "HARD",
                  "楼梯底部必须可进入：楼梯簇最底层至少一格有合法站位，且相邻站位高程 ≤ 底格高程+0.55"
                  "（可走上/平级踏上），该邻居不能是同簇更高一级。底格全在 y=0 时按隐含地面放行。",
                  vsrc("V005"), "high", "OBSERVED", {"all": True},
                  validator_params=val["V005"]["params"]),
        hand_rule("VA-G-02", c, "HARD",
                  "楼梯顶部必须有落点+净高——'楼梯尽头是墙' 的生成侧预防：顶格至少一格可走出，"
                  "即存在邻居高程 > 顶格+0.05（继续向上），或高程 ≥ 顶格−0.05 且支撑为非楼梯实体（平台/半砖落点）；"
                  "顶格上方 2 格内不得被实体埋住（无 headroom 判 WARNING，顶格有站位但无出口判 HARD_FAIL）。"
                  "生成时先放落点平台，再接楼梯。",
                  vsrc("V006"), "high", "OBSERVED", {"all": True},
                  validator_params=val["V006"]["params"]),
        hand_rule("VA-G-03", c, "STRONG",
                  "不要让楼梯顶部唯一出口是关闭的活板门舱口：模型里关着的活板门是半格实体，V006 会判堵"
                  "（玩家实际可翻开，但静态判定不降级，见 known_limitations §2 V006 行）。",
                  {"dataset": "05_SPATIAL_VALIDATOR/known_limitations.md", "rule_id": "KL.§2.V006"},
                  "high", "OBSERVED", {"all": True}),
        hand_rule("VA-G-04", c, "HARD",
                  "多层 ⇒ 有效垂直连接：可用楼层（内部站位 ≥6，层高容差 0.6）≥2 时，各层站位必须与第一层同连通分量；"
                  "楼梯簇需 size≥3、y_span≥2、底部接入主流通才被计为'有通行意义'（V005/V007 共用口径）。",
                  vsrc("V007"), "high", "HEURISTIC", {"all": True},
                  validator_params=val["V007"]["params"]),
        hand_rule("VA-G-05", c, "SOFT",
                  "梯柱（ladder）井两侧若通向不同房间，同高程的多个站位都会被连接到上下级（P2 已修复为完全二部连接），"
                  "但仍建议梯井出口处留 1 格平台，避免出口即墙。",
                  {"dataset": "05_SPATIAL_VALIDATOR/VALIDATION_SPEC.md", "rule_id": "SPEC.§3.fix2"},
                  "medium", "OBSERVED", {"all": True}),
    ]

    # ---------- 8. validator_precheck（生成后提交前自检，逐项对应 V001–V012） ----------
    precheck_items = [
        ("PC-V001", "V001", "是否存在至少一个入口候选（外部门/无门开口/梯子舱口）？",
         "无入口且 interior_air≥27、interior_stances≥9 → HARD_FAIL"),
        ("PC-V002", "V002", "主入口门槛内外是否各有可站立接近位（高程差 ≤1.0）？",
         "缺任一侧 → HARD_FAIL；舱口接近问题只 WARNING"),
        ("PC-V003", "V003", "从主入口出发能否到达 ≥50% 的内部站位？",
         "可达占比 <0.5 且不可达 ≥9 站位 → HARD_FAIL（隔离环有可交互构件降 WARNING）"),
        ("PC-V004", "V004", "是否存在主分量之外 ≥9 内部站位的封闭空间？",
         "9–19 站位 WARNING；≥20 且纯实体封闭 HARD_FAIL"),
        ("PC-V005", "V005", "每个有通行意义的楼梯簇底部是否至少一格可进入？",
         "底格全不可进入 → HARD_FAIL"),
        ("PC-V006", "V006", "每个楼梯簇顶部是否至少一格可走出（平台/上行）且有净高？★重点自检",
         "顶格有站位无出口 → HARD_FAIL；顶格被实体埋住 → WARNING"),
        ("PC-V007", "V007", "若 ≥2 个可用楼层，是否都有垂直连接与第一层同分量？",
         "任一层断开 → HARD_FAIL"),
        ("PC-V008", "V008", "每扇门沿通行轴两侧是否都有接近站位？",
         "任一侧缺失 → WARNING"),
        ("PC-V009", "V009", "主要通路净高是否 ≥2 格？",
         "低净高格 ≥12 且占内部站位 ≥35% → WARNING"),
        ("PC-V010", "V010", "窗洞是否已用玻璃/活板门填充？围护是否有非设计性缺口？",
         "泄漏 ≥10 格且 ≥2% 内部空气 → WARNING"),
        ("PC-V011", "V011", "内部空间上方是否有屋顶覆盖？（有意天井请标注）",
         "无屋顶柱 ≥12 且 ≥20% 内部柱 → WARNING"),
        ("PC-V012", "V012", "内部死端站位数量统计？",
         "≥6 INFO；≥15 WARNING"),
    ]
    for pid, vid, question, threshold_note in precheck_items:
        rules.append(hand_rule(
            pid, "validator_precheck", "HARD" if val[vid]["severity"] == "HARD_FAIL" else "STRONG",
            f"提交前自检（对应 {vid}，severity={val[vid]['severity']}）：{question}",
            vsrc(vid), "high", val[vid]["basis"], {"all": True},
            validator_severity=val[vid]["severity"],
            validator_params=val[vid]["params"],
            fail_condition=threshold_note))

    unknown_dimensions = {
        "style": {
            "window_rhythm": {"classes": ["Medieval", "Rustic", "Fantasy", "Japanese", "Chinese"],
                              "reason": "窗洞位置节奏需立面聚合，P3 阶段 UNKNOWN", "handling": "LLM 自由发挥/人工"},
            "entrance_placement": {"classes": ["Medieval", "Rustic", "Fantasy", "Japanese", "Chinese"],
                                   "reason": "main_entrance 可判定样本过少（全库 89% UNKNOWN）", "handling": "LLM 自由发挥/人工"},
            "floor_height": {"classes": ["Medieval", "Fantasy", "Chinese"],
                             "reason": "可得样本不足半数或 <4", "handling": "LLM 自由发挥/人工"},
            "floor_count": {"classes": ["Chinese"], "reason": "可得样本 3/4 不足", "handling": "LLM 自由发挥/人工"},
            "roof_form": {"classes": ["Medieval", "Rustic", "Fantasy", "Japanese", "Chinese"],
                          "reason": "屋顶形制/坡度曲线未测量", "handling": "LLM 自由发挥/人工"},
            "all_dimensions": {"classes": ["Other", "Modern", "Industrial", "Gothic", "Victorian", "Nordic"],
                               "reason": "Other 异质仅观测；其余全库 0 样本", "handling": "回退策略见 SS-004"},
        },
        "function": {
            "entrance_relation.方位": {"classes": ["Residential", "Decoration", "Castle", "Tower", "Religious",
                                                   "Workshop", "Vehicle", "Inn", "Civic"],
                                       "reason": "main_entrance 可判定样本过少", "handling": "LLM 自由发挥/人工"},
            "all_dimensions": {"classes": ["Gate", "Blacksmith", "Farm", "Mixed-use", "Warehouse"],
                               "reason": "样本 <4，OBSERVATION ONLY", "handling": "回退策略见 SS-007"},
        },
    }

    pack = {
        "version": "P5-1.0",
        "generated_by": "07_ARCHITECT_SYSTEM/build_rulepacks.py",
        "rule_type_legend": style.get("rule_types"),
        "basis_legend": {"OBSERVED": "数据实测", "HEURISTIC": "启发式", "INFERRED": "推断", "UNKNOWN": "数据不足不编规则"},
        "categories": {
            "global_architecture_rules": "任何建筑通用：落地/围护/入口/净高等，映射 Validator 使生成即合规",
            "style_selection_rules": "按 brief 检索 grammar 与样本不足时的回退策略",
            "function_rules": "功能分区/出入口/垂直交通有无，转换自 functional_rules.json",
            "circulation_rules": "主入口→主空间连通与死端控制，对齐 V001–V004/V012",
            "vertical_access_rules": "楼梯底可进/顶有落点+净高，对齐 V005/V006/V007",
            "roof_rules": "屋顶比例/出檐，转换自 style grammar；形制 UNKNOWN 不编规则",
            "palette_rules": "材料族比例与高频方块，带 sample_n 与 IQR",
            "validator_precheck": "生成后提交前自检清单，逐项对应 V001–V012",
        },
        "unknown_dimensions": unknown_dimensions,
        "rules": rules,
    }
    return pack


def build_critic():
    """Critic：判断性评审。HEURISTIC 规则的量化指标引用 grammar/validator 真实统计；LLM_ONLY 不给阈值。"""
    R = []
    def cr(rid, dim, rtype_check, statement, severity, revision, source=None, metric=None):
        R.append({
            "id": rid, "dimension": dim, "statement": statement,
            "check": rtype_check, "severity": severity,
            "revision_template": revision,
            "source": source or {"dataset": None, "rule_id": None, "note": "critic_judgment（无 grammar 数值来源）"},
            **({"metric": metric} if metric else {}),
        })

    # spatial hierarchy
    cr("CR-SH-01", "spatial_hierarchy", {"kind": "HEURISTIC"},
       "体量主次：单盒包络（footprint_ratio≈1）且无可识别次级体量/凹凸时，提示缺乏空间层级。",
       "suggestion",
       "修改建议：拆分或附加一个次级体量（侧翼/门廊/塔），形成主-次关系；参考 V4 B 的 L 形主次体量做法。",
       source={"dataset": "AI-Test/Architecture-V4/B-design.md（只读参考）", "rule_id": "B.§1.Macro"},
       metric={"signal": "footprint_ratio≈1 且包络填充率高、无次级脚印", "threshold": "定性阈值，供程序初筛"}),
    cr("CR-SH-02", "spatial_hierarchy", {"kind": "LLM_ONLY"},
       "主入口应在接近方向上可辨认（门廊/踏步/灯光/凹口等手段）。",
       "important",
       "修改建议：用门廊、双柱、踏步、灯光或偏心罩棚强调主入口；参考 V4 C 的 'Minecraft readability' 行。",
       source={"dataset": "AI-Test/Architecture-V4/C-critique.md（只读参考）", "rule_id": "C.Minecraft_readability"}),
    # circulation quality
    cr("CR-CQ-01", "circulation_quality", {"kind": "HEURISTIC"},
       "死端比例超过所属功能类 IQR 上界（p75）时提示动线碎片化。",
       "suggestion",
       "修改建议：打通尽端走廊成环路，或把死端改造为房间；对照 circulation_rules 中 FUNC.{function}.dead_end_ratio。",
       source={"dataset": "04_GRAMMARS/functional_rules.json", "rule_id": "FUNC.{function}.circulation_constraints.dead_end_ratio"},
       metric={"signal": "dead_end_ratio > class p75", "threshold": "按功能类 p75 取值"}),
    cr("CR-CQ-02", "circulation_quality", {"kind": "LLM_ONLY"},
       "语义动线合理性：图上连通 ≠ 动线合理（如必须穿卧室到厨房、出后门再进侧门）。Validator 不判此类问题。",
       "important",
       "修改建议：调整门位/走廊使公共-私密动线分离；参照 CIR-G-03。",
       source={"dataset": "05_SPATIAL_VALIDATOR/VALIDATION_SPEC.md", "rule_id": "V003.blind_spot"}),
    # function coherence
    cr("CR-FC-01", "function_coherence", {"kind": "HEURISTIC"},
       "可用楼面面积显著低于所属功能类 p25 时，提示功能容量不足。",
       "important",
       "修改建议：扩大楼面或增加楼层；对照 FUNC.{function}.circulation_constraints.usable_floor_area。",
       source={"dataset": "04_GRAMMARS/functional_rules.json", "rule_id": "FUNC.{function}.circulation_constraints.usable_floor_area"},
       metric={"signal": "usable_floor_area < class p25", "threshold": "按功能类 p25 取值"}),
    cr("CR-FC-02", "function_coherence", {"kind": "LLM_ONLY"},
       "功能分区语义：grammar 不识别房间语义（bedroom/kitchen），分区合理性只能 LLM 判断（公私分层假设为 INFERRED）。",
       "suggestion",
       "修改建议：住宅类优先'公共首层/私密上层'；对照 FUNC.{function}.public_private_separation（INFERRED）。",
       source={"dataset": "04_GRAMMARS/functional_rules.json", "rule_id": "FUNC.{function}.public_private_separation"}),
    # style coherence
    cr("CR-SC-01", "style_coherence", {"kind": "HEURISTIC"},
       "材料族占比偏离所属风格 IQR（wood/stone/glass/decorative 四项中 ≥2 项出界）时提示风格漂移。",
       "important",
       "修改建议：把偏离材料族占比调回 STYLE.{style}.palette_*_ratio 的 IQR 内；PROVISIONAL 风格仅作参考。",
       source={"dataset": "04_GRAMMARS/style_rules.json", "rule_id": "STYLE.{style}.palette_*_ratio"},
       metric={"signal": "≥2 个材料族占比超出 IQR", "threshold": "按风格类 IQR 取值"}),
    cr("CR-SC-02", "style_coherence", {"kind": "LLM_ONLY"},
       "风格元素一致性：混搭多种风格语汇（如中式瓦顶+中世纪木框架）只能语义判断。",
       "suggestion",
       "修改建议：统一主导风格语汇；风格为 UNKNOWN/零样本时不评此项（无 grammar 背书）。",
       source={"dataset": "03_TAXONOMY/style_taxonomy.json", "rule_id": "not_built_zero_sample"}),
    # proportion
    cr("CR-PR-01", "proportion", {"kind": "HEURISTIC"},
       "高宽比超出所属风格 IQR 时提示比例异常（如 Fantasy 类 median 0.82，超出 [0.72,1.23] 需注意）。",
       "suggestion",
       "修改建议：调整高度或面宽使 height_ratio 回到 STYLE.{style}.height_ratio 的 IQR；塔楼类功能可豁免。",
       source={"dataset": "04_GRAMMARS/style_rules.json", "rule_id": "STYLE.{style}.height_ratio"},
       metric={"signal": "height_ratio 出 IQR", "threshold": "按风格类 IQR 取值"}),
    cr("CR-PR-02", "proportion", {"kind": "HEURISTIC"},
       "平面长宽比超出所属风格 IQR 时提示平面比例异常。",
       "suggestion",
       "修改建议：调整平面使 footprint_ratio 回到 STYLE.{style}.footprint_ratio 的 IQR。",
       source={"dataset": "04_GRAMMARS/style_rules.json", "rule_id": "STYLE.{style}.footprint_ratio"},
       metric={"signal": "footprint_ratio 出 IQR", "threshold": "按风格类 IQR 取值"}),
    # facade rhythm
    cr("CR-FR-01", "facade_rhythm", {"kind": "LLM_ONLY"},
       "窗洞位置节奏：grammar 全风格 UNKNOWN（P3 未做立面聚合），不提供阈值，只由 LLM 从预览判断开窗是否有节奏感。",
       "suggestion",
       "修改建议：对齐窗洞列/层节奏或有意打破；UNKNOWN 维度，评审时注明无数据背书。",
       source={"dataset": "04_GRAMMARS/grammar_confidence_report.md", "rule_id": "GCR.§2.window_rhythm"}),
    cr("CR-FR-02", "facade_rhythm", {"kind": "HEURISTIC"},
       "窗密度超出所属风格 IQR 时提示开窗过密/过疏。",
       "suggestion",
       "修改建议：调整玻璃用量使 window_density 回到 STYLE.{style}.window_density 的 IQR。",
       source={"dataset": "04_GRAMMARS/style_rules.json", "rule_id": "STYLE.{style}.window_density"},
       metric={"signal": "window_density 出 IQR", "threshold": "按风格类 IQR 取值"}),
    # roof massing
    cr("CR-RM-01", "roof_massing", {"kind": "HEURISTIC"},
       "屋顶高度占比超出所属风格 IQR 时提示屋顶体量异常（过平或过高）。",
       "suggestion",
       "修改建议：调整屋顶带高度使 roof_height_ratio 回到 STYLE.{style}.roof_height_ratio 的 IQR。",
       source={"dataset": "04_GRAMMARS/style_rules.json", "rule_id": "STYLE.{style}.roof_height_ratio"},
       metric={"signal": "roof_height_ratio 出 IQR", "threshold": "按风格类 IQR 取值"}),
    cr("CR-RM-02", "roof_massing", {"kind": "LLM_ONLY"},
       "屋顶形制与风格的匹配（坡度曲线、歇山/悬山/攒尖等）：grammar 未测量形制，LLM 依据风格常识判断。",
       "suggestion",
       "修改建议：调整屋顶形制；UNKNOWN 维度，评审时注明无数据背书。",
       source={"dataset": "04_GRAMMARS/grammar_confidence_report.md", "rule_id": "GCR.§2.roof_form"}),
    # material transition
    cr("CR-MT-01", "material_transition", {"kind": "HEURISTIC"},
       "底部 1/3 主导材料族与所属风格众数不一致时提示基座材料异常（如 Medieval 众数 stone，频率 0.89）。",
       "suggestion",
       "修改建议：基座改用类内众数材料族；对照 STYLE.{style}.foundation_bottom_family。",
       source={"dataset": "04_GRAMMARS/style_rules.json", "rule_id": "STYLE.{style}.foundation_bottom_family"},
       metric={"signal": "bottom_family != class mode", "threshold": "按风格类众数"}),
    cr("CR-MT-02", "material_transition", {"kind": "LLM_ONLY"},
       "材料过渡质量：竖向底/中/顶过渡是否有层级（承重石→结构木→填充），还是随机噪声铺色。",
       "important",
       "修改建议：建立材料层级而非随机点缀；参考 V4 B '材料层级' 与 C 'Material hierarchy'。",
       source={"dataset": "AI-Test/Architecture-V4/C-critique.md（只读参考）", "rule_id": "C.Material_hierarchy"}),
    # repetition
    cr("CR-RP-01", "repetition", {"kind": "LLM_ONLY"},
       "过度重复：等距复制同一窗饰/构件且各立面无差异时提示（V4 C 实测问题：'庭院下层百叶等距重复'）。",
       "suggestion",
       "修改建议：打破机械重复，用有识别度的入口或变异构件替换部分重复单元。",
       source={"dataset": "AI-Test/Architecture-V4/C-critique.md（只读参考）", "rule_id": "C.Repetition"}),
    cr("CR-RP-02", "repetition", {"kind": "HEURISTIC"},
       "对称性偏离所属风格典型区间时提示（如 Rustic 高对称频率 0.0，做成高对称即偏离类内常态）。",
       "suggestion",
       "修改建议：对照 STYLE.{style}.symmetry 与 symmetry_high；有意对称（如宗教类）可豁免并注明。",
       source={"dataset": "04_GRAMMARS/style_rules.json", "rule_id": "STYLE.{style}.symmetry_high"},
       metric={"signal": "symmetry 出 IQR 或高对称与类内频率矛盾", "threshold": "按风格类统计"}),
    # visual focal point
    cr("CR-VF-01", "visual_focal_point", {"kind": "LLM_ONLY"},
       "是否存在可识别的视觉焦点（入口强调/塔/脊线/烟囱）；全立面均质无焦点时提示。",
       "suggestion",
       "修改建议：增加或强化一个焦点构件；烟囱频率可参考 STYLE.{style}.chimney_frequency。",
       source={"dataset": "04_GRAMMARS/style_rules.json", "rule_id": "STYLE.{style}.chimney_frequency"}),
    cr("CR-VF-02", "visual_focal_point", {"kind": "HUMAN_REVIEW"},
       "审美最终裁决归 Owner：Critic 不判'丑'，不自动宣称改后更美（V4 纪律：'规则满足不等于美观自动通过'）。",
       "suggestion",
       "修改建议：所有 aesthetic 争议项提交人工评审，附修改前后对比说明。",
       source={"dataset": "AI-Test/Architecture-V4/B-design.md（只读参考）", "rule_id": "B.§末"}),

    return {
        "version": "P5-1.0",
        "generated_by": "07_ARCHITECT_SYSTEM/build_rulepacks.py",
        "scope_declaration": {
            "validator": "回答'有没有客观错误'（确定性检查，V001–V012）",
            "critic": "回答'即使可用，设计是否合理'（判断性评审）",
            "prohibitions": [
                "Critic 不重复 Validator 的客观错误检查（V001–V012 触发项直接进 Revision，不在 Critic 重复裁决）",
                "Critic 不评'丑'或任何纯审美贬损；审美终裁归人工（CR-VF-02）",
            ],
        },
        "check_kind_legend": {
            "HEURISTIC": "可程序化检查：给量化指标与阈值（阈值引自 grammar/validator 真实统计）",
            "LLM_ONLY": "只能由模型判断：不给阈值，评审时必须注明是否有数据背书",
            "HUMAN_REVIEW": "需人工裁决",
        },
        "severity_legend": {"suggestion": "可权衡", "important": "强烈建议修改", "critical": "接近必须修改（本 pack 暂无 critical；客观必须项归 Validator HARD_FAIL）"},
        "rules": R,
    }


def main():
    arch = build_architect()
    crit = build_critic()
    (HERE / "architect_rules.json").write_text(
        json.dumps(arch, ensure_ascii=False, indent=1), encoding="utf-8")
    (HERE / "critic_rules.json").write_text(
        json.dumps(crit, ensure_ascii=False, indent=1), encoding="utf-8")

    # 自检：所有 grammar 来源的 rule_id 必须真实存在
    style_ids = {r["rule_id"] for r in json.loads(STYLE_RULES.read_text(encoding="utf-8"))["rules"]}
    func_ids = {r["rule_id"] for r in json.loads(FUNC_RULES.read_text(encoding="utf-8"))["rules"]}
    val = json.loads(VALIDATOR_RULES.read_text(encoding="utf-8"))
    val_ids = {k for k in val if k.startswith("V")}
    bad = []
    for r in arch["rules"]:
        rid = r["source"].get("rule_id", "")
        ds = r["source"].get("dataset", "")
        if ds.endswith("style_rules.json") and rid not in style_ids and rid != "sample_discipline":
            bad.append((r["id"], rid))
        if ds.endswith("functional_rules.json") and rid not in func_ids:
            bad.append((r["id"], rid))
        if ds.endswith("validator_rules.json") and rid not in val_ids:
            bad.append((r["id"], rid))
    if bad:
        print("SOURCE CHECK FAILED:", bad)
        sys.exit(1)
    from collections import Counter
    cnt = Counter((r["category"], r["type"]) for r in arch["rules"])
    print("architect rules:", len(arch["rules"]))
    for (cat, t), n in sorted(cnt.items()):
        print(f"  {cat:28s} {t:9s} {n}")
    ccnt = Counter((r["dimension"], r["check"]["kind"]) for r in crit["rules"])
    print("critic rules:", len(crit["rules"]))
    for (dim, k), n in sorted(ccnt.items()):
        print(f"  {dim:22s} {k:12s} {n}")
    print("source self-check: OK")


if __name__ == "__main__":
    main()
