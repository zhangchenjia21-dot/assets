// 基线证据：把当前世界（应处于 SPATIAL_COMPLETE）快照为基线，并把 baseline/final 的
// 同机位视图并排比较所需的中间数据一并留档。
// 用法：node tools/基线.mjs  （在 Finishing 之前执行；Finishing 之后再执行视图证据.mjs final）
import fs from 'node:fs';
import path from 'node:path';
import { runJob, PROJECT, WORLD } from './执行器.mjs';

const outDir = path.join(PROJECT, 'evidence/baseline');
fs.mkdirSync(outDir, { recursive: true });

// 1) 只生成 Builder Core（不含 Finishing）的蓝本，作为 SPATIAL_COMPLETE 的语义基线记录
const { generateCore, CORE_STAGES } = await import('./蓝本.mjs');
const core = generateCore();
const coreRep = core.report();
fs.writeFileSync(path.join(outDir, 'core-baseline-report.json'), JSON.stringify({
  stage: 'SPATIAL_COMPLETE',
  captured_at: new Date().toISOString(),
  world_path: WORLD,
  core_stages: CORE_STAGES,
  blocks: coreRep.blocks,
  distinct_states: coreRep.distinctStates,
  bounds: coreRep.bounds,
  conflicts: coreRep.conflicts,
  stages: coreRep.stages,
}, null, 1));
console.log('Core 基线: ' + coreRep.blocks + ' 方块 / ' + coreRep.distinctStates + ' 状态');

// 2) 冻结 Core 语义的关键边界（Space Graph edges / roofline / major route），供 Finishing 后复核
const b = core;
const at = (x, y, z) => (b.get(x, y, z) || 'air');
const frozen = {
  // 关键 Space Graph edges：两端必须是空气（可通行）
  '拱廊中门(x=6..7,z=26)': [[6, 1, 26], [7, 1, 26], [6, 3, 26]],
  '交易厅北门(x=18..19,z=26)': [[18, 1, 26], [19, 1, 26]],
  '后勤外门(x=23..24,z=13)': [[24, 1, 13]],
  '主楼梯井(x=9,z=6)': [[9, 4, 6], [9, 5, 6], [9, 6, 6]],
  '大厅入口(x=6..7,z=3..4,y=7)': [[6, 7, 3], [7, 7, 3]],
  '地窖井口(x=9,z=32)': [[9, 1, 32], [9, 2, 32]],
  // 关键结构：屋面轮廓点
  '屋脊(x=12..13,y=30,z=22)': [[12, 30, 22], [13, 30, 22]],
  '檐口(x=6,y=17,z=22)': [[6, 17, 22]],
  // 主入口门槛
  '门廊门槛(x=3..5,z=-9..-8,y=1)': [[3, 1, -8], [4, 1, -8], [5, 1, -8]],
};
const frozenState = {};
let openEdges = 0, totalEdges = 0;
for (const [name, cells] of Object.entries(frozen)) {
  frozenState[name] = cells.map(([x, y, z]) => {
    const st = at(x, y, z);
    if (name.startsWith('拱廊') || name.startsWith('交易厅') || name.startsWith('后勤') || name.startsWith('主楼梯') || name.startsWith('大厅入口') || name.startsWith('地窖') || name.startsWith('门廊')) {
      totalEdges++;
      if (st === 'air') openEdges++;
    }
    return { pos: [x, y, z], state: st };
  });
}
fs.writeFileSync(path.join(outDir, 'frozen-core-baseline.json'), JSON.stringify({
  note: 'Phase Protection 基线：Finishing 不得改变这些 Frozen Core 语义',
  frozen_stages: ['Program / Space Graph', '主体量', '主要 Plan / Section', '主屋顶体系', '主入口与主要 Circulation', '大地形', '核心 skyline'],
  edges_open: openEdges, edges_total: totalEdges,
  frozen: frozenState,
}, null, 1));
console.log('关键边可通行: ' + openEdges + '/' + totalEdges + '（其余为结构点，记录状态供复核）');
console.log('基线文件: evidence/baseline/');
