// 离线 3D 体素渲染器：从存档 RLE 扫描或蓝图 Builder 生成多机位透视图。
// 用途：在无客户端截图工具时提供最好的替代三维证据，并用于施工前的几何自检。
// 渲染方式：正交/透视投影 + 简单朗伯光照 + 最近面 z-buffer，输出 PNG。
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';

// ---------- 方块基色表（近似 Minecraft 材质主色，用于体素示意） ----------
const COLORS = {
  'minecraft:air': null,
  'minecraft:cinnabar_bricks': [136, 62, 52],
  'minecraft:cinnabar_brick_stairs': [129, 58, 49],
  'minecraft:cinnabar_brick_slab': [140, 66, 55],
  'minecraft:cinnabar_brick_wall': [133, 60, 50],
  'minecraft:cinnabar_slab': [143, 74, 62],
  'minecraft:cinnabar_stairs': [132, 66, 56],
  'minecraft:cinnabar_wall': [136, 70, 58],
  'minecraft:polished_deepslate': [72, 72, 74],
  'minecraft:polished_deepslate_stairs': [70, 70, 72],
  'minecraft:polished_deepslate_slab': [74, 74, 76],
  'minecraft:polished_deepslate_wall': [70, 70, 72],
  'minecraft:deepslate_bricks': [78, 78, 80],
  'minecraft:deepslate_brick_stairs': [76, 76, 78],
  'minecraft:deepslate_brick_slab': [80, 80, 82],
  'minecraft:deepslate_brick_wall': [76, 76, 78],
  'minecraft:deepslate_tiles': [66, 66, 68],
  'minecraft:deepslate_tile_stairs': [64, 64, 66],
  'minecraft:deepslate_tile_slab': [68, 68, 70],
  'minecraft:deepslate_tile_wall': [64, 64, 66],
  'minecraft:cobbled_deepslate': [80, 80, 82],
  'minecraft:cobbled_deepslate_stairs': [78, 78, 80],
  'minecraft:cobbled_deepslate_slab': [82, 82, 84],
  'minecraft:cobbled_deepslate_wall': [78, 78, 80],
  'minecraft:chiseled_deepslate': [70, 70, 72],
  'minecraft:cracked_deepslate_bricks': [74, 72, 70],
  'minecraft:cracked_deepslate_tiles': [68, 67, 66],
  'minecraft:diorite': [207, 207, 208],
  'minecraft:polished_diorite': [192, 192, 194],
  'minecraft:polished_diorite_stairs': [190, 190, 192],
  'minecraft:polished_diorite_slab': [194, 194, 196],
  'minecraft:diorite_wall': [200, 200, 202],
  'minecraft:calcite': [224, 224, 220],
  'minecraft:quartz_block': [235, 229, 220],
  'minecraft:smooth_quartz': [238, 233, 226],
  'minecraft:chiseled_quartz_block': [236, 231, 223],
  'minecraft:smooth_quartz_stairs': [236, 231, 224],
  'minecraft:smooth_quartz_slab': [237, 232, 225],
  'minecraft:quartz_slab': [240, 236, 230],
  'minecraft:quartz_stairs': [238, 234, 228],
  'minecraft:polished_tuff': [104, 108, 102],
  'minecraft:polished_tuff_stairs': [102, 106, 100],
  'minecraft:polished_tuff_slab': [106, 110, 104],
  'minecraft:polished_tuff_wall': [102, 106, 100],
  'minecraft:tuff_bricks': [96, 100, 94],
  'minecraft:tuff_brick_stairs': [94, 98, 92],
  'minecraft:tuff_brick_wall': [94, 98, 92],
  'minecraft:tuff': [108, 112, 104],
  'minecraft:stone': [125, 125, 125],
  'minecraft:stone_bricks': [122, 122, 122],
  'minecraft:stone_stairs': [120, 120, 120],
  'minecraft:stone_slab': [126, 126, 126],
  'minecraft:stone_brick_stairs': [120, 120, 120],
  'minecraft:stone_brick_slab': [126, 126, 126],
  'minecraft:smooth_stone': [158, 158, 158],
  'minecraft:smooth_stone_slab': [160, 160, 160],
  'minecraft:chiseled_stone_bricks': [118, 118, 118],
  'minecraft:cracked_stone_bricks': [116, 114, 112],
  'minecraft:mossy_stone_bricks': [110, 122, 100],
  'minecraft:andesite': [132, 134, 133],
  'minecraft:polished_andesite': [132, 135, 134],
  'minecraft:gravel': [131, 127, 126],
  'minecraft:bricks': [150, 97, 83],
  'minecraft:brick_stairs': [146, 94, 80],
  'minecraft:brick_slab': [153, 100, 86],
  'minecraft:brick_wall': [148, 96, 82],
  'minecraft:mud_bricks': [137, 107, 90],
  'minecraft:mud_brick_stairs': [133, 104, 87],
  'minecraft:mud_brick_slab': [140, 110, 92],
  'minecraft:mud_brick_wall': [135, 106, 88],
  'minecraft:resin_bricks': [196, 120, 48],
  'minecraft:sulfur_bricks': [206, 200, 128],
  'minecraft:red_nether_bricks': [86, 34, 36],
  'minecraft:nether_bricks': [44, 22, 26],
  'minecraft:polished_blackstone_bricks': [52, 48, 54],
  'minecraft:blackstone': [42, 36, 42],
  'minecraft:dark_oak_planks': [66, 43, 20],
  'minecraft:dark_oak_log': [60, 46, 26],
  'minecraft:dark_oak_wood': [56, 40, 22],
  'minecraft:stripped_dark_oak_log': [76, 56, 32],
  'minecraft:dark_oak_stairs': [64, 42, 20],
  'minecraft:dark_oak_slab': [68, 45, 22],
  'minecraft:dark_oak_fence': [62, 41, 19],
  'minecraft:dark_oak_fence_gate': [62, 41, 19],
  'minecraft:oak_planks': [162, 130, 78],
  'minecraft:oak_stairs': [158, 126, 75],
  'minecraft:oak_slab': [164, 132, 80],
  'minecraft:oak_fence': [156, 124, 74],
  'minecraft:oak_fence_gate': [156, 124, 74],
  'minecraft:oak_log': [104, 82, 48],
  'minecraft:spruce_planks': [114, 84, 48],
  'minecraft:spruce_stairs': [111, 82, 47],
  'minecraft:spruce_slab': [116, 86, 50],
  'minecraft:spruce_fence': [110, 81, 46],
  'minecraft:stripped_spruce_log': [116, 90, 52],
  'minecraft:mangrove_planks': [117, 54, 49],
  'minecraft:glass': [200, 226, 240],
  'minecraft:white_stained_glass_pane': [235, 240, 244],
  'minecraft:gray_stained_glass_pane': [90, 94, 98],
  'minecraft:glass_pane': [200, 226, 240],
  'minecraft:iron_bars': [130, 130, 134],
  'minecraft:iron_chain': [110, 110, 116],
  'minecraft:iron_block': [220, 220, 220],
  'minecraft:iron_trapdoor': [200, 200, 202],
  'minecraft:oak_door': [150, 118, 70],
  'minecraft:spruce_door': [110, 82, 48],
  'minecraft:dark_oak_door': [64, 42, 20],
  'minecraft:iron_door': [190, 190, 192],
  'minecraft:oak_trapdoor': [156, 124, 74],
  'minecraft:spruce_trapdoor': [112, 84, 48],
  'minecraft:dark_oak_trapdoor': [64, 42, 20],
  'minecraft:lantern': [250, 210, 120],
  'minecraft:soul_lantern': [120, 200, 210],
  'minecraft:torch': [250, 210, 120],
  'minecraft:wall_torch': [250, 210, 120],
  'minecraft:campfire': [180, 120, 60],
  'minecraft:candle': [240, 235, 220],
  'minecraft:white_candle': [240, 235, 220],
  'minecraft:barrel': [120, 88, 48],
  'minecraft:chest': [126, 92, 50],
  'minecraft:trapped_chest': [126, 92, 50],
  'minecraft:lectern': [140, 104, 58],
  'minecraft:bell': [212, 168, 74],
  'minecraft:furnace': [110, 110, 110],
  'minecraft:blast_furnace': [100, 100, 102],
  'minecraft:smoker': [104, 104, 104],
  'minecraft:cauldron': [70, 70, 72],
  'minecraft:smithing_table': [60, 58, 66],
  'minecraft:stonecutter': [120, 120, 120],
  'minecraft:grindstone': [110, 110, 112],
  'minecraft:loom': [140, 116, 78],
  'minecraft:cartography_table': [110, 86, 52],
  'minecraft:anvil': [64, 64, 66],
  'minecraft:bookshelf': [160, 128, 76],
  'minecraft:hay_block': [166, 142, 42],
  'minecraft:scaffolding': [168, 138, 78],
  'minecraft:ladder': [150, 118, 70],
  'minecraft:moss_block': [88, 110, 62],
  'minecraft:moss_carpet': [92, 114, 66],
  'minecraft:dirt': [134, 96, 67],
  'minecraft:coarse_dirt': [122, 88, 62],
  'minecraft:dirt_path': [148, 118, 74],
  'minecraft:clay': [160, 164, 174],
  'minecraft:sand': [219, 207, 163],
  'minecraft:red_sand': [190, 102, 33],
  'minecraft:short_grass': [110, 140, 70],
  'minecraft:fern': [96, 128, 64],
  'minecraft:tall_grass': [104, 136, 68],
  'minecraft:large_fern': [92, 124, 60],
  'minecraft:oak_leaves': [70, 112, 44],
  'minecraft:spruce_leaves': [52, 88, 52],
  'minecraft:dark_oak_leaves': [58, 96, 42],
  'minecraft:white_wool': [234, 236, 237],
  'minecraft:brown_wool': [114, 71, 40],
  'minecraft:red_wool': [160, 39, 34],
  'minecraft:gray_wool': [62, 68, 71],
  'minecraft:red_carpet': [160, 39, 34],
  'minecraft:white_carpet': [234, 236, 237],
  'minecraft:brown_carpet': [114, 71, 40],
  'minecraft:flower_pot': [150, 100, 78],
  'minecraft:potted_fern': [96, 128, 64],
  'minecraft:potted_oak_sapling': [110, 140, 70],
  'minecraft:vine': [60, 100, 48],
  'minecraft:spruce_wall_sign': [110, 82, 48],
  'minecraft:oak_wall_sign': [150, 118, 70],
  'minecraft:red_wall_banner': [160, 39, 34],
  'minecraft:spruce_wall_hanging_sign': [110, 82, 48],
  'minecraft:grass_block': [110, 150, 76],
  'minecraft:bedrock': [40, 40, 40],
};

