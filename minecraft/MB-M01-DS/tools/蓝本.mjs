// 蓝色方案装配：把各施工阶段按 v1.10 §29 的 Macro→Meso→Base Micro 顺序串起来。
import { Builder } from './几何核心.mjs';
import { stageSite, stageCellar, stageGround, stageFloor, stageUpper, stageRoof, stageTower, stageCirculation } from './建筑生成器.mjs';
import { passFunctional, passArchitectural, passMaterial, passComposition, passRestraint } from './精修.mjs';

export const CORE_STAGES = [
  'S1-场地与台基',
  'S2-地窖',
  'S3-交易层',
  'S4-楼板与披檐',
  'S5-上层大厅',
  'S6-屋面',
  'S7-屋脊钟塔',
  'S8-开口与主楼梯',
];

export const FINISH_STAGES = ['F1-功能精修', 'F2-建筑收口', 'F3-材质与环境', 'F4-构图与氛围', 'F5-Restraint'];

export const STAGES = [...CORE_STAGES, ...FINISH_STAGES];

/** 生成到 SPATIAL_COMPLETE 的 Builder Core 蓝本（Finishing 前基线）。 */
export function generateCore() {
  const b = new Builder('Rathaus und Kaufhaus Wiethmar');
  stageSite(b);
  stageCellar(b);
  stageGround(b);
  stageFloor(b);
  stageUpper(b);
  stageRoof(b);
  stageTower(b);
  stageCirculation(b);
  return b;
}

/** 生成完整蓝本：Core + Finishing（Five Passes，含 Restraint）。 */
export function generateBlueprint() {
  const b = generateCore();
  passFunctional(b);
  passArchitectural(b);
  passMaterial(b);
  passComposition(b);
  passRestraint(b);
  return b;
}

/** 只生成到指定阶段（用于基线存档与分阶段施工）。 */
export function generateThrough(lastStage) {
  const b = new Builder('Rathaus und Kaufhaus Wiethmar');
  if (CORE_STAGES.includes(lastStage)) {
    stageSite(b); stageCellar(b); stageGround(b); stageFloor(b); stageUpper(b); stageRoof(b); stageTower(b);
    if (lastStage === 'S8-开口与主楼梯' || CORE_STAGES.indexOf(lastStage) >= CORE_STAGES.indexOf('S8-开口与主楼梯')) stageCirculation(b);
    return b;
  }
  generateCore(b);
  for (const s of FINISH_STAGES) {
    if (s === 'F1-功能精修') passFunctional(b);
    if (s === 'F2-建筑收口') passArchitectural(b);
    if (s === 'F3-材质与环境') passMaterial(b);
    if (s === 'F4-构图与氛围') passComposition(b);
    if (s === 'F5-Restraint') passRestraint(b);
    if (s === lastStage) break;
  }
  return b;
}
