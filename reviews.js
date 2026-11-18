/* v0.6 learner analytics and transparent interval-based spaced repetition.
   All timepoints are local ISO datetimes; algorithm is pedagogical, not exam validation. */
(function(){'use strict';
const DAYS=[1,3,7,14,30,60,120];
function review(old,score,total,date=new Date()){
 const prev=old&&typeof old==='object'?old:{};
 const success=total>0&&score/total>=.8;
 const streak=success?Math.max(0,Number(prev.streak)||0)+1:0;
 const interval=success?DAYS[Math.min(streak-1,DAYS.length-1)]:1;
 return {streak,interval,due:new Date(date.getTime()+interval*86400000).toISOString(),lastAt:date.toISOString(),lastScore:score,total,attempts:(Number(prev.attempts)||0)+1};
}
function due(state,date=new Date()){
 const v=state.reviews||{};return Object.entries(v).filter(([id,r])=>r&&Date.parse(r.due)<=date.getTime()).map(([id])=>id);
}
function stats(state,lessons,modules){
 const completed=new Set(state.lessonDone||[]), attempts=state.attemptHistory||[];
 const dueIds=due(state), hard=Object.entries(state.reviews||{}).filter(([,r])=>r&&(r.lastScore/(r.total||1)<.8)).map(([id])=>id);
 const average=attempts.length?Math.round(100*attempts.reduce((a,b)=>a+b.score/(b.total||1),0)/attempts.length):0;
 const years=[1,2,3,4].map(year=>{const l=lessons.filter(x=>modules.find(m=>m.id===x.moduleId)?.year===year);const done=l.filter(x=>completed.has(x.id));return {year,total:l.length,done:done.length,percent:l.length?Math.round(done.length*100/l.length):0}});
 const byDay={};for(const a of attempts){const d=(a.at||'').slice(0,10);if(d)byDay[d]=(byDay[d]||0)+1}
 return {completed:completed.size,total:lessons.length,dueIds,hard,attempts:attempts.length,average,years,byDay};
}
function merged(a,b){const newer=Date.parse(a?.updated||'')>=Date.parse(b?.updated||'')?a:b,older=newer===a?b:a;const r=JSON.parse(JSON.stringify(newer||{}));r.lessonDone=[...new Set([...(a?.lessonDone||[]),...(b?.lessonDone||[])])];r.normDone=[...new Set([...(a?.normDone||[]),...(b?.normDone||[])])];
 for(const key of ['quizAnswers','notes','audioIndex','audioTime','reviews','exerciseProgress','quizAttemptDone','normNotes','normQuiz','normStudyNotes'])r[key]={...(older?.[key]||{}),...(newer?.[key]||{})};
 const events=[...(a?.attemptHistory||[]),...(b?.attemptHistory||[])];r.attemptHistory=[...new Map(events.map(x=>[x.id||`${x.lessonId}-${x.at}-${x.score}`,x])).values()].sort((x,y)=>String(x.at).localeCompare(String(y.at))).slice(-2000);
 r.adaptiveResults=[...new Map([...(a?.adaptiveResults||[]),...(b?.adaptiveResults||[])].map(x=>[`${x.at}-${x.level}-${x.kind}-${x.correct}`,x])).values()].sort((x,y)=>String(x.at).localeCompare(String(y.at))).slice(-500);
 // v0.9: keep nested study-workshop data across optional cloud merges.
 const acNew=newer?.academy||{}, acOld=older?.academy||{};
 const ac={...acOld,...acNew};
 for(const key of ['competence','confidence','projectNotes','projectChecks','docs','safety','lessonBookmarks','audioPos']){
  ac[key]={...(acOld[key]||{}),...(acNew[key]||{})};
 }
 for(const key of ['portfolio','reports','exams']){
  const seen=new Set(),items=[];
  for(const item of [...(acOld[key]||[]),...(acNew[key]||[])]){
   const id=JSON.stringify(item);if(seen.has(id))continue;seen.add(id);items.push(item)
  }
  ac[key]=items.slice(key==='exams'?-40:-250);
 }
 // Active timed exam from newer side only; never combine two running attempts.
 ac.exam=acNew.exam||null;
 r.academy=ac;
 r.updated=new Date().toISOString();return r;
}
window.ElektroReviews={review,due,stats,merged};
})();