function baseColor(state) {
  const name = state.slice(0, state.indexOf('[') < 0 ? undefined : state.indexOf('['));
  return COLORS[name] || [128, 128, 128];
}

// ---------- 扫描（RLE）解码 ----------
export function decodeScan(scan) {
  const b = scan.bounds;
  const nx = b.x2 - b.x1 + 1, ny = b.y2 - b.y1 + 1, nz = b.z2 - b.z1 + 1;
  const grid = new Array(nx * ny * nz);
  let pos = 0;
  for (const [offset, len, pi] of scan.runs) {
    for (let k = 0; k < len; k++) grid[offset + k] = scan.palette[pi];
    pos += len;
  }
  return { grid, nx, ny, nz, bounds: b };
}

export function fromBuilder(builder) {
  let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity, minZ = Infinity, maxZ = -Infinity;
  for (const k of builder.cells.keys()) {
    const [x, y, z] = k.split(',').map(Number);
    minX = Math.min(minX, x); maxX = Math.max(maxX, x);
    minY = Math.min(minY, y); maxY = Math.max(maxY, y);
    minZ = Math.min(minZ, z); maxZ = Math.max(maxZ, z);
  }
  const nx = maxX - minX + 1, ny = maxY - minY + 1, nz = maxZ - minZ + 1;
  const grid = new Array(nx * ny * nz).fill('minecraft:air');
  for (const [k, st] of builder.cells) {
    const [x, y, z] = k.split(',').map(Number);
    grid[(y - minY) * nz * nx + (z - minZ) * nx + (x - minX)] = st;
  }
  return { grid, nx, ny, nz, bounds: { x1: minX, y1: minY, z1: minZ, x2: maxX, y2: maxY, z2: maxZ } };
}

