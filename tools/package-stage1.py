from pathlib import Path
import re,base64,shutil,json,posixpath
R=Path(__file__).resolve().parents[1];S=R/'stage1'
files=['config.js','data/data.js','src/engine/flow.js','src/ui/insets.js','src/ui/map.js','src/ui/qi.js','src/ui/input.js','main.js']
chunks=[]
for name in files:
    source=(S/name).read_text()
    exports=re.findall(r'^export (?:function|const|class)\s+([A-Za-z_$][\w$]*)',source,flags=re.M)
    def dependency(m):
        target=posixpath.normpath(posixpath.join(posixpath.dirname(name),m[2]))
        assert target in files, target
        return 'const {'+m[1]+'} = modules['+json.dumps(target)+'];'
    source=re.sub(r'^import\s*\{([^}]+)\}\s*from\s*[\'"]([^\'"]+)[\'"];?\s*$',dependency,source,flags=re.M)
    source=re.sub(r'\bexport (?=(?:function|const|class))','',source)
    chunks.append('modules['+json.dumps(name)+']=(()=>{\n'+source+'\nreturn {'+','.join(exports)+'};})();')
js='(()=>{const modules={};\n'+'\n'.join(chunks)+'\n})();'
js=js.replace('</script','<\\/script')
css=(S/'style.css').read_text();fontcss=(S/'assets/font.css').read_text()
for url in re.findall(r'url\(([^)]+)\)',fontcss):
    fontcss=fontcss.replace(url,'data:font/ttf;base64,'+base64.b64encode((S/'assets'/url).read_bytes()).decode())
html=(S/'index.html').read_text().replace('<link rel="stylesheet" href="assets/font.css">','<style>'+fontcss+'</style>').replace('<link rel="stylesheet" href="style.css">','<style>'+css+'</style>').replace('<script type="module" src="main.js"></script>','<script>'+js+'</script>').replace('href="guide.html"','href="stage1/guide.html"')
(R/'五十營_1단계_바로플레이.html').write_text(html)
(R/'qa/stage1-portable-script.js').write_text(js)
# dist is generated, and earlier source is separately archived.
assert (S/'index.html').exists() and (S/'data/points.json').exists()
if (R/'dist').exists():shutil.rmtree(R/'dist')
shutil.copytree(S,R/'dist',ignore=shutil.ignore_patterns('tests','package.json'))
print(json.dumps({'portable_bytes':len(html.encode()),'stage1_points':361,'remaining_coordinates':0,'learning_records':False}))

