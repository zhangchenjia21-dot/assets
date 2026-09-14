import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const read=f=>JSON.parse(fs.readFileSync(path.join(dir,f),'utf8'));
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const key=([x,z])=>`${x},${z}`;
const neighbors=([x,z])=>[[x+1,z],[x-1,z],[x,z+1],[x,z-1]];
const checks=[],facts=[];
function check(name,ok,evidence){checks.push({name,ok,evidence});}
function connected(cells){const set=new Set(cells.map(key)),components=[];while(set.size){const first=[...set][0],q=[first];set.delete(first);for(let i=0;i<q.length;i++)for(const p of neighbors(q[i].split(',').map(Number))){const k=key(p);if(set.delete(k))q.push(k);}components.push(q.length);}return components;}
const p=read('planning-data.json'),bd=read('builder-design-packages.json'),ifs=read('interface-baselines.json').interfaces,services=read('external-service-interfaces.json').services;
const ids=new Set(ifs.map(i=>i.interface_id));
check('two_households_only',p.parcels.length===2&&p.parcels.reduce((s,c)=>s+c.households,0)===2,p.capacity);
check('no_regression_verdict',p.regression_verdict===null,p.review_status);
let all=new Set();
for(const parcel of p.parcels){const own=new Set(parcel.cells.map(key));check(parcel.id+'_unique_cells',own.size===parcel.cells.length,own.size);
check(parcel.id+'_no_other_parcel_overlap',parcel.cells.every(c=>!all.has(key(c))),parcel.cells.length);parcel.cells.forEach(c=>all.add(key(c)));
const portions=[parcel.allocation.private_open_yard,parcel.allocation.private_frontage_apron,parcel.allocation.architectural_search_mask],part=new Set();let clean=true;for(const a of portions)for(const c of a.cells){if(!own.has(key(c))||part.has(key(c)))clean=false;part.add(key(c));}
check(parcel.id+'_disjoint_complete_allocation',clean&&part.size===own.size,portions.map(a=>a.area));
check(parcel.id+'_private_yard_connected',connected(portions[0].cells).length===1,connected(portions[0].cells));
facts.push({name:parcel.id+'_architectural_search_components',component_column_counts:connected(portions[2].cells),interpretation:'不将碎片或搜索总量当作房间面积/居住证明。'});
}
check('gross_parcel_mask_269',all.size===269,all.size);
const publicCells=[...ifs.filter(i=>i.interface_id.includes('LANE')).flatMap(i=>i.local_geometry.cells),...ifs.find(i=>i.interface_id==='R2-IF-COMMON-EDGE').local_geometry.cells];
const pub=new Set(publicCells.map(key));
check('private_public_masks_disjoint',[...all].every(k=>!pub.has(k)),{private:all.size,public_union:pub.size});
check('direct_public_union_face_connected',connected([...pub].map(k=>k.split(',').map(Number))).length===1,connected([...pub].map(k=>k.split(',').map(Number))));
for(const parcel of p.parcels){const contacts=parcel.allocation.private_frontage_apron.cells.filter(c=>neighbors(c).some(n=>pub.has(key(n))));check(parcel.id+'_frontage_touches_public',contacts.length>0,{contact_cells:contacts});}
// 二格方形在公共并集内的平面候选只检验保护空地，不代替最终步级/碰撞设计。
const squareAnchors=[...pub].map(k=>k.split(',').map(Number)).filter(([x,z])=>[[x,z],[x+1,z],[x,z+1],[x+1,z+1]].every(c=>pub.has(key(c))));
facts.push({name:'two_by_two_public_plan_candidates',anchors:squareAnchors.length,components:connected(squareAnchors),interpretation:'平面空地候选统计；未断言沿名义中心线全程满足2格净宽。公共肩部适应需回签。'});
for(const iface of ifs){check(iface.interface_id+'_minimum_contract',['interface_id','interface_revision','source_object','source_revision','status','local_geometry','coordinate_semantic','height_or_section_baseline','nominal_width','minimum_clear_requirement','adjustment_envelope','rights_access_semantic','flow_or_service_semantic','coordination_owner','resolve_before','uncertainty'].every(k=>Object.hasOwn(iface,k)),iface.interface_revision);}
for(const b of bd.packages){check(b.package_id+'_readiness_is_explicit_concept',b.builder_handoff_readiness==='CONCEPT_DESIGN_READY'&&b.known_uncertainty.some(u=>u.resolve_before==='BEFORE_DESIGN_FREEZE'),b.readiness_reason);
check(b.package_id+'_no_world_write',b.world_write_authorization===false,false);
check(b.package_id+'_embedded_interfaces_resolve',b.required_access.every(id=>b.interface_baselines.some(i=>i.interface_id===id))&&b.interface_baselines.every(i=>ids.has(i.interface_id)),b.required_access);
for(const dep of b.dependencies){const actual=hash(fs.readFileSync(path.join(dir,dep.file)));check(b.package_id+'_direct_dependency_'+dep.file,actual===dep.sha256,{expected:dep.sha256,actual});}
check(b.package_id+'_own_services',b.external_service_interfaces.length===4,b.external_service_interfaces.map(v=>v.service_id));}
for(const s of services)check(s.service_id+'_resolvable_location',ids.has(s.interface_location_or_ref.split('#')[1])&&s.builder_responsibility==='RESERVE_INTERFACE_ONLY'&&Boolean(s.upstream_or_downstream_owner)&&Boolean(s.resolve_before),s.interface_location_or_ref);
const sourceRegister=read('sources/来源登记.json');
const repo=path.resolve(dir,'../..');
const sourceResults=[];
// 只核验白名单源文件，绝不递归扫描任何既有规划或Independent Review。
for(const s of sourceRegister.files){const location=path.join(repo,s.path);if(fs.existsSync(location)){const actual=hash(fs.readFileSync(location));sourceResults.push({path:s.path,unchanged:actual===s.sha256});}else sourceResults.push({path:s.path,unchanged:null,note:'原始源文件在此环境不可用；归档仍可独立查看'});}
check('available_allowed_sources_unchanged',sourceResults.every(s=>s.unchanged!==false),sourceResults);
const world=read('evidence/世界来源核验.json'),worldResults=[];
for(const f of world.files){const location=path.join(world.source_path,f.path);if(fs.existsSync(location))worldResults.push({path:f.path,sha256:hash(fs.readFileSync(location)),matches_initial:hash(fs.readFileSync(location))===f.sha256});}
check('available_world_files_unchanged',worldResults.every(f=>f.matches_initial),worldResults);
for(const f of ['maps/01-组团与地形.svg','maps/02-门前与公共接口.svg','maps/03-地形与门前剖面.svg']){const s=fs.readFileSync(path.join(dir,f),'utf8');check('map_present_'+f,s.includes('<svg')&&s.endsWith('</svg>'),{bytes:Buffer.byteLength(s)});}
const report={type:'ARTIFACT_CONSISTENCY_CHECKS_NOT_REGRESSION_VERDICT',regression_verdict:null,review_status:'AWAITING_GPT_AND_OWNER_REVIEW',world_writes:0,checks,derived_facts:facts,summary:{checks:checks.length,unsatisfied_checks:checks.filter(c=>!c.ok).length},not_verified:['Builder Architecture Design','真实门/楼板/楼梯/净宽与转弯碰撞','结构稳定与基础影响体积','公共接口接受、土地/通行许可','供水量/清运及运行能力','独立回归裁定']};
fs.writeFileSync(path.join(dir,'validation.json'),JSON.stringify(report,null,2)+'\n');
const list=[];
function walk(rel=''){for(const e of fs.readdirSync(path.join(dir,rel),{withFileTypes:true})){const sub=path.join(rel,e.name);if(e.isDirectory())walk(sub);else if(sub!=='manifest.json'){const b=fs.readFileSync(path.join(dir,sub));list.push({path:sub.replaceAll('\\','/'),bytes:b.length,sha256:hash(b)});}}}
walk();list.sort((a,b)=>a.path.localeCompare(b.path));fs.writeFileSync(path.join(dir,'manifest.json'),JSON.stringify({test_id:'MP-P05R2',revision:'r1',excluded_self:'manifest.json',world_writes:0,files:list},null,2)+'\n');
console.log(JSON.stringify({summary:report.summary,derived_facts:facts,artifact_files:list.length}));
if(report.summary.unsatisfied_checks)process.exitCode=1;
