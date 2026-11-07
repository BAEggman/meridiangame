# 經絡 게임 구현 지시서 v1 — GPT용

Nov 7, 2026 · @성영석

## 1. 읽는 법·작업 규칙·목표

이 문서는 GPT에게 주는 구현 지시서다. 설계의 근거는 「타이쿤·탐험 게임 100선 — 재미의 해부와 經絡 게임 적용」 6·7절에 있고, 이 문서는 그것을 코드와 데이터로 옮기는 방법만 적는다. 사용자는 한 사람이고 개인용이다.

### 한 줄

게임의 상태는 하나다. 氣가 스스로 흐르는가. 처음의 몸은 흐르지 않아서 모든 穴에서 氣를 손으로 밀어야 하고(회상), 외운 구간은 스스로 흐르며 더는 사용자를 부르지 않는다(자동화 = 암기). 잊어버림은 자동 운행의 고장이고, 끝은 몸 전체가 손 안 대도 하루 50번 도는 五十營이다. 세계는 經絡圖 하나다.

### 규칙 체계는 넷뿐이다

| 체계 | 한 줄 |
| --- | --- |
| 흐름 | 經마다 流注 순서로 氣가 흐른다. 설치된 구간은 저절로, 아닌 구간은 사용자가 다음 穴을 지목해야 흐른다 |
| 고장 | 시간으로 오는 마모와 오답으로 오는 결함. 고장은 부품 단위로 생기고 그 부품을 쓰는 기계만 멈춘다 |
| 환자 | 증상 단서로 經·穴·虛實 세 칸을 확정하고 五行 바퀴로 치료한다 |
| 검문 | 서류 한 장에서 한 군데가 틀린 가짜를 잡는다. 이설은 出典 도장 둘로 통과시킨다 |

醫家 대사, 화첩, 노래, 銅人, 코덱스는 규칙이 없는 내용물이다. 다섯 번째 규칙 체계를 만드는 제안은 하지 않는다.

### 작업 규칙

1. 한 대화에 한 단계만 만든다(6절). 다음 단계의 기능을 미리 넣지 않는다.
2. 기능을 제안하기 전에 스스로 묻는다. "이게 氣가 스스로 흐르는 것과 무슨 관계인가." 답이 없으면 제안하지 않는다.
3. 사실을 지어내지 않는다. 모든 부품은 기존 데이터(허브 문항 은행, 1,586 학습 단위, OneDrive 원문자료 18개)에서 온다. 교재와 원전이 다르면 둘 다 보존하고 출전을 붙인다. 한쪽을 정답으로 고르지 않는다.
4. 게임 수치(氣 비용, 간격, 배수)는 config.json에 두고, 원문 사실과 섞지 않는다.
5. 문항을 절차 생성하지 않는다. 환자·검문 서류는 은행의 사실과 함정을 조합해 만들되, 조합 규칙은 이 문서가 정한 범위 안에서만.
6. 작동 검사 통과를 재미나 학습의 검증으로 적지 않는다. 재미는 사용자의 20분 플레이와 검수 양식(7절)으로만 판정된다.
7. 매 단계 끝에 실행 가능한 빌드, 10줄 변경 요약, "하지 않은 것" 목록, 대장 갱신본을 낸다(7절).
8. 버린다: 경락의 마을의 주민 운반·건설·피로 시뮬레이션, D2R 에셋 도구, 같은 단어 매칭 네트워크. 남긴다: 허브 문항 은행, 1,586 단위와 coverage-ledger.json, 낭독 1,569파일, 암기송 12곡, 五行·母子·虛實 계산기, 의미 구분 관계망, 마을판의 패드 입력 코드.

### 학습 기록의 세 가지 구분 (어기면 게임이 아니라 거짓말이 된다)

- 보기·듣기·자동 진행은 노출이다. 회상이 아니다.
- 힌트 뒤 정답, 선지에서 고르기(인식)는 도움받은 성공이다. 따로 기록한다.
- 설치(銅人 점등, 자동 흐름)는 다른 날의 무힌트 회상 성공 두 번에만 준다.

## 2. 기술 스택과 파일 구조

단일 페이지 웹 앱, 빌드 도구 없이 ES 모듈과 정적 파일만 쓴다. 지도는 SVG(선이 선명하고 CSS로 먹·朱砂·금 스타일을 주기 쉽고 클릭 판정이 공짜), 氣 입자는 그 위의 Canvas 한 장. 프레임워크 없이 vanilla JS. 실행은 기존 묶음의 시작하기.py 로컬 서버 그대로, 나중에 GitHub Pages. 저장은 localStorage + JSON 내보내기·가져오기. 엔진은 순수 함수로 짜서 node 테스트가 돌게 한다(UI 없이 하루를 시뮬레이션할 수 있어야 한다).

