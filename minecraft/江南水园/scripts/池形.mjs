/**
 * 江南水园 池形：一池三岛带水巷的湖面几何。
 * 湖体 = 主湖 A ∪ 西湾 B ∪ 东湾 C ∪ 南湾 D ∪ 西水巷(运河) ∪ 连通渠；
 * 水体 = 湖体 − 四岛(I1..I4)。
 * 坐标：+x 东，+z 南，以园心(0,0)为原点；围墙在 ±63。
 */
export function 椭圆(x, z, cx, cz, rx, rz) { return ((x - cx) / rx) ** 2 + ((z - cz) / rz) ** 2; }

const 湖体 = [
  [0, -6, 33, 27],    // A 主湖
  [-40, -6, 12, 11],  // B 西湾
  [38, 4, 11, 9],     // C 东湾
  [2, 18, 13, 6],     // D 南湾
];
const 岛 = [
  [0, -6, 10, 8],     // I1 湖心岛（澄心堂）
  [26, -4, 5, 4],     // I2 东岛（一镜亭）
  [-28, -6, 4, 3],    // I3 西岛（沧浪亭）
  [2, 12, 4, 3],      // I4 南岛（笠亭）
];
// 西水巷（运河）与主湖连通渠
const 水巷 = (x, z) => x >= -58 && x <= -54 && z >= -56 && z <= 58;
const 连通渠 = (x, z) => x >= -56 && x <= -50 && z >= -4 && z <= 0;

export function 池内(x, z) {
  const 湖 = 湖体.some(([cx, cz, rx, rz]) => 椭圆(x, z, cx, cz, rx, rz) <= 1) || 水巷(x, z) || 连通渠(x, z);
  return 湖 && !岛.some(([cx, cz, rx, rz]) => 椭圆(x, z, cx, cz, rx, rz) <= 1);
}
export function 岛内(x, z) { return 岛.some(([cx, cz, rx, rz]) => 椭圆(x, z, cx, cz, rx, rz) <= 1); }
export function 水体(x, z) { return 池内(x, z) && !岛内(x, z); }
export function 岸线(x, z) {
  return !水体(x, z) && (水体(x + 1, z) || 水体(x - 1, z) || 水体(x, z + 1) || 水体(x, z - 1));
}
