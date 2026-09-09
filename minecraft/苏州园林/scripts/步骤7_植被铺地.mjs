/**
 * 步骤7 植被铺地：荷盖（东半池）、垂柳、松、梅、竹丛、芭蕉、枇杷（杜鹃）、
 * 花街铺地（入口/庭院/枇杷园）、北岸步道、石径、灯笼点缀。
 * 荷盖自动避让桥舫廊道占格。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { 作业, M, 地面, 水面, 随机, 垂柳, 松, 梅, 竹丛, 芭蕉 } from './园林库.mjs';
import { 水体 } from './池形.mjs';

const 根 = path.dirname(fileURLToPath(import.meta.url));
const 世界 = 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/苏州园林';
const J = new 作业();
const rnd = 随机(3321);
const 首 = {}; // 每种首件采样
function 记(k, x, y, z, b) { if (!首[k]) 首[k] = [x, y, z, b]; }

// ── 桥舫占格集合（荷盖避让）──
const 占 = new Set();
function 折线占(points, 宽) {
  for (let i = 0; i < points.length - 1; i++) {
    let [ax, az] = points[i]; const [bx, bz] = points[i + 1];
    const dx = Math.sign(bx - ax), dz = Math.sign(bz - az);
    while (ax !== bx || az !== bz) { for (let d = -1; d <= 宽; d++) 占.add((ax + (dz ? d : 0)) + ',' + (az + (dx ? d : 0))); ax += dx; az += dz; }
  }
}
折线占([[-8, -7], [-8, 6], [-12, 6], [-12, 22]], 1);
折线占([[-40, -10], [-40, -28], [-36, -28], [-36, -44]], 1);
折线占([[-72, -30], [-72, -18]], 1);
for (let x = -75; x <= -62; x++) for (let z = -9; z <= -3; z++) 占.add(x + ',' + z); // 石舫
for (let x = -51; x <= -41; x++) for (let z = 23; z <= 27; z++) 占.add(x + ',' + z); // 石拱桥

// ── 荷盖：东半池（x≥-20），约 12% 水面 ──
let 荷数 = 0;
for (let x = -20; x <= 12; x++) for (let z = -46; z <= 24; z++) {
  if (!水体(x, z) || 占.has(x + ',' + z)) continue;
  if (((x * 31 + z * 17) >>> 0) % 100 < 12) { J.放(x, 水面 + 1, z, M.荷叶); 记('荷', x, 水面 + 1, z, M.荷叶); 荷数++; }
}

// ── 树木 ──
const 柳位 = [[8, -38], [14, -14], [-22, 26], [2, 26], [-34, -48], [-58, -38], [-64, 26]];
for (const [x, z] of 柳位) { 垂柳(J, x, z); 记('柳', x, 地面 + 1, z, M.柳干); }
const 松位 = [[-34, -64], [-6, -64], [66, 48], [-94, 20]];
for (const [x, z] of 松位) { 松(J, x, z); 记('松', x, 地面 + 1, z, M.松干); }
const 梅位 = [[-12, -18], [-4, -10], [-43, -1], [-37, -7], [-86, 4]];
for (const [x, z] of 梅位) 梅(J, x, z, x * 100 + z);
const 竹位 = [[16, -16], [24, -4], [14, -4], [24, 58], [70, -60], [76, -52], [60, -70], [78, -66], [64, -64], [88, -60], [80, -70], [76, 64]];
for (const [x, z] of 竹位) 竹丛(J, x, z, x * 7 + z, 2, 6);
J.放(16, 地面 + 1, -16, M.竹); 记('竹', 16, 地面 + 1, -16, M.竹); // 中心定竿
const 芭位 = [[20, 55], [17, 59], [40, 70], [-32, -50]];
for (const [x, z] of 芭位) { 芭蕉(J, x, z, x + z); 记('芭蕉', x, 地面 + 1, z, M.芭蕉); }

// ── 枇杷园果树（开花杜鹃 + 小乔木感）──
const 杷位 = [[44, 64], [52, 70], [64, 58], [48, 76], [68, 70], [38, 46], [58, 44], [36, 74]];
for (const [x, z] of 杷位) { J.放(x, 地面 + 1, z, M.杜鹃); 记('枇杷', x, 地面 + 1, z, M.杜鹃); }

// ── 花街铺地（卵石碎砖纹）──
function 花街(J, x1, z1, x2, z2) {
  for (let x = x1; x <= x2; x++) for (let z = z1; z <= z2; z++) {
    const 边 = x === x1 || x === x2 || z === z1 || z === z2;
    let b;
    if (边) b = M.地面砖;
    else { const t = ((x * 5 + z * 9) >>> 0) % 10; b = t < 4 ? M.卵石 : t < 7 ? 'minecraft:andesite' : t < 9 ? 'minecraft:light_gray_concrete' : M.碎石; }
    J.放(x, 地面 - 1, z, b);
  }
}
花街(J, 81, 78, 95, 82);   // 入口庭院
花街(J, 12, 48, 26, 62);   // 听雨轩全院
花街(J, 44, 60, 62, 74);   // 枇杷园中庭
// 北岸步道（远香堂前）
for (let x = -36; x <= -6; x++) { J.放(x, 地面 - 1, -46, M.地面砖); J.放(x, 地面 - 1, -45, M.地面砖); }
// 枇杷园内石径：月洞门(32,58)→玲珑馆(46,54)
for (let x = 33; x <= 45; x++) { J.放(x, 地面 - 1, 58, M.地面砖); }
for (let z = 55; z <= 58; z++) { J.放(45, 地面 - 1, z, M.地面砖); }
// 西园石径：月洞门(-76,8)→鸳鸯馆
for (const [x, z] of [[-75, 8], [-77, 8], [-78, 9], [-80, 10], [-82, 12], [-84, 14], [-86, 18], [-87, 22], [-88, 26], [-89, 30], [-89, 32]]) J.放(x, 地面 - 1, z, M.地面砖);
// 南岸主径：小沧浪—曲桥A南头（z=23，避让小沧浪台基与石拱桥栏板）
for (let x = -50; x <= -14; x++) { J.放(x, 地面 - 1, 23, M.地面砖); }

// ── 灯笼点缀（亭心、门口、桥头）──
const 灯位 = [[-8, -14], [-40, -4], [20, -10], [84, -64], [-52, 26], [-58 + 0, 50 + 0], // 各亭（笠亭在峰顶单独处理）
  [86, 83], [90, 83], [-20, -55], [-89, 34], [50, 55]];
for (const [x, z] of 灯位) { J.放(x, 地面, z, M.灯); 记('灯', x, 地面, z, M.灯); }
J.放(-58, 地面 + 15, 50, M.灯); // 笠亭内

const samples = Object.values(首);
samples.push([-58, 地面 + 15, 50, 'minecraft:lantern[hanging=false,waterlogged=false]']);
const job = {
  world_path: 世界,
  phases: [J.阶段()],
  samples,
  scan: { x1: -100, x2: 100, z1: -84, z2: 84, y1: 62, y2: 76 },
};
fs.writeFileSync(path.join(根, '..', '施工', '步骤7.json'), JSON.stringify(job));
console.log('步骤7 ops=', J.operations.length, 'palette=', J.palette.length, '荷数=', 荷数, 'samples=', samples.length);