// ---------- 渲染 ----------
/**
 * 相机：eye 与 target 为世界坐标；相机朝 target 看。
 * 渲染到 z-buffer，背景为天空渐变。
 */
export function render(vol, { eye, target, width = 900, height = 620, fov = 62, up = [0, 1, 0], background = [150, 180, 210], fog = null }) {
  const { grid, nx, ny, nz, bounds } = vol;
  const img = new Uint8Array(width * height * 3);
  const zbuf = new Float32Array(width * height).fill(Infinity);
  for (let i = 0; i < width * height; i++) {
    img[i * 3] = background[0]; img[i * 3 + 1] = background[1]; img[i * 3 + 2] = background[2];
  }
  const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
  const norm = (v) => { const l = Math.hypot(...v) || 1; return [v[0] / l, v[1] / l, v[2] / l]; };
  const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
  const fwd = norm(sub(target, eye));
  const right = norm(cross(fwd, up));
  const trueUp = cross(right, fwd);
  const aspect = width / height;
  const tanF = Math.tan((fov * Math.PI) / 360);
  const LIGHT = norm([-0.45, 0.82, -0.35]);

  // 逐方块前向投影：对方块 6 个面做投影光栅化（只画朝向相机的面）
  for (let i = 0; i < grid.length; i++) {
    const st = grid[i];
    if (!st || st === 'minecraft:air') continue;
    const y = Math.floor(i / (nz * nx));
    const rem = i % (nz * nx);
    const z = Math.floor(rem / nx);
    const x = rem % nx;
    const wx = bounds.x1 + x, wy = bounds.y1 + y, wz = bounds.z1 + z;
    const base = baseColor(st);
    // 方块形状近似：半砖半球高；楼梯按 facing 近似为半高台阶（上半砖/下半砖），
    // 使竖向交通在透视图里可读（否则楼梯会被画成整块立方体而看不出踏步）。
    const isSlab = st.includes('_slab') || st.includes('carpet') || st.includes('dirt_path');
    const isStair = st.includes('_stairs');
    let top = 1, bot = 0;
    if (isSlab) {
      top = st.includes('type=top') ? 1 : 0.5;
      bot = st.includes('type=top') ? 0.5 : 0;
    } else if (isStair) {
      const upper = st.includes('half=top');
      top = 1;
      bot = upper ? 0.5 : 0;
    }
    // 6 个面（用 8 顶点 + 面索引）
    const P = [
      [wx, wy + bot, wz], [wx + 1, wy + bot, wz], [wx + 1, wy + bot, wz + 1], [wx, wy + bot, wz + 1],
      [wx, wy + top, wz], [wx + 1, wy + top, wz], [wx + 1, wy + top, wz + 1], [wx, wy + top, wz + 1],
    ];
    const faces = [
      [0, 1, 2, 3, [0, -1, 0]],
      [4, 7, 6, 5, [0, 1, 0]],
      [0, 4, 5, 1, [0, 0, -1]],
      [2, 6, 7, 3, [0, 0, 1]],
      [1, 5, 6, 2, [1, 0, 0]],
      [3, 7, 4, 0, [-1, 0, 0]],
    ];
    for (const [a, b2, c, d, nrm] of faces) {
      const toEye = norm(sub(eye, P[a]));
      if (dot(nrm, toEye) <= 0.001) continue;
      const lam = Math.max(0.28, dot(nrm, LIGHT)) + 0.12;
      const shade = Math.min(1.25, lam);
      const col = [Math.min(255, base[0] * shade) | 0, Math.min(255, base[1] * shade) | 0, Math.min(255, base[2] * shade) | 0];
      // 把四个顶点投影到屏幕
      const sp = [P[a], P[b2], P[c], P[d]].map((v) => {
        const rel = sub(v, eye);
        const cx = dot(rel, right), cy = dot(rel, trueUp), cz = dot(rel, fwd);
        if (cz <= 0.05) return null;
        return [(cx / (cz * tanF * aspect)) * (width / 2) + width / 2, height / 2 - (cy / (cz * tanF)) * (height / 2), cz];
      });
      if (sp.some((s) => s === null)) continue;
      rasterTri(img, zbuf, width, height, sp[0], sp[1], sp[2], col, fog, eye, P);
      rasterTri(img, zbuf, width, height, sp[0], sp[2], sp[3], col, fog, eye, P);
    }
  }
  return { width, height, img };
}

