/** 仅读取已核实字节的事实快照；不加载游戏，不调用任何施工接口。
 * 扩展至地下24格和地上4格，供拟用通路/地块比选；不裁决结构安全。
 */
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {gunzipSync,gzipSync} from 'node:zlib';
import {RegionReader} from 'file:///D:/Games/Minecraft/AI工程/AI-Offline/L3_外交层/存档读取接口.mjs';
const root=path.dirname(fileURLToPath(import.meta.url));
const upstream=path.join(root,'../MP-P03M-NORTH-ROCK-TERRACE');
const provenance=JSON.parse(fs.readFileSync(path.join(upstream,'evidence/world-read-provenance.json'),'utf8'));
const snapshot='D:/Games/Minecraft/AI工程/MP-P03-cache/readonly-snapshot';
const hash=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const initial={};
for(const [rel,expected] of Object.entries(provenance.source_before)){
 const source=hash(path.join(provenance.source_path,rel)),copy=hash(path.join(snapshot,rel));
 if(source!==expected||copy!==expected)throw Error('Source/snapshot changed: '+rel);
 initial[rel]={source_sha256:source,snapshot_sha256:copy};
}
const raw=gunzipSync(fs.readFileSync(path.join(upstream,'evidence/surface.json.gz')));
if(createHash('sha256').update(raw).digest('hex')!==provenance.raw_sha256)throw Error('Raw surface mismatch');
const surface=JSON.parse(raw),bounds=[730,1616,806,1674];
const rows=surface.columns.filter(c=>c[0]>=bounds[0]&&c[0]<=bounds[2]&&c[1]>=bounds[1]&&c[1]<=bounds[3]);
const reader=new RegionReader(snapshot),palette=[],stateId=new Map();
const index=s=>{if(s===null)throw Error('Missing chunk');if(!stateId.has(s)){stateId.set(s,palette.length);palette.push(s)}return stateId.get(s)};
const columns=[],entities=[];
for(const c of rows){
 const [x,z,,y]=c;const ids=[];
 for(let dy=-24;dy<=4;dy++)ids.push(index(reader.get(x,y+dy,z)));
 if(reader.get(x,y,z)!==surface.palette[c[4]])throw Error('Surface readback mismatch');
 columns.push({x,z,ground_y:y,state_ids:ids});
}
for(let cz=Math.floor(bounds[1]/16);cz<=Math.floor(bounds[3]/16);cz++)for(let cx=Math.floor(bounds[0]/16);cx<=Math.floor(bounds[2]/16);cx++){
 for(const b of reader.chunk(cx,cz).nbt.block_entities||[]){
  if(b.x>=bounds[0]&&b.x<=bounds[2]&&b.z>=bounds[1]&&b.z<=bounds[3])entities.push({x:b.x,y:b.y,z:b.z,id:b.id});
 }
}
for(const [rel,v] of Object.entries(initial))if(hash(path.join(provenance.source_path,rel))!==v.source_sha256||hash(path.join(snapshot,rel))!==v.snapshot_sha256)throw Error('Input changed during scan');
fs.mkdirSync(path.join(root,'evidence'),{recursive:true});
const write=(name,data)=>fs.writeFileSync(path.join(root,'evidence',name),JSON.stringify(data,null,2)+'\n');
fs.writeFileSync(path.join(root,'evidence/near-ground.json.gz'),gzipSync(JSON.stringify({bounds,dy_range:[-24,4],palette,columns,block_entities:entities})));
fs.writeFileSync(path.join(root,'evidence/surface-crop.json.gz'),gzipSync(JSON.stringify({...surface,columns:rows,substrate_witnesses:[],block_entities:[],bounds})));
write('world-read-provenance.json',{world:'建筑师',source_path:provenance.source_path,read_snapshot:snapshot,original_snapshot_utc:provenance.read_utc,checked_utc:new Date().toISOString(),source_and_snapshot_hashes:initial,bounds,column_count:columns.length,block_reads:columns.length*29,dy_range:[-24,4],world_writes:0,missing_columns:0,method:'Existing L3 RegionReader on byte-matching readonly snapshot; original hash reads only; no game/server',raw_surface_sha256:provenance.raw_sha256,limitations:['Neither physics/movement nor stability verified','No inventories/player/entity files read','Ownership and historic paths not inferred from block states','Hashes cover relevant three source files only']});
console.log(JSON.stringify({columns:columns.length,states:palette.length,block_entities:entities.length,source_unchanged:true,world_writes:0}));
