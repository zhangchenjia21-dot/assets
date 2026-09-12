// 施工几何核心库（minecraft-builder v1.10 的 Builder Core 实现层）
// 设计约束：
//  - 只负责把"已成立的空间/剖面/结构意图"转成方块；不做风格贴皮。
//  - 每个坐标只能被写入一次；重复写入不同方块即视为几何冲突（防止旧结构残留）。
//  - 所有状态字符串都按 26.2 原生 schema 生成，避免属性顺序或取值错误。
import fs from 'node:fs';
import path from 'node:path';

const SCHEMA = JSON.parse(
  fs.readFileSync(new URL('../research/blocks_schema.json', import.meta.url), 'utf8')
);

/** 规范状态字符串：按 schema 中的属性顺序输出。 */
export function S(block, props = {}) {
  const name = block.startsWith('minecraft:') ? block : 'minecraft:' + block;
  const def = SCHEMA[name];
  if (!def) throw new Error('UNKNOWN_BLOCK: ' + name);
  const keys = Object.keys(def.properties);
  if (keys.length === 0) return name;
  const parts = [];
  for (const k of keys) {
    const v = props[k] !== undefined ? String(props[k]) : null;
    if (v === null) {
      // 未指定：若该属性取值唯一则自动补全，否则报错（不猜测状态）
      const vals = def.properties[k];
      if (vals.length === 1) {
        parts.push(`${k}=${vals[0]}`);
        continue;
      }
      throw new Error(`MISSING_PROPERTY: ${name} needs ${k} (values: ${vals.join('|')})`);
    }
    const vals = def.properties[k];
    if (!vals.includes(v)) throw new Error(`BAD_PROPERTY_VALUE: ${name} ${k}=${v} (values: ${vals.join('|')})`);
    parts.push(`${k}=${v}`);
  }
  for (const k of Object.keys(props)) if (!keys.includes(k)) throw new Error(`UNKNOWN_PROPERTY: ${name}.${k}`);
  return `${name}[${parts.join(',')}]`;
}

export const AIR = 'minecraft:air';

/** 依据调色板验证证据，把请求状态映射为 Minecraft 实际生效状态（含 waterlogged 等自动补全）。 */
let PALETTE_MAP = null;
export function normState(state) {
  if (PALETTE_MAP === null) {
    try {
      const p = JSON.parse(fs.readFileSync(new URL('../research/palette.json', import.meta.url), 'utf8'));
      PALETTE_MAP = new Map(Object.entries(p.mapping));
    } catch { PALETTE_MAP = new Map(); }
  }
  return PALETTE_MAP.get(state) || state;
}

/** 规范化状态字符串：按字母序排列属性，便于与世界回读结果逐字比较。 */
export function canonical(state) {
  const i = state.indexOf('[');
  if (i < 0) return state;
  const name = state.slice(0, i);
  const props = state.slice(i + 1, -1).split(',').sort();
  return name + '[' + props.join(',') + ']';
}

/** 朝向工具：给定水平方向名，返回楼梯/门等需要的 facing。 */
export const DIRS = ['north', 'east', 'south', 'west'];

