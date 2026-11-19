/* Elektro EFZ · Masterclass 1.03-B. Real, sample-aligned Thorsten-High audio.
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
const names={
 intro:'DER STROMKREIS',calc:'DAS OHMSCHE GESETZ',compare:'WIDERSTAND VERÄNDERN',
 direction:'STROMRICHTUNG',check:'LERNKONTROLLE'
};
const S={cyan:'#8de5d8',mint:'#72ecc0',white:'#edf8fb',light:'#b9d4e4',muted:'#6f94ab',dark:'#0b2235',blue:'#7bbefa',yellow:'#e8cb8a'};
const esc=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const txt=(x,y,s,size=30,color=S.white,weight=600,anchor='middle')=>'<text x="'+x+'" y="'+y+'" fill="'+color+'" font-size="'+size+'" font-family="Inter,-apple-system,BlinkMacSystemFont,Arial,sans-serif" font-weight="'+weight+'" text-anchor="'+anchor+'">'+esc(s)+'</text>';
const box=(x,y,w,h,fill='#12364b',stroke='#3c667d',radius=14)=>'<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="'+radius+'" fill="'+fill+'" stroke="'+stroke+'" stroke-width="1.6"/>';
const fmt=x=>{x=Number.isFinite(x)?Math.max(0,Math.floor(x)):0;return Math.floor(x/60)+':'+String(x%60).padStart(2,'0')};
const mark=(label,sub)=>'<div class="mc-top"><div><span class="mc-lesson-mark">ELEKTRO · EFZ / MASTERCLASS</span><span class="mc-topic">'+esc(label)+'</span></div><span class="mc-stage-tag">'+esc(sub)+'</span></div>';
const svg=art=>'<svg class="mc-illustration" viewBox="0 0 960 540" role="img" aria-label="Schematisches Lehrbild zur elektrischen Stromstärke">'+
 '<defs><marker id="mc-arr" markerWidth="12" markerHeight="12" refX="9" refY="6" orient="auto"><path d="M1 1 L10 6 L1 11" stroke="#72ecc0" stroke-width="2" fill="none"/></marker>'+
 '<linearGradient id="mc-wire"><stop offset="0%" stop-color="#5fa7bf"/><stop offset="100%" stop-color="#80d7ce"/></linearGradient></defs>'+art+'</svg>';
function moving(path,n=7,duration=6){
 let p='';
 for(let i=0;i<n;i++)p+='<circle class="mc-carrier" r="6.5" fill="'+(i%2?S.mint:S.cyan)+'" opacity=".92">'+
 '<animateMotion dur="'+duration+'s" begin="-'+(i*duration/n).toFixed(2)+'s" repeatCount="indefinite" path="'+path+'"/></circle>';
 return p;
}
function circuit(visual){
 const isOpen=visual==='open'||visual==='start'||visual==='source';
 const isFlow=!isOpen&&['close','flow','resistor','valueU','valueR','result','testR','doubleR','halfR','restore','dc'].includes(visual);
 const R=visual==='doubleR'?'240 Ω':visual==='halfR'?'60 Ω':'120 Ω';
 const I=visual==='doubleR'?'50 mA':visual==='halfR'?'200 mA':'100 mA';
 const valueShown=!['start','open','close'].includes(visual);
 const partial=visual==='source'||visual==='start';
 const signal='M205 215 V124 H768 V410 H205 V310';
 let g='';
 // Circuit: external conventional direction + -> resistor -> -, no bypass.
 g+='<path d="M205 215 V124 H627" fill="none" stroke="url(#mc-wire)" stroke-width="7" stroke-linecap="round"/>';
 g+='<path d="M757 124 H768 V410 H205 V310" fill="none" stroke="url(#mc-wire)" stroke-width="7" stroke-linecap="round"/>';
 if(isOpen){g+='<path d="M627 124 L644 75" stroke="#f0bf83" stroke-width="6" stroke-linecap="round"/>'+txt(689,70,'Schalter offen',17,S.yellow); }
 else {g+='<path d="M627 124 H647" stroke="url(#mc-wire)" stroke-width="7"/>';}
 g+=box(647,96,110,56,'#163b50','#b6e7ed',8)+txt(702,132,'R',30,S.white,700);
 // Correct voltage-source symbol, wires end at plates.
 g+='<path d="M169 216 H241 M180 306 H230" stroke="#eef7f9" stroke-width="7" stroke-linecap="round"/>';
 g+=txt(148,225,'+',31,S.mint)+txt(148,317,'−',31,S.blue);
 if(!partial){
  g+=box(65,337,275,84,'#102f44',visual==='valueU'?'#6af3c0':'#355e78',14);
  g+=txt(201,370,'SPANNUNGSQUELLE',16,S.light,700);
  g+=txt(201,405,'U = 12 V',32,S.white,750);
 }
 if(partial){
  g+=box(69,337,267,83,'#123f4e','#66c5bc',14);
  g+=txt(201,371,'GLEICHSPANNUNG',17,S.light);
  g+=txt(201,405,'12 V',34,S.white,760);
 }
 if(valueShown){
  g+=box(602,170,232,71,'#133448',visual==='valueR'?'#73e8d0':'#3c677d',14);
  g+=txt(718,196,'WIDERSTAND',15,S.light,680);
  g+=txt(718,225,R,31,S.white,760);
 }
 if(isFlow){
  g+=moving(signal,8,5.8);
  g+='<path d="M340 86 H485" stroke="'+S.mint+'" stroke-width="4" marker-end="url(#mc-arr)"/>';
  g+=txt(413,67,'Technische Stromrichtung',18,S.mint);
 }
 if(['result','doubleR','halfR','restore','dc'].includes(visual)){
  g+=box(356,323,244,99,'#125267','#81e9d4',16);
  g+=txt(480,359,'STROMSTÄRKE',17,S.light,700);
  g+=txt(480,399,'I = '+I,34,S.white,800);
 }
 if(visual==='testR'){
  g+=box(356,323,260,99,'#473d30','#e5ca9f',16);
  g+=txt(486,359,'WAS PASSIERT?',19,S.yellow,750);
  g+=txt(486,396,'R × 2 → I = ?',27,S.white,750);
 }
 if(visual==='flow')g+=txt(484,484,'Technische Richtung – keine Teilchenbahnen',18,S.light);
 if(visual==='resistor')g+=txt(483,484,'Höherer Widerstand → bei gleicher Spannung weniger Strom',18,S.light);
 return svg(g);
}
function formula(visual){
 const rows={
 relation:['U = R × I','Spannung · Widerstand · Strom'],
 formula:['I = U / R','Gesucht ist die Stromstärke I'],
 valueU:['I = 12 V / R','12 Volt aus der Spannungsquelle'],
 valueR:['I = 12 V / 120 Ω','120 Ohm direkt vom Widerstand'],
 substitution:['12 / 120 = 0,1','Zahlenwert berechnen'],
 units:['I = 0,1 A','Volt durch Ohm ergibt Ampere'],
 milli:['0,1 A = 100 mA','Einheit in Milliampere umrechnen'],
 recap:['I = U / R','Mehr Widerstand → weniger Strom']
 };
 const [main,description]=rows[visual]||rows.formula;
 const parts=main.split(' = ');
 let g='';
 g+=txt(480,128,visual==='relation'?'DER ZUSAMMENHANG':'SCHRITT FÜR SCHRITT',21,S.mint,730);
 g+=box(120,167,720,161,'#12364c','#3c697b',23);
 g+=txt(480,261,main,visual==='valueR'?58:65,S.white,750);
 g+=txt(480,377,description,24,S.light,500);
 if(['valueR','substitution','units','milli'].includes(visual)){
  g+='<path d="M330 421 H630" stroke="'+S.mint+'" stroke-width="4" stroke-linecap="round"/>';
  g+=txt(480,464,'12 V   ÷   120 Ω',23,S.mint);
 }
 return svg(g);
}
function direction(visual){
 if(visual==='dc')return circuit('dc');
 const ac=visual==='ac'||visual==='acdetail';
 let g='';
 g+=txt(480,101,'GLEICHSTROM UND WECHSELSTROM',28,S.white,740);
 g+=box(53,149,412,267,'#102e43','#305e77',19)+box(495,149,412,267,'#102e43','#305e77',19);
 g+=txt(257,205,'DC',40,S.mint,790)+txt(702,205,'AC',40,S.blue,790);
 g+='<path d="M112 293 H404 M554 293 H845" stroke="#76a2b8" stroke-width="8" stroke-linecap="round"/>';
 g+=moving('M118 293 H396',5,3.4);
 // AC: separate reversing arrows and a charge carrier visibly moving back and forth.
 g+='<path class="mc-ac-forth" d="M583 249 H821" stroke="'+S.blue+'" stroke-width="5" marker-end="url(#mc-arr)"/>';
 g+='<path class="mc-ac-back" d="M819 249 H581" stroke="'+S.blue+'" stroke-width="5" marker-end="url(#mc-arr)"/>';
 g+='<circle r="9" fill="#9dd1ff"><animateMotion dur="4s" repeatCount="indefinite" path="M582 293 H817 H582"/></circle>';
 g+=txt(257,369,'Richtung konstant',20,S.light)+txt(702,369,'Richtung wechselt',20,S.light);
 g+=txt(480,465,'Schematisch · Zeitlupe · keine Elektronenbahnen',17,S.muted);
 return svg(g);
}
function quiz(visual){
 const isAnswer=visual==='answer';
 let g=txt(480,120,'KURZE LERNKONTROLLE',24,S.mint,730);
 g+=box(130,157,700,212,'#133a50','#4a8a96',23);
 g+=txt(480,223,'12 V   ·   240 Ω',48,S.white,750);
 g+=txt(480,294,isAnswer?'I = 50 mA':'Wie gross ist die Stromstärke?',isAnswer?49:31,isAnswer?S.mint:S.light,750);
 if(isAnswer)g+=txt(480,409,'Verdoppelter Widerstand → halbierter Strom',23,S.light);
 else g+=txt(480,414,'Kurz überlegen, dann Antwort anzeigen',22,S.yellow);
 return svg(g);
}
function artFor(visual){
 if(['relation','formula','valueU','valueR','substitution','units','milli','recap'].includes(visual))return formula(visual);
 if(['ac','acdetail'].includes(visual))return direction(visual);
 if(['question','answer'].includes(visual))return quiz(visual);
 return circuit(visual);
}
const groups={
 start:'EINSTIEG',source:'EINSTIEG',open:'EINSTIEG',close:'STROMFLUSS',flow:'STROMFLUSS',
 resistor:'WIDERSTAND',relation:'OHMSCHES GESETZ',formula:'OHMSCHES GESETZ',
 valueU:'BERECHNUNG',valueR:'BERECHNUNG',substitution:'BERECHNUNG',
 units:'ERGEBNIS',milli:'ERGEBNIS',result:'ERGEBNIS',
 testR:'PLAUSIBILITÄT',doubleR:'PLAUSIBILITÄT',halfR:'PLAUSIBILITÄT',restore:'PLAUSIBILITÄT',
 dc:'STROMRICHTUNG',ac:'STROMRICHTUNG',acdetail:'STROMRICHTUNG',
 recap:'ZUSAMMENFASSUNG',question:'LERNKONTROLLE',answer:'LERNKONTROLLE'
};
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
 const selected=[0,3,6,8,11,14,18,21,22];
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
audio.addEventListener('seeking',()=>{if(answerPauseDone)ui.answer.hidden=true;frame()});
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
  const response=await fetch('./master-103-b/audio/timeline.json',{cache:'no-store'});
  if(!response.ok)throw Error('Zeitdaten HTTP '+response.status);
  const t=await response.json();
  if(t.lesson_id!=='1.03-B-master'||t.beats.length!==24)throw Error('Unpassende Szenendaten');
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
window.ElektroMaster=Object.freeze({getTimeline:()=>timeline, getActiveBeat:()=>active,artFor});
})();