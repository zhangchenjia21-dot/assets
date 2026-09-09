/**
 * 全园终验汇总：读取步骤10a~d 四份 result.json，
 * 1) 水面不变量（水只在 y60..62）；2) 动线洪泛连通抽检（16 节点自园门可达）；
 * 3) 全景顶视 PNG（四象限 heightmap 拼接）。
 * 用法：node 检查.mjs <jobDirA> <jobDirB> <jobDirC> <jobDirD> <输出.png>
 */
import fs from 'node:fs';
import zlib from 'node:zlib';

const [, , ...args] = process.argv;
const 出 = args.pop();
const 结果 = args.map(p => JSON.parse(fs.readFileSync(p + '/result.json', 'utf8')));

// ── 拼接体素（四象限有 1 格接缝重叠，后写覆盖）──
const 格 = new Map(); // 'x,y,z' → 名
let 全景 = null;      // heightmap 拼接
for (const r of 结果) {
  const b = r.scan.bounds;
  const W = b.x2 - b.x1 + 1, D = b.z2 - b.z1 + 1, H = b.y2 - b.y1 + 1;
  const grid = new Array(W * D * H);
  for (const [off, len, pi] of r.scan.runs) for (let i = 0; i < len; i++) grid[off + i] = pi;
  for (let y = 0; y < H; y++) for (let z = 0; z < D; z++) for (let x = 0; x < W; x++)
    格.set((b.x1 + x) + ',' + (b.y1 + y) + ',' + (b.z1 + z), r.scan.palette[grid[(y * D + z) * W + x]]);
  for (const rr of [r]) {
    if (!全景) 全景 = { map: new Map() };
    const hm = rr.heightmap, hb = hm.bounds, hw = hb.x2 - hb.x1 + 1;
    for (let z = 0; z <= hb.z2 - hb.z1; z++) for (let x = 0; x < hw; x++)
      全景.map.set((hb.x1 + x) + ',' + (hb.z1 + z), { 名: hm.surface[z * hw + x], y: hm.heights[z * hw + x] });
  }
}
const at = (x, y, z) => 格.get(x + ',' + y + ',' + z) || 'minecraft:air';

// ── 不变量 ──
let 水错层 = 0, 水数 = 0;
for (const [k, 名] of 格) if (名.startsWith('minecraft:water')) {
  水数++;
  const y = +k.split(',')[1];
  if (y < 60 || y > 62) 水错层++;
}
console.log(`不变量：水体 ${水数} 格，越出 y60..62 的 ${水错层} 格 → ${水错层 === 0 ? 'OK' : 'FAIL'}`);

// ── 动线洪泛连通 ──
const 可立 = new Set(['stone_bricks', 'stone', 'andesite', 'tuff', 'cobblestone', 'mossy_cobblestone', 'gravel',
  'grass_block', 'dirt', 'clay', 'white_concrete', 'light_gray_concrete', 'dark_oak_planks', 'polished_andesite',
  'bedrock', 'stone_brick_stairs', 'deepslate_tile_stairs', 'dark_oak_stairs'].map(s => 'minecraft:' + s));
const 是半砖 = n => n.includes('slab') && n.includes('type=bottom');
function 立足(x, z) {
  for (let g = 62; g <= 66; g++) { // 自下而上：隧道/廊下有顶板时取最低可站层
    const b = at(x, g, z);
    const b0 = b.replace(/\[.*\]$/, ''); // 去状态后缀再比对（palette 带 [snowy=false] 等）
    const 实 = 可立.has(b0) || 是半砖(b) || (b.includes('stairs') && b.includes('half=bottom'));
    if (!实) continue;
    if (at(x, g + 1, z) === 'minecraft:air' && at(x, g + 2, z) === 'minecraft:air') return g;
  }
  return null;
}
const 节点 = {
  园门内: [116, 118], 小院: [110, 95], 绿荫轩东: [26, 52], 涵碧堂南: [-16, 68],
  月台: [-20, 49], 岛A: [-44, -6], 北岸步道: [-30, -44], 远翠阁南: [-18, -47],
  五峰前院: [64, -8], 林泉馆北: [67, 19], 冠云庭院: [118, -28], 盆景园: [10, -95],
  石舫甲板: [-89, 16], 山洞内室: [-109, 60], 绿漪亭东: [102, -86], 北部竹林: [-48, -106],
};
const 起g = 立足(116, 118);
const 可达 = new Set();
if (起g !== null) {
  const 队 = [[116, 118, 起g]];
  可达.add('116,118');
  while (队.length) {
    const [x, z, g] = 队.shift();
    for (const [dx, dz] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
      const nx = x + dx, nz = z + dz, k = nx + ',' + nz;
      if (可达.has(k)) continue;
      const ng = 立足(nx, nz);
      if (ng === null || Math.abs(ng - g) > 1) continue;
      可达.add(k); 队.push([nx, nz, ng]);
    }
  }
}
console.log(`洪泛连通：自园门可达 ${可达.size} 格`);
let 全通 = true;
for (const [名, [x, z]] of Object.entries(节点)) {
  const g = 立足(x, z);
  const ok = g !== null && 可达.has(x + ',' + z);
  if (!ok) 全通 = false;
  console.log(`  ${ok ? '✓' : '✗'} ${名} (${x},${z})${g === null ? ' 无立足点' : ''}`);
}
console.log('动线结论：' + (全通 ? '16 节点全部连通 OK' : '存在不可达节点 FAIL'));

