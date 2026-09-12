"""保存公开研究资料和提取正文，保留来源 URL；不读取其它测试。"""
from pathlib import Path
from urllib.request import Request,urlopen
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor
import json,sys
sys.stdout.reconfigure(encoding='utf8')
R=Path(__file__).resolve().parent/'研究'
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.text=[];self.links=[]
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
  if t in ['a','img']:self.links.append(dict(a))
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip and d.strip():self.text.append(d.strip())
def fetch(pair):
 name,url=pair
 try:
  b=urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=25).read();(R/(name+'.html')).write_bytes(b);p=Parser();p.feed(b.decode('utf8'));t=' '.join(p.text);(R/(name+'.txt')).write_text(t,encoding='utf8');(R/(name+'-links.json')).write_text(json.dumps(p.links,ensure_ascii=False,indent=2),encoding='utf8');return {'name':name,'url':url,'text':t[:10500]}
 except Exception as e:return {'name':name,'url':url,'error':str(e)}
if __name__=='__main__':
 urls=json.loads(sys.argv[1]);print(json.dumps(list(ThreadPoolExecutor(4).map(fetch,urls)),ensure_ascii=False,indent=2))
