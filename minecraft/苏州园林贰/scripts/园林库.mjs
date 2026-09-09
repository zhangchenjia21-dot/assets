/**
 * 园林库：苏州园林离线施工共用车间。
 * 职责：把设计几何编译为 AI-Offline 作业 JSON（palette + operations）。
 * 约定：+x 东，+z 南，y 竖直；地表草方块顶 y=63，站立面 y=64，水面 y=62。
 * 所有屋面/玻璃/树叶的连接状态在此一次性烘焙，依赖执行器"无副作用"写入。
 */
import { 水体 } from './池形.mjs';

// ── 标高常量（与 generator-options 的 1 基岩 + 126 泥土 + 1 草一致）──
export const 地表 = 63;   // 草方块顶面所在 y（方块本身）
export const 地面 = 64;   // 人站立/铺装层
export const 水面 = 62;   // 池水表层
export const 池底 = 59;   // 池底泥土/黏土顶面

// ── 材料表（统一江南语言：粉墙黛瓦栗木）──
export const M = {
  粉墙: 'minecraft:white_concrete',
  瓦: 'minecraft:deepslate_tile_stairs',
  瓦面: 'minecraft:deepslate_tile_slab[type=top,waterlogged=false]',
  瓦檐: 'minecraft:deepslate_tile_slab[type=bottom,waterlogged=false]',
  脊: 'minecraft:deepslate_tile_slab[type=bottom,waterlogged=false]',
  脊头: 'minecraft:deepslate_tile_stairs[half=top,shape=straight',
  柱: 'minecraft:dark_oak_log[axis=y]',
  梁: 'minecraft:dark_oak_planks',
  槛墙: 'minecraft:dark_oak_planks',
  栏干: 'minecraft:dark_oak_fence',
  台基: 'minecraft:stone_bricks',
  阶石: 'minecraft:stone_brick_stairs',
  地面砖: 'minecraft:stone_bricks',
  地面板: 'minecraft:stone_brick_slab[type=bottom,waterlogged=false]',
  驳岸: 'minecraft:stone',
  湖石1: 'minecraft:tuff',
  湖石2: 'minecraft:andesite',
  湖石3: 'minecraft:stone',
  湖石4: 'minecraft:cobblestone',
  湖石5: 'minecraft:light_gray_concrete',
  卵石: 'minecraft:cobblestone',
  碎石: 'minecraft:gravel',
  草: 'minecraft:grass_block[snowy=false]',
  土: 'minecraft:dirt',
  黏土: 'minecraft:clay',
  水: 'minecraft:water[level=0]',
  玻璃: 'minecraft:glass_pane',
  荷叶: 'minecraft:lily_pad',
  竹: 'minecraft:bamboo[age=0,leaves=large,stage=0]',
  竹笋: 'minecraft:bamboo[age=0,leaves=none,stage=0]',
  松干: 'minecraft:spruce_log[axis=y]',
  松叶: 'minecraft:spruce_leaves[persistent=true]',
  梅干: 'minecraft:cherry_log[axis=y]',
  梅叶: 'minecraft:cherry_leaves[persistent=true]',
  柳干: 'minecraft:oak_log[axis=y]',
  柳叶: 'minecraft:mangrove_leaves[persistent=true]',
  柳叶2: 'minecraft:oak_leaves[persistent=true]',
  芭蕉: 'minecraft:big_dripleaf[facing=south,tilt=none,waterlogged=false]',
  杜鹃: 'minecraft:flowering_azalea',
  花叶: 'minecraft:flowering_azalea_leaves[persistent=true]',
  灯: 'minecraft:lantern[hanging=false,waterlogged=false]',
  戗尖: 'minecraft:end_rod[facing=up]',
};

