import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';
import {execute,worldStatus} from '../AI-Offline/L3_外交层/离线执行接口.mjs';
import {readNBT,RegionReader} from '../AI-Offline/L3_外交层/存档读取接口.mjs';
import {blueprintPhase} from '../AI-Offline/L3_外交层/蓝图执行接口.mjs';
import {inspectBlockStates} from '../AI-Blueprints/library/L3_外交层/资产公开接口.mjs';
const base=new URL('./',import.meta.url),world='D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V15-T07-绿洲驿站';
const stage=process.argv[2];if(!/^0[1-9]-[A-Za-z]+$/.test(stage))throw Error('INVALID_STAGE');
const read=u=>JSON.parse(fs.readFileSync(u,'utf8'));
// 每次绑定真实路径、名称、生成配置；不能从参数指定另一存档。
const actual=fs.realpathSync(world),level=readNBT(fs.readFileSync(world+'/level.dat')).Data;
const gen=readNBT(fs.readFileSync(world+'/data/minecraft/world_gen_settings.dat')).data;
if(path.resolve(actual)!==path.resolve(world)||level.LevelName!=='MB-V15-T07-绿洲驿站'||gen.generate_structures!==0||gen.dimensions['minecraft:overworld'].generator.type!=='minecraft:flat')throw Error('T07_IDENTITY_BLOCKER');
await worldStatus(world);
const list=read(new URL(`蓝图/${stage}/清单.json`,base));
const bps=list.files.map(f=>read(new URL(`蓝图/${stage}/${f}`,base)));
inspectBlockStates([...new Set(bps.flatMap(b=>b.palette))]);
const converted=bps.map(blueprintPhase);const phases=converted.map(({palette,operations})=>({palette,operations}));
const samples=converted.flatMap(p=>p.samples.filter((_,i)=>i%199===0));
const result=await execute({world_path:world,phases,samples,spawn:[243,18,218]});
fs.writeFileSync(new URL(`证据/${stage}-执行.json`,base),JSON.stringify(result,null,2));
// 保存关闭后重新从磁盘读取；不是把蓝图冒充现场。
await worldStatus(world);const reader=new RegionReader(world),pal=[],idx=new Map();const buf=Buffer.alloc(52*240*288*2);let k=0;
for(let y=12;y<64;y++)for(let z=0;z<240;z++)for(let x=0;x<288;x++){
 const s=reader.get(x,y,z)??'UNGENERATED';if(!idx.has(s)){idx.set(s,pal.length);pal.push(s);}buf.writeUInt16LE(idx.get(s),k);k+=2;
}
const mismatches=[];let checked=0;
for(const p of converted)for(const [x,y,z,i]of p.operations){checked++;const got=reader.get(x,y,z);if(got!==p.palette[i]&&mismatches.length<50)mismatches.push({x,y,z,expected:p.palette[i],got});}
fs.writeFileSync(new URL(`证据/${stage}-实存方块.u16`,base),buf);
fs.writeFileSync(new URL(`证据/${stage}-实存元数据.json`,base),JSON.stringify({world,stage,origin:[0,12,0],shape_yzx:[52,240,288],palette:pal,sha256:crypto.createHash('sha256').update(buf).digest('hex'),checked,mismatches,source:'Read-only RegionReader after executor save/shutdown; not blueprint preview',fluid_stability:'unverified'},null,2));
console.log(JSON.stringify({stage,world,changed:result.changed_blocks,checked,mismatches,job:result.job_directory}));
