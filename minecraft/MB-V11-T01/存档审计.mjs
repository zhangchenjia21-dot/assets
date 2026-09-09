import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
import {RegionReader,readNBT} from '../AI-Offline/L3_外交层/存档读取接口.mjs';
import {worldStatus} from '../AI-Offline/L3_外交层/离线执行接口.mjs';
const root=path.dirname(fileURLToPath(import.meta.url)),stage=Number(process.argv[2]??3),name='MB-V11-T01-苏州园林',world=path.resolve('D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves',name);
await worldStatus(world);const level=readNBT(fs.readFileSync(path.join(world,'level.dat'))).Data,gen=readNBT(fs.readFileSync(path.join(world,'data/minecraft/world_gen_settings.dat')));
if(level.LevelName!==name)throw Error('TEST_WORLD_NAME_MISMATCH:'+level.LevelName);
const reader=new RegionReader(world),manifest=JSON.parse(fs.readFileSync(path.join(root,'阶段清单.json'),'utf8')),expected=new Map();
for(const s of manifest.stages.slice(0,Math.min(stage,3)))for(const f of s.files){let b=JSON.parse(fs.readFileSync(path.join(root,f),'utf8'));for(const[x,y,z,p]of b.blocks)expected.set(`${x+b.origin.x},${y+b.origin.y},${z+b.origin.z}`,b.palette[p]);}
if(stage>=4&&fs.existsSync(path.join(root,'修正批次.json')))for(const p of JSON.parse(fs.readFileSync(path.join(root,'修正批次.json'),'utf8')))for(const[x,y,z,i]of p.operations)expected.set(`${x},${y},${z}`,p.palette[i]);
const parse=s=>{let[id,p]=s.split('[');return{id,props:Object.fromEntries((p??'').replace(']','').split(',').filter(Boolean).map(v=>v.split('=')))}};let mismatch=[];
for(const[k,e]of expected){const p=k.split(',').map(Number),actual=reader.get(...p);if(!actual){mismatch.push({p,e,actual});continue;}let a=parse(actual),b=parse(e);if(a.id!==b.id||Object.entries(b.props).some(([k,v])=>a.props[k]!==v))mismatch.push({p,e,actual});}
const rows=[];for(let z=-3;z<=153;z++)for(let x=-3;x<=187;x++)for(let y=58;y<=103;y++){let s=reader.get(x,y,z);if(s&&!s.endsWith(':air'))rows.push([x,y,z,s]);}
fs.writeFileSync(path.join(root,'存档回读方块.json'),JSON.stringify(rows));
const air=(x,y,z)=>{let s=reader.get(x,y,z);return s==='minecraft:air'||s==='minecraft:cave_air';};
const floor=(x,y,z)=>{let s=reader.get(x,y,z);return s&&!s.endsWith(':air')&&!s.endsWith(':cave_air')&&!s.startsWith('minecraft:water[')&&s!=='minecraft:water'&&!s.includes('fence')&&!s.includes('bamboo')&&!s.includes('leaves')&&!s.includes('lily_pad');};
// 保守的两格净空、四邻接行走图允许一级台阶跳跃；不以飞行作为可达性证据。
const nodes=new Set();for(let z=1;z<=151;z++)for(let x=1;x<=183;x++)for(let y=62;y<=89;y++)if(floor(x,y,z)&&air(x,y+1,z)&&air(x,y+2,z))nodes.add(`${x},${y},${z}`);
const start='38,63,146',seen=new Set([start]),queue=[start];for(let i=0;i<queue.length;i++){let[x,y,z]=queue[i].split(',').map(Number);for(let[dx,dz]of[[1,0],[-1,0],[0,1],[0,-1]])for(let dy of[0,1,-1]){let k=`${x+dx},${y+dy},${z+dz}`;if(nodes.has(k)&&!seen.has(k)&&(dy!==1||air(x,y+3,z))){seen.add(k);queue.push(k);}}}
const targets=manifest.components.filter(c=>c.type==='building').map(c=>{let x=Math.round((c.bounds[0]+c.bounds[3])/2),z=Math.round((c.bounds[2]+c.bounds[5])/2);return{name:c.name,position:[x,c.floor+1,z],reachable:seen.has(`${x},${c.floor},${z}`)};});
const routeIssues=[];if(stage>=2)for(const r of manifest.routes){let blocked=r.cells.filter(([x,y,z])=>!floor(x,y,z)||!air(x,y+1,z)||!air(x,y+2,z));routeIssues.push({name:r.name,blocked_cells:blocked.length,examples:blocked.slice(0,12)});}
const result={status:mismatch.length?'FAIL':'PASS',world_path:world,level_name:level.LevelName,generation:gen,stage,expected_blocks:expected.size,mismatches:mismatch.length,mismatch_examples:mismatch.slice(0,30),readback_blocks:rows.length,reachability:{method:'4-neighbor, two air blocks, max 1 block step; conservative block approximation; jumping required where full steps remain',reachable_nodes:seen.size,targets,routes:routeIssues}};
fs.writeFileSync(path.join(root,`审计-${stage}.json`),JSON.stringify(result,(_,v)=>typeof v==='bigint'?v.toString():v,2));console.log(JSON.stringify({...result,generation:undefined}));
