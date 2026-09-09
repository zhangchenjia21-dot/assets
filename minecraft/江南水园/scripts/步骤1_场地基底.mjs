/**
 * 步骤1 场地基底：创建超平坦世界（关结构）+ 开挖注水（主湖/西湾/东湾/南湾/西水巷/连通渠）
 * + 四岛 + 湖畔水巷驳岸。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { 作业, M, 水面, 池底, 地表, 随机 } from './园林库.mjs';
import { 水体 } from './池形.mjs';

const 根 = path.dirname(fileURLToPath(import.meta.url));
const 世界 = 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/江南水园';

const J = new 作业();
const rnd = 随机(20261011);
const 统计 = { 水格: 0, 驳岸: 0 };
let 岸线样本 = null;

const X1 = -62, X2 = 52, Z1 = -58, Z2 = 62;
for (let x = X1; x <= X2; x++) for (let z = Z1; z <= Z2; z++) {
  if (水体(x, z)) {
    统计.水格++;
    J.放(x, 地表, z, 'minecraft:air');
    for (let y = 水面; y > 池底; y--) J.放(x, y, z, M.水);
    J.放(x, 池底, z, M.黏土);
    J.放(x, 池底 - 1, z, rnd() < 0.3 ? M.碎石 : M.土);
  } else {
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

const samples = [];
function 水样(x, z) { samples.push([x, 水面, z, 'minecraft:water[level=0]'], [x, 池底, z, 'minecraft:clay']); }
水样(0, -30); 水样(-40, -6); 水样(38, 4); 水样(2, 18); 水样(-56, 20); // 五处水面+西水巷
// 四岛心草面
samples.push([0, 地表, -6, 'minecraft:grass_block[snowy=false]']);
samples.push([26, 地表, -4, 'minecraft:grass_block[snowy=false]']);
samples.push([-28, 地表, -6, 'minecraft:grass_block[snowy=false]']);
samples.push([2, 地表, 12, 'minecraft:grass_block[snowy=false]']);
if (岸线样本) samples.push(岸线样本);
// 未动对照
samples.push([40, 地表, 50, 'minecraft:grass_block[snowy=false]'], [0, -64, 0, 'minecraft:bedrock']);

const job = {
  world_path: 世界,
  create: {
    type: 'superflat', seed: 20261011,
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
  spawn: [0, 64, 58],
  phases: [J.阶段()],
  samples,
  scan: { x1: X1, x2: X2, z1: Z1, z2: Z2, y1: 56, y2: 64 },
};
fs.writeFileSync(path.join(根, '..', '施工', '步骤1.json'), JSON.stringify(job));
console.log('步骤1 水格=', 统计.水格, '驳岸=', 统计.驳岸, 'ops=', J.operations.length, 'palette=', J.palette.length);