function rasterTri(img, zbuf, W, H, p0, p1, p2, col, fog, eye, P) {
  const minX = Math.max(0, Math.floor(Math.min(p0[0], p1[0], p2[0])));
  const maxX = Math.min(W - 1, Math.ceil(Math.max(p0[0], p1[0], p2[0])));
  const minY = Math.max(0, Math.floor(Math.min(p0[1], p1[1], p2[1])));
  const maxY = Math.min(H - 1, Math.ceil(Math.max(p0[1], p1[1], p2[1])));
  const area = (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1]);
  if (Math.abs(area) < 1e-9) return;
  for (let y = minY; y <= maxY; y++) {
    for (let x = minX; x <= maxX; x++) {
      const w0 = ((p1[0] - x) * (p2[1] - y) - (p2[0] - x) * (p1[1] - y)) / area;
      const w1 = ((p2[0] - x) * (p0[1] - y) - (p0[0] - x) * (p2[1] - y)) / area;
      const w2 = 1 - w0 - w1;
      if (w0 < -0.001 || w1 < -0.001 || w2 < -0.001) continue;
      const z = w0 * p0[2] + w1 * p1[2] + w2 * p2[2];
      const idx = y * W + x;
      if (z >= zbuf[idx]) continue;
      zbuf[idx] = z;
      let c = col;
      if (fog) {
        const t = Math.min(1, Math.max(0, (z - fog.near) / (fog.far - fog.near)));
        const k = t * t * (3 - 2 * t) * (fog.strength ?? 1);
        c = [col[0] + (fog.color[0] - col[0]) * k, col[1] + (fog.color[1] - col[1]) * k, col[2] + (fog.color[2] - col[2]) * k];
      }
      img[idx * 3] = c[0]; img[idx * 3 + 1] = c[1]; img[idx * 3 + 2] = c[2];
    }
  }
}

