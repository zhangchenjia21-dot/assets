import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';
import {execute,worldStatus} from '../AI-Offline/L3_外交层/离线执行接口.mjs';
import {readNBT,RegionReader} from '../AI-Offline/L3_外交层/存档读取接口.mjs';
import {blueprintPhase} from '../AI-Offline/L3_外交层/蓝图执行接口.mjs';
import {inspectBlockStates} from '../AI-Blueprints/library/L3_外交层/资产公开接口.mjs';
const root=new URL('./',import.meta.url),world='D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V16-T08-哥特教堂',stage=process.argv[2];
const write=(name,data)=>fs.writeFileSync(new URL(name,root),JSON.stringify(data,(_,v)=>typeof v==='bigint'?String(v):v,2));
fs.mkdirSync(new URL('证据/',root),{recursive:true});
function identity(){const d=readNBT(fs.readFileSync(world+'/level.dat')).Data,g=readNBT(fs.readFileSync(world+'/data/minecraft/world_gen_settings.dat')).data;if(fs.realpathSync(world)!==path.resolve(world)||d.LevelName!=='MB-V16-T08-哥特教堂'||g.generate_structures!==0||g.dimensions['minecraft:overworld'].generator.type!=='minecraft:flat')throw Error('T08_WORLD_IDENTITY_BLOCKER');return{world,name:d.LevelName,version:d.Version,generation:g};}
if(stage==='create'){
 if(fs.existsSync(world))throw Error('NEW_WORLD_ALREADY_EXISTS');
 const result=await execute({world_path:world,create:{type:'superflat',seed:1608,generator_options:{biome:'minecraft:plains',layers:[{block:'minecraft:bedrock',height:1},{block:'minecraft:stone',height:73},{block:'minecraft:dirt',height:5},{block:'minecraft:grass_block',height:1}],structure_overrides:[]}},spawn:[18,16,56],samples:[[0,15,0,'minecraft:grass_block[snowy=false]']]});write('证据/世界身份.json',{...identity(),result,lock:await worldStatus(world)});console.log('T08 created and identity verified');
}else{
 if(!/^(01-Macro|02-Meso|03-Micro|04-Repair|reload)$/.test(stage))throw Error('UNSUPPORTED_STAGE');identity();await worldStatus(world);
 let phases=[],samples=[];
 if(stage!=='reload'){
  const manifest=JSON.parse(fs.readFileSync(new URL(`蓝图/${stage}/清单.json`,root)));const bps=manifest.files.map(f=>JSON.parse(fs.readFileSync(new URL(`蓝图/${stage}/${f}`,root))));
  const native=inspectBlockStates([...new Set(bps.flatMap(b=>b.palette))]);write(`证据/${stage}-原生状态.json`,native);if(Object.values(native).some(v=>!v.valid))throw Error('INVALID_NATIVE_STATES');
  for(const bp of bps){const p=blueprintPhase(bp);phases.push({palette:p.palette,operations:p.operations});samples.push(...p.samples.filter((_,i)=>i%113===0));}
 }
 const result=await execute({world_path:world,phases,samples});write(`证据/${stage}-执行.json`,result);await worldStatus(world);const rr=new RegionReader(world),palette=[],indexes=new Map(),buffer=Buffer.alloc(160*144*84*2);let i=0;
 for(let y=12;y<96;y++)for(let z=0;z<144;z++)for(let x=0;x<160;x++){const s=rr.get(x,y,z)??'UNGENERATED';if(!indexes.has(s)){indexes.set(s,palette.length);palette.push(s);}buffer.writeUInt16LE(indexes.get(s),i++*2);}
 fs.writeFileSync(new URL(`证据/${stage}.u16`,root),buffer);write(`证据/${stage}-实存.json`,{world,shape_yzx:[84,144,160],origin:[0,12,0],palette,sha256:crypto.createHash('sha256').update(buffer).digest('hex'),source:'RegionReader after save and shutdown'});console.log(JSON.stringify({stage,changed:result.changed_blocks,job:result.job_directory}));
}
