// ============================================================================
// Rathaus und Kaufhaus der Stadt Wiethmar（约 1500）— Builder Core 生成器
// v1.10 §7 生成顺序：
//   Program/Space Graph → Plan+Section → 结构体系 → Circulation
//   → Massing/Roofline → Envelope/Openings → Core Facade
//
// 空间图：
//   市场广场 → 拱廊(摊/市秤) → 交易厅 → 北穿通 → 过磅间 → 北院(卸货)
//   市场广场 → 大楼梯门廊 → 上层前厅 → 大厅 → 议事厅 / 市长室 / 法院厅
//   北院 → 后勤门 → 后穿通 → 服务梯 → 上层后勤
//
// 竖向：街道 0 ｜ 交易层地坪 1 ｜ 起拱 3 ｜ 拱腹 4 ｜ 楼板 5-6 ｜ 大厅地坪 7
//       大厅檐口 17 ｜ 屋脊 30 ｜ 山墙顶 36
// ============================================================================
import { Builder, S, AIR } from './几何核心.mjs';
import { G, M, STAIR, SLAB, arch, archProfile, barrelZ, bayOpen, bayMid } from './设计参数.mjs';

const inRect = (x, z, ax, bx, az, bz) => x >= ax && x <= bx && z >= az && z <= bz;
const ribBands = () => { const a = []; for (let i = 0; i < G.zPier.length - 1; i++) a.push(G.zPier[i] + 2, G.zPier[i] + 4); return a; };

/** 门洞（墙体法向为 x）：先挖空，再加门套与门楣，最后放门扇。
 *  frameSide: 'both' 两侧门套；'inner' 只在 z 较大一侧；'outer' 只在 z 较小一侧。
 *  （单侧门套用于外墙入口，避免门套伸到室外台阶上形成 4 格高的墙。） */
function portalX(b, { x1, x2, zFrom, zTo, yFrom, yTo, frame, head = null, door = null, frameSide = 'both' }) {
  for (let z = zFrom; z <= zTo; z++) for (let y = yFrom; y <= yTo; y++) for (let x = x1; x <= x2; x++) b.override(x, y, z, AIR, '门洞');
  if (frame) {
    for (let x = x1; x <= x2; x++) {
      for (let y = yFrom; y <= yTo; y++) {
        if (frameSide !== 'inner') b.override(x, y, zFrom - 1, frame, '门套');
        if (frameSide !== 'outer') b.override(x, y, zTo + 1, frame, '门套');
      }
      for (let z = zFrom; z <= zTo; z++) b.override(x, yTo + 1, z, head || frame, '门楣');
    }
  }
  if (door) {
    const wide = zTo - zFrom + 1, half = Math.ceil(wide / 2);
    for (let i = 0; i < wide; i++) {
      const z = zFrom + i, hinge = i < half ? 'left' : 'right';
      for (let y = yFrom; y <= Math.min(yFrom + 1, yTo); y++) {
        b.override(door.x, y, z, S(door.material, { facing: door.facing, half: y === yFrom ? 'lower' : 'upper', hinge, open: 'false' }), '门扇');
      }
    }
  }
}

/** 门洞（墙体法向为 z）。 */
function portalZ(b, { z1, z2, xFrom, xTo, yFrom, yTo, frame, door = null }) {
  for (let x = xFrom; x <= xTo; x++) for (let y = yFrom; y <= yTo; y++) for (let z = z1; z <= z2; z++) b.override(x, y, z, AIR, '门洞');
  if (frame) {
    for (let z = z1; z <= z2; z++) {
      for (let y = yFrom; y <= yTo; y++) { b.override(xFrom - 1, y, z, frame, '门套'); b.override(xTo + 1, y, z, frame, '门套'); }
      for (let x = xFrom; x <= xTo; x++) b.override(x, yTo + 1, z, frame, '门楣');
    }
  }
  if (door) {
    const wide = xTo - xFrom + 1, half = Math.ceil(wide / 2);
    for (let i = 0; i < wide; i++) {
      const x = xFrom + i, hinge = i < half ? 'left' : 'right';
      for (let y = yFrom; y <= Math.min(yFrom + 1, yTo); y++) {
        b.override(x, y, door.z, S(door.material, { facing: door.facing, half: y === yFrom ? 'lower' : 'upper', hinge, open: 'false' }), '门扇');
      }
    }
  }
}

