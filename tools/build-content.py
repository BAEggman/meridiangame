from pathlib import Path
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT.parent
catalogPath=ROOT/'reference/input/catalog.json';sourcePath=ROOT/'reference/input/onedrive-extract.json'
catalog=json.loads(catalogPath.read_text())
source=json.loads(sourcePath.read_text())
config=json.loads((ROOT/'dist/config.json').read_text())
(ROOT/'dist/config.mjs').write_text('export const CONFIG = '+json.dumps(config,ensure_ascii=False,indent=2)+';\n')
docs={d['id']:d for d in source}; units={u['id']:u for u in catalog['units']}
# These are schematic landmarks, not acupuncture measurements.
nodes={
 'middle':['中焦','중초',350,365,'deep'], 'colon':['大腸','대장',365,459,'deep'],
 'stomach':['胃口','위구',329,328,'deep'], 'diaphragm':['膈','격',350,292,'deep'],
 'lung':['肺','폐',325,237,'deep'], 'tract':['肺系','폐계',350,189,'deep'],
 'axilla':['腋下','액하',261,257,'surface'],'upper':['臑內','위팔 안쪽',239,332,'surface'],
 'elbow':['肘中','팔꿈치 안쪽',215,404,'surface'],'forearm':['臂內上骨下廉','아래팔 요골 쪽',178,463,'surface'],
 'wrist':['寸口','촌구',143,518,'surface'],'thenar':['魚','어복',121,550,'surface'],
 'edge':['魚際','어제 경계',96,564,'surface'],'thumb':['大指端','엄지 끝',71,554,'surface'],
 'backwrist':['腕後','손목 뒤쪽',158,492,'surface'],'indexedge':['次指內廉','검지 안쪽',101,593,'surface'],'index':['次指端','검지 끝',81,620,'surface'],
 'heart':['心','심',376,254,'deep'],'liver':['肝','간',394,335,'deep'],'kidney':['腎','신',394,404,'deep'],
 'little':['小指端','새끼손가락 끝',135,624,'surface'], 'nose':['鼻','코',352,123,'surface'],
 'lieque':['列缺','열결',157,510,'point'],'taiyuan':['太淵','태연',138,534,'point'],
 'ren':['任脈','임맥',350,540,'network'],'du':['督脈','독맥',411,541,'network'],
 'chong':['衝脈','충맥',305,542,'network'],'dai':['帶脈','대맥',425,455,'network'],
 'pc':['心包','심포',483,360,'network'],'ht':['心經','심경',519,360,'network'],
 'li':['大腸經','대장경',520,526,'network'],'sp':['脾經','비경',481,645,'network'],
 'wood':['木','목',498,224,'seal'],'fire':['火','화',553,266,'seal'],'earth':['土','토',531,329,'seal'],
 'metal':['金','금',462,329,'seal'],'water':['水','수',440,266,'seal'],
 'taiBai':['太白','태백',250,747,'point'],'yuji':['魚際穴','어제혈',108,577,'point'],'shaofu':['少府','소부',568,572,'point']}
facts=[]
def add(id,fr,to,label,prompt,quote,kind='flow',unit=None,refs=None,options=None,aliases=None,detail='',assessment='map'):
 refs=refs or [('doc4',194)]
 if kind not in ['flow','branch'] and assessment == 'map': assessment='selection'
 sourceRefs=[{'document':did,'block':i,'text':docs[did]['blocks'][i]['text']} for did,i in refs]
 facts.append(dict(id=id,fr=fr,to=to,label=label,prompt=prompt,quote=quote,kind=kind,unitIds=unit or [],sources=sourceRefs,options=options or [],aliases=aliases or [],detail=detail,assessment=assessment))
