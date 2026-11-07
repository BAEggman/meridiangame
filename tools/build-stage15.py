from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
s=json.loads((R/'stage1/data/scene.json').read_text())
v=json.loads((R/'reference/location-research/onedrive-location-variants.json').read_text())
pts=[p for p in s['points'] if p['meridian']=='LU']
notes=[60,62,64,67,69,67,64,62,60,67,64]
elements={5:'水',8:'金',9:'土',10:'火',11:'木'}
for i,p in enumerate(pts):
 p['variants']+= [x for x in v['variants'] if x['pointId']==p['id']]
 p['midi']=notes[i];p['element']=elements.get(i+1)
 # Only the cited excerpt is needed by this small play surface, not other channels' raw textbook blocks.
 for x in p['variants']:
  x['source']=[{k:val for k,val in q.items() if k!='text'} for q in x['source']]
data={'points':pts,'outline':s['outlines']['front'],'scope':'肺經11穴 · 前面','melodyNote':'五輸의 五行은 교재 acu.MERID / osstep.YIN. 음높이는 宮(土)=C, 商(金)=D, 角(木)=E, 徵(火)=G, 羽(水)=A로 택한 창작 기억 단서. 나머지 6혈은 연결음이며 五行 속성을 뜻하지 않음.','context':'이것은 肺經 체표 11혈의 학습 루프입니다. 中焦에서 시작하는 체내 유주와 腕後→次指 분지를 포함한 전체 지도는 1단계 자료에 보존되어 있습니다. 少商→中府를 해부학적 연결선으로 그리지 않습니다.'}
(R/'stage15/data/lung.js').write_text('export const LUNG = '+json.dumps(data,ensure_ascii=False)+';\n')
print('肺經 11혈 · LU7 교재/표준 병기 · 전체 361혈 소스 보존')
