import fs from 'node:fs';import path from 'node:path';
import {promoteOriginalAsset,inspectAsset,instantiateAsset,inspectBlockStates} from '../AI-Blueprints/library/L3_外交层/资产公开接口.mjs';
import {RegionReader,readNBT} from '../AI-Offline/L3_外交层/存档读取接口.mjs';
const root=path.dirname(new URL(import.meta.url).pathname).replace(/^\/([A-Z]:)/,'$1');
const dir=decodeURIComponent(root),results=[];
for(const id of ['AI-T07-PALM-B','AI-T07-CANOPY-A']){
 const folder=path.join(dir,id),file=path.join(folder,'blueprint.json'),bp=JSON.parse(fs.readFileSync(file)),p=JSON.parse(fs.readFileSync(path.join(folder,'提取来源.json')));
 if(readNBT(fs.readFileSync(p.world+'/level.dat')).Data.LevelName!=='MB-V15-T07-绿洲驿站')throw Error('SOURCE_WORLD_MISMATCH');
 const rr=new RegionReader(p.world),states=inspectBlockStates(bp.palette);
 for(const [x,y,z,v] of bp.blocks){const state=rr.get(x+p.bounds[0][0],y+p.bounds[0][1],z+p.bounds[0][2]);if(state!==bp.palette[v])throw Error('SOURCE_WORLD_CHANGED');}
 if(Object.values(states).some(s=>!s.valid))throw Error('INVALID_STATE');
 const tree=id.includes('PALM'),source={id,name:bp.metadata.name,source_kind:'AI_ORIGINAL',normalized_blueprint_path:file,owner_authorization:'2026-09-11 用户明确要求：把上轮的羽状椰枣树 B 和木脊布棚 A 入库',max_repetitions:tree?4:3,classification_v2:{primary_use:tree?'vegetation':'market',secondary_use:['shade'],structure_type:tree?'tree':'open_shelter',terrain_fit:[{tag:'flat'}],styles:[{tag:'desert'},{tag:'historical'}],scale:'small'},source:{source_url:'https://github.com/zhangchenjia21-dot/assets/tree/main/minecraft/MB-V15-T07',author:'Codex original for Owner',license:'Owner-authorized reuse; no separate public license declared'},brief_path:path.join(dir,'README.md')};
 fs.writeFileSync(path.join(folder,'原创来源.json'),JSON.stringify(source,null,2));
 const asset=promoteOriginalAsset(source);const check=inspectAsset(asset.asset_id);let variants=0;
 for(const rotation of [0,90,180,270])for(const mirror of ['none','x','z']){const instance=instantiateAsset(asset.asset_id,{rotation,mirror});if(instance.blueprint.blocks.length!==bp.blocks.length)throw Error('TRANSFORM_BLOCK_LOSS');variants++;}
 results.push({asset_id:asset.asset_id,name:asset.name,status:asset.status,dimensions:asset.dimensions,occupied_blocks:asset.occupied_blocks,blueprint_sha256:asset.blueprint_sha256,anchor:check.placement.anchor,variants_checked:variants,source_world_block_mismatches:0,world_writes:0});
}
fs.writeFileSync(path.join(dir,'入库结果.json'),JSON.stringify(results,null,2));console.log(JSON.stringify(results));