// ------------------------------------------------------------------ S1 场地
export function stageSite(b) {
  b.beginStage('S1-场地与台基');
  const SITE = { x1: -22, x2: 44, z1: -20, z2: 54 };
  for (let x = SITE.x1; x <= SITE.x2; x++) for (let z = SITE.z1; z <= SITE.z2; z++) {
    const n = Math.abs(((x * 2246822519) ^ (z * 3266489917)) % 100);
    b.paint(x, G.yStreet - 1, z, n < 70 ? M.cobbleA : n < 92 ? M.cobbleC : M.rubble, '自然地面');
  }
  for (let x = SITE.x1; x <= SITE.x2; x++) for (let z = SITE.z1; z <= SITE.z2; z++) {
    if (inRect(x, z, 5, 25, -1, 45) || inRect(x, z, 0, 8, -8, -2)) continue;
    const n = Math.abs(((x * 73856093) ^ (z * 19349663)) % 100);
    b.paint(x, G.yStreet, z, n < 24 ? M.cobbleB : n < 38 ? M.cobbleC : n < 45 ? M.plinth : M.cobbleA, '铺地');
  }
  for (let x = -22; x <= 2; x++) for (let z = -7; z <= -1; z++) b.paint(x, G.yStreet, z, ((x + z) % 3 === 0) ? M.plinth : M.cobbleB, '主通道');
  // 建筑北侧排水沟（位于广场侧，不侵占拱廊通行带 x=3..5；去向：东端集水坑）
  for (let z = -2; z <= 50; z++) { b.paint(1, G.yStreet, z, M.paving, '排水沟'); b.paint(2, G.yStreet, z, SLAB(M.slabTile), '排水沟盖板'); }
  for (let x = 1; x <= 4; x++) for (let z = 50; z <= 52; z++) b.paint(x, G.yStreet, z, M.paving, '集水坑');
  for (let x = -6; x <= 26; x++) {
    for (let z = -14; z <= -8; z++) b.paint(x, G.yStreet, z, ((x * 3 + z) % 5 < 2) ? M.cobbleB : M.cobbleA, '巷道');
    for (let z = 49; z <= 54; z++) b.paint(x, G.yStreet, z, ((x * 3 + z) % 5 < 2) ? M.cobbleB : M.cobbleA, '巷道');
  }
  for (let x = 5; x <= 25; x++) for (let z = -1; z <= 45; z++) {
    const edge = x === 5 || x === 25 || z === -1 || z === 45;
    b.paint(x, G.yStreet, z, edge ? M.plinthDark : M.plinth, '台基勒脚');
    if (edge) b.paint(x, G.yGround, z, M.plinth, '台基顶');
  }
  for (let x = 0; x <= 8; x++) for (let z = -8; z <= -2; z++) {
    const edge = x === 0 || x === 8 || z === -8 || z === -2;
    b.paint(x, G.yStreet, z, edge ? M.plinthDark : M.plinth, '门廊台基');
    if (edge) b.paint(x, G.yGround, z, M.plinth, '门廊台基顶');
  }
  // 门前台阶：广场(y=0) → 门廊地坪(y=1)，一级整步（在 S8 与门廊一并完成）
  for (let x = 25; x <= 40; x++) for (let z = -2; z <= 34; z++) {
    const n = Math.abs(((x * 40503) ^ (z * 12289)) % 100);
    b.paint(x, G.yStreet, z, n < 52 ? M.cobbleA : n < 78 ? M.cobbleC : M.cobbleB, '北院');
  }
  for (let z = -2; z <= 34; z++) { b.box(40, G.yGround, z, 40, 2, z, M.rubble); b.set(40, 3, z, M.plinthDark); }
  for (let x = 33; x <= 40; x++) { b.box(x, G.yGround, 34, x, 2, 34, M.rubble); b.set(x, 3, 34, M.plinthDark); }
  for (let x = 30; x <= 32; x++) for (let y = G.yGround; y <= 2; y++) b.override(x, y, 34, AIR, '院门');
  for (let dx = 0; dx <= 1; dx++) for (let dz = 0; dz <= 1; dz++) {
    b.override(33 + dx, G.yGround, 11 + dz, AIR, '井口');
    b.paint(33 + dx, G.yGround - 1, 11 + dz, 'minecraft:water', '井水');
  }
  for (let dx = -1; dx <= 2; dx++) for (let dz = -1; dz <= 2; dz++) {
    if (dx >= 0 && dx <= 1 && dz >= 0 && dz <= 1) continue;
    b.box(33 + dx, G.yGround, 11 + dz, 33 + dx, G.yGround + 1, 11 + dz, M.rubble);
  }
  b.box(33, G.yGround + 2, 11, 34, G.yGround + 2, 12, M.timber);
  return b;
}