/** 作业容器：去重调色板 + 两种操作（单块 / 长方体） + 落格记录（供采样校对） */
export class 作业 {
  constructor() { this.索引 = new Map(); this.palette = []; this.operations = []; this.落格 = new Map(); }
  配(方块) {
    let i = this.索引.get(方块);
    if (i === undefined) { i = this.palette.length; this.palette.push(方块); this.索引.set(方块, i); }
    return i;
  }
  /** 单块 */
  放(x, y, z, 方块) { this.operations.push([x, y, z, this.配(方块)]); this.落格.set(x + ',' + y + ',' + z, 方块); }
  /** 长方体（自动归一化角点） */
  盒(x1, y1, z1, x2, y2, z2, 方块) {
    const ax = Math.min(x1, x2), bx = Math.max(x1, x2), ay = Math.min(y1, y2), by = Math.max(y1, y2), az = Math.min(z1, z2), bz = Math.max(z1, z2);
    this.operations.push([ax, ay, az, bx, by, bz, this.配(方块)]);
    for (let x = ax; x <= bx; x++) for (let y = ay; y <= by; y++) for (let z = az; z <= bz; z++) this.落格.set(x + ',' + y + ',' + z, 方块);
  }
  /** 落盘为执行器 job JSON 的 phases 片段 */
  阶段() { return { palette: this.palette, operations: this.operations }; }
  /**
   * 采样校对（生成期自检）：凡本作业写过的格，samples 期望必须与模型一致（后写覆盖先写）；
   * 未写过的格仅提示（依赖既有世界状态，由执行器回读兜底）。不一致即抛错，阻止带病作业落盘。
   */
  校对(samples) {
    let 坏 = 0, 外部 = 0;
    for (const [x, y, z, 期望] of samples) {
      if (期望 === undefined) continue;
      const 实 = this.落格.get(x + ',' + y + ',' + z);
      if (实 === undefined) { 外部++; console.log(`  外部采样(依赖既有世界) [${x},${y},${z}] ← ${期望}`); }
      else if (实 !== 期望) { 坏++; console.log(`  采样模型不符 [${x},${y},${z}] 期望 ${期望} 模型实置 ${实}`); }
    }
    if (坏) throw new Error(`采样校对失败：${坏} 处与模型不符（修正后再落盘）`);
    console.log(`采样校对通过：${samples.length - 坏 - 外部} 处模型内一致，${外部} 处依赖既有世界`);
  }
}

// ── 基础几何 ─────────────────────────────────────────────

/** 矩形环（厚度 1），用于墙线/檐线 */
export function 环(J, cx, y, cz, hx, hz, 方块) {
  for (let x = cx - hx; x <= cx + hx; x++) { J.放(x, y, cz - hz, 方块); J.放(x, y, cz + hz, 方块); }
  for (let z = cz - hz + 1; z <= cz + hz - 1; z++) { J.放(cx - hx, y, z, 方块); J.放(cx + hx, y, z, 方块); }
}

/** 确定性伪随机（保证可复现） */
export function 随机(seed) {
  let s = seed >>> 0;
  return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
}

// ── 屋面系统（江南屋面：檐口起翘、屋脊收头）──────────────

function 楼梯(方向, mat = M.瓦) { return `${mat}[facing=${方向},half=bottom,shape=straight,waterlogged=false]`; }

/**
 * 屋面一圈：四周朝外楼梯 + 内部顶板。
 * rx/rz 为半宽；角部起翘：最低层（k=0）四角抬高 1 并加戗尖。
 */
/**
 * 屋面一圈：四周朝外楼梯 + 内部顶板。
 * rx/rz 为半宽；角部起翘：最低层四角抬高 1 并加戗脊。
 * 实端x/实端z：歇山收山段把对应端头填实为山面。
 */
function 屋面环(J, cx, y, cz, rx, rz, 起翘, 实端x = false, 实端z = false) {
  const x1 = cx - rx, x2 = cx + rx, z1 = cz - rz, z2 = cz + rz;
  // 内部填顶板（次层即被覆盖）
  if (rx >= 1 && rz >= 1) J.盒(x1 + 1, y, z1 + 1, x2 - 1, y, z2 - 1, M.瓦面);
  for (let x = x1; x <= x2; x++) { J.放(x, y, z1, 楼梯('north')); J.放(x, y, z2, 楼梯('south')); }
  for (let z = z1 + 1; z <= z2 - 1; z++) { J.放(x1, y, z, 楼梯('west')); J.放(x2, y, z, 楼梯('east')); }
  if (实端x) for (let z = z1; z <= z2; z++) { J.放(x1, y, z, M.粉墙); J.放(x2, y, z, M.粉墙); }
  if (实端z) for (let x = x1; x <= x2; x++) { J.放(x, y, z1, M.粉墙); J.放(x, y, z2, M.粉墙); }
  if (起翘) {
    // 发戗：四角檐口抬高一层，并向内一格外伸戗脊
    const 角 = [[x1, z1, 'north'], [x2, z1, 'north'], [x1, z2, 'south'], [x2, z2, 'south']];
    for (const [ax, az, f] of 角) {
      J.放(ax, y + 1, az, 楼梯(f));
      const ix = ax === x1 ? ax + 1 : ax - 1, iz = az === z1 ? az + 1 : az - 1;
      J.放(ix, y + 1, iz, 楼梯(ax === x1 ? 'west' : 'east'));
    }
  }
}

/** 攒尖顶（方亭/多角亭近似）：逐层内收至脊心，收宝顶 */
export function 攒尖顶(J, cx, y, cz, hx, hz) {
  let k = 0;
  while (true) {
    const rx = hx - k, rz = hz - k;
    if (rx < 0 || rz < 0) break;
    屋面环(J, cx, y + k, cz, rx, rz, k <= 1);
    if (rx === 0 || rz === 0) break;
    k++;
  }
  const 顶y = y + Math.max(hx, hz);
  J.放(cx, 顶y, cz, M.脊);
  J.放(cx, 顶y + 1, cz, M.戗尖); // 宝顶
}