// ── 全景顶视渲染 ──
const xs = [...全景.map.keys()].map(k => +k.split(',')[0]);
const zs = [...全景.map.keys()].map(k => +k.split(',')[1]);
const X1 = Math.min(...xs), X2 = Math.max(...xs), Z1 = Math.min(...zs), Z2 = Math.max(...zs);
const W = X2 - X1 + 1, D = Z2 - Z1 + 1;
const 色 = {
  grass_block: [104, 168, 88], dirt: [134, 96, 67], water: [52, 95, 218], clay: [159, 164, 177],
  stone_bricks: [122, 122, 122], stone: [128, 128, 128], andesite: [136, 136, 138], tuff: [108, 108, 104],
  cobblestone: [110, 110, 110], gravel: [131, 127, 126], white_concrete: [207, 213, 214],
  deepslate_tile_stairs: [52, 52, 60], deepslate_tile_slab: [58, 58, 66], dark_oak_log: [60, 41, 18],
  dark_oak_planks: [66, 43, 20], dark_oak_fence: [66, 43, 20], glass_pane: [183, 220, 225],
  bamboo: [93, 153, 50], spruce_leaves: [44, 84, 44], cherry_leaves: [235, 171, 200], oak_leaves: [62, 120, 42],
  mangrove_leaves: [40, 96, 56], lily_pad: [32, 128, 48], big_dripleaf: [80, 140, 60], flowering_azalea: [160, 90, 160],
  flowering_azalea_leaves: [150, 100, 170], spruce_log: [58, 38, 16], cherry_log: [72, 44, 40], oak_log: [104, 82, 50],
  light_gray_concrete: [157, 157, 151], lantern: [240, 180, 80], end_rod: [220, 220, 200], bedrock: [40, 40, 40],
  stone_brick_stairs: [118, 118, 118], stone_brick_slab: [124, 124, 124], azalea: [120, 150, 70],
  polished_andesite: [132, 132, 134], mossy_cobblestone: [100, 120, 90], moss_carpet: [90, 130, 60], fern: [70, 120, 50],
  stone_slab: [126, 126, 126],
};
function 颜色(名) {
  if (!名) return [255, 0, 255];
  let k = 名.replace('minecraft:', '').replace(/\[.*\]/, '');
  if (色[k]) return 色[k];
  let h = 0; for (const c of k) h = (h * 31 + c.charCodeAt(0)) >>> 0;
  return [80 + h % 160, 80 + (h >> 8) % 160, 80 + (h >> 16) % 160];
}
const S = 2;
const img = Buffer.alloc(W * S * D * S * 4);
for (let z = 0; z < D; z++) for (let x = 0; x < W; x++) {
  const 格2 = 全景.map.get((X1 + x) + ',' + (Z1 + z));
  const [r, g, b3] = 颜色(格2 && 格2.名);
  for (let dz = 0; dz < S; dz++) for (let dx = 0; dx < S; dx++) {
    const o = ((z * S + dz) * W * S + (x * S + dx)) * 4; img[o] = r; img[o + 1] = g; img[o + 2] = b3; img[o + 3] = 255;
  }
}
function crc32(buf) {
  let t = crc32.t; if (!t) { t = crc32.t = new Uint32Array(256); for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } }
  let c = 0xFFFFFFFF; for (const byte of buf) c = t[(c ^ byte) & 0xFF] ^ (c >>> 8); return (c ^ 0xFFFFFFFF) >>> 0;
}
function 块(type, data) { const len = Buffer.alloc(4); len.writeUInt32BE(data.length); const td = Buffer.concat([Buffer.from(type), data]); const crc = Buffer.alloc(4); crc.writeUInt32BE(crc32(td)); return Buffer.concat([len, td, crc]); }
const ihdr = Buffer.alloc(13); ihdr.writeUInt32BE(W * S, 0); ihdr.writeUInt32BE(D * S, 4); ihdr[8] = 8; ihdr[9] = 6;
const raw = Buffer.alloc((W * S * 4 + 1) * D * S);
for (let z = 0; z < D * S; z++) { raw[z * (W * S * 4 + 1)] = 0; img.copy(raw, z * (W * S * 4 + 1) + 1, z * W * S * 4, (z + 1) * W * S * 4); }
fs.writeFileSync(出, Buffer.concat([Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]), 块('IHDR', ihdr), 块('IDAT', zlib.deflateSync(raw)), 块('IEND', Buffer.alloc(0))]));
console.log('全景顶视已输出', 出, W + 'x' + D);
