/* 四邻接QA只提供几何候选，不自动裁决政治有效性。水隔开的岛片可能完全合理。 */
(function(g){'use strict';
 function analyze(model,threshold=64){if(!Number.isInteger(threshold)||threshold<1)throw Error('碎片阈值应为正整数');const v=model.values,w=model.w,n=v.length,h=model.h,seen=new Uint8Array(n),queue=new Int32Array(n),areas=Array(6).fill(0),shore=Array(6).fill(0),adj=Array.from({length:6},()=>Array(6).fill(0)),parts=Array.from({length:6},()=>[]);let acceptedChanged=0;
  for(let i=0;i<n;i++){const c=v[i];if(c===255)continue;areas[c]++;if(model.accepted[i]!==255&&model.accepted[i]!==c)acceptedChanged++;
   const x=i%w,z=(i/w)|0;for(const j of [x+1<w?i+1:-1,z+1<h?i+w:-1])if(j>=0&&v[j]!==255&&v[j]!==c){adj[c][v[j]]++;adj[v[j]][c]++;}
   if(seen[i])continue;let head=0,tail=1;queue[0]=i;seen[i]=1;let water=false,edge=false,minX=x,maxX=x,minZ=z,maxZ=z,neighbors=new Set();
   while(head<tail){const q=queue[head++],qx=q%w,qz=(q/w)|0;minX=Math.min(minX,qx);maxX=Math.max(maxX,qx);minZ=Math.min(minZ,qz);maxZ=Math.max(maxZ,qz);
    for(const j of [qx>0?q-1:-1,qx+1<w?q+1:-1,qz>0?q-w:-1,qz+1<h?q+w:-1]){if(j<0){edge=true;continue;}if(v[j]===255){water=true;shore[c]++;}else if(v[j]!==c)neighbors.add(v[j]);else if(!seen[j]){seen[j]=1;queue[tail++]=j;}}
   }
   parts[c].push({area:tail,bounds:[minX+model.base.bounds[0],minZ+model.base.bounds[1],maxX+model.base.bounds[0],maxZ+model.base.bounds[1]],seed:[x+model.base.bounds[0],z+model.base.bounds[1]],touchesWater:water,touchesStudyEdge:edge,neighbors:[...neighbors].sort(),enclaveCandidate:!water&&!edge&&neighbors.size===1});
  }
  const fragmentation=parts.map((p,c)=>{p.sort((a,b)=>b.area-a.area||a.seed[1]-b.seed[1]||a.seed[0]-b.seed[0]);return {category:c,components:p.length,largestArea:p[0]?.area||0,secondaryComponents:Math.max(0,p.length-1),smallComponents:p.filter(q=>q.area<threshold).length,smallArea:p.filter(q=>q.area<threshold).reduce((n,q)=>n+q.area,0),enclaveCandidates:p.filter(q=>q.enclaveCandidate).length,topComponents:p.slice(0,20),smallExamples:p.filter(q=>q.area<threshold).slice(0,20),enclaveExamples:p.filter(q=>q.enclaveCandidate).slice(0,20)};});
  return {revision:model.revision,landColumns:areas.reduce((a,b)=>a+b,0),areas,unassigned:areas[4],disputed:areas[5],acceptedChanged,adjacency:adj,shoreEdges:shore,fragmentation,threshold,method:'4-neighbor; adjacency counts shared unit land edges; water crossings excluded. Enclave candidate: no water/study edge and exactly one surrounding other class. Fragment: area<threshold; disconnected areas may be natural islands. UNASSIGNED/DISPUTED are explicit classes, not errors repaired automatically.'};
 }
 g.TerritoryQA=analyze;if(typeof module!=='undefined')module.exports=analyze;
})(globalThis);
