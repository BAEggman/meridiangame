from pathlib import Path
import json,re,posixpath,base64,shutil,zipfile
R=Path(__file__).resolve().parents[1]; S=R/'clinic'; O=R.parent/'output'; O.mkdir(exist_ok=True)
(S/'config.js').write_text('export const CONFIG = '+(S/'config.json').read_text()+';\n')
files=['data/data.js','config.js','src/engine/log.js','src/engine/clock.js','src/engine/score.js','src/engine/patients.js','src/engine/blueprints.js','src/engine/judge.js','src/engine/transfer.js','src/engine/storyteller.js','src/ui/body.js','src/ui/pad.js','src/app.js']
chunks=[]
for name in files:
 source=(S/name).read_text(); exports=re.findall(r'^export (?:function|const|class)\s+([A-Za-z_$][\w$]*)',source,re.M)
 def dep(m):return 'const {'+m[1]+'} = modules['+json.dumps(posixpath.normpath(posixpath.join(posixpath.dirname(name),m[2].split('?')[0])))+'];'
 source=re.sub(r'import\s*\{([^}]+)\}\s*from\s*[\'"]([^\'"]+)[\'"];?',dep,source)
 source=re.sub(r'\bexport (?=(?:function|const|class))','',source)
 chunks.append('modules['+json.dumps(name)+']=(()=>{\n'+source+'\nreturn {'+','.join(exports)+'};})();')
js='(()=>{const modules={};\n'+'\n'.join(chunks)+'\n})();';js=js.replace('</script','<\\/script')
fontcss=(S/'assets/font.css').read_text()
for url in re.findall(r'url\(([^)]+)\)',fontcss):fontcss=fontcss.replace(url,'data:font/ttf;base64,'+base64.b64encode((S/'assets'/url).read_bytes()).decode())
html=(S/'index.html').read_text().replace('<link rel="stylesheet" href="assets/font.css">','<style>'+fontcss+'</style>').replace('<link rel="stylesheet" href="style.css">','<style>'+(S/'style.css').read_text()+'</style>').replace('<script type="module" src="src/app.js"></script>','<script>'+js+'</script>').replace('href="guide/"','href="醫館_v2_검수장부.html"')
(O/'醫館_v2_실행.html').write_text(html);(R/'qa/clinic-portable-script.js').write_text(js)
shutil.copy2(S/'guide/index.html',O/'醫館_v2_검수장부.html')
if(R/'dist').exists():shutil.rmtree(R/'dist')
shutil.copytree(S,R/'dist',ignore=shutil.ignore_patterns('tests','qa'))
with zipfile.ZipFile(O/'醫館_v2_Claude_공동개발.zip','w',zipfile.ZIP_DEFLATED)as z:
 for dirname in ['clinic','stage1','stage15','reference','docs','tools','qa']:
  for p in (R/dirname).rglob('*'):
   if not p.is_file()or any(x in p.parts for x in ['__pycache__','node_modules','.git','kmcric-pages','originals','visual']):continue
   if p.suffix in ['.pdf','.png','.webm'] and dirname not in ['clinic']:continue
   if p.name.endswith('portable-script.js'):continue
   z.write(p,'meridian-flow/'+str(p.relative_to(R)))
 for name in ['serve.py','package.json','CHANGES.md','질문.md','START_HERE_CLAUDE.txt','먼저읽기.txt']:z.write(R/name,'meridian-flow/'+name)
 z.write(O/'醫館_v2_실행.html','醫館_v2_실행.html');z.write(O/'醫館_v2_검수장부.html','醫館_v2_검수장부.html')
print(json.dumps({'active':'clinic','portable_bytes':len(html.encode()),'zip':str(O/'醫館_v2_Claude_공동개발.zip')},ensure_ascii=False))
