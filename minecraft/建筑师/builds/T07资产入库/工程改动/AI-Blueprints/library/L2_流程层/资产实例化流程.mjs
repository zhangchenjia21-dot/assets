import {point,direction,dimensions,requireTransform,AIR,bounds} from '../L0_公理层/资产契约.mjs';
import {contentPolicy,contentOmission} from '../L1_器件层/实体内容省略器.mjs';
/** 原资产不动；返回同一 Canonical Schema 的实例。省略项必须逐坐标列出，预览不等于批准。 */
export function instantiate(bundle,native,options={},capability){
 const{asset,placement:p,blueprint:bp}=bundle,{rotation=0,mirror='none',geometry_only=false,preview_only=false,target_anchor=null}=options;requireTransform(rotation,mirror);
 if(asset.status==='NOT_DEPLOYABLE')throw Error('ASSET_NOT_DEPLOYABLE');if(asset.status==='NEEDS_REVIEW'&&!preview_only)throw Error('ASSET_NEEDS_REVIEW');
 if(asset.geometry_only_required&&!geometry_only)throw Error('EXPLICIT_GEOMETRY_ONLY_REQUIRED');if(!asset.rotation_allowed.includes(rotation)||mirror!=='none'&&!asset.mirror_allowed)throw Error('TRANSFORM_NOT_ALLOWED');
 const states=native.ensure(bp.palette),content=contentPolicy(bp,states,capability),verified=new Set(capability.verified_states),palette=[],index=new Map(),blocks=[],omitted=[],contentOmissions=[];const remap=s=>{if(!index.has(s)){index.set(s,palette.length);palette.push(s);}return index.get(s);};
 // 证明被撤回后不得继续使用旧 READY 状态；显式 geometry-only 仍保留原有受限预览能力。
 if(!geometry_only&&(content.unsafe.length||content.non_block_entity_payload))throw Error('EXPLICIT_GEOMETRY_ONLY_REQUIRED');
 for(const[x,y,z,i]of bp.blocks){const source=bp.palette[i],row=states[source],position=point([x,y,z],bp.dimensions,rotation,mirror);if(!row?.valid)throw Error('UNRESOLVED_BLOCK:'+source);const transformed=row.variants[rotation+'/'+mirror];
  if(row.block_entity){if(!verified.has(transformed)){if(!geometry_only)throw Error('UNVERIFIED_BASE_ENTITY_STATE');omitted.push({source_position:[x,y,z],instance_position:position,state:source,reason:'BLOCK_ENTITY_UNSUPPORTED'});continue;}contentOmissions.push(contentOmission([x,y,z],position,transformed));}
  blocks.push([...position,remap(transformed)]);
 }
 const anchor=point(p.anchor.position,bp.dimensions,rotation,mirror);let origin={x:0,y:0,z:0};if(target_anchor){if(target_anchor.length!==3||target_anchor.some(n=>!Number.isFinite(n)))throw Error('INVALID_TARGET_ANCHOR');origin=Object.fromEntries(['x','y','z'].map((k,i)=>[k,target_anchor[i]-anchor[i]]));if(Object.values(origin).some(n=>!Number.isInteger(n)))throw Error('ANCHOR_ALIGNMENT_REQUIRES_INTEGER_TRANSLATION');}
 const d=dimensions(bp.dimensions,rotation),occupied=blocks.filter(v=>!AIR.has(palette[v[3]])),occupiedBounds=bounds(occupied),columns=new Map();
 for(const[x,y,z]of occupied){const k=[x,z].join();if(!columns.has(k)||columns.get(k)[1]>y)columns.set(k,[x,y,z]);}
 const mask=[...columns.values()].map(([x,y,z])=>[x,z]),contact=[...columns.values()].filter(v=>v[1]===occupiedBounds.y1);
 const corners=[];for(const x of[p.clearance_bounds.x1,p.clearance_bounds.x2])for(const y of[p.clearance_bounds.y1,p.clearance_bounds.y2])for(const z of[p.clearance_bounds.z1,p.clearance_bounds.z2])corners.push(point([x,y,z],bp.dimensions,rotation,mirror));
 const placement={...p,dimensions:d,occupied_blocks:occupied.length,front_direction:direction(p.front_direction,rotation,mirror),anchor:{...p.anchor,position:anchor},entrance_candidates:p.entrance_candidates.map(c=>({...c,position:point(c.position,bp.dimensions,rotation,mirror),front_direction:direction(c.front_direction,rotation,mirror)})),footprint_mask:mask,ground_contact_mask:contact,ground_plane_y:occupiedBounds.y1,clearance_bounds:bounds(corners),occupied_bounds:occupiedBounds,footprint:{...p.footprint,footprint_mask:mask,bounds:{x1:occupiedBounds.x1,x2:occupiedBounds.x2,z1:occupiedBounds.z1,z2:occupiedBounds.z2}},origin};
 const instance={schema_version:1,origin,dimensions:d,rotation:0,mirror:'none',palette,blocks,metadata:{name:asset.name,block_state_data_version:asset.minecraft_data_version,asset_status:'ASSET_INSTANCE',asset_instance:{asset_id:asset.asset_id,source_ref_id:asset.source_ref_id,source_sha256:asset.blueprint_sha256,rotation,mirror,transform_order:'mirror then clockwise rotation; baked coordinates and native states',geometry_only,omitted_block_entities:omitted,auxiliary_payloads:'not deployed; retained verbatim in asset blueprint.json under original source coordinates',site_approval_required:true,preview_only},litematica:{minecraft_data_version:asset.minecraft_data_version,top_level_tags:{Metadata:{type:10,value:{Author:{type:8,value:bundle.source.author||'unknown'}}}},warnings:asset.warnings.map(w=>({code:w.code,message:w.policy||w.reason||w.code}))}}};
 if(asset.source_kind==='AI_ORIGINAL'&&bp.metadata.asset_contract){
  const c=bp.metadata.asset_contract,move=v=>point(v,bp.dimensions,rotation,mirror);
  // 无门构件的根部、净空路线和支柱顶点必须与方块一起变换。
  instance.metadata.asset_contract={...c,anchor:move(c.anchor),front:direction(c.front,rotation,mirror),...(c.route?{route:c.route.map(move)}:{}),...(c.supports?{supports:c.supports.map(move)}:{})};
 }else if(asset.source_kind==='AI_ORIGINAL'){
  const move=v=>point(v,bp.dimensions,rotation,mirror),f=bp.metadata.functional;
  instance.logical_components=bp.logical_components;
  instance.metadata.component_map=Object.fromEntries(Object.entries(bp.metadata.component_map).map(([k,v])=>[move(k.split(',').map(Number)).join(),v]));
  instance.metadata.functional={...f,entrance:move(f.entrance),floors:f.floors.map(v=>({...v,anchor:move(v.anchor)})),routes:f.routes.map(move),supports:f.supports.map(([x,z,a,b])=>{const p=move([x,a,z]);return[p[0],p[2],a,b];}),stairs:f.stairs.map(s=>{
   const facing=direction(s.facing.toUpperCase(),rotation,mirror).toLowerCase(),start=move(s.start),end=move([s.start[0]+(['north','south'].includes(s.facing)?s.width-1:0),s.start[1],s.start[2]+(['east','west'].includes(s.facing)?s.width-1:0)]);
   if(['north','south'].includes(facing))start[0]=Math.min(start[0],end[0]);else start[2]=Math.min(start[2],end[2]);return{...s,start,facing};
  })};
  // 原创标注随几何一起变换；不能在实例化时丢失已通过的功能契约。
 }
 instance.metadata.content_omissions=contentOmissions;instance.metadata.auxiliary_content_omissions=content.auxiliary;
 instance.metadata.asset_instance.base_entity_policy=capability.policy_version;
 return{blueprint:instance,placement,omissions:omitted,content_omissions:contentOmissions,auxiliary_content_omissions:content.auxiliary,asset_id:asset.asset_id,deployable:!preview_only&&asset.status!=='NEEDS_REVIEW',world_writes:0};
}
/** 分析给定 heightmap，绝不自动填地或替换地形；缺少列数据必须报错。 */
export function analyzeTerrain(instance,heightmap){
 const p=instance.placement,o=instance.blueprint.origin,b=heightmap.bounds,dx=b.x2-b.x1+1,gaps=[];
 for(const[x,y,z]of p.ground_contact_mask){const xx=x+o.x,zz=z+o.z;if(xx<b.x1||xx>b.x2||zz<b.z1||zz>b.z2)throw Error('HEIGHTMAP_COVERAGE_INCOMPLETE');const surface=heightmap.heights[(zz-b.z1)*dx+xx-b.x1];if(!Number.isFinite(surface))throw Error('HEIGHTMAP_COVERAGE_INCOMPLETE');gaps.push({x:xx,z:zz,support_gap:y+o.y-1-surface});}
 const fill=gaps.filter(v=>v.support_gap>0),cut=gaps.filter(v=>v.support_gap<0);return{asset_id:instance.asset_id,terrain_mode:p.terrain_mode,contact_cells:gaps.length,max_fill:Math.max(0,...fill.map(v=>v.support_gap)),max_cut:Math.max(0,...cut.map(v=>-v.support_gap)),status:p.terrain_mode==='CUSTOM_REQUIRED'?'CUSTOM_REQUIRED':cut.length||fill.length?'NEEDS_SITE_REVIEW':'CONTACT_ALIGNED',gaps,world_writes:0,limitation:'heightmap contact only; trees/structures/clearance still require full live scan'};
}
