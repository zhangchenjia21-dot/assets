"""向既有 REF 目录增量注册一个 Owner 获批条目；不运行固定 122 项历史批次，不改旧条目或词表。"""
from pathlib import Path
import json,hashlib,shutil,csv,collections
R=Path(__file__).resolve().parent;B=R.parent;L=B/'AI-Blueprints/references'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,v):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
catalog=read(L/'catalog/catalog.json');mapping=read(L/'catalog/reference-id-map.json')
assert len({r['id'] for r in catalog})==len(catalog)
rid=f"REF-{max(int(r['reference_id'].split('-')[1]) for r in mapping)+1:04d}"
assert rid=='REF-0123','REF allocation changed; re-evaluate before registering'
assert not (L/'derived'/rid).exists()
bp=read(R/'blueprint.json');validation=read(R/'提取验证.json');native=read(R/'原生回读验证.json')
assert all(r['full_state_differences']==0 for r in native)
assert sha(R/'blueprint.json')==validation['blueprint_sha256']
approval=B/'发布/assets/minecraft/MB-V110-T12/Asset Approval.md'
assert 'APPROVED FOR INGEST' in approval.read_text(encoding='utf8')
# 先保存既有 registry 字节以便审计；新条目只追加，ID 不重排，现有字段不回写。
registry=['catalog/catalog.json','catalog/catalog.csv','catalog/reference-id-map.json','indexes/inverted-index.json','classification-v2/catalog-v2.json','classification-v2/catalog-v2.csv','classification-v2/catalog-final.json','classification-v2/catalog-final.csv']
for rel in registry:
 p=R/'注册前-本地限定'/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(L/rel,p)
D=L/'derived'/rid;N=D/'normalized';N.mkdir(parents=True)
O=L/'originals'/rid;O.mkdir(parents=True)
for dst in [D/'blueprint.json',N/'original-blueprint.json',N/'normalized-blueprint.json']:shutil.copy2(R/'blueprint.json',dst)
shutil.copy2(R/'京町家修复.litematic',O/'京町家修复.litematic');shutil.copy2(approval,D/'Asset Approval.md')
P=D/'proxy';P.mkdir();views={}
for key,name in [('isometric','完整等轴'),('front','正面'),('side','侧面'),('top','俯视'),('rear','完整背面')]:
 shutil.copy2(R/f'证据/正式资产-{name}.png',P/f'{key}.png');views[key]=str(P/f'{key}.png')