// ------------------------------------------------------------------ S2 地窖
export function stageCellar(b) {
  b.beginStage('S2-地窖');
  b.plate(6, 0, 24, 44, G.yCellarFloor, M.paving);
  // 地窖墙壳：只占拱券区（y=-3..-1），不侵入台基（y=0）与地面层（y=1）
  const shellY0 = G.yCellarFloor + 1, shellY1 = G.yCellarCrown - 1;
  for (let x = 6; x <= 7; x++) for (let z = 1; z <= 43; z++) for (let y = shellY0; y <= shellY1; y++) b.paint(x, y, z, M.rubble, '地窖墙');
  for (let x = 23; x <= 24; x++) for (let z = 1; z <= 43; z++) for (let y = shellY0; y <= shellY1; y++) b.paint(x, y, z, M.rubble, '地窖墙');
  for (let x = 8; x <= 22; x++) for (let z = 1; z <= 2; z++) for (let y = shellY0; y <= shellY1; y++) b.paint(x, y, z, M.rubble, '地窖墙');
  for (let x = 8; x <= 22; x++) for (let z = 42; z <= 43; z++) for (let y = shellY0; y <= shellY1; y++) b.paint(x, y, z, M.rubble, '地窖墙');
  for (const px of [11, 18]) for (let z = 4; z <= 40; z += 6) b.box(px, G.yCellarFloor + 1, z, px + 1, G.yCellarSpring, z + 1, M.pierStone);
  barrelZ(b, { xa: 8, xb: 11, springY: G.yCellarSpring, rise: G.yCellarCrown - G.yCellarSpring, zFrom: 3, zTo: 41, crownFill: M.rib, bellyFill: M.wall, ribZ: [15, 31], ribState: M.rib });
  barrelZ(b, { xa: 13, xb: 18, springY: G.yCellarSpring, rise: G.yCellarCrown - G.yCellarSpring, zFrom: 3, zTo: 41, crownFill: M.rib, bellyFill: M.wall, ribZ: [15, 31], ribState: M.rib });
  barrelZ(b, { xa: 20, xb: 22, springY: G.yCellarSpring, rise: G.yCellarCrown - G.yCellarSpring, zFrom: 3, zTo: 41, crownFill: M.rib, bellyFill: M.wall, ribZ: [15, 31], ribState: M.rib });
  for (const zw of [15, 31]) b.box(8, G.yCellarFloor + 1, zw, 22, G.yCellarSpring - 1, zw, M.rubble);
  // 地窖楼梯（x=8..10，自交易层 z=26 向北下到地窖 z=32），并在交易层留井口
  for (let i = 0; i < 7; i++) {
    const y = G.yCellarFloor + i, z = 26 + i;
    for (let x = 8; x <= 10; x++) {
      b.paint(x, y, z, M.paving, '地窖梯');
      for (let y2 = G.yCellarFloor; y2 < y; y2++) b.paint(x, y2, z, AIR, '地窖梯井');
      for (let y2 = y + 1; y2 <= G.yGround + 2; y2++) b.paint(x, y2, z, AIR, '地窖梯净空');
    }
  }
  // 交易层井口（位于梯段顶端，z=30..33；不得覆盖梯段本身，否则梯段会被挖掉）
  for (let z = 30; z <= 33; z++) for (let x = 8; x <= 10; x++) for (let y = G.yGround; y <= G.yGround + 2; y++) b.paint(x, y, z, AIR, '地窖井口');
  for (let x = 8; x <= 10; x++) b.paint(x, G.yGround, 24, SLAB(M.slabPier), '地窖井口收边');
  return b;
}