export class Builder {
  constructor(name) {
    this.name = name;
    /** @type {Map<string,string>} 坐标 -> 状态字符串 */
    this.cells = new Map();
    /** @type {Map<string,string>} 坐标 -> 最后定义它的阶段名 */
    this.owner = new Map();
    this.conflicts = [];
    this.overrides = [];
    this.paintOver = [];
    this.stage = 'unnamed';
    this.stageLog = new Map();
  }
  static key(x, y, z) {
    return x + ',' + y + ',' + z;
  }
  /** 进入一个施工阶段；后续写入都归属该阶段。 */
  beginStage(name) {
    this.stage = name;
    if (!this.stageLog.has(name)) this.stageLog.set(name, 0);
    return this;
  }
  _record(x, y, z) {
    const st = this.cells.get(Builder.key(x, y, z));
    if (typeof st !== 'string' || st.length === 0) {
      throw new Error(`INVALID_STATE: ${this.stage} @ ${x},${y},${z} = ${JSON.stringify(st)}`);
    }
    this.stageLog.set(this.stage, (this.stageLog.get(this.stage) || 0) + 1);
    this.owner.set(Builder.key(x, y, z), this.stage);
  }
  /** 写入一个方块；写空气表示显式清除。同一坐标二次写入不同状态会被记为冲突（供审查）。 */
  set(x, y, z, state) {
    x = Math.round(x); y = Math.round(y); z = Math.round(z);
    const k = Builder.key(x, y, z);
    const prev = this.cells.get(k);
    if (prev !== undefined && prev !== state && prev !== AIR) {
      this.conflicts.push({ stage: this.stage, pos: [x, y, z], from: prev, to: state });
      return this;
    }
    this.cells.set(k, state);
    this._record(x, y, z);
    return this;
  }
  /**
   * 分层绘制（paint）：用于"同一体量按构造分层"的有意叠加（基槽→勒脚→面层）。
   * 与 override 的区别：paint 只记录"覆盖了本层已绘制格子"的次数，用于发现真正写乱的层。
   */
  paint(x, y, z, state, layer = '') {
    x = Math.round(x); y = Math.round(y); z = Math.round(z);
    const k = Builder.key(x, y, z);
    const prev = this.cells.get(k);
    if (prev !== undefined && prev !== state) {
      this.paintOver.push({ stage: this.stage, layer, pos: [x, y, z], from: prev, to: state });
    }
    this.cells.set(k, state);
    this._record(x, y, z);
    return this;
  }

  /** 显式覆盖：用于"在已成立体量上开洞/改造"这类有意为之的二次写入（带理由）。 */
  override(x, y, z, state, reason = '') {
    x = Math.round(x); y = Math.round(y); z = Math.round(z);
    const k = Builder.key(x, y, z);
    const prev = this.cells.get(k);
    if (prev !== undefined && prev !== state && prev !== AIR) this.overrides.push({ stage: this.stage, pos: [x, y, z], from: prev, to: state, reason });
    this.cells.set(k, state);
    this._record(x, y, z);
    return this;
  }
  get(x, y, z) {
    return this.cells.get(Builder.key(Math.round(x), Math.round(y), Math.round(z)));
  }
  /**
   * 实心长方体（含端点）。默认走 paint（分层绘制），因为大体积施工中
   * "墙与墙在转角相遇"属于正常构造，应计入 paintOver 而不是 conflicts。
   * 需要严格唯一写入时用 boxStrict。
   */
  box(x1, y1, z1, x2, y2, z2, state) {
    const [ax, bx] = [Math.min(x1, x2), Math.max(x1, x2)];
    const [ay, by] = [Math.min(y1, y2), Math.max(y1, y2)];
    const [az, bz] = [Math.min(z1, z2), Math.max(z1, z2)];
    for (let x = ax; x <= bx; x++) for (let y = ay; y <= by; y++) for (let z = az; z <= bz; z++) this.paint(x, y, z, state);
    return this;
  }
  /** 严格写入长方体：任何二次写入都会被记为冲突，用于检查几何是否重叠。 */
  boxStrict(x1, y1, z1, x2, y2, z2, state) {
    const [ax, bx] = [Math.min(x1, x2), Math.max(x1, x2)];
    const [ay, by] = [Math.min(y1, y2), Math.max(y1, y2)];
    const [az, bz] = [Math.min(z1, z2), Math.max(z1, z2)];
    for (let x = ax; x <= bx; x++) for (let y = ay; y <= by; y++) for (let z = az; z <= bz; z++) this.set(x, y, z, state);
    return this;
  }
  /** 挖空（显式 air）。 */
  carve(x1, y1, z1, x2, y2, z2) {
    return this.box(x1, y1, z1, x2, y2, z2, AIR);
  }
  /** 空心盒：只做壳，不含内部。 */
  shell(x1, y1, z1, x2, y2, z2, state) {
    const [ax, bx] = [Math.min(x1, x2), Math.max(x1, x2)];
    const [ay, by] = [Math.min(y1, y2), Math.max(y1, y2)];
    const [az, bz] = [Math.min(z1, z2), Math.max(z1, z2)];
    for (let x = ax; x <= bx; x++) for (let y = ay; y <= by; y++) for (let z = az; z <= bz; z++) {
      if (x === ax || x === bx || y === ay || y === by || z === az || z === bz) this.set(x, y, z, state);
    }
    return this;
  }
  /** 水平板（一层楼板）：明确使用 (x1,z1)-(x2,z2) 平面范围 + 高度 y。 */
  plate(x1, z1, x2, z2, y, state) {
    return this.box(x1, y, z1, x2, y, z2, state);
  }
  /** 只有边框的水平环（用于加固轮廓），thickness 为环宽。 */
  ring(x1, z1, x2, z2, y, state, thickness = 1) {
    for (let t = 0; t < thickness; t++) {
      const ax = Math.min(x1, x2) + t, bx = Math.max(x1, x2) - t;
      const az = Math.min(z1, z2) + t, bz = Math.max(z1, z2) - t;
      if (ax > bx || az > bz) break;
      for (let x = ax; x <= bx; x++) { this.set(x, y, az, state); this.set(x, y, bz, state); }
      for (let z = az; z <= bz; z++) { this.set(ax, y, z, state); this.set(bx, y, z, state); }
    }
    return this;
  }

