import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';

// 只读取明确列出的父包对象与事实文件；不遍历规划目录，不导出父包完整数组。
const out=path.dirname(fileURLToPath(import.meta.url));
const root=path.dirname(out), parent=path.join(root,'MP-P04-WEST-APPROACH');
const hashes=[];
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
function read(rel,gzip=false){const b=fs.readFileSync(path.join(parent,rel));hashes.push({path:'minecraft/MP-P04-WEST-APPROACH/'+rel,sha256:sha(b),authority:rel.startsWith('evidence/')?'OBSERVED_SNAPSHOT':'DESIGN_PROPOSAL'});return JSON.parse(gzip?zlib.gunzipSync(b):b.toString('utf8'));}
function write(rel,o){const p=path.join(out,rel);fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,JSON.stringify(o,null,2)+'\n');}
const pk=read('implementation-packages.json');
const packages=pk.filter(p=>p.id==='PACKAGE-01'||p.id==='PACKAGE-03');
const p=read('planning-data.json');
const selected={source_plan:p.id,source_revision:p.revision,packages,parcels:p.parcels.filter(o=>['PARCEL-01','PARCEL-02'].includes(o.id)),frontages:p.frontages.filter(o=>['FRONTAGE-01','FRONTAGE-02'].includes(o.id)),blocks:p.blocks.filter(o=>o.id==='BLOCK-01'),lanes:p.lanes.filter(o=>['LANE-01','LANE-02','LANE-04'].includes(o.id)),shared_spaces:p.shared_spaces.filter(o=>o.id==='SPACE-01')};
// 所有选中对象都由 PACKAGE-01 的范围或直接公共接口关系指向。
write('sources/父包直接对象.json',selected);
const old=read('evidence/world-read-provenance.json');
const surface=read('evidence/surface-crop.json.gz',true),near=read('evidence/near-ground.json.gz',true);
const bounds=[746,1620,799,1653];
const inside=(x,z)=>x>=bounds[0]&&x<=bounds[2]&&z>=bounds[1]&&z<=bounds[3];
write('evidence/地表采样.json',{bounds,fields:surface.fields,palette:surface.palette,columns:surface.columns.filter(c=>inside(c[0],c[1])),authority:'OBSERVED_SNAPSHOT'});
write('evidence/浅层采样.json',{bounds,dy_range:near.dy_range,palette:near.palette,columns:near.columns.filter(c=>inside(c.x,c.z)),block_entities:near.block_entities.filter(c=>inside(c.x,c.z)),authority:'OBSERVED_SNAPSHOT',note:'block_entities 仅位置和种类；未读取容器内容。浅层切片不是深层排除证明。'});
write('evidence/公共路纵断面.json',read('evidence/lane-profiles.json').filter(c=>['LANE-01','LANE-02','LANE-04'].includes(c.id)));
const verified=Object.entries(old.source_and_snapshot_hashes).map(([rel,h])=>{const live=path.join(old.source_path,rel),b=fs.readFileSync(live);return {path:rel,sha256:sha(b),matches_parent_snapshot:sha(b)===h.source_sha256};});
if(verified.some(v=>!v.matches_parent_snapshot))throw Error('源世界已变化，不能把父快照当成当前证据');
write('evidence/世界来源核验.json',{checked_utc:new Date().toISOString(),original_snapshot_utc:old.original_snapshot_utc,world:old.world,source_path:old.source_path,method:'READ_ONLY_HASH_MATCH_AND_BOUNDED_FACT_EXTRACTION',files:verified,world_writes:0,limitations:['仅核验相关三个文件；非整个存档不变证明','未启动游戏/执行器；未进行碰撞、物理通行或结构稳定试验','体素分布不证明权属、地层承载或供水量'],parent_observation:old});
const canonRoot=path.join(root,'建筑师');
for(const [rel,name] of [['world/civilizations/CIV-001/README.md','CIV-001-Canon.md'],['decisions/D-014_CIV-001最小文明Canon收敛与AB-001进入.md','CIV-001-批准.md'],['architecture/civilizations/CIV-001/Architecture-Grammar.md','CIV-001-Grammar.md']]){const b=fs.readFileSync(path.join(canonRoot,rel));hashes.push({path:'minecraft/建筑师/'+rel,sha256:sha(b),authority:'APPROVED_CANON'});fs.writeFileSync(path.join(out,'sources',name),b);}
write('sources/来源登记.json',{assets_snapshot_commit:'6c6dafc6c1bc5163dccce76b54470e8edb48ab2a',selection:'PACKAGE-01; PACKAGE-03 direct public coordination; BLOCK-01; PARCEL/FRONTAGE-01,02; LANE-01,02,04; SPACE-01. No other package answers or review files.',files:hashes});
console.log(JSON.stringify({selected: selected.parcels.map(o=>o.id),current_world_hashes_match:verified.every(v=>v.matches_parent_snapshot),bounds,world_writes:0}));
