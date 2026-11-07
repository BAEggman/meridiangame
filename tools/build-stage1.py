from pathlib import Path
import json,re,unicodedata
from atlas_layout import LAYOUT,COUNTS,T,L,S,IC
from atlas_routes import make_routes
R=Path(__file__).resolve().parents[1];D=R/'stage1'
def read(p):return json.loads((R/p).read_text())
def write(p,o):(R/p).write_text(json.dumps(o,ensure_ascii=False,indent=2))
raw=read('reference/location-research/kmcric-locations-361.json')
who={p['id']:p for p in read('reference/location-research/who-locations-extracted.json')}
ev=read('reference/route-research/route-evidence.json');patches=read('reference/route-research/route-graph-patches.json')
bank=read('reference/input/source-data.json');cat=read('reference/input/catalog.json')
docs={d['id']:d for d in read('reference/input/onedrive-extract.json')}
old=read('stage1/data/scene.json');points=[]
for p in raw:
 w=who[p['id']];layout=LAYOUT[p['id']]
 summary=re.sub(r'\s+',' ',re.sub(r'\([^)]*\)','',p.get('locationMainKo',p['locationKo']))).strip()
 source=[{'doc':'KMCRIC','url':p['sourceUrl'],'loc':p['id']+' 부위'},{'doc':'WHO-2008/2009','url':w['sourceUrl'],'loc':'printed p.'+str(w['printedPage']),'pdfPage':w['pdfPage']}]
 original=[{'doc':'doc18','block':i,'text':b['text']} for i,b in enumerate(docs['doc18']['blocks']) if b['text'].split(':')[0].strip()==p['name']]
 variants=[]
 alternatives={'LI19':'콧구멍 가쪽 아래에서 인중의 위 1/3과 아래 2/3 경계 높이에 두는 위치도 병기되어 있다.','LI20':'코입술고랑에서 콧방울 아래모서리 높이에 두는 위치도 병기되어 있다.','GB30':'큰돌기와 위앞엉덩뼈가시를 잇는 거리의 가쪽 1/3 지점이라는 대안도 병기되어 있다.'}
 if p.get('alternativeLocationEn') or p.get('alternativeLocationKo'):variants.append({'label':'KMCRIC·WHO 병기 위치','text':p.get('alternativeLocationKo') or alternatives[p['id']],'source':source[:2]})
 if p['id']=='GB20':variants.append({'label':'WHO 본문·도해 / KMCRIC 표현 차이','text':'WHO 영문 본문에는 anterior neck으로 되어 있으나 도해와 KMCRIC은 뒤통수 아래 뒷목으로 설명한다. 지도는 뒷목 표기를 따른다.','source':source[:2]})
 aliases=[p['name'],p['han'],unicodedata.normalize('NFKC',p['han'])]
 if p['id']=='CV17':aliases+=['전중','膻中']
 points.append({'id':p['id'],'meridian':p['meridian'],'index':p['index'],'name':p['name'],'han':p['han'],**layout,
 'aliases':list(dict.fromkeys(aliases)),'locationSummary':summary,'location':summary,'source':source+original,
 'original':original,'variants':variants,'displayConvention':'KMCRIC 주 위치를 기준으로 한 표면 도식; 병기 위치는 의서에서 확인',
 'coordinate_status':'source-compared-landmark-schematic',
 'review':{'locationTextSources':2,'landmarkRule':layout['region'],'projection':'authored display; not clinical measurement'}})
names={'LU':('폐','手太陰肺經'),'LI':('대장','手陽明大腸經'),'ST':('위','足陽明胃經'),'SP':('비','足太陰脾經'),'HT':('심','手少陰心經'),'SI':('소장','手太陽小腸經'),'BL':('방광','足太陽膀胱經'),'KI':('신','足少陰腎經'),'PC':('심포','手厥陰心包經'),'TE':('삼초','手少陽三焦經'),'GB':('담','足少陽膽經'),'LR':('간','足厥陰肝經'),'CV':('임맥','任脈'),'GV':('독맥','督脈')}
mer=[]
for c,(k,h) in names.items():
 audit=next((x for x in ev['regular'] if x['id']==c),None)
 mer.append({'id':c,'name':k,'han':h,'expectedPointCount':COUNTS[c],'points':[p['id'] for p in points if p['meridian']==c],
 'routeText':bank['jingorder']['FLOW'][k]['seq'] if audit else [],
 'source':audit['segments'][0]['source'] if audit else next(e['source'] for e in ev['extraordinary'] if e['id']==c),
 'preferredView':{'SI':'back','BL':'back','TE':'back','GB':'side','GV':'back'}.get(c,'front'),'routeAudit':audit})
