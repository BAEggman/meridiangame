from pathlib import Path
import re,urllib.request,concurrent.futures
R=Path(__file__).resolve().parents[1];S=R/'stage1';css=(R/'reference/visual/noto-serif-kr.css').read_text();urls=list(dict.fromkeys(re.findall(r'url\((https://[^)]+)\)',css)));(S/'assets/fonts').mkdir(parents=True,exist_ok=True)
def get(pair):
 i,url=pair;p=S/'assets/fonts'/f'noto-serif-kr-{i}.woff2'
 if not p.exists():
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=20) as r:p.write_bytes(r.read())
 return url,'fonts/'+p.name
for url,local in concurrent.futures.ThreadPoolExecutor(max_workers=8).map(get,enumerate(urls)):css=css.replace(url,local)
(S/'assets/font.css').write_text(css)
print(len(urls),'font files',sum(p.stat().st_size for p in (S/'assets/fonts').glob('*')),'bytes')
