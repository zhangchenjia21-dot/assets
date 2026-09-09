"""读取已安装世界生成包的少量声明作为材料来源背景；不认定单块来源，不修改环境。"""
import json,zipfile,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
p=Path('D:/Games/Minecraft/.minecraft/versions/26.2-Fabric 0.19.5/mods/Terralith_26.2_v2.6.4.jar')
entries=[]
with zipfile.ZipFile(p) as z:
    for name in ['data/terralith/worldgen/configured_feature/canyon/generic/slab_stone.json','data/terralith/worldgen/placed_feature/erosion/slabs.json','data/minecraft/worldgen/biome/stony_peaks.json','data/minecraft/worldgen/noise_settings/overworld.json']:
        raw=z.read(name);obj=json.loads(raw);e={'entry':name,'sha256':hashlib.sha256(raw).hexdigest()}
        if 'noise_settings' not in name:e['json']=obj
        else:
            hits=[]
            def walk(node,path='',ancestors=()):
                if isinstance(node,dict):
                    if node.get('Name')=='minecraft:dirt_path':hits.append({'json_pointer':path,'enclosing_rule':ancestors[-3] if len(ancestors)>=3 else node})
                    for k,v in node.items():walk(v,path+'/'+str(k),ancestors+(node,))
                elif isinstance(node,list):
                    for k,v in enumerate(node):walk(v,path+'/'+str(k),ancestors+(node,))
            walk(obj);e['dirt_path_rules']=hits
        entries.append(e)
result={'kind':'installed worldgen material context, not individual block origin proof','jar_name':p.name,'jar_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'entries':entries,'conclusion':'Terralith declares natural stone_slab features and dirt_path surface rules. Candidate material flags alone do not prove human edits. Current installed jar is supporting context, not historical generation provenance.'}
(ROOT/'validation/worldgen-material-context.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('worldgen context written; entries',len(entries),'dirt_path rules',len(entries[-1]['dirt_path_rules']))
