/**
 * 步骤1 场地基底：创建超平坦世界（关结构）+ 大池开挖注水 + 三岛 + 驳岸
 *   + 西部土山两峰 + 活泼泼地溪床。
 * 产出 施工/步骤1.json；同一作业内完成 create + phases + samples + scan。
 * 施工顺序：土山 → 池/溪开挖（水优先于山，形成山涧入水）→ 岸线驳岸。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { 作业, M, 水面, 池底, 地表, 随机 } from './园林库.mjs';
import { 池内, 岛内, 水体, 溪水 } from './池形.mjs';

const 根 = path.dirname(fileURLToPath(import.meta.url));
const 世界 = 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/苏州园林贰';

const J = new 作业();
const rnd = 随机(20261012);
const 统计 = { 水格: 0, 驳岸: 0, 山格: 0 };
let 岸线样本 = null;

// ── 西部土山：椭圆丘，高度随 (1-e) 收分；山1 高 10，山2 高 7 ──
const 丘 = [[-115, -30, 22, 18, 10], [-112, 8, 15, 12, 7]];
function 山高(x, z) {
  let h = 0;
  for (const [cx, cz, rx, rz, 峰] of 丘) {
    const e = ((x - cx) / rx) ** 2 + ((z - cz) / rz) ** 2;
    if (e <= 1) h = Math.max(h, Math.round((1 - e) * 峰));
  }
  return h;
}

const X1 = -140, X2 = 45, Z1 = -62, Z2 = 55;
for (let x = X1; x <= X2; x++) for (let z = Z1; z <= Z2; z++) {
  const h = 山高(x, z);
  if (水体(x, z)) {
    // 先削平可能存在的山坡，再注水
    if (h > 0) for (let y = 地表 + 1; y <= 地表 + h; y++) J.放(x, y, z, 'minecraft:air');
    统计.水格++;
    J.放(x, 地表, z, 'minecraft:air');
    for (let y = 水面; y > 池底; y--) J.放(x, y, z, M.水);
    J.放(x, 池底, z, M.黏土);
    J.放(x, 池底 - 1, z, rnd() < 0.3 ? M.碎石 : M.土);
  } else if (h > 0) {
    // 土山：草顶 + 下填泥土（坡脚渐次落地）
    统计.山格++;
    J.放(x, 地表 + h, z, 'minecraft:grass_block[snowy=false]');
    if (h > 1) J.盒(x, 地表 + 1, z, x, 地表 + h - 1, z, M.土);
  } else {
    // 岸线：四邻有水的陆地格 → 湖石驳岸
    const 邻水 = 水体(x + 1, z) || 水体(x - 1, z) || 水体(x, z + 1) || 水体(x, z - 1);
    if (邻水) {
      统计.驳岸++;
      const 石 = [M.驳岸, M.湖石2, M.湖石1][Math.floor(rnd() * 3)];
      if (!岸线样本) 岸线样本 = [x, 地表, z, 石];
      J.放(x, 地表, z, 石);
      J.放(x, 地表 - 1, z, 石);
    }
  }
}

// ── 自检采样：从同一模型取代表性坐标 ──
const samples = [];
function 采水(x, z) {
  if (!水体(x, z)) throw new Error(`采样点非水体 ${x},${z}`);
  samples.push([x, 水面, z, 'minecraft:water[level=0]'], [x, 池底, z, 'minecraft:clay']);
}
采水(-20, -20);  // E1 主体（避开岛A）
采水(-88, 25);   // E2 西湾
采水(24, -34);   // E3 东湾
采水(-5, 38);    // E4 南湾
采水(-62, -48);  // E5 西北源
采水(-112, -40); // 活泼泼地溪
// 岛心草面
for (const [x, z] of [[-38, -6], [-70, 10], [16, -30]])
  samples.push([x, 地表, z, 'minecraft:grass_block[snowy=false]']);
// 两山峰顶草面（高度与山高()同源）
samples.push([-115, 地表 + 山高(-115, -30), -30, 'minecraft:grass_block[snowy=false]']);
samples.push([-112, 地表 + 山高(-112, 8), 8, 'minecraft:grass_block[snowy=false]']);
// 岸线石（取脚本实际放置的那一格）
if (岸线样本) samples.push(岸线样本);
// 远处 untouched 对照
samples.push([120, 地表, 100, 'minecraft:grass_block[snowy=false]'], [0, -64, 0, 'minecraft:bedrock']);

const job = {
  world_path: 世界,
  create: {
    type: 'superflat', seed: 20261012,
    generator_options: {
      biome: 'minecraft:plains',
      layers: [
        { block: 'minecraft:bedrock', height: 1 },
        { block: 'minecraft:dirt', height: 126 },
        { block: 'minecraft:grass_block', height: 1 },
      ],
      structure_overrides: [],
    },
  },
  difficulty: 'peaceful',
  spawn: [116, 64, 112],
  phases: [J.阶段()],
  samples,
  scan: { x1: X1, x2: X2, z1: Z1, z2: Z2, y1: 56, y2: 74 },
};
fs.mkdirSync(path.join(根, '..', '施工'), { recursive: true });
const 出 = path.join(根, '..', '施工', '步骤1.json');
fs.writeFileSync(出, JSON.stringify(job));
console.log('已生成', 出, 统计, 'ops=', J.operations.length, 'palette=', J.palette.length, 'samples=', samples.length);
