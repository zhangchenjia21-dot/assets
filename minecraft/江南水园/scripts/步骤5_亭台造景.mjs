/**
 * 步骤5 亭台造景：一镜亭/沧浪亭/笠亭（攒尖方亭）、北岸湖石小假山、峰石、
 * 垂柳/松/梅/竹/芭蕉、池中荷盖（避让桥舫廊道）、入口花街铺地、石桌凳、灯笼。
 * 所有植栽落位于草地，避让桥、廊、路、建筑，保证通行不受阻。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { 作业, M, 地面, 水面, 随机, 方亭, 垂柳, 松, 梅, 竹丛, 芭蕉, 栏杆带 } from './园林库.mjs';
import { 水体 } from './池形.mjs';

const 根 = path.dirname(fileURLToPath(import.meta.url));
const 世界 = 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/江南水园';
const J = new 作业();
const 首 = {};
const 记 = (k, x, y, z, b) => { if (!首[k]) 首[k] = [x, y, z, b]; };

// ── 三亭 ──
方亭(J, 26, -4, 2);   // 一镜亭（东岛）
方亭(J, -28, -6, 2);  // 沧浪亭（西岛）
方亭(J, 4, 12, 1);    // 笠亭（南岛，避让曲桥栏杆线 x=2）

// ── 北岸湖石小假山（三峰）──
const 石材 = [M.湖石1, M.湖石2, M.湖石3, M.湖石4, M.湖石5];
const 选石 = (x, y, z) => 石材[((x * 7 + z * 3 + y * 5) >>> 0) % 石材.length];
{
  const 峰 = [[-14, -38, 4, 3], [-17, -36, 3, 2], [-11, -36, 3, 2]];
  for (let x = -20; x <= -8; x++) for (let z = -40; z <= -33; z++) {
    const e = ((x + 14) / 7) ** 2 + ((z + 37) / 4) ** 2;
    if (e > 1) continue;
    let h = 0;
    for (const [px, pz, ph, sig] of 峰) h = Math.max(h, ph * Math.exp(-(((x - px) ** 2 + (z - pz) ** 2) / (2 * sig * sig))));
    h *= Math.max(0, 1.1 - e);
    const hi = Math.max(0, Math.round(h));
    for (let y = 地面; y < 地面 + hi; y++) {
      if (y >= 地面 + hi - 2 && ((x * 31 + z * 17 + y * 13) >>> 0) % 100 < 14) continue; // 孔窍
      J.放(x, y, z, 选石(x, y, z));
    }
  }
}

// ── 池中荷盖（避让桥、廊、石舫占格）──
const 占 = new Set();
function 折线占(points, 半宽) {
  for (let i = 0; i < points.length - 1; i++) {
    let [ax, az] = points[i]; const [bx, bz] = points[i + 1];
    const dx = Math.sign(bx - ax), dz = Math.sign(bz - az);
    for (;;) {
      for (let d = -半宽; d <= 半宽; d++) 占.add((ax + (dz ? d : 0)) + ',' + (az + (dx ? d : 0)));
      if (ax === bx && az === bz) break;
      ax += dx; az += dz;
    }
  }
}
折线占([[0, 30], [0, 1]], 2);            // 曲桥A（含栏杆线）
折线占([[50, 4], [33, 4], [33, -2], [8, -2]], 2); // 曲桥B
折线占([[-25, -6], [-9, -6]], 2);        // 曲桥西
折线占([[0, -34], [0, -13]], 2);         // 小飞虹廊桥
for (let x = -50; x <= -42; x++) for (let z = -15; z <= -7; z++) 占.add(x + ',' + z); // 石舫
for (let x = -54; x <= -30; x++) for (let z = -7; z <= -3; z++) 占.add(x + ',' + z);  // 西屿石拱桥
for (let z = -6; z <= 2; z++) for (let x = -55; x <= -51; x++) 占.add(x + ',' + z);   // 连通渠桥
for (const z of [-30, 2, 32, 50]) for (let x = -60; x <= -52; x++) for (let d = 0; d <= 2; d++) 占.add(x + ',' + (z + d)); // 水巷桥
let 荷 = 0;
for (let x = -60; x <= 50; x++) for (let z = -56; z <= 58; z++) {
  if (!水体(x, z) || 占.has(x + ',' + z)) continue;
  if (((x * 37 + z * 61) >>> 0) % 100 < 9) { J.放(x, 水面 + 1, z, M.荷叶); 记('荷', x, 水面 + 1, z, M.荷叶); 荷++; }
}

// ── 植物（草地落位）──
const 柳位 = [[-24, 26], [14, 26], [-38, 16], [40, -14], [0, -38]];
for (const [x, z] of 柳位) { 垂柳(J, x, z); 记('柳', x, 地面 + 1, z, M.柳干); }
const 松位 = [[-30, -30], [30, -24], [44, -30]];
for (const [x, z] of 松位) { 松(J, x, z); 记('松', x, 地面 + 1, z, M.松干); }
const 梅位 = [[8, -36], [-8, -36], [24, 28], [-24, 30]];
for (const [x, z] of 梅位) 梅(J, x, z, x * 13 + z);
const 竹位 = [[48, -40], [52, 20], [-44, 30], [30, 30], [20, -34]];
for (const [x, z] of 竹位) 竹丛(J, x, z, x * 7 + z, 2, 6);
J.放(48, 地面 + 1, -40, M.竹); 记('竹', 48, 地面 + 1, -40, M.竹);
const 芭位 = [[16, 46], [-16, 46]];
for (const [x, z] of 芭位) { 芭蕉(J, x, z, x + z); 记('芭蕉', x, 地面 + 1, z, M.芭蕉); }

// ── 入口与花厅前花街铺地 ──
function 花街(J, x1, z1, x2, z2) {
  for (let x = x1; x <= x2; x++) for (let z = z1; z <= z2; z++) {
    if (水体(x, z)) continue;
    const 边 = x === x1 || x === x2 || z === z1 || z === z2;
    const t = ((x * 5 + z * 9) >>> 0) % 10;
    const b = 边 ? M.地面砖 : (t < 4 ? M.卵石 : t < 7 ? 'minecraft:andesite' : t < 9 ? 'minecraft:light_gray_concrete' : M.碎石);
    J.放(x, 地面 - 1, z, b);
  }
}
花街(J, -8, 59, 8, 62);   // 入口庭院（影壁—南门之间）
花街(J, -7, 55, 7, 57);   // 花厅前庭
花街(J, 12, 46, 20, 50);  // 花厅东侧小庭

// ── 石桌凳 ──
const 桌凳 = [[6, 0], [8, 50], [10, 52]];
for (const [x, z] of 桌凳) {
  J.放(x, 地面, z, 'minecraft:polished_andesite');
  for (const [dx, dz] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) J.放(x + dx, 地面, z + dz, 'minecraft:stone_brick_slab[type=bottom,waterlogged=false]');
}
记('桌', 6, 地面, 0, 'minecraft:polished_andesite');

// ── 灯笼 ──
for (const [x, z] of [[26, -4], [-28, -6], [4, 12], [16, -33], [-48, -12], [0, 61]]) { J.放(x, 地面, z, M.灯); 记('灯', x, 地面, z, M.灯); }

const samples = Object.values(首);
samples.push(
  [24, 地面, -6, 'minecraft:dark_oak_log[axis=y]'],  // 一镜亭角柱
  [24, 地面 - 1, -6, 'minecraft:stone_bricks'],      // 一镜亭台基
  [4, 地面 - 1, 12, 'minecraft:stone_bricks'],       // 笠亭台基
  [-14, 地面 + 1, -38, 选石(-14, 地面 + 1, -38)],    // 北岸假山
  [-8, 地面 - 1, 60, 'minecraft:stone_bricks'],      // 入口花街收边
  [8, 地面, 50, 'minecraft:polished_andesite'],      // 石桌
);
const job = {
  world_path: 世界,
  phases: [J.阶段()],
  samples,
  scan: { x1: -64, x2: 64, z1: -64, z2: 64, y1: 62, y2: 78 },
};
fs.writeFileSync(path.join(根, '..', '施工', '步骤5.json'), JSON.stringify(job));
console.log('步骤5 ops=', J.operations.length, 'palette=', J.palette.length, '荷=', 荷, 'samples=', samples.length);
