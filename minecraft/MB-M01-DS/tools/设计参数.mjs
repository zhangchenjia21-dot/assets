// 设计参数与几何定义（Rathaus und Kaufhaus der Stadt Wiethmar，约 1500）
// ---------------------------------------------------------------------------
// 坐标：x 由市场侧（小）向城内（大）；z 由西端（小）向东端（大）；y 竖直。
// 竖向（街道 y=0，1 格 ≈ 0.75 m）：
//    0  广场铺地
//    1  台基顶 = 交易层地坪 / 拱廊地坪
//    3  砖墩柱头，拱顶起拱
//    5  拱顶冠（顶在楼板下皮）
//    5–6 楼板
//    7  上层大厅地坪
//   14  大厅窗顶
//   17  大厅墙顶（檐口）
//   30  屋脊
// 结构概念：一层为砖墩 + 纵向筒拱的承重防火层；二层为无柱木屋架大厅。
// ---------------------------------------------------------------------------
import { S, AIR } from './几何核心.mjs';

export const G = {
  // x 向
  xArcadeOuter: 3, xArcadeInner: 5,
  xSouthWall: 6, xSouthWallIn: 7,
  xSpineIn: 11, xSpineOut: 14,
  xNorthWallIn: 18, xNorthWall: 19,
  xServiceOut: 24,
  xBuildingWest: 6, xBuildingEast: 24,
  // z 向
  zWest: 0, zEast: 44,
  zArcadeWest: 0, zArcadeEast: 48,
  zPorchWest: -6, zPorchEast: 0,
  zPier: [0, 6, 12, 18, 24, 30, 36, 42, 48],
  // y 向
  yStreet: 0, yGround: 1,
  ySpring: 3, yCrown: 5,
  yDeck: 5, yDeckTop: 6,
  yGreatFloor: 7, ySill: 9, yWinTop: 14, yWallTop: 17, yRidge: 30, yGableTop: 36,
  yCellarFloor: -4, yCellarSpring: -2, yCellarCrown: 0,
};

export const bayOpen = (i) => [G.zPier[i] + 1, G.zPier[i + 1] - 1];
export const bayMid = (i) => G.zPier[i] + 3;

export const M = {
  plinth: 'minecraft:polished_deepslate',
  plinthDark: 'minecraft:deepslate_tiles',
  wall: 'minecraft:cinnabar_bricks',
  rubble: 'minecraft:cobbled_deepslate',
  pierStone: 'minecraft:polished_deepslate',
  rib: 'minecraft:deepslate_bricks',
  quoin: 'minecraft:deepslate_bricks',
  light: 'minecraft:polished_diorite',
  trim: 'minecraft:diorite',
  calcite: 'minecraft:calcite',
  paving: 'minecraft:deepslate_tiles',
  pavingIn: 'minecraft:polished_deepslate',
  cobbleA: 'minecraft:cobbled_deepslate',
  cobbleB: 'minecraft:stone',
  cobbleC: 'minecraft:andesite',
  timber: 'minecraft:dark_oak_planks',
  beam: 'minecraft:dark_oak_wood',
  timberLog: 'minecraft:dark_oak_log',
  timberStrip: 'minecraft:stripped_dark_oak_log',
  roofTile: 'minecraft:deepslate_tiles',
  glazed: 'minecraft:resin_bricks',
  glass: 'minecraft:glass',
  pane: 'minecraft:glass_pane',
  grayPane: 'minecraft:gray_stained_glass_pane',
  iron: 'minecraft:iron_bars',
  lantern: 'minecraft:lantern',
  torch: 'minecraft:torch',
  sWall: 'minecraft:cinnabar_brick_stairs',
  sRib: 'minecraft:deepslate_brick_stairs',
  sPier: 'minecraft:polished_deepslate_stairs',
  sTile: 'minecraft:deepslate_tile_stairs',
  sTimber: 'minecraft:dark_oak_stairs',
  sLight: 'minecraft:polished_diorite_stairs',
  slabWall: 'minecraft:cinnabar_brick_slab',
  slabRib: 'minecraft:deepslate_brick_slab',
  slabPier: 'minecraft:polished_deepslate_slab',
  slabTile: 'minecraft:deepslate_tile_slab',
  slabTimber: 'minecraft:dark_oak_slab',
  slabLight: 'minecraft:polished_diorite_slab',
  doorOak: 'minecraft:oak_door',
  doorDark: 'minecraft:dark_oak_door',
  doorSpruce: 'minecraft:spruce_door',
  doorIron: 'minecraft:iron_door',
  trapdoorDark: 'minecraft:dark_oak_trapdoor',
};

