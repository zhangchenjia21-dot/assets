"""复用 T12 体素审计 renderer，但输入只来自本轮正式提取的 Canonical Blueprint。"""
from pathlib import Path
import json
R=Path(__file__).resolve().parent
source=(R.parent/'MB-V110-T12/审计视图.py').read_text(encoding='utf8')
start=source.index("R=Path(__file__).resolve().parent;s=sys.argv[1]")
end=source.index('\nC=[]',start)
source=source[:start]+'''R=Path(__file__).resolve().parent;s='正式资产'
bp=json.loads((R/'blueprint.json').read_text(encoding='utf8'));pal=bp['palette']
A=np.full((36,96,56),pal.index('minecraft:air'),dtype=np.uint16)
for x,y,z,p in bp['blocks']:A[y+5,z+16,x+11]=p
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',14)
(R/'证据').mkdir(exist_ok=True)
'''+source[end:]
source=source.replace('实存体素渲染，非客户端截图','正式蓝图渲染，非客户端截图')
source=source.replace('for i,v in enumerate(views):',"views += [('完整等轴',(88,78,-38),(25,23,52)),('完整背面',(-48,68,124),(25,23,52)),('侧面',(-58,35,52),(25,24,52)),('正面',(25,24,-22),(25,23,36)),('俯视',(25,140,53),(25,20,52))]\nfor i,v in enumerate(views):")
source=source.replace("if len(sys.argv)==2 or str(i) in sys.argv[2:]:render(*v)","if i>=25:render(*v)")
exec(compile(source,str(R/'正式视图运行.py'),'exec'),{'__file__':str(R/'正式视图运行.py'),'__name__':'__main__'})
