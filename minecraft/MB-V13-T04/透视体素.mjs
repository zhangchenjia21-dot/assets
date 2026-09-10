/** 从只读体素生成几何审计图。非客户端渲染，不合成设计中不存在的结构。 */
import fs from 'node:fs';const c=JSON.parse(fs.readFileSync(process.argv[2],'utf8').replace(/^\uFEFF/,'')),v=fs.readFileSync(c.volume),[W,H,D]=c.size,[rw,rh]=c.res;
const unit=a=>{const l=Math.hypot(...a);return a.map(x=>x/l)},cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const forward=unit(c.target.map((x,i)=>x-c.eye[i])),right=unit(cross(forward,[0,1,0])),up=cross(right,forward),scale=Math.tan(c.fov*Math.PI/360),eye=[c.eye[0],c.eye[1]-c.y0,c.eye[2]],sun=unit([-0.7,1,-0.5]);
function intersect(o,d,b){let lo=-Infinity,hi=Infinity,n=[0,1,0];for(let i=0;i<3;i++){if(Math.abs(d[i])<1e-8){if(o[i]<b[i]||o[i]>b[i+3])return null;continue;}let a=(b[i]-o[i])/d[i],z=(b[i+3]-o[i])/d[i],nn=[0,0,0];nn[i]=d[i]>0?-1:1;if(a>z)[a,z]=[z,a];if(a>lo){lo=a;n=nn;}hi=Math.min(hi,z);if(lo>hi)return null;}return hi<0?null:{t:Math.max(lo,0),n};}
const shapes=c.palette.map(p=>{
 if(/:(air|cave_air|void_air)$/.test(p))return [];
 if(/short_grass|fern|oxeye_daisy|torch/.test(p))return [[.15,0,.46,.85,.65,.54],[.46,0,.15,.54,.65,.85]];
 if(p.includes('_slab'))return [[0,0,0,1,.5,1]];
 if(p.includes('_stairs')){const b=[0,0,0,1,.5,1];let t=[0,.5,0,1,1,1];if(p.includes('facing=north'))t[5]=.5;else if(p.includes('facing=south'))t[2]=.5;else if(p.includes('facing=east'))t[0]=.5;else t[3]=.5;return[b,t];}
 if(p.includes('_fence')){const a=[[.375,0,.375,.625,1.5,.625]];for(const y of [.375,.8]){if(p.includes('east=true'))a.push([.5,y,.43,1,y+.15,.57]);if(p.includes('west=true'))a.push([0,y,.43,.5,y+.15,.57]);if(p.includes('north=true'))a.push([.43,y,0,.57,y+.15,.5]);if(p.includes('south=true'))a.push([.43,y,.5,.57,y+.15,1]);}return a;}
 return [[0,0,0,1,1,1]];
});
function ray(o,d,max=700,shadow=false){const entry=intersect(o,d,[0,0,0,W,H,D]);if(!entry)return null;let t=entry.t+1e-5;let pos=o.map((x,i)=>x+d[i]*t),cell=pos.map(Math.floor),step=d.map(x=>x>0?1:-1),delta=d.map(x=>Math.abs(1/x));let next=d.map((x,i)=>t+((x>0?cell[i]+1:cell[i])-pos[i])/x);
 for(let it=0;it<1000&&t<max;it++){
  const[x,y,z]=cell;if(x<0||x>=W||y<0||y>=H||z<0||z>=D)return null;const p=v[(x*H+y)*D+z];
  if(shapes[p].length&&!(shadow&&/short_grass|fern|oxeye/.test(c.palette[p]))){let best=null;for(const b of shapes[p]){const hit=intersect(o,d,b.map((q,i)=>q+cell[i%3]));if(hit&&hit.t>=t-1e-4&&(!best||hit.t<best.t))best=hit;}if(best)return{...best,p,cell};}
  let a=next[0]<next[1]?(next[0]<next[2]?0:2):(next[1]<next[2]?1:2);t=next[a];cell[a]+=step[a];next[a]+=delta[a];
 }return null;}
const out=Buffer.alloc(rw*rh*3);
for(let y=0;y<rh;y++)for(let x=0;x<rw;x++){
 const sx=(2*(x+.5)/rw-1)*scale*rw/rh,sy=(1-2*(y+.5)/rh)*scale,d=unit(forward.map((a,i)=>a+sx*right[i]+sy*up[i]));const h=ray(eye,d);let col=[173,199,208];
 if(h){const point=eye.map((a,i)=>a+d[i]*h.t+h.n[i]*.006);const shade=ray(point,sun,80,true)?0.72:1;const light=(.64+.36*Math.max(0,h.n.reduce((a,b,i)=>a+b*sun[i],0)))*shade;col=c.colors[h.p].map(q=>q*light);const fog=Math.min(.15,h.t/1500);col=col.map((a,i)=>a*(1-fog)+[173,199,208][i]*fog);}
 const k=(y*rw+x)*3;for(let i=0;i<3;i++)out[k+i]=Math.max(0,Math.min(255,Math.round(col[i])));
}
fs.writeFileSync(c.output,Buffer.concat([Buffer.from(`P6\n${rw} ${rh}\n255\n`),out]));
