import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import {fileURLToPath} from 'node:url';
import {execute,worldStatus} from '../AI-Offline/L3_外交层/离线执行接口.mjs';
import {readNBT,RegionReader} from '../AI-Offline/L3_外交层/存档读取接口.mjs';
import {blueprintPhase} from '../AI-Offline/L3_外交层/蓝图执行接口.mjs';
const root=path.dirname(fileURLToPath(import.meta.url)),world='D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V17-T09-罗马浴场',stage=process.argv[2];
const write=(n,v)=>fs.writeFileSync(path.join(root,'证据',n),JSON.stringify(v,(_,x)=>typeof x==='bigint'?String(x):x,2));fs.mkdirSync(path.join(root,'证据'),{recursive:true});
function identity(){const d=readNBT(fs.readFileSync(world+'/level.dat')).Data,g=readNBT(fs.readFileSync(world+'/data/minecraft/world_gen_settings.dat')).data;if(fs.realpathSync(world)!==path.resolve(world)||d.LevelName!=='MB-V17-T09-罗马浴场'||g.generate_structures!==0||g.dimensions['minecraft:overworld'].generator.type!=='minecraft:flat')throw Error('T09_WORLD_IDENTITY_BLOCKER');return {world,name:d.LevelName,version:d.Version,generation:g};}
if(stage==='create'){
 if(fs.existsSync(world))throw Error('NEW_WORLD_ALREADY_EXISTS');
 const result=await execute({world_path:world,create:{type:'superflat',seed:1709,generator_options:{biome:'minecraft:plains',layers:[{block:'minecraft:bedrock',height:1},{block:'minecraft:stone',height:73},{block:'minecraft:dirt',height:5},{block:'minecraft:grass_block',height:1}],structure_overrides:[]}},spawn:[66,16,13]});write('世界身份.json',{...identity(),result,lock:await worldStatus(world)});console.log('T09 created: identity verified');
}else{
 if(!['01-Macro','01-GateRepair','02-Meso','02-JunctionRepair','03-Micro','04-Repair','reload'].includes(stage))throw Error('INVALID_STAGE');identity();await worldStatus(world);
 const phases=[];
 if(stage!=='reload'){const list=JSON.parse(fs.readFileSync(path.join(root,'蓝图',stage,'清单.json')));for(const file of list.files){const bp=JSON.parse(fs.readFileSync(path.join(root,'蓝图',stage,file))),p=blueprintPhase(bp);phases.push({palette:p.palette,operations:p.operations});}}
 const result=await execute({world_path:world,phases});write(stage+'-执行.json',result);const rr=new RegionReader(world),pal=[],map=new Map(),buffer=Buffer.alloc(144*144*56*2);let i=0;
 for(let y=10;y<66;y++)for(let z=0;z<144;z++)for(let x=0;x<144;x++){const s=rr.get(x,y,z)??'UNGENERATED';if(!map.has(s)){map.set(s,pal.length);pal.push(s);}buffer.writeUInt16LE(map.get(s),i++*2);}
 fs.writeFileSync(path.join(root,'证据',stage+'.u16'),buffer);write(stage+'-实存.json',{...identity(),origin:[0,10,0],shape_yzx:[56,144,144],palette:pal,sha256:crypto.createHash('sha256').update(buffer).digest('hex'),source:'RegionReader after formal save/shutdown'});console.log(JSON.stringify({stage,changed:result.changed_blocks,job:result.job_directory}));
}