export const STAIR = (m, facing, half = 'bottom', shape = 'straight') => S(m, { facing, half, shape });
export const SLAB = (m, type = 'bottom') => S(m, { type });

/** 拱轮廓（segmental 弓形 / round 半圆 / pointed 尖拱）。返回 [位置, 拱腹高度] 列。 */
export function archProfile({ from, to, springY, rise, curve = 'segmental' }) {
  const span = to - from, r = span / 2, c = from + r;
  const at = (t) => {
    const d = t - c;
    if (curve === 'round') {
      const rr = Math.min(r, rise);
      return springY + Math.round(Math.sqrt(Math.max(0, rr * rr - (d * rr / r) ** 2)));
    }
    if (curve === 'pointed') {
      const R = span, center = t >= c ? from : to;
      const raw = springY + Math.sqrt(Math.max(0, R * R - (t - center) ** 2)) - Math.sqrt(Math.max(0, R * R - r * r));
      return Math.min(Math.round(raw), springY + rise);
    }
    const R = (r * r + rise * rise) / (2 * rise);
    return springY + Math.round(rise - R + Math.sqrt(Math.max(0, R * R - d * d)));
  };
  const cols = [];
  for (let t = from; t <= to; t++) cols.push([t, at(t)]);
  return cols;
}

/**
 * 拱券：axis='z' 表示拱沿 z 跨越、墙法向为 x（占 fixed..fixed+thickness-1）。
 * 拱腹以下为空气，拱券石用楼梯方块，拱肩填 fill。
 */
export function arch(b, { axis, fixed, thickness = 1, from, to, springY, rise, topY, fill, voussoir, curve = 'segmental', belowToY = null, belowFill = null }) {
  const cols = archProfile({ from, to, springY, rise, curve });
  for (let i = 0; i < cols.length; i++) {
    const [t, yc] = cols[i];
    const prev = i > 0 ? cols[i - 1][1] : yc, next = i < cols.length - 1 ? cols[i + 1][1] : yc;
    const slope = (next - prev) / 2;
    const y0 = belowToY === null ? springY : belowToY;
    for (let y = y0; y <= topY; y++) {
      for (let k = 0; k < thickness; k++) {
        const px = axis === 'z' ? t : fixed + k;
        const pz = axis === 'z' ? fixed + k : t;
        if (y < yc) {
          if (y >= springY) b.set(px, y, pz, AIR);
          else b.set(px, y, pz, belowFill || fill);
        } else if (y === yc) {
          const facing = axis === 'z' ? (slope >= 0 ? 'east' : 'west') : (slope >= 0 ? 'south' : 'north');
          const shape = Math.abs(slope) < 0.35 ? 'straight' : slope > 0 ? 'outer_left' : 'outer_right';
          b.set(px, y, pz, STAIR(voussoir, facing, 'bottom', shape));
        } else {
          b.set(px, y, pz, fill);
        }
      }
    }
  }
  return cols;
}

/**
 * 纵向筒拱（沿 z 贯通）：拱腹以下挖空，拱背自 springY 到拱腹线全部砌实（真实拱背构造）。
 * 返回拱腹线，便于上层结构对齐。ribZ 处的拱腹行换成肋石，形成横向肋带。
 */
export function barrelZ(b, { xa, xb, springY, rise, zFrom, zTo, crownFill, ribZ = [], ribState = null, bellyFill = null }) {
  const cols = archProfile({ from: xa, to: xb, springY, rise, curve: 'segmental' });
  for (const [x, yc] of cols) {
    for (let z = zFrom; z <= zTo; z++) {
      const isRib = ribZ.includes(z);
      for (let y = springY; y <= yc; y++) {
        if (y === yc) b.paint(x, y, z, isRib && ribState ? ribState : crownFill, '筒拱拱腹');
        else b.paint(x, y, z, bellyFill || crownFill, '筒拱拱背');
      }
    }
  }
  return cols;
}
