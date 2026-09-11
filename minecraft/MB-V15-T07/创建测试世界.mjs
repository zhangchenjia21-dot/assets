import fs from 'node:fs';
import path from 'node:path';
import {execute,worldStatus} from '../AI-Offline/L3_外交层/离线执行接口.mjs';
import {readNBT} from '../AI-Offline/L3_外交层/存档读取接口.mjs';
const root=path.dirname(new URL(import.meta.url).pathname).replace(/^\/(\w:)/,'$1');
const world='D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V15-T07-绿洲驿站';
// 独立新世界工厂，目标已存在时拒绝覆盖；不接受任何外部世界参数。
if(fs.existsSync(world))throw Error('T07_NEW_WORLD_ALREADY_EXISTS');
const job={world_path:world,create:{type:'superflat',seed:1507,generator_options:{biome:'minecraft:desert',layers:[{block:'minecraft:bedrock',height:1},{block:'minecraft:stone',height:55},{block:'minecraft:sandstone',height:20},{block:'minecraft:sand',height:4}],structure_overrides:[]}},spawn:[244,16,220],samples:[[0,15,0,'minecraft:sand']]};
fs.mkdirSync(new URL('./证据/',import.meta.url),{recursive:true});
const r=await execute(job);
const level=readNBT(fs.readFileSync(world+'/level.dat')).Data;
const generation=readNBT(fs.readFileSync(world+'/data/minecraft/world_gen_settings.dat'));
const e={world,level_name:level.LevelName,version:level.Version,generation,execution:r,lock:await worldStatus(world)};
fs.writeFileSync(new URL('./证据/新世界身份.json',import.meta.url),JSON.stringify(e,(_,v)=>typeof v==='bigint'?String(v):v,2));
if(level.LevelName!=='MB-V15-T07-绿洲驿站')throw Error('WORLD_NAME_MISMATCH');
console.log(JSON.stringify(e,(_,v)=>typeof v==='bigint'?String(v):v));
