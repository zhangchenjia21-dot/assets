"""交付前只读检查代码、数据库、导出引用及归档；结果写入NG-2 validation。"""
import ast,hashlib,json,platform,sqlite3,subprocess,sys
from pathlib import Path
import numpy,PIL
from PIL import Image
sys.path.append('D:/Games/Minecraft/AI工程/AI-Blueprints/参考入库/第三方')
import nbtlib
ROOT=Path(__file__).resolve().parents[2]
repo=ROOT.parents[4]
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def digest(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
errors=[];imports=[]
for path in (ROOT/'tooling').rglob('*.py'):
    source=path.read_text(encoding='utf-8');tree=ast.parse(source);compile(tree,str(path),'exec')
    layer=next((int(s[1]) for s in path.parts if s.startswith(('L0_','L1_','L2_','L3_'))),None)
    if layer is not None:
        for node in ast.walk(tree):
            if isinstance(node,ast.ImportFrom) and node.module and node.module.startswith(('L0_','L1_','L2_','L3_')):
                target=int(node.module[1]);imports.append({'file':path.relative_to(ROOT).as_posix(),'dependency':node.module})
                if target>layer:errors.append('upward dependency '+str(path))
tests=subprocess.run([sys.executable,'-B',str(ROOT/'tooling/测试/精查解码拓扑测试.py')],capture_output=True,text=True)
if tests.returncode:errors.append(tests.stderr)
db=sqlite3.connect('file:'+str(ROOT/'raw-or-queryable/refinement.sqlite')+'?mode=ro',uri=True)
for id,raw in db.execute('SELECT target,json FROM assessments'):
    a=load('assessments/'+id+'.json')
    if a!=json.loads(raw):errors.append(id+' DB/JSON mismatch')
    if digest(ROOT/a['refined_metrics']['source'])!=a['refined_metrics']['sha256']:errors.append(id+' metric digest mismatch')
db.close()
archive=load('manifest/archive.json')
if digest(ROOT/'raw-or-queryable/refinement.sqlite')!=archive['sqlite_sha256']:errors.append('archive no longer matches current DB')
for p in archive['parts']:
    if digest(ROOT/'raw-or-queryable'/p['name'])!=p['sha256']:errors.append('part digest mismatch')
if load('manifest/world-before.json')!=load('manifest/world-after.json'):errors.append('world inventory mismatch')
if load('manifest/v1-before.json')!=load('manifest/v1-after.json'):errors.append('V1 inventory mismatch')
delta=subprocess.run(['git','diff','--exit-code','4b9b1f7e600708ff67e1ef2f844a9d3de0ba2242','--','minecraft/建筑师/research/natural-geography/V1'],cwd=repo,capture_output=True,text=True)
if delta.returncode:errors.append('V1 Git baseline changed or git failed: '+delta.stderr)
images=[]
for p in sorted((ROOT/'visual').glob('*.png')):
    with Image.open(p) as im:im.load();images.append({'file':p.relative_to(ROOT).as_posix(),'size':list(im.size),'sha256':digest(p)})
if len(images)!=21:errors.append('expected 21 PNG views')
result={'python':platform.python_version(),'numpy':numpy.__version__,'Pillow':PIL.__version__,'nbtlib':nbtlib.__version__,'syntax_compile':'ok','layer_imports':imports,'upward_dependencies':0 if not any('upward' in e for e in errors) else 'error','architecture_scope':'single tooling module; cross-layer imports descend; Bootstrap and tests are engineering periphery','unit_test_exit_code':tests.returncode,'unit_test_output':tests.stderr,'db_json_metric_archive_consistency':not errors,'v1_git_baseline_unchanged':delta.returncode==0,'image_inventory':images,'in_game_visual_review':'BLOCKED_BY_SAFE_ENVIRONMENT','world_writes':0,'errors':errors}
(ROOT/'validation/runtime-and-scope.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'errors':errors,'tests':tests.returncode,'images':len(images),'python':platform.python_version()}))
if errors:sys.exit(1)
