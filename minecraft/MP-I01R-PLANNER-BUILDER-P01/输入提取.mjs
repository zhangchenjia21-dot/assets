// 仅提取 BDP-01；依赖中的同级对象不进入设计上下文或归档。
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const source=path.resolve(root,'../发布/assets/minecraft/MP-P05R2-NORTH-FRONTAGE-ENSEMBLE');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8').replace(/^\uFEFF/,''));
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const out=(name,v)=>fs.writeFileSync(path.join(root,'inputs',name),JSON.stringify(v,null,2)+'\n');
const b=read(path.join(root,'inputs/BDP-01.json'));
if(b.package_id!=='BDP-01')throw Error('wrong package');
const mask=new Set(b.spatial_envelope.cells.map(c=>c.join(',')));
const receipts=[];
for(const dep of b.dependencies){
 const p=path.join(source,dep.file), actual=hash(p);
 if(actual!==dep.sha256)throw Error('dependency changed: '+dep.file);
 receipts.push({...dep,actual_sha256:actual});
}
const s=read(path.join(source,'evidence/地表采样.json'));
const n=read(path.join(source,'evidence/浅层采样.json'));
out('场地事实切片.json',{authority:s.authority,fields:s.fields,palette:s.palette,columns:s.columns.filter(c=>mask.has(c.slice(0,2).join(','))),near_ground:{dy_range:n.dy_range,palette:n.palette,columns:n.columns.filter(c=>mask.has([c.x,c.z].join(','))),note:n.note},scope:'BDP-01 parcel columns only; no live save opened'});
// BDP 自带完整接口切片；外部文件只选择这些确切 ID，不遍历其它包的设计。
for(const [file,ids,name] of [['interface-baselines.json',b.interface_baselines.map(i=>i.interface_id),'接口直接依赖.json'],['external-service-interfaces.json',b.external_service_interfaces.map(i=>i.service_id),'服务直接依赖.json']]){
 const j=read(path.join(source,file));const values=Array.isArray(j)?j:Object.values(j).filter(Array.isArray).flat();
 const selected=values.filter(v=>ids.includes(v.interface_id??v.service_id));
 if(selected.length!==ids.length)throw Error('cannot resolve selected IDs '+file);
 out(name,selected);
}
const canonBase=path.resolve(source,'../建筑师');
for(const [p,name] of [['world/civilizations/CIV-001/README.md','CIV-001-Canon.md'],['decisions/D-014_CIV-001最小文明Canon收敛与AB-001进入.md','CIV-001-D014.md'],['architecture/civilizations/CIV-001/Architecture-Grammar.md','CIV-001-Architecture-Grammar.md']]){
 const sourcePath=path.join(canonBase,p);fs.copyFileSync(sourcePath,path.join(root,'inputs',name));receipts.push({file:sourcePath,sha256:hash(sourcePath),snapshot:name});
}
out('来源与读取记录.json',{test:'MP-I01R',date:'2026-09-14',builder:{version:'1.11',commit:'fc6371361685e2eeaefdef5a513f21dbe64c6696',source:'https://github.com/zhangchenjia21-dot/Vibe-Coding/blob/fc6371361685e2eeaefdef5a513f21dbe64c6696/skill/codex/minecraft-builder/SKILL.md',load:'commit-pinned read-only snapshot; not installed or modified',sha256:hash(path.join(root,'inputs/Builder-SKILL.md'))},contract:{version:'1.0',commit:'fc6371361685e2eeaefdef5a513f21dbe64c6696',path:'skill/codex/shared/minecraft-planner-builder-contract.md',sha256:hash(path.join(root,'inputs/planner-builder-contract.md'))},handoff:{plan:'MP-P05R2',package:'BDP-01',revision:b.package_revision,selected_snapshot_sha256:hash(path.join(root,'inputs/BDP-01.json')),selection:'JSON container parsed by tool; only package_id == BDP-01 selected/output/used. BDP-02 was not output or consumed. No whole-file package copy archived.'},dependencies:receipts,other_reads:['AI工程/ARCHITECTURE.md','assets/AGENTS.md','BDP-01 source_refs: provenance.json; sources/来源登记.json (provenance only; no transitive MP-P04 content followed)','memory registry searched solely to locate Builder source; historical design answers not opened'],prohibited_content_consumed:[],world_writes:0,world_write_authorization:false,regression_verdict:'NOT_ASSIGNED',input_state:'Planner directory was already untracked; preserved untouched and excluded from task commit'});
console.log(JSON.stringify({selected:'BDP-01',terrain_columns:mask.size,dependencies:receipts.length,world_writes:0}));
