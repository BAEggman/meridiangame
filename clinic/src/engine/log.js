export function log(s,kind,fields={}){s.log.push({t:s.now,day:s.day,kind,hours_left:s.hours,...fields});}
export function random(s){s.seed=(Math.imul(s.seed,1664525)+1013904223)>>>0;return s.seed/4294967296;}
export function pick(s,a){return a[Math.floor(random(s)*a.length)];}
