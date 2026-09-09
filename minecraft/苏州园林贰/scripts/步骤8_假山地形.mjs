/**
 * 步骤8 假山与地形补塑：
 *   西南湖石大假山（多峰高斯、孔窍、山洞+内室、盘降蹬道、峰顶卧云亭，主峰 y82）；
 *   冠云峰立峰（高10，瘦透秀立，冠云庭院中心）；
 *   地形补塑（西北余脉两阜、东北疏林三处微起伏，参数见 地势.mjs 丘2）；
 *   庭院峰石若干（五峰仙馆前院、林泉馆后、涵碧堂后、小院、揖峰轩侧、池面岛礁）。
 * 同作业另落 施工/步骤8验.json：东半区只读扫描（samples+scan），供自检东半施工面。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { 作业, M, 地面, 方亭, 游廊, 随机 } from './园林库.mjs';
import { 丘2, 丘高 } from './地势.mjs';

const 根 = path.dirname(fileURLToPath(import.meta.url));
const 世界 = 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/苏州园林贰';
const J = new 作业();
const 石材 = [M.湖石1, M.湖石2, M.湖石3, M.湖石4, M.湖石5];
const 选石 = (x, y, z) => 石材[((x * 7 + z * 3 + y * 5) >>> 0) % 石材.length];

/** 湖石假山：多峰高斯叠加 + 边缘收分 + 抖动；表层随机孔窍（太湖石瘦皱漏透） */
function 湖石假山(J, cx, cz, rx, rz, 峰表) {
  const H = new Map();
  for (let x = cx - rx; x <= cx + rx; x++) for (let z = cz - rz; z <= cz + rz; z++) {
    const e = ((x - cx) / rx) ** 2 + ((z - cz) / rz) ** 2;
    if (e > 1) continue;
    let h = 0;
    for (const [px, pz, ph, sig] of 峰表)
      h = Math.max(h, ph * Math.exp(-(((x - px) ** 2 + (z - pz) ** 2) / (2 * sig * sig))));
    h *= Math.max(0, 1.1 - e);
    h += (((x * 7349 + z * 15161) >>> 0) % 100) / 100 * 1.2 - 0.6;
    const hi = Math.max(0, Math.round(h));
    if (hi >= 1) H.set(x + ',' + z, hi);
  }
  for (const [k, hi] of H) {
    const [x, z] = k.split(',').map(Number);
    for (let y = 地面; y < 地面 + hi; y++) {
      const 表层 = y >= 地面 + hi - 2;
      const 窍 = ((x * 31 + z * 17 + y * 13) >>> 0) % 100;
      if (表层 && 窍 < 12 && hi > 2) continue;
      J.放(x, y, z, 选石(x, y, z));
    }
  }
  return H;
}

/** 独立峰石：基座 3×3，瘦柱盘旋而上，多孔旁枝 */
function 峰石(J, x, z, h, seed, 卧水 = false) {
  const rnd = 随机(seed);
  if (卧水) J.盒(x - 1, 59, z - 1, x + 1, 地面 - 1, z + 1, M.驳岸); // 岛礁水下基座
  J.盒(x - 1, 地面, z - 1, x + 1, 地面, z + 1, 选石(x, 地面, z));
  let ox = 0, oz = 0;
  for (let y = 地面 + 1; y < 地面 + h; y++) {
    if (rnd() < 0.4) ox += rnd() < 0.5 ? 1 : -1; else oz += rnd() < 0.5 ? 1 : -1;
    ox = Math.max(-1, Math.min(1, ox)); oz = Math.max(-1, Math.min(1, oz));
    if (rnd() < 0.15) continue;
    J.放(x + ox, y, z + oz, 选石(x, y, z));
    if (rnd() < 0.5) J.放(x - oz, y, z + ox, 选石(x + 1, y, z));
  }
  J.放(x + ox, 地面 + h, z + oz, M.湖石5);
}

