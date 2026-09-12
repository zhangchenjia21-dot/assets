// ============================================================================
// Layer C｜Finishing（v1.10 §15–§17）
// 原则：
//   §15.1 Finish From Use    —— 家具与陈设由活动推出，不因空间空就塞东西
//   §15.2 Finish From Construction —— 门窗收口、柱脚、檐口、梁端、排水说明建筑怎么落地
//   §15.3 Finish From Material & Time —— 时间层按"原因+位置+强度"，不做均匀随机噪声
//   §15.4 Finish From Attention —— Focal / Supporting / Quiet 有主次，但 Quiet ≠ 未处理
//   §15.5 Finish From Light  —— 按功能照度与路线识别布光，不按格距插火把
//   §15.6 Finish From Life   —— 储物、货物、工具、维护状态
//   §15.7 For Minecraft Perception —— Far/Mid/Near 三层可读性
// 权限：Allowed 全用；Restricted 仅在不改 Core semantic 时使用；Frozen 一律不动。
// ============================================================================
import { S, AIR } from './几何核心.mjs';
import { G, M } from './设计参数.mjs';

const T = (m, facing, half = 'bottom', shape = 'straight') => S(m, { facing, half, shape });
const SLAB = (m, type = 'bottom') => S(m, { type });

// 便捷：面朝某方向放置壁挂物（火把/灯笼/招牌/旗帜）；只传 schema 中真实存在的属性
const torch = (facing) => S('minecraft:wall_torch', { facing });
const lanternH = (hanging) => S('minecraft:lantern', { hanging });
const barrel = (facing = 'up', open = 'false') => S('minecraft:barrel', { facing, open });
const chest = (facing) => S('minecraft:chest', { facing });
const lectern = (facing) => S('minecraft:lectern', { facing });
const sign = (facing, mat = 'minecraft:spruce_wall_sign') => S(mat, { facing });
const banner = (facing) => S('minecraft:red_wall_banner', { facing });
const candle = (n, lit) => S('minecraft:candle', { candles: String(n), lit: String(lit) });
const campfire = (facing, lit) => S('minecraft:campfire', { facing, lit: String(lit) });
const ladder = (facing) => S('minecraft:ladder', { facing });
const fence = () => S('minecraft:dark_oak_fence', { north: 'true', east: 'true', south: 'true', west: 'true' });
const trapdoor = (facing, half, open) => S('minecraft:dark_oak_trapdoor', { facing, half, open });
const moss = () => S('minecraft:moss_carpet', {});
const shortGrass = () => S('minecraft:short_grass', {});
const fern = () => S('minecraft:fern', {});

