// 针对本任务的只读体素光线投射；不读取或写入 Minecraft 存档。
import fs from 'node:fs';
const c=JSON.parse(fs.readFileSync(process.argv[2],'utf8')),v=fs.readFileSync(c.volume),[W,H,D]=c.size,[w,h]=c.res,out=Buffer.alloc(w*h*3),e=c.eye.slice();e[1]-=63;
const norm=a=>{let s=Math.hypot(...a);return a.map(x=>x/s);},cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const f=norm(c.target.map((x,i)=>x-(i===1?63:0)-e[i])),right=norm(cross(f,[0,1,0])),up=cross(right,f),scale=2*Math.tan(c.fov*Math.PI/360),get=(x,y,z)=>x>=0&&x<W&&y>=0&&y<H&&z>=0&&z<D?v[(x*H+y)*D+z]:-1;
for(let py=0;py<h;py++)for(let px=0;px<w;px++){
 const u=(px+.5-w/2)/w*scale,b=(h/2-py-.5)/w*scale,r=norm(f.map((a,i)=>a+u*right[i]+b*up[i])).map(a=>Math.abs(a)<1e-9?1e-9:a),rx=r[0],ry=r[1],rz=r[2],ex=e[0],ey=e[1],ez=e[2];
 let t=0,end=1e6,axis=1;
 for(let a=0;a<3;a++){let lo=(0-e[a])/r[a],hi=([W,H,D][a]-e[a])/r[a];t=Math.max(t,Math.min(lo,hi));end=Math.min(end,Math.max(lo,hi));}
 t+=1e-5;let col=[177+8-17*py/h,200+8-17*py/h,213+8-17*py/h];
 for(let step=0;step<650&&t<end;step++){
  const qx=ex+rx*t,qy=ey+ry*t,qz=ez+rz*t,ax=Math.floor(qx),ay=Math.floor(qy),az=Math.floor(qz),id=get(ax,ay,az);if(id<0)break;
  if(!c.air[id]){
   const p=[qx,qy,qz],a=[ax,ay,az];
   let shade=[.76,1.04,.87][axis]*(1+.035*Math.sin(a[0]*17+a[1]*23+a[2]*31));
   const other=[0,1,2].filter(i=>i!==axis);if(other.some(i=>p[i]-a[i]<.025))shade*=.84;
   let shadow=false;
   for(const k of [.5,1.5,3,5,8,12,18,26]){const q=p.map((a,i)=>Math.floor(a-r[i]*.02+[-.50,.83,.24][i]*k)),s=get(...q);if(s>=0&&!c.air[s]){shadow=true;break;}}
   if(shadow)shade*=.70;let fog=Math.min(.30,t/650);col=c.colors[id].map((a,i)=>a*shade*(1-fog)+[177,200,213][i]*fog);break;
  }
  const tx=(ax+(rx>0?1:0)-ex)/rx,ty=(ay+(ry>0?1:0)-ey)/ry,tz=(az+(rz>0?1:0)-ez)/rz;
  if(tx<ty&&tx<tz){axis=0;t=tx+1e-5;}else if(ty<tz){axis=1;t=ty+1e-5;}else{axis=2;t=tz+1e-5;}
 }
 for(let a=0;a<3;a++)out[(py*w+px)*3+a]=Math.max(0,Math.min(255,Math.round(col[a])));
}
fs.writeFileSync(c.output,Buffer.concat([Buffer.from(`P6\n${w} ${h}\n255\n`),out]));