// ---------- PNG 输出 ----------
export function writePNG(file, { width, height, img }) {
  const raw = Buffer.alloc((width * 3 + 1) * height);
  for (let y = 0; y < height; y++) {
    raw[y * (width * 3 + 1)] = 0;
    Buffer.from(img.buffer, y * width * 3, width * 3).copy(raw, y * (width * 3 + 1) + 1);
  }
  const idat = zlib.deflateSync(raw, { level: 9 });
  const chunks = [];
  const sig = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);
  const chunk = (type, data) => {
    const len = Buffer.alloc(4); len.writeUInt32BE(data.length);
    const t = Buffer.from(type, 'ascii');
    const crcBuf = Buffer.concat([t, data]);
    const crc = Buffer.alloc(4); crc.writeUInt32BE(crc32(crcBuf) >>> 0);
    return Buffer.concat([len, t, data, crc]);
  };
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(width, 0); ihdr.writeUInt32BE(height, 4);
  ihdr[8] = 8; ihdr[9] = 2; ihdr[10] = 0; ihdr[11] = 0; ihdr[12] = 0;
  chunks.push(sig, chunk('IHDR', ihdr), chunk('IDAT', idat), chunk('IEND', Buffer.alloc(0)));
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, Buffer.concat(chunks));
  return file;
}

let CRC_TABLE = null;
function crc32(buf) {
  if (!CRC_TABLE) {
    CRC_TABLE = new Int32Array(256);
    for (let n = 0; n < 256; n++) {
      let c = n;
      for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
      CRC_TABLE[n] = c;
    }
  }
  let c = 0xffffffff;
  for (let i = 0; i < buf.length; i++) c = CRC_TABLE[(c ^ buf[i]) & 0xff] ^ (c >>> 8);
  return c ^ 0xffffffff;
}

