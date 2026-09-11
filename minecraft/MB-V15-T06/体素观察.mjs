/** 仅渲染给定实存/设计体素；软件几何近似，不是客户端截图或物理模拟。 */
import fs from 'node:fs';const c=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));const V=fs.readFileSync(c.volume),[W,H,D]=c.size,[rw,rh]=c.res,P=c.palette,colors=c.colors;
const norm=v=>{const l=Math.hypot(...v);return v.map(x=>x/l)},cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const F=norm(c.target.map((x,i)=>x-c.eye[i])),R=norm(cross(F,[0,1,0])),U=cross(R,F),scale=Math.tan(c.fov*Math.PI/360);const eye=[c.eye[0],c.eye[1]-56,c.eye[2]];
const empty=P.map(p=>p.includes(':air')||p.includes(':cave_air'));const shapes=P.map(p=>p.includes('moss_carpet')?[0,0,0,1,.0625,1]:p.includes('_slab')?[0,0,0,1,.5,1]:p.includes('tulip')||p.includes('cornflower')?[.22,0,.22,.78,.8,.78]:p.includes(':fern')?[.1,0,.1,.9,.7,.9]:[0,0,0,1,1,1]);
function intersect(o,d,min,max){let lo=-Infinity,hi=Infinity;for(let i=0;i<3;i++){if(Math.abs(d[i])<1e-9){if(o[i]<min[i]||o[i]>max[i])return null;continue;}let a=(min[i]-o[i])/d[i],b=(max[i]-o[i])/d[i];if(a>b)[a,b]=[b,a];lo=Math.max(lo,a);hi=Math.min(hi,b);}return hi>=Math.max(0,lo)?[Math.max(0,lo),hi]:null;}
function ray(o,d){const bounds=intersect(o,d,[0,0,0],[W,H,D]);if(!bounds)return null;let t=bounds[0]+1e-6,pos=o.map((x,i)=>x+d[i]*t),cell=pos.map(Math.floor),step=d.map(Math.sign),delta=d.map(x=>Math.abs(1/x));let next=d.map((x,i)=>t+((cell[i]+(x>0?1:0))-pos[i])/x),face=1;
 for(let it=0;it<1000&&t<bounds[1]&&cell[0]>=0&&cell[0]<W&&cell[1]>=0&&cell[1]<H&&cell[2]>=0&&cell[2]<D;it++){
  const p=V[(cell[0]*H+cell[1])*D+cell[2]];
  if(!empty[p]){const s=shapes[p],hit=intersect(o,d,cell.map((x,i)=>x+s[i]),cell.map((x,i)=>x+s[i+3]));if(hit&&hit[0]<=Math.min(...next)+1e-5)return {p,t:hit[0],face,cell};}
  face=next[0]<next[1]?(next[0]<next[2]?0:2):(next[1]<next[2]?1:2);t=next[face];cell[face]+=step[face];next[face]+=delta[face];
 }return null;
}
const out=Buffer.alloc(rw*rh*3);for(let y=0;y<rh;y++)for(let x=0;x<rw;x++){
 const u=((x+.5)/rw*2-1)*scale*rw/rh,v=(1-(y+.5)/rh*2)*scale,d=norm(F.map((a,i)=>a+R[i]*u+U[i]*v)),hit=ray(eye,d);let rgb=[183,207,214];
 if(hit){const {p,face,t}=hit;let k=[.77,1,.88][face];const point=eye.map((a,i)=>a+d[i]*t);point[face]-=Math.sign(d[face])*.025;
  const sun=ray(point,norm([-.4,1,-.3]));if(sun&&sun.t<65)k*=.72;
  const fog=Math.min(.2,t/1500);rgb=colors[p].map((a,i)=>a*k*(1-fog)+rgb[i]*fog);
 }
 const k=(y*rw+x)*3;for(let j=0;j<3;j++)out[k+j]=Math.max(0,Math.min(255,Math.round(rgb[j])));
}fs.writeFileSync(c.output,Buffer.concat([Buffer.from(`P6\n${rw} ${rh}\n255\n`),out]));
