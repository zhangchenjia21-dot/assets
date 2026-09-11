import fs from 'node:fs';import path from 'node:path';
import {execute,worldStatus} from '../AI-Offline/L3_外交层/离线执行接口.mjs';
import {readNBT,RegionReader} from '../AI-Offline/L3_外交层/存档读取接口.mjs';
const world='D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V15-T07-绿洲驿站';
const d=readNBT(fs.readFileSync(world+'/level.dat')).Data;
if(d.LevelName!=='MB-V15-T07-绿洲驿站'||fs.realpathSync(world)!==path.resolve(world))throw Error('WORLD_IDENTITY_MISMATCH');
await worldStatus(world);const result=await execute({world_path:world});await worldStatus(world);
const r=new RegionReader(world),m=JSON.parse(fs.readFileSync(new URL('./证据/05-Water-实存元数据.json',import.meta.url))),buf=fs.readFileSync(new URL('./证据/05-Water-实存方块.u16',import.meta.url));let count=0,diff=0;const examples=[];
for(let y=12;y<64;y++)for(let z=0;z<240;z++)for(let x=0;x<288;x++){
 const expected=m.palette[buf.readUInt16LE(count*2)],actual=r.get(x,y,z);count++;if(actual!==expected){diff++;if(examples.length<20)examples.push({x,y,z,actual,expected});}
}
fs.writeFileSync(new URL('./证据/保存重载核验.json',import.meta.url),JSON.stringify({world,explicit_block_writes:0,checked:count,differences:diff,examples,result,note:'Normal reload only; not a controlled fluid update or client traversal.'},null,2));console.log(JSON.stringify({checked:count,differences:diff,explicit_block_writes:0}));