// ------------------------------------------------------------------ S3 交易层
export function stageGround(b) {
  b.beginStage('S3-交易层');
  // 地面
  b.plate(6, 0, 24, 44, G.yGround, M.paving);
  b.plate(3, 0, 5, 48, G.yGround, M.pavingIn);
  // 拱廊外柱列
  for (const z of G.zPier) {
    b.box(3, G.yGround, z, 4, G.yGround + 1, z + 1, M.pierStone);
    b.box(3, G.yGround + 2, z, 4, G.ySpring, z + 1, M.pierStone);
    b.box(3, G.ySpring + 1, z - 1, 4, G.ySpring + 1, z + 2, M.light);
  }
  // 拱廊外沿：券脚以上砌实为实墙（承大厅南墙窗下墙），顶部为披檐下的挑檐收口
  b.box(3, G.yCrown + 1, 0, 5, G.yCrown + 4, 48, M.wall);
  b.box(3, G.yGround, 0, 5, G.yDeckTop, 0, M.wall);
  b.box(3, G.yGround, 48, 5, G.yDeckTop, 48, M.wall);
  // 拱廊纵向筒拱：起拱 y=4，冠 y=5（净高 4 格，与交易厅同高）
  barrelZ(b, { xa: 3, xb: 5, springY: G.ySpring + 1, rise: G.yCrown - G.ySpring - 1, zFrom: 1, zTo: 47, crownFill: M.wall, bellyFill: M.wall, ribZ: ribBands(), ribState: M.rib });
  // 南墙 / 北墙 / 端墙
  b.box(6, G.yGround, 0, 7, G.yDeckTop, 44, M.wall);
  b.box(18, G.yGround, 0, 19, G.yDeckTop, 44, M.wall);
  b.box(6, G.yGround, 0, 24, G.yDeckTop, 1, M.wall);
  b.box(6, G.yGround, 43, 24, G.yDeckTop, 44, M.wall);
  // 中列柱
  for (const z of G.zPier) {
    b.box(11, G.yGround, z, 13, G.yGround + 1, z + 1, M.pierStone);
    b.box(11, G.yGround + 2, z, 13, G.ySpring + 1, z + 1, M.pierStone);
    b.box(10, G.ySpring + 2, z - 1, 14, G.ySpring + 2, z + 2, M.light);
  }
  // 交易厅两道纵向筒拱：起拱 y=4、冠 y=5 → 交易厅净高 4 格（与拱廊连续）
  barrelZ(b, { xa: 8, xb: 10, springY: G.ySpring + 1, rise: G.yCrown - G.ySpring - 1, zFrom: 2, zTo: 42, crownFill: M.wall, bellyFill: M.wall, ribZ: ribBands(), ribState: M.rib });
  barrelZ(b, { xa: 14, xb: 17, springY: G.ySpring + 1, rise: G.yCrown - G.ySpring - 1, zFrom: 2, zTo: 42, crownFill: M.wall, bellyFill: M.wall, ribZ: ribBands(), ribState: M.rib });
  // 后勤翼隔墙与门洞
  for (const zw of [8, 18, 28, 38]) b.box(20, G.yGround, zw, 24, G.yDeckTop, zw + 1, M.wall);
  return b;
}

// ------------------------------------------------------------------ S4 楼板
export function stageFloor(b) {
  b.beginStage('S4-楼板与披檐');
  // 主楼板：只覆盖建筑主体（x=6..24），拱廊另有自己的披檐
  b.plate(6, 0, 24, 44, G.yDeck, M.timberLog);
  b.plate(6, 0, 24, 44, G.yDeckTop, M.timber);
  // 主梁（沿 x，落在柱列与墙上）
  for (const z of G.zPier) {
    for (let x = 6; x <= 24; x++) b.paint(x, G.yDeck, z, M.beam, '主梁');
    for (let x = 6; x <= 24; x++) b.paint(x, G.yDeck, z + 1, M.beam, '主梁');
  }
  // 搁栅（沿 z）
  for (let x = 8; x <= 22; x += 2) for (let z = 0; z <= 44; z++) if (b.get(x, G.yDeck, z) === M.timberLog) b.paint(x, G.yDeck, z, M.timberStrip, '搁栅');
  // 拱廊披檐（单坡，自交易厅前墙向外檐倾斜，只覆盖拱廊 x=3..5；檐口在 y=10）
  for (let x = 3; x <= 5; x++) {
    const y = G.yCrown + 5 + (x - 3);
    for (let z = -1; z <= 49; z++) b.set(x, y, z, M.roofTile);
  }
  for (let z = -1; z <= 49; z++) { b.set(3, G.yCrown + 5, z, STAIR(M.sTile, 'north')); b.set(2, G.yCrown + 5, z, SLAB(M.slabTile)); }
  // 大厅地坪面层
  b.plate(6, 0, 24, 44, G.yGreatFloor, M.timber);
  // 中列柱柱头托臂
  for (const z of G.zPier) for (let dz = 0; dz <= 1; dz++) { b.set(10, G.ySpring + 3, z + dz, SLAB(M.slabPier)); b.set(14, G.ySpring + 3, z + dz, SLAB(M.slabPier)); }
  return b;
}

