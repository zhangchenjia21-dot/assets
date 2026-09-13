/** 本轮外围证据脚本：只复制明确的region到独立缓存，通过现有L3读取；不启动游戏、不回写来源。 */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import {RegionReader,readNBT} from '../../../..//AI-Offline/L3_外交层/存档读取接口.mjs';
const root=path.dirname(fileURLToPath(import.meta.url));
const cache=path.resolve(root,'../../../..','MP-P03-cache');
const source='D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/建筑师';
const names=['level.dat','dimensions/minecraft/overworld/region/r.1.2.mca','dimensions/minecraft/overworld/region/r.1.3.mca'];
const sha=f=>crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const save=(p,v)=>fs.writeFileSync(p,JSON.stringify(v,null,2)+'\n');
const processes=execFileSync('powershell.exe',['-NoProfile','-Command',"@(Get-Process | Where-Object { $_.ProcessName -in @('java','javaw') }).Count"],{encoding:'utf8'}).trim();
if(processes!=='0')throw Error('Minecraft runtime exit is not confirmed');
const identity=readNBT(fs.readFileSync(path.join(source,'level.dat'))).Data;
if(identity.LevelName!=='建筑师')throw Error('WORLD_IDENTITY_MISMATCH');
fs.mkdirSync(path.join(root,'evidence'),{recursive:true});
const before=Object.fromEntries(names.map(n=>[n,sha(path.join(source,n))]));
for(const n of names){const dest=path.join(cache,'readonly-snapshot',n);fs.mkdirSync(path.dirname(dest),{recursive:true});fs.copyFileSync(path.join(source,n),dest);if(sha(dest)!==before[n])throw Error('COPY_HASH_MISMATCH');}
const reader=new RegionReader(path.join(cache,'readonly-snapshot'));const bounds=[640,1488,959,1775];
const palette=[];const ids=new Map();const id=s=>{if(!ids.has(s)){ids.set(s,palette.length);palette.push(s);}return ids.get(s);};
const air=s=>s==='minecraft:air'||s==='minecraft:cave_air'||s==='minecraft:void_air';
// 显式观察分类只剥离可辨认植物以取得地面，不判断任何规划用途。
const plant=s=>/(_leaves|_log|_wood|_sapling|grass|fern|flower|bush|vine|poppy|dandelion|lily|mushroom|cactus|sugar_cane)/.test(s.split('[')[0])&&!/grass_block|mushroom_stem/.test(s);
const columns=[];const witnesses=[];let missing=0;const blockEntities=[];
for(let cz=Math.floor(bounds[1]/16);cz<=Math.floor(bounds[3]/16);cz++)for(let cx=Math.floor(bounds[0]/16);cx<=Math.floor(bounds[2]/16);cx++){const ch=reader.chunk(cx,cz);if(!ch)continue;for(const b of ch.nbt.block_entities||[])if(b.x>=bounds[0]&&b.x<=bounds[2]&&b.z>=bounds[1]&&b.z<=bounds[3])blockEntities.push({x:b.x,y:b.y,z:b.z,id:b.id});}
for(let z=bounds[1];z<=bounds[3];z++)for(let x=bounds[0];x<=bounds[2];x++){
 const ch=reader.chunk(Math.floor(x/16),Math.floor(z/16));if(!ch){missing++;continue;}
 let top=null,ground=null,water=null,leaf=0,trunk=0,plants=0;
 for(let y=320;y>=-64;y--){const s=reader.get(x,y,z);if(air(s))continue;if(top===null)top=y;
  if(s.startsWith('minecraft:water')){if(water===null)water=y;continue;}
  if(plant(s)){if(s.includes('_leaves'))leaf++;else if(/_log|_wood/.test(s))trunk++;else plants++;continue;}
  ground=[y,id(s)];break;
 }
 if(!ground)throw Error('GROUND_NOT_FOUND '+x+','+z);
 columns.push([x,z,top,ground[0],ground[1],water,leaf,trunk,plants]);
 if(x%8===0&&z%8===0){const states=[];for(let y=ground[0];y>=ground[0]-12;y--)states.push(id(reader.get(x,y,z)));witnesses.push({x,z,top_y:ground[0],state_ids:states});}
}
save(path.join(cache,'surface.json'),{bounds,fields:['x','z','top_y','ground_y','ground_state','water_y','leaf_blocks','trunk_blocks','other_plant_blocks'],palette,columns,substrate_witnesses:witnesses,block_entities:blockEntities,missing_columns:missing});
const after=Object.fromEntries(names.map(n=>[n,sha(path.join(source,n))]));
if(JSON.stringify(before)!==JSON.stringify(after))throw Error('SOURCE_CHANGED_DURING_READ');
save(path.join(root,'evidence/world-read-provenance.json'),{world:identity.LevelName,source_path:source,data_version:identity.DataVersion,read_utc:new Date().toISOString(),runtime_process_count:0,bounds,source_before:before,source_after:after,source_changed:false,world_writes:0,method:'existing L3 RegionReader on byte-verified two-region copy; original only read; no server start',raw_cache:path.join(cache,'surface.json'),raw_sha256:sha(path.join(cache,'surface.json')),column_count:columns.length,substrate_grid:8,substrate_depth:13,missing_columns:missing,block_entities:blockEntities,limits:['Block entity IDs only, no inventory/player data','Entity files/POI/caves/ownership not surveyed','Ground extraction plant filter is explicit heuristic; raw palette retained','Hashes cover touched files only, not the whole save']});
console.log(JSON.stringify({world:identity.LevelName,columns:columns.length,palette:palette.length,blockEntities,world_writes:0}));
