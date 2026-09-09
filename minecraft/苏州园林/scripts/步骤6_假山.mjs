/**
 * 步骤6 假山：西南湖石大假山（多峰、孔窍、山洞、蹬道、笠亭）、
 * 入口障景石群、各庭院峰石、岛礁点缀。附：通往山洞的游廊。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { 作业, M, 地面, 方亭, 游廊, 随机 } from './园林库.mjs';

const 根 = path.dirname(fileURLToPath(import.meta.url));
const 世界 = 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/苏州园林';
const J = new 作业();
const 石材 = [M.湖石1, M.湖石2, M.湖石3, M.湖石4, M.湖石5];
const 选石 = (x, y, z) => 石材[((x * 7 + z * 3 + y * 5) >>> 0) % 石材.length];

/**
 * 湖石假山：多峰高斯叠加 + 边缘收分 + 抖动；表层随机孔窍（太湖石瘦皱漏透）。
 * 返回高度表（键 'x,z' → 岩体高度，含 0 起算；岩体自 y=地面 起堆）。
 */
function 湖石假山(J, cx, cz, rx, rz, 峰表, seed) {
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
      if (表层 && 窍 < 12 && hi > 2) continue; // 表层孔窍
      J.放(x, y, z, 选石(x, y, z));
    }
  }
  return H;
}

/** 独立峰石（庭院点缀）：基座 3×3，瘦柱盘旋而上，多孔 */
function 峰石(J, x, z, h, seed) {
  const rnd = 随机(seed);
  J.盒(x - 1, 地面, z - 1, x + 1, 地面, z + 1, 选石(x, 地面, z));
  let ox = 0, oz = 0;
  for (let y = 地面 + 1; y < 地面 + h; y++) {
    if (rnd() < 0.4) ox += rnd() < 0.5 ? 1 : -1; else oz += rnd() < 0.5 ? 1 : -1;
    ox = Math.max(-1, Math.min(1, ox)); oz = Math.max(-1, Math.min(1, oz));
    if (rnd() < 0.15) continue; // 透
    J.放(x + ox, y, z + oz, 选石(x, y, z));
    if (rnd() < 0.5) J.放(x - oz, y, z + ox, 选石(x + 1, y, z)); // 旁枝
  }
  J.放(x + ox, 地面 + h, z + oz, M.湖石5); // 峰顶
}

// ── 大假山（西南）：主峰 15（y78），余峰错落 ──
const 峰 = [[-58, 50, 15, 7], [-48, 56, 10, 6], [-64, 56, 9, 6], [-62, 42, 8, 5], [-46, 44, 6, 5], [-54, 44, 7, 4]];
const H = 湖石假山(J, -54, 50, 16, 13, 峰, 9001);

// 峰顶平台（笠亭基）：7×7 填实至 15 高，并压平上空（防自然峰顶穿出亭面）
for (let x = -61; x <= -55; x++) for (let z = 47; z <= 53; z++) {
  for (let y = 地面; y < 地面 + 15; y++) J.放(x, y, z, 选石(x, y, z));
  for (let y = 地面 + 15; y <= 地面 + 19; y++) J.放(x, y, z, 'minecraft:air');
}
方亭(J, -58, 50, 2, { 基y: 地面 + 15 }); // 笠亭

// 山洞：南入口隧道（x=-52, z40..47）+ 内室（-52,48）
for (let z = 40; z <= 47; z++) { J.放(-52, 地面, z, 'minecraft:air'); J.放(-52, 地面 + 1, z, 'minecraft:air'); }
for (let dx = -2; dx <= 2; dx++) for (let dz = -2; dz <= 2; dz++) for (let y = 地面; y <= 地面 + 2; y++)
  if (dx * dx + dz * dz <= 5) J.放(-52 + dx, y, 48 + dz, 'minecraft:air');

// 蹬道：自峰顶盘降，逐格找次高邻格，铺石阶
{
  const 访 = new Set(['-58,50']);
  let cur = [-57, 50], prevDir = null;
  for (let step = 0; step < 60; step++) {
    const h = H.get(cur[0] + ',' + cur[1]);
    if (h === undefined || h <= 1) break;
    const 邻 = [];
    for (let dx = -1; dx <= 1; dx++) for (let dz = -1; dz <= 1; dz++) {
      if (!dx && !dz) continue;
      const nx = cur[0] + dx, nz = cur[1] + dz, nh = H.get(nx + ',' + nz);
      if (nh !== undefined && nh < h && !访.has(nx + ',' + nz)) 邻.push([nx, nz, nh, dx, dz]);
    }
    if (!邻.length) break;
    // 优先降 1 格的平滑踏步，其次降多格；同优先换向（盘陀路）
    邻.sort((a, b2) => (b2[2] - a[2]));
    const 缓降 = 邻.filter(n => n[2] === h - 1);
    const 选 = (缓降.length ? 缓降 : 邻);
    const [nx, nz, nh, dx, dz] = 选[0];
    const f = dz === 1 ? 'north' : dz === -1 ? 'south' : dx === 1 ? 'west' : 'east'; // 面向来向（上爬方向）
    J.放(nx, 地面 + nh - 1, nz, `minecraft:stone_brick_stairs[facing=${f},half=bottom,shape=straight,waterlogged=false]`);
    访.add(nx + ',' + nz); prevDir = [dx, dz]; cur = [nx, nz];
  }
}

// ── 通往山洞的游廊（接南岸曲廊西端）──
游廊(J, [[-44, 33], [-52, 33], [-52, 40]]);

// ── 入口障景石群（影壁后西侧）──
湖石假山(J, 84, 69, 6, 4, [[82, 68, 5, 3], [88, 70, 4, 3]], 7001);

// ── 庭院峰石 ──
峰石(J, 60, 66, 5, 11); 峰石(J, 54, 72, 4, 12);   // 枇杷园
峰石(J, 15, 53, 4, 13);                              // 听雨轩
峰石(J, -27, -74, 5, 14); 峰石(J, -13, -72, 4, 15); // 远香堂后
峰石(J, -4, -19, 3, 16); 峰石(J, -45, -7, 3, 17);   // 双岛礁

// ── 自检采样（选石公式确定性复算）──
const samples = [
  [-48, 地面 + 3, 56, 选石(-48, 地面 + 3, 56)],     // 次峰岩体
  [-58, 地面 + 14, 50, 'minecraft:stone_bricks'],    // 峰顶平台（笠亭台基）
  [-60, 地面 + 15, 48, 'minecraft:dark_oak_log[axis=y]'], // 笠亭角柱
  [-52, 地面, 48, 'minecraft:air'],                  // 山洞内室
  [-48, 地面 + 5, 33, 'minecraft:deepslate_tile_slab[type=top,waterlogged=false]'], // 游廊脊
  [84, 地面 + 1, 69, 选石(84, 地面 + 1, 69)],        // 障景石
];
const job = {
  world_path: 世界,
  phases: [J.阶段()],
  samples,
  scan: { x1: -80, x2: 100, z1: 30, z2: 84, y1: 62, y2: 92 },
};
fs.writeFileSync(path.join(根, '..', '施工', '步骤6.json'), JSON.stringify(job));
console.log('步骤6 ops=', J.operations.length, 'palette=', J.palette.length);
