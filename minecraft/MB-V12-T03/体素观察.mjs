/** 保存体素的独立光线投射。用基本包围盒表达台阶、半砖与近地植物，不访问游戏。 */
import fs from 'node:fs';
const cfg=JSON.parse(fs.readFileSync(process.argv[2],'utf8')),vox=fs.readFileSync(cfg.volume),[nx,ny,nz]=cfg.size,[w,h]=cfg.res,eye=cfg.eye.slice();eye[1]-=cfg.y0;
const unit=v=>{const l=Math.hypot(...v);return v.map(t=>t/l)},cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],forward=unit(cfg.target.map((a,i)=>a-(i===1?cfg.y0:0)-eye[i])),right=unit(cross(forward,[0,1,0])),up=cross(right,forward),spread=2*Math.tan(cfg.fov*Math.PI/360);
const get=(x,y,z)=>x>=0&&x<nx&&y>=0&&y<ny&&z>=0&&z<nz?vox[(x*ny+y)*nz+z]:-1;
const shapes=cfg.palette.map(s=>{
 if(s.includes(':air')||s.includes(':cave_air'))return[];
 if(s.includes('_stairs')){let upper=s.includes('facing=east')?[.5,.5,0,1,1,1]:s.includes('facing=west')?[0,.5,0,.5,1,1]:s.includes('facing=south')?[0,.5,.5,1,1,1]:[0,.5,0,1,1,.5];return[[0,0,0,1,.5,1],upper]}
 if(s.includes('_slab'))return[[0,0,0,1,.5,1]];
 if(s.includes('_fence')){const b=[[.38,0,.38,.62,1,.62]];if(s.includes('east=true'))b.push([.5,.4,.44,1,.6,.56]);if(s.includes('west=true'))b.push([0,.4,.44,.5,.6,.56]);if(s.includes('south=true'))b.push([.44,.4,.5,.56,.6,1]);if(s.includes('north=true'))b.push([.44,.4,0,.56,.6,.5]);return b;}
 if(s.includes(':torch'))return[[.43,0,.43,.57,.7,.57]];
 if(/:(short_grass|fern|wheat|oxeye_daisy|poppy)/.test(s))return[[.12,0,.47,.88,.75,.53],[.47,0,.12,.53,.75,.88]];
 if(s.includes(':water'))return[[0,0,0,1,.88,1]];
 return[[0,0,0,1,1,1]];
});
const out=Buffer.alloc(w*h*3),[ex,ey,ez]=eye;
for(let py=0;py<h;py++)for(let px=0;px<w;px++){
 const u=(px+.5-w/2)/w*spread,v=(h/2-py-.5)/w*spread,d=unit(forward.map((a,i)=>a+right[i]*u+up[i]*v)).map(x=>Math.abs(x)<1e-8?1e-8:x),[dx,dy,dz]=d;
 let begin=0,end=1000;for(let a=0;a<3;a++){const t0=-eye[a]/d[a],t1=([nx,ny,nz][a]-eye[a])/d[a];begin=Math.max(begin,Math.min(t0,t1));end=Math.min(end,Math.max(t0,t1));}
 let t=begin+1e-5,rgb=[179,202,217];
 for(let k=0;k<800&&t<end;k++){
  const x=Math.floor(ex+dx*t),y=Math.floor(ey+dy*t),z=Math.floor(ez+dz*t),id=get(x,y,z);if(id<0)break;
  const tx=(x+(dx>0?1:0)-ex)/dx,ty=(y+(dy>0?1:0)-ey)/dy,tz=(z+(dz>0?1:0)-ez)/dz,step=Math.min(tx,ty,tz);let nearest=1e9,axis=1;
  for(const b of shapes[id]){
   let enter=-1e9,leave=1e9,face=1;
   for(let a=0;a<3;a++){let q0=([x,y,z][a]+b[a]-eye[a])/d[a],q1=([x,y,z][a]+b[a+3]-eye[a])/d[a];const lo=Math.min(q0,q1);if(lo>enter){enter=lo;face=a}leave=Math.min(leave,Math.max(q0,q1));}
   if(leave>=Math.max(enter,t-1e-4)&&enter<=step+1e-4&&enter<nearest){nearest=Math.max(t,enter);axis=face;}
  }
  if(nearest<1e8){
   const q=[ex+dx*nearest,ey+dy*nearest,ez+dz*nearest];let shade=[.78,1.03,.90][axis]*(1+.028*Math.sin(x*13+y*23+z*17));
   let shadow=false;for(const dist of [1,3,6,11,18]){const a=get(Math.floor(q[0]-dx*.03-dist*.5),Math.floor(q[1]-dy*.03+dist*.83),Math.floor(q[2]-dz*.03+dist*.22));if(a>=0&&shapes[a].length&& !/grass|wheat|flower|fern|water/.test(cfg.palette[a])){shadow=true;break;}}
   if(shadow)shade*=.72;
   const fog=Math.min(.20,nearest/850);rgb=cfg.colors[id].map((c,i)=>c*shade*(1-fog)+[179,202,217][i]*fog);break;
  }
  t=step+1e-5;
 }
 for(let a=0;a<3;a++)out[(py*w+px)*3+a]=Math.min(255,Math.max(0,Math.round(rgb[a])));
}
fs.writeFileSync(cfg.output,Buffer.concat([Buffer.from(`P6\n${w} ${h}\n255\n`),out]));