/**
 * 歇山顶：庑殿段四面内收至非脊轴半宽 1；其上为通长正脊 + 两端山花三角 + 鸱吻。
 * 屋脊自动沿长轴。脊长 = 2·|hx-hz|+1（符合真实歇山比例）。
 */
export function 歇山顶(J, cx, y, cz, hx, hz) {
  const 沿X = hx >= hz, 脊半 = 1;
  const 长 = 沿X ? hx : hz, 短 = 沿X ? hz : hx;
  const k1 = 短 - 脊半; // 庑殿段末层
  for (let k = 0; k <= k1; k++) {
    const rx = 沿X ? 长 - k : 短 - k;
    const rz = 沿X ? 短 - k : 长 - k;
    屋面环(J, cx, y + k, cz, rx, rz, k <= 1);
  }
  const rx1 = 沿X ? 长 - k1 : 脊半;
  const rz1 = 沿X ? 脊半 : 长 - k1;
  const 脊y = y + k1 + 1;
  // 正脊：通长脊瓦线（在末层台面中线上抬高）
  if (沿X) for (let x = cx - rx1 + 1; x <= cx + rx1 - 1; x++) J.放(x, 脊y, cz, M.脊);
  else for (let z = cz - rz1 + 1; z <= cz + rz1 - 1; z++) J.放(cx, 脊y, z, M.脊);
  // 山花：两端三角粉墙（收进一格），两层收分；端点立鸱吻
  for (const 端 of [-1, 1]) {
    if (沿X) {
      for (let z = cz - 1; z <= cz + 1; z++) J.放(cx + 端 * (rx1 - 1), 脊y, z, M.粉墙);
      J.放(cx + 端 * (rx1 - 2), 脊y + 1, cz, M.粉墙);
      J.放(cx + 端 * rx1, 脊y, cz, M.戗尖);
    } else {
      for (let x = cx - 1; x <= cx + 1; x++) J.放(x, 脊y, cz + 端 * (rz1 - 1), M.粉墙);
      J.放(cx, 脊y + 1, cz + 端 * (rz1 - 2), M.粉墙);
      J.放(cx, 脊y, cz + 端 * rz1, M.戗尖);
    }
  }
}

/** 硬山顶（人字坡，用于走廊/小筑）：仅短轴内收，端头山花填实 */
export function 硬山顶(J, cx, y, cz, hx, hz, 脊沿X = true) {
  let k = 0;
  while (true) {
    const rx = 脊沿X ? hx : hx - k;
    const rz = 脊沿X ? hz - k : hz;
    if (rx < 0 || rz < 0) break;
    if (脊沿X) {
      const x1 = cx - rx, x2 = cx + rx, z1 = cz - rz, z2 = cz + rz;
      if (rx >= 1 && rz >= 1) J.盒(x1 + 1, y + k, z1 + 1, x2 - 1, y + k, z2 - 1, M.瓦面);
      for (let x = x1; x <= x2; x++) { J.放(x, y + k, z1, 楼梯('north')); J.放(x, y + k, z2, 楼梯('south')); }
      // 两端山面
      for (let z = z1; z <= z2; z++) { J.放(x1, y + k, z, M.粉墙); J.放(x2, y + k, z, M.粉墙); }
      if (rz === 0) break;
    } else {
      const x1 = cx - rx, x2 = cx + rx, z1 = cz - rz, z2 = cz + rz;
      if (rx >= 1 && rz >= 1) J.盒(x1 + 1, y + k, z1 + 1, x2 - 1, y + k, z2 - 1, M.瓦面);
      for (let z = z1; z <= z2; z++) { J.放(x1, y + k, z, 楼梯('west')); J.放(x2, y + k, z, 楼梯('east')); }
      for (let x = x1; x <= x2; x++) { J.放(x, y + k, z1, M.粉墙); J.放(x, y + k, z2, M.粉墙); }
      if (rx === 0) break;
    }
    k++;
  }
  const 脊y = y + k - 1;
  if (脊沿X) for (let x = cx - hx; x <= cx + hx; x++) J.放(x, 脊y, cz, M.脊);
  else for (let z = cz - hz; z <= cz + hz; z++) J.放(z === cz ? cx : cx, 脊y, z, M.脊);
}

// ── 立面构件 ─────────────────────────────────────────────

/** 玻璃长窗带（状态烘焙：沿 x 用东西连接，沿 z 用南北连接） */
export function 长窗带(J, x1, y, z1, x2, y2, z2) {
  const 沿X = z1 === z2;
  const b = 沿X ? 'minecraft:glass_pane[east=true,north=false,south=false,waterlogged=false,west=true]'
                : 'minecraft:glass_pane[east=false,north=true,south=true,waterlogged=false,west=false]';
  J.盒(x1, y, z1, x2, y2, z2, b);
}