// ------------------------------------------------------------------ S5 上层
export function stageUpper(b) {
  b.beginStage('S5-上层大厅');
  const y0 = G.yGreatFloor;
  b.box(6, y0, 0, 7, G.yWallTop, 44, M.wall);
  b.box(18, y0, 0, 19, G.yWallTop, 44, M.wall);
  b.box(6, y0, 0, 24, G.yWallTop, 1, M.wall);
  b.box(6, y0, 43, 24, G.yWallTop, 44, M.wall);
  // 大厅南向 3 樘大窗（面向市场）
  for (const [za, zb] of [[8, 13], [19, 24], [30, 35]]) windowXMain(b, { x1: 6, x2: 7, zFrom: za, zTo: zb, sill: G.ySill, spring: G.ySill + 3, rise: 3, frame: M.light });
  // 后墙 2 樘
  for (const [za, zb] of [[10, 14], [28, 32]]) windowXMain(b, { x1: 18, x2: 19, zFrom: za, zTo: zb, sill: G.ySill + 1, spring: G.ySill + 4, rise: 2, frame: M.trim, bars: true });
  // 东西山墙窗
  windowZMain(b, { z1: 0, z2: 1, xFrom: 10, xTo: 15, sill: G.ySill + 1, spring: G.ySill + 4, rise: 2, frame: M.trim });
  windowZMain(b, { z1: 43, z2: 44, xFrom: 10, xTo: 15, sill: G.ySill + 1, spring: G.ySill + 4, rise: 2, frame: M.trim });
  // 阶梯山墙（东西两端）
  steppedGableZ(b, { z1: 0, z2: 1, xFrom: 6, xTo: 24, y0: G.yWallTop + 1, yTop: G.yGableTop });
  steppedGableZ(b, { z1: 43, z2: 44, xFrom: 6, xTo: 24, y0: G.yWallTop + 1, yTop: G.yGableTop });
  // 上层：大厅为完整无柱空间；辅助房间沿北墙（x=20..24 低檐区）分隔
  for (const zw of [10, 21, 32]) b.box(20, y0, zw, 24, G.yWallTop - 5, zw + 1, M.wall);
  b.box(20, y0, 2, 20, G.yWallTop - 5, 42, M.wall);
  // 辅助房间门洞（通大厅）
  for (const zw of [10, 21, 32]) for (let z = zw + 1; z <= zw + 2; z++) for (let x = 20; x <= 21; x++) for (let y = y0; y <= y0 + 2; y++) b.override(x, y, z, AIR, '房间门');
  return b;
}

function windowXMain(b, { x1, x2, zFrom, zTo, sill, spring, rise, frame, bars = false }) {
  const cols = archProfile({ from: zFrom, to: zTo, springY: spring, rise, curve: 'segmental' });
  const yOf = new Map(cols);
  const top = cols.reduce((a, [, y]) => Math.max(a, y), 0);
  for (let z = zFrom; z <= zTo; z++) {
    const yc = yOf.get(z) ?? top;
    for (let y = G.yGreatFloor; y <= top; y++) {
      for (let x = x1; x <= x2; x++) {
        const edge = x === x1 || x === x2;
        let st = M.glass;
        if (y < sill) st = M.wall;
        else if (y === sill) st = frame;
        else if (y >= yc) st = frame;
        else if (edge) st = frame;
        else if (bars && (z - zFrom) % 2 === 1 && y > sill + 1 && y < yc - 1) st = M.iron;
        else if (z === Math.round((zFrom + zTo) / 2) && y > sill + 1 && y < yc - 1) st = frame;
        b.override(x, y, z, st, '窗');
      }
    }
    for (let y = top + 1; y <= G.yWallTop; y++) for (let x = x1; x <= x2; x++) b.override(x, y, z, M.wall, '窗上墙');
  }
}