  /**
   * 半圆拱券（截面在给定平面内），逐列逼近曲线。
   * axis: 'x' 表示拱沿 x 方向跨越，拱脚在 x1 与 x2；'z' 类推。
   * fill: 拱上方与两侧砌体（spandrel）材质；voussoir: 拱券本身（楼梯方块）。
   * 返回实际占用的坐标，便于上层结构对齐。
   */
  arch({ axis, fixed, from, to, springY, rise, wallLow, wallHigh, fill, voussoir, thickness = 1, sideThickness = 0 }) {
    const span = to - from;
    const r = span / 2;
    const cx = from + r;
    const cy = springY + rise - r; // 圆心高度（半圆时 rise === r）
    const curveY = (t) => {
      const dx = t - cx;
      const inside = r * r - dx * dx;
      const y = cy + Math.sqrt(Math.max(0, inside));
      return Math.round(y);
    };
    const columns = [];
    for (let t = from; t <= to; t++) {
      const yc = curveY(t);
      columns.push([t, yc]);
    }
    for (let i = 0; i < columns.length; i++) {
      const [t, yc] = columns[i];
      const prevY = i > 0 ? columns[i - 1][1] : yc;
      const nextY = i < columns.length - 1 ? columns[i + 1][1] : yc;
      const slope = (nextY - prevY) / 2;
      // 拱下净空：从 springY 起挖到 yc-1
      for (let y = wallLow; y <= wallHigh; y++) {
        const at = (dx) => (axis === 'x' ? [dx, y, fixed] : [fixed, y, dx]);
        if (y < yc) {
          if (y >= springY) {
            const [X, Y, Z] = at(t);
            for (let k = 0; k < thickness; k++) {
              const p = axis === 'x' ? [X, Y, Z + k] : [X + k, Y, Z];
              this.set(p[0], p[1], p[2], AIR);
            }
          } else {
            for (let k = 0; k < thickness; k++) {
              const p = axis === 'x' ? [t, y, fixed + k] : [fixed + k, y, t];
              this.set(p[0], p[1], p[2], fill);
            }
          }
        } else if (y === yc) {
          // 拱券石：用楼梯方块表达曲线
          let facing, half;
          const positive = slope >= 0;
          if (axis === 'x') {
            facing = positive ? 'east' : 'west';
            half = slope > 0.4 ? 'bottom' : slope < -0.4 ? 'top' : 'bottom';
          } else {
            facing = positive ? 'south' : 'north';
            half = slope > 0.4 ? 'bottom' : slope < -0.4 ? 'top' : 'bottom';
          }
          const shape = Math.abs(slope) < 0.35 ? 'straight' : slope > 0 ? 'outer_left' : 'outer_right';
          const st = S(voussoir, { facing, half, shape });
          for (let k = 0; k < thickness; k++) {
            const p = axis === 'x' ? [t, y, fixed + k] : [fixed + k, y, t];
            this.set(p[0], p[1], p[2], st);
          }
        } else {
          for (let k = 0; k < thickness; k++) {
            const p = axis === 'x' ? [t, y, fixed + k] : [fixed + k, y, t];
            this.set(p[0], p[1], p[2], fill);
          }
        }
      }
      // 拱券两侧的墙垛（当 fixed 是墙厚而不是单层时）
      if (sideThickness > 0) {
        for (let s = 1; s <= sideThickness; s++) {
          for (let y = wallLow; y <= wallHigh; y++) {
            const p = axis === 'x' ? [t, y, fixed - s] : [fixed - s, y, t];
            if (y < springY) this.set(p[0], p[1], p[2], fill);
          }
        }
      }
    }
    return columns;
  }