/** 月洞门：墙线（沿 x 或 z）上开直径 5 圆洞，洞周粉墙照砌 */
export function 月洞门(J, cx, cz, 轴, 底y = 地面) {
  // 圆洞剖面（相对洞心）：逐行半宽
  const 行 = [[-2, 1], [-1, 2], [0, 2], [1, 2], [2, 1]]; // dy, 半宽 → 总高5，底行在 地面
  for (const [dy, hw] of 行) {
    const y = 底y + 2 + dy; // 洞心抬至 地面+2
    for (let d = -hw; d <= hw; d++) {
      if (轴 === 'x') J.放(cx + d, y, cz, 'minecraft:air'); else J.放(cx, y, cz + d, 'minecraft:air');
    }
  }
  // 洞口地面过门石
  if (轴 === 'x') J.盒(cx - 1, 地面 - 1, cz, cx + 1, 地面 - 1, cz, M.地面砖);
  else J.盒(cx, 地面 - 1, cz - 1, cx, 地面 - 1, cz + 1, M.地面砖);
}

/** 漏窗：白粉墙上 3×3 花窗（灰色砖框 + 镂空花纹），轴为墙走向 */
export function 漏窗(J, cx, cz, 轴, 底y = 地面, 式 = 0) {
  const 框 = 'minecraft:tuff';
  const 芯 = [
    [[1,0,1],[0,0,0],[1,0,1]],   // 四隅纹
    [[0,1,0],[1,1,1],[0,1,0]],   // 十字纹
    [[1,1,1],[1,0,1],[1,1,1]],   // 回字纹
  ][式 % 3];
  for (let dy = 0; dy < 3; dy++) for (let d = -1; d <= 1; d++) {
    const 填 = 芯[dy][d + 1] === 1;
    const 方块 = 填 ? 框 : 'minecraft:air';
    const y = 底y + 1 + dy;
    if (轴 === 'x') J.放(cx + d, y, cz, 方块); else J.放(cx, y, cz + d, 方块);
  }
}

/** 直墙段：粉墙身 + 黛瓦压顶（墙帽楼梯朝外两侧） */
export function 墙段(J, x1, z1, x2, z2, 高 = 4, 底y = 地面) {
  const 沿X = z1 === z2;
  J.盒(x1, 底y, z1, x2, 底y + 高 - 1, z2, M.粉墙);
  if (沿X) {
    for (let x = x1; x <= x2; x++) { J.放(x, 底y + 高, z1, M.瓦檐); }
  } else {
    for (let z = z1; z <= z2; z++) { J.放(x1, 底y + 高, z, M.瓦檐); }
  }
}

// ── 植物 ─────────────────────────────────────────────────

/** 竹丛：n 竿，高 4..7 */
export function 竹丛(J, cx, cz, seed, 范围 = 2, 竿数 = 6) {
  const rnd = 随机(seed);
  for (let i = 0; i < 竿数; i++) {
    const x = cx + Math.floor(rnd() * (范围 * 2 + 1)) - 范围;
    const z = cz + Math.floor(rnd() * (范围 * 2 + 1)) - 范围;
    const h = 4 + Math.floor(rnd() * 4);
    for (let y = 地面 + 1; y <= 地面 + h; y++) J.放(x, y, z, M.竹);
  }
}

/** 松：直干 + 分层平展叶盘（江南整形松） */
export function 松(J, cx, cz, 高 = 6) {
  for (let y = 地面 + 1; y <= 地面 + 高; y++) J.放(cx, y, cz, M.松干);
  const 层 = [[高 - 1, 2], [高 - 3, 3], [高 - 5, 2]];
  for (const [dy, r] of 层) {
    const y = 地面 + 高 + dy - 高; // 层位：干顶、干中、干下
    const yy = 地面 + dy;
    for (let dx = -r; dx <= r; dx++) for (let dz = -r; dz <= r; dz++)
      if (Math.abs(dx) + Math.abs(dz) <= r + 1 && !(dx === 0 && dz === 0)) J.放(cx + dx, yy, cz + dz, M.松叶);
  }
  J.放(cx, 地面 + 高 + 1, cz, M.松叶);
}

/** 梅：曲干 + 粉团花叶 */
export function 梅(J, cx, cz, seed = 1) {
  const rnd = 随机(seed);
  let x = cx, z = cz;
  for (let y = 地面 + 1; y <= 地面 + 4; y++) { J.放(x, y, z, M.梅干); if (rnd() < 0.5) x += rnd() < 0.5 ? 1 : -1; else z += rnd() < 0.5 ? 1 : -1; }
  const 顶y = 地面 + 4;
  for (let dx = -2; dx <= 2; dx++) for (let dz = -2; dz <= 2; dz++) for (let dy = 0; dy <= 2; dy++)
    if (Math.abs(dx) + Math.abs(dz) + dy * 0.5 <= 3.4) J.放(x + dx, 顶y + dy, z + dz, M.梅叶);
}

