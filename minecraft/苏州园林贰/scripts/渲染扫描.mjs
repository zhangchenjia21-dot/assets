/**
 * 扫描检查与顶视渲染：读取 run-job 的 result.json（含 scan/heightmap），
 * 输出：1) 控制台统计与不变量检查；2) 顶视 PNG（按表面方块着色）。
 * 用法：node 渲染扫描.mjs <result.json> <输出.png> [--json]
 */
import fs from 'node:fs';
import zlib from 'node:zlib';

const [, , resultPath, pngPath, ...flags] = process.argv;
const result = JSON.parse(fs.readFileSync(resultPath, 'utf8'));
if (!result.scan) throw new Error('result 无 scan');
const b = result.scan.bounds;
const [x1, x2, z1, z2, y1, y2] = [b.x1, b.x2, b.z1, b.z2, b.y1, b.y2];
const W = x2 - x1 + 1, D = z2 - z1 + 1, H = y2 - y1 + 1;

// ── 解码 RLE（循环顺序：y 外层 → z → x 最快）──
const grid = new Array(W * D * H);
const palette = result.scan.palette;
for (const [off, len, pi] of result.scan.runs) for (let i = 0; i < len; i++) grid[off + i] = pi;
const at = (x, y, z) => grid[((y - y1) * D + (z - z1)) * W + (x - x1)];

// ── 统计 ──
const counts = new Map();
let nonAir = 0;
for (const pi of grid) { const n = palette[pi]; counts.set(n, (counts.get(n) || 0) + 1); if (!n.includes('air')) nonAir++; }
const 简 = new Map();
for (const [n, c] of counts) { const k = n.replace('minecraft:', '').replace(/\[.*\]/, ''); 简.set(k, (简.get(k) || 0) + c); }
console.log('体积', W * D * H, '非空气', nonAir);
console.log([...简.entries()].sort((a, c) => c[1] - a[1]).map(([k, v]) => `${k}:${v}`).join(' '));

// ── 顶视渲染（heightmap 表面方块着色）──
const hm = result.heightmap; // 与 scan 同级
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
};
function 颜色(名) {
  if (!名) return [255, 0, 255];
  let k = 名.replace('minecraft:', '').replace(/\[.*\]/, '');
  if (色[k]) return 色[k];
  let h = 0; for (const c of k) h = (h * 31 + c.charCodeAt(0)) >>> 0;
  return [80 + h % 160, 80 + (h >> 8) % 160, 80 + (h >> 16) % 160];
}
const S = 2; // 放大倍数，便于目视
const img = Buffer.alloc(W * S * D * S * 4);
for (let z = 0; z < D; z++) for (let x = 0; x < W; x++) {
  const i = z * W + x; const 名 = hm.surface[i]; const [r, g, b3] = 颜色(名);
  for (let dz = 0; dz < S; dz++) for (let dx = 0; dx < S; dx++) {
    const o = ((z * S + dz) * W * S + (x * S + dx)) * 4; img[o] = r; img[o + 1] = g; img[o + 2] = b3; img[o + 3] = 255;
  }
}
// PNG 编码（8bit RGBA，无隔行）
function crc32(buf) {
  let t = crc32.t; if (!t) { t = crc32.t = new Uint32Array(256); for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } }
  let c = 0xFFFFFFFF; for (const byte of buf) c = t[(c ^ byte) & 0xFF] ^ (c >>> 8); return (c ^ 0xFFFFFFFF) >>> 0;
}
function 块(type, data) { const len = Buffer.alloc(4); len.writeUInt32BE(data.length); const td = Buffer.concat([Buffer.from(type), data]); const crc = Buffer.alloc(4); crc.writeUInt32BE(crc32(td)); return Buffer.concat([len, td, crc]); }
const ihdr = Buffer.alloc(13); ihdr.writeUInt32BE(W * S, 0); ihdr.writeUInt32BE(D * S, 4); ihdr[8] = 8; ihdr[9] = 6;
const raw = Buffer.alloc((W * S * 4 + 1) * D * S);
for (let z = 0; z < D * S; z++) { raw[z * (W * S * 4 + 1)] = 0; img.copy(raw, z * (W * S * 4 + 1) + 1, z * W * S * 4, (z + 1) * W * S * 4); }
const png = Buffer.concat([Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]), 块('IHDR', ihdr), 块('IDAT', zlib.deflateSync(raw)), 块('IEND', Buffer.alloc(0))]);
if (pngPath) fs.writeFileSync(pngPath, png);

// ── 顶层摘要（供自检脚本复用）──
if (flags.includes('--json')) console.log(JSON.stringify({ nonAir, counts: Object.fromEntries(简) }));