```
meridian-flow/
  index.html
  config.json              게임 수치 전부 (4절 초기값 표)
  main.js
  src/engine/
    parts.js               부품 상태: 마모·결함·수리·설치
    machines.js            기계 가동 판정, 부품 공유 전파
    flow.js                流注 흐름, 정체 지점, 하류 굳주림
    srs.js                 간격·기한·기록 (무힌트/도움/노출 구분)
    storyteller.js         오늘의 계획 (큐 넷, 몲, 완급)
    patients.js            환자 생성·단서·채점
    inspection.js          검문 서류 생성·채점
    wuxing.js              五行·母子·虛實 계산기 (기존 코드 이식)
    ledger.js              1,586 단위 대장
    save.js
  src/ui/
    map.js                 SVG 經絡圖, 3뷰 2층, 안개
    qi.js                  Canvas 氣 입자 (흐름·깜빡임·꺼짐·재가동)
    tongren.js             銅人
    book.js                의서: 코덱스·穴典(화첩)·책장
    clinic.js              醫館: 환자 대기열·醫家
    booth.js               검문 창구
    wheel.js               五行 바퀴
    input.js               패드·키보드·마우스 (마을판 코드 이식)
    audio.js               암기송·낭독
  data/
    meridians.json         12正經 + 8奇經: 경로 좌표, 流注 순서, 속성
    points.json            361穴: 소속·코드·취혈 문장·유래·역할
    parts.json             부품 사전
    machines.json          기계 → 부품
    symptoms.json          是動·所生·주치
    traps.json             기출 함정 = 변장 은행
    physicians.json        醫家
    sources.json           출전 목록, 교재·원전 병기
    ledger.json            단위별 등장/결정/무힌트
  assets/audio/narration/  기존 1,569파일
  assets/audio/songs/      기존 12곡
  tests/
```

기존 자산이 어디로 가는지.

| 기존 파일 | 가는 곳 |
| --- | --- |
| afterwork-prototype/data/catalog.json (1,586 학습 단위), coverage-ledger.json | parts.json·ledger.json의 원재료 |
| meridian 허브 문항 은행(계통·순행·是動所生·특정혈·배수혈·교회혈·사암·변별) | symptoms.json, traps.json, points.json 역할 |
| 원문자료 doc3 유주 마스터표, doc15·16 원락극모배수, doc5 교회혈, doc18 경락이름유래, doc2 인체부위 이명 | meridians.json 순서, points.json 역할·유래·취혈 문장 |
| design-rethink-20261106/원문대조\_텍스트.json, 자료목록.json | sources.json (모든 부품의 source 필드) |
| meridian-prototype의 五行·母子·虛實 계산 | wuxing.js |
| meridian-village의 패드 입력·버튼 재지정 코드 | input.js |
| afterwork-prototype/dist/narration, audio/ | assets/audio |
| meridian-atelier-prototype의 의미 구분 관계망 | machines.json의 관계 기계(交會·表裏·奇經 통혈) |

모든 데이터 레코드는 source 배열을 가진다. 예: `"source": [{"doc": "doc3_유주_마스터표_12경.docx", "loc": "肺經 표 1행"}]`. source가 없는 레코드는 로드 시 거부한다. 교재와 원전이 다른 사실은 한 부품에 `variants: [{text, source}]`로 둘 다 담고, 채점은 어느 쪽이든 정답으로 본다.

## 3. 데이터 모델

부품(원자 사실)과 기계(부품의 조립)가 전부다. 다른 모든 것(환자, 서류, 醫家, 銅人)은 부품을 가리키기만 한다. 한 부품은 여러 기계에 쓰이고, 그것이 고장이 번지는 유일한 경로다.

### 3.1 부품 parts.json

```json
{
  "id": "p.LU.element",
  "kind": "element",
  "unit": "u-0412",
  "dirs": [
    {"ask": "肺經의 五行은?", "answer": "金", "ability": "relation"},
    {"ask": "金에 속하는 經은?", "answer": ["肺經", "大腸經"], "ability": "relation"}
  ],
  "variants": [],
  "source": [{"doc": "doc6_5장 경락.docx", "loc": "12경맥 총론 표"}]
}
```

- kind: element(五行) · assign(五輸 배속) · order(流注 인접 한 쌍) · route(起止·分支·교접) · role(原·絡·郄·募·背兪·八會·八脈交會·下合·交會) · relation(表裏·屬絡·通脈·相生·相剋) · rule(사암·配穴 규칙) · symptom(是動·所生·주치) · location(취혈 문장) · origin(이름 유래) · history(醫家·著書·穴數) · time(子午流注).
- unit: 1,586 학습 단위 id. 대장과 이어진다. 한 단위가 여러 부품으로 쪼개질 수 있다.
- dirs: 같은 사실을 묻는 방향들. ability는 이름 · 한자 · 순서 · 위치 · 관계 · 원리 · 예외 중 하나. 역방향이 부자연스러운 사실은 방향을 하나만 둔다.
- variants: 교재와 원전이 다를 때 둘 다. `[{"text": "...", "source": {...}, "label": "교재"}, {"text": "...", "source": {...}, "label": "원전"}]`. 어느 쪽을 답해도 정답이고 채점 기록에 label이 남는다.

### 3.2 부품 상태 state.parts (저장 파일)

```json
{
  "p.LU.element": {
    "status": "installed",
    "interval_days": 8,
    "last_unaided": "2026-11-05",
    "unaided_days": ["2026-11-01", "2026-11-05"],
    "due": "2026-11-13",
    "fault_since": null,
    "hinted": 1,
    "errors": 1
  }
}
```

- status: manual(아직 설치 전, 만날 때마다 회상) · installed(자동) · worn(기한 임박, 깜빡임) · fault(꺼짐). 파생 값은 저장하지 않고 날짜와 interval에서 계산한다(4절).
- installed 조건: unaided\_days에 20시간 이상 떨어진 날이 두 개 이상.

