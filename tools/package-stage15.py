from pathlib import Path
import re,base64,shutil,json,posixpath
R=Path(__file__).resolve().parents[1];S=R/'stage15'
files=['data/lung.js','src/loop.js','src/hangul.js','src/audio.js','main.js'];chunks=[]
for name in files:
 source=(S/name).read_text();exports=re.findall(r'^export (?:function|const|class)\s+([A-Za-z_$][\w$]*)',source,re.M)
 def dep(m):return 'const {'+m[1]+'} = modules['+json.dumps(posixpath.normpath(posixpath.join(posixpath.dirname(name),m[2])))+'];'
 source=re.sub(r'^import\s*\{([^}]+)\}\s*from\s*[\'"]([^\'"]+)[\'"];?\s*$',dep,source,flags=re.M)
 source=re.sub(r'\bexport (?=(?:function|const|class))','',source)
 chunks.append('modules['+json.dumps(name)+']=(()=>{\n'+source+'\nreturn {'+','.join(exports)+'};})();')
js='(()=>{const modules={};\n'+'\n'.join(chunks)+'\n})();';js=js.replace('</script','<\\/script')
fontcss=(S/'assets/font.css').read_text()
for url in re.findall(r'url\(([^)]+)\)',fontcss):fontcss=fontcss.replace(url,'data:font/ttf;base64,'+base64.b64encode((S/'assets'/url).read_bytes()).decode())
html=(S/'index.html').read_text().replace('<link rel="stylesheet" href="assets/font.css">','<style>'+fontcss+'</style>').replace('<link rel="stylesheet" href="style.css">','<style>'+(S/'style.css').read_text()+'</style>').replace('<script type="module" src="main.js"></script>','<script>'+js+'</script>')
(R/'五十營_1.5단계_肺의첫소절.html').write_text(html)
(R/'qa/stage15-portable-script.js').write_text(js)
if (R/'dist').exists():shutil.rmtree(R/'dist')
shutil.copytree(S,R/'dist',ignore=shutil.ignore_patterns('tests'))
print(json.dumps({'portable_bytes':len(html.encode()),'active':'stage15','points':11}))