// ============================================================================
// Pass 1｜Functional Finish（家具、活动区、储物、功能照明、净空）
// ============================================================================
export function passFunctional(b) {
  b.beginStage('F1-功能精修');

  // ---------- 1.1 交易厅：Kaufkammern（可租摊位）+ 市秤 + 过秤 + 账房 ----------
  // 摊位沿南北两跨的后墙布置（背靠实墙、面向通道），每 6 格一档，与墩距一致
  const stallZ = [16, 22, 28, 34, 40];
  for (const z of stallZ) {
    // 南跨摊位：靠南墙（x=8..9），台面 + 货箱 + 招牌
    for (let dz = 0; dz <= 2; dz++) b.override(8, G.yGround, z + dz, M.timberStrip, '摊位台面');
    b.override(8, G.yGround + 1, z + 2, SLAB(M.slabTimber), '摊位台面');
    b.override(9, G.yGround, z, barrel('up'), '货桶');
    b.override(9, G.yGround, z + 1, barrel('up'), '货桶');
    if (z !== 40) b.override(8, G.yGround + 2, z + 1, sign('south'), '摊位标识');
    // 北跨摊位：靠北墙（x=15..16）
    for (let dz = 0; dz <= 2; dz++) b.override(16, G.yGround, z + dz, M.timberStrip, '摊位台面');
    b.override(16, G.yGround + 1, z + 2, SLAB(M.slabTimber), '摊位台面');
    b.override(15, G.yGround, z, barrel('up'), '货桶');
    b.override(15, G.yGround, z + 1, chest('west'), '货箱');
  }
  // 市秤（Waage）：位于拱廊西端第一开间中央——公共可达，且不阻断 x=5 通行带
  const wgX = 4, wgZ = 4;
  b.override(wgX, G.yGround, wgZ, M.pavingIn, '市秤台基');
  b.override(wgX, G.yGround + 1, wgZ, M.plinth, '市秤座');
  b.override(wgX, G.yGround + 2, wgZ, SLAB(M.slabPier), '市秤天平');
  b.override(wgX, G.yGround + 3, wgZ, S('minecraft:iron_chain', { axis: 'y' }), '秤链');
  b.override(wgX, G.yGround + 4, wgZ, M.iron, '秤盘');
  b.override(wgX, G.yGround + 5, wgZ, lanternH('true'), '市秤灯');
  b.override(wgX, G.yGround + 2, wgZ - 1, sign('east'), '市秤标识');
  // 账房（Kaufhaus-Schreiber）：交易厅东端，一张账桌 + 书架 + 灯
  b.override(9, G.yGround, 42, M.timberStrip, '账桌');
  b.override(9, G.yGround + 1, 42, SLAB(M.slabTimber), '账桌');
  b.override(9, G.yGround + 1, 43, lectern('north'), '账册台');
  b.override(8, G.yGround + 1, 42, candle(2, 'true'), '账房烛台');
  b.override(8, G.yGround, 43, chest('east'), '账册箱');
  // 过秤间（后勤翼）：台秤 + 货堆
  b.override(21, G.yGround, 25, M.plinth, '台秤座');
  b.override(21, G.yGround + 1, 25, M.iron, '秤盘');
  b.override(22, G.yGround, 24, barrel('up'), '待过秤货');
  b.override(22, G.yGround, 26, barrel('up'), '待过秤货');
  b.override(22, G.yGround + 1, 25, S('minecraft:iron_chain', { axis: 'y' }), '秤链');
  // 看守室（Pförtner）：门侧一桌一椅一灯
  b.override(21, G.yGround, 6, M.timberStrip, '看守桌');
  b.override(21, G.yGround + 1, 6, SLAB(M.slabTimber), '看守桌');
  b.override(21, G.yGround + 1, 7, lanternH('false'), '看守灯');
  b.override(22, G.yGround, 5, chest('east'), '看守柜');
  // 后勤储物间：桶与箱成组（由"收货—暂存—发运"推出，不做均匀铺撒）
  for (const [x, z, st] of [[22, 12, barrel('up')], [23, 12, barrel('up')], [22, 13, barrel('up')],
    [23, 30, chest('west')], [23, 31, chest('west')], [22, 31, barrel('up')], [22, 37, barrel('up')], [23, 37, chest('east')]]) {
    b.override(x, G.yGround, z, st, '后勤储物');
  }
  // 地窖：酒桶列 + 盐/粮箱（酒窖/盐仓/粮仓三分区，与 S2 的隔墙一致）
  for (let z = 4; z <= 12; z += 2) { b.override(9, G.yCellarFloor, z, barrel('up'), '酒桶'); b.override(10, G.yCellarFloor, z + 1, barrel('up'), '酒桶'); }
  for (let z = 18; z <= 26; z += 2) { b.override(15, G.yCellarFloor, z, chest('east'), '盐箱'); b.override(16, G.yCellarFloor, z + 1, chest('east'), '盐箱'); }
  for (let z = 34; z <= 42; z += 2) { b.override(9, G.yCellarFloor, z, barrel('up'), '粮桶'); b.override(20, G.yCellarFloor, z, barrel('up'), '粮桶'); }
  b.override(15, G.yCellarFloor, 20, lanternH('false'), '地窖灯');
  b.override(10, G.yCellarFloor, 8, lanternH('false'), '地窖灯');
  b.override(20, G.yCellarFloor, 36, lanternH('false'), '地窖灯');

  // ---------- 1.2 上层大厅：市民大会/Fest 的空间 ----------
  // 长桌与长凳沿大厅中部（集会时的主家具），不做密集排布
  for (let z = 8; z <= 34; z += 13) {
    for (let x = 12; x <= 16; x++) b.override(x, G.yGreatFloor, z, M.timberStrip, '长桌');
    for (let x = 12; x <= 16; x++) b.override(x, G.yGreatFloor, z + 2, SLAB(M.slabTimber), '长凳');
    b.override(14, G.yGreatFloor + 1, z, candle(4, 'true'), '桌上烛台');
    b.override(12, G.yGreatFloor, z + 2, barrel('up'), '厅内储物');
  }
  // 议事厅（Ratsstube，上层北侧辅助房间）：议事桌 + 席位 + 账册
  b.override(22, G.yGreatFloor, 14, M.timberStrip, '议事桌');
  b.override(22, G.yGreatFloor + 1, 14, SLAB(M.slabTimber), '议事桌');
  b.override(21, G.yGreatFloor, 14, SLAB(M.slabTimber), '席位');
  b.override(21, G.yGreatFloor, 15, SLAB(M.slabTimber), '席位');
  b.override(23, G.yGreatFloor, 15, lectern('west'), '议事册');
  b.override(22, G.yGreatFloor + 1, 16, candle(3, 'true'), '议事烛台');
  // 市长室（ Bürgermeister）：桌 + 柜 + 旗
  b.override(22, G.yGreatFloor, 26, M.timberStrip, '市长桌');
  b.override(21, G.yGreatFloor, 26, SLAB(M.slabTimber), '座椅');
  b.override(22, G.yGreatFloor + 1, 27, candle(2, 'true'), '烛台');
  b.override(23, G.yGreatFloor, 24, chest('west'), '卷宗柜');
  b.override(24, G.yGreatFloor + 2, 26, banner('west'), '市旗');
  // 金库 / 档案（Schatzkammer）：铁门 + 铁栅 + 双层箱
  b.override(20, G.yGreatFloor, 21, S(M.doorIron, { facing: 'east', half: 'lower', hinge: 'left', open: 'false' }), '金库门');
  b.override(20, G.yGreatFloor + 1, 21, S(M.doorIron, { facing: 'east', half: 'upper', hinge: 'left', open: 'false' }), '金库门');
  b.override(22, G.yGreatFloor, 20, chest('east'), '金库箱');
  b.override(23, G.yGreatFloor, 20, chest('east'), '金库箱');
  b.override(22, G.yGreatFloor + 1, 20, chest('east'), '金库箱');
  // 法院厅（Gerichtsstube）：审判席 + 旁听长凳 + 吕贝克树式的界桩
  b.override(22, G.yGreatFloor, 34, M.plinth, '审判席位');
  b.override(22, G.yGreatFloor + 1, 34, SLAB(M.slabPier), '审判席位');
  for (let z = 32; z <= 36; z += 2) b.override(21, G.yGreatFloor, z, SLAB(M.slabTimber), '旁听长凳');
  b.override(23, G.yGreatFloor + 2, 34, sign('west'), '法院标识');
  b.override(23, G.yGreatFloor, 36, lectern('north'), '律册台');

  // ---------- 1.3 垂直交通与门槛的功能性收口 ----------
  // 主楼梯口：扶手（Allowed 范围内的栏杆调整）
  for (let z = 4; z <= 9; z++) {
    const i = Math.max(0, 9 - z);
    b.override(11, G.yGround + i + 2, z, fence(), '楼梯扶手');
  }
  // 大厅井口护栏（沿井口三边，Quiet 但必须成立）
  for (let z = 3; z <= 10; z++) b.override(7, G.yGreatFloor + 1, z, fence(), '井口扶手');
  for (let x = 8; x <= 10; x++) b.override(x, G.yGreatFloor + 1, 10, fence(), '井口扶手');
  // 地窖井口护栏
  for (let z = 30; z <= 33; z++) b.override(7, G.yGround + 1, z, fence(), '地窖口栏');
  for (let x = 8; x <= 10; x++) b.override(x, G.yGround + 1, 34, fence(), '地窖口栏');

  return b;
}