### 3.3 기계 machines.json

```json
[
  {"id": "m.LU.flow", "kind": "flow", "name": "肺經 흐름",
   "parts": ["p.LU.order.01", "p.LU.order.02", "p.LU.order.03", "p.LU.order.04", "p.LU.order.05",
             "p.LU.order.06", "p.LU.order.07", "p.LU.order.08", "p.LU.order.09", "p.LU.order.10", "p.LU.route"],
   "output": {"meridian": "LU"}},
  {"id": "m.LU.zhengge", "kind": "deriver", "name": "肺正格",
   "parts": ["p.rule.zhengge", "p.LU.element", "p.sheng.earth-metal", "p.ke.fire-metal",
             "p.LU.assign.shu", "p.SP.assign.shu", "p.LU.assign.ying", "p.HT.assign.ying"],
   "output": {"tonify": ["太白", "太淵"], "sedate": ["少府", "魚際"]}, "codex": "肺正格"},
  {"id": "m.LU.shengge", "kind": "deriver", "name": "肺勝格",
   "parts": ["p.rule.shengge", "p.LU.element", "p.sheng.metal-water", "p.ke.fire-metal",
             "p.LU.assign.ying", "p.HT.assign.ying", "p.LU.assign.he", "p.KI.assign.he"],
   "output": {"tonify": ["少府", "魚際"], "sedate": ["陰谷", "尺澤"]}, "codex": "肺勝格"},
  {"id": "m.LU-LI.yuanluo", "kind": "configurer", "name": "肺·大腸 主客原絡",
   "parts": ["p.rule.yuanluo", "p.LU.biaoli", "p.LU.role.yuan", "p.LI.role.luo"],
   "output": {"points": ["太淵", "偏歷"]}, "codex": "主客原絡配穴"},
  {"id": "m.LU.renmai", "kind": "shortcut", "name": "列缺→任脈",
   "parts": ["p.LU.role.bamai"], "output": {"from": "列缺", "to": "任脈"}},
  {"id": "m.bahui.mai", "kind": "tool", "name": "脈會",
   "parts": ["p.LU.role.bahui"], "output": {"point": "太淵"}},
  {"id": "m.LU.diagnoser", "kind": "diagnoser", "name": "肺經 병증",
   "parts": ["p.LU.symptom.shidong.01", "p.LU.symptom.shidong.02", "p.LU.symptom.suosheng.01"],
   "output": {"meridian": "LU"}}
]
```

- kind: flow(흐름) · deriver(사암 도출) · configurer(配穴) · tool(八會·下合 등 도구) · shortcut(交會·八脈交會·表裏) · diagnoser(증상→經).
- 가동 조건: 모든 parts가 installed 또는 worn이고 fault가 없다. worn이 하나라도 있으면 기계는 돌되 깜빡인다. manual이 하나라도 있으면 사용자가 그 부품을 직접 넣어야 돈다.
- 주의: 肺正格이 脾經의 太白을 빌리므로 脾經 부품 하나가 肺經 기계에 들어간다. 이 교차가 부품 공유의 핵심이다.

### 3.4 肺經 부품 목록 (샘플, 이 형식으로 12經 전부)

| id | kind | 묻는 방향 → 답 |
| --- | --- | --- |
| p.LU.element | element | 肺經 → 金 / 金 → 肺·大腸 |
| p.LU.yinyang | assign | 肺經 → 手太陰, 陰經의 五輸은 井木·滎火·輸土·經金·合水 |
| p.LU.assign.jing / ying / shu / jing2 / he | assign | 井 → 少商(木), 滎 → 魚際(火), 輸 → 太淵(土), 經 → 經渠(金), 合 → 尺澤(水); 역방향 전부(土 → 太淵) |
| p.LU.role.yuan | role | 原穴 → 太淵 (규칙 부품 p.rule.yin-yuan: 陰經의 原穴은 輸穴) |
| p.LU.role.luo | role | 絡穴 → 列缺, 大腸經으로 |
| p.LU.role.xi | role | 郄穴 → 孔最 |
| p.LU.role.mu / p.LU.role.beishu | role | 募穴 → 中府 / 背兪穴 → 肺兪 |
| p.LU.role.bahui | role | 脈會 → 太淵 |
| p.LU.role.bamai | role | 八脈交會 → 列缺 通 任脈 |
| p.LU.order.01 … p.LU.order.10 | order | 中府→雲門, 雲門→天府, … 魚際→少商 (인접 한 쌍씩, 정체는 쌍 단위로 난다) |
| p.LU.route | route | 起於中焦, 下絡大腸, 少商에서 商陽으로 교접 |
| p.LU.biaoli | relation | 表裏 → 大腸 |
| p.LU.time | time | 寅時 |
| p.LU.symptom.shidong.NN / suosheng.NN | symptom | 是動·所生 문장 하나씩 (허브 은행 그대로) |
| p.LU.location.NN | location | 穴마다 취혈 문장 |
| p.LU.origin.NN | origin | 穴마다 이름 유래 (doc18) |
| p.rule.zhengge / p.rule.shengge | rule | 虛 → 補母·瀉剋我 / 實 → 瀉子·補剋我 |
| p.sheng.earth-metal 등 5 / p.ke.fire-metal 등 5 | relation | 相生 5 · 相剋 5 (전 經이 공유) |