// ---------- 平面/剖面 ASCII 图 ----------
export function sliceY(vol, y, { x1, x2, z1, z2 } = {}) {
  const { grid, nx, nz, bounds } = vol;
  const ax1 = x1 ?? bounds.x1, ax2 = x2 ?? bounds.x2, az1 = z1 ?? bounds.z1, az2 = z2 ?? bounds.z2;
  const lines = [];
  for (let x = ax2; x >= ax1; x--) {       // 北在上
    let line = String(x).padStart(4) + ' ';
    for (let z = az1; z <= az2; z++) {
      const ix = x - bounds.x1, iy = y - bounds.y1, iz = z - bounds.z1;
      if (ix < 0 || iy < 0 || iz < 0 || ix >= nx || iy >= vol.ny || iz >= nz) { line += ' '; continue; }
      const st = grid[iy * nz * nx + iz * nx + ix] || 'minecraft:air';
      line += glyph(st);
    }
    lines.push(line);
  }
  lines.push('     ' + 'z→'.padEnd(2) + Array.from({ length: az2 - az1 + 1 }, (_, i) => (az1 + i) % 10).join(''));
  return lines.join('\n');
}

export function sliceZ(vol, z, { x1, x2, y1, y2 } = {}) {
  const { grid, nx, ny, nz, bounds } = vol;
  const ax1 = x1 ?? bounds.x1, ax2 = x2 ?? bounds.x2, ay1 = y1 ?? bounds.y1, ay2 = y2 ?? bounds.y2;
  const lines = [];
  for (let y = ay2; y >= ay1; y--) {
    let line = String(y).padStart(4) + ' ';
    for (let x = ax1; x <= ax2; x++) {
      const ix = x - bounds.x1, iy = y - bounds.y1, iz = z - bounds.z1;
      if (ix < 0 || iy < 0 || iz < 0 || ix >= nx || iy >= ny || iz >= nz) { line += ' '; continue; }
      const st = grid[iy * nz * nx + iz * nx + ix] || 'minecraft:air';
      line += glyph(st);
    }
    lines.push(line);
  }
  lines.push('     ' + Array.from({ length: ax2 - ax1 + 1 }, (_, i) => (ax1 + i) % 10).join(''));
  return lines.join('\n');
}

export function sliceX(vol, x, { z1, z2, y1, y2 } = {}) {
  const { grid, nx, ny, nz, bounds } = vol;
  const az1 = z1 ?? bounds.z1, az2 = z2 ?? bounds.z2, ay1 = y1 ?? bounds.y1, ay2 = y2 ?? bounds.y2;
  const lines = [];
  for (let y = ay2; y >= ay1; y--) {
    let line = String(y).padStart(4) + ' ';
    for (let z = az1; z <= az2; z++) {
      const ix = x - bounds.x1, iy = y - bounds.y1, iz = z - bounds.z1;
      if (ix < 0 || iy < 0 || iz < 0 || ix >= nx || iy >= vol.ny || iz >= nz) { line += ' '; continue; }
      const st = grid[iy * nz * nx + iz * nx + ix] || 'minecraft:air';
      line += glyph(st);
    }
    lines.push(line);
  }
  lines.push('     ' + Array.from({ length: az2 - az1 + 1 }, (_, i) => (az1 + i) % 10).join(''));
  return lines.join('\n');
}

const GLYPHS = [
  [/^minecraft:air$/, ' '],
  [/cinnabar|resin|bricks|brick_/, '#'],
  [/deepslate|blackstone|cobbled/, 'D'],
  [/diorite|calcite|quartz|polished_tuff|tuff/, 'S'],
  [/dark_oak|oak|spruce|mangrove|log|wood/, 'W'],
  [/glass|pane|bars/, 'g'],
  [/lantern|torch|candle|campfire/, '*'],
  [/barrel|chest|lectern|crate/, 'b'],
  [/door|trapdoor|fence|gate|sign|banner|chain|ladder/, 'd'],
  [/leaves|grass|fern|moss|vine|flower|hay|wool|carpet/, 'v'],
  [/stone|andesite|gravel|smooth/, 's'],
  [/torch|candle/, '*'],
];
function glyph(st) {
  if (st === 'minecraft:air') return ' ';
  const name = st.slice(0, st.indexOf('[') < 0 ? undefined : st.indexOf('['));
  for (const [re, g] of GLYPHS) if (re.test(name)) return g;
  return '?';
}