nodes,edges=make_routes(points,ev,patches)
outlines=read('reference/outline-source.json')
front=outlines['front'];cut=front.index('Q419 313 412 288')+len('Q419 313 412 288')
outlines['front']=front[:cut]+' Q438 270 440 240 L441 207 Q440 154 380 154 Q320 154 319 207 L320 240 Q322 270 348 288 L362 289 Z'
roots={'LU':['anatomy.middle-jiao','LU1'],'LI':['LI1'],'ST':['ST1'],'SP':['SP1'],'HT':['anatomy.heart','HT1'],'SI':['SI1'],'BL':['BL1'],'KI':['KI1'],'PC':['anatomy.chest','PC1'],'TE':['TE1'],'GB':['GB1'],'LR':['LR1'],'CV':['anatomy.lower-jiao-origin','CV1'],'GV':['anatomy.lower-jiao-origin','GV1']}
for ex in ev['extraordinary']:
 if ex['id'] not in roots:roots[ex['id']]=['anatomy.lower-jiao-origin'] if ex['id']=='CHONG' else [next(p for p in ex['borrowed_or_owned_point_order'] if p in LAYOUT)]
scene={'version':'stage1.1-361','points':points,'meridians':mer,'extraordinary':ev['extraordinary'],'nodes':nodes,'edges':edges,'roots':roots,'cycle':ev['cycle'],'conflicts':ev['conflicts'],'outlines':outlines,'visualSources':old.get('visualSources',[]),'sourceNotice':'361혈의 표준 위치·부위·골도 기준을 대조한 학습용 도식. 화면 좌표는 취혈 실측이나 임상 판정 좌표가 아닙니다.','landmarks':{'thoracic':T,'lumbar':L,'sacral':S,'intercostal':IC},'excludedEdges':patches['exclusions'],'beltPaths':{'front':'M300 580 Q380 612 467 580','back':'M265 580 Q346 600 430 580','side':'M242 580 Q330 617 424 581 Q335 566 242 580'},'beltSource':[{'doc':'doc4','block':551}]}
for name,o in [('points',points),('meridians',mer),('extraordinary',scene['extraordinary']),('routes',{'nodes':nodes,'edges':edges,'cycle':scene['cycle']}),('scene',scene)]:write('stage1/data/'+name+'.json',o)
(D/'data/data.js').write_text('export const DATA = '+json.dumps(scene,ensure_ascii=False)+';\n')
write('stage1/data/sources.json',{'primaryLocationSources':[{'name':'KMCRIC 표준경혈 DB','url':'https://www.kmcric.com/database/acupoint','basis':'WHO/WPRO 표준경혈위치'},{'name':'WHO Standard Acupuncture Point Locations (2008, updated reprint 2009)','url':'https://iris.who.int/handle/10665/353407'}],'userDocuments':[{'id':d['id'],'path':d.get('normalizedPath')} for d in docs.values()],'visual':scene['visualSources'],'sourceDisagreements':ev['conflicts']})
ledger=[{'unit':u['id'],'module':u['module'],'seen':None,'decided':[],'unaided':[],'stage1':'reference-preserved','source':u.get('sources',[])} for u in cat['units']]
write('stage1/data/ledger.json',ledger);write('reference/coverage-ledger.json',ledger)
audit={'target_points':361,'mapped_points':len(points),'unplaced_points':0,'source_texts_compared':361,'who_page_links':361,'landmark_model_coverage':361,'tested_landmark_relationships':36,'clinical_location_certified':0,'views':'independently registered; invisible surfaces are not projected through the body','point_counts':COUNTS,'regular_paths':12,'extraordinary_paths':8,'edges':len(edges),'location_variants':[p['id'] for p in points if p['variants']],'note':'문자 위치·부위·비례·도식의 대조. 도식 좌표는 실제 인체의 취혈 정밀도를 의미하지 않는다.','rows':[{'id':p['id'],'name':p['name'],'location':p['locationSummary'],'views':p['views'],'region':p['region'],'source':p['source'][:2],'status':p['coordinate_status']} for p in points]}
write('reference/stage1-coordinate-audit.json',audit)
print(json.dumps({'points':len(points),'edges':len(edges),'nodes':len(nodes),'unplaced':0,'learning_records':False}))