### 3.5 환자·검문 서류·醫家·대장·로그

```json
{"patient": {"id": "pt.20261107.3", "truth": {"meridian": "LU", "point": "太淵", "xushi": "虛"},
  "clues": [{"text": "缺盆中痛", "part": "p.LU.symptom.shidong.03", "shown": true},
            {"text": "寸口 脈 無力", "part": "p.LU.role.yuan", "shown": false, "test": "切診"}],
  "tests": [{"name": "問診", "cost": 1}, {"name": "切診", "cost": 1}],
  "slots": {"meridian": null, "point": null, "xushi": null}},
 "inspection": {"id": "insp.20261107.1", "kind": "chart",
  "fields": [{"label": "絡穴", "value": "列缺"}, {"label": "郄穴", "value": "孔最"},
             {"label": "脈會", "value": "大淵", "forged": true, "truth": "太淵", "trap": "t.hanja.taiyuan"}],
  "legit_variant": false},
 "physician": {"id": "phys.huangfu-mi", "name": "皇甫謐", "zi": "士安", "book": "鍼灸甲乙經", "era": "晉", "count": 349,
  "function": "catalog", "recruit_parts": ["p.hist.huangfu.zi", "p.hist.huangfu.book"],
  "lines": {"recruit": "…", "first_cure": "…", "repair": "…", "boss_pass": "…", "boss_fail": "…", "absent": "…"}},
 "ledger_row": {"unit": "u-0412", "seen": "2026-11-02", "decided": ["2026-11-05"], "unaided": ["2026-11-06"]},
 "log_row": {"t": "2026-11-07T10:12:03+09:00", "part": "p.LU.element", "machine": "m.LU.zhengge",
  "context": "expedition", "format": "type-in", "first_answer": "土", "correct": false, "partial": false,
  "hint_level": 0, "confidence": 3, "rt_ms": 4100, "interval_before": 8, "variant_label": null}}
```

- inspection.legit\_variant가 true면 이설이다. 정답은 出典 도장 둘이고, 邪 도장은 오답이다.
- format: type-in(독음 입력 후 한자 확정 = 회상) · point(銅人에서 가리키기 = 회상) · wheel(五行 바퀴 = 회상) · choice(선지 = 인식). 설치는 type-in·point·wheel만 인정한다.
- 로그는 추가만 한다. 삭제·수정 금지.

## 4. 핵심 알고리즘

모든 수치는 config.json의 값이고 4.10의 표가 초기값이다. 엔진은 날짜와 상태만 받아 결과를 돌려주는 순수 함수로 짜고, 화면은 그 결과를 그리기만 한다.

### 4.1 마모 — 시간이 부품을 닳는다

설치된 부품은 due = last\_unaided + interval\_days. 오늘이 due보다 worn\_window(interval의 20%, 최소 1일) 안에 들어오면 worn(깜빡임). due + fault\_grace\_days를 넘기면 fault(꺼짐). due + spread\_days를 넘기면 傳變: 그 부품의 이웃(流注 앞뒤 쌍, 表裏 經의 같은 역할 부품)이 installed였으면 worn으로 바뀜다. 傳變은 이웃을 꺼뜨리지 않고 깜빡이게만 한다. 한 부품은 하루 한 번만 傳變을 받는다.

정비: worn 부품을 무힌트로 맞히면 interval = min(interval × 2, interval\_max), last\_unaided = 오늘, installed. 틀리면 4.2로.

### 4.2 결함 — 오답이 부품을 꺼뜨린다

어느 맥락에서든 오답이 나오면 그 문항이 시험한 부품(dirs의 부품)을 fault로 표시한다. fault\_since = 지금. 기계 단위 답(사암 도출, 配穴)이 틀리면 부품 진단을 연다. 기계의 부품을 나열하고, 엔진이 오답에서 용의자를 추론한다(補할 곳에 土 대신 火를 놨으면 용의자는 p.sheng.earth-metal과 p.rule.zhengge). 사용자가 어느 부품이 틀렸는지 고른다. 고른 부품만 fault가 되고, 그 부품을 공유하는 다른 기계는 fault가 아니라 worn(점검 표시)이 된다. 상류는 건드리지 않는다. 흐름 기계에서 fault 부품은 정체 지점이고 그 하류는 어둡게 그리기만 한다. 하류 부품의 상태는 바뛌지 않는다.

### 4.3 수리 — 세 단계, 그리고 재가동 장면

1. 교정: 정답, 출전, variants를 보여 준다. 그 자리의 氣가 꺼지는 연출.
2. 재통과: 흐름이면 상류 세 穴 앞부터 다시 지목하며 지나와 고장 穴에서 다시 입력한다(상류는 설치된 구간이라 확인만, 빠르게). 도출이면 五行 바퀴에서 母·剋我부터 다시 조립한다.
3. 재인출: 같은 세션에서 다른 항목 reask\_after\_items개 뒤에 다시 묻는다. 이 성공은 hinted로 기록한다. 다른 날 무힌트 성공이 있어야 재설치되고, 그때 interval은 interval\_first부터 다시 시작한다.

재가동 장면: 2단계를 마치는 순간 상류에서 氣 입자가 고장 穴을 지나 사슬 끝까지 1.5초 동안 쏟아지고 단음 하나가 울린다. 이 장면은 생략할 수 없다. 고장이 벌이 아닌 이유가 이 장면이다.

