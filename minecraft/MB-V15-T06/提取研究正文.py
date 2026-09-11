from pathlib import Path
from html.parser import HTMLParser
import sys
sys.stdout.reconfigure(encoding='utf8')
class 正文(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.parts=[]
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip-=1
 def handle_data(self,d):
  if not self.skip and d.strip():self.parts.append(d.strip())
for f in (Path(__file__).parent/'来源').glob('*.html'):
 p=正文();p.feed(f.read_text(encoding='utf-8-sig'));text='\n'.join(p.parts);f.with_suffix('.txt').write_text(text,encoding='utf8');start=text.find('Breadcrumb');end=text.find('News',start);print(f.stem+'\n'+text[start:end if end>start else start+11000])