function windowZMain(b, { z1, z2, xFrom, xTo, sill, spring, rise, frame }) {
  const cols = archProfile({ from: xFrom, to: xTo, springY: spring, rise, curve: 'segmental' });
  const yOf = new Map(cols);
  const top = cols.reduce((a, [, y]) => Math.max(a, y), 0);
  for (let x = xFrom; x <= xTo; x++) {
    const yc = yOf.get(x) ?? top;
    for (let y = G.yGreatFloor; y <= top; y++) {
      for (let z = z1; z <= z2; z++) {
        const edge = z === z1 || z === z2;
        let st = M.glass;
        if (y < sill) st = M.wall;
        else if (y === sill || y >= yc || edge) st = frame;
        else if (x === Math.round((xFrom + xTo) / 2) && y > sill + 1 && y < yc - 1) st = frame;
        b.override(x, y, z, st, '窗');
      }
    }
    for (let y = top + 1; y <= G.yWallTop; y++) for (let z = z1; z <= z2; z++) b.override(x, y, z, M.wall, '窗上墙');
  }
}

function steppedGableZ(b, { z1, z2, xFrom, xTo, y0, yTop }) {
  const half = (xTo - xFrom) / 2;
  for (let y = y0; y <= yTop; y++) {
    const t = (y - y0) / (yTop - y0);
    const inset = Math.round(t * (half - 1));
    const a = xFrom + inset, c = xTo - inset;
    for (let x = a; x <= c; x++) {
      const edge = x === a || x === c;
      for (let z = z1; z <= z2; z++) {
        let st = M.wall;
        if (edge) st = M.quoin;
        if ((y - y0) % 5 === 2 && (x - a) % 4 === 2) st = M.glazed;
        b.paint(x, y, z, st, '山墙');
      }
    }
  }
}

// ------------------------------------------------------------------ S6 屋面
export function stageRoof(b) {
  b.beginStage('S6-屋面');
  const halfSpan = 6.5;
  for (let y = G.yWallTop + 1; y <= G.yRidge; y++) {
    const t = (y - G.yWallTop) / (G.yRidge - G.yWallTop);
    const inset = Math.round(halfSpan * t);
    const xa = 6 + inset, xb = 25 - inset;
    for (let x = xa; x <= xb; x++) for (let z = -2; z <= 46; z++) {
      b.paint(x, y, z, y >= G.yRidge ? SLAB(M.slabTile) : M.roofTile, '屋面');
    }
  }
  // 屋脊线与脊瓦
  for (let z = -2; z <= 46; z++) { b.paint(12, G.yRidge, z, M.plinthDark, '屋脊'); b.paint(13, G.yRidge, z, M.plinthDark, '屋脊'); }
  for (let z = -2; z <= 46; z++) { b.paint(12, G.yRidge + 1, z, SLAB(M.slabTile), '脊瓦'); b.paint(13, G.yRidge + 1, z, SLAB(M.slabTile), '脊瓦'); }
  // 檐口滴水（挑出 1 格）
  for (let z = -2; z <= 46; z++) {
    b.set(5, G.yWallTop, z, STAIR(M.sTile, 'north'));
    b.set(26, G.yWallTop, z, STAIR(M.sTile, 'south'));
  }
  // 老虎窗/通风缝（屋面收口，同时给阁楼采光）
  for (const z of [12, 32]) {
    b.paint(20, G.yWallTop + 5, z, AIR, '屋面通风缝');
    b.paint(21, G.yWallTop + 5, z, AIR, '屋面通风缝');
  }
  return b;
}

// ------------------------------------------------------------------ S7 钟塔
export function stageTower(b) {
  b.beginStage('S7-屋脊钟塔');
  const x1 = 11, x2 = 14, z1 = 20, z2 = 23;
  const base = G.yRidge + 2, top = G.yRidge + 9;
  for (let y = base; y <= top; y++) {
    for (let x = x1; x <= x2; x++) for (let z = z1; z <= z2; z++) {
      const edge = x === x1 || x === x2 || z === z1 || z === z2;
      if (!edge) { b.paint(x, y, z, AIR, '塔内'); continue; }
      const louvre = y >= base + 3 && y <= base + 5;
      b.paint(x, y, z, louvre && (x + z) % 2 === 0 ? AIR : M.wall, '塔身');
    }
  }
  b.box(x1, top, z1, x2, top, z2, SLAB(M.slabTile));
  b.box(x1 + 1, top + 1, z1 + 1, x2 - 1, top + 1, z2 - 1, M.plinthDark);
  b.box(x1 + 1, top + 2, z1 + 1, x2 - 1, top + 2, z2 - 1, SLAB(M.slabTile));
  b.set(12, top + 3, 21, M.plinthDark); b.set(13, top + 3, 22, M.plinthDark);
  b.set(12, top + 4, 22, M.plinthDark); b.set(13, top + 4, 21, M.plinthDark);
  b.set(12, top + 5, 21, S('minecraft:iron_chain', { axis: 'y' }));
  // 阁楼木梯（自大厅楼板经阁楼到塔层）
  for (let i = 0; i < 14; i++) {
    const y = G.yGreatFloor + 1 + i, z = 25 - Math.floor(i / 2);
    b.paint(12, y, z, S('minecraft:ladder', { facing: 'south' }), '阁楼梯');
    if (i % 2 === 1) b.paint(12, y, z, AIR, '阁楼梯井');
  }
  return b;
}