// ============================================================================
// Pass 2｜Architectural Finish（门窗收口、墙脚、柱、檐口、屋脊、转角接口）
// ============================================================================
export function passArchitectural(b) {
  b.beginStage('F2-建筑收口');

  // ---------- 2.1 墙脚（Sockel）：沿建筑外缘做连续勒脚带 ----------
  // 只在"墙面与铺地交界"处加一道浅色石收边；**不得封堵门洞**
  const solidAt = (x, y, z) => {
    const cur = b.get(x, y, z);
    return typeof cur === 'string' && cur !== AIR && cur.includes('cinnabar_bricks');
  };
  for (let z = 0; z <= 44; z++) {
    if (solidAt(6, G.yGround + 1, z)) b.override(6, G.yGround + 1, z, M.light, '墙脚收边');
    if (solidAt(18, G.yGround + 1, z)) b.override(18, G.yGround + 1, z, M.light, '墙脚收边');
  }
  for (let x = 6; x <= 24; x++) {
    if (solidAt(x, G.yGround + 1, 0)) b.override(x, G.yGround + 1, 0, M.light, '墙脚收边');
    if (solidAt(x, G.yGround + 1, 44)) b.override(x, G.yGround + 1, 44, M.light, '墙脚收边');
  }
  // 上层墙脚（大厅地坪以上）；同样跳过门窗洞口
  for (let z = 0; z <= 44; z++) {
    if (solidAt(6, G.yGreatFloor, z)) b.override(6, G.yGreatFloor, z, M.plinthDark, '上层墙脚');
    if (solidAt(18, G.yGreatFloor, z)) b.override(18, G.yGreatFloor, z, M.plinthDark, '上层墙脚');
  }
  for (let x = 6; x <= 24; x++) {
    if (solidAt(x, G.yGreatFloor, 0)) b.override(x, G.yGreatFloor, 0, M.plinthDark, '上层墙脚');
    if (solidAt(x, G.yGreatFloor, 44)) b.override(x, G.yGreatFloor, 44, M.plinthDark, '上层墙脚');
  }

  // ---------- 2.2 拱廊柱脚与柱头收口 ----------
  for (const z of G.zPier) {
    for (let dz = 0; dz <= 1; dz++) {
      b.override(3, G.yGround, z + dz, M.plinthDark, '柱脚');
      b.override(4, G.yGround, z + dz, M.plinthDark, '柱脚');
      b.override(3, G.ySpring + 2, z + dz, SLAB(M.slabLight), '柱头线脚');
      b.override(4, G.ySpring + 2, z + dz, SLAB(M.slabLight), '柱头线脚');
    }
  }
  // 拱廊中列柱柱脚
  for (const z of G.zPier) for (let dz = 0; dz <= 1; dz++) {
    for (let x = 11; x <= 13; x++) b.override(x, G.yGround, z + dz, M.plinthDark, '柱脚');
  }

  // ---------- 2.3 檐口与屋脊收口 ----------
  for (let z = -2; z <= 46; z++) {
    b.override(6, G.yWallTop, z, SLAB(M.slabLight), '檐口线脚');
    b.override(25, G.yWallTop, z, SLAB(M.slabLight), '檐口线脚');
  }
  // 山墙压顶（阶梯顶面，仅在该格确有山墙砌体时加）
  for (let z = 0; z <= 1; z++) for (let x = 6; x <= 24; x++) {
    const cur = b.get(x, G.yGableTop, z);
    if (cur && cur !== AIR) b.override(x, G.yGableTop + 1, z, SLAB(M.slabTile), '山墙压顶');
  }

  // ---------- 2.4 排水：檐沟与落水管（有明确去向） ----------
  for (let z = 0; z <= 44; z++) b.override(6, G.yWallTop - 1, z, trapdoor('north', 'bottom', 'false'), '檐沟示意');
  // 落水管：南墙两端与中部（3 处，对应屋面汇水）
  for (const z of [1, 22, 43]) {
    for (let y = G.yGround + 1; y <= G.yWallTop - 1; y++) b.override(5, y, z, S('minecraft:iron_chain', { axis: 'y' }), '落水管');
    b.override(5, G.yGround, z, M.plinthDark, '落水口');
    b.override(4, G.yGround, z, M.paving, '散水');
  }
  // 屋脊端头收口（避免锐利断口）
  for (const z of [-2, 46]) for (const x of [12, 13]) b.override(x, G.yRidge + 1, z, SLAB(M.slabTile), '屋脊端头');

  // ---------- 2.5 转角与门窗洞口线脚 ----------
  // 建筑四角做隅石（Quoins）——只在真正的转角
  for (const [x, z, dx, dz] of [[6, 0, 0, 1], [24, 0, 0, 1], [6, 44, 0, -1], [24, 44, 0, -1]]) {
    void dx;
    for (let y = G.yGround + 2; y <= G.yWallTop; y += 3) {
      b.override(x, y, z, M.light, '隅石');
      b.override(x, y, z + dz, M.light, '隅石');
    }
  }
  // 门廊角部与门套加线脚
  for (let y = G.yGround + 1; y <= G.yDeckTop + 1; y += 3) {
    b.override(0, y, -9, M.light, '门廊隅石');
    b.override(8, y, -9, M.light, '门廊隅石');
  }

  return b;
}