add('lu-origin','middle','middle','起於中焦','第一站。肺手太陰之脈，起於何處？','起於中焦',unit=['flow-폐-1','acu-gyeongmaek-起始'],options=['middle','lung','heart','kidney'])
flow=[
('lu-colon','middle','colon','下絡大腸','中焦에서 아래로 絡하는 곳을 가리키세요.',2),
('lu-stomach','colon','stomach','還循胃口','大腸을 絡한 뒤, 어디를 따라 돌아옵니까?',3),
('lu-diaphragm','stomach','diaphragm','上膈','胃口에서 위로 지나가는 경계를 가리키세요.',4),
('lu-lung','diaphragm','lung','屬肺','膈을 올라 이 경맥이 屬하는 장부를 가리키세요.',4),
('lu-tract','lung','tract','從肺系','肺에서 어느 연결 부위를 따릅니까?',5),
('lu-axilla','tract','axilla','橫出腋下','肺系에서 가로로 나오는 곳을 가리키세요.',6),
('lu-upper','axilla','upper','下循臑內','腋下 다음으로 내려가 따르는 부위를 가리키세요.',7),
('lu-elbow','upper','elbow','下肘中','위팔 안쪽을 내려가 도달할 관절을 가리키세요.',9),
('lu-forearm','elbow','forearm','循臂內上骨下廉','肘中에서 이어지는 아래팔의 길을 가리키세요.',10),
('lu-wrist','forearm','wrist','入寸口','아래팔에서 들어가는 손목 부위를 가리키세요.',11),
('lu-thenar','wrist','thenar','上魚','寸口 다음으로 올라가는 부위를 가리키세요.',12),
('lu-edge','thenar','edge','循魚際','魚에서 따르는 경계를 가리키세요.',13),
('lu-thumb','edge','thumb','出大指之端','본행의 끝. 어느 손가락 끝으로 나옵니까?',14)]
for id,fr,to,label,prompt,i in flow:add(id,fr,to,label,prompt,label,unit=[f'flow-폐-{i}'])
add('lu-branch-origin','wrist','backwrist','從腕後','其支者. 본행의 끝이 아니라 가지가 갈라지는 곳을 가리키세요.','其支者，從腕後',kind='branch',unit=['flow-폐-15','flow-폐-16'],refs=[('doc3',2),('doc4',202)])
add('lu-index-edge','backwrist','indexedge','直出次指內廉','腕後의 가지는 어느 손가락의 안쪽 모서리를 향합니까?','直出次指內廉',kind='branch',unit=['flow-폐-17'],refs=[('doc3',2),('doc4',202)])
add('lu-index-tip','indexedge','index','出其端','그 가지가 마치는 끝을 가리키세요.','出其端',kind='branch',unit=['flow-폐-18'],refs=[('doc3',2),('doc4',202)])
add('lu-next','index','li','次指에서 大腸經으로','이 가지 끝에서 다음 경맥의 기록을 펼칩니다. 어느 경맥입니까?','肺經의 次指 분지 → 大腸經',kind='connection',unit=['saambosafill-base-0'],refs=[('doc3',2),('doc4',202)],options=['li','pc','ht','sp'],detail='경맥 연접의 기록입니다. 任脈 통회와 다른 관계입니다.')
add('lu-luo','wrist','lieque','肺의 絡穴','肺의 絡을 조사합니다. 해당 혈을 가리키세요.','肺의 絡穴 = 列缺',kind='luo',unit=['acu-폐-락'],refs=[('doc15',0)],options=['lieque','taiyuan','yuji'],detail='列缺의 絡穴 소속과 任脈 통회는 별개 부품입니다.')
add('lu-ren','lieque','ren','列缺 通任脈','列缺의 팔맥교회 기록. 어느 기경과 통합니까?','列缺 — 任脈',kind='confluent',unit=['acu-palmaek-0','cloze-ren'],refs=[('doc4',421),('doc4',434)],options=['ren','du','chong','dai'],detail='팔맥교회 관계. 肺經 본행이 이 선을 따라 任脈으로 흐른다는 뜻이 아닙니다.')
add('lu-yuan','wrist','taiyuan','肺의 原穴','이번에는 肺의 原穴을 조사합니다. 가리킬 곳은?','肺의 原穴 = 太淵',kind='specific',unit=['acu-폐-원'],refs=[('doc15',0)],options=['lieque','taiyuan','yuji'])
add('lu-shu','wrist','taiyuan','肺의 輸穴','같은 손목, 다른 관계. 肺의 輸穴을 가리키세요.','肺 輸穴 = 太淵',kind='shu',unit=['acu-osu-폐-2'],refs=[('doc18',10),('doc4',372)],options=['lieque','taiyuan','yuji'],detail='原穴로 맞혔다고 輸穴 관계가 자동 설치되지는 않습니다.')
add('lu-earth','taiyuan','earth','陰經 輸土','陰經의 輸에 놓일 五行을 바퀴에서 고르세요.','陰經：井木 滎火 輸土 經金 合水',kind='derive',unit=['acu-osu-폐-2','saambosafill-base-0'],refs=[('doc4',372)],options=['wood','fire','earth','metal','water'],detail='바퀴 선택은 보조 선택 회상으로 기록합니다. 지연 독립 회상은 빈 서찰에서 확인합니다.',assessment='selection',aliases=['토','土'])
add('lu-maihui','wrist','taiyuan','脈會','八會의 脈會를 같은 몸 위에서 찾습니다.','脈會 = 太淵',kind='specific',unit=['acu-palhoe-5'],refs=[('doc4',411),('doc4',417)],options=['lieque','taiyuan','yuji'])
add('lu-position','upper','upper','行少陰心主之前','肺經은 少陰·心主의 어느 쪽을 지납니까? 의서의 빈 서찰에 적으세요.','行少陰心主之前',kind='relative',unit=['flow-폐-8'],refs=[('doc4',194)],assessment='text',aliases=['앞','앞쪽','전','前','앞을','앞쪽을','소음심주앞','소음심주의앞'])
add('lu-mother','metal','earth','土生金','肺金이 虛할 때 補母의 母를 고르세요.','土生金 → 補母 土',kind='derive',unit=['saambosafill-3'],refs=[('doc4',608)],options=['wood','fire','earth','metal','water'],assessment='selection',aliases=['토','土'])
add('lu-mother-point','earth','taiBai','脾의 土穴','자경 太淵과 함께 母經에서 쓸 土穴을 가리키세요.','肺正格 補：太淵·太白',kind='derive',unit=['saambosafill-3'],refs=[('doc4',608)],options=['taiBai','shaofu','yuji'],detail='이 원정은 肺正格의 補母 부분만 다룹니다. 瀉官까지 완성한 처방이 아닙니다.')
# Mission routes share actual semantic fact IDs, not names.
inner=['lu-origin','lu-colon','lu-stomach','lu-diaphragm','lu-lung']
arm=inner+['lu-tract','lu-axilla','lu-upper','lu-position','lu-elbow','lu-forearm','lu-wrist','lu-thenar','lu-edge','lu-thumb']
wrist=arm[:12]
missions=[
 dict(id='inner',name='안쪽의 불씨',han='內行',tag='첫 기록',desc='中焦에서 肺까지. 屬과 絡이 다른 방향을 만든다.',route=inner,focus=7,requires=[],reward='안쪽 길의 원문이 지도에 남습니다.',duration='2–3분',layer='deep'),
 dict(id='thumb',name='엄지에 닿는 빛',han='本行',tag='본행',desc='안쪽 길을 맡기고 팔과 엄지 끝까지 나아간다.',route=arm,focus=9,requires=['inner'],reward='본행과 支脈을 비교할 수 있습니다.',duration='4–6분',layer='surface'),
 dict(id='branch',name='끝에서 갈라지지 않는 길',han='支脈',tag='大腸으로',desc='엄지 끝 대신 손목 뒤로. 次指에서 다음 경맥을 찾는다.',route=wrist+['lu-branch-origin','lu-index-edge','lu-index-tip','lu-next'],focus=9,requires=['inner'],reward='大腸經 연접을 발견합니다.',duration='3–4분',layer='surface'),
 dict(id='ren',name='任의 서찰',han='通脈',tag='기경과 연결',desc='列缺의 두 역할을 나누고 任脈의 기록을 가져온다.',route=wrist+['lu-luo','lu-ren'],focus=9,requires=['inner'],reward='기경은 초반부터 같은 몸에 연결됩니다.',duration='2–3분',layer='surface'),
 dict(id='roles',name='같은 혈, 다른 세 자리',han='太淵',tag='공유 부품',desc='原·輸·脈會. 한 이름에 매달린 세 관계를 따로 다룬다.',route=wrist+['lu-yuan','lu-shu','lu-earth','lu-maihui'],focus=9,requires=['inner'],reward='서로 다른 관계의 자동 운행을 비교합니다.',duration='3–4분',layer='surface'),
 dict(id='mother',name='肺에서 脾로 보는 까닭',han='補母',tag='사암의 첫 도출',desc='陰經 輸土와 土生金을 이용해 補母의 두 혈을 연결한다.',route=inner+['lu-yuan','lu-shu','lu-earth','lu-mother','lu-mother-point'],focus=7,requires=['roles'],reward='肺正格 중 補母의 도출을 조작합니다.',duration='2–3분',layer='surface'),
 dict(id='survey',name='세 갈래를 한 손으로',han='合觀',tag='첫 장의 완주',desc='본행·支脈·任脈을 연달아 조사한다. 자동 운행이 늘수록 손이 남는다.',route=arm+['lu-branch-origin','lu-index-edge','lu-index-tip','lu-next','lu-luo','lu-ren','lu-yuan','lu-shu','lu-earth','lu-maihui'],focus=8,requires=['thumb','branch','ren'],reward='첫 장의 흐름을 조용히 감상합니다. 기록은 다음 날에도 남습니다.',duration='3–5분',layer='surface')]
