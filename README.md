# 醫館 — 經絡 학습 게임 (v2 · 1단계)

환자가 오고, 나는 길을 고르고, 좋은 계획은 청사진이 되어 내 대신 병동을 돌린다.

肺·大腸 수직 절편입니다. 原絡·兪募·사암 正格/勝格 8길, 40혈. 성공한 계획은 청사진으로 남고, 다른 날 무힌트로 두 번 맞히면 士安(皇甫謐)이 開門 때 대신 봅니다. 틀린 혈은 그 혈을 쓰는 청사진만 멈춥니다.

## 실행

- GitHub Pages: 저장소 루트 `index.html`이 `clinic/`으로 넘깁니다.
- 로컬: `python3 serve.py --open` (설치 없음) 또는 `clinic/index.html`을 로컬 서버로.
- 검사: `node --test clinic/tests/*.test.mjs` (16개)
- 단일 파일판 만들기: `python3 tools/package-clinic.py` → `../output/醫館_v2_실행.html`

## 조작

| 입력 | 동작 |
| --- | --- |
| 마우스 | 몸 클릭 = 지정, 휠 = 확대, 드래그 = 이동 |
| 키보드 | 방향키/WASD 커서, Enter 지정, Esc 취소, B 의서, N 청사진 책, Q/E 환자, [ ] 확대, Space 閉門, Tab 정원, 1·2·3 보기, 4 表/深 |
| Switch Pro Controller | 좌 스틱: 銅人의 혈 구멍(이름 없음) 사이를 건너뛰며 고르기 · A 지정/누름 · B 취소 · 십자키 판 이동 · X 의서 · Y 청사진 책 · L/R 환자 · ZL/ZR 확대 · 좌 스틱 누름 부위 전환(전체·손팔·몸통·다리발) · + 길게 閉門 · − 정원 · 우 스틱 보기 전환. 배치가 다르면 화면 아래 🎮 패드 설정 |

## 구조

- `clinic/data/` 사실(출전 포함) · `clinic/config.json` 게임 수치(임상값 아님)
- `clinic/src/engine/` 시계·생성기·채점·판정·청사진·傳變·스토리텔러·로그
- `clinic/src/ui/` 몸 도식(body.js)·패드(pad.js) · `clinic/src/app.js` 화면
- `clinic/guide/` 검수 장부 · `docs/` 지시서 수신본과 변경 기록 · `질문.md` 충돌과 근거 공백

교재 추출본·KMCRIC/WHO 원문 사본(`reference/`)과 이전 판(`stage1/`, `stage15/`)은 저작권·용량 때문에 저장소에 넣지 않았습니다. `tools/build-clinic-data.py`는 그 폴더가 있어야 돌아갑니다.

## 기록

브라우저 localStorage `meridian.clinic.v2.real` / `.debug` / `.pad`. 기기 간 동기화는 없습니다. 「기록 내보내기」로 JSON 보관.