// ============================================================================
// Pass 3｜Material / Environmental Finish（时间层、Detail Vegetation、Micro Ground）
// 时间层按"原因 + 位置 + 强度"分布：接地受潮、檐下滴水、人流踩踏、烟熏、维修差异。
// ============================================================================
export function passMaterial(b) {
  b.beginStage('F3-材质与环境');

  const hash = (x, y, z) => Math.abs(((x * 374761393) ^ (y * 668265263) ^ (z * 2246822519)) % 1000);

  // ---------- 3.1 受潮带：勒脚以上 1–2 格、背阴面（北侧）更强 ----------
  for (let z = 0; z <= 44; z++) {
    for (let y = G.yGround + 1; y <= G.yGround + 2; y++) {
      // 北墙（背阴、受水）——用深色砌块替换
      if (hash(18, y, z) < 380) b.override(18, y, z, M.plinthDark, '受潮带');
      if (hash(19, y, z) < 260) b.override(19, y, z, M.plinthDark, '受潮带');
      // 南墙（向阳、干燥）——只有零星
      if (hash(6, y, z) < 120) b.override(6, y, z, M.plinthDark, '受潮带');
    }
  }
  // ---------- 3.2 檐下滴水痕：檐口下 2 格、每 3–5 格一道（与落水管位置无关的雨水路径） ----------
  for (let z = 0; z <= 44; z++) {
    if (hash(0, 0, z) % 5 !== 0) continue;
    for (let y = G.yWallTop - 3; y <= G.yWallTop - 1; y++) {
      if (hash(6, y, z) < 500) b.override(6, y, z, M.plinth, '檐下滴水痕');
    }
  }
  // ---------- 3.3 人流踩踏：门槛、楼梯口、通道中线的铺地磨损（浅色石露底） ----------
  const worn = [
    [4, G.yGround, 20], [4, G.yGround, 21], [4, G.yGround, 22], [4, G.yGround, 23], [4, G.yGround, 24],
    [5, G.yGround, 22], [6, G.yGround, 22], [7, G.yGround, 22], [8, G.yGround, 22],
    [4, G.yGround, -4], [4, G.yGround, -3], [5, G.yGround, -2], [6, G.yGround, -2],
    [9, G.yGround, 9], [9, G.yGround, 8], [9, G.yGround, 7],
    [9, G.yGreatFloor, 3], [9, G.yGreatFloor, 4], [12, G.yGreatFloor, 8], [12, G.yGreatFloor, 20],
  ];
  for (const [x, y, z] of worn) b.override(x, y, z, M.pavingIn, '踩踏磨损');
  // ---------- 3.4 烟熏：厨房/铁匠相关处（北院灶位与过秤间灯下） ----------
  for (const [x, y, z] of [[22, G.yGround + 4, 32], [22, G.yGround + 3, 32], [21, G.yGround + 4, 25]]) {
    b.override(x, y, z, M.plinthDark, '烟熏');
  }
  // ---------- 3.5 维修差异：局部补砌（新砖色更亮），集中在 2–3 处，不做均匀分布 ----------
  for (const [x, z, h] of [[6, 30, 4], [18, 12, 3], [24, 20, 5]]) {
    for (let i = 0; i < h; i++) {
      if (hash(x, i, z) < 700) b.override(x, G.yGround + 2 + i, z, M.wall, '维修补砌');
    }
  }
  // ---------- 3.6 Detail Vegetation / Micro Ground ----------
  // 建筑北侧排水沟边：苔藓与杂草（阴湿处，成带状而非均匀撒点；不得侵占拱廊通行带 x=3..5）
  for (let z = -2; z <= 50; z++) {
    if (hash(0, 1, z) % 4 !== 0) continue;
    b.override(1, G.yStreet + 1, z, moss(), '沟边苔藓');
  }
  for (let z = 0; z <= 44; z++) {
    if (hash(1, 1, z) % 7 !== 0) continue;
    b.override(0, G.yStreet + 1, z, shortGrass(), '台基边草');
  }
  // 台基与广场交界处：碎石与土（踩踏边缘）
  for (let z = -1; z <= 45; z++) {
    if (hash(2, 2, z) % 9 !== 0) continue;
    b.override(0, G.yStreet, z, M.rubble, '边缘碎石');
  }
  // 北院水井旁：湿土与蕨（用水点附近的植被）
  for (const [x, z] of [[32, 10], [35, 13], [32, 14], [36, 10]]) {
    b.override(x, G.yStreet, z, M.cobbleC, '井边湿地');
    b.override(x, G.yStreet + 1, z, fern(), '井边蕨');
  }
  // 建筑墙脚边缘（x=6 一侧）：少量草丛，不侵占 x=5 的拱廊通行带
  for (let z = 0; z <= 44; z += 1) {
    if (hash(3, 3, z) % 11 !== 0) continue;
    b.override(2, G.yStreet + 1, z, S('minecraft:tall_grass', { half: 'lower' }), '沟边草');
    b.override(2, G.yStreet + 2, z, S('minecraft:tall_grass', { half: 'upper' }), '沟边草');
  }

  return b;
}