/** 垂柳：干 + 伞盖 + 四周垂叶帘 */
export function 垂柳(J, cx, cz, 高 = 5) {
  for (let y = 地面 + 1; y <= 地面 + 高; y++) J.放(cx, y, cz, M.柳干);
  const 顶 = 地面 + 高;
  for (let dx = -3; dx <= 3; dx++) for (let dz = -3; dz <= 3; dz++) {
    const d = Math.abs(dx) + Math.abs(dz);
    if (d <= 4) J.放(cx + dx, 顶, cz + dz, M.柳叶2);
    if (d >= 2 && d <= 4 && (dx + dz) % 2 === 0) { // 垂条
      J.放(cx + dx, 顶 - 1, cz + dz, M.柳叶);
      if (d >= 3) J.放(cx + dx, 顶 - 2, cz + dz, M.柳叶);
    }
  }
}

/** 芭蕉丛：中心大叶（滴水观音拟芭蕉），两侧杜鹃陪衬 */
export function 芭蕉(J, cx, cz, seed) {
  const rnd = 随机(seed);
  for (let i = 0; i < 5; i++) {
    const x = cx + Math.floor(rnd() * 5) - 2, z = cz + Math.floor(rnd() * 5) - 2;
    J.放(x, 地面 + 1, z, M.杜鹃);
  }
  J.放(cx, 地面 + 1, cz, M.芭蕉);
  J.放(cx + 1, 地面 + 1, cz, M.杜鹃);
  J.放(cx - 1, 地面 + 1, cz, M.杜鹃);
}

/**
 * 连续栏杆带（烘焙围栏连接状态，执行器无副作用，故自行计算）。
 * cells 为 [[x,z],...] 折线；每格按相邻杆格设置 e/w/n/s 连接。
 */
export function 栏杆带(J, cells, y = 地面) {
  const 集 = new Set(cells.map(([x, z]) => x + ',' + z));
  for (const [x, z] of cells) {
    const p = ['east', 'west', 'north', 'south'].map(d => {
      const [dx, dz] = d === 'east' ? [1, 0] : d === 'west' ? [-1, 0] : d === 'north' ? [0, -1] : [0, 1];
      return `${d}=${集.has((x + dx) + ',' + (z + dz))}`;
    }).join(',');
    J.放(x, y, z, `minecraft:dark_oak_fence[${p},waterlogged=false]`);
  }
}

// ── 建筑单体 ─────────────────────────────────────────────

/**
 * 方亭：石台基 + 四柱 + 攒尖顶 + 美人靠。
 * 月洞墙=true 时四面砌粉墙短墙并开圆洞（梧竹幽居式）。
 */
export function 方亭(J, cx, cz, hx, opts = {}) {
  const { 月洞墙 = false, 基y = 地面 } = opts;
  const hz = hx, x1 = cx - hx, x2 = cx + hx, z1 = cz - hz, z2 = cz + hz;
  const 底 = 基y, 墙高 = 月洞墙 ? 3 : 4;
  J.盒(x1 - 1, 底 - 1, z1 - 1, x2 + 1, 底 - 1, z2 + 1, M.台基); // 台基
  // 四角柱
  for (const [px, pz] of [[x1, z1], [x2, z1], [x1, z2], [x2, z2]]) J.盒(px, 底, pz, px, 底 + 墙高 - 1, pz, M.柱);
  if (月洞墙) {
    // 四面粉墙（柱间），每面开满月圆洞：中行全宽、上下行收
    for (let x = x1 + 1; x <= x2 - 1; x++) for (const z of [z1, z2]) for (let y = 底; y < 底 + 墙高; y++) J.放(x, y, z, M.粉墙);
    for (let z = z1 + 1; z <= z2 - 1; z++) for (const x of [x1, x2]) for (let y = 底; y < 底 + 墙高; y++) J.放(x, y, z, M.粉墙);
    // 圆洞：y=底+1 行开 3 宽，y=底+2 行开 1 宽（洞心即各面中点）；底行留 1 宽入口
    for (const d of [-1, 0, 1]) { J.放(cx + d, 底 + 1, z1, 'minecraft:air'); J.放(cx + d, 底 + 1, z2, 'minecraft:air'); }
    J.放(cx, 底 + 2, z1, 'minecraft:air'); J.放(cx, 底 + 2, z2, 'minecraft:air');
    for (const d of [-1, 0, 1]) { J.放(x1, 底 + 1, cz + d, 'minecraft:air'); J.放(x2, 底 + 1, cz + d, 'minecraft:air'); }
    J.放(x1, 底 + 2, cz, 'minecraft:air'); J.放(x2, 底 + 2, cz, 'minecraft:air');
    J.放(cx, 底, z1, 'minecraft:air'); J.放(cx, 底, z2, 'minecraft:air');
    J.放(x1, 底, cz, 'minecraft:air'); J.放(x2, 底, cz, 'minecraft:air');
  } else {
    // 美人靠：四面柱间朝外木凳
    for (let x = x1 + 1; x <= x2 - 1; x++) { J.放(x, 底, z1, 'minecraft:dark_oak_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]'); J.放(x, 底, z2, 'minecraft:dark_oak_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]'); }
    for (let z = z1 + 1; z <= z2 - 1; z++) { J.放(x1, 底, z, 'minecraft:dark_oak_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]'); J.放(x2, 底, z, 'minecraft:dark_oak_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]'); }
  }
  攒尖顶(J, cx, 底 + 墙高, cz, hx + 2, hz + 2);
}
// ── 游廊与桥梁 ───────────────────────────────────────────

