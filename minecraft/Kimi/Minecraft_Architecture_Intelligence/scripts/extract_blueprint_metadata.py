# -*- coding: utf-8 -*-
"""extract_blueprint_metadata — 批量提取 123 张参考蓝图的 Metadata DB（项目代号 H · P1）。

用法：
    python extract_blueprint_metadata.py \
        --references-root <references路径> \
        --catalog <catalog.json> \
        --output <输出目录>

输出：
    blueprint_metadata.jsonl   每行一张蓝图（含 _basis 字段级标记）
    blueprint_metadata.csv     扁平主要字段
    extraction_summary.json    成功/失败/UNKNOWN 统计（供 feature_extraction_report）

纪律：
- 逐文件 try/except，失败记录 PARSE_FAILURE 结构，不中断批次；
- 判不出的字段写字符串 "UNKNOWN"（不用 None/空值冒充）；
- 每个字段在 _basis dict 中标注 OBSERVED / HEURISTIC / INFERRED / UNKNOWN；
- 只读 references，不碰 .litematic 原件。
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy import ndimage

sys.path.insert(0, str(Path(__file__).resolve().parent))
from blueprint_io import load_blueprint, to_voxels  # noqa: E402
from walkability import analyze as walk_analyze, classify_block  # noqa: E402

OBSERVED, HEURISTIC, INFERRED, UNKNOWN = "OBSERVED", "HEURISTIC", "INFERRED", "UNKNOWN"

# 楼层检测参数（HEURISTIC 阈值，见 METADATA_SCHEMA.md）
FLOOR_DENSITY_THRESHOLD = 0.30   # 某 y 层实体占比 ≥ 此值视为“楼板候选层”
FLOOR_HIGH_CONF_DENSITY = 0.40
MIN_FLOOR_GAP = 2                # 相邻楼层层最小间隔（格）


# ---------------------------------------------------------------------------
# 材料族
# ---------------------------------------------------------------------------
def load_palette_dictionary(path: Path) -> list[tuple[str, list[str]]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [(fam, spec["patterns"]) for fam, spec in data["families"].items()]


def material_family(block_id: str, families: list[tuple[str, list[str]]]) -> str:
    bid = block_id.lower()
    for fam, patterns in families:
        for p in patterns:
            if p in bid:
                return fam
    return UNKNOWN


# ---------------------------------------------------------------------------
# 主提取
# ---------------------------------------------------------------------------
def extract_one(ref_dir: Path, catalog_item: dict | None, families) -> dict:
    ir = load_blueprint(ref_dir)
    voxels, air_index = to_voxels(ir)
    X, Y, Z = voxels.shape
    bounding_volume = int(X * Y * Z)

    solid = voxels != air_index
    # palette 中可能另有 cave_air 等索引，统一按 block_id 判空气
    air_ids = {i for i, bid in enumerate(ir.block_ids) if bid.endswith(":air") or "air" == bid.split(":")[-1]}
    if len(air_ids) > 1:
        solid &= ~np.isin(voxels, list(air_ids - {air_index}))

    non_air = int(solid.sum())
    air_blocks = bounding_volume - non_air

    basis: dict[str, str] = {}
    rec: dict = {"ref_id": ir.ref_id or ref_dir.name, "status": "OK"}
    basis["ref_id"] = OBSERVED
    basis["status"] = OBSERVED

    # ---- 6.1 基础字段 -----------------------------------------------------
    cat = catalog_item or {}
    rec["source_file"] = cat.get("original_filename", UNKNOWN)
    rec["source_name"] = cat.get("name") or cat.get("schematic_name") or UNKNOWN
    rec["data_version"] = cat.get("minecraft_data_version", UNKNOWN)
    rec["normalized_status"] = cat.get("compatibility", UNKNOWN)
    rec["region_count"] = cat.get("region_count", UNKNOWN)
    for k in ("source_file", "source_name", "data_version", "normalized_status", "region_count"):
        basis[k] = OBSERVED if rec[k] != UNKNOWN else UNKNOWN

    rec["size_x"], rec["size_y"], rec["size_z"] = X, Y, Z
    rec["bounding_volume"] = bounding_volume
    rec["non_air_blocks"] = non_air
    rec["air_blocks"] = air_blocks
    rec["occupancy_ratio"] = round(non_air / bounding_volume, 6) if bounding_volume else 0.0

    used_idx, used_counts = np.unique(voxels[solid], return_counts=True)
    rec["unique_block_states"] = int(len(used_idx))
    rec["unique_block_types"] = int(len({ir.block_ids[i] for i in used_idx}))
    # Shannon entropy（按非空气体素的 block state 频次，自然对数/ln2 → bit）
    probs = used_counts / used_counts.sum()
    rec["palette_entropy"] = float(-(probs * np.log2(probs)).sum())
    for k in ("size_x", "size_y", "size_z", "bounding_volume", "non_air_blocks",
              "air_blocks", "occupancy_ratio", "unique_block_states",
              "unique_block_types", "palette_entropy"):
        basis[k] = OBSERVED

    # ---- 6.2 材料字段 -----------------------------------------------------
    type_counts: Counter = Counter()
    state_counts: Counter = Counter()
    fam_counts: Counter = Counter()
    unknown_material_types: set[str] = set()
    for i, c in zip(used_idx.tolist(), used_counts.tolist()):
        bid = ir.block_ids[i]
        type_counts[bid] += c
        state_counts[ir.palette[i]] += c
        fam = material_family(bid, families)
        fam_counts[fam] += c
        if fam == UNKNOWN:
            unknown_material_types.add(bid)

    rec["dominant_palette"] = [s for s, _ in state_counts.most_common(10)]
    rec["top_5_block_types"] = [{"block": b, "count": c} for b, c in type_counts.most_common(5)]
    rec["top_10_block_states"] = [{"state": s, "count": c} for s, c in state_counts.most_common(10)]
    for fam in ("wood", "stone", "glass", "metal", "decorative", "functional"):
        key = f"{fam}_ratio" if fam != "functional" else "functional_block_ratio"
        rec[key] = round(fam_counts.get(fam, 0) / non_air, 6) if non_air else 0.0
        basis[key] = OBSERVED
    rec["unknown_material_ratio"] = round(fam_counts.get(UNKNOWN, 0) / non_air, 6) if non_air else 0.0
    rec["unknown_material_block_types"] = sorted(unknown_material_types)
    for k in ("dominant_palette", "top_5_block_types", "top_10_block_states",
              "unknown_material_ratio", "unknown_material_block_types"):
        basis[k] = OBSERVED

    # ---- 6.3 几何字段 -----------------------------------------------------
    # footprint：含 ≥1 非空气体素的 (x,z) 柱数
    rec["footprint_area"] = int(solid.any(axis=1).sum())
    rec["solid_volume"] = non_air
    # 暴露面计数：6×N − 2×相邻实体对
    adj = 0
    for axis in range(3):
        sl_a = [slice(None)] * 3
        sl_b = [slice(None)] * 3
        sl_a[axis] = slice(0, -1)
        sl_b[axis] = slice(1, None)
        adj += int((solid[tuple(sl_a)] & solid[tuple(sl_b)]).sum())
    rec["surface_area_estimate"] = int(6 * non_air - 2 * adj)
    rec["width_height_ratio"] = round(X / Y, 4) if Y else UNKNOWN
    rec["depth_height_ratio"] = round(Z / Y, 4) if Y else UNKNOWN
    for k in ("footprint_area", "solid_volume", "surface_area_estimate"):
        basis[k] = OBSERVED
    for k in ("width_height_ratio", "depth_height_ratio"):
        basis[k] = OBSERVED if rec[k] != UNKNOWN else UNKNOWN

    if non_air > 0:
        coords = np.argwhere(solid)
        rec["center_of_mass"] = [round(float(v), 3) for v in coords.mean(axis=0)]
        # 垂直质量分布：5 等分 y 带的实体占比
        bands = np.minimum((coords[:, 1] * 5) // max(Y, 1), 4)
        band_counts = np.bincount(bands, minlength=5)
        rec["vertical_mass_distribution"] = [round(float(c / non_air), 4) for c in band_counts]
    else:
        rec["center_of_mass"] = UNKNOWN
        rec["vertical_mass_distribution"] = UNKNOWN
    basis["center_of_mass"] = OBSERVED if rec["center_of_mass"] != UNKNOWN else UNKNOWN
    basis["vertical_mass_distribution"] = OBSERVED if rec["vertical_mass_distribution"] != UNKNOWN else UNKNOWN

    # 镜像对称匹配率：只看“至少一侧为实体”的体素对
    if non_air > 0:
        fx = solid[::-1, :, :]
        cand = solid | fx
        rec["symmetry_x"] = round(float((solid & fx).sum() / cand.sum()), 4) if cand.any() else 1.0
        fz = solid[:, :, ::-1]
        candz = solid | fz
        rec["symmetry_z"] = round(float((solid & fz).sum() / candz.sum()), 4) if candz.any() else 1.0
    else:
        rec["symmetry_x"] = rec["symmetry_z"] = UNKNOWN
    for k in ("symmetry_x", "symmetry_z"):
        basis[k] = OBSERVED if rec[k] != UNKNOWN else UNKNOWN

    # 外部空气洪泛：从包络边界出发标记 exterior air；其余 air 为 interior
    air_mask = ~solid
    air_labels, n_air = ndimage.label(air_mask)
    exterior_labels = set(np.unique(np.concatenate([
        air_labels[0, :, :].ravel(), air_labels[-1, :, :].ravel(),
        air_labels[:, 0, :].ravel(), air_labels[:, -1, :].ravel(),
        air_labels[:, :, 0].ravel(), air_labels[:, :, -1].ravel(),
    ]))) - {0}
    exterior_air = np.isin(air_labels, list(exterior_labels)) if exterior_labels else np.zeros_like(air_mask)
    interior_air = air_mask & ~exterior_air
    interior_air_count = int(interior_air.sum())
    rec["interior_air_ratio"] = round(interior_air_count / bounding_volume, 6) if bounding_volume else 0.0
    basis["interior_air_ratio"] = HEURISTIC  # “内部”由洪泛定义，语义为近似

    # 外壳实体：与外部空气相邻的实体体素
    shell = np.zeros_like(solid)
    for axis in range(3):
        sl_a = [slice(None)] * 3
        sl_b = [slice(None)] * 3
        sl_a[axis] = slice(0, -1)
        sl_b[axis] = slice(1, None)
        touch = exterior_air[tuple(sl_a)] & solid[tuple(sl_b)]
        shell[tuple(sl_b)] |= touch
        touch2 = solid[tuple(sl_a)] & exterior_air[tuple(sl_b)]
        shell[tuple(sl_a)] |= touch2
    rec["exterior_shell_ratio"] = round(float(shell.sum()) / non_air, 6) if non_air else 0.0
    basis["exterior_shell_ratio"] = HEURISTIC

    # ---- walkability（6.6 先行计算，6.4 的 usable_floor_area 复用 E） ------
    walk = walk_analyze(voxels, ir)
    for k in ("walkable_voxels", "walkable_components", "largest_component_ratio",
              "isolated_space_count", "vertical_connections", "dead_end_count"):
        rec[k] = walk[k]
        basis[k] = HEURISTIC  # 依赖可通行近似模型
    rec["walkability_unknown_block_types"] = walk["unknown_block_types"]
    basis["walkability_unknown_block_types"] = OBSERVED

    # ---- 6.4 楼层特征（HEURISTIC） ----------------------------------------
    layer_density = solid.sum(axis=(0, 2)) / (X * Z) if X * Z else np.zeros(Y)
    cand_layers = np.flatnonzero(layer_density >= FLOOR_DENSITY_THRESHOLD)
    # 连续候选层分组，取组顶+1 为楼面（行走面）高程
    floor_groups: list[list[int]] = []
    for yv in cand_layers.tolist():
        if floor_groups and yv - floor_groups[-1][-1] <= 1:
            floor_groups[-1].append(yv)
        else:
            floor_groups.append([yv])
    raw_elevations = [g[-1] + 1 for g in floor_groups]
    # 合并间隔过小的层
    floor_elevations: list[int] = []
    for e in raw_elevations:
        if floor_elevations and e - floor_elevations[-1] < MIN_FLOOR_GAP:
            continue
        floor_elevations.append(e)

    if not floor_elevations:
        rec["estimated_floor_count"] = UNKNOWN
        rec["floor_elevations"] = UNKNOWN
        rec["floor_heights"] = UNKNOWN
        rec["usable_floor_area"] = UNKNOWN
        rec["floor_detection_confidence"] = "low"
        for k in ("estimated_floor_count", "floor_elevations", "floor_heights", "usable_floor_area"):
            basis[k] = UNKNOWN
        basis["floor_detection_confidence"] = HEURISTIC
    else:
        peak_density = max(float(layer_density[max(e - 1, 0)]) for e in floor_elevations)
        confidence = "high" if (len(floor_elevations) >= 2 and peak_density >= FLOOR_HIGH_CONF_DENSITY) else "medium"
        rec["estimated_floor_count"] = len(floor_elevations)
        rec["floor_elevations"] = floor_elevations
        rec["floor_heights"] = [b - a for a, b in zip(floor_elevations, floor_elevations[1:])]
        # usable_floor_area：各楼面高程 ±0.5 内的站位体素数之和
        # 重新取站位高程（walk_analyze 未带 labels 时无 E，这里用 return_labels 重算代价高；
        # 采用近似：以各层顶面实体柱数 = 楼面 y=e-1 处实体体素数）
        usable = 0
        for e in floor_elevations:
            if 0 <= e - 1 < Y:
                usable += int(solid[:, e - 1, :].sum())
        rec["usable_floor_area"] = usable
        rec["floor_detection_confidence"] = confidence
        for k in ("estimated_floor_count", "floor_elevations", "floor_heights",
                  "usable_floor_area", "floor_detection_confidence"):
            basis[k] = HEURISTIC

    # ---- 6.5 门 / 窗 / 垂直交通 -------------------------------------------
    pid_of = voxels  # palette 索引体素
    door_lower_positions: list[tuple[int, int, int]] = []
    stair_mask = np.zeros_like(solid)
    ladder_mask = np.zeros_like(solid)
    glass_count = 0
    door_idx_set = set()
    ladder_idx_set = set()
    stair_idx_set = set()
    glass_idx_set = set()
    for i, bid in enumerate(ir.block_ids):
        cls = classify_block(bid, ir.properties[i])
        if cls == "DOOR":
            door_idx_set.add(i)
        elif cls == "LADDER":
            ladder_idx_set.add(i)
        elif cls == "STAIR":
            stair_idx_set.add(i)
        if "glass" in bid:
            glass_idx_set.add(i)

    if door_idx_set:
        door_mask = np.isin(pid_of, list(door_idx_set))
        door_coords = np.argwhere(door_mask)
        for x, y, z in door_coords:
            props = ir.properties[int(pid_of[x, y, z])]
            if props.get("half", "lower") == "lower":
                door_lower_positions.append((int(x), int(y), int(z)))
    rec["door_count"] = len(door_lower_positions)
    basis["door_count"] = OBSERVED

    # exterior_door_candidates：门扇 4 邻存在外部空气
    exterior_doors: list[dict] = []
    for (x, y, z) in door_lower_positions:
        for nx, nz, facing in ((x - 1, z, "west"), (x + 1, z, "east"),
                               (x, z - 1, "north"), (x, z + 1, "south")):
            if 0 <= nx < X and 0 <= nz < Z and exterior_air[nx, y, nz]:
                exterior_doors.append({"pos": [x, y, z], "facing_out": facing})
                break
    rec["exterior_door_candidates"] = len(exterior_doors)
    basis["exterior_door_candidates"] = HEURISTIC
    rec["entrance_candidates"] = exterior_doors
    basis["entrance_candidates"] = HEURISTIC
    if len(exterior_doors) == 1:
        rec["main_entrance"] = exterior_doors[0]
        rec["entrance_orientation"] = exterior_doors[0]["facing_out"]
        basis["main_entrance"] = HEURISTIC
        basis["entrance_orientation"] = HEURISTIC
    else:
        rec["main_entrance"] = UNKNOWN
        rec["entrance_orientation"] = UNKNOWN
        basis["main_entrance"] = UNKNOWN
        basis["entrance_orientation"] = UNKNOWN

    rec["window_count_estimate"] = int(np.isin(pid_of, list(glass_idx_set)).sum()) if glass_idx_set else 0
    basis["window_count_estimate"] = HEURISTIC  # 玻璃体素计数≈窗面积，非“窗个数”

    if stair_idx_set:
        stair_mask = np.isin(pid_of, list(stair_idx_set))
    rec["stair_count"] = int(stair_mask.sum())
    basis["stair_count"] = OBSERVED
    if rec["stair_count"] > 0:
        struct26 = np.ones((3, 3, 3), dtype=int)
        _, n_stair_clusters = ndimage.label(stair_mask, structure=struct26)
        rec["stair_cluster_count"] = int(n_stair_clusters)
    else:
        rec["stair_cluster_count"] = 0
    basis["stair_cluster_count"] = HEURISTIC  # 26 连通聚类定义属本工程约定

    ladder_columns = 0
    ladder_voxels_n = 0
    if ladder_idx_set:
        ladder_mask = np.isin(pid_of, list(ladder_idx_set))
        ladder_voxels_n = int(ladder_mask.sum())
        cols: dict[tuple[int, int], list[int]] = {}
        for x, y, z in np.argwhere(ladder_mask):
            cols.setdefault((int(x), int(z)), []).append(int(y))
        ladder_columns = len(cols)
    rec["ladder_count"] = ladder_voxels_n
    rec["vertical_access_candidates"] = rec["stair_cluster_count"] + ladder_columns
    basis["ladder_count"] = OBSERVED
    basis["ladder_column_count"] = OBSERVED
    rec["ladder_column_count"] = ladder_columns
    basis["vertical_access_candidates"] = HEURISTIC

    # ---- 收尾 -------------------------------------------------------------
    rec["ir_source"] = ir.ir_source
    basis["ir_source"] = OBSERVED
    rec["_basis"] = basis
    return rec


def main() -> None:
    ap = argparse.ArgumentParser(description="批量提取蓝图 Metadata DB")
    ap.add_argument("--references-root", required=True)
    ap.add_argument("--catalog", required=True)
    ap.add_argument("--output", required=True, help="输出目录（02_BLUEPRINT_METADATA）")
    args = ap.parse_args()

    root = Path(args.references_root)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    families = load_palette_dictionary(out_dir / "palette_dictionary.json")

    catalog = {it["reference_id"]: it for it in json.loads(Path(args.catalog).read_text(encoding="utf-8"))}
    ref_dirs = sorted(p for p in (root / "derived").iterdir() if p.is_dir() and p.name.startswith("REF-"))

    records: list[dict] = []
    failures: list[dict] = []
    for rd in ref_dirs:
        try:
            records.append(extract_one(rd, catalog.get(rd.name), families))
        except Exception as exc:  # noqa: BLE001 — 批次纪律：单张失败不中断
            failures.append({
                "ref_id": rd.name,
                "status": "PARSE_FAILURE",
                "file": str(rd),
                "error": f"{type(exc).__name__}: {exc}",
                "possible_reason": "IR 文件损坏或结构偏离 schema_version=1",
            })

    jsonl_path = out_dir / "blueprint_metadata.jsonl"
    with jsonl_path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
        for r in failures:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # CSV：扁平主要字段
    import csv

    flat_fields = [
        "ref_id", "status", "source_file", "source_name", "data_version",
        "normalized_status", "region_count", "size_x", "size_y", "size_z",
        "bounding_volume", "non_air_blocks", "air_blocks", "occupancy_ratio",
        "unique_block_states", "unique_block_types", "palette_entropy",
        "wood_ratio", "stone_ratio", "glass_ratio", "metal_ratio",
        "decorative_ratio", "functional_block_ratio", "unknown_material_ratio",
        "footprint_area", "solid_volume", "surface_area_estimate",
        "width_height_ratio", "depth_height_ratio",
        "symmetry_x", "symmetry_z", "exterior_shell_ratio", "interior_air_ratio",
        "estimated_floor_count", "floor_detection_confidence", "usable_floor_area",
        "door_count", "exterior_door_candidates", "window_count_estimate",
        "stair_count", "stair_cluster_count", "ladder_count",
        "vertical_access_candidates",
        "walkable_voxels", "walkable_components", "largest_component_ratio",
        "isolated_space_count", "vertical_connections", "dead_end_count",
        "ir_source",
    ]
    csv_path = out_dir / "blueprint_metadata.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=flat_fields, extrasaction="ignore")
        w.writeheader()
        for r in records + failures:
            w.writerow({k: r.get(k, "") for k in flat_fields})

    # 汇总统计（供报告）
    basis_fields = sorted({k for r in records for k in r.get("_basis", {})})
    unknown_by_field = {}
    for k in basis_fields:
        n_unk = sum(1 for r in records if r["_basis"].get(k) == UNKNOWN)
        unknown_by_field[k] = {"unknown": n_unk, "total": len(records),
                               "ratio": round(n_unk / len(records), 4) if records else 0.0}
    summary = {
        "total": len(ref_dirs),
        "success": len(records),
        "parse_failures": failures,
        "unknown_ratio_by_field": dict(sorted(unknown_by_field.items(),
                                              key=lambda kv: -kv[1]["ratio"])),
        "floor_count_distribution": dict(Counter(str(r.get("estimated_floor_count")) for r in records)),
        "component_count_distribution": dict(Counter(str(r.get("walkable_components")) for r in records)),
        "confidence_distribution": dict(Counter(str(r.get("floor_detection_confidence")) for r in records)),
    }
    (out_dir / "extraction_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"success": len(records), "failures": len(failures),
                      "jsonl": str(jsonl_path), "csv": str(csv_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
