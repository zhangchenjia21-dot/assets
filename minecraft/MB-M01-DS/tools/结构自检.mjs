// 结构自检：不依赖图像，直接从蓝本体素做几何与连通性断言。
// 覆盖 v1.10 §20 Construction Closure & Clearance Gate 的可计算部分：
//   A. Ground Contact / Support Closure —— 悬空检测、墙脚/门槛接触链
//   B. Movement Envelope Clearance —— 玩家碰撞体（高 2 格、宽 1 格）沿真实路径的连续净空
//   C. 房间/空间成立性 —— 关键空间是否有足够净体积、是否被意外封死
import { Builder, AIR } from './几何核心.mjs';
import { G, M } from './设计参数.mjs';

const PASSABLE = new Set(['minecraft:air', 'minecraft:water']);

export function makeSolid(vol) {
  const { grid, nx, ny, nz, bounds } = vol;
  const at = (x, y, z) => {
    const ix = x - bounds.x1, iy = y - bounds.y1, iz = z - bounds.z1;
    if (ix < 0 || iy < 0 || iz < 0 || ix >= nx || iy >= ny || iz >= nz) return 'minecraft:air';
    return grid[iy * nz * nx + iz * nx + ix] || 'minecraft:air';
  };
  const isAir = (x, y, z) => {
    const s = at(x, y, z);
    return s === 'minecraft:air';
  };
  // 可通行：玩家碰撞体（脚下 1 格 + 头 1 格）均为空气；台阶类（楼梯/半砖）视为可站立
  const standable = (x, y, z) => {
    const s = at(x, y, z);
    if (s === 'minecraft:air') return false;
    if (/slab\[type=top/.test(s)) return false;
    return true;
  };
  const canOccupy = (x, y, z) => isAir(x, y, z) && isAir(x, y + 1, z);
  return { at, isAir, standable, canOccupy, bounds, nx, ny, nz };
}

/** A. 悬空检测：统计"下方无任何支承且非悬挑意图"的方块。 */
export function checkFloating(solid, { ignoreBelow = -4 } = {}) {
  const { bounds } = solid;
  const bad = [];
  for (let x = bounds.x1; x <= bounds.x2; x++) for (let z = bounds.z1; z <= bounds.z2; z++) {
    for (let y = bounds.y1 + 1; y <= bounds.y2; y++) {
      const s = solid.at(x, y, z);
      if (s === 'minecraft:air') continue;
      if (solid.at(x, y - 1, z) !== 'minecraft:air') continue;
      // 下方为空：检查是否有侧向支承（悬挑/拱券允许）
      const lateral = solid.isAir(x - 1, y, z) || solid.isAir(x + 1, y, z) || solid.isAir(x, y, z - 1) || solid.isAir(x, y, z + 1);
      if (!lateral) bad.push([x, y, z, s]);
    }
  }
  return bad;
}

/**
 * B. 运动净空：以 1×2 碰撞体沿指定路径做真实步进检查。
 * 站立面 = 脚下是实体（或台阶/半砖等可站方块），且其上方 2 格均为空气。
 * 相邻点高差 > 1 格需跳跃（Minecraft step height 仅 0.6 格），记为问题。
 */
export function walkPath(solid, path, { name = '', maxRise = 1, maxDrop = 4, tolerance = 2 } = {}) {
  const issues = [];
  let prev = null;
  for (const [x, z, expectY] of path) {
    // 在预期标高 ±tolerance 内，自下而上寻找**最低的**合法落脚面：
    // 最低可站立面才是玩家实际行走面（避免误选上方平台/梁顶）。
    let found = null;
    for (let dy = -tolerance; dy <= tolerance && found === null; dy++) {
      const y = expectY + dy;
      if (solid.standable(x, y, z) && solid.canOccupy(x, y + 1, z)) found = y;
    }
    if (found === null) {
      issues.push({ at: [x, expectY, z], kind: 'NO_STANDING_SPACE', detail: `预期标高 ±${tolerance} 内无"可站立面 + 上方 2 格净空"` });
      prev = null;
      continue;
    }
    if (prev !== null) {
      const rise = found - prev.y;
      // 0.6 格以内的抬升是 Minecraft 原生 step-up；这里以 1 格为保守上限
      if (rise > maxRise) issues.push({ at: [x, found, z], kind: 'STEP_TOO_HIGH', detail: `相对上一格抬升 ${rise} 格（>${maxRise}，需跳跃）` });
      if (rise < -maxDrop) issues.push({ at: [x, found, z], kind: 'DROP_TOO_DEEP', detail: `相对上一格下降 ${-rise} 格` });
    }
    prev = { x, y: found, z };
  }
  return { name, issues, steps: path.length };
}

/** C. 空间体积：统计某长方体范围内的空气格数量与连通体积（判断空间是否成立且未被封死）。 */
export function compartmentVolume(solid, { x1, x2, y1, y2, z1, z2 }) {
  const seen = new Set();
  let air = 0;
  for (let x = x1; x <= x2; x++) for (let y = y1; y <= y2; y++) for (let z = z1; z <= z2; z++) if (solid.isAir(x, y, z)) air++;
  // 从中心做 6 邻域洪泛（只在该长方体内）
  const key = (x, y, z) => x + ',' + y + ',' + z;
  const start = [Math.round((x1 + x2) / 2), Math.round((y1 + y2) / 2), Math.round((z1 + z2) / 2)];
  let seed = null;
  outer: for (let r = 0; r < 6 && !seed; r++) {
    for (let x = start[0] - r; x <= start[0] + r; x++) for (let y = start[1] - r; y <= start[1] + r; y++) for (let z = start[2] - r; z <= start[2] + r; z++) {
      if (x < x1 || x > x2 || y < y1 || y > y2 || z < z1 || z > z2) continue;
      if (solid.isAir(x, y, z)) { seed = [x, y, z]; break outer; }
    }
  }
  if (!seed) return { air, largest: 0, pockets: 0 };
  const stack = [seed];
  seen.add(key(...seed));
  while (stack.length) {
    const [x, y, z] = stack.pop();
    for (const [dx, dy, dz] of [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]) {
      const nx = x + dx, ny = y + dy, nz = z + dz;
      if (nx < x1 || nx > x2 || ny < y1 || ny > y2 || nz < z1 || nz > z2) continue;
      const k = key(nx, ny, nz);
      if (seen.has(k)) continue;
      if (!solid.isAir(nx, ny, nz)) continue;
      seen.add(k);
      stack.push([nx, ny, nz]);
    }
  }
  return { air, largest: seen.size, pockets: air - seen.size };
}
