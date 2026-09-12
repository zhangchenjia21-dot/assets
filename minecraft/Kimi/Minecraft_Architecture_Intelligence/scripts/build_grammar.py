# -*- coding: utf-8 -*-
"""build_grammar.py — P3 任务2：Architecture Grammar 构建器。

输入 P1 元数据（blueprint_metadata.jsonl）+ P3 标签表（labels.jsonl），
对样本充足的 style / function 类提取可执行约束（规则），全部带样本纪律分级。

样本纪律（硬性，任务书第 9 节）：
    sample_n >= 8  → SUPPORTED（允许 STRONG）
    sample_n 4–7   → PROVISIONAL（最高 SOFT）
    sample_n < 4   → OBSERVATION ONLY（不出规则，只列观测）
Other（style 异质集合）与 Unknown 不出 grammar。

规则类型（任务书第 20 节）：
    HARD=功能必需（frequency==1.0 且 n≥8 且为功能维度；style grammar 不出 HARD）
    STRONG=高频稳定（freq≥0.75 或数值分布集中 IQR/median≤0.5）
    SOFT=常见可打破（0.4≤freq<0.75 或分布较散）
    OPTIONAL=装饰倾向（freq<0.4）

用法：
    py -3 scripts/build_grammar.py \
      --metadata "02_BLUEPRINT_METADATA\\blueprint_metadata.jsonl" \
      --labels "03_TAXONOMY\\labels.jsonl" \
      --output "04_GRAMMARS" \
      --references-root "D:\\Games\\...\\references\\derived" \
      --palette-dictionary "02_BLUEPRINT_METADATA\\palette_dictionary.json"

--references-root 省略时，IR 衍生维度（roof/material_transition/wall_thickness/chimney）
全部标 UNKNOWN。只读参考库；产出只写 --output。
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_blueprint_metadata import load_palette_dictionary, material_family  # noqa: E402

OBSERVED, HEURISTIC, INFERRED, UNKNOWN = "OBSERVED", "HEURISTIC", "INFERRED", "UNKNOWN"

# 屋顶带判定：某 y 层 楼梯+半砖 / 实体 ≥ 此比例 → 属于屋顶带（HEURISTIC）
ROOF_BAND_MIN_SHARE = 0.25
# 烟囱候选：柱顶高出全图柱顶 P90 至少这么多格，且四周邻居柱顶都低 ≥2 格（HEURISTIC）
CHIMNEY_MIN_RISE = 3
# 墙体扫描线：实体段长度上限（超过视为实心肌体/楼板，不计入墙厚样本）
WALL_RUN_MAX = 8

STYLE_GRAMMAR_CLASSES = ["Medieval", "Rustic", "Fantasy", "Japanese", "Chinese"]
FUNCTION_GRAMMAR_CLASSES = ["Residential", "Decoration", "Castle", "Tower", "Religious",
                            "Workshop", "Vehicle", "Inn", "Civic",
                            "Gate", "Blacksmith", "Farm", "Mixed-use", "Warehouse"]
# 缺口矩阵中出现但当前 0 样本的功能类（候选类、任务书 Q6 需要）
FUNCTION_ZERO_SAMPLE = ["Bridge"]
MATRIX_STYLES = STYLE_GRAMMAR_CLASSES  # Other/Unknown 不是设计目标，不进矩阵
MATRIX_SIZES = ["tiny", "small", "medium", "large", "monumental"]
# 村落核心但样本不足的功能（P0 优先级判定用）
CENTRAL_FUNCTIONS = ["Blacksmith", "Farm", "Warehouse", "Inn", "Civic", "Gate", "Bridge"]


# ---------------------------------------------------------------------------
# IR 衍生特征（全部 HEURISTIC，算法与盲区写入文档）
# ---------------------------------------------------------------------------
def compute_ir_features(ref_dir: Path, families) -> dict:
    """对单张蓝图计算 IR 衍生特征。全部 HEURISTIC；无法判断时值为 "UNKNOWN"。"""
    from blueprint_io import load_blueprint, to_voxels
    ir = load_blueprint(ref_dir)
    voxels, air_index = to_voxels(ir)
    X, Y, Z = voxels.shape
    bids = ir.block_ids
    air_ids = {i for i, b in enumerate(bids) if b.endswith(":air") or b.split(":")[-1] == "air"}
    solid = voxels != air_index
    if len(air_ids) > 1:
        solid &= ~np.isin(voxels, list(air_ids - {air_index}))

    feat: dict = {"ref_id": ir.ref_id or ref_dir.name}

    # stair / slab 掩码（屋顶材料信号）
    stair_slab_ids = {i for i, b in enumerate(bids) if "stairs" in b or "_slab" in b}
    roofmat = np.isin(voxels, list(stair_slab_ids)) & solid if stair_slab_ids else np.zeros_like(solid)

    # ---- roof_height_ratio（HEURISTIC：上部 stair+slab 最长连续带）----
    # 算法：在 y ≥ 0.4·size_y 范围内，找"本层 stair+slab/实体 ≥ 0.25 且本层实体 ≥3"的
    # 最长连续层带（不从最顶层起算——尖顶/装饰帽常为非楼梯方块，从顶起算会立即断裂，
    # 本次调试实测证实）；ratio = 带高 / size_y；无合格带 → 0。
    # 另报 roof_material_share_top3 = 顶部 1/3 区域 stair+slab/实体（任务书建议的屋顶材料信号）。
    # 盲区：平屋顶带长≈0–1；立面/基座装饰楼梯若在上部成带会高估；植被顶不成带（→0）；
    # 塔尖/阁楼楼梯间可能计入。该指标是"屋顶材料信号"，不是屋面几何重建。
    solid_per_y = solid.reshape(X, Y, Z).sum(axis=(0, 2))
    roof_per_y = roofmat.sum(axis=(0, 2))
    ys = np.nonzero(solid_per_y)[0]
    if len(ys) == 0:
        feat["roof_height_ratio"] = UNKNOWN
        feat["roof_note"] = "无实体"
    else:
        y_lo = int(0.4 * Y)
        best_band, cur = 0, 0
        for y in range(y_lo, int(ys.max()) + 1):
            if solid_per_y[y] >= 3 and roof_per_y[y] / solid_per_y[y] >= ROOF_BAND_MIN_SHARE:
                cur += 1
                best_band = max(best_band, cur)
            else:
                cur = 0
        feat["roof_height_ratio"] = round(best_band / Y, 4)
        top3 = slice(int(2 * Y / 3), Y)
        s3, r3 = int(solid_per_y[top3].sum()), int(roof_per_y[top3].sum())
        feat["roof_material_share_top3"] = round(r3 / s3, 4) if s3 else UNKNOWN
        feat["roof_note"] = ("上部 stair+slab 最长连续带" if best_band
                             else "上部无 stair+slab 集中带（平屋顶/无屋顶/植被顶/实心顶）")

    # ---- roof_overhang_ratio（HEURISTIC：顶部 1/3 脚印超出中部 1/3 的比例）----
    t = Y / 3.0
    mid_mask = solid[:, int(t):int(2 * t) or 1, :].any(axis=1)
    top_mask = solid[:, int(2 * t):, :].any(axis=1)
    mid_n = int(mid_mask.sum())
    overhang = int((top_mask & ~mid_mask).sum())
    feat["roof_overhang_ratio"] = round(overhang / mid_n, 4) if mid_n else UNKNOWN

    # ---- material_transition（HEURISTIC：底/中/顶三段主导材料族）----
    fam_counts = [Counter(), Counter(), Counter()]
    bounds = [0, int(t), int(2 * t), Y]
    used = np.unique(voxels[solid])
    fam_of = {i: material_family(bids[i], families) for i in used}
    for seg in range(3):
        sub = voxels[:, bounds[seg]:bounds[seg + 1], :]
        sub_solid = solid[:, bounds[seg]:bounds[seg + 1], :]
        vals, cnts = np.unique(sub[sub_solid], return_counts=True)
        for v, c in zip(vals.tolist(), cnts.tolist()):
            fam_counts[seg][fam_of.get(v, UNKNOWN)] += c
    pattern = []
    for fc in fam_counts:
        if not fc:
            pattern.append("none")
        else:
            pattern.append(fc.most_common(1)[0][0].lower())
    feat["material_transition_pattern"] = "→".join(pattern)
    feat["material_transition_count"] = sum(1 for a, b in zip(pattern, pattern[1:]) if a != b)

    # ---- wall_thickness（HEURISTIC：中部 1/3 层水平扫描线，两侧为空气的实体段中位数）----
    # 盲区：多房间隔断墙一并计入（仍是"墙"）；露天构件（栅栏/树干）短段会拉低中位数；
    # 实心肌体长段 >WALL_RUN_MAX 被排除。
    samples: list[int] = []

    def _runs(row: np.ndarray):
        n = len(row)
        i = 0
        while i < n:
            if row[i]:
                j = i
                while j < n and row[j]:
                    j += 1
                length = j - i
                left_open = i == 0 or not row[i - 1]
                right_open = j == n or not row[j]
                if left_open and right_open and 1 <= length <= WALL_RUN_MAX:
                    samples.append(length)
                i = j
            else:
                i += 1

    for y in range(int(t), max(int(2 * t), int(t) + 1)):
        layer = solid[:, y, :]
        for z in range(Z):
            _runs(layer[:, z])
        for x in range(X):
            _runs(layer[x, :])
    if samples:
        feat["wall_thickness"] = float(np.median(samples))
        feat["wall_thickness_samples"] = len(samples)
    else:
        feat["wall_thickness"] = UNKNOWN
        feat["wall_thickness_samples"] = 0

    # ---- chimney_candidate（HEURISTIC：高出柱顶 P90 的孤立细柱）----
    # 盲区：尖顶/塔尖/树梢/天线同样会触发——只作"频率倾向"，不作判定。
    col_top = np.full((X, Z), -1, dtype=int)
    for x in range(X):
        for z in range(Z):
            ys_col = np.nonzero(solid[x, :, z])[0]
            if len(ys_col):
                col_top[x, z] = int(ys_col.max())
    tops = col_top[col_top >= 0]
    if len(tops) >= 4:
        h90 = float(np.percentile(tops, 90))
        cands = 0
        for x in range(X):
            for z in range(Z):
                if col_top[x, z] < h90 + CHIMNEY_MIN_RISE:
                    continue
                isolated = True
                for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, nz = x + dx, z + dz
                    if 0 <= nx < X and 0 <= nz < Z and col_top[nx, nz] >= col_top[x, z] - 2:
                        isolated = False
                        break
                if isolated:
                    cands += 1
        feat["chimney_candidate_count"] = cands
    else:
        feat["chimney_candidate_count"] = UNKNOWN
    return feat


# ---------------------------------------------------------------------------
# 统计辅助
# ---------------------------------------------------------------------------
def num_stats(values: list[float]) -> dict:
    a = np.asarray(values, dtype=float)
    return {
        "sample_n": int(len(a)),
        "median": round(float(np.median(a)), 4),
        "p25": round(float(np.percentile(a, 25)), 4),
        "p75": round(float(np.percentile(a, 75)), 4),
        "min": round(float(a.min()), 4),
        "max": round(float(a.max()), 4),
    }


def support_tier(n: int) -> str:
    if n >= 8:
        return "SUPPORTED"
    if n >= 4:
        return "PROVISIONAL"
    return "OBSERVATION ONLY"


_TIER_ORDER = {"OBSERVATION ONLY": 0, "PROVISIONAL": 1, "SUPPORTED": 2}


def eff_tier(class_tier: str, rule_n: int) -> str:
    """规则自身的有效级别 = min(类级别, 规则自身 sample_n 级别)。
    样本纪律按规则自身 sample_n 执行：条件规则（如"多层⇒垂直交通"）只看子集 n。"""
    t = support_tier(rule_n)
    return t if _TIER_ORDER[t] < _TIER_ORDER[class_tier] else class_tier


def numeric_rule_type(stats: dict, class_tier: str) -> str:
    """数值维度：分布集中(IQR/median≤0.5)且有效级别 SUPPORTED → STRONG；否则 SOFT。"""
    tier = eff_tier(class_tier, stats.get("sample_n", 0))
    if tier != "SUPPORTED":
        return "SOFT"
    med = abs(stats["median"]) or 1e-9
    iqr = stats["p75"] - stats["p25"]
    return "STRONG" if iqr / med <= 0.5 else "SOFT"


def freq_rule_type(freq: float, class_tier: str, hard_eligible: bool = False,
                   rule_n: int | None = None) -> str:
    """频率维度。HARD 仅功能必需且 freq==1.0 且有效级别 SUPPORTED（rule_n≥8）。"""
    tier = eff_tier(class_tier, rule_n) if rule_n is not None else class_tier
    if hard_eligible and tier == "SUPPORTED" and freq >= 0.999:
        return "HARD"
    if freq >= 0.75:
        return "STRONG" if tier == "SUPPORTED" else "SOFT"
    if freq >= 0.4:
        return "SOFT"
    return "OPTIONAL"


def conf_of(basis: str, tier: str) -> str:
    if tier == "SUPPORTED":
        return "high" if basis == OBSERVED else "medium"
    if tier == "PROVISIONAL":
        return "medium" if basis == OBSERVED else "low"
    return "low"


# ---------------------------------------------------------------------------
# Style grammar
# ---------------------------------------------------------------------------
def build_style_rules(rows: list[dict], meta: dict, irf: dict, labels: dict) -> tuple[list[dict], dict]:
    """返回 (rules, per_class_unknown_dims)。rows=有标签且有元数据的样本。"""
    rules: list[dict] = []
    unknown_dims: dict[str, list[str]] = {}

    def mk(cls, dim, tier, statement, basis, stats=None, freq=None, value=None,
           rtype=None, notes=""):
        rule_n = stats["sample_n"] if stats and "sample_n" in stats else n
        tier = eff_tier(tier, rule_n)  # 规则级别按自身 sample_n 收紧
        r = {
            "rule_id": f"STYLE.{cls}.{dim}",
            "class": cls, "dimension": dim,
            "support": tier,
            "rule_type": rtype,
            "statement": statement,
            "basis": basis,
            "confidence": conf_of(basis, tier),
        }
        if stats:
            r.update(stats)
        if freq is not None:
            r["frequency"] = round(freq, 4)
            r["sample_n"] = stats["sample_n"] if stats else r.get("sample_n")
        if value is not None:
            r["value"] = value
        if notes:
            r["notes"] = notes
        rules.append(r)

    for cls in STYLE_GRAMMAR_CLASSES + ["Other"]:
        members = [r for r in rows if labels[r["ref_id"]]["style_label"] == cls]
        n = len(members)
        tier = support_tier(n)
        heterogeneous = cls == "Other"
        if heterogeneous:
            tier = "OBSERVATION ONLY"
        udims: list[str] = []
        if n == 0:
            continue

        def vals(field, fn=None):
            out = []
            for r in members:
                v = r.get(field)
                if v in (UNKNOWN, None):
                    continue
                if fn:
                    v = fn(v)
                if v is not None:
                    out.append(v)
            return out

        def irvals(field):
            out = []
            for r in members:
                v = irf.get(r["ref_id"], {}).get(field, UNKNOWN)
                if v != UNKNOWN:
                    out.append(v)
            return out

        def emit_numeric(dim, values, basis, statement, unit_note=""):
            if len(values) < max(4, n // 2):
                udims.append(f"{dim}（可得样本 {len(values)}/{n}，不足半数或 <4）")
                return
            st = num_stats(values)
            rt = numeric_rule_type(st, tier)
            st["sample_n_total"] = n
            mk(cls, dim, tier, statement, basis, stats=st, rtype=rt, notes=unit_note)

        def emit_freq(dim, hits, denom, basis, statement, hard=False, notes=""):
            if denom < 1:
                udims.append(f"{dim}（无有效分母）")
                return
            freq = hits / denom
            rt = freq_rule_type(freq, tier, hard_eligible=hard, rule_n=denom)
            mk(cls, dim, tier, statement, basis,
               stats={"sample_n": denom}, freq=freq, rtype=rt, notes=notes)

        if tier == "OBSERVATION ONLY":
            unknown_dims[cls] = ["全部维度：样本不足/异质集合，仅列观测不形成规则"]
            continue

        # 1 footprint_ratio
        emit_numeric("footprint_ratio",
                     [max(r["size_x"], r["size_z"]) / max(1, min(r["size_x"], r["size_z"])) for r in members],
                     OBSERVED, f"{cls} 平面长宽比 = max(x,z)/min(x,z)，1.0=方形", "OBSERVED 自包络尺寸")
        # 2 height_ratio
        emit_numeric("height_ratio",
                     [r["size_y"] / max(1, max(r["size_x"], r["size_z"])) for r in members],
                     OBSERVED, f"{cls} 高宽比 = size_y/max(size_x,size_z)")
        # 3 floor_count
        fc = vals("estimated_floor_count")
        miss = n - len(fc)
        fc_note = "HEURISTIC：density≥0.30 层为楼板候选"
        if miss:
            fc_note += f"；楼层启发式 UNKNOWN {miss}/{n}"
        emit_numeric("floor_count", fc, HEURISTIC, f"{cls} 楼层数（楼板密度启发式）", fc_note)
        # 4 floor_height
        fh = []
        for r in members:
            v = r.get("floor_heights")
            if isinstance(v, list) and v:
                fh.append(float(np.median(v)))
        emit_numeric("floor_height", fh, HEURISTIC, f"{cls} 层高中位数（相邻楼面高差）")
        # 5 roof_height_ratio（IR HEURISTIC）
        rr = irvals("roof_height_ratio")
        emit_numeric("roof_height_ratio", rr, HEURISTIC,
                     f"{cls} 屋顶高度占比 = 上部 stair+slab 最长连续带高 / size_y",
                     "HEURISTIC 算法与盲区见 STYLE_GRAMMARS.md 附录")
        rs3 = irvals("roof_material_share_top3")
        emit_numeric("roof_material_share_top3", rs3, HEURISTIC,
                     f"{cls} 顶部 1/3 区域 stair+slab 材料占比（屋顶材料信号）",
                     "HEURISTIC：任务书 9.1 建议信号；平屋顶/植被顶会拉低")
        # 6 roof_overhang（IR HEURISTIC，频率化）
        oh = irvals("roof_overhang_ratio")
        if oh:
            emit_freq("roof_overhang", sum(1 for v in oh if v > 0.05), len(oh), HEURISTIC,
                      f"{cls} 屋顶出檐：顶部1/3 脚印超出中部1/3 >5% 的样本频率")
            st = num_stats(oh)
            mk(cls, "roof_overhang_ratio", tier, f"{cls} 出檐比例分布", HEURISTIC,
               stats=st, rtype=numeric_rule_type(st, tier))
        else:
            udims.append("roof_overhang（IR 不可用）")
        # 7 vertical_rhythm（vmd 熵）
        vr = []
        for r in members:
            v = r.get("vertical_mass_distribution")
            if isinstance(v, list) and sum(v) > 0:
                p = [x for x in v if x > 0]
                vr.append(-sum(x * math.log2(x) for x in p) / math.log2(5))
        emit_numeric("vertical_rhythm", vr, OBSERVED,
                     f"{cls} 竖向节奏 = 5 等分质量分布归一化熵（1=均匀，低=质量集中）")
        # 8 symmetry
        sy = vals(None, None) if False else [max(r["symmetry_x"], r["symmetry_z"]) for r in members
                                             if isinstance(r.get("symmetry_x"), (int, float))]
        if sy:
            st = num_stats(sy)
            mk(cls, "symmetry", tier, f"{cls} 对称性 = max(symmetry_x, symmetry_z)",
               OBSERVED, stats=st, rtype=numeric_rule_type(st, tier))
            emit_freq("symmetry_high", sum(1 for v in sy if v >= 0.9), len(sy), OBSERVED,
                      f"{cls} 高对称（≥0.9）样本频率")
        # 9 window_rhythm → 密度可算，节奏规律性 UNKNOWN
        wd = [r["window_count_estimate"] / max(1, r["surface_area_estimate"]) for r in members
              if isinstance(r.get("window_count_estimate"), (int, float))]
        emit_numeric("window_density", wd, HEURISTIC,
                     f"{cls} 窗密度 = 玻璃体素数/暴露面估计（窗面积代理）",
                     "HEURISTIC：玻璃体素≈窗面积，非窗个数")
        udims.append("window_rhythm 规律性（窗洞位置节奏需立面聚合，本阶段 UNKNOWN）")
        # 10 entrance_placement
        known_ent = sum(1 for r in members if r.get("main_entrance") not in (UNKNOWN, None))
        if known_ent < max(4, n // 2):
            udims.append(f"entrance_placement（main_entrance 可判定仅 {known_ent}/{n}，"
                         "89% 全库 UNKNOWN 的纪律结果）")
        else:
            emit_freq("entrance_single", known_ent, n, HEURISTIC,
                      f"{cls} 单一外部门（main_entrance 可判定）频率")
        # 11 palette_composition
        for fam, field in (("wood", "wood_ratio"), ("stone", "stone_ratio"),
                           ("glass", "glass_ratio"), ("decorative", "decorative_ratio")):
            vv = vals(field)
            if vv:
                st = num_stats(vv)
                mk(cls, f"palette_{fam}_ratio", tier, f"{cls} {fam} 材料占比",
                   OBSERVED, stats=st, rtype=numeric_rule_type(st, tier))
        # 类内聚合 Top 方块
        agg = Counter()
        total = 0
        for r in members:
            total += r.get("non_air_blocks", 0)
            for item in r.get("top_5_block_types", []):
                agg[item["block"]] += item["count"]
        top_blocks = [{"block": b, "share_of_class": round(c / max(1, total), 4)}
                      for b, c in agg.most_common(8)]
        mk(cls, "palette_top_blocks", tier, f"{cls} 高频方块 Top（类内聚合）",
           OBSERVED, stats={"sample_n": n}, value=top_blocks, rtype="SOFT")
        # 12 material_transition（IR）
        pats = [irf.get(r["ref_id"], {}).get("material_transition_pattern") for r in members]
        pats = [p for p in pats if p]
        if pats:
            mode_pat, mode_n = Counter(pats).most_common(1)[0]
            emit_freq("material_transition", mode_n, len(pats), HEURISTIC,
                      f"{cls} 底/中/顶主导材料族模式众数：{mode_pat}",
                      notes="HEURISTIC：三段体素多数族；盲区见文档")
        else:
            udims.append("material_transition（IR 不可用）")
        # 13 wall_thickness（IR）
        wt = irvals("wall_thickness")
        emit_numeric("wall_thickness", wt, HEURISTIC,
                     f"{cls} 墙厚估计 = 中部1/3 层水平扫描线实体段中位数",
                     "HEURISTIC：含隔断墙；露天构件会拉低；实心肌体排除长段")
        # 14 cantilever_frequency（V6C2 特征，OBSERVED 自审核分类）
        feats_list = [set(labels[r["ref_id"]].get("v6c2_features", [])) for r in members]
        cant = sum(1 for f in feats_list if "second_floor_overhang" in f)
        emit_freq("cantilever_frequency", cant, n, OBSERVED,
                  f"{cls} 二层出挑（second_floor_overhang）频率",
                  notes="V6C2 特征检测要求多层楼板候选，单层样本天然为 0（盲区）")
        # 15 chimney_frequency
        ch = [irf.get(r["ref_id"], {}).get("chimney_candidate_count") for r in members]
        ch = [c for c in ch if isinstance(c, int)]
        if ch:
            emit_freq("chimney_frequency", sum(1 for c in ch if c >= 1), len(ch), HEURISTIC,
                      f"{cls} 烟囱候选频率（高出柱顶 P90 的孤立细柱）",
                      notes="HEURISTIC：尖顶/塔尖/树梢同样触发；V6C2 chimney 特征全库 0 次")
        else:
            udims.append("chimney_frequency（IR 不可用）")
        # 16 foundation_pattern
        sb = sum(1 for f in feats_list if "stone_base" in f)
        emit_freq("foundation_stone_base", sb, n, OBSERVED,
                  f"{cls} 石质基座（stone_base，底部20% 石≥55%）频率")
        bot = [p.split("→")[0] for p in pats] if pats else []
        if bot:
            bmode, bn = Counter(bot).most_common(1)[0]
            emit_freq("foundation_bottom_family", bn, len(bot), HEURISTIC,
                      f"{cls} 底部 1/3 主导材料族众数：{bmode}")

        unknown_dims[cls] = udims
    return rules, unknown_dims


# ---------------------------------------------------------------------------
# Functional grammar
# ---------------------------------------------------------------------------
def build_functional_rules(rows: list[dict], labels: dict) -> tuple[list[dict], dict]:
    rules: list[dict] = []
    unknown_dims: dict[str, list[str]] = {}

    def mk(cls, dim, tier, statement, basis, stats=None, freq=None, rtype=None, notes="", value=None):
        rule_n = stats["sample_n"] if stats and "sample_n" in stats else n
        tier = eff_tier(tier, rule_n)  # 规则级别按自身 sample_n 收紧
        r = {"rule_id": f"FUNC.{cls}.{dim}", "class": cls, "dimension": dim,
             "support": tier, "rule_type": rtype, "statement": statement,
             "basis": basis, "confidence": conf_of(basis, tier)}
        if stats:
            r.update(stats)
        if freq is not None:
            r["frequency"] = round(freq, 4)
        if value is not None:
            r["value"] = value
        if notes:
            r["notes"] = notes
        rules.append(r)

    for cls in FUNCTION_GRAMMAR_CLASSES:
        members = [r for r in rows if labels[r["ref_id"]]["function_label"] == cls]
        n = len(members)
        if n == 0:
            continue
        tier = support_tier(n)
        udims: list[str] = []
        if tier == "OBSERVATION ONLY":
            unknown_dims[cls] = ["全部维度：样本 <4，仅列观测不形成规则"]
            continue

        # zone 语义退化声明：房间语义不可自动识别，一切 zone = 可走连通区域（walkability 分量）
        zone_note = "zone = walkable connected region；房间语义（bedroom/kitchen 等）不可识别，不声称"

        # 1 required_zones：围合室内 + 外部门
        ia = [r["interior_air_ratio"] for r in members if isinstance(r.get("interior_air_ratio"), (int, float))]
        if ia:
            hits = sum(1 for v in ia if v >= 0.01)
            freq = hits / len(ia)
            mk(cls, "required_zones.enclosed_interior", tier,
               f"{cls} 存在围合室内（interior_air_ratio≥0.01）频率 {freq:.2f}",
               HEURISTIC, stats={"sample_n": len(ia)}, freq=freq,
               rtype=freq_rule_type(freq, tier, hard_eligible=(cls in ("Residential", "Inn")),
                                    rule_n=len(ia)),
               notes=zone_note)
        ed = [r for r in members if isinstance(r.get("exterior_door_candidates"), int)]
        hits = sum(1 for r in ed if r["exterior_door_candidates"] >= 1)
        freq = hits / n
        mk(cls, "required_zones.exterior_door", tier,
           f"{cls} 至少 1 扇外部门频率 {freq:.2f}（door_count≠entrance_count，此处为外部门候选）",
           HEURISTIC, stats={"sample_n": n}, freq=freq,
           rtype=freq_rule_type(freq, tier, hard_eligible=(cls in ("Residential", "Inn"))),
           notes="门可交互开启视为可过；铁质关门除外")

        # 2 optional_zones：上层 / 院落
        floors = [r["estimated_floor_count"] for r in members
                  if isinstance(r.get("estimated_floor_count"), int)]
        if floors:
            f2 = sum(1 for v in floors if v >= 2) / len(floors)
            mk(cls, "optional_zones.upper_floor", tier,
               f"{cls} ≥2 层频率 {f2:.2f}（上层作为可选 zone）",
               HEURISTIC, stats={"sample_n": len(floors)}, freq=f2,
               rtype=freq_rule_type(f2, tier, rule_n=len(floors)))
        else:
            udims.append("optional_zones.upper_floor（楼层全 UNKNOWN）")
        feats_list = [set(labels[r["ref_id"]].get("v6c2_features", [])) for r in members]
        cy = sum(1 for f in feats_list if "courtyard" in f)
        mk(cls, "optional_zones.courtyard", tier,
           f"{cls} 院落（courtyard 特征）频率 {cy / n:.2f}",
           OBSERVED, stats={"sample_n": n}, freq=cy / n,
           rtype=freq_rule_type(cy / n, tier))

        # 3 zone_adjacency：分量结构
        lcr = [r["largest_component_ratio"] for r in members
               if isinstance(r.get("largest_component_ratio"), (int, float))]
        if lcr:
            st = num_stats(lcr)
            mk(cls, "zone_adjacency.largest_component", tier,
               f"{cls} 最大可走分量占比中位 {st['median']:.2f}（高=各区连通好）",
               HEURISTIC, stats=st, rtype=numeric_rule_type(st, tier),
               notes="分量含屋顶/墙顶露天站位，解读需谨慎")
        iso = [r["isolated_space_count"] for r in members
               if isinstance(r.get("isolated_space_count"), (int, float))]
        if iso:
            st = num_stats(iso)
            mk(cls, "zone_adjacency.isolated_spaces", tier,
               f"{cls} 孤立空间数（≥8 体素非主分量）中位 {st['median']}",
               HEURISTIC, stats=st, rtype=numeric_rule_type(st, tier))

        # 4 public_private_separation：只能给弱代理
        if floors:
            mk(cls, "public_private_separation", tier,
               f"{cls} 公私分区不可从 IR 直接判定；弱代理：≥2 层频率 "
               f"{sum(1 for v in floors if v >= 2) / len(floors):.2f}（上层私密假设为 INFERRED）",
               INFERRED, stats={"sample_n": len(floors)},
               freq=sum(1 for v in floors if v >= 2) / len(floors),
               rtype="OPTIONAL",
               notes="INFERRED：楼上=私密是建筑常识推断，非本库测量")
        else:
            udims.append("public_private_separation（无楼层信号 → UNKNOWN）")

        # 5 vertical_access
        va = [r for r in members if isinstance(r.get("vertical_access_candidates"), int)]
        hits = sum(1 for r in va if r["vertical_access_candidates"] >= 1)
        freq = hits / n
        mk(cls, "vertical_access.presence", tier,
           f"{cls} 存在垂直交通（楼梯簇/梯柱≥1）频率 {freq:.2f}",
           HEURISTIC, stats={"sample_n": n}, freq=freq,
           rtype=freq_rule_type(freq, tier))
        multi = [r for r in members if isinstance(r.get("estimated_floor_count"), int)
                 and r["estimated_floor_count"] >= 2]
        if multi:
            cond = sum(1 for r in multi if r.get("vertical_access_candidates", 0) >= 1) / len(multi)
            mk(cls, "vertical_access.multifloor_requires", tier,
               f"{cls} 多层 ⇒ 有垂直交通：条件频率 {cond:.2f}（n_multi={len(multi)}）",
               HEURISTIC, stats={"sample_n": len(multi)}, freq=cond,
               rtype=freq_rule_type(cond, tier, hard_eligible=True, rule_n=len(multi)),
               notes="功能必需候选：多层无楼梯/梯子则上层不可达")
        st_c = [r.get("stair_cluster_count", 0) for r in members]
        ld_c = [r.get("ladder_column_count", 0) for r in members]
        mk(cls, "vertical_access.means", tier,
           f"{cls} 垂直交通方式：楼梯簇中位 {float(np.median(st_c)):.0f}、"
           f"梯柱中位 {float(np.median(ld_c)):.0f}",
           OBSERVED, stats={"sample_n": n},
           value={"stair_cluster_median": float(np.median(st_c)),
                  "ladder_column_median": float(np.median(ld_c))},
           rtype="SOFT")

        # 6 entrance_relation
        edc = [r["exterior_door_candidates"] for r in members
               if isinstance(r.get("exterior_door_candidates"), int)]
        if edc:
            st = num_stats(edc)
            mk(cls, "entrance_relation.exterior_door_count", tier,
               f"{cls} 外部门候选数中位 {st['median']:.0f}", HEURISTIC,
               stats=st, rtype=numeric_rule_type(st, tier))
        known_ent = sum(1 for r in members if r.get("main_entrance") not in (UNKNOWN, None))
        if known_ent < max(4, n // 2):
            udims.append(f"entrance_relation.方位（main_entrance 可判定仅 {known_ent}/{n} → UNKNOWN）")
        else:
            mk(cls, "entrance_relation.single_entrance", tier,
               f"{cls} 单一主入口可判定频率 {known_ent / n:.2f}", HEURISTIC,
               stats={"sample_n": n}, freq=known_ent / n,
               rtype=freq_rule_type(known_ent / n, tier))

        # 7 circulation_constraints
        de = []
        for r in members:
            wv = r.get("walkable_voxels", 0)
            if isinstance(wv, int) and wv > 0 and isinstance(r.get("dead_end_count"), int):
                de.append(r["dead_end_count"] / wv)
        if de:
            st = num_stats(de)
            mk(cls, "circulation_constraints.dead_end_ratio", tier,
               f"{cls} 死端比例（度1站位/总站位）中位 {st['median']:.2f}",
               HEURISTIC, stats=st, rtype=numeric_rule_type(st, tier))
        ufa = [r["usable_floor_area"] for r in members
               if isinstance(r.get("usable_floor_area"), (int, float))]
        if ufa:
            st = num_stats(ufa)
            mk(cls, "circulation_constraints.usable_floor_area", tier,
               f"{cls} 可用楼面面积中位 {st['median']:.0f} 格",
               HEURISTIC, stats=st, rtype=numeric_rule_type(st, tier))
        else:
            udims.append("circulation_constraints.usable_floor_area（楼层 UNKNOWN）")

        unknown_dims[cls] = udims
    return rules, unknown_dims


# ---------------------------------------------------------------------------
# 数据缺口矩阵（任务书第 24 节）
# ---------------------------------------------------------------------------
def build_gap_matrix(rows: list[dict], labels: dict) -> dict:
    funcs = FUNCTION_GRAMMAR_CLASSES + FUNCTION_ZERO_SAMPLE
    # 类总量
    style_total = Counter(labels[r["ref_id"]]["style_label"] for r in rows)
    func_total = Counter(labels[r["ref_id"]]["function_label"] for r in rows)
    func_total.setdefault("Bridge", 0)

    cells = []
    for style in MATRIX_STYLES:
        for func in funcs:
            for size in MATRIX_SIZES:
                sub = [r for r in rows
                       if labels[r["ref_id"]]["style_label"] == style
                       and labels[r["ref_id"]]["function_label"] == func
                       and labels[r["ref_id"]].get("scale") == size]
                n = len(sub)
                if n >= 8:
                    cq = "SUPPORTED"
                elif n >= 4:
                    cq = "PROVISIONAL"
                elif n >= 1:
                    cq = "OBSERVATION"
                else:
                    cq = "GAP"
                # missing_features：对该 cell 子集检查关键维度可得性
                miss = []
                if n == 0:
                    miss = ["all（无样本）"]
                else:
                    if all(r.get("estimated_floor_count") in (UNKNOWN, None) for r in sub):
                        miss.append("floor_count 全 UNKNOWN")
                    if all(r.get("main_entrance") in (UNKNOWN, None) for r in sub):
                        miss.append("entrance_placement 全 UNKNOWN")
                    if all(r.get("window_count_estimate", 0) == 0 for r in sub):
                        miss.append("window 信号为 0")
                # priority
                ft, st_ = func_total.get(func, 0), style_total.get(style, 0)
                if n >= 4:
                    pr = "P3"
                    reason = "样本≥4，可候补至 SUPPORTED" if n < 8 else "覆盖充足"
                elif n >= 1:
                    pr = "P2"
                    reason = f"仅 {n} 样本，补至 ≥4"
                else:
                    if ft < 8 and func in CENTRAL_FUNCTIONS and size in ("small", "medium") \
                            and style in ("Medieval", "Rustic", "Japanese", "Chinese"):
                        pr = "P0"
                        reason = f"村落核心功能 {func} 全库仅 {ft} 样本且该 cell 空缺"
                    elif ft >= 8 and st_ >= 8 and size in ("small", "medium", "large"):
                        pr = "P1"
                        reason = f"{style}×{func} 两类均 SUPPORTED 但组合空缺"
                    else:
                        pr = "P2"
                        reason = "组合空缺"
                cells.append({"style": style, "function": func, "size_class": size,
                              "sample_n": n, "coverage_quality": cq,
                              "missing_features": miss, "priority": pr,
                              "priority_reason": reason})
    rank = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    top_gaps = sorted((c for c in cells if c["sample_n"] < 4),
                      key=lambda c: (rank[c["priority"]], c["sample_n"]))[:20]
    return {
        "size_class_rule": "复用 V6C2 catalog scale 字段（tiny≤16边&≤1000块&≤4096包络 / small≤32 / "
                           "medium≤64 / large≤128 / monumental 超 large；阈值见 references/catalog/"
                           "classification-rules.md 规模表）",
        "styles_in_matrix": MATRIX_STYLES,
        "functions_in_matrix": funcs,
        "size_classes": MATRIX_SIZES,
        "class_totals": {"style": dict(style_total), "function": dict(func_total)},
        "cells": cells,
        "top_gaps": top_gaps,
    }


# ---------------------------------------------------------------------------
# 文档生成
# ---------------------------------------------------------------------------
TIER_LABEL = {"SUPPORTED": "SUPPORTED", "PROVISIONAL": "PROVISIONAL",
              "OBSERVATION ONLY": "OBSERVATION ONLY"}


def render_rules_md(title: str, intro: str, rules: list[dict],
                    class_notes: dict[str, str]) -> str:
    out = [f"# {title}\n\n{intro}\n"]
    by_class: dict[str, list[dict]] = {}
    for r in rules:
        by_class.setdefault(r["class"], []).append(r)
    for cls, rs in by_class.items():
        tier = rs[0]["support"]
        n = max(r.get("sample_n", 0) for r in rs)
        out.append(f"\n## {cls}（sample_n={n}，{tier}）\n")
        if cls in class_notes:
            out.append(f"\n> {class_notes[cls]}\n")
        out.append("\n| 维度 | 规则 | 类型 | basis | 统计 | 置信 |\n")
        out.append("|---|---|---|---|---|---|\n")
        for r in rs:
            stat = ""
            if "median" in r:
                stat = f"n={r['sample_n']} median={r['median']} IQR[{r['p25']},{r['p75']}]"
            if "frequency" in r:
                stat = (stat + " " if stat else "") + f"freq={r['frequency']}"
            if "value" in r and isinstance(r["value"], list):
                tb = ", ".join(f"{x['block'].split(':')[-1]} {x['share_of_class']:.0%}"
                               for x in r["value"][:5])
                stat = (stat + " " if stat else "") + tb
            elif "value" in r and isinstance(r["value"], dict):
                tb = ", ".join(f"{k}={v}" for k, v in r["value"].items())
                stat = (stat + " " if stat else "") + tb
            stmt = r["statement"].replace("|", "\\|")
            out.append(f"| {r['dimension']} | {stmt} | {r['rule_type']} | {r['basis']} "
                       f"| {stat} | {r['confidence']} |\n")
    return "".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="P3 Architecture Grammar 构建")
    ap.add_argument("--metadata", required=True)
    ap.add_argument("--labels", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--references-root", default=None,
                    help="references\\derived 根目录（只读）；省略则 IR 衍生维度 UNKNOWN")
    ap.add_argument("--palette-dictionary", default=None,
                    help="palette_dictionary.json；给 references-root 时必填")
    args = ap.parse_args()

    meta_rows = {}
    with open(args.metadata, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if r.get("status") == "OK":
                meta_rows[r["ref_id"]] = r
    labels = {}
    with open(args.labels, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            labels[r["ref_id"]] = r
    rows = [meta_rows[k] for k in meta_rows if k in labels]

    # ---- IR 衍生特征 ----
    irf: dict[str, dict] = {}
    ir_available = bool(args.references_root)
    if ir_available:
        if not args.palette_dictionary:
            print("ERROR: --references-root 需要 --palette-dictionary", file=sys.stderr)
            return 2
        families = load_palette_dictionary(Path(args.palette_dictionary))
        cache_path = Path(args.output) / "ir_features.jsonl"
        for ref in sorted(rows, key=lambda r: r["ref_id"]):
            rid = ref["ref_id"]
            try:
                irf[rid] = compute_ir_features(Path(args.references_root) / rid, families)
            except Exception as ex:  # 单张失败不拖垮全批，如实记录
                irf[rid] = {"ref_id": rid, "error": str(ex)}
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_path, "w", encoding="utf-8") as f:
            for rid in sorted(irf):
                f.write(json.dumps(irf[rid], ensure_ascii=False) + "\n")

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    # ---- Style grammar ----
    style_rules, style_udims = build_style_rules(rows, meta_rows, irf, labels)
    (out_dir / "style_rules.json").write_text(json.dumps(
        {"version": "P3-1.0",
         "sample_discipline": {"SUPPORTED": "n>=8", "PROVISIONAL": "4-7", "OBSERVATION ONLY": "<4"},
         "rule_types": {"HARD": "功能必需（style grammar 不出 HARD）",
                        "STRONG": "高频稳定", "SOFT": "常见可打破", "OPTIONAL": "装饰倾向"},
         "ir_features_available": ir_available,
         "rules": style_rules}, ensure_ascii=False, indent=2), encoding="utf-8")

    style_intro = (
        "> 生成：`scripts/build_grammar.py`。样本纪律：n≥8 SUPPORTED（可 STRONG）、4–7 PROVISIONAL"
        "（最高 SOFT）、<4 OBSERVATION ONLY（不出规则）。Style 维度无 HARD（HARD=功能必需，"
        "见任务书第 20 节）。Other 为异质集合不出规则；Unknown（56 张）不是类别。\n"
        "> basis：OBSERVED=元数据/审核分类直接统计；HEURISTIC=明确算法近似（算法与盲区见文末附录）。\n")
    style_notes = {
        "Other": "european/desert/classical 异质集合，仅观测不泛化。",
    }
    style_md = render_rules_md("STYLE_GRAMMARS — 风格语法", style_intro, style_rules, style_notes)
    style_md += (
        "\n\n## 附录：IR 衍生 HEURISTIC 算法与盲区\n\n"
        "1. **roof_height_ratio**：在 y≥0.4·size_y 范围找\"本层 (stair+slab)/实体 ≥0.25 且本层实体≥3\""
        "的最长连续层带，带高 / size_y；**不从最顶层起算**（尖顶/装饰帽常为非楼梯方块，从顶起算"
        "会立即断裂——调试实测：世界之塔顶部 8 层 share=0）。盲区：平屋顶带长≈0–1；上部立面/"
        "基座装饰楼梯成带会高估；植被顶不成带（→0）。配套信号 **roof_material_share_top3** ="
        "顶部 1/3 区域 (stair+slab)/实体（任务书 9.1 建议的屋顶材料信号）。二者均为材料信号，"
        "不是屋面几何重建。\n"
        "2. **roof_overhang_ratio**：顶部 1/3 脚印超出中部 1/3 的比例。盲区：三层皆错位的塔/雕塑"
        "会得到非零值，不等于真正屋檐。\n"
        "3. **material_transition**：底/中/顶三段体素多数材料族（palette_dictionary 族表）。"
        "盲区：段内混合时只取多数族；装饰族（树叶）在顶部常胜出，可能掩盖屋面瓦材料。\n"
        "4. **wall_thickness**：中部 1/3 层水平扫描线，两侧为空气的实体段（≤8 格）中位数。"
        "盲区：含室内隔断墙；露天构件（栅栏/树干）短段拉低中位数；实心肌体长段被排除。\n"
        "5. **chimney_candidate**：柱顶高出全图柱顶 P90 ≥3 格且四邻柱顶低 ≥2 格的孤立细柱。"
        "盲区：尖顶/塔尖/树梢/旗杆同样触发——仅作频率倾向。V6C2 chimney 特征检测全库 0 次，"
        "故此处为唯一烟囱信号，可靠性低。\n"
        "6. **window_rhythm 规律性 / entrance_placement 方位**：元数据不足，按纪律 UNKNOWN。\n")
    (out_dir / "STYLE_GRAMMARS.md").write_text(style_md, encoding="utf-8")

    # ---- Functional grammar ----
    func_rules, func_udims = build_functional_rules(rows, labels)
    (out_dir / "functional_rules.json").write_text(json.dumps(
        {"version": "P3-1.0",
         "sample_discipline": {"SUPPORTED": "n>=8", "PROVISIONAL": "4-7", "OBSERVATION ONLY": "<4"},
         "zone_semantics": "zone = walkable connected region（walkability 分量）；房间语义不可自动识别",
         "rules": func_rules}, ensure_ascii=False, indent=2), encoding="utf-8")
    func_intro = (
        "> 生成：`scripts/build_grammar.py`。样本纪律同上。**房间语义无法自动识别**："
        "所有 zone 均为 walkable connected region（可走连通分量），不声称识别 bedroom/kitchen；"
        "public/private 等语义推断标 INFERRED。Decoration/Vehicle 多为非建筑样本，"
        "其「规则」多为负向特征（无门/无室内），这本身就是功能画像。\n")
    func_md = render_rules_md("FUNCTIONAL_GRAMMARS — 功能语法", func_intro, func_rules, {})
    (out_dir / "FUNCTIONAL_GRAMMARS.md").write_text(func_md, encoding="utf-8")

    # ---- 缺口矩阵 ----
    gap = build_gap_matrix(rows, labels)
    (out_dir / "data_gap_matrix.json").write_text(
        json.dumps(gap, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- 置信度报告 ----
    rep = ["# grammar_confidence_report — P3 Grammar 置信度与覆盖报告\n"]
    rep.append("\n## 1. 各类别样本量与规则分级计数\n\n")
    rep.append("### Style\n\n| 类别 | sample_n | 级别 | 规则数 | HARD/STRONG/SOFT/OPTIONAL |\n|---|---:|---|---:|---|\n")
    for cls in STYLE_GRAMMAR_CLASSES + ["Other"]:
        rs = [r for r in style_rules if r["class"] == cls]
        n = sum(1 for k in labels.values() if k["style_label"] == cls)
        tier = support_tier(n) if cls != "Other" else "OBSERVATION ONLY"
        tc = Counter(r["rule_type"] for r in rs)
        rep.append(f"| {cls} | {n} | {tier} | {len(rs)} | "
                   f"{tc.get('HARD', 0)}/{tc.get('STRONG', 0)}/{tc.get('SOFT', 0)}/{tc.get('OPTIONAL', 0)} |\n")
    n_unknown_style = sum(1 for k in labels.values() if k["style_label"] == "Unknown")
    rep.append(f"| Unknown | {n_unknown_style} | 非类别 | 0 | — |\n")
    rep.append("\n### Function\n\n| 类别 | sample_n | 级别 | 规则数 | HARD/STRONG/SOFT/OPTIONAL |\n|---|---:|---|---:|---|\n")
    for cls in FUNCTION_GRAMMAR_CLASSES:
        rs = [r for r in func_rules if r["class"] == cls]
        n = sum(1 for k in labels.values() if k["function_label"] == cls)
        tc = Counter(r["rule_type"] for r in rs)
        rep.append(f"| {cls} | {n} | {support_tier(n)} | {len(rs)} | "
                   f"{tc.get('HARD', 0)}/{tc.get('STRONG', 0)}/{tc.get('SOFT', 0)}/{tc.get('OPTIONAL', 0)} |\n")
    rep.append("\n## 2. UNKNOWN 维度清单（按类别，含原因）\n\n")
    for src, uds in (("Style", style_udims), ("Function", func_udims)):
        for cls, dims in uds.items():
            if dims:
                rep.append(f"- **{src}/{cls}**：" + "；".join(dims) + "\n")
    rep.append("\n## 3. 数据缺口矩阵解读（任务书第 24 节）\n\n")
    rep.append(f"矩阵：{len(gap['styles_in_matrix'])} style × {len(gap['functions_in_matrix'])} function "
               f"× {len(gap['size_classes'])} size = {len(gap['cells'])} cells；"
               f"size_class 复用 V6C2 scale（阈值见分类规则规模表）。\n\n")
    prank = Counter(c["priority"] for c in gap["cells"])
    rep.append(f"优先级分布：P0={prank.get('P0', 0)} / P1={prank.get('P1', 0)} / "
               f"P2={prank.get('P2', 0)} / P3={prank.get('P3', 0)}\n\n")
    rep.append("### Top 缺口（前 20）\n\n| style | function | size | n | coverage | priority | 原因 |\n|---|---|---|---:|---|---|---|\n")
    for c in gap["top_gaps"]:
        rep.append(f"| {c['style']} | {c['function']} | {c['size_class']} | {c['sample_n']} "
                   f"| {c['coverage_quality']} | {c['priority']} | {c['priority_reason']} |\n")
    rep.append("\n### 补充：0 样本风格大类（不进矩阵）\n\n"
               "Modern / Industrial / Gothic / Victorian / Nordic 全库 0 样本（见 "
               "03_TAXONOMY/ARCHITECTURE_TAXONOMY.md），任何 function×size 组合都无法形成 grammar，"
               "整体列为最高优先采集方向之一（与 P0 cell 同级，按需求排序）。\n")
    (out_dir / "grammar_confidence_report.md").write_text("".join(rep), encoding="utf-8")

    print(json.dumps({
        "style_rules": len(style_rules),
        "functional_rules": len(func_rules),
        "gap_cells": len(gap["cells"]),
        "gap_priority": dict(prank),
        "ir_features": len(irf),
        "ir_available": ir_available,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
