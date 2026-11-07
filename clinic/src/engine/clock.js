export const DAY=86400000;
export function dateKey(t){const d=new Date(t);return [d.getFullYear(),String(d.getMonth()+1).padStart(2,'0'),String(d.getDate()).padStart(2,'0')].join('-');}
export function separated(a,b,c){return dateKey(a)!==dateKey(b)&&b-a>=c.install_gap_hours*3600000;}
export function charge(s,n){if(!Number.isFinite(n)||n<0||s.closed||s.hours<n)throw Error('남은 時辰이 부족합니다.');s.hours-=n;}
export function makeState(data,c,now=Date.now(),debug=false,seed=Date.now()>>>0){return {schema:21,debug,now,day:dateKey(now),opened:null,closed:false,hours:c.hours_per_day,prevRegion:'hand',seed,seq:0,patients:[],blueprints:[],parts:Object.fromEntries(data.points.map(p=>['position.'+p.id,{exposed:null,passes:[],installed:false,due:null,interval:c.interval_first,fault:false,correctedAt:null,after:[],aided:0}])),ledger:{seen:0,unaided:0,aided:0,seen_by_physicians:0,leaves:0},doctor:{hours:0,region:'hand'},log:[]};}
