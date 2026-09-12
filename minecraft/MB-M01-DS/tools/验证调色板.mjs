// 调色板验证（第 1 步）：在本执行器自建的一次性世界中批量放置候选方块状态。
// 不设置 samples 断言——因为 Minecraft 会对楼梯/墙/栅栏/栅栏门做自动连接规范化，
// 断言只会掩盖真实结果。改为把 world 全文扫描（RLE）作为权威观测，供第 2 步解码。
import fs from 'node:fs';
import path from 'node:path';
import { Builder, S } from './几何核心.mjs';
import { runJob, PROJECT } from './执行器.mjs';

const TEST_WORLD = path.join(PROJECT, 'jobs/_调色板测试世界');
const SCHEMA = JSON.parse(fs.readFileSync(path.join(PROJECT, 'research/blocks_schema.json'), 'utf8'));

const FAMILIES = `cinnabar_bricks mud_bricks bricks resin_bricks sulfur_bricks
cinnabar_brick_stairs mud_brick_stairs brick_stairs cinnabar_brick_slab mud_brick_slab brick_slab
cinnabar_brick_wall mud_brick_wall brick_wall cinnabar_slab cinnabar_stairs cinnabar_wall
polished_deepslate deepslate_bricks deepslate_tiles chiseled_deepslate cobbled_deepslate
deepslate_tile_stairs deepslate_brick_stairs polished_deepslate_stairs
deepslate_tile_slab deepslate_brick_slab polished_deepslate_slab
deepslate_tile_wall deepslate_brick_wall polished_deepslate_wall cobbled_deepslate_wall
cracked_deepslate_bricks cracked_deepslate_tiles cobbled_deepslate_stairs cobbled_deepslate_slab
diorite polished_diorite polished_diorite_stairs polished_diorite_slab diorite_wall
calcite quartz_block smooth_quartz chiseled_quartz_block smooth_quartz_stairs smooth_quartz_slab quartz_slab quartz_stairs
polished_tuff tuff_bricks tuff polished_tuff_stairs polished_tuff_slab tuff_brick_stairs polished_tuff_wall tuff_brick_wall
stone stone_bricks smooth_stone smooth_stone_slab stone_slab stone_stairs stone_brick_stairs stone_brick_slab
chiseled_stone_bricks cracked_stone_bricks mossy_stone_bricks andesite polished_andesite gravel
dark_oak_planks stripped_dark_oak_log dark_oak_log dark_oak_wood dark_oak_stairs dark_oak_slab dark_oak_fence dark_oak_fence_gate
spruce_planks stripped_spruce_log spruce_stairs spruce_slab spruce_fence
glass glass_pane iron_bars iron_chain iron_block iron_trapdoor
oak_planks oak_stairs oak_slab oak_fence oak_fence_gate oak_log
mangrove_planks mangrove_stairs mangrove_slab
red_nether_bricks nether_bricks polished_blackstone_bricks blackstone brick_wall
moss_block moss_carpet dirt coarse_dirt dirt_path clay sand red_sand
short_grass fern tall_grass large_fern
white_wool brown_wool red_wool gray_wool red_carpet white_carpet brown_carpet
oak_leaves spruce_leaves dark_oak_leaves
hay_block scaffolding ladder
oak_door spruce_door dark_oak_door iron_door oak_trapdoor spruce_trapdoor dark_oak_trapdoor
berry`.split(/\s+/).filter((x) => x && x !== 'berry').map((f) => 'minecraft:' + f);

