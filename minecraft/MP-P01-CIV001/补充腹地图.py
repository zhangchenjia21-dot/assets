"""在同一真实坐标底图上补充关系型腹地说明；不生成伪精确的服务半径或政治面域。"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent
im=Image.open(R/'maps/territory.png').convert('RGB');d=ImageDraw.Draw(im);f=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',18);t=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',30)
d.rectangle((65,15,1740,62),fill='#f0efe4');d.text((70,22),'节点层级与关系腹地｜同一地点对不同流有不同覆盖',font=t,fill='#223331')
lines=['腹地关系（提案，不是封闭面域）','01 ← 西岛南部生产家庭','02 ← 西岛北弧家庭；与01重叠竞争','03 ← 01/02的周期货流和赴会人流','05 ← 跨水货流 + 山地分段运输','06/07/08 ← 各自地方生活与季节生产','04 ← 三席制度成员，非人口半径圈','09 ← 条件性南端货流，低量则不升级','', '位阶不能互换：','人口与日常：01较强，地方节点分散','经济吞吐：03/05可高于常住位阶','政治与象征：04高，但不垄断商业','主脊、水面、频率改变实际可达腹地','下一层核实后才画精细catchment']
d.rounded_rectangle((1150,275,1710,740),radius=10,fill='#f0efe4',outline='#527276',width=2)
for i,s in enumerate(lines):d.text((1166,291+i*28),s,font=f,fill='#203838')
im.save(R/'maps/catchments.png')
p=R/'index.html';s=p.read_text(encoding='utf8');s=s.replace('<div><img id="map"', '<button onclick="show(\'catchments\')">节点与腹地</button><div><img id="map"');p.write_text(s,encoding='utf8')

import json
p=R/'map-register.json';m=json.loads(p.read_text(encoding='utf8'));m['maps']=list(dict.fromkeys(m['maps']+['catchments']));p.write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf8')