/**
 * 游廊（曲廊/回廊）：正交折线，宽 3（ walk 3 格），两侧柱（每 4 格），
 * 人字瓦顶（高 3 收分），转角平台。底面 y63 石板。
 * points: [[x,z],...] 轴对齐折线。
 */
export function 游廊(J, points, opts = {}) {
  const 柱高 = 3, 底 = 地面;
  const 梯 = (f) => `minecraft:deepslate_tile_stairs[facing=${f},half=bottom,shape=straight,waterlogged=false]`;
  const 板 = M.瓦面, 檐 = M.瓦檐;
  // 收集走廊覆盖格（宽3：中心线±1）
  const 覆盖 = new Set();
  const 段 = [];
  for (let i = 0; i < points.length - 1; i++) {
    let [ax, az] = points[i]; const [bx, bz] = points[i + 1];
    const dx = Math.sign(bx - ax), dz = Math.sign(bz - az);
    if (dx !== 0 && dz !== 0) throw new Error('游廊只支持正交折线: ' + JSON.stringify([points[i], points[i + 1]]));
    段.push([ax, az, bx, bz, dx, dz]);
    while (ax !== bx || az !== bz) {
      for (const d of [-1, 0, 1]) 覆盖.add((ax + (dz === 0 ? 0 : d)) + ',' + (az + (dx === 0 ? 0 : d)));
      ax += dx; az += dz;
    }
  }
  for (const d of [-1, 0, 1]) 覆盖.add((points.at(-1)[0] + d) + ',' + points.at(-1)[1]);
  for (const d of [-1, 0, 1]) 覆盖.add((points.at(-1)[0]) + ',' + (points.at(-1)[1] + d));
  // 地面铺装
  for (const k of 覆盖) { const [x, z] = k.split(',').map(Number); J.放(x, 底 - 1, z, M.地面砖); }
  // 柱与顶：逐段
  const 转角 = new Set(points.map(p => p[0] + ',' + p[1]));
  for (const [ax, az, bx, bz, dx, dz] of 段) {
    const 长 = Math.max(Math.abs(bx - ax), Math.abs(bz - az));
    let n = 0;
    for (let i = 0; i <= 长; i++) {
      const x = ax + dx * i, z = az + dz * i;
      // 屋面五格断面：檐-坡-脊-坡-檐
      const 横 = dz === 0 ? [[0, -2], [0, -1], [0, 0], [0, 1], [0, 2]] : [[-2, 0], [-1, 0], [0, 0], [1, 0], [2, 0]];
      for (const [ox, oz] of 横) {
        const t = Math.abs(dz === 0 ? oz : ox); // 距中线 0/1/2
        const y = 底 + 柱高 + (t === 2 ? 0 : t === 1 ? 1 : 2);
        if (t === 0) J.放(x + ox, y, z + oz, 板);
        else if (t === 1) J.放(x + ox, y, z + oz, 梯(dz === 0 ? (oz < 0 ? 'north' : 'south') : (ox < 0 ? 'west' : 'east')));
        else J.放(x + ox, y, z + oz, 檐);
      }
      // 柱：每 4 格于两侧
      if (n % 4 === 0) {
        for (const s of [-1, 1]) {
          const px = x + (dz === 0 ? 0 : s), pz = z + (dx === 0 ? 0 : s);
          if (!转角.has(px + ',' + pz) || true) J.盒(px, 底, pz, px, 底 + 柱高 - 1, pz, M.柱);
        }
      }
      n++;
    }
  }
  // 转角平台（5×5 平瓦，遮转角拼缝）
  for (const [px, pz] of points) J.盒(px - 2, 底 + 柱高 + 1, pz - 2, px + 2, 底 + 柱高 + 1, pz + 2, 板);
}

