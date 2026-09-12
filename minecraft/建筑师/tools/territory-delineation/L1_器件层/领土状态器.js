/* 只拥有内存草稿。工具绘制受源/目标类别锁约束；撤销恢复自己完整的历史事务。 */
(function(g){'use strict';const C=g.TerritoryContract||(typeof require==='function'?require('../L0_公理层/领土契约.js'):null);
 class Model{
  constructor(base){this.base=base;this.w=base.width;this.h=base.height;this.n=this.w*this.h;const bytes=Uint8Array.from(atob(base.landBits),v=>v.charCodeAt(0));if(bytes.length!==Math.ceil(this.n/8))throw Error('陆地mask长度错误');this.values=new Uint8Array(this.n);this.accepted=new Uint8Array(this.n);this.accepted.fill(255);this.landCount=0;
   for(let i=0;i<this.n;i++){const land=(bytes[i>>3]>>(i&7))&1;this.values[i]=land?4:255;this.landCount+=land;}if(this.landCount!==base.landCount)throw Error('陆地面积不匹配');
   for(const [runs,code] of [[base.commons,0],[base.connector,2]])for(const [z,a,b]of runs)for(let x=a;x<=b;x++){const i=this.index(x,z);if(i<0||this.values[i]===255||this.accepted[i]!==255)throw Error('accepted geometry不属于有效陆地或重叠');this.values[i]=code;this.accepted[i]=code;}
   this.locks=[true,false,true,false,false,false];this.undoStack=[];this.redoStack=[];this.marks=new Uint32Array(this.n);this.token=0;this.revision=0;this.trimmed=0;
  }
  index(x,z){const xx=x-this.base.bounds[0],zz=z-this.base.bounds[1];return Number.isInteger(x)&&Number.isInteger(z)&&xx>=0&&zz>=0&&xx<this.w&&zz<this.h?zz*this.w+xx:-1;}
  begin(code){if(this.pending)throw Error('已有未完成笔画');if(!C.validCode(code))throw Error('未知领土类别');if(++this.token===0xffffffff){this.marks.fill(0);this.token=1;}this.pending={code,ids:[],old:[]};}
  set(x,z){const i=this.index(x,z),p=this.pending;if(!p)throw Error('缺少事务');if(i<0||this.values[i]===255||this.values[i]===p.code||this.locks[this.values[i]]||this.locks[p.code])return false;
   if(this.marks[i]!==this.token){this.marks[i]=this.token;p.ids.push(i);p.old.push(this.values[i]);}this.values[i]=p.code;return true;}
  brush(x,z,r){let changed=0;const rr=Math.max(0,r-1);for(let dz=-rr;dz<=rr;dz++)for(let dx=-rr;dx<=rr;dx++)if(dx*dx+dz*dz<=rr*rr)changed+=this.set(x+dx,z+dz);return changed;}
  rectangle(x0,z0,x1,z1){const b=this.base.bounds;let changed=0;for(let z=Math.max(b[1],Math.min(z0,z1));z<=Math.min(b[3],Math.max(z0,z1));z++)for(let x=Math.max(b[0],Math.min(x0,x1));x<=Math.min(b[2],Math.max(x0,x1));x++)changed+=this.set(x,z);return changed;}
  end(){const p=this.pending;this.pending=null;if(!p||!p.ids.length)return 0;const ids=Uint32Array.from(p.ids),before=Uint8Array.from(p.old),after=Uint8Array.from(ids,i=>this.values[i]);this.undoStack.push({ids,before,after});this.redoStack=[];this.revision++;this.limitHistory();return ids.length;}
  limitHistory(){let bytes=this.undoStack.reduce((n,a)=>n+a.ids.length*6,0);while(this.undoStack.length>1&&(bytes>24*1024*1024||this.undoStack.length>100)){bytes-=this.undoStack.shift().ids.length*6;this.trimmed++;}}
  history(redo){if(this.pending)throw Error('请先结束笔画');const from=redo?this.redoStack:this.undoStack,to=redo?this.undoStack:this.redoStack,a=from.pop();if(!a)return false;const v=redo?a.after:a.before;for(let k=0;k<a.ids.length;k++)this.values[a.ids[k]]=v[k];to.push(a);this.revision++;return true;}
  replace(values){if(this.pending)throw Error('请先结束笔画');const ids=[],before=[],after=[];for(let i=0;i<this.n;i++)if(values[i]!==this.values[i]){if(this.values[i]===255||values[i]===255||this.locks[this.values[i]]||this.locks[values[i]])throw Error('载入会改变锁定层；请先核对并解锁相关类别');ids.push(i);before.push(this.values[i]);after.push(values[i]);}if(ids.length){this.values.set(values);this.undoStack.push({ids:Uint32Array.from(ids),before:Uint8Array.from(before),after:Uint8Array.from(after)});this.redoStack=[];this.revision++;this.limitHistory();}return ids.length;}
 }
 g.TerritoryModel=Model;if(typeof module!=='undefined')module.exports=Model;
})(globalThis);