const EXPLICIT = [
  ['minecraft:oak_door', { facing: ['north', 'south', 'east', 'west'], half: ['lower', 'upper'], hinge: ['left', 'right'], open: ['false'] }],
  ['minecraft:iron_door', { facing: ['north', 'south', 'east', 'west'], half: ['lower', 'upper'], hinge: ['left', 'right'], open: ['false'] }],
  ['minecraft:spruce_door', { facing: ['north', 'south', 'east', 'west'], half: ['lower', 'upper'], hinge: ['left', 'right'], open: ['false'] }],
  ['minecraft:dark_oak_door', { facing: ['north', 'south', 'east', 'west'], half: ['lower', 'upper'], hinge: ['left', 'right'], open: ['false'] }],
  ['minecraft:dark_oak_trapdoor', { facing: ['north', 'south', 'east', 'west'], half: ['top', 'bottom'], open: ['false', 'true'] }],
  ['minecraft:spruce_trapdoor', { facing: ['north', 'south', 'east', 'west'], half: ['top', 'bottom'], open: ['false', 'true'] }],
  ['minecraft:iron_trapdoor', { facing: ['north', 'south', 'east', 'west'], half: ['top', 'bottom'], open: ['false', 'true'] }],
  ['minecraft:lantern', { hanging: ['false', 'true'] }],
  ['minecraft:campfire', { facing: ['north', 'south', 'east', 'west'], lit: ['false', 'true'] }],
  ['minecraft:barrel', { facing: ['up', 'down', 'north', 'south', 'east', 'west'], open: ['false'] }],
  ['minecraft:chest', { facing: ['north', 'south', 'east', 'west'], type: ['single'], waterlogged: ['false'] }],
  ['minecraft:lectern', { facing: ['north', 'south', 'east', 'west'] }],
  ['minecraft:bell', { attachment: ['floor', 'ceiling', 'single_wall'], facing: ['north', 'south', 'east', 'west'] }],
  ['minecraft:spruce_wall_sign', { facing: ['north', 'south', 'east', 'west'] }],
  ['minecraft:oak_wall_sign', { facing: ['north', 'south', 'east', 'west'] }],
  ['minecraft:red_wall_banner', { facing: ['north', 'south', 'east', 'west'] }],
  ['minecraft:spruce_wall_hanging_sign', { facing: ['north', 'south', 'east', 'west'] }],
  ['minecraft:ladder', { facing: ['north', 'south', 'east', 'west'] }],
  ['minecraft:iron_chain', { axis: ['x', 'y', 'z'] }],
  ['minecraft:candle', { candles: ['1', '2', '3', '4'], lit: ['false', 'true'] }],
  ['minecraft:torch', {}],
  ['minecraft:wall_torch', { facing: ['north', 'south', 'east', 'west'] }],
  ['minecraft:soul_lantern', { hanging: ['false', 'true'] }],
  ['minecraft:furnace', { facing: ['north', 'south', 'east', 'west'], lit: ['false'] }],
  ['minecraft:blast_furnace', { facing: ['north', 'south', 'east', 'west'], lit: ['false'] }],
  ['minecraft:smoker', { facing: ['north', 'south', 'east', 'west'], lit: ['false'] }],
  ['minecraft:cauldron', {}],
  ['minecraft:hay_block', { axis: ['x', 'y', 'z'] }],
  ['minecraft:smithing_table', {}],
  ['minecraft:stonecutter', { facing: ['north', 'south', 'east', 'west'] }],
  ['minecraft:grindstone', { face: ['floor', 'wall', 'ceiling'], facing: ['north', 'south', 'east', 'west'] }],
  ['minecraft:loom', { facing: ['north', 'south', 'east', 'west'] }],
  ['minecraft:cartography_table', {}],
  ['minecraft:anvil', { facing: ['north', 'south', 'east', 'west'] }],
  ['minecraft:trapped_chest', { facing: ['north', 'south', 'east', 'west'], type: ['single'], waterlogged: ['false'] }],
  ['minecraft:white_candle', { candles: ['1', '2', '3', '4'], lit: ['false', 'true'] }],
  ['minecraft:bookshelf', {}],
  ['minecraft:flower_pot', {}],
  ['minecraft:potted_fern', {}],
  ['minecraft:potted_oak_sapling', {}],
  ['minecraft:vine', { north: ['false'], east: ['false'], south: ['false'], west: ['false'], up: ['false'] }],
  ['minecraft:white_stained_glass_pane', { north: ['false'], east: ['false'], south: ['false'], west: ['false'], waterlogged: ['false'] }],
  ['minecraft:gray_stained_glass_pane', { north: ['false'], east: ['false'], south: ['false'], west: ['false'], waterlogged: ['false'] }],
];

