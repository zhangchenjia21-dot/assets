import fs from 'node:fs';
import crypto from 'node:crypto';
import {RegionReader,readNBT} from '../AI-Offline/L3_外交层/存档读取接口.mjs';
const base='D:/Games/Minecraft/AI工程';
const meta=JSON.parse(fs.readFileSync(base+'/MB-V110-T12/证据/reload-实存.json'));
const evidence=fs.readFileSync(base+'/MB-V110-T12/证据/reload.u16');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
if(sha(evidence)!==meta.sha256)throw Error('RELOAD_EVIDENCE_CHANGED');
const worlds=[meta.world,'D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V110-T12-京町家修复'];
const rows=[];
for(const world of worlds){
 if(!fs.existsSync(world))continue;
 const level=readNBT(fs.readFileSync(world+'/level.dat'));
 if(level.Data.LevelName!==meta.name)throw Error('WRONG_WORLD');
 const rr=new RegionReader(world);let mismatch=0;const examples=[];
 for(let y=10;y<46;y++)for(let z=0;z<96;z++)for(let x=0;x<56;x++){
  const before=meta.palette[evidence.readUInt16LE((((y-10)*96+z)*56+x)*2)],after=rr.get(x,y,z);
  if(before!==after){mismatch++;if(examples.length<10)examples.push({x,y,z,before,after});}
 }
 rows.push({world,name:level.Data.LevelName,data_version:level.Data.DataVersion,mismatch,examples});
}
fs.writeFileSync(base+'/T12正式入库/来源核对.json',JSON.stringify(rows,null,2));console.log(JSON.stringify(rows));