// ============================================================================
// Pass 4｜Composition / Atmosphere（视觉主次、光暗、节奏、空间气氛）
// ============================================================================
export function passComposition(b) {
  b.beginStage('F4-构图与氛围');

  // ---------- 4.1 光：按功能照度与路线识别布光，不按格距插火把 ----------
  // 拱廊：只在开间中段悬挂灯笼（每开间 1 盏，形成柱列节奏的光节拍）
  for (let i = 0; i < G.zPier.length - 1; i++) {
    const zc = G.zPier[i] + 3;
    b.override(4, G.ySpring + 2, zc, lanternH('true'), '拱廊吊灯');
  }
  // 交易厅：沿中列柱两侧（墩间）布置，光随结构走
  for (const z of [3, 9, 15, 21, 27, 33, 39]) {
    b.override(11, G.ySpring + 3, z, lanternH('true'), '交易厅吊灯');
    if (z % 2 === 1) b.override(13, G.ySpring + 3, z + 1, lanternH('true'), '交易厅吊灯');
  }
  // 上层大厅：Focal —— 大厅东端（议事与集会的主位）光更密；西端 Quiet 只留基本照度
  for (const z of [30, 34, 38]) b.override(14, G.yGreatFloor + 5, z, lanternH('true'), '大厅主灯');
  for (const z of [10, 18, 26]) b.override(14, G.yGreatFloor + 5, z, lanternH('true'), '大厅灯');
  b.override(10, G.yGreatFloor + 5, 40, lanternH('true'), '大厅灯');
  b.override(18, G.yGreatFloor + 5, 6, lanternH('true'), '大厅灯');
  // 上层前厅（楼梯口）——路线识别
  b.override(9, G.yGreatFloor + 3, 2, lanternH('true'), '前厅灯');
  // 门廊：入口 Focal —— 门两侧壁灯 + 顶部吊灯
  b.override(2, G.yGround + 3, -8, torch('south'), '门廊壁灯');
  b.override(6, G.yGround + 3, -8, torch('south'), '门廊壁灯');
  b.override(4, G.yDeckTop, -5, lanternH('true'), '门廊吊灯');
  // 后勤翼与地窖：够用即可（Quiet，但必须可用）
  for (const z of [12, 24, 36]) b.override(22, G.yDeck - 1, z, lanternH('true'), '后勤灯');
  b.override(21, G.yGround + 3, 6, lanternH('true'), '看守灯');

  // ---------- 4.2 主次：入口与山墙的视觉权重 ----------
  // 主入口上方：市徽浮雕（几何化的浅浮雕，凸出 1 格）
  const gx = 6;
  const emblem = [
    [0, 2, 1, 2], [1, 1, 1, 4], [2, 0, 1, 6], [3, 0, 1, 6], [4, 0, 1, 6], [5, 1, 1, 4], [6, 2, 1, 2],
  ];
  for (const [dx, dy, w, h] of emblem) {
    for (let x = 0; x < w; x++) for (let y = 0; y < h; y++) {
      b.override(gx - 1, G.yGround + 6 + dy + y, -9 + 2 + dx + x, M.light, '市徽浮雕');
    }
  }
  // 山墙中央：绿釉砖饰带（对应 R3 记载的"不同颜色砖砌成的展示墙"）
  for (let y = G.yWallTop + 2; y <= G.yGableTop - 1; y += 4) {
    for (let x = 8; x <= 22; x++) {
      const zz = [0, 1];
      for (const z of zz) if (b.get(x, y, z) !== undefined) b.override(x, y, z, M.glazed, '山墙釉砖饰带');
    }
  }

  return b;
}

