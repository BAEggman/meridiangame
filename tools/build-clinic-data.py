from pathlib import Path
import json, shutil
R=Path(__file__).resolve().parents[1]
O=R/'clinic'; (O/'data').mkdir(parents=True,exist_ok=True)
def read(p): return json.loads((R/p).read_text())
def put(n,d): (O/'data'/n).write_text(json.dumps(d,ensure_ascii=False,indent=2))
a=read('reference/clinic-research/approaches-audit.json')
s=read('reference/clinic-research/symptoms-audit.json')
atlas=read('stage1/data/scene.json')
variants=read('reference/location-research/onedrive-location-variants.json')['variants']
borrowed={p['point'] for x in a['approaches'] for p in x['points'] if not p['point'].startswith(('LU','LI'))}
points=[p for p in atlas['points'] if p['meridian'] in ['LU','LI'] or p['id'] in borrowed]
for p in points:
 p['borrowed']=p['id'] in borrowed
 p['variants']+= [x for x in variants if x['pointId']==p['id']]
approaches=a['approaches']
for x in approaches:
 x['parts']=['position.'+p['point'] for p in x['points']]
 # Position recall is what stage 1 measures. Role/derivation claims remain in the book.
 x['assesses']='혈 위치 집합만. 補瀉 역할·도출 원리 회상은 측정하지 않음.'
symptoms=s['candidates']
phys=read('reference/clinic-research/physician-audit.json')['physician']
scene={k:atlas[k] for k in ['outlines','landmarks','nodes']}
scene['edges']=[e for e in atlas['edges'] if e['channel'] in ['LU','LI']]
scene['meridians']=[m for m in atlas['meridians'] if m['id'] in ['LU','LI']]
data={'approaches':approaches,'symptoms':symptoms,'constraints':[], 'physician':phys,'points':points,'scene':scene}
for k in ['approaches','symptoms','constraints','points']:put(k+'.json',data[k])
put('physicians.json',[phys]);put('meridians.json',scene['meridians'])
(O/'data/data.js').write_text('export const DATA = '+json.dumps(data,ensure_ascii=False)+';\n')
shutil.copytree(R/'stage15/assets',O/'assets',dirs_exist_ok=True)
print(f'40혈={len(points)} / 8길={len(approaches)} / 원문 증상={len(symptoms)} / 검증 금기=0')
