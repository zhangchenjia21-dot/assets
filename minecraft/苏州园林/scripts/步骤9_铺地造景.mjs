/**
 * 步骤9 全园铺地与造景加密（整改：消灭秃草坪）。
 * 七大铺装区（花街/石板/卵石三纹样，树穴留草）、全池岸石矶、
 * 剩余草地地被点染、补植与石桌凳四组。
 * 严格避让建筑台基、墙体、廊道、桥舫、假山、水面与既有树位。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { 作业, M, 地面, 水面, 随机, 垂柳, 竹丛, 梅, 芭蕉 } from './园林库.mjs';
import { 水体, 岸线 } from './池形.mjs';

const 根 = path.dirname(fileURLToPath(import.meta.url));
const 世界 = 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/苏州园林';
const J = new 作业();
const 首 = {};
const 记 = (k, x, y, z, b) => { if (!首[k]) 首[k] = [x, y, z, b]; };

// ── 排除格集合 ──
const 排除 = new Set();
const 矩排 = (x1, z1, x2, z2) => { for (let x = x1; x <= x2; x++) for (let z = z1; z <= z2; z++) 排除.add(x + ',' + z); };
const 圆排 = (cx, cz, r) => { for (let x = cx - r; x <= cx + r; x++) for (let z = cz - r; z <= cz + r; z++) if ((x - cx) ** 2 + (z - cz) ** 2 <= r * r) 排除.add(x + ',' + z); };
const 椭排 = (cx, cz, rx, rz) => { for (let x = cx - rx; x <= cx + rx; x++) for (let z = cz - rz; z <= cz + rz; z++) if (((x - cx) / rx) ** 2 + ((z - cz) / rz) ** 2 <= 1.15) 排除.add(x + ',' + z); };
const 折线排 = (points, 半宽) => {
  for (let i = 0; i < points.length - 1; i++) {
    let [ax, az] = points[i]; const [bx, bz] = points[i + 1];
    const dx = Math.sign(bx - ax), dz = Math.sign(bz - az);
    for (;;) {
      for (let d = -半宽; d <= 半宽; d++) 排除.add((ax + (dz ? d : 0)) + ',' + (az + (dx ? d : 0)));
      if (ax === bx && az === bz) break;
      ax += dx; az += dz;
    }
  }
};
// 建筑台基与屋檐
矩排(-34, -70, -6, -54); 矩排(-29, -54, -11, -46);        // 远香堂+月台
矩排(-97, 21, -81, 35);                                    // 卅六鸳鸯馆
矩排(-70, -46, -58, -34);                                  // 见山楼
矩排(55, -46, 69, -34);                                    // 秫香馆
矩排(44, 49, 56, 59);                                      // 玲珑馆
矩排(-95, -14, -85, -6);                                   // 留听阁
矩排(15, -15, 25, -5);                                     // 梧竹幽居
矩排(-12, -18, -4, -10); 矩排(-44, -8, -36, 0);            // 双岛亭
矩排(80, -68, 88, -60); 矩排(-55, 23, -49, 29);            // 绿漪亭、小沧浪亭
矩排(84, 81, 92, 87); 矩排(79, 75, 97, 77);                // 门楼、影壁
矩排(-76, -9, -61, -3);                                    // 香洲石舫
矩排(-48, 16, -44, 29); 矩排(-52, 22, -40, 28);            // 水院渠、石拱桥区
// 墙体
矩排(-101, -85, -99, 85); 矩排(99, -85, 101, 85);
矩排(-101, -85, 101, -83); 矩排(-101, 83, 101, 85);
矩排(-77, -85, -75, 41);                                   // 西园隔墙
矩排(31, 39, 33, 79); 矩排(71, 39, 73, 79); 矩排(31, 39, 73, 41); 矩排(31, 77, 73, 79); // 枇杷园墙
矩排(9, 45, 11, 65); 矩排(27, 45, 29, 65); 矩排(9, 45, 29, 47); 矩排(9, 63, 29, 65);   // 听雨轩墙
// 廊道桥舫
折线排([[78, 80], [36, 80], [36, 58], [34, 58]], 1);
折线排([[-48, 30], [-20, 30], [0, 30], [8, 30], [8, 44]], 1);
折线排([[-80, 20], [-80, -28], [-78, -28]], 1);
折线排([[-72, -30], [-72, -18]], 1);
折线排([[-44, 33], [-52, 33], [-52, 40]], 1);
折线排([[-8, -7], [-8, 6], [-12, 6], [-12, 22]], 1);
折线排([[-40, -10], [-40, -28], [-36, -28], [-36, -44]], 1);
// 假山、障景石、水院
椭排(-54, 50, 17, 14); 椭排(84, 69, 7, 5); 椭排(-46, 32, 7, 6);
// 既有树位（留树穴）
const 树穴 = [
  [8, -38], [14, -14], [-22, 26], [2, 26], [-34, -48], [-58, -38], [-64, 26],   // 柳
  [-34, -64], [-6, -64], [66, 48], [-94, 20],                                  // 松
  [-12, -18], [-4, -10], [-43, -1], [-37, -7], [-86, 4],                       // 梅
  [16, -16], [24, -4], [14, -4], [24, 58], [70, -60], [76, -52], [60, -70], [78, -66], [64, -64], [88, -60], [80, -70], [76, 64], // 竹
  [20, 55], [17, 59], [40, 70], [-32, -50],                                    // 芭蕉
  [44, 64], [52, 70], [64, 58], [48, 76], [68, 70], [38, 46], [58, 44], [36, 74], // 枇杷
  [60, 66], [54, 72], [15, 53], [-27, -74], [-13, -72], [-4, -19], [-45, -7],  // 峰石
];
for (const [x, z] of 树穴) 圆排(x, z, 2);
// 新增植栽位（也先留穴，后栽植）
const 新柳 = [[-2, -46], [-46, -52], [-68, 8], [10, 4], [-72, -6]];
const 新竹 = [[30, -20], [28, 8]];
const 新梅 = [[40, 50], [64, 44]];
const 新芭 = [[-22, -72], [-90, -24]];
for (const [x, z] of [...新柳, ...新竹, ...新梅, ...新芭]) 圆排(x, z, 2);
// 石桌凳位
const 桌凳 = [[50, 66], [18, 54], [-20, -50], [-88, 10]];
for (const [x, z] of 桌凳) 圆排(x, z, 2);

// ── 铺装纹样 ──
const 花街 = (x, z, 边) => {
  if (边) return M.地面砖;
  const t = ((x * 5 + z * 9) >>> 0) % 10;
  return t < 4 ? M.卵石 : t < 7 ? 'minecraft:andesite' : t < 9 ? 'minecraft:light_gray_concrete' : M.碎石;
};
const 石板 = (x, z, 边) => {
  if (边) return 'minecraft:polished_andesite';
  const t = ((x * 7 + z * 5) >>> 0) % 10;
  return t < 7 ? M.地面砖 : t < 9 ? 'minecraft:polished_andesite' : 'minecraft:mossy_cobblestone';
};
const 卵石 = (x, z, 边) => {
  if (边) return M.地面砖;
  const t = ((x * 3 + z * 11) >>> 0) % 10;
  return t < 5 ? M.卵石 : t < 8 ? 'minecraft:andesite' : M.碎石;
};
const 区 = [
  [-40, -52, -2, -42, 花街, '北岸庭院'],
  [-48, 26, 8, 36, 石板, '南岸带'],
  [2, -36, 26, 10, 卵石, '东岸园'],
  [-96, 2, -80, 36, 花街, '西园庭院'],
  [34, 42, 70, 76, 花街, '枇杷园'],
  [74, 58, 98, 82, 石板, '入口区'],
  [-54, 24, -38, 38, 卵石, '水院边'],
];
let 铺数 = 0;
for (const [x1, z1, x2, z2, 纹, 名] of 区) {
  for (let x = x1; x <= x2; x++) for (let z = z1; z <= z2; z++) {
    const k = x + ',' + z;
    if (排除.has(k) || 水体(x, z) || 岸线(x, z)) continue;
    const 边 = x === x1 || x === x2 || z === z1 || z === z2;
    const b = 纹(x, z, 边);
    J.放(x, 地面 - 1, z, b);
    记('铺' + 名, x, 地面 - 1, z, b);
    排除.add(k); // 铺过的格子不再做地被
    铺数++;
  }
}

// ── 全池岸石矶（湖石矶头，部分起挑石）──
let 矶数 = 0;
const 矶石 = [M.湖石1, M.湖石2, M.湖石3, M.驳岸, 'minecraft:mossy_cobblestone'];
for (let x = -78; x <= 14; x++) for (let z = -50; z <= 32; z++) {
  const k = x + ',' + z;
  if (!岸线(x, z) || 排除.has(k)) continue;
  const h = ((x * 13 + z * 29) >>> 0) % 100;
  if (h < 25) {
    J.放(x, 地面 - 1, z, 矶石[h % 矶石.length]);
    记('石矶', x, 地面 - 1, z, 矶石[h % 矶石.length]);
    矶数++;
    if (h < 8) { J.放(x, 地面, z, 矶石[(h + 2) % 矶石.length]); } // 挑石
  }
}

// ── 剩余草地地被点染 ──
let 被数 = 0;
for (let x = -98; x <= 98; x++) for (let z = -82; z <= 82; z++) {
  const k = x + ',' + z;
  if (排除.has(k) || 水体(x, z) || 岸线(x, z)) continue;
  const h = ((x * 41 + z * 97) >>> 0) % 100;
  let b = null;
  if (h < 8) b = 'minecraft:moss_carpet';
  else if (h < 11) b = 'minecraft:azalea';
  else if (h < 14) b = 'minecraft:fern';
  if (b) { J.放(x, 地面, z, b); 记('地被', x, 地面, z, b); 被数++; }
}

// ── 补植 ──
for (const [x, z] of 新柳) 垂柳(J, x, z);
for (const [x, z] of 新竹) 竹丛(J, x, z, x * 5 + z, 2, 6);
for (const [x, z] of 新梅) 梅(J, x, z, x * 101 + z);
for (const [x, z] of 新芭) 芭蕉(J, x, z, x * 3 + z);
J.放(10, 地面 + 1, 4, M.柳干); // 定本采样

// ── 石桌凳四组 ──
for (const [x, z] of 桌凳) {
  J.放(x, 地面, z, 'minecraft:polished_andesite'); // 石桌
  for (const [dx, dz] of [[1, 0], [-1, 0], [0, 1], [0, -1]])
    J.放(x + dx, 地面, z + dz, 'minecraft:stone_brick_slab[type=bottom,waterlogged=false]'); // 石凳
}

const samples = Object.values(首);
samples.push(
  [10, 地面 + 1, 4, 'minecraft:oak_log[axis=y]'],
  [-20, 地面, -50, 'minecraft:polished_andesite'],
  [-19, 地面, -50, 'minecraft:stone_brick_slab[type=bottom,waterlogged=false]'],
);
const job = {
  world_path: 世界,
  phases: [J.阶段()],
  samples,
  scan: { x1: -100, x2: 100, z1: -84, z2: 84, y1: 62, y2: 76 },
};
fs.writeFileSync(path.join(根, '..', '施工', '步骤9.json'), JSON.stringify(job));
console.log('步骤9 ops=', J.operations.length, 'palette=', J.palette.length, '铺数=', 铺数, '矶数=', 矶数, '被数=', 被数, 'samples=', samples.length);