  /**
   * 尖拱（两心拱）开口：给定宽度按 riseRatio 生成。
   * 只做"开口 + 券石"，砌体由调用方负责，便于在同一墙上连续开多个洞。
   */
  pointedOpening({ axis, fixed, from, to, sillY, springY, rise, state, voussoir, thickness = 1 }) {
    const span = to - from;
    const r = span / 2;
    const cx = from + r;
    const curveY = (t) => {
      const dx = t - cx;
      // 两心尖拱：以对侧拱脚为圆心
      const R = span * 1.0;
      const y = springY + Math.sqrt(Math.max(0, R * R - (t - (dx >= 0 ? from : to)) ** 2)) - Math.sqrt(Math.max(0, R * R - r * r));
      return Math.round(Math.min(y, springY + rise));
    };
    for (let t = from; t <= to; t++) {
      const yc = curveY(t);
      for (let y = sillY; y < yc; y++) {
        const p = axis === 'x' ? [t, y, fixed] : [fixed, y, t];
        for (let k = 0; k < thickness; k++) {
          const q = axis === 'x' ? [p[0], p[1], p[2] + k] : [p[0] + k, p[1], p[2]];
          this.set(q[0], q[1], q[2], AIR);
        }
      }
      if (voussoir) {
        const p = axis === 'x' ? [t, yc, fixed] : [fixed, yc, t];
        for (let k = 0; k < thickness; k++) {
          const q = axis === 'x' ? [p[0], p[1], p[2] + k] : [p[0] + k, p[1], p[2]];
          this.set(q[0], q[1], q[2], state || voussoir);
        }
      }
    }
  }

  /** 直跑楼梯：沿 dir 方向每前进 1 格升 1 格；宽 width。返回踏板坐标。 */
  stair({ dir, x, y, z, width, steps, tread, riser, slabBottom, slabDouble }) {
    const out = [];
    for (let i = 0; i < steps; i++) {
      const yy = y + i * riser;
      const pos = dir === 'north' ? [x, yy, z - i * tread]
        : dir === 'south' ? [x, yy, z + i * tread]
        : dir === 'east' ? [x + i * tread, yy, z]
        : [x - i * tread, yy, z];
      for (let w = 0; w < width; w++) {
        const px = dir === 'north' || dir === 'south' ? pos[0] + w : pos[0];
        const pz = dir === 'north' || dir === 'south' ? pos[2] : pos[2] + w;
        const st = riser === 0.5 ? (i % 2 === 0 ? slabBottom : slabDouble) : slabDouble;
        this.set(px, Math.round(yy), pz, st);
        out.push([px, Math.round(yy), pz]);
      }
    }
    return out;
  }

  /**
   * 两坡屋面：沿 z 为屋脊方向，跨度为 x1..x2，脊在 xMid。
   * 每层外扩 overhang 格，used 记录屋面覆盖。
   */
  gableRoof({ z1, z2, x1, x2, eaveY, ridgeY, overhangZ = 0, tile, ridgeCap, eaveEdge }) {
    const xMid = (x1 + x2) / 2;
    const halfSpan = (x2 - x1) / 2;
    const rise = ridgeY - eaveY;
    for (let y = eaveY; y <= ridgeY; y++) {
      const t = (y - eaveY) / rise;
      const inset = Math.round(halfSpan * t);
      const ax = x1 + inset, bx = x2 - inset;
      for (let x = ax; x <= bx; x++) {
        for (let z = z1 - overhangZ; z <= z2 + overhangZ; z++) {
          const isEaveCourse = y === eaveY;
          const isRidgeCourse = y === ridgeY;
          let st = tile;
          if (isRidgeCourse) st = ridgeCap;
          else if (isEaveCourse && eaveEdge && (z < z1 || z > z2)) st = eaveEdge;
          this.set(x, y, z, st);
        }
      }
    }
  }

  /** 阶梯山墙（Treppengiebel）：在 x 平面上的墙，沿 z 方向阶梯收分。 */
  steppedGable({ x1, x2, zFrom, zTo, baseY, topY, stepH, stepW, wall, coping, innerWall }) {
    for (let y = baseY; y <= topY; y++) {
      const k = Math.floor((y - baseY) / stepH);
      const inset = k * stepW;
      const a = zFrom + inset, b = zTo - inset;
      if (a > b) break;
      for (let z = a; z <= b; z++) {
        for (let x = x1; x <= x2; x++) {
          const isEdge = z === a || z === b;
          this.set(x, y, z, isEdge ? coping : (x === x1 || x === x2 ? wall : (innerWall || wall)));
        }
      }
    }
  }

