import {AIR} from '../L0_公理层/资产契约.mjs';
/** 仅校验作者声明的树木/敞棚几何契约，不推断题材，不批准任何世界施工。 */
export function validateNonBuilding(bp){
 const c=bp.metadata?.asset_contract;
 if(!c||!['TREE','OPEN_SHELTER'].includes(c.kind))throw Error('INVALID_NON_BUILDING_CONTRACT');
 const m=new Map(bp.blocks.filter(v=>!AIR.has(bp.palette[v[3]])).map(v=>[v.slice(0,3).join(),bp.palette[v[3]]]));
 const point=p=>Array.isArray(p)&&p.length===3&&p.every((n,i)=>Number.isInteger(n)&&n>=0&&n<bp.dimensions[['x','y','z'][i]]);
 if(!point(c.anchor)||c.anchor[1]!==0||!m.has(c.anchor.join())||!['NORTH','EAST','SOUTH','WEST'].includes(c.front))throw Error('INVALID_ASSET_ANCHOR');
 const roots=[...m.keys()].filter(k=>k.split(',')[1]==='0'),seen=new Set(roots),q=roots.map(k=>k.split(',').map(Number));
 for(let i=0;i<q.length;i++){const p=q[i];for(const d of [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]]){const v=p.map((n,j)=>n+d[j]),k=v.join();if(m.has(k)&&!seen.has(k)){seen.add(k);q.push(v);}}}
 if(!roots.length||seen.size!==m.size)throw Error('UNROOTED_ASSET_GEOMETRY');
 if(c.kind==='TREE'){
  if(!m.get(c.anchor.join()).includes('_log[')||![...m.values()].some(s=>s.includes('_leaves[')))throw Error('TREE_ROOT_OR_CANOPY_MISSING');
 }else{
  if(!Array.isArray(c.route)||c.route.length<3)throw Error('SHELTER_ROUTE_MISSING');
  for(let i=0;i<c.route.length;i++){const p=c.route[i];if(!point(p)||p[1]!==0||m.has(p.join())||m.has([p[0],1,p[2]].join()))throw Error('SHELTER_ROUTE_BLOCKED');if(i&&p.reduce((n,v,j)=>n+Math.abs(v-c.route[i-1][j]),0)!==1)throw Error('SHELTER_ROUTE_DISCONNECTED');}
  if(!Array.isArray(c.supports)||c.supports.length<4)throw Error('SHELTER_SUPPORTS_MISSING');
  for(const p of c.supports){if(!point(p)||p[1]<2)throw Error('INVALID_SUPPORT');for(let y=0;y<=p[1];y++)if(!m.has([p[0],y,p[2]].join()))throw Error('SHELTER_SUPPORT_BROKEN');}
 }
 return {kind:c.kind,ground_contacts:roots.length,rooted_blocks:seen.size,site_ground_required:true};
}
