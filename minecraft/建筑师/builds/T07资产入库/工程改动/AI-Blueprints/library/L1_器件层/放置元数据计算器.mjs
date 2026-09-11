import {AIR,bounds,point,direction,dimensions} from '../L0_公理层/资产契约.mjs';
import {validateNonBuilding} from './非房屋资产校验器.mjs';
const DIR={NORTH:[0,-1],EAST:[1,0],SOUTH:[0,1],WEST:[-1,0]};
/** 只变换只读放置契约，不构造 Blueprint、不省略实体位置、不宣称状态获得部署权限。 */
export function fitVariants(p){
 const out=[];for(const rotation of p.rotation_allowed)for(const mirror of p.mirror_allowed?['none','x','z']:['none']){
  const move=v=>point(v,p.dimensions,rotation,mirror),corners=b=>{const vs=[];for(const x of[b.x1,b.x2])for(const y of[b.y1,b.y2])for(const z of[b.z1,b.z2])vs.push(move([x,y,z]));return bounds(vs);};
  out.push({rotation,mirror,dimensions:dimensions(p.dimensions,rotation),front_direction:direction(p.front_direction,rotation,mirror),anchor:{...p.anchor,position:move(p.anchor.position)},footprint_mask:p.footprint_mask.map(([x,z])=>{const v=move([x,0,z]);return[v[0],v[2]];}),ground_contact_mask:p.ground_contact_mask.map(move),ground_plane_y:p.ground_plane_y,clearance_bounds:corners(p.clearance_bounds),occupied_bounds:corners(p.occupied_bounds)});
 }return out;
}
/** 门朝向仅作候选；外向射线和最低入口层共同限定证据，歧义保留 UNKNOWN。 */
export function placementOf(bp,ref){
 const occupied=bp.blocks.filter(v=>!AIR.has(bp.palette[v[3]])),box=bounds(occupied),map=new Map(bp.blocks.map(v=>[v.slice(0,3).join(),bp.palette[v[3]]])),foot=new Map();
 for(const[x,y,z]of occupied){const key=[x,z].join();if(!foot.has(key)||y<foot.get(key)[1])foot.set(key,[x,y,z]);}
 const contact=[...foot.values()].filter(v=>v[1]===box.y1),candidates=[];
 const pass=s=>AIR.has(s)||/_door\[|:short_grass|:tall_grass/.test(s);
 const get=(x,y,z)=>map.get([x,y,z].join())||'minecraft:air';
 for(const[x,y,z,p]of occupied){const s=bp.palette[p];if(!/_door\[/.test(s)||!s.includes('half=lower'))continue;
  for(const[front,[dx,dz]]of Object.entries(DIR)){
   const facing=s.match(/facing=([a-z]+)/)?.[1];if((dx!==0)!==['east','west'].includes(facing))continue;
   let clear=true;for(let n=1;n<=Math.max(bp.dimensions.x,bp.dimensions.z);n++){const xx=x+dx*n,zz=z+dz*n;if(xx<0||zz<0||xx>=bp.dimensions.x||zz>=bp.dimensions.z)break;if(!pass(get(xx,y,zz))||!pass(get(xx,y+1,zz))){clear=false;break;}}
   const support=get(x,y-1,z);if(clear&&!AIR.has(support))candidates.push({position:[x,y,z],front_direction:front,basis:'lower door + support + two-block outward ray',confidence:0.86});
  }
 }
 let entrance=null,front='UNKNOWN',confidence=0;const lowest=candidates.length?Math.min(...candidates.map(c=>c.position[1])):null,primary=candidates.filter(c=>c.position[1]===lowest);
 // 同层同向连续双门视为一个入口；不把分离的多个入口强行合并。
 if(primary.length&&new Set(primary.map(c=>c.front_direction)).size===1){const p=primary.map(c=>c.position),b=bounds(p);if(b.x2-b.x1<=1&&b.z2-b.z1<=1){front=primary[0].front_direction;confidence=.86;entrance=[(b.x1+b.x2)/2,b.y1,(b.z1+b.z2)/2];}}
 const anchor=entrance?{type:'ENTRANCE_GROUND_CENTER',position:entrance,coordinate_space:'blueprint_local',surface:'feet above supporting block'}:{type:'BLUEPRINT_ORIGIN',position:[0,0,0],coordinate_space:'blueprint_local',fallback_reason:'主入口/正面证据不唯一；不采用未经确认的 proxy 朝向'};
 // 无门原创资产使用已校验的显式根部/柱脚锚点，绝不伪装成门洞识别结果。
 if(ref.source_kind==='AI_ORIGINAL'&&bp.metadata?.asset_contract){validateNonBuilding(bp);const c=bp.metadata.asset_contract;front=c.front;confidence=1;Object.assign(anchor,{type:'AUTHORED_GROUND_CONTACT',position:c.anchor,surface:'lowest occupied block; supporting terrain required below',fallback_reason:null});}
 const v=ref.classification_v2,terrainTags=v.terrain_fit.map(x=>x.tag);const special=v.structure_type==='ship'||v.primary_use==='transport'||terrainTags.some(t=>['water','cliff','floating','flexible'].includes(t));
 const mode=special?'CUSTOM_REQUIRED':terrainTags.includes('gentle_slope')?'FOUNDATION_FILL':'RIGID';
 return{dimensions:bp.dimensions,occupied_blocks:occupied.length,front_direction:front,front_confidence:confidence,front_evidence:primary,previous_front_candidate:v.evidence?.normalized_geometry,anchor,anchor_type:anchor.type,entrance_candidates:candidates,footprint:{coordinate_space:'blueprint_local',encoding:'explicit x,z cells',definition:'all non-air vertical projection including roof overhangs',footprint_mask:[...foot.values()].map(([x,y,z])=>[x,z]),bounds:{x1:box.x1,x2:box.x2,z1:box.z1,z2:box.z2}},footprint_mask:[...foot.values()].map(([x,y,z])=>[x,z]),ground_contact_mask:contact,ground_contact_definition:'lowest occupied blueprint plane only; entries x,y,z; not all hanging column bottoms',ground_plane_y:box.y1,occupied_bounds:box,clearance_bounds:{x1:box.x1-1,y1:box.y1,z1:box.z1-1,x2:box.x2+1,y2:box.y2+1,z2:box.z2+1},clearance_margin:{horizontal:1,top:1,bottom:0},rotation_allowed:[0,90,180,270],mirror_allowed:true,terrain_mode:mode,terrain_contract:mode==='FOUNDATION_FILL'?'body rigid; future support fill max 2 blocks, no current adaptation':mode==='CUSTOM_REQUIRED'?'requires explicit site/anchor review':'body rigid; translation only, no terrain deformation',recommended_use:v.primary_use,secondary_use:v.secondary_use,styles:v.styles.map(s=>s.tag),scale:v.scale};
}