  /** 出图：转换为 executor 的 phases（含大块合并以减小 JSON）。 */
  phases({ mergeBoxes = true, stages = null } = {}) {
    const byState = new Map();
    for (const [k, st] of this.cells) {
      if (stages && !stages.includes(this.owner.get(k))) continue;
      if (!byState.has(st)) byState.set(st, []);
      const [x, y, z] = k.split(',').map(Number);
      byState.get(st).push([x, y, z]);
    }
    const palette = [];
    const operations = [];
    for (const [st, list] of byState) {
      const idx = palette.length;
      palette.push(st);
      if (!mergeBoxes) {
        for (const [x, y, z] of list) operations.push([x, y, z, idx]);
        continue;
      }
      // 贪心合并同状态连续体块：先按 x 连续，再按 z 连续，再按 y 连续
      const set = new Set(list.map(([x, y, z]) => Builder.key(x, y, z)));
      const used = new Set();
      const sorted = list.slice().sort((a, b) => a[1] - b[1] || a[2] - b[2] || a[0] - b[0]);
      for (const [x, y, z] of sorted) {
        if (used.has(Builder.key(x, y, z))) continue;
        let x2 = x;
        while (set.has(Builder.key(x2 + 1, y, z)) && !used.has(Builder.key(x2 + 1, y, z))) x2++;
        let z2 = z;
        outer: while (true) {
          for (let xx = x; xx <= x2; xx++) {
            if (!set.has(Builder.key(xx, y, z2 + 1)) || used.has(Builder.key(xx, y, z2 + 1))) break outer;
          }
          z2++;
        }
        let y2 = y;
        outer2: while (true) {
          for (let xx = x; xx <= x2; xx++) for (let zz = z; zz <= z2; zz++) {
            if (!set.has(Builder.key(xx, y2 + 1, zz)) || used.has(Builder.key(xx, y2 + 1, zz))) break outer2;
          }
          y2++;
        }
        for (let xx = x; xx <= x2; xx++) for (let yy = y; yy <= y2; yy++) for (let zz = z; zz <= z2; zz++) used.add(Builder.key(xx, yy, zz));
        if (x === x2 && y === y2 && z === z2) operations.push([x, y, z, idx]);
        else operations.push([x, y, z, x2, y2, z2, idx]);
      }
    }
    return { palette, operations };
  }

  report() {
    const counts = new Map();
    for (const st of this.cells.values()) counts.set(st, (counts.get(st) || 0) + 1);
    const top = [...counts.entries()].sort((a, b) => b[1] - a[1]);
    let minY = Infinity, maxY = -Infinity, minX = Infinity, maxX = -Infinity, minZ = Infinity, maxZ = -Infinity;
    for (const k of this.cells.keys()) {
      const [x, y, z] = k.split(',').map(Number);
      minX = Math.min(minX, x); maxX = Math.max(maxX, x);
      minY = Math.min(minY, y); maxY = Math.max(maxY, y);
      minZ = Math.min(minZ, z); maxZ = Math.max(maxZ, z);
    }
    return {
      name: this.name,
      blocks: this.cells.size,
      conflicts: this.conflicts.length,
      overrides: this.overrides.length,
      paintOver: this.paintOver.length,
      overridesByReason: [...this.overrides.reduce((m, o) => m.set(o.reason || '(未标注)', (m.get(o.reason || '(未标注)') || 0) + 1), new Map())].sort((a, b) => b[1] - a[1]),
      paintOverByLayer: [...this.paintOver.reduce((m, o) => m.set(o.layer || '(未标注)', (m.get(o.layer || '(未标注)') || 0) + 1), new Map())].sort((a, b) => b[1] - a[1]),
      bounds: { minX, maxX, minY, maxY, minZ, maxZ },
      distinctStates: counts.size,
      stages: [...this.stageLog.entries()],
      top: top.slice(0, 25),
    };
  }
}

export function savePhases(builder, file) {
  const p = builder.phases();
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(p));
  return p;
}
