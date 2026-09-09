/**
 * 步骤9b 动线修补（终验发现的两处断点）：
 *   1) 石舫跳板：步骤9 灯笼误置跳板通行格 (-92,64,10) → 移除，迁至西侧岸石 (-94,64,10)；
 *   2) 山洞洞口：z48 头顶层悬岩 (-109,64,48) 未凿 + 洞口灯笼 (-109,64,49) 堵头
 *      → 凿开岩面、灯笼迁至廊旁草地 (-111,64,47)。
 * 仅 6 格改动，修后重跑 10c 扫描供终验复核。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { 作业, M } from './园林库.mjs';

const 根 = path.dirname(fileURLToPath(import.meta.url));
const 世界 = 'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/苏州园林贰';
const J = new 作业();

// ── 石舫跳板 ──
J.放(-92, 64, 10, 'minecraft:air');   // 移除堵路灯笼
J.放(-94, 64, 10, M.灯);              // 迁至西侧岸石（y63 stone 承托）

// ── 山洞洞口 ──
J.放(-109, 64, 48, 'minecraft:air');  // 凿开洞口头顶悬岩
J.放(-109, 64, 49, 'minecraft:air');  // 移除洞口堵头灯笼
J.放(-111, 64, 47, M.灯);             // 迁至短廊旁草地（y63 grass 承托）

const samples = [
  [-92, 64, 10, 'minecraft:air'],                            // 跳板通行格已净
  [-94, 64, 10, M.灯],                                       // 迁至岸石
  [-92, 63, 13, 'minecraft:stone_slab[type=bottom,waterlogged=false]'], // 跳板本体未动
  [-109, 64, 48, 'minecraft:air'],                           // 洞口已通
  [-109, 64, 49, 'minecraft:air'],                           // 洞口灯已拆
  [-111, 64, 47, M.灯],                                      // 迁至廊旁
  [-109, 64, 50, 'minecraft:air'],                           // 隧道本体未动
  [-109, 64, 60, 'minecraft:air'],                           // 内室未动
];
J.校对(samples);

const 出 = path.join(根, '..', '施工', '步骤9b.json');
fs.writeFileSync(出, JSON.stringify({ world_path: 世界, phases: [J.阶段()], samples }, null, 2));
console.log('已生成', 出, '操作数', J.operations.length);