/** 曲桥（石梁桥）：正交折线，宽 2 平板桥面 y63，两侧低栏每 3 格，水中落石桥墩。 */
export function 曲桥(J, points) {
  const 底 = 地面 - 1; // 63：桥面半高（bottom slab）
  for (let i = 0; i < points.length - 1; i++) {
    let [ax, az] = points[i]; const [bx, bz] = points[i + 1];
    const dx = Math.sign(bx - ax), dz = Math.sign(bz - az);
    if (dx !== 0 && dz !== 0) throw new Error('曲桥只支持正交折线');
    const 长 = Math.max(Math.abs(bx - ax), Math.abs(bz - az));
    for (let s = 0; s <= 长; s++) {
      const x = ax + dx * s, z = az + dz * s;
      // 宽 2：桥身 + 法向一格
      const 格 = dz === 0 ? [[x, z], [x, z + 1]] : [[x, z], [x + 1, z]];
      for (const [gx, gz] of 格) {
        J.放(gx, 底, gz, 'minecraft:stone_slab[type=bottom,waterlogged=false]');
        if (水体(gx, gz)) J.放(gx, 底 - 1, gz, M.驳岸); // 水下桥脚
      }
    }
  }
  // 栏干：沿桥外缘每 3 格立柱
  const 栏集 = [];
  for (let i = 0; i < points.length - 1; i++) {
    let [ax, az] = points[i]; const [bx, bz] = points[i + 1];
    const dx = Math.sign(bx - ax), dz = Math.sign(bz - az);
    const 长 = Math.max(Math.abs(bx - ax), Math.abs(bz - az));
    for (let s = 0; s <= 长; s += 3) {
      const x = ax + dx * s, z = az + dz * s;
      栏集.push(dz === 0 ? [x, z - 1] : [x - 1, z]);
      栏集.push(dz === 0 ? [x, z + 2] : [x + 2, z]);
    }
  }
  栏杆带(J, 栏集, 底 + 1);
}

/**
 * 石拱桥：直线跨，轴='z' 时沿 z 从 a1 到 a2、桥位 x=固；轴='x' 时沿 x、桥位 z=固。
 * 宽 3，矢高可调，栏板随拱起伏，两端外侧踏步。
 */
export function 石拱桥(J, 固, a1, a2, 轴, 宽 = 3, 矢高 = 3) {
  const 底 = 地面 - 1;
  const 长 = a2 - a1;
  for (let s = 0; s <= 长; s++) {
    const t = s / 长, 起 = Math.round(矢高 * Math.sin(Math.PI * t));
    for (let dx = 0; dx < 宽; dx++) {
      const [gx, gz] = 轴 === 'z' ? [固 + dx, a1 + s] : [a1 + s, 固 + dx];
      J.放(gx, 底 + 起, gz, M.台基);
      if (s > 0 && s < 长 && 水体(gx, gz)) for (let y = 底 - 1; y < 底 + 起; y++) J.放(gx, y, gz, M.驳岸); // 水中桥身
    }
    // 栏板（两侧石栏，随拱起伏）
    for (const e of [-1, 宽]) {
      const [gx, gz] = 轴 === 'z' ? [固 + e, a1 + s] : [a1 + s, 固 + e];
      J.放(gx, 底 + 起, gz, 'minecraft:stone_brick_slab[type=bottom,waterlogged=false]');
    }
    // 踏步（两端桥头下一级）
    if (s === 1) for (let dx = 0; dx < 宽; dx++) {
      const [gx, gz, f] = 轴 === 'z' ? [固 + dx, a1 - 1, 'north'] : [a1 - 1, 固 + dx, 'west'];
      J.放(gx, 底, gz, `minecraft:stone_brick_stairs[facing=${f},half=bottom,shape=straight,waterlogged=false]`);
    }
    if (s === 长 - 1) for (let dx = 0; dx < 宽; dx++) {
      const [gx, gz, f] = 轴 === 'z' ? [固 + dx, a2 + 1, 'south'] : [a2 + 1, 固 + dx, 'east'];
      J.放(gx, 底, gz, `minecraft:stone_brick_stairs[facing=${f},half=bottom,shape=straight,waterlogged=false]`);
    }
  }
}

/**
 * 江南厅堂（外部完成，内部留空）。
 * cx/cz 中心；hx/hz 外轮廓半宽（柱网外缘）。
 * opts: 四面=四面厅长窗；门向='south'|'north'|'east'|'west'；墙高；楼=加建二层（楼阁）。
 */