for file in (R/'证据').glob('*.png'):shutil.copy2(file,P/file.name)
counts=collections.Counter(bp['palette'][r[3]] for r in bp['blocks']);occupied=sum(v for k,v in counts.items() if k!='minecraft:air')
requirements=[{'state':k,'count':v} for k,v in sorted(counts.items()) if k!='minecraft:air']
save(D/'block-requirements.json',requirements)
warnings=[{'code':'BLOCK_ENTITY_NBT_NOT_EXPORTED','count':10,'message':'10 个空容器/炉的方块状态保留；NBT 未导出。无库存物品。实装需遵守当前基础实体策略。'}]
norm={'reference_id':rid,'compatibility':'CURRENT_NATIVE','original_data_version':4903,'normalized_target_version':'26.2','normalized_target_data_version':4903,'changed':0,'unresolved':[],'warnings':warnings,'verification':{'canonical_explicit_cell_differences':0,'native_litematica_full_state_differences':0,'dimensions_equal':True,'origin_equal':True},'source_sha256':sha(O/'京町家修复.litematic'),'method':'Already 26.2 native; identity normalization, no legacy replacement or DataFixer migration needed.'}
save(N/'normalization-report.json',norm)
binding={'source_sha256':sha(N/'normalized-blueprint.json'),'view_sha256':{k:sha(v) for k,v in views.items()},'review_views':list(views),'reviewer':'Codex asset extraction review','owner_review':False}
styles=[{'tag':'japanese','confidence':1.0,'evidence':['Owner approved Kyoto machiya; timber shopfront, earthen walls, tiled roofs, courtyard compound']},{'tag':'east_asian','confidence':1.0,'evidence':['Japanese machiya typology']}]
features=['courtyard','timber_frame','stone_base','multi_story','asymmetrical'];evidence='从 T12 最终实存提取；前店、侧土间、住宅、两庭与后仓库保持同一院落序列。'
values={k:{'rating':'useful','note':evidence} for k in read(L/'catalog/controlled-vocabulary.json')['reference_value_dimensions']}
placement={'anchor':{'x':13,'y':2,'z':1},'origin':bp['origin'],'ground_level':2,'ground_level_definition':'主土间/院地行走面 local Y2；地表方块 local Y1；抬高木地板行走面 local Y3','primary_entrance':{'local':{'x':13,'y':3,'z':2},'source_world':{'x':24,'y':18,'z':18},'facing':'north'},'front_direction':'north','ground_interface_regions':['GroundInterface'],'recommended_placement':'狭长城市平地，北侧接街。先整备地基和净空，按完整二 Region 放置；不要仅粘贴上部或过滤显式空气。目标行走面标高减 2 为 Blueprint 最小 Y。','ground_interface_notes':'保留 X12..39/Y15..16/Z17..88 的院地与基础薄层；出檐可超出地界一格。北面街路不在资产内，需在新 SITE 单独接续；本资产不含世界施工授权。','rotation':'仅用现有原生 block-state 变换流程；本轮原生加载验证为原始 north 朝向。'}
source={'source_kind':'AI_ORIGINAL','world':validation['world'],'source_url':'https://github.com/zhangchenjia21-dot/assets/tree/c3c246a/minecraft/MB-V110-T12','lineage':'MB-V19-T11-京町家 → T12 47-cell bounded repair → final client copy','author':'Codex original design for Owner','license':'Owner authorized asset reuse; no separate public license declared','approved_source':'T12 final repaired actual world only','source_bounds':validation['bounds'],'source_files_unchanged':True,'source_manifest_sha256':validation['source_manifest_sha256'],'archived_reload_comparison':{'differing_cells':6,'all_at_y':15,'change':'grass_block to dirt below supported steps','interpretation':'客户端副本地表状态差异；正式资产保留当前实际泥土，不从旧版补回。'},'skill_version':'minecraft-builder v1.10'}
owner={'status':'APPROVED_FOR_INGEST','file':str(D/'Asset Approval.md'),'sha256':sha(approval),'git_commit':'c3c246a','url':'https://github.com/zhangchenjia21-dot/assets/blob/c3c246a/minecraft/MB-V110-T12/Asset%20Approval.md','current_instruction':'执行 T12 町家正式资产入库。Owner 已明确批准入库。','canon_world_write':False}
meta={'id':rid,'reference_id':rid,'name':bp['metadata']['name'],'schematic_name':bp['metadata']['name'],'original_filename':'京町家修复.litematic','original_absolute_path':str(O/'京町家修复.litematic'),'file_hash':sha(O/'京町家修复.litematic'),'asset_status':'REFERENCE_ONLY','ingest_status':'REGISTERED_OWNER_APPROVED','source':source,'owner_approval':owner,'primary_use':'mixed_use','primary_use_confidence':1.0,'primary_use_evidence':[evidence],'secondary_use':['shop','house','townhouse','warehouse','garden'],'styles':styles,'scale':'large','settlement_roles':['commerce','residential','storage'],'terrain_fit':[{'tag':v,'confidence':1.0,'evidence':[evidence]} for v in ['flat','urban_infill','courtyard']],'features':features,'feature_evidence':{k:evidence for k in features},'reference_value':values,'reference_strengths':list(values),'classification_conflicts':[],'classification_method':'Owner approved identity + actual source / preview inspection','minecraft_data_version':4903,'regions':validation['inspection']['regions'],'region_count':2,'dimensions':bp['dimensions'],'block_count':occupied,'occupied_block_count':occupied,'total_volume':42660,'enclosing_volume':42920,'specified_volume':42660,'palette_size':len(bp['palette']),'block_palette':bp['palette'],'block_requirements_path':str(D/'block-requirements.json'),'modded_block_count':0,'block_entity_count':10,'exported_block_entity_nbt_count':0,'entity_count':0,'entity_count_basis':'No free entities included; reference is block compound only','technical_status':'READY_WITH_WARNINGS','technical_flags':['BLOCK_ENTITY_NBT_NOT_EXPORTED'],'unsupported_features':warnings,'unresolved_blocks':[],'functional_validation':'OWNER_ACCEPTED_T12_SOURCE; NEW_SITE_NOT_VALIDATED','preview_compatible':True,'ingestion_complete':True,'ingestion_version':5,'compatibility':'CURRENT_NATIVE','original_data_version':4903,'normalized_target_version':'26.2','normalized_target_data_version':4903,'default_representation':'normalized','blueprint_path':str(N/'normalized-blueprint.json'),'normalized_blueprint_path':str(N/'normalized-blueprint.json'),'original_blueprint_path':str(N/'original-blueprint.json'),'normalization_report_path':str(N/'normalization-report.json'),'normalization_warnings':warnings,'block_state_registry_validation':'VALID_CURRENT_STATE_NATIVE_LITEMATICA_READBACK','placement':placement,'architecture':{'tradition':'Japanese','era':'late Edo, circa 1840','type':'Kyoto machiya','use':'Gofuku textile retail / wholesale and household','compound':'commercial-residential courtyard compound'},'architecture_proxy':{'views':views,'front_confidence':1.0},'preview_binding':binding}
# 分类字段沿用正式词表；时代与具体类型作为描述，不扩充 taxonomy。
v2={'structure_type':'building','primary_use':'mixed_use','secondary_use':meta['secondary_use'],'styles':styles,'architectural_features':features,'terrain_fit':meta['terrain_fit'],'scale':'large','settlement_roles':meta['settlement_roles'],'material_profile':[],'reference_value':{k:{'rating':'useful','evidence':evidence} for k in values},'massing_signature':{'type':'compound','estimated_floors':2,'floors_basis':'前屋二层；后主屋及仓库独立屋面'},'confidence':{'primary_use':1.0,'style_max':1.0,'structure_type':1.0,'overall':1.0,'interpretation':'known original identity, not calibrated score'},'evidence':{'visual_observation':evidence,'standard_views':views,'review_binding':binding},'source':'codex_final_asset_review','owner_approved':True,'conflicts':[]}
vocab=read(L/'classification-v2/vocabulary-v2.json');assert v2['primary_use'] in vocab['primary_use'];assert all(s['tag'] in vocab['style'] for s in styles)
assert v2['massing_signature']['type'] in vocab['massing']
meta.update(classification_v1={k:meta[k] for k in ['primary_use','secondary_use','styles','scale']},classification_v2=v2,classification_v2_automatic=v2,default_classification='classification_v2')
save(D/'metadata.json',meta);save(D/'placement.json',placement);save(D/'preview-metadata.json',{'reference_id':rid,'blueprint_path':meta['blueprint_path'],'blueprint_sha256':binding['source_sha256'],'default_representation':'normalized','compatibility':'CURRENT_NATIVE','asset_status':'REFERENCE_ONLY','approval':None,'owner_ingest_approval':owner,'v5_size_compatible':True,'warnings':warnings,'views':views})
shutil.copy2(R/'提取验证.json',D/'extraction-validation.json');shutil.copy2(R/'原生回读验证.json',D/'native-validation.json')
catalog.append(meta);mapping.append({'reference_id':rid,'original_filename':meta['original_filename'],'original_absolute_path':meta['original_absolute_path'],'file_hash':meta['file_hash']})
save(L/'catalog/catalog.json',catalog);save(L/'catalog/reference-id-map.json',mapping)
index=read(L/'indexes/inverted-index.json')
tokens=[rid,meta['primary_use'],meta['scale'],*meta['secondary_use'],*meta['settlement_roles'],*features,*[s['tag'] for s in styles],*[s['tag'] for s in meta['terrain_fit']],'primary_use=mixed_use','scale=large',*['style='+s['tag'] for s in styles]]
for token in tokens:index.setdefault(token,[]).append(rid)
save(L/'indexes/inverted-index.json',index)
for rel in ['classification-v2/catalog-v2.json','classification-v2/catalog-final.json']:
 rows=read(L/rel);rows.append(meta);save(L/rel,rows)
# CSV 是既有 catalog 的并行导出，只增一行且保留原列。
for rel in ['catalog/catalog.csv','classification-v2/catalog-v2.csv','classification-v2/catalog-final.csv']:
 with (L/rel).open(encoding='utf-8-sig',newline='') as f:headers=next(csv.reader(f))
 with (L/rel).open('a',encoding='utf8',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=headers);row={**meta,**v2} if 'classification-v2' in rel else meta
  writer.writerow({k:json.dumps(row.get(k,''),ensure_ascii=False) if isinstance(row.get(k,''),(dict,list)) else row.get(k,'') for k in headers})
for rel in ['catalog/catalog.json','classification-v2/catalog-v2.json','classification-v2/catalog-final.json']:
 assert read(L/rel)[:-1]==read(R/'注册前-本地限定'/rel)
save(R/'注册结果.json',{'reference_id':rid,'name':meta['name'],'library':str(D),'litematic':meta['original_absolute_path'],'blueprint':meta['blueprint_path'],'previous_records_unchanged':122,'registry_files':registry,'world_writes':0})
print(json.dumps({'reference_id':rid,'dimensions':meta['dimensions'],'occupied':occupied},ensure_ascii=False))