// ============================================================================
// Pass 5｜Restraint（删除冗余、重复、抢戏或破坏空间关系的细节）
// Restraint 的目标是删除噪声，不是把必要的完成度一起删掉。
// ============================================================================
export function passRestraint(b) {
  b.beginStage('F5-Restraint');
  const removed = { 摊位重复: 0, 灯过量: 0, 杂草过量: 0 };
  // 5.1 摊位：7 档 × 2 跨 = 14 组，后半段（z≥34）减半——避免机械重复
  for (const z of [34, 40]) {
    for (const x of [9, 15]) {
      if (b.get(x, G.yGround, z) === barrel('up')) { b.override(x, G.yGround, z, M.paving, 'Restraint:减摊位'); removed.摊位重复++; }
      if (b.get(x, G.yGround, z + 1) === barrel('up')) { b.override(x, G.yGround, z + 1, M.paving, 'Restraint:减摊位'); removed.摊位重复++; }
    }
  }
  // 5.2 大厅灯：把西端（Quiet 区）的重复灯删掉，保留东端 Focal 密度
  for (const z of [10, 26]) {
    if (b.get(14, G.yGreatFloor + 5, z) === lanternH('true')) { b.override(14, G.yGreatFloor + 5, z, AIR, 'Restraint:减灯'); removed.灯过量++; }
  }
  // 5.3 交易厅吊灯：隔一个删一个，减少机械感
  for (const z of [9, 21, 33]) {
    if (b.get(11, G.ySpring + 3, z) === lanternH('true')) { b.override(11, G.ySpring + 3, z, AIR, 'Restraint:减灯'); removed.灯过量++; }
  }
  // 5.4 广场边草：删掉靠近主入口的一段（入口前应清空，保持礼仪性）
  for (let z = -6; z <= 6; z++) {
    const cur = b.get(5, G.yStreet + 1, z);
    if (cur && cur.includes('short_grass')) { b.override(5, G.yStreet + 1, z, AIR, 'Restraint:清入口'); removed.杂草过量++; }
    const up = b.get(5, G.yStreet + 2, z);
    if (up && up.includes('tall_grass')) { b.override(5, G.yStreet + 2, z, AIR, 'Restraint:清入口'); removed.杂草过量++; }
  }
  b.restraintLog = removed;
  return b;
}