for mission in missions: mission['focus']=config['expedition_budgets'][mission['id']]
areas=[
 ['十二經脈','flow','본행·지행·직행과 장부의 屬絡','肺 본행과 支脈을 직접 탐사','다른 11경의 원문은 의서에서 열람'],
 ['經別·絡脈','network','정경의 체내·체표 연락','肺 絡穴 列缺의 관계만 사용','경별 離入出合·十五絡의 개별 기능은 후속'],
 ['奇經八脈','confluent','정경과 기경의 통회·조절 관계','列缺—任脈을 초반 탐사','衝·督·帶·蹻·維는 원문 열람과 후속 설계'],
 ['經筋·皮部','layer','결취산락과 체표 분포','전체 맥락의 별도 관계층으로 보존','현재 흐름 엔진의 배관으로 취급하지 않음'],
 ['五輸·특정혈','parts','혈의 소속·분류·기능 관계','太淵의 原·輸·脈會와 列缺','다른 혈의 원문은 의서에서 열람'],
 ['舍岩鍼法','derive','五行·母子·虛實·補瀉 도출','肺正格 補母 부분을 조작','瀉官과 다른 정승한열격은 원문 열람'],
 ['病症·主治','evidence','원문 병증과 경맥·혈의 관계','원문과 관계 탐사 목적을 함께 열람','환자 3칸 진단은 아직 미구현'],
 ['標本·根結·氣街·四海','systems','국소와 전신을 연결하는 체계','원문을 전체 목차에서 열람','독립된 관계 규칙으로 후속 확장'],
 ['발전사·穴名유래','history','문헌·의가·용어의 출전','원문을 전체 목차에서 열람','동료·책장·화첩의 실제 사건은 후속']]