/** 立峰（冠云峰）：底两层 3×3 实心，中段盘旋渐收，上部 2×2，顶 1×1 秀尖；总高 h */
function 立峰(J, x, z, h, seed) {
  const rnd = 随机(seed);
  J.盒(x - 2, 地面 - 1, z - 2, x + 2, 地面 - 1, z + 2, 选石(x, 地面 - 1, z)); // 座 5×5
  J.盒(x - 1, 地面, z - 1, x + 1, 地面 + 1, z + 1, 选石(x, 地面, z));         // 底两层实心 3×3
  let ox = 0, oz = 0;
  for (let y = 地面 + 2; y < 地面 + h - 3; y++) {                              // 中段 3×3 透孔盘旋
    if (rnd() < 0.35) ox += rnd() < 0.5 ? 1 : -1; else oz += rnd() < 0.5 ? 1 : -1;
    ox = Math.max(-1, Math.min(1, ox)); oz = Math.max(-1, Math.min(1, oz));
    for (let dx = -1; dx <= 1; dx++) for (let dz = -1; dz <= 1; dz++) {
      if (dx && dz && rnd() < 0.5) continue;            // 收角
      if (rnd() < 0.12) continue;                       // 透
      J.放(x + ox + dx, y, z + oz + dz, 选石(x + dx, y, z + dz));
    }
  }
  const 顶基 = 地面 + h - 3;
  for (let dy = 0; dy < 2; dy++) for (let dx = 0; dx <= 1; dx++) for (let dz = 0; dz <= 1; dz++)
    J.放(x + ox + dx, 顶基 + dy, z + oz + dz, 选石(x + dx, 顶基 + dy, z + dz)); // 上段 2×2
  J.放(x + ox, 顶基 + 2, z + oz, M.湖石5);                                      // 秀尖
  J.放(x + ox, 顶基 + 3, z + oz, M.湖石5);
}

// ── 地形补塑：丘2 两阜三起伏（草顶土心）──
for (const [cx, cz, rx, rz] of 丘2) {
  for (let x = cx - rx; x <= cx + rx; x++) for (let z = cz - rz; z <= cz + rz; z++) {
    const h = 丘高(x, z, 丘2);
    if (h <= 0) continue;
    J.放(x, 63 + h, z, 'minecraft:grass_block[snowy=false]');
    if (h > 1) J.盒(x, 64, z, x, 63 + h - 1, z, M.土);
  }
}

// ── 西南大假山：c(-116,70) r20×24，主峰 18（y82）──
const 峰 = [[-118, 68, 18, 7], [-108, 78, 13, 6], [-126, 62, 11, 6], [-104, 58, 9, 5], [-122, 80, 10, 5], [-112, 52, 8, 4]];
const H = 湖石假山(J, -116, 70, 20, 24, 峰);

// 峰顶平台（卧云亭基）：7×7 填实至 y81，压平上空，亭基 y82
for (let x = -121; x <= -115; x++) for (let z = 65; z <= 71; z++) {
  for (let y = 地面; y <= 81; y++) J.放(x, y, z, 选石(x, y, z));
  for (let y = 82; y <= 86; y++) J.放(x, y, z, 'minecraft:air');
}
方亭(J, -118, 68, 2, { 基y: 82 }); // 卧云亭

// 山洞：北入口隧道（x=-109, z50..59）+ 内室（c(-109,60) r2，高3）
for (let z = 50; z <= 59; z++) { J.放(-109, 地面, z, 'minecraft:air'); J.放(-109, 地面 + 1, z, 'minecraft:air'); }
for (let dx = -2; dx <= 2; dx++) for (let dz = -2; dz <= 2; dz++) for (let y = 地面; y <= 地面 + 2; y++)
  if (dx * dx + dz * dz <= 5) J.放(-109 + dx, y, 60 + dz, 'minecraft:air');

