import path from 'node:path';import {fileURLToPath} from 'node:url';
import {AssetStore} from '../L1_器件层/资产记录器.mjs';import {NativeStates} from '../L1_器件层/原生变换客户端.mjs';
import {promote,publishSource} from '../L2_流程层/资产晋升流程.mjs';import {instantiate,analyzeTerrain} from '../L2_流程层/资产实例化流程.mjs';
import {checkBlueprint,ProjectStore,digest,functionalValidation} from '../../../AI-Preview/L3_外交层/预览公开接口.mjs';
import {readBaseEntityCapability} from '../../../AI-Offline/L3_外交层/基础实体策略接口.mjs';
import {fitVariants} from '../L1_器件层/放置元数据计算器.mjs';
import {validateNonBuilding} from '../L1_器件层/非房屋资产校验器.mjs';
export const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const REFS=path.resolve(ROOT,'../references');
/** 晋升只复制 authoritative normalized 数据；同 REF 重复调用返回原 AST，不重分配。 */
export function promoteReference(id,{root=ROOT,references=REFS,native=new NativeStates(ROOT)}={}){return promote(root,references,id,native,bp=>checkBlueprint(bp,{previewOnly:true}),readBaseEntityCapability());}
/** 原创来源必须有显式用途、授权和稳定身份；房屋保留原功能验证，TREE/OPEN_SHELTER 显式契约验证根接、锚点及通道。只写资产库，不批准世界施工。 */
export function promoteOriginalAsset(source,{root=ROOT,native=new NativeStates(ROOT)}={}){
 if(source.source_kind!=='AI_ORIGINAL'||!/^AI-[A-Z0-9-]+$/.test(source.id)||!source.owner_authorization||!source.classification_v2||!Number.isInteger(source.max_repetitions)||source.max_repetitions<1)throw Error('INVALID_ORIGINAL_SOURCE');
 return publishSource(root,source,source.normalized_blueprint_path,native,bp=>{checkBlueprint(bp);if(bp.metadata?.asset_contract){validateNonBuilding(bp);}else{const f=functionalValidation(bp);if(f.status==='FAIL')throw Error('ORIGINAL_FUNCTIONAL_FAIL');}},readBaseEntityCapability());
}
/** 在同一 AST ID 上复审已验证能力；不会修改源 Blueprint，也不代表场地批准。 */
export function reevaluateAsset(id,{root=ROOT,references=REFS,native=new NativeStates(ROOT)}={}){const a=inspectAsset(id,{root}).asset;return promote(root,references,a.source_ref_id,native,bp=>checkBlueprint(bp,{previewOnly:true}),readBaseEntityCapability(),{refresh:true});}
/** 批量读取本机 26.2 原生状态及变换，不构造或访问世界。 */
export function inspectBlockStates(states){return new NativeStates(ROOT).ensure(states);}
/** 返回经过 hash 核对的资产与放置契约；未知 ID / 内容被修改时明确失败。 */
export function inspectAsset(id,{root=ROOT}={}){return new AssetStore(root).inspect(id);}
/** 读取原资产全部允许变换后的 footprint/contact/clearance/front/anchor。仅 fit 模拟；无实例化、无 geometry-only 开关、无世界调用。状态准入由协调器另行强制检查。 */
export function inspectAssetFitVariants(id,options={}){return fitVariants(inspectAsset(id,options).placement);}
/** 精确字段过滤；仅搜索 Asset 快照，绝不回退 Reference 或重分类。 */
export function searchAssets(filters={}, {root=ROOT}={}){for(const key of Object.keys(filters))if(!['use','style','scale','terrain_mode','status'].includes(key))throw Error('UNKNOWN_FILTER:'+key);return new AssetStore(root).list().filter(a=>Object.entries(filters).every(([key,value])=>{const wanted=Array.isArray(value)?value:[value],actual=key==='style'?a.styles:[a[key]];return wanted.some(v=>actual.includes(v));}));}
/** 输出旋转/镜像烘焙后的 Canonical Blueprint；geometry_only 不会被默认开启。无世界调用。 */
export function instantiateAsset(id,options={}, {root=ROOT,native=new NativeStates(ROOT)}={}){const result=instantiate(inspectAsset(id,{root}),native,options,readBaseEntityCapability());checkBlueprint(result.blueprint,{previewOnly:options.preview_only===true});return result;}
/** 给未来 Planner 的完整放置契约，无需再次解析 litematic。 */
export function plannerAsset(id,options={}){const{asset:a,placement:p}=inspectAsset(id,options);return{asset_id:a.asset_id,status:a.status,use:a.use,style:a.styles,scale:a.scale,footprint:p.footprint,anchor:p.anchor,front:{direction:p.front_direction,confidence:p.front_confidence},clearance:p.clearance_bounds,rotation:a.rotation_allowed,mirror:a.mirror_allowed,terrain_mode:a.terrain_mode,dimensions:a.dimensions,ground_contact_mask:p.ground_contact_mask,geometry_only_required:a.geometry_only_required};}
/** 只分析调用方提供的高度图；不采集或修改世界，覆盖缺失明确拒绝。 */
export function analyzeAssetTerrain(instance,heightmap){return analyzeTerrain(instance,heightmap);}
/** 直接复用 V5 存储和渲染契约；预览无世界场地与功能验收，固定禁用批准。 */
export function previewAsset(id,options={}){
 const result=instantiateAsset(id,{...options,preview_only:true}),bp=result.blueprint,store=new ProjectStore(path.join(ROOT,'state/previews')),project=`v6e_${id.toLowerCase()}_${options.rotation||0}_${options.mirror||'none'}`;
 const existing=store.list().find(m=>m.blueprint_id===project);if(existing&&digest(store.blueprint(project))===digest(bp))return{project,url:`http://127.0.0.1:43825/?id=${project}`,revision:existing.revision};
 const meta=store.saveRevision(project,bp,{name:`${bp.metadata.name} · ${id} · ${options.rotation||0}° · mirror ${options.mirror||'none'}`,mode:'ASSET PREVIEW',group:id,description:'V6E 资产实例预览；原 normalized 结构直接变换。未选定场地，禁止施工。',dimensions:bp.dimensions,estimated_blocks:bp.blocks.filter(v=>!['minecraft:air','minecraft:cave_air','minecraft:void_air'].includes(bp.palette[v[3]])).length,estimated_changed_blocks:'未指定场地',palette:[...new Set(bp.palette.map(v=>v.split('[')[0]))],validation:{functional:{status:'FAIL',checks:[],issues:[{severity:'FAIL',message:'资产技术可复用；本预览未审核场地及完整功能动线，禁止批准施工'}]},blueprint:{valid:false,status:'NOT_RUN'}},workflow:'V6E_ASSET_PREVIEW_ONLY',include_terrain:false,target_world:null},'V6E: only preview; world writes forbidden');
 return{project,url:`http://127.0.0.1:43825/?id=${project}`,revision:meta.revision};
}