// ==========================================================================
// S8 主要开口与主楼梯（Circulation）——让建筑真正可以进入与使用
// ==========================================================================
export function stageCirculation(b) {
  b.beginStage('S8-开口与主楼梯');
  // ---- 拱廊 → 交易厅：每开间一个门洞（宽 4、高 4，落在通道层）----
  for (let i = 0; i < G.zPier.length - 1; i++) {
    const [a, c] = bayOpen(i);
    const za = a + 1, zb = c - 1;                       // 每开间 4 格宽中的中间 2 格…此处取净宽 2
    portalX(b, { x1: 6, x2: 7, zFrom: za, zTo: zb, yFrom: G.yGround, yTo: G.yGround + 3, frame: M.light, head: M.light });
  }
  // ---- 交易厅 → 北穿通：3 个门洞（同时对好后勤翼的分隔间）----
  for (const [za, zb] of [[12, 15], [24, 27], [36, 39]]) {
    portalX(b, { x1: 18, x2: 19, zFrom: za, zTo: zb, yFrom: G.yGround, yTo: G.yGround + 2, frame: M.trim });
    for (let z = za; z <= zb; z++) for (let y = G.yGround; y <= G.yGround + 2; y++) {
      for (let x = 20; x <= 23; x++) b.override(x, y, z, AIR, '后勤通道');
    }
  }
  // ---- 后勤翼 → 北院：2 个后勤门 ----
  for (const [za, zb] of [[12, 15], [30, 33]]) {
    portalX(b, { x1: 23, x2: 24, zFrom: za, zTo: zb, yFrom: G.yGround, yTo: G.yGround + 2, frame: M.trim, door: { x: 23, material: M.doorDark, facing: 'east' } });
  }
  // ---- 地窖口（交易厅南跨东段）：井口敞开，不设盖板（保证下行净空连续）----

  // ---- 主楼梯（市场进入 → 上层大厅）：南跨西端，直跑 ----
  // 楼梯间：x=8..10，z=3..9。井道贯通楼板与交易厅拱顶，保证平台上方净空。
  const sx1 = 8, sx2 = 10, sz1 = 3, sz2 = 9;
  for (let z = sz1; z <= sz2; z++) for (let x = sx1; x <= sx2; x++) {
    for (let y = G.yVaultSpring; y <= G.yGreatFloor + 2; y++) b.override(x, y, z, AIR, '主楼梯井道');
  }
  // 井道正上方的楼板主梁必须断开（否则梁底 y=5 会切断梯段净空）
  for (let z = sz1; z <= sz2; z++) for (let x = sx1; x <= sx2; x++) b.override(x, G.yDeck, z, AIR, '井道处主梁断开');
  // 梁端做托臂收头（结构可读：梁由两侧墙/柱承托，跨过楼梯井）
  for (const z of [sz1 - 1, sz2 + 1]) for (let x = sx1 - 1; x <= sx2 + 1; x++) b.override(x, G.yDeck - 1, z, SLAB(M.slabPier), '梁端托臂');
  // 梯段：自 z=9（y=1）向北升至 z=4（y=6）；每级 1 格，级上 2 格净空
  for (let i = 0; i < 6; i++) {
    const y = G.yGround + i, z = sz2 - i;
    for (let x = sx1; x <= sx2; x++) {
      b.override(x, y, z, M.plinth, '主楼梯踏步');
      b.override(x, y + 1, z, AIR, '主楼梯净空');
      b.override(x, y + 2, z, AIR, '主楼梯净空');
    }
  }
  // 梯段东侧栏墙（阅读为石作楼梯）
  for (let z = sz1; z <= sz2; z++) {
    const i = Math.max(0, sz2 - z);
    b.override(11, G.yGround + i, z, M.plinthDark, '楼梯栏墙');
    b.override(11, G.yGround + i + 1, z, SLAB(M.slabPier), '楼梯栏墙');
  }
  // 顶部过渡（z=3）：半砖台阶，衔接末级踏步(y=6)与大厅地坪(y=7)，避免 1 格跳跃
  for (let x = sx1; x <= sx2; x++) {
    b.override(x, G.yGround + 5, sz1, SLAB(M.slabPier), '主楼梯平台半砖');
    for (let y = G.yGround + 6; y <= G.yGround + 8; y++) b.override(x, y, sz1, AIR, '平台净空');
  }
  // 平台与大厅地坪之间的衔接踏步（z=2，落在南墙内）
  for (let x = sx1; x <= sx2; x++) {
    b.override(x, G.yGreatFloor, sz1 - 1, M.paving, '衔接踏步');
    for (let y = G.yGreatFloor + 1; y <= G.yGreatFloor + 3; y++) b.override(x, y, sz1 - 1, AIR, '衔接净空');
  }
  // 大厅地坪上的楼梯井口收边（护栏）
  for (let x = sx1; x <= sx2; x++) b.override(x, G.yGreatFloor + 1, sz2 + 1, SLAB(M.slabPier), '井口护栏');
  for (let z = sz1; z <= sz2 + 1; z++) b.override(sx1 - 1, G.yGreatFloor + 1, z, SLAB(M.slabPier), '井口护栏');
  // ---- 大厅入口门（自平台穿南墙）----
  portalX(b, { x1: 6, x2: 7, zFrom: sz1, zTo: sz1 + 1, yFrom: G.yGreatFloor, yTo: G.yGreatFloor + 3, frame: M.light, door: { x: 6, material: M.doorDark, facing: 'south' } });
  // ---- 入口门廊（广场 → 建筑）：地面、门洞、围护、台阶 ----
  // 门廊内部：x=1..7, z=-7..-3；地坪 y=1
  for (let x = 1; x <= 7; x++) for (let z = -7; z <= -3; z++) b.override(x, G.yGround, z, M.pavingIn, '门廊地面');
  // 前墙（厚 2 格：z=-9 与 z=-8），高到披檐
  for (let x = 0; x <= 8; x++) for (let z = -9; z <= -8; z++) {
    b.box(x, G.yGround + 1, z, x, G.yDeckTop, z, M.wall);
    b.box(x, G.yDeckTop + 1, z, x, G.yDeckTop + 1, z, M.plinthDark);
  }
  // 侧墙（含门廊窗）
  for (let z = -9; z <= -3; z++) {
    b.box(0, G.yGround + 1, z, 0, G.yDeckTop, z, M.wall);
    b.box(8, G.yGround + 1, z, 8, G.yDeckTop, z, M.wall);
  }
  // 侧墙上的窗（门廊采光）
  for (const xw of [0, 8]) for (const zw of [-6, -4]) {
    for (let y = G.yGround + 2; y <= G.yGround + 3; y++) b.override(xw, y, zw, M.glass, '门廊窗');
  }
  // 门廊入口门洞（前墙正中，贯穿 2 格墙厚）
  portalX(b, { x1: 2, x2: 6, zFrom: -9, zTo: -8, yFrom: G.yGround, yTo: G.yGround + 3, frame: M.light, head: M.light, frameSide: 'inner', door: { x: 2, material: M.doorOak, facing: 'north' } });
  // 门廊 → 拱廊（东侧开口）
  portalZ(b, { z1: -3, z2: -3, xFrom: 2, xTo: 6, yFrom: G.yGround, yTo: G.yGround + 3, frame: M.light });
  // 门前台阶：广场(y=0) → 半砖(y=0.5) → 门廊地坪(y=1)
  for (let x = 3; x <= 5; x++) {
    b.paint(x, G.yStreet, -11, SLAB(M.slabPier), '门前台阶');
    b.paint(x, G.yStreet, -10, M.plinth, '门前台阶');
  }
  // 台阶两侧矮墙（栏杆）
  for (const xr of [2, 6]) for (let z = -11; z <= -10; z++) {
    b.paint(xr, G.yGround, z, M.plinth, '台阶栏杆');
    b.paint(xr, G.yGround + 1, z, SLAB(M.slabPier), '台阶栏杆');
  }
  // 门廊屋顶（平缓单坡，与拱廊披檐连续）
  for (let x = 0; x <= 8; x++) for (let z = -9; z <= -3; z++) b.paint(x, G.yDeckTop + 1, z, M.roofTile, '门廊屋面');
  for (let z = -9; z <= -3; z++) { b.set(9, G.yDeckTop + 1, z, STAIR(M.sTile, 'west')); }
  return b;
}
