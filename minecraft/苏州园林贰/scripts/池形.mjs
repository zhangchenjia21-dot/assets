/**
 * 池形：苏州园林贰全园水系的共享几何判定。
 * 所有需要与水面/岸线/溪流打交道的步骤（桥、舫、廊、假山、植被）必须引用本模块，
 * 保证与步骤1 实际施工完全一致。
 * 坐标约定：+x 东，+z 南；水面 y=62，池底 y=59。
 */

// 池形参数：椭圆复合 + 岸线抖动（与设计文档 §2 一致，改形必须同步改文档）
const 椭圆组 = [
  [-35, -5, 52, 38],  // E1 主体
  [-88, 25, 20, 15],  // E2 西湾
  [18, -32, 20, 14],  // E3 东湾
  [-5, 38, 26, 13],   // E4 南湾
  [-62, -48, 17, 12], // E5 西北源（接活泼泼地溪口）
];
const 岛组 = [
  [-38, -6, 9, 8],    // 岛A 主岛·湖心亭
  [-70, 10, 6, 5],    // 岛B 荷风亭
  [16, -30, 5, 4],    // 岛C 笠亭小岛
];

const 椭圆 = (x, z, cx, cz, rx, rz) => ((x - cx) / rx) ** 2 + ((z - cz) / rz) ** 2;
function 抖动(x, z) {
  let h = (x * 374761393 + z * 668265263) >>> 0; h = (h ^ (h >> 13)) * 1274126177 >>> 0;
  return ((h % 1000) / 1000 - 0.5) * 0.12;
}
export function 池内(x, z) {
  const j = 抖动(x, z);
  return 椭圆组.some(([cx, cz, rx, rz]) => 椭圆(x, z, cx, cz, rx, rz) + j <= 1);
}
export function 岛内(x, z) { return 岛组.some(([cx, cz, rx, rz]) => 椭圆(x, z, cx, cz, rx, rz) <= 1); }
export function 池水(x, z) { return 池内(x, z) && !岛内(x, z); }

/** 活泼泼地溪流中心线（西北土山 → E5 西北源），正交折线 */
export const 溪线 = [[-124, -40], [-112, -40], [-112, -34], [-100, -34], [-100, -42], [-88, -42], [-88, -48], [-78, -48]];
/** 溪流格：距中心线曼哈顿宽 1（水面宽 3） */
export function 溪水(x, z) {
  for (let i = 0; i < 溪线.length - 1; i++) {
    const [ax, az] = 溪线[i], [bx, bz] = 溪线[i + 1];
    const x1 = Math.min(ax, bx) - 1, x2 = Math.max(ax, bx) + 1;
    const z1 = Math.min(az, bz) - 1, z2 = Math.max(az, bz) + 1;
    if (x >= x1 && x <= x2 && z >= z1 && z <= z2) return true;
  }
  return false;
}

export function 水体(x, z) { return 池水(x, z) || 溪水(x, z); }
/** 岸线：本身非水但四邻含水的陆地格 */
export function 岸线(x, z) {
  return !水体(x, z) && (水体(x + 1, z) || 水体(x - 1, z) || 水体(x, z + 1) || 水体(x, z - 1));
}
