"""Bundle the static ES modules, reference text, and audio into a local-file playable HTML."""
from pathlib import Path
import re,json,base64
root=Path(__file__).resolve().parents[1];dist=root/'dist'
content=json.loads((dist/'content.mjs').read_text().removeprefix('export const CONTENT = ').rstrip(';\n'))
for f in content['facts']:
 if f.get('audio'):
  data=base64.b64encode((dist/f['audio']).read_bytes()).decode()
  f['audio']='data:audio/mpeg;base64,'+data
reference=(dist/'reference.json').read_text()
config=(dist/'config.json').read_text()
def plain(name):
 text=(dist/name).read_text()
 text=re.sub(r'^import .*?;\n','',text,flags=re.M)
 return re.sub(r'\bexport (?=(?:const|function|class))','',text)
engine=plain('engine.mjs');names=re.findall(r'export function (\w+)',(dist/'engine.mjs').read_text())
e='const E={'+','.join(['DAY','MINUTE','SAVE_VERSION','FACTS','MISSIONS']+names)+'};\n'
app=plain('app.mjs').replace('reference=null','reference=INLINE_REFERENCE')
js='(()=>{\nconst CONFIG='+config+';\nconst CONTENT='+json.dumps(content,ensure_ascii=False)+';\nconst INLINE_REFERENCE='+reference+';\n'+engine+'\n'+plain('art.mjs')+'\n'+e+app+'\n})();'
# Literal closing script tags in source records must never terminate the inline script.
js=js.replace('</script','<\\/script')
html=(dist/'index.html').read_text().replace('<link rel="stylesheet" href="style.css">','<style>'+(dist/'style.css').read_text()+'</style>').replace('<script type="module" src="app.mjs"></script>','<script>'+js+'</script>')
html=html.replace('href="guide.html"','href="dist/guide.html"')
path=root/'五十營_바로플레이.html';path.write_text(html)
(root/'qa/portable-script.js').write_text(js)
print(path.name, path.stat().st_size)