used={uid for f in facts for uid in f['unitIds']}
ledger=[{'unitId':u['id'],'module':u['module'],'kind':u.get('kind'),'status':'play-linked' if u['id'] in used else ('held-conflict' if u.get('conflict') else 'reference-only'),'parts':[f['id'] for f in facts if u['id'] in f['unitIds']]} for u in catalog['units']]
publicUnits=[{k:u.get(k) for k in ['id','module','topic','q','a','note','conflict','sources','kind']} for u in catalog['units']]
refs={'documents':[{'id':did,'name':Path(docs[did]['path']).name,'blocks':docs[did]['blocks'],'images':docs[did]['images']} for did in ['doc3','doc4','doc15','doc18']], 'units':publicUnits,'areas':areas,'ledger':ledger,'notice':'원문 보존은 실제 플레이 구현과 다릅니다. 전체 1,586단위 중 play-linked 표시는 일부 사실을 본 시제품의 관계 부품에 연결했다는 뜻입니다.'}
(ROOT/'dist/reference.json').write_text(json.dumps(refs,ensure_ascii=False))
content=dict(version='0.1.0',nodes=nodes,facts=facts,missions=missions,areas=areas,sourceUnits=1586,linkedUnits=len(used),referenceOnly=sum(x['status']=='reference-only' for x in ledger),held=sum(x['status']=='held-conflict' for x in ledger))
(ROOT/'dist/content.mjs').write_text('export const CONTENT = '+json.dumps(content,ensure_ascii=False,indent=2)+';\n')
(ROOT/'reference/coverage-ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2))
(ROOT/'reference/source-hashes.json').write_text(json.dumps([{'file':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [catalogPath,sourcePath,ROOT/'reference/input/source-data.json']],ensure_ascii=False,indent=2))
(ROOT/'dist/audio').mkdir(exist_ok=True)
for fact in facts:
 for uid in fact['unitIds']:
  u=units.get(uid,{})
  if u.get('audio'):
   src=BASE/'afterwork-prototype/dist'/u['audio']
   dest=ROOT/'dist/audio'/src.name
   if src.exists():shutil.copy2(src,dest)
   if dest.exists():fact['audio']='audio/'+src.name;break
(ROOT/'dist/content.mjs').write_text('export const CONTENT = '+json.dumps(content,ensure_ascii=False,indent=2)+';\n')
print(json.dumps({'parts':len(facts),'missions':len(missions),'linkedUnits':len(used),'wholeUnits':len(ledger)},ensure_ascii=False))