const familyStates = [];
for (const b of FAMILIES) {
  const def = SCHEMA[b];
  if (!def) { console.error('缺少 schema: ' + b); continue; }
  const keys = Object.keys(def.properties);
  if (keys.length === 0) { familyStates.push([b, {}]); continue; }
  const acc = {};
  const walk = (i) => {
    if (i === keys.length) { familyStates.push([b, { ...acc }]); return; }
    for (const v of def.properties[keys[i]]) { acc[keys[i]] = v; walk(i + 1); }
  };
  walk(0);
}
const explicitStates = [];
for (const [b, props] of EXPLICIT) {
  const def = SCHEMA[b];
  if (!def) { console.error('缺少 schema: ' + b); continue; }
  const keys = Object.keys(props);
  const acc = {};
  const walk = (i) => {
    if (i === keys.length) { explicitStates.push([b, { ...acc }]); return; }
    for (const v of props[keys[i]]) { acc[keys[i]] = v; walk(i + 1); }
  };
  walk(0);
}

// 策略预筛
const POLICY = JSON.parse(fs.readFileSync('D:/Games/Minecraft/AI工程/AI-Offline/state/base-entity-policy.json', 'utf8'));
const verified = new Set(POLICY.verified_states);
const ENTITY_LIKE = /(_sign|_banner|shelf|bookshelf|lectern|chest|barrel|furnace|smoker|blast_furnace|campfire|bell|brewing_stand|hopper|dispenser|enchanting_table)$/;
const runnable = [];
const skipped = [];
for (const [block, props] of [...familyStates, ...explicitStates]) {
  let st;
  try { st = S(block, props); } catch (e) { skipped.push({ block, props, reason: e.message }); continue; }
  if (ENTITY_LIKE.test(block) && !verified.has(st)) { skipped.push({ block, props, reason: 'POLICY_NOT_VERIFIED', state: st }); continue; }
  runnable.push([block, props, st]);
}
console.log('可施工候选: ' + runnable.length + '  排除: ' + skipped.length);

const b = new Builder('调色板验证');
const COLS = 40;
const cellFor = new Map();
runnable.forEach(([block, props, st], i) => {
  const cx = (i % COLS) * 4;
  const cz = Math.floor(i / COLS) * 4;
  b.box(cx, 69, cz, cx + 1, 69, cz + 1, 'minecraft:deepslate_tiles');
  b.set(cx, 70, cz, st);
  cellFor.set(`${cx},${70},${cz}`, { block, props, intended: st });
});
const rep = b.report();
const rows = Math.ceil(runnable.length / COLS);
const scan = { x1: -1, y1: 68, z1: -1, x2: COLS * 4 + 1, y2: 71, z2: rows * 4 + 1 };
console.log('网格: ' + COLS + '×' + rows + '  方块数=' + rep.blocks + '  冲突=' + rep.conflicts + '  状态种类=' + rep.distinctStates);

const { result, stamp, jobDirectory } = runJob(
  { create: { type: 'superflat', seed: 20260912 }, phases: [b.phases()], scan },
  { label: '调色板验证', worldPath: TEST_WORLD }
);
console.log('作业 ' + stamp + '  status=' + result.status + '  不符=' + result.mismatches + '  写入=' + result.changed_blocks + '  耗时=' + Math.round(result.wall_seconds) + 's');
fs.writeFileSync(path.join(PROJECT, `jobs/_调色板网格-${stamp}.json`), JSON.stringify({
  stamp, job_directory: jobDirectory, scan: result.scan, cells: [...cellFor.entries()], skipped: skipped.map((s) => s.state || s.reason)
}));
console.log('已保存网格证据 jobs/_调色板网格-' + stamp + '.json');