### 4.4 설치 — 손에서 자동으로

manual 부품은 만날 때마다 묻는다(type-in·point·wheel 중 하나). 무힌트 성공이면 오늘 날짜를 unaided\_days에 넣는다. 서로 install\_gap\_hours 이상 떨어진 날이 install\_min\_days개가 되면 installed, interval = interval\_first × 2. 설치된 부품은 worn·fault·보스·巡察 이외에는 묻지 않는다. 이것이 해방이다.

### 4.5 흐름 — 어디까지 氣가 가는가

經 M의 order 부품을 순서대로 보며 첫 fault 또는 manual 부품의 위치를 찾는다. 氣는 시작 穴부터 그 직전까지 흐르고 나머지는 어둡다. worn 부품은 통과하되 그 구간에서 깜빡인다. route 부품(교접)이 설치되면 끝 穴에서 다음 經의 시작 穴로 氣가 이어진다. 五十營 지표 = 전체 order·route 부품 중 installed의 비율. 銅人의 밝기와 "오늘 n/50 바퀴"가 이 값에서 나온다.

### 4.6 스토리텔러 — 오늘의 계획

큐 넷. Q1 worn·fault(오늘 기한이거나 지남). Q2 최근 7일 안 오답 부품과 그 부품을 쓰는 기계의 다른 부품(선수개념). Q3 아직 안 물어본 manual 부품, 이번 달 經의 流注 순서대로. Q4 유지 확인, interval ≥ 30인 설치 부품 중 무작위 3%.

하루 예산 B = budget\_normal(피곤한 날 budget\_tired) 회상 행동. 몲은 Q1 50%, Q2 20%, Q3 20%(있으면 최소 3), Q4 10%. 어제 오답률 > 30%면 Q3 = 0, B × 0.7. 어제 오답률 < 10%이고 Q1이 작으면 Q3를 40%까지. 매일 같은 압력이 아니라 파도가 되게 한다.

배치: Q1 → 정비(직접 회상)와 환자(symptom·role 부품이면). Q2 → 같은 환자의 재방문(같은 id, 다른 단서). Q3 → 원정의 다음 manual 穴과 귀환 3택(세 부품 제시, 고른 것이 내일 Q3의 선두). Q4 → 巡察 환자 하루 1명 또는 검문 서류의 진짜 필드. 검문은 traps.json에서 하루 inspections\_per\_day건, 안 나온 함정 먼저, 다음은 표적 부품이 worn인 함정.

### 4.7 환자 생성과 채점

스토리텔러가 經 M과 부품 묶음을 정한다. truth = {meridian M, xushi 무작위, point = xushi에 맞는 사암 취혈 또는 role 부품의 穴}. 단서 1은 symptom 부품 문장, 보여 준다. 問診(氣 qi\_test)은 symptom 단서를 하나 더 연다(經을 좁힌다). 切診(氣 qi\_test)은 虛實을 연다. 세 칸(經·穴·虛實)이 다 채워져야 확정 버튼이 켜진다. 채점은 칸별. 經이 틀리면 보여 준 symptom 부품이 fault, 穴이 틀리면 그 穴을 받치는 role·assign 부품이 fault, 虛實은 부품 없이 로그만. 확정 후 치료: 五行 바퀴에 補·瀉를 놓고 穴을 고른다. deriver 기계의 output과 같으면 codex 이름을 부르고 코덱스에 남긴다. 환자 한 명 완치 = 氣 qi\_per\_cure.

氣는 회상을 막지 않는다. 氣 0에서도 정비·원정·환자는 할 수 있고, 검사와 3택 다시 뽑기만 못 한다. 희소성은 선택에만 걸리고 공부에는 걸리지 않는다.

### 4.8 검문 생성과 채점

traps.json의 함정 = {target\_part, true\_value, forged\_value, kind(hanja·number·direction·role·era)}. 서류 한 장 = 같은 經의 설치된 부품에서 진짜 필드 3\~5개 + 위조 필드 하나. 서류의 inspection\_true\_ratio는 위조 없음(늘 邪로 찍는 것을 막는다). inspection\_variant\_ratio는 이설 서류: 필드에 variants 중 하나가 들어 있고 정답은 出典 도장 둘. 도장은 셋: 正, 邪, 出典(교재/원전 선택). 틀리면 함정의 target\_part가 fault(설치된 경우) 또는 함정에 missed 표시(2일 뒤 재출제). PP처럼 가끔 규칙이 하나 늘어난다: 달이 바뀜 때 새 kind가 추가된다(처음은 hanja·role, 다음 달 number, 그다음 direction…).

### 4.9 白紙 보스 「五十營」 — 월말

이번 달 經에 대해 빈 종이: 流注 전체를 순서대로 type-in, 五輸 5, 原絡郄募背兪 5, 起止·교접, 是動·所生 문장. 힌트 없음, 음악 없음. 복원률 ≥ boss\_pass면 통과: 그 經에 연결된 奇經 구간이 지도에 나타나고 통혈 shortcut이 열린다. 실패하면 빠진 항목이 다음 달 Q1의 선두가 된다. 보스 기록은 context=boss로 따로 남긴다.

### 4.10 config.json 초기값

