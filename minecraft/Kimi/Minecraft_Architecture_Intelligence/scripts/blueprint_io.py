# -*- coding: utf-8 -*-
"""blueprint_io — Canonical Blueprint IR 加载与体素化共享模块（项目代号 H）。

职责：
1. 加载 Canonical IR：优先 ``normalized/normalized-blueprint.json``，
   缺失时回退 ``blueprint.json``，并在结果中记录实际使用的来源（ir_source）。
2. 解析 palette block state 字符串：
   ``minecraft:oak_stairs[facing=north,half=bottom]`` → ``("minecraft:oak_stairs", {"facing": "north", "half": "bottom"})``
3. 构建 3D 体素数组（numpy，int32，值为 palette 索引），坐标最小值归零；
   包络内未被 blocks 覆盖的坐标按 air 处理（若 palette 无 air 则追加一个）。

本模块不写任何文件到参考库；只读。

用法（CLI 自检）：
    python blueprint_io.py <REF目录或blueprint.json路径> --info
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import numpy as np

# block state 字符串：<namespace>:<block_id>[k=v,k=v]
_STATE_RE = re.compile(r"^(?P<id>[a-z0-9_.:]+?)(?:\[(?P<props>[^\]]*)\])?$")

AIR_IDS = ("minecraft:air", "minecraft:cave_air", "minecraft:void_air")


def parse_block_state(state: str) -> tuple[str, dict[str, str]]:
    """解析完整 block state 字符串，返回 (block_id, properties dict)。

    解析失败时抛 ValueError（由调用方按 PARSE_FAILURE 纪律处理）。
    """
    m = _STATE_RE.match(state.strip())
    if not m:
        raise ValueError(f"无法解析 block state: {state!r}")
    block_id = m.group("id")
    props: dict[str, str] = {}
    raw = m.group("props")
    if raw:
        for kv in raw.split(","):
            if "=" not in kv:
                raise ValueError(f"无法解析 block state 属性: {state!r}")
            k, v = kv.split("=", 1)
            props[k.strip()] = v.strip()
    return block_id, props


@dataclass
class BlueprintIR:
    """一张蓝图的 Canonical IR 内存表示。"""

    path: Path                      # 实际读取的 IR 文件
    ir_source: str                  # "normalized" | "canonical"（回退时记录）
    ref_id: Optional[str]           # 从目录名推断（REF-xxxx），否则 None
    schema_version: int
    metadata: dict
    origin: tuple[int, int, int]
    dimensions: tuple[int, int, int]
    rotation: object
    mirror: object
    palette: list[str]                       # 原始 block state 字符串
    block_ids: list[str]                     # palette 每项的 block_id
    properties: list[dict[str, str]]         # palette 每项的属性 dict
    blocks: np.ndarray                       # shape (n, 4) int32: [x,y,z,palette_index]
    raw: dict = field(repr=False, default_factory=dict)

    @property
    def air_indices(self) -> set[int]:
        return {i for i, bid in enumerate(self.block_ids) if bid in AIR_IDS}


def _find_ir_file(path: Path) -> tuple[Path, str, Optional[str]]:
    """定位 IR 文件：接受 REF 派生目录或直接 JSON 路径。

    返回 (文件路径, ir_source, ref_id)。优先 normalized，回退 canonical。
    """
    path = Path(path)
    if path.is_dir():
        ref_id = path.name if path.name.startswith("REF-") else None
        normalized = path / "normalized" / "normalized-blueprint.json"
        canonical = path / "blueprint.json"
        if normalized.is_file():
            return normalized, "normalized", ref_id
        if canonical.is_file():
            return canonical, "canonical", ref_id
        raise FileNotFoundError(f"目录内未找到 normalized-blueprint.json / blueprint.json: {path}")
    if path.is_file():
        ref_id = path.parent.parent.name if path.parent.name == "normalized" else path.parent.name
        if not ref_id.startswith("REF-"):
            ref_id = None
        source = "normalized" if path.name == "normalized-blueprint.json" else "canonical"
        return path, source, ref_id
    raise FileNotFoundError(f"路径不存在: {path}")


def load_blueprint(path: str | Path) -> BlueprintIR:
    """加载一张蓝图的 Canonical IR（优先 normalized，回退 canonical）。"""
    file_path, ir_source, ref_id = _find_ir_file(Path(path))
    data = json.loads(file_path.read_text(encoding="utf-8"))

    palette = list(data.get("palette", []))
    block_ids: list[str] = []
    properties: list[dict[str, str]] = []
    for state in palette:
        bid, props = parse_block_state(state)
        block_ids.append(bid)
        properties.append(props)

    blocks = np.asarray(data.get("blocks", []), dtype=np.int32)
    if blocks.size == 0:
        blocks = blocks.reshape(0, 4)
    if blocks.ndim != 2 or blocks.shape[1] != 4:
        raise ValueError(f"blocks 结构异常（期望 n×4）: {file_path}")

    dims = data.get("dimensions", {})
    origin = data.get("origin", {"x": 0, "y": 0, "z": 0})
    if isinstance(origin, dict):
        origin_t = (int(origin.get("x", 0)), int(origin.get("y", 0)), int(origin.get("z", 0)))
    else:
        origin_t = tuple(int(v) for v in origin)  # type: ignore[arg-type]

    return BlueprintIR(
        path=file_path,
        ir_source=ir_source,
        ref_id=ref_id,
        schema_version=int(data.get("schema_version", 0)),
        metadata=data.get("metadata", {}),
        origin=origin_t,
        dimensions=(int(dims.get("x", 0)), int(dims.get("y", 0)), int(dims.get("z", 0))),
        rotation=data.get("rotation"),
        mirror=data.get("mirror"),
        palette=palette,
        block_ids=block_ids,
        properties=properties,
        blocks=blocks,
        raw=data,
    )


def to_voxels(ir: BlueprintIR) -> tuple[np.ndarray, int]:
    """将 IR 体素化为 numpy int32 数组（值为 palette 索引），轴序 (x, y, z)。

    - 尺寸取 dimensions 与 blocks 实际最大坐标+1 的较大者；
    - 坐标按 blocks 最小坐标归零（Canonical 契约已从包络最小角归零，此处兜底）；
    - 未覆盖坐标填 air 索引（palette 无 air 时追加一个 ``minecraft:air``）。

    返回 (voxels, air_index)。注意：若在 ir.palette 上追加 air，
    ir.block_ids / ir.properties 会同步追加（原地扩展，供下游分类使用）。
    """
    dims = ir.dimensions
    if ir.blocks.shape[0] > 0:
        min_c = ir.blocks[:, :3].min(axis=0)
        max_c = ir.blocks[:, :3].max(axis=0)
        size = np.maximum(np.array(dims, dtype=np.int32), max_c - min_c + 1)
    else:
        min_c = np.zeros(3, dtype=np.int32)
        size = np.array(dims, dtype=np.int32)
    size = np.maximum(size, 1)

    air_idx_set = ir.air_indices
    if air_idx_set:
        air_index = min(air_idx_set)
    else:
        air_index = len(ir.palette)
        ir.palette.append("minecraft:air")
        ir.block_ids.append("minecraft:air")
        ir.properties.append({})

    voxels = np.full(tuple(int(v) for v in size), air_index, dtype=np.int32)
    if ir.blocks.shape[0] > 0:
        coords = ir.blocks[:, :3] - min_c
        voxels[coords[:, 0], coords[:, 1], coords[:, 2]] = ir.blocks[:, 3]
    return voxels, air_index


def main() -> None:
    ap = argparse.ArgumentParser(description="Canonical Blueprint IR 加载自检")
    ap.add_argument("path", help="REF 派生目录或 blueprint.json 路径")
    ap.add_argument("--info", action="store_true", help="打印结构摘要")
    args = ap.parse_args()

    ir = load_blueprint(args.path)
    voxels, air_index = to_voxels(ir)
    if args.info:
        print(json.dumps({
            "path": str(ir.path),
            "ir_source": ir.ir_source,
            "ref_id": ir.ref_id,
            "schema_version": ir.schema_version,
            "dimensions": ir.dimensions,
            "voxel_shape": list(voxels.shape),
            "palette_size": len(ir.palette),
            "blocks": int(ir.blocks.shape[0]),
            "air_index": air_index,
            "air_voxels": int((voxels == air_index).sum()),
        }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
