// 패드 입력 · Nintendo Switch Pro Controller / Joy-Con (Gamepad API)
// 좌 스틱: 몸 위 커서 · 십자키: 판의 버튼 포커스 · A: 지정 / 누름 · B: 취소 / 덮기
// X: 의서 · Y: 청사진 책 · L/R: 환자 · ZL/ZR: 축소/확대 · +(길게): 閉門 · −: 정원 · 우 스틱: 보기 전환
const STANDARD={A:1,B:0,X:3,Y:2,L:4,R:5,ZL:6,ZR:7,MINUS:8,PLUS:9,LS:10,RS:11,UP:12,DOWN:13,LEFT:14,RIGHT:15};
const NAMES=['A','B','X','Y','L','R','ZL','ZR','MINUS','PLUS','UP','DOWN','LEFT','RIGHT'];
const LABEL={A:'A',B:'B',X:'X',Y:'Y',L:'L',R:'R',ZL:'ZL',ZR:'ZR',MINUS:'−',PLUS:'+',UP:'십자 ↑',DOWN:'십자 ↓',LEFT:'십자 ←',RIGHT:'십자 →'};
const HINT='A 지정·누름 · B 취소 · X 의서 · Y 청사진 책 · L/R 환자 · ZL/ZR 확대 · + 길게 閉門 · − 정원 · 좌스틱 커서 · 십자키 판 · 우스틱 보기';
export function installPad(api,{storageKey='meridian.clinic.v2.pad',deadzone=.22,speed=.022,holdMs=600,repeatDelay=380,repeatEvery=95}={}){
 let map={...STANDARD};
 try{const saved=JSON.parse(localStorage.getItem(storageKey)||'null');if(saved&&typeof saved==='object')map={...map,...saved};}catch{}
 const st={zone:'body',focus:null,prev:[],held:{},repeat:{},plusAt:null,connected:false,hintTimer:null,remap:null,rs:{x:0,y:0},lastMove:0};
 const hint=document.createElement('div');hint.id='padHint';hint.hidden=true;document.body.append(hint);
 const showHint=(text=HINT,ms=9000)=>{hint.textContent='🎮 '+text;hint.hidden=false;clearTimeout(st.hintTimer);if(ms)st.hintTimer=setTimeout(()=>{hint.hidden=true;},ms);};
 const pad=()=>{const list=navigator.getGamepads?navigator.getGamepads():[];for(const g of list)if(g&&g.connected!==false)return g;return null;};
 // ---- 판 포커스 (기하 탐색) ----
 const visible=el=>{if(el.disabled||el.hidden||el.closest('[hidden]'))return false;const r=el.getBoundingClientRect();return r.width>0&&r.height>0;};
 const candidates=()=>{const sheet=document.getElementById('sheet');const root=sheet?.open?sheet:document;const sel=sheet?.open?'button,input':'header nav button, main button, #garden button, .global-footer button';return[...root.querySelectorAll(sel)].filter(visible);};
 const center=el=>{const r=el.getBoundingClientRect();return{x:r.left+r.width/2,y:r.top+r.height/2,r};};
 function setFocus(el){if(st.focus&&st.focus!==el)st.focus.classList.remove('pad-focus');st.focus=el||null;if(el){el.classList.add('pad-focus');el.scrollIntoView({block:'nearest',inline:'nearest'});}}
 function ensureFocus(){const list=candidates();if(!list.length){setFocus(null);return null;}if(!st.focus||!list.includes(st.focus)||!visible(st.focus)){const same=st.focusText&&list.find(b=>b.textContent.trim()===st.focusText);setFocus(same||list.find(b=>b.closest('#plan'))||list[0]);}return st.focus;}
 function moveFocus(dir){const list=candidates();const cur=ensureFocus();if(!cur)return;const c=center(cur);let best=null,bestScore=Infinity;for(const el of list){if(el===cur)continue;const o=center(el);const dx=o.x-c.x,dy=o.y-c.y;let along,across;if(dir==='UP'){along=-dy;across=Math.abs(dx);}else if(dir==='DOWN'){along=dy;across=Math.abs(dx);}else if(dir==='LEFT'){along=-dx;across=Math.abs(dy);}else{along=dx;across=Math.abs(dy);}if(along<8)continue;const score=along+across*2.2;if(score<bestScore){bestScore=score;best=el;}}if(best){setFocus(best);st.focusText=best.textContent.trim();}}
 const NEXT=[['시술',['성공한 계획을 청사진으로','교정 뒤 다시 지정']],['교정 뒤 다시 지정',['시술']]];
 function press(){const el=ensureFocus();if(!el)return;if(el.tagName==='INPUT'){api.notify('이름은 키보드로만 바꿀 수 있습니다.');return;}const text=el.textContent.trim();st.focusText=text;el.click();const hint=NEXT.find(([k])=>text.startsWith(k));if(hint){const list=candidates();const next=hint[1].map(h=>list.find(b=>b.textContent.trim().startsWith(h))).find(Boolean);if(next){setFocus(next);st.focusText=next.textContent.trim();}}}
 // ---- 버튼 읽기 ----
 const down=(g,name)=>{const i=map[name];const b=g.buttons[i];return !!b&&(b.pressed||b.value>.5);};
 function edges(g){const now=performance.now(),out=[];for(const n of NAMES){const d=down(g,n);const was=!!st.held[n];if(d&&!was){st.held[n]=now;st.repeat[n]=now+repeatDelay;out.push(n);}else if(d&&was&&['UP','DOWN','LEFT','RIGHT'].includes(n)&&now>=st.repeat[n]){st.repeat[n]=now+repeatEvery;out.push(n);}else if(!d&&was){delete st.held[n];if(n==='PLUS')st.plusAt=null;}}return out;}
 // ---- 리맵 ----
 function startRemap(){st.remap={i:0,result:{}};showHint('패드 설정 · '+LABEL[NAMES[0]]+' 버튼을 누르세요',0);}
 function remapStep(g){const i=st.remap.i;const pressedIdx=g.buttons.findIndex(b=>b.pressed||b.value>.5);if(pressedIdx<0){st.remap.waitRelease=false;return;}if(st.remap.waitRelease)return;st.remap.result[NAMES[i]]=pressedIdx;st.remap.waitRelease=true;st.remap.i++;if(st.remap.i>=NAMES.length){map={...map,...st.remap.result};try{localStorage.setItem(storageKey,JSON.stringify(st.remap.result));}catch{}st.remap=null;showHint('패드 설정 저장 · '+HINT);return;}showHint('패드 설정 · '+LABEL[NAMES[st.remap.i]]+' 버튼을 누르세요',0);}
 // ---- 프레임 ----
 function frame(){const g=pad();if(g){if(!st.connected){st.connected=true;showHint(HINT);api.notify('컨트롤러 연결 · '+(g.id||'').replace(/\(.*\)/,'').trim());}
  if(st.remap){remapStep(g);}else{
   const sheetOpen=api.sheetOpen();
   // 좌 스틱 → 몸 커서
   const ax=g.axes[0]||0,ay=g.axes[1]||0,mag=Math.hypot(ax,ay);
   if(mag>deadzone&&!sheetOpen&&!api.gardenOpen()){const k=((mag-deadzone)/(1-deadzone))**2*speed;api.moveCursor(ax/mag*k*mag,ay/mag*k*mag);st.zone='body';if(st.focus)st.focus.classList.remove('pad-focus');}
   // 우 스틱 → 보기 전환 (가장자리 넘김 때 한 번)
   const rx=g.axes[2]||0,ry=g.axes[3]||0;
   if(Math.abs(rx)>.6&&Math.abs(st.rs.x)<=.6&&!sheetOpen)api.cycleView(rx>0?1:-1);
   if(Math.abs(ry)>.6&&Math.abs(st.rs.y)<=.6&&!sheetOpen)api.toggleLayer();
   st.rs={x:rx,y:ry};
   for(const n of edges(g)){
    if(sheetOpen){if(n==='B'||n==='X'||n==='Y')api.closeSheet();else if(n==='A')press();else if(['UP','DOWN','LEFT','RIGHT'].includes(n))moveFocus(n);continue;}
    if(api.gardenOpen()){if(n==='A'||n==='B'||n==='MINUS')api.toggleGarden();continue;}
    switch(n){
     case 'UP':case 'DOWN':case 'LEFT':case 'RIGHT':if(st.zone!=='panel'){st.zone='panel';ensureFocus();}else moveFocus(n);break;
     case 'A':if(st.zone==='body'){const done=api.designate();if(done==='complete'){st.zone='panel';st.focusText='시술';setFocus(null);ensureFocus();const b=candidates().find(x=>x.textContent.trim().startsWith('시술'));if(b)setFocus(b);}}else press();break;
     case 'B':if(st.zone==='body')api.undo();else{st.zone='body';if(st.focus)st.focus.classList.remove('pad-focus');}break;
     case 'X':api.openBook();break;
     case 'Y':api.openBlueprints();break;
     case 'L':api.nextPatient(-1);break;
     case 'R':api.nextPatient(1);break;
     case 'ZL':api.zoom(1.4);break;
     case 'ZR':api.zoom(.7);break;
     case 'MINUS':api.toggleGarden();break;
     case 'PLUS':st.plusAt=performance.now();showHint('+ 를 계속 누르면 閉門',0);break;
    }
   }
   if(st.plusAt&&down(g,'PLUS')){const t=performance.now()-st.plusAt;const n=Math.min(12,Math.round(t/holdMs*12));hint.textContent='🎮 閉門 '+'■'.repeat(n)+'□'.repeat(12-n);if(t>=holdMs){st.plusAt=null;hint.hidden=true;api.closeDay();}}
   else if(!st.plusAt&&hint.textContent.startsWith('🎮 + 를')){hint.hidden=true;}
   if(st.zone==='panel'&&!sheetOpen&&!api.gardenOpen())ensureFocus();
  }}
  else if(st.connected){st.connected=false;api.notify('컨트롤러 끊김');}
  requestAnimationFrame(frame);}
 window.addEventListener('gamepadconnected',()=>{});
 requestAnimationFrame(frame);
 return{remap:startRemap,hint:()=>showHint(HINT),map:()=>({...map})};
}