| key | 값 | 뜻 |
| --- | --- | --- |
| interval\_first | 1 | 첫 설치 간격(일), 재설치도 여기서 |
| interval\_mult | 2 | 정비 성공 시 배수 |
| interval\_max | 60 | 최대 간격(일) |
| worn\_window\_ratio | 0.2 | due 앞 깜빡임 구간(interval 비율, 최소 1일) |
| fault\_grace\_days | 1 | due 지나 꺼지기까지 |
| spread\_days | 4 | due 지나 傳變까지 |
| spread\_max\_per\_day | 1 | 한 부품이 하루에 받는 傳變 |
| install\_min\_days | 2 | 설치에 필요한 무힌트 성공 날짜 수 |
| install\_gap\_hours | 20 | 그 날짜들의 최소 간격 |
| reask\_after\_items | 3 | 오답 후 재인출까지 다른 항목 수 |
| budget\_normal / budget\_tired | 30 / 8 | 하루 회상 행동 예산 |
| quota\_q1..q4 | 0.5 / 0.2 / 0.2 / 0.1 | 큐 몲 |
| qi\_start / qi\_per\_cure / qi\_test / qi\_reroll | 10 / 3 / 1 / 2 | 氣 경제 |
| patients\_per\_day | 3\~6 | 스토리텔러가 정함 |
| inspections\_per\_day | 2\~3 |  |
| inspection\_true\_ratio / inspection\_variant\_ratio | 0.3 / 0.1 | 위조 없는 서류 / 이설 서류 비율 |
| boss\_pass | 0.95 | 白紙 통과 복원률 |
| restart\_scene\_ms | 1500 | 재가동 장면 길이 |

## 5. 화면·미감·소리·입력·저장

### 5.1 그래픽은 만들지 않는다

선, 점, 종이, 글꼴, 빛. 이 다섯으로 끝낸다. 외부 게임 에셋(D2R, ONI 등)은 쓰지 않는다. 세계가 둘이 되고, 에셋이 설계를 끌고 간다.

- 몸 윤곽 3뷰(전·후·측): 퍼블릭 도메인 銅人圖·明堂圖 스캔(Wikimedia Commons, Wellcome Collection)에서 윤곽만 따서 SVG path 하나씩. 스캔 자체를 배경으로 깔지 않는다(글씨와 격자가 세계를 어지럽힙다).
- 經脈: path, 穴: circle. 奇經은 점선 path.
- 종이: CC0 텍스처 한 장을 바탕에 깔거나 CSS 노이즈.
- 글꼴: Noto Serif KR 또는 Source Han Serif 하나. 크기는 두 가지(본문 16, 작은 글 12).
- 銅人: 같은 윤곽에 청동색 그라데이션. 등 = 穴 점이 금빛으로 켜짐.
- 醫家: 초상 없음. 명패 한 장(名·字·號·著書·시대).
- 화첩 카드: 유래 문장 + 먹점 하나(붓 원). 그림 없음.
- 아이콘 없음. 글자로 쓴다.

### 5.2 색 (CSS 변수, 이 여덟 밖의 색은 쓰지 않는다)

| 변수 | 값 | 쓰임 |
| --- | --- | --- |
| --paper | #EFE7D3 | 바탕 |
| --ink | #1E1B16 | 글자, 윤곽 |
| --ink-soft | #5A554B | 작은 글, 안개 속 표시 |
| --cinnabar | #B5362A | 經脈 선, 포커스 링, 도장 |
| --gold | #C9A227 | 설치된 穴, 銅人 등 |
| --qi | #F2C14E | 氣 입자 |
| --fog | #8A847A (35%) | 설치 안 된 穴·구간 |
| --bronze | #6B5A2A | 銅人 바탕 |

상태는 색이 아니라 빛의 움직임으로 보여 준다. 흐름 = 움직임, 마모 = 깜빡임, 고장 = 꺼짐과 하류의 회색.

### 5.3 레이아웃

화면은 하나다. 가운데 經絡圖(viewBox 1000×1600, 세로), 왼쪽 위 작은 銅人(항상), 오른쪽 의서 서랍(코덱스·穴典·책장·醫家, Y로 열고 닫음), 아래 한 줄(날짜 · 氣 · 오늘 n/50 · 현재 時의 經). 그 외 HUD 없음. 환자와 검문 창구는 醫館(지도 아래쪽 문)에서 같은 화면 위에 종이 한 장으로 뜨고, 모달 대화상자는 쓰지 않는다.

뷰 전환: 전·후·측(LB/RB). 층: 표층(皮部·經筋 색 구역) / 經脈 / 심층(經別·臟腑)(LT/RT). 안개: 설치 안 된 穴은 이름 없이 회색 점, 현재 穴에서 流注 다음 두 칸과 交會 한 칸만 흐릿하게 보인다.

### 5.4 氣의 빛 (qi.js)

- 입자는 path를 따라 일정 속도(config qi\_speed)로, 일정 간격으로 달린다.
- 설치 구간: 금빛 입자 흐름. worn 구간: 입자가 1 Hz로 흐려졌다 밝아진다. fault: 그 穴에서 입자 소멸, 하류 path는 회색. manual: 입자 없음, 먹선만.
- 재가동: restart\_scene\_ms 동안 상류에서 하류 끝까지 입자 밀도 3배로 쏟아지고 단음 하나.
- 子午流注: 실제 시각의 經 path를 아주 약하게 더 밝게.
- 프레임 30이면 충분하다.