// 蹬道：自峰顶平台旁盘降，逐格找次高邻格铺石阶
{
  const 访 = new Set(['-118,68']);
  let cur = [-117, 69];
  for (let step = 0; step < 90; step++) {
    const h = H.get(cur[0] + ',' + cur[1]);
    if (h === undefined || h <= 1) break;
    const 邻 = [];
    for (let dx = -1; dx <= 1; dx++) for (let dz = -1; dz <= 1; dz++) {
      if (!dx && !dz) continue;
      const nx = cur[0] + dx, nz = cur[1] + dz, nh = H.get(nx + ',' + nz);
      if (nh !== undefined && nh < h && !访.has(nx + ',' + nz)) 邻.push([nx, nz, nh, dx, dz]);
    }
    if (!邻.length) break;
    邻.sort((a, b) => b[2] - a[2]);
    const 缓降 = 邻.filter(n => n[2] === h - 1);
    const [nx, nz, nh, dx, dz] = (缓降.length ? 缓降 : 邻)[0];
    const f = dz === 1 ? 'north' : dz === -1 ? 'south' : dx === 1 ? 'west' : 'east';
    J.放(nx, 地面 + nh - 1, nz, `minecraft:stone_brick_stairs[facing=${f},half=bottom,shape=straight,waterlogged=false]`);
    访.add(nx + ',' + nz); cur = [nx, nz];
  }
}

// ── 冠云峰立峰（冠云庭院中心，总高 10 → 峰顶 y76）──
立峰(J, 118, -32, 10, 5188);

// ── 庭院峰石与岛礁 ──
峰石(J, 64, -14, 5, 21); 峰石(J, 64, -2, 4, 22);   // 五峰仙馆前院
峰石(J, 72, 36, 4, 23);                              // 林泉馆后
峰石(J, -16, 69, 4, 24);                             // 涵碧堂后
峰石(J, 110, 92, 4, 25);                             // 古木交柯小院
峰石(J, 100, -4, 4, 26);                             // 揖峰轩侧
峰石(J, 4, -78, 3, 27);                              // 又一村入口
峰石(J, -52, -18, 3, 28, true);                      // 池面岛礁（西）
峰石(J, -14, 10, 2, 29, true);                       // 池面岛礁（东）

// ── 通往山洞的短廊（南岸步道 → 洞口）──
游廊(J, [[-109, 44], [-109, 49]]);

// ── 自检采样（选石公式确定性复算）──
const samples = [
  [-108, 地面 + 2, 78, 选石(-108, 地面 + 2, 78)],    // 次峰岩体内部
  [-118, 81, 68, 'minecraft:stone_bricks'],          // 峰顶平台（卧云亭台基）
  [-120, 82, 66, 'minecraft:dark_oak_log[axis=y]'],  // 卧云亭角柱
  [-109, 地面, 60, 'minecraft:air'],                 // 山洞内室
  [118, 地面 + 1, -32, 选石(118, 地面, -32)],        // 冠云峰实心基段（盒体单色）
  [118, 地面 + 9, -32, 'minecraft:air'],             // 立峰旁侧透空（收角外必空）——校对以模型为准
  [-108, 67, -64, 'minecraft:grass_block[snowy=false]'], // 余脉主阜顶
  [120, 65, -90, 'minecraft:grass_block[snowy=false]'],  // 东北微起伏
  [64, 地面, -14, 选石(64, 地面, -14)],              // 五峰仙馆前院峰石座
  [-52, 地面 - 1, -18, 'minecraft:stone'],           // 岛礁水下基座出水面
];
J.校对(samples);

const job = {
  world_path: 世界,
  phases: [J.阶段()],
  samples,
  scan: { x1: -140, x2: -60, z1: -80, z2: 100, y1: 62, y2: 92 },
};
fs.writeFileSync(path.join(根, '..', '施工', '步骤8.json'), JSON.stringify(job));

// 东半区只读验收扫描（冠云峰庭院、东北丘、五峰仙馆前院峰石）
const 验 = {
  world_path: 世界,
  phases: [],
  samples: [
    [118, 地面 + 1, -32, 选石(118, 地面, -32)],
    [120, 65, -90, 'minecraft:grass_block[snowy=false]'],
    [64, 地面, -14, 选石(64, 地面, -14)],
  ],
  scan: { x1: 55, x2: 140, z1: -120, z2: 45, y1: 62, y2: 80 },
};
fs.writeFileSync(path.join(根, '..', '施工', '步骤8验.json'), JSON.stringify(验));
console.log('步骤8 ops=', J.operations.length, 'palette=', J.palette.length, 'samples=', samples.length, '+东半区验收扫描');
