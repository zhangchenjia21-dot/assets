import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';import {gunzipSync} from 'node:zlib';import crypto from 'node:crypto';
import {execute,worldStatus} from '../AI-Offline/L3_外交层/离线执行接口.mjs';
import {readNBT,RegionReader} from '../AI-Offline/L3_外交层/存档读取接口.mjs';
import {checkBlueprint} from '../AI-Preview/L3_外交层/预览公开接口.mjs';
import {inspectBlockStates} from '../AI-Blueprints/library/L3_外交层/资产公开接口.mjs';
const root=path.dirname(fileURLToPath(import.meta.url)),scene=JSON.parse(fs.readFileSync(path.join(root,'场景.json'),'utf8'));
const world='D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/saves/MB-V11-T02-山地修道院';
if(scene.world!==world)throw Error('TARGET_IDENTITY_MISMATCH');
const [action,stage='3']=process.argv.slice(2),n=Number(stage),out=path.join(root,'证据');fs.mkdirSync(out,{recursive:true});
const json=(v)=>JSON.stringify(v,(_,x)=>typeof x==='bigint'?x.toString():x,2);
function identity(){
 const level=readNBT(fs.readFileSync(path.join(world,'level.dat'))).Data;
 if(level.LevelName!=='MB-V11-T02-山地修道院')throw Error('LEVEL_NAME_MISMATCH');
 const gen=readNBT(fs.readFileSync(path.join(world,'data/minecraft/world_gen_settings.dat')));
 const evidence={world,level_name:level.LevelName,game_type:level.GameType,generation:gen};
 fs.writeFileSync(path.join(out,'世界身份.json'),json(evidence));return evidence;
}
if(action==='run'){
 const job=JSON.parse(fs.readFileSync(path.join(root,'作业',String(n).padStart(2,'0')+'.json'),'utf8'));
 if(job.world_path!==world)throw Error('JOB_TARGET_MISMATCH');
 if(n===1){if(fs.existsSync(world))throw Error('NEW_WORLD_ALREADY_EXISTS');}else{identity();await worldStatus(world);}
 const folder=fs.readdirSync(path.join(root,'蓝图')).find(s=>s.startsWith(String(n).padStart(2,'0')+'-'));
 const specified=new Map();let tiles=0;
 for(const file of fs.readdirSync(path.join(root,'蓝图',folder))){
  const bp=JSON.parse(gunzipSync(fs.readFileSync(path.join(root,'蓝图',folder,file))));checkBlueprint(bp,{previewOnly:true});
  for(const[x,y,z,p]of bp.blocks)specified.set((x+bp.origin.x)*100000+(y+bp.origin.y)*250+z+bp.origin.z,bp.palette[p]);tiles++;
 }
 const count=specified.size,states=inspectBlockStates(scene.palette);let operations=0;
 for(const ph of job.phases){
  for(const row of ph.operations){const[x,y,z,X,Y,Z,p]=row;operations++;for(let a=x;a<=X;a++)for(let b=y;b<=Y;b++)for(let c=z;c<=Z;c++){
   const k=a*100000+b*250+c;if(specified.get(k)!==ph.palette[p])throw Error('CANONICAL_OPERATION_MISMATCH');specified.delete(k);
  }}
  ph.palette=ph.palette.map(s=>{if(!states[s]?.valid)throw Error('INVALID_STATE '+s);return states[s].variants['0/none'];});
 }
 if(specified.size)throw Error('UNWRITTEN_CANONICAL_BLOCKS');
 fs.writeFileSync(path.join(out,`阶段${n}-蓝图核验.json`),json({tiles,blocks:count,operations,canonical_equivalent:true}));
 console.log('Validated',count,'blocks',operations,'operations');
 const result=await execute(job);identity();fs.writeFileSync(path.join(out,`阶段${n}-执行.json`),json(result));console.log(json(result));
}else if(action==='read'){
 await worldStatus(world);identity();const rr=new RegionReader(world);const [w,h,d]=scene.size,buffer=Buffer.alloc(w*h*d);const palette=[],map=new Map();let missing=0;
 for(let x=0;x<w;x++)for(let y=0;y<h;y++)for(let z=0;z<d;z++){
  const state=rr.get(x,y+scene.y0,z);if(state===null){missing++;continue;}if(!map.has(state)){map.set(state,palette.length);palette.push(state);if(palette.length>255)throw Error('PALETTE_TOO_LARGE');}
  buffer[(x*h+y)*d+z]=map.get(state);
 }
 if(missing)throw Error('MISSING_CHUNK '+missing);
 fs.writeFileSync(path.join(out,`阶段${n}-实存.bin`),buffer);fs.writeFileSync(path.join(out,`阶段${n}-实存.json`),json({world,size:scene.size,y0:scene.y0,palette,sha256:crypto.createHash('sha256').update(buffer).digest('hex'),read_at:new Date().toISOString(),source:'RegionReader: existing saved chunks only'}));console.log('READ',buffer.length,'voxels',palette.length,'states');
}else throw Error('UNKNOWN_ACTION');