### 5.5 소리

12經 암기송 = 그 經 지역에 있을 때 배경(작게, 끌 수 있게). 穴에 커서가 0.3초 머물면 낭독 재생. 효과음은 셋뿐: 설치(짧은 종), 고장(둘탁한 끊김), 재가동(상승 단음). 보스는 무음.

### 5.6 입력

| 패드(Switch Pro 표준 매핑) | 동작 |
| --- | --- |
| 왼스틱 | 커서. 經脈 위에서는 path를 따라 다음·이전 穴로 스냅 |
| A | 지목·확정 |
| B | 검사·취소 |
| X | 五行 바퀴 · 도장 |
| Y | 의서 서랍 |
| LB / RB | 전·후·측 뷰 |
| LT / RT | 표층 · 經脈 · 심층 |
| + / − | 오늘의 계획 · 피곤한 날 모드 |

한자 입력(type-in): 독음을 한글 자모 휠로 입력(초성→중성→종성, 스틱 8방향 + A) → 동음 후보 중 한자 확정. 독음까지가 회상, 후보 확정은 변별(禾髎/和髎). 키보드는 그냥 타이핑. 마우스·터치도 전부 동작. 포커스 링은 --cinnabar 1px. 마을판의 패드 등록·재지정 코드를 그대로 쓴다.

### 5.7 저장

localStorage 키 meridian-flow-v1: {day, qi, parts(3.2), physicians, codex, lamps, ledger, logs\[\], config\_override}. 행동마다 자동 저장. JSON 내보내기·가져오기. 로그는 추가만. 기존 시제품의 기록은 합치지 않는다(인수인계서 12절). 단, 저녁의 서재의 무힌트 성공 기록을 부품에 매핑해 가져오는 도구는 선택 사항으로 만들 수 있다.

## 6. 단계별 지시

한 대화에 한 단계. 각 단계는 그 자체로 실행되고 사용자가 20분 플레이한다. 기준을 통과하기 전에는 다음 단계를 시작하지 않는다.

### 1단계 — 經絡圖와 氣

- 목표: 보고만 있어도 좋은 화면. 세 상태(흐름·깜빡임·꺼짐)가 설명 없이 구별된다.
- 만드는 것: index.html, map.js(12正經 path + 361 circle + 奇經 점선, 3뷰 2층 토글, 안개 규칙), qi.js(입자 네 상태 + 재가동 장면), input.js 이식(스틱 스냅·A·LB/RB·LT/RT), meridians.json·points.json의 좌표(퍼블릭 도메인 스캔 트레이스), 종이·글꼴·색 토큰, 아래 상태 줄.
- 시연 데이터: 肺經 전체 installed, 大腸經 절반 manual, 胃經 한 곳 fault, 脾經 한 곳 worn. 네 상태가 한 화면에 보인다.
- 손밀기: manual 穴에서 A → type-in(이 단계는 키보드만) → 맞으면 입자가 한 칸 더 흐른다. 저장 없이 세션 안에서만.
- 기준: 30fps. 뷰 전환 0.2초 안. 1920×1080과 13인치 노트북에서 잘림 없음. 사용자 질문: "보고만 있어도 좋은가. 어디를 고쳐야 하는지 설명 없이 보이는가."
- 금지: 환자, 고장 로직, 醫家, 설정 화면, 소리(배경 한 곡은 허용).

### 2단계 — 부품·기계·고장·수리 (肺·大腸 두 經)

- 목표: 고장이 벌처럼 느껴지지 않고 고치고 싶어진다.
- 만드는 것: parts.json·machines.json(肺·大腸 전체 + 공유 부품: 相生 5·相剋 5·사암 규칙·原絡 규칙), parts.js·machines.js·srs.js·flow.js, 마모·결함·수리 3단계·설치·재가동, 부품 진단 화면, 저장(save.js), storyteller v0(Q1·Q3만), 開門 화면(오늘 할 일이 지도 위에만 보인다), 정비 행동.
- 테스트: UI 없이 30일 시뮬레이션(가상 사용자 정답률 70%)에서 상태 전이와 간격이 4절과 같다. 상류 불변·하류 어둠·傳變 하루 1회를 테스트로 고정한다.
- 기준: 肺經 11穴을 사흘에 걸쳐 설치하면 氣가 끝까지 흐른다. 고장 내면 그 자리만 꺼지고 수리 후 재가동 장면이 나온다. 肺正格을 틀리면 부품 진단이 열리고 고른 부품만 fault, 공유 기계는 worn. 사용자 질문: "고장이 벌처럼 느껴지지 않는가. 고치고 싶어지는가."
- 금지: 환자·검문·醫家. 나머지 10經 데이터는 아직.

### 3단계 — 환자·진단·五行 바퀴

- 목표: 어느 부품이 틀렸는지 짚게 된다.
- 만드는 것: symptoms.json(허브의 是動·所生·주치), patients.js, clinic.js(환자 한 명 = 종이 한 장), wheel.js(五行 바퀴 + 補瀉 배치 + 穴 선택), wuxing.js 이식, deriver output 대조와 codex 이름 호출, 出典 병기, 氣 경제, storyteller Q2(재방문).
- 기준: 환자 한 명 전 과정 90초 안. 세 칸 전에는 확정 불가. 틀린 칸이 맞는 부품을 fault로. 바퀴 조합이 正格과 같으면 이름이 불린다. 이설 둘 다 정답 테스트 통과. 사용자 질문: "어느 부품이 틀렸는지 짚게 되는가."
- 금지: 醫家 대사, 검문.

