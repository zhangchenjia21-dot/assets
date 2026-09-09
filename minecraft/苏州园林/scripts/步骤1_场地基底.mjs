/**
 * 步骤1 场地基底：创建超平坦世界（关结构）+ 大水池开挖注水 + 双岛 + 驳岸。
 * 产出 施工/步骤1.json；同一作业内完成 create + phases + samples + scan。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { 作业, M, 水面, 池底, 地表, 随机 } from './园林库.mjs';
import { 池内, 岛内, 水体 } from './池形.mjs';

const 根 = path.dirname(fileURLToPath(import.meta.url));
const 世界 = 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/苏州园林';

const J = new 作业();
const rnd = 随机(20261010);
const 统计 = { 水格: 0, 驳岸: 0 };
let 岸线样本 = null; // 记录首个被改写的岸线格及其真实用石，供回读校验

const X1 = -82, X2 = 18, Z1 = -52, Z2 = 32;
for (let x = X1; x <= X2; x++) for (let z = Z1; z <= Z2; z++) {
  if (水体(x, z)) {
    统计.水格++;
    J.放(x, 地表, z, 'minecraft:air');                    // 去草
    for (let y = 水面; y > 池底; y--) J.放(x, y, z, M.水);  // 60..62 水
    J.放(x, 池底, z, M.黏土);                              // 池底黏土
    J.放(x, 池底 - 1, z, rnd() < 0.3 ? M.碎石 : M.土);      // 池底下层
  } else {
    // 岸线：四邻有水的陆地格 → 湖石驳岸（草换湖石，水下边也换）
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
function 采样(x, z) {
  if (水体(x, z)) { samples.push([x, 水面, z, 'minecraft:water[level=0]'], [x, 池底, z, 'minecraft:clay']); return true; }
  return false;
}
采样(-30, -10); 采样(-55, 8); 采样(-5, -30); 采样(-64, -24);
// 岛心草面
samples.push([-8, 地表, -14, 'minecraft:grass_block[snowy=false]'], [-40, 地表, -4, 'minecraft:grass_block[snowy=false]']);
// 岸线石（取脚本实际放置的那一格）
if (岸线样本) samples.push(岸线样本);
// 远处 untouched 对照
samples.push([88, 地表, 72, 'minecraft:grass_block[snowy=false]'], [0, -64, 0, 'minecraft:bedrock']);

const job = {
  world_path: 世界,
  create: {
    type: 'superflat', seed: 20261010,
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
  spawn: [88, 64, 72],
  phases: [J.阶段()],
  samples,
  scan: { x1: X1, x2: X2, z1: Z1, z2: Z2, y1: 56, y2: 64 },
};
fs.mkdirSync(path.join(根, '..', '施工'), { recursive: true });
const 出 = path.join(根, '..', '施工', '步骤1.json');
fs.writeFileSync(出, JSON.stringify(job));
console.log('已生成', 出, 统计, 'ops=', J.operations.length, 'palette=', J.palette.length, 'samples=', samples.length);
