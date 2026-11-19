/* Elektro EFZ · Reusable masterclass engine for 178 sequentially approved lessons. Real, beat-aligned Thorsten-High audio.
 * Not a slideshow: visual state transitions are keyed to the exact start
 * of separately rendered narration beats (from PCM sample counts).
 * DC/AC movement represents conventional current direction schematically,
 * never literal electron trajectories or real-time 50 Hz behaviour.
 */
(()=>{'use strict';
const ROOT=document.querySelector('#mc-root');
if(!ROOT)return;
const audio=document.querySelector('#mc-audio');
const stage=document.querySelector('#mc-stage');
const ui={
 play:document.querySelector('#mc-play'),back:document.querySelector('#mc-back'),
 next:document.querySelector('#mc-next'),seek:document.querySelector('#mc-seek'),
 time:document.querySelector('#mc-clock'),duration:document.querySelector('#mc-duration'),
 speed:document.querySelector('#mc-speed'),status:document.querySelector('#mc-status'),
 captions:document.querySelector('#mc-captions'),captoggle:document.querySelector('#mc-captoggle'),
 caption:document.querySelector('#mc-caption'),
 chapters:document.querySelector('#mc-chapters'),fullscreen:document.querySelector('#mc-fullscreen'),
 answer:document.querySelector('#mc-answer'),support:document.querySelector('#mc-support')
};
let timeline=null,active=-1,lastTick=0,captionOn=false,answerPauseDone=false,ended=false;
const LESSON=document.body.dataset.masterLesson||'1.01-A';
const renderer=window.EFZ_MasterRenderers?.[LESSON];
if(!renderer||!renderer.groups||typeof renderer.render!=='function')
 throw Error('Fehlende Fachvisualisierungen für '+LESSON);
const groups=renderer.groups;
const artFor=renderer.render;
const esc=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt=x=>{x=Number.isFinite(x)?Math.max(0,Math.floor(x)):0;return Math.floor(x/60)+':'+String(x%60).padStart(2,'0')};
const mark=(label,sub)=>'<div class="mc-top"><div><span class="mc-lesson-mark">ELEKTRO · EFZ / MASTERCLASS</span><span class="mc-topic">'+esc(label)+'</span></div><span class="mc-stage-tag">'+esc(sub)+'</span></div>';
function beatAt(t){
 const beats=timeline?.beats||[];
 let low=0,high=beats.length-1;
 while(low<=high){
  const mid=(low+high)>>1;
  if(beats[mid].start<=t)low=mid+1;else high=mid-1;
 }
 return Math.max(0,Math.min(beats.length-1,high));
}
function redraw(index){
 if(!timeline)return;
 const beat=timeline.beats[index];if(!beat)return;
 const label=groups[beat.visual]||'OHMSCHES GESETZ';
 const first=mark(label,'SCHRITT '+String(index+1).padStart(2,'0')+' / '+timeline.beats.length);
 stage.innerHTML=first+artFor(beat.visual);
 active=index;
 ui.chapters.querySelectorAll('[data-cue]').forEach(n=>n.classList.toggle('selected',Number(n.dataset.cue)===index));
 if(captionOn)ui.caption.textContent=beat.narration;
 try{
  const element=stage.querySelector('svg');
  if(element&&typeof element.pauseAnimations==='function'){
   if(audio.paused)element.pauseAnimations();else element.unpauseAnimations();
  }
 }catch(_){}
}
function frame(){
 if(!timeline)return;
 const t=audio.currentTime||0;
 const idx=beatAt(t);
 if(idx!==active)redraw(idx);
 ui.seek.value=Math.round(1000*t/Math.max(1,audio.duration||timeline.duration_seconds));
 ui.time.textContent=fmt(t);
 ui.duration.textContent=fmt(audio.duration||timeline.duration_seconds);
 ui.play.textContent=audio.paused?'▶  Film fortsetzen':'Ⅱ  Pause';
 stage.classList.toggle('mc-playing',!audio.paused);
 if(!answerPauseDone){
  // When the last spoken question reaches its end, pause *before* the answer.
  // A larger pre-boundary guard is needed because Safari's timeupdate and MP3
  // seek positions can differ by 100-300 ms.
  const q=timeline.beats[timeline.beats.length-2];
  const a=timeline.beats[timeline.beats.length-1];
  if(q?.visual==='question' && t>=q.end-0.10 && t<a.start+0.6){
   answerPauseDone=true;
   audio.pause();
   // Seeked-over or buffered iOS audio is returned to the exact boundary.
   // Staying just before the first answer frame prevents accidental spoilers.
   if(audio.currentTime>q.end)audio.currentTime=q.end-0.07;
   ui.answer.hidden=false;
   ui.answer.textContent='Antwort anhören';
   redraw(timeline.beats.length-2);
   ui.status.textContent='Denke zuerst selbst nach. Die Antwort hörst du nach dem Fortsetzen.';
  }
 }
 try{
  const element=stage.querySelector('svg');
  if(element&&typeof element.pauseAnimations==='function'){
   if(audio.paused)element.pauseAnimations();else element.unpauseAnimations();
  }
 }catch(_){}
}
let frameHandle=null;
function loop(){
 frame();if(!audio.paused)frameHandle=requestAnimationFrame(loop);
}
function stopFrame(){if(frameHandle!==null)cancelAnimationFrame(frameHandle);frameHandle=null}
function seek(t){
 if(!timeline)return;
 audio.currentTime=Math.max(0,Math.min(t,(audio.duration||timeline.duration_seconds)-.12));
 frame(); 
}
function buildNav(){
 const beats=timeline.beats;
 const selected=[...new Set(beats.map((b,i)=>i).filter((i)=>i===0||i===beats.length-2||groups[beats[i].visual]!==groups[beats[i-1].visual]))];
 ui.chapters.innerHTML=selected.map(i=>{
  const b=beats[i];
  return '<button type="button" class="mc-nav-item" data-cue="'+i+'" aria-label="Direkt zu '+esc(groups[b.visual])+' springen">'+
  '<span>'+fmt(b.start)+'</span>'+esc(groups[b.visual])+'</button>';
 }).join('');
 ui.chapters.querySelectorAll('[data-cue]').forEach(b=>b.addEventListener('click',()=>{
  seek(beats[Number(b.dataset.cue)].start+.02);ui.chapters.closest('details')?.removeAttribute('open');
 }));
}
function start(){
 if(!timeline){ui.status.textContent='Audio- und Zeitdaten laden …';return}
 if(audio.paused)audio.play().catch(err=>{ui.status.textContent='Audio konnte nicht gestartet werden: '+err.message;});
 else audio.pause();
}
ui.play.addEventListener('click',start);
ui.back.addEventListener('click',()=>{
 if(!timeline)return;seek(timeline.beats[Math.max(0,beatAt(audio.currentTime)-1)].start+.02);
});
ui.next.addEventListener('click',()=>{
 if(!timeline)return;seek(timeline.beats[Math.min(timeline.beats.length-1,beatAt(audio.currentTime)+1)].start+.02);
});
ui.seek.addEventListener('input',()=>{if(timeline)seek(Number(ui.seek.value)/1000*(audio.duration||timeline.duration_seconds))});
ui.speed.addEventListener('change',()=>{audio.playbackRate=Number(ui.speed.value)||1});
ui.captoggle.addEventListener('click',()=>{
 captionOn=!captionOn;ui.captions.hidden=!captionOn;
 ui.captoggle.setAttribute('aria-pressed',String(captionOn));
 if(captionOn&&timeline)ui.caption.textContent=timeline.beats[beatAt(audio.currentTime)].narration;
});
ui.fullscreen.addEventListener('click',()=>{
 if(ROOT.requestFullscreen)ROOT.requestFullscreen().catch(()=>ROOT.classList.toggle('mc-pseudo-fullscreen'));
 else ROOT.classList.toggle('mc-pseudo-fullscreen');
});
ui.answer.addEventListener('click',()=>{
 ui.answer.hidden=true;ui.status.textContent='';
 const answer=timeline.beats[timeline.beats.length-1];
 seek(answer.start+.02);
 audio.play().catch(e=>{ui.status.textContent=e.message});
});
audio.addEventListener('play',()=>{ui.play.textContent='Ⅱ  Pause';stopFrame();loop()});
audio.addEventListener('pause',()=>{stopFrame();frame()});
audio.addEventListener('timeupdate',frame);
audio.addEventListener('seeking',()=>{
 // Keep the "answer" button visible when the player itself rewinds 70ms
 // to the end of the question. Only user-initiated jumps hide it.
 if(answerPauseDone && timeline){
  const holdAt=timeline.beats[timeline.beats.length-2].end-.07;
  if(Math.abs(audio.currentTime-holdAt)>.15)ui.answer.hidden=true;
 }
 frame();
});
audio.addEventListener('ended',()=>{stopFrame();ui.status.textContent='Sequenz abgeschlossen. Die vollständige Lektion bleibt separat verfügbar.';frame()});
audio.addEventListener('error',()=>{
 ui.status.textContent='Audio konnte nicht geladen werden. Prüfe die Internetverbindung oder lade die Seite erneut.';
 ui.support.hidden=false;
});
audio.addEventListener('loadedmetadata',()=>{
 if(timeline && Math.abs(audio.duration-timeline.duration_seconds)>0.4)
  ui.status.textContent='Hinweis: Zeitdaten passen nicht genau zum Audio.';
 else ui.status.textContent='';
 frame();
});
document.addEventListener('keydown',e=>{
 if(e.target?.tagName==='INPUT'||e.target?.tagName==='SELECT'||e.target?.tagName==='BUTTON')return;
 if(e.code==='Space'){e.preventDefault();start();}
});
(async()=>{
 try{
  const response=await fetch('./masterclasses/'+encodeURIComponent(LESSON)+'/audio/timeline.json',{cache:'no-store'});
  if(!response.ok)throw Error('Zeitdaten HTTP '+response.status);
  const t=await response.json();
  if(t.lesson_id!==LESSON+'-master'||t.beats.length<15||t.beats.length>50)throw Error('Unpassende Szenendaten');
  if(!t.beats.every((b,i)=>i===0?b.start===0:b.start>=t.beats[i-1].end-.005))
   throw Error('Zeitdaten nicht aufsteigend');
  timeline=t;
  buildNav();redraw(0);
  ui.play.disabled=false;ui.back.disabled=false;ui.next.disabled=false;ui.seek.disabled=false;
  ui.status.textContent='Bereit · Jede Bildsequenz beginnt mit dem entsprechenden Sprecher-Audiobaustein.';
  audio.load();
 }catch(e){
  ui.status.textContent='Pilot konnte nicht vollständig geladen werden: '+e.message;
  ui.support.hidden=false;
 }
})();
window.ElektroMaster=Object.freeze({getTimeline:()=>timeline, getActiveBeat:()=>active,artFor, lesson:LESSON});
})();