### 4단계 — 醫家·책장·화첩·검문

- 목표: 평평한 사실이 노가다로 느껴지지 않는다.
- 만드는 것: physicians.json(허브 발전사 탭의 인물 전원, 기능 하나씩, 대사 6종씩 — 각 대사에 著書·시대 사실 한 개), 영입 장면(字·號 소개 → recruit\_parts 회상), 책장(등표지 고르기 = 정비), 삐침(하루 기능 정지), 화첩(points.json 유래 → 카드, 빈 액자), 工房(카드 글 수정), traps.json(허브 변별·기출 함정 → 변장), booth.js(서류·도장 셋), 달마다 kind 추가.
- 기준: 하루 醫家 대사 ≤ 3줄. 검문 2\~3건 ≤ 2분. 이설 서류에 邪를 찍으면 오답. 사용자 질문: "평평한 사실이 노가다로 느껴지지 않는가."

### 5단계 — 銅人·시즌·白紙·奇經, 12經 전체

- 목표: 내일 켜고 싶고, 한 달 뒤가 기다려진다.
- 만드는 것: tongren.js(361 등, 설치 시 점등), 12달 시즌(달의 經, 월말 보스), 白紙 화면(type-in 연속, 무음), 통과 시 奇經 path·통혈 shortcut 개방, 12經 전체 parts·machines(+ 奇經 8, 交會穴, 表裏), 대장 완성(1,586 모두 매핑, 미매핑 목록을 보고), 歸館 3택, 피곤한 날 모드.
- 기준: 대장에서 decided가 0인 단위 수를 보고한다. 월말 보스 전 과정 15분 안. 사용자 질문: "내일 켜고 싶은가."

### 6단계 — 소리·패드·마감

- 만드는 것: audio.js(암기송 12·낭독·효과음 3), 패드 자모 휠, 실물 패드 검증 체크리스트, 성능, 내보내기·가져오기, 설정 최소(볼륨·피곤한 날·하루 시작 시각).
- 기준: 눈 감고 패드만으로 정비 한 바퀴가 가능하다. 사용자 질문: "눈 감고도 어디인지 아는가."

## 7. 산출물·검수 양식·금지 목록

### 매 단계 GPT가 내는 것

1. 실행 가능한 빌드(폴더 통째로, 시작하기.py로 열림).
2. 10줄 변경 요약.
3. "하지 않은 것" 목록. 기준에 있는데 안 한 것, 할 수 없어서 안 한 것을 나눠 적는다.
4. 대장 갱신본과 요약 한 줄: 단위 1,586 중 등장 n, 결정에 사용 n, 무힌트 n.
5. 화면 3장(시작 화면, 고장 난 상태, 수리 후).
6. node 테스트 결과. 테스트 통과는 "작동한다"의 증거이지 재미나 학습의 증거가 아니다. 그렇게 적지 않는다.

### 사용자의 20분 검수 양식 (단계마다 한 번, 이 다섯만)

| 묻는 것 | 답 |
| --- | --- |
| 어디서 시계를 봤나 |  |
| 무엇을 다시 하고 싶었나 |  |
| 설명 없이 알 수 있었던 것 / 없었던 것 |  |
| 공부가 됐다는 느낌이 든 순간 |  |
| 예쁘다고 느낀 순간 / 깨진 순간 |  |

이 다섯 답과 화면 한 장이 다음 단계의 입력이다. 단계의 사용자 질문에 "아니오"면 같은 단계를 다시 한다.

### 금지 목록

- 이 문서에 없는 다섯 번째 규칙 체계를 만드는 것.
- 모달 퀴즈 화면, 문 앞 퀴즈 관문, 점수·배지·레벨·연속 일수 표시.
- 같은 단어 매칭, 정답 → 공격력, 숫자만 오르는 보상.
- 상류를 멈추거나 진도를 회수하는 고장. 다른 부품의 상태를 오답 한 번으로 바꾸는 것(worn 표시는 허용, fault 전파는 금지).
- 노출·듣기·선지·힌트 후 정답을 무힌트 회상으로 기록하는 것.
- 사실 지어내기, 출전 없는 레코드, 교재·원전 중 한쪽을 정답으로 고르기, 원문에 없는 조합에 사암 이름 붙이기.
- 절차 생성 문항, 튜토리얼로 설명하기, 전부 보이는 지도.
- 외부 게임 에셋(D2R·ONI), 아이콘, 5.2 밖의 색, 그림 일러스트.
- 주민·운반·건설·피로 시뮬레이션, 자유 건축, 실시간 전투.
- 기존 시제품 기록을 자동으로 합치는 것.
- 작동 검사 통과를 재미·학습의 검증으로 적는 것.

관련 문서: [타이쿤·탐험 게임 100선 — 재미의 해부와 經絡 게임 적용](https://claude.ai/artifact/1q1mhtx5MmKkufZUPaVbS7) 6·7절, [正邪相爭 설계 한 장](https://claude.ai/artifact/NKUriNDLiCREunfZjqmwg3), 인수인계서 「경락과 포제 전체작업 설명서」(2026-11-07)와 learning\_science\_requirements.txt.
