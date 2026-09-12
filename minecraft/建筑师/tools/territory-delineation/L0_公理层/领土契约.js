/* 稳定格网契约：水域255不可赋领土；6类归属互斥，逐柱RLE首尾均包含。 */
(function(g){'use strict';
 const categories=Object.freeze([
  {id:'ALLIANCE_COMMONS',name:'联盟公地',color:'#e2bd66'},
  {id:'WEST_DOMAIN',name:'西域',color:'#5cbd98'},
  {id:'MIDDLE_DOMAIN',name:'中域',color:'#ae93dc'},
  {id:'EAST_DOMAIN',name:'东域',color:'#e88e69'},
  {id:'UNASSIGNED',name:'未分配',color:'#9ba9b8'},
  {id:'DISPUTED',name:'争议区',color:'#ef6e98'}]);
 const api=Object.freeze({categories,WATER:255,SCHEMA:'civ-territories/1',INITIAL:4,validCode:v=>Number.isInteger(v)&&v>=0&&v<6});
 g.TerritoryContract=api;if(typeof module!=='undefined')module.exports=api;
})(globalThis);