export function 厅堂(J, cx, cz, hx, hz, opts = {}) {
  const { 四面 = false, 门向 = 'south', 墙高 = 4, 楼 = false } = opts;
  const x1 = cx - hx, x2 = cx + hx, z1 = cz - hz, z2 = cz + hz;
  const 底 = 地面; // 64：台基顶面在其下一格 y63
  // 台基（外挑 1 格）+ 地面
  J.盒(x1 - 1, 底 - 1, z1 - 1, x2 + 1, 底 - 1, z2 + 1, M.台基);
  // 柱位：四角 + 边线上每 3 格
  const 柱X = new Set(), 柱Z = new Set();
  for (let x = x1; x <= x2; x += 3) 柱X.add(x); 柱X.add(x2);
  for (let z = z1; z <= z2; z += 3) 柱Z.add(z); 柱Z.add(z2);
  const 是柱 = (x, z) => ((z === z1 || z === z2) && 柱X.has(x)) || ((x === x1 || x === x2) && 柱Z.has(z));
  // 围护：先整圈填充，再覆柱，再开门窗（顺序覆写）
  for (let y = 底; y < 底 + 墙高; y++) {
    for (let x = x1; x <= x2; x++) for (const z of [z1, z2]) {
      J.放(x, y, z, 四面 ? (y === 底 || y === 底 + 墙高 - 1 ? M.梁 : `minecraft:glass_pane[east=true,north=false,south=false,waterlogged=false,west=true]`) : M.粉墙);
    }
    for (let z = z1 + 1; z <= z2 - 1; z++) for (const x of [x1, x2]) {
      J.放(x, y, z, 四面 ? (y === 底 || y === 底 + 墙高 - 1 ? M.梁 : `minecraft:glass_pane[east=false,north=true,south=true,waterlogged=false,west=false]`) : M.粉墙);
    }
  }
  for (let x = x1; x <= x2; x++) for (const z of [z1, z2]) if (是柱(x, z)) J.盒(x, 底, z, x, 底 + 墙高 - 1, z, M.柱);
  for (let z = z1; z <= z2; z++) for (const x of [x1, x2]) if (是柱(x, z)) J.盒(x, 底, z, x, 底 + 墙高 - 1, z, M.柱);
  // 门（2 宽 × 3 高，含过桥下肩）
  const 开门 = (x, z) => { J.盒(x, 底, z, x, 底 + 2, z, 'minecraft:air'); };
  if (门向 === 'south') { 开门(cx, z2); 开门(cx + 1, z2); }
  if (门向 === 'north') { 开门(cx, z1); 开门(cx + 1, z1); }
  if (门向 === 'west') { 开门(x1, cz); 开门(x1, cz + 1); }
  if (门向 === 'east') { 开门(x2, cz); 开门(x2, cz + 1); }
  // 封闭厅堂的方窗：前后檐墙柱间开窗（窗宽=柱间净宽，避免吃掉柱子）
  if (!四面) {
    const xs = [...柱X].sort((a, b) => a - b);
    for (let i = 0; i < xs.length - 1; i++) {
      if (i % 2 === 1) continue; // 隔一开一
      const b1 = xs[i] + 1, b2 = xs[i + 1] - 1; // 柱间净跨
      if (b2 < b1) continue;
      for (const z of [z1, z2]) {
        const 门侧 = (z === z2 && 门向 === 'south') || (z === z1 && 门向 === 'north');
        if (门侧 && !(b2 < cx || b1 > cx + 1)) continue; // 门口所在柱间不开窗
        J.盒(b1, 底 + 1, z, b2, 底 + 2, z, 'minecraft:glass_pane[east=true,north=false,south=false,waterlogged=false,west=true]');
      }
    }
  }
  // 楼阁二层：楼板 + 四面长窗 + 收回一格
  let 顶y = 底 + 墙高;
  if (楼) {
    J.盒(x1, 顶y - 1, z1, x2, 顶y - 1, z2, M.梁); // 二层楼板（用户不要求内饰，仅结构）
    for (let y = 顶y; y < 顶y + 墙高; y++) {
      for (let x = x1; x <= x2; x++) for (const z of [z1, z2]) J.放(x, y, z, y === 顶y || y === 顶y + 墙高 - 1 ? M.梁 : 'minecraft:glass_pane[east=true,north=false,south=false,waterlogged=false,west=true]');
      for (let z = z1 + 1; z <= z2 - 1; z++) for (const x of [x1, x2]) J.放(x, y, z, y === 顶y || y === 顶y + 墙高 - 1 ? M.梁 : 'minecraft:glass_pane[east=false,north=true,south=true,waterlogged=false,west=false]');
    }
    for (let x = x1; x <= x2; x++) for (const z of [z1, z2]) if (是柱(x, z)) J.盒(x, 顶y, z, x, 顶y + 墙高 - 1, z, M.柱);
    for (let z = z1; z <= z2; z++) for (const x of [x1, x2]) if (是柱(x, z)) J.盒(x, 顶y, z, x, 顶y + 墙高 - 1, z, M.柱);
    顶y += 墙高;
  }
  歇山顶(J, cx, 顶y, cz, hx + 2, hz + 2);
}
