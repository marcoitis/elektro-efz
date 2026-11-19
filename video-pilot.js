/* Elektro EFZ – videogleiche Pilotlektion 1.03-B.
 * Originales Thorsten-High-Audio aus ElektroAudio, nicht synthetisierte Folienstimme.
 * Zeitmarken entsprechen den Wortpositionen im veröffentlichten Sprechertext.
 * Kapitelgenaue Annäherung; kein behauptetes Wort-für-Wort-Forced-Alignment.
 * 100% lokale SVG/CSS-Grafiken, kein Analytics-Tracking und keine neuen Abhängigkeiten.
 */
(function(){'use strict';
const ID='1.03-B';
const CUES=[
 {marker:'Lektion 1.03-B.',title:'Ohmsches Gesetz',sub:'Eine Erklärung mit Bild und Ton',kind:'opening',
  points:['Spannung U – Volt','Strom I – Ampere','Widerstand R – Ohm']},
 {marker:'Einleitung und Lernziel.',title:'Lernziel und sicherer Rahmen',sub:'Rechnen verstehen statt Formeln auswendig lernen',kind:'overview',
  points:['Aus zwei Grössen die dritte berechnen','Einheiten und Resultate prüfen','Grenzen des ohmschen Modells erkennen']},
 {marker:'Abschnitt eins.',title:'Spannung, Strom und Widerstand',sub:'Drei Grössen – ein geschlossener Modellstromkreis',kind:'definitions',
  points:['U: Potenzialdifferenz in Volt','I: Ladung je Zeit in Ampere','R: Widerstand in Ohm']},
 {marker:'Abschnitt zwei.',title:'Der zentrale Zusammenhang',sub:'U = R × I – drei Formen, ein Modell',kind:'formula',
  points:['U = R × I','I = U / R','R = U / I']},
 {marker:'Ein guter Lösungsweg hat fünf Teile.',title:'In fünf Schritten sicher rechnen',sub:'Aufgabe · bekannte Werte · gesuchte Grösse · Formel · Kontrolle',kind:'steps',
  points:['1. Ausgangslage verstehen','2. Gegebene Werte mit Einheit notieren','3. Gesuchte Grösse festlegen','4. Formel einsetzen und rechnen','5. Resultat plausibilisieren']},
 {marker:'Rechnen wir gemeinsam das erste Beispiel.',title:'Beispiel: 12 V an 120 Ω',sub:'Wie gross ist der elektrische Strom?',kind:'example',
  points:['Gegeben: U = 12 V, R = 120 Ω','I = U / R','I = 12 / 120 = 0,1 A','0,1 A = 100 mA']},
 {marker:'Jetzt die Plausibilität:',title:'Wie wirkt sich R aus?',sub:'Bei gleicher Spannung: höherer Widerstand, kleinerer Strom',kind:'resistance',
  points:['60 Ω → 200 mA','120 Ω → 100 mA','240 Ω → 50 mA']},
 {marker:'Abschnitt drei.',title:'Zwei weitere Umformungen',sub:'Spannung und Widerstand berechnen',kind:'twoways',
  points:['U = 470 Ω × 0,02 A = 9,4 V','R = 9 V / 0,03 A = 300 Ω','2,2 kΩ entspricht 2 200 Ω']},
 {marker:'Abschnitt vier.',title:'Die U-I-Kennlinie',sub:'Ein idealer Widerstand ergibt eine Gerade durch den Ursprung',kind:'graph',
  points:['3 V → 25 mA','6 V → 50 mA','12 V → 100 mA']},
 {marker:'Warum sprechen wir ausdrücklich',title:'Ohmsch oder nichtlinear?',sub:'Eine LED ist kein konstanter Widerstand',kind:'nonlinear',
  points:['Ohmscher Widerstand: gerade Kennlinie','LED: nichtlineare Strom-Spannungs-Kennlinie','Temperatur und Betriebspunkt berücksichtigen']},
 {marker:'Abschnitt fünf.',title:'Strom ist nicht Leistung',sub:'Leistung braucht Spannung und Strom',kind:'power',
  points:['P = U × I','12 V × 0,1 A = 1,2 W','Bei Widerständen auch: P = I² × R']},
 {marker:'Ändern wir die Spannung',title:'Doppelte Spannung – vierfache Leistung',sub:'Vergleich bei konstantem Widerstand 120 Ω',kind:'quad',
  points:['12 V → 0,1 A → 1,2 W','24 V → 0,2 A → 4,8 W','Spannung × 2, Leistung × 4']},
 {marker:'Abschnitt sechs.',title:'Widerstände in Serie',sub:'Gleicher Strom, aufgeteilte Spannung',kind:'series',
  points:['Rges = 100 Ω + 200 Ω = 300 Ω','I = 12 V / 300 Ω = 40 mA','Teilspannungen: 4 V + 8 V = 12 V']},
 {marker:'In einer Parallelschaltung',title:'Widerstände parallel',sub:'Gleiche Spannung, aufgeteilte Ströme',kind:'parallel',
  points:['U1 = U2 = 12 V','I1 = 100 mA; I2 = 50 mA','Iges = 150 mA']},
 {marker:'Abschnitt sieben.',title:'Messwerte kritisch prüfen',sub:'Nennwert, Istwert und Messunsicherheit unterscheiden',kind:'measure',
  points:['Berechnet: 100 mA','Gemessen: beispielsweise 95 mA','Netzteil, Toleranz und Messgerät prüfen']},
 {marker:'Abschnitt acht.',title:'Prüfungsaufgabe – Serienschaltung',sub:'180 Ω und 320 Ω an 10 V',kind:'exam',
  points:['Rges = 500 Ω','I = 10 V / 500 Ω = 20 mA','U1 = 3,6 V und U2 = 6,4 V']},
 {marker:'Jetzt prüfen wir die Teil-Leistungen.',title:'Leistungsbilanz der Aufgabe',sub:'Die Summe der Teil-Leistungen stimmt mit der Gesamtleistung überein',kind:'balance',
  points:['Pges = 10 V × 0,02 A = 0,2 W','P1 = 0,072 W','P2 = 0,128 W','0,072 W + 0,128 W = 0,2 W']},
 {marker:'Abschnitt neun.',title:'Typische Denkfehler vermeiden',sub:'Formel, Einheit, Schaltung und Randbedingungen gehören zusammen',kind:'mistakes',
  points:['mA und A nicht verwechseln','Serien- und Parallelschaltungen unterscheiden','LED nicht als konstanten Widerstand behandeln','Verlustleistung mitprüfen']},
 {marker:'Abschluss und Lernkontrolle.',title:'Überprüfe dein Verständnis',sub:'Drei Kontrollfragen – anschliessend weiter zum Quiz',kind:'finish',
  points:['8 V / 400 Ω = 20 mA','5 V / 10 mA = 500 Ω','Warum ist die LED-Kennlinie nicht ohmsch?']}
];
let ticker=null,rootElement=null,activeIndex=-1,activePhase=-1,sceneTimes=[],disposed=false,playingSince=0;
const escapeHtml=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const $=(q)=>rootElement?.querySelector(q);
function makeTimeline(script){
 const source=String(script||'');
 const words=source.trim().split(/\s+/);
 const n=words.length;
 const starts=CUES.map(c=>{
  const offset=source.indexOf(c.marker);
  if(offset<0)throw Error('Sprechertext-Marker nicht gefunden: '+c.marker);
  return {marker:c.marker,offset,pct:offset===0?0:source.slice(0,offset).trim().split(/\s+/).length/n};
 });
 if(starts[0].pct!==0||starts.some((x,i)=>i>0&&x.pct<=starts[i-1].pct))
  throw Error('Sprechertext-Kapitel nicht aufsteigend');
 return starts;
}
function clamp(n,min,max){return Math.max(min,Math.min(max,n))}
function formatTime(sec){if(!Number.isFinite(sec))sec=0;sec=Math.max(0,Math.floor(sec));return Math.floor(sec/60)+':'+String(sec%60).padStart(2,'0')}
function svg(content){return '<svg class="vp-svg" viewBox="0 0 800 400" role="img" aria-label="Animierte didaktische Grafik; nur Modellstromkreis mit Schutzkleinspannung">'+content+'</svg>'}
function text(x,y,s,size,fill,cls){return '<text x="'+x+'" y="'+y+'" font-size="'+(size||23)+'" fill="'+(fill||'#e8f6ff')+'" text-anchor="middle" class="'+(cls||'')+'">'+escapeHtml(s)+'</text>'}
function badge(x,y,s,fill){return '<rect x="'+(x-75)+'" y="'+(y-28)+'" width="150" height="45" rx="13" fill="'+(fill||'#12485e')+'"/>'+text(x,y,s,20)}
function circuit(config,phase){
 const c=Object.assign({u:'12 V',r:'120 Ω',i:'100 mA',r2:'',u1:'',u2:''},config||{});
 const lead='#7fe0dd',white='#b9d6e7';
 let lines='<path class="vp-current-line" d="M185 290 L185 112 L615 112 L615 290 L185 290" stroke="'+lead+'" fill="none" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>';
 lines+='<rect x="515" y="90" width="116" height="44" rx="10" fill="#142f45" stroke="#fff" stroke-width="3"/>';
 lines+=text(573,117,'R = '+c.r,19);
 lines+='<path d="M166 217 L204 217 M173 239 L197 239" stroke="white" stroke-width="5"/>';
 lines+=text(122,224,'+',22)+text(122,275,'−',22);
 lines+=badge(190,357,'U = '+c.u);
 lines+=badge(579,357,'I = '+c.i);
 lines+=text(398,80,'Einfacher DC-Modellstromkreis',22);
 if(phase>0)lines+='<path d="M250 148 L370 148" stroke="#76e3ae" stroke-width="5" marker-end="url(#vp-arrow)"/>'+text(345,191,'Stromrichtung I',18,'#9decd2');
 if(phase>1)lines+=text(399,270,'I = U / R',36,'#fff');
 return svg('<defs><marker id="vp-arrow" markerWidth="12" markerHeight="12" refX="9" refY="5" orient="auto"><path d="M0 0 L0 10 L10 5 z" fill="#76e3ae"/></marker></defs>'+lines);
}
function graph(nonlinear,phase){
 let x=90,y=330,w=610,h=240, strokes='<path d="M'+x+' '+y+' V'+(-h)+' M'+x+' '+y+' H'+(x+w)+'" stroke="#91aabb" fill="none" stroke-width="3"/>';
 for(let j=1;j<=4;j++){
  const yy=y-h*j/4;
  strokes+='<path d="M'+x+' '+yy+' H'+(x+w)+'" stroke="#ffffff" stroke-opacity=".1" stroke-width="1"/>';
 }
 strokes+=text(424,386,'Spannung U (V)',21,'#aacddf')+text(55,72,'I',25,'#aacddf');
 if(nonlinear){
  strokes+='<path d="M90 330 L670 99" stroke="#83cdeb" stroke-dasharray="9 6" stroke-width="3" fill="none"/>';
  strokes+='<path d="M90 330 C350 330 478 328 560 290 S650 142 700 44" stroke="#78f0b5" stroke-width="7" fill="none" class="vp-graph-line"/>';
  strokes+=text(600,83,'LED (schematisch)',24,'#91fac0')+text(310,169,'Ohmsch',21,'#83cdeb');
 }else{
  strokes+='<path d="M90 330 L665 90" stroke="#70efd7" stroke-width="7" fill="none" class="vp-graph-line"/>';
  const pts=[[3,25],[6,50],[12,100]],color=['#b4e4f0','#a3edbd','#fff'];
  pts.slice(0,Math.max(1,phase+1)).forEach((p,i)=>{
   const px=x+p[0]/12*575,py=y-p[1]/100*240;
   strokes+='<circle cx="'+px+'" cy="'+py+'" r="9" fill="'+color[i]+'"/>'+text(px,py-23,p[0]+' V / '+p[1]+' mA',17);
  });
 }
 return svg(strokes);
}
function bars(type,phase){
 const data=type==='quad'?[{label:'12 V',n:1.2,value:'1,2 W'},{label:'24 V',n:4.8,value:'4,8 W'}]:[{label:'60 Ω',n:200,value:'200 mA'},{label:'120 Ω',n:100,value:'100 mA'},{label:'240 Ω',n:50,value:'50 mA'}];
 const max=Math.max(...data.map(d=>d.n)),unit=type==='quad'?'W':'mA';
 let content=text(400,51,type==='quad'?'Verlustleistung bei R = 120 Ω':'Strom bei U = 12 V',26);
 data.forEach((d,i)=>{
  const left=145+i*(type==='quad'?280:190),h=d.n/max*215,vis=phase>=i;
  content+='<rect x="'+left+'" y="'+(310-(vis?h:8))+'" width="120" height="'+(vis?h:8)+'" rx="9" fill="'+(i%2===0?'#45b6cf':'#77e5b7')+'" class="vp-bar"/>';
  content+=text(left+60,340,d.label,22)+text(left+60,Math.max(70,305-h-16),vis?d.value:'…',22);
 });
 return svg(content);
}
function formulaArt(phase){
 const f=['U = R × I','I = U / R','R = U / I'],y=[105,208,310];
 let code='';
 f.forEach((part,i)=>{code+='<rect x="125" y="'+(y[i]-52)+'" width="540" height="86" rx="19" fill="'+(i===phase?'#126e78':'#102c45')+'" stroke="'+(i===phase?'#87f0d6':'#416679')+'" stroke-width="'+(i===phase?3:1)+'"/>'+text(395,y[i],part,39,i===phase?'#fff':'#a8c4d5');});
 return svg(code);
}
function parallelArt(phase){
 let s='<path d="M125 190 H240 V95 H630 V190 H690 M240 190 V290 H630 V190" stroke="#8ce8dc" stroke-width="6" stroke-linejoin="round" fill="none"/>'+
 '<rect x="377" y="73" width="126" height="44" rx="8" fill="#153348" stroke="#e8f7fa" stroke-width="3"/>'+
 '<rect x="377" y="269" width="126" height="44" rx="8" fill="#153348" stroke="#e8f7fa" stroke-width="3"/>'+
 text(440,101,'R1 = 120 Ω',18)+text(440,297,'R2 = 240 Ω',18)+
 text(150,143,'12 V',26)+text(642,143,'12 V',22)+text(392,35,'Parallelschaltung',25);
 if(phase>0)s+=text(380,157,'I1 = 100 mA',23,'#92efd5');
 if(phase>1)s+=text(380,260,'I2 = 50 mA',23,'#92efd5')+badge(405,370,'Iges = 150 mA');
 return svg(s);
}
function seriesArt(phase,exam){
 const r1=exam?'180 Ω':'100 Ω',r2=exam?'320 Ω':'200 Ω',u=exam?'10 V':'12 V',i=exam?'20 mA':'40 mA';
 let p='<path class="vp-current-line" d="M125 315 V115 H685 V315 H125" stroke="#82e6d9" stroke-width="6" fill="none"/>'+
 '<rect x="240" y="94" width="140" height="44" rx="9" fill="#183c51" stroke="white" stroke-width="3"/>'+
 '<rect x="475" y="94" width="140" height="44" rx="9" fill="#183c51" stroke="white" stroke-width="3"/>'+
 text(310,122,'R1 = '+r1,19)+text(545,122,'R2 = '+r2,19)+
 text(100,217,'+',27)+text(100,262,'−',27)+badge(196,365,'U = '+u)+badge(608,365,'I = '+i);
 if(phase>0)p+=text(310,195,exam?'3,6 V':'4 V',27,'#92efd5')+text(545,195,exam?'6,4 V':'8 V',27,'#92efd5');
 if(phase>1)p+=text(406,254,exam?'180 + 320 = 500 Ω':'100 + 200 = 300 Ω',29,'#fff');
 return svg(p);
}
function gauge(phase){
 const labels=['Sollwert','Istwert','Differenz'],values=['100 mA','95 mA','−5 mA'];
 let s=text(400,50,'Beispiel: modellierte Messabweichung',26);
 labels.forEach((v,i)=>{s+='<rect x="120" y="'+(80+i*93)+'" width="560" height="73" rx="15" fill="'+(i===phase?'#116577':'#14334b')+'"/>'+text(265,126+i*93,v,22)+text(555,126+i*93,values[i],26,i===phase?'#aaf9df':'#e7f2f6');});
 return svg(s);
}
function slidesFor(c,phase){
 switch(c.kind){
  case 'opening':return circuit({u:'12 V',r:'120 Ω',i:'100 mA'},2);
  case 'overview':return circuit({},phase);
  case 'definitions':return circuit({},phase);
  case 'formula':return formulaArt(phase);
  case 'steps':return formulaArt(phase);
  case 'example':return circuit({},phase);
  case 'resistance':return bars('resistance',phase);
  case 'twoways':return formulaArt(phase);
  case 'graph':return graph(false,phase);
  case 'nonlinear':return graph(true,phase);
  case 'power':return circuit({u:'12 V',r:'120 Ω',i:'100 mA'},phase);
  case 'quad':return bars('quad',phase);
  case 'series':return seriesArt(phase,false);
  case 'parallel':return parallelArt(phase);
  case 'measure':return gauge(phase);
  case 'exam':return seriesArt(phase,true);
  case 'balance':return bars('quad',phase);
  case 'mistakes':return formulaArt(phase);
  case 'finish':return circuit({},phase);
  default:return circuit({},phase);
 }
}
function pointsMarkup(points,phase){
 return '<div class="vp-facts">'+points.map((point,i)=>
  '<div class="vp-fact '+(i<=phase+Math.max(0,points.length-4)?'vp-fact-on':'')+'">'+
  '<span class="vp-fact-no">'+String(i+1).padStart(2,'0')+'</span><span>'+escapeHtml(point)+'</span></div>').join('')+'</div>';
}
function sceneMarkup(c,phase,index){
 return '<div class="vp-scene vp-scene-fade"><div class="vp-scene-header"><span class="vp-kicker">Kapitel '+String(index+1).padStart(2,'0')+' / '+CUES.length+'</span><h3>'+escapeHtml(c.title)+'</h3><p>'+escapeHtml(c.sub)+'</p></div>'+
 '<div class="vp-presentation"><div class="vp-visual">'+slidesFor(c,phase)+'</div><div class="vp-interpretation"><span class="vp-caption">Während Thorsten High erklärt</span>'+pointsMarkup(c.points,phase)+'</div></div>'+
 '<div class="vp-safe">Didaktisches Modell · ausschliesslich für Papier, Simulation und geeignete Schutzkleinspannung · keine Installationsanweisung</div></div>';
}
function render(l,state){
 if(l?.id!==ID)return '';
 return '<section id="video-pilot" class="vp-shell" aria-label="Audiovisueller Pilotunterricht" data-lesson="'+ID+'">'+
 '<div class="vp-headline"><div><span class="vp-chip">PILOT · ANIMIERTER UNTERRICHT</span><h2>Ohmsches Gesetz – Bild und Ton</h2><p>Eine zusammenhängende visuelle Lektion mit der originalen Thorsten-High-Aufnahme.</p></div><button class="btn" type="button" id="vp-expand" aria-label="Darstellung vergrössern">Bildschirm füllen</button></div>'+
 '<div class="vp-stage" id="vp-stage" role="group" aria-label="Animierte Lehrdarstellung">'+sceneMarkup(CUES[0],0,0)+'</div>'+
 '<div class="vp-control-panel"><div class="vp-progress-row"><span id="vp-time">0:00</span><input id="vp-seek" type="range" min="0" max="1000" value="0" step="1" aria-label="Position in der Audiolektion" disabled><span id="vp-duration">–:––</span></div>'+
 '<div class="vp-controls"><button class="btn" id="vp-back" type="button" aria-label="15 Sekunden zurück">−15 s</button>'+
 '<button class="btn teal vp-primary" id="vp-play" type="button" disabled>Audio wird geladen …</button>'+
 '<button class="btn" id="vp-forward" type="button" aria-label="15 Sekunden vorwärts">+15 s</button>'+
 '<label class="vp-speed-label" for="vp-speed">Tempo <select id="vp-speed" aria-label="Wiedergabegeschwindigkeit">'+
 [0.8,1,1.15,1.3,1.5].map(x=>'<option value="'+x+'" '+((Number(state?.settings?.rate)||1)===x?'selected':'')+'>'+String(x).replace('.',',')+'×</option>').join('')+
 '</select></label></div><div class="vp-status" id="vp-status" role="status" aria-live="polite">Verbinde die Sprecheraufnahme …</div></div>'+
 '<div class="vp-chapter-head"><h3>Kapitel direkt anwählen</h3><span>Das Bild folgt der aktuellen Audioposition</span></div>'+
 '<div id="vp-chapters" class="vp-chapters">'+CUES.map((c,i)=>'<button type="button" data-vp-chapter="'+i+'" class="vp-chapter '+(i===0?'active':'')+'"><span class="vp-ch-number">'+String(i+1).padStart(2,'0')+'</span><span>'+escapeHtml(c.title)+'</span><small data-vp-time="'+i+'">–:––</small></button>').join('')+'</div>'+
 '<p class="vp-note"><strong>Synchronisation:</strong> Die Kapitelwechsel sind aus den Wortpositionen des originalen Sprechmanuskripts geschätzt. Die Bilder folgen dem Audio kapitelweise, sind aber noch nicht auf einzelne Wörter exakt ausgerichtet. Die Aufnahme selbst ist unverändert.</p>'+
 '<a class="vp-source-link" href="https://github.com/marcoitis/elektro-efz/releases/download/thorsten-high-v0118-audio-20261118/1.03-B.mp3" target="_blank" rel="noopener noreferrer">MP3 direkt öffnen (falls Online-Wiedergabe scheitert)</a>'+
 '</section>';
}
function halt(){
 disposed=true;
 if(ticker){clearInterval(ticker);ticker=null;}
 if(rootElement?.classList.contains('vp-expanded'))rootElement.classList.remove('vp-expanded');
 rootElement=null;activeIndex=-1;activePhase=-1;
}
function bind(state,actions){
 const el=document.querySelector('#video-pilot');
 if(!el)return;
 halt();disposed=false;rootElement=el;
 let times;
 try{times=makeTimeline(window.ElektroLectures?.[ID]||'')}catch(e){
  $('#vp-status').textContent='Kapitelanalyse fehlgeschlagen: '+e.message;return;
 }
 sceneTimes=times;
 const api=window.ElektroAudio;
 const sync=()=>{
  if(disposed||!rootElement||!document.contains(rootElement)){halt();return;}
  const v=api.getState();
  const valid=v.lessonId===ID&&v.loaded;
  const dur=Number(v.duration)||0;
  const t=valid?Number(v.current)||0:0;
  const f=dur>0?clamp(t/dur,0,1):0;
  const idx=clamp(times.reduce((n,x,i)=>f>=x.pct?i:n,0),0,CUES.length-1);
  const end=idx+1<times.length?times[idx+1].pct:1;
  const within=end>times[idx].pct?clamp((f-times[idx].pct)/(end-times[idx].pct),0,.999):0;
  const phase=clamp(Math.floor(within*3),0,2);
  if(idx!==activeIndex||phase!==activePhase){
   activeIndex=idx;activePhase=phase;
   const stage=$('#vp-stage');
   if(stage)stage.innerHTML=sceneMarkup(CUES[idx],phase,idx);
   rootElement.querySelectorAll('[data-vp-chapter]').forEach(b=>b.classList.toggle('active',Number(b.dataset.vpChapter)===idx));
  }
  const seek=$('#vp-seek'),play=$('#vp-play');
  if(seek&&!seek.matches(':active')){seek.value=Math.round(f*1000);seek.disabled=!valid;}
  if($('#vp-time'))$('#vp-time').textContent=formatTime(t);
  if($('#vp-duration'))$('#vp-duration').textContent=dur>0?formatTime(dur):'–:––';
  if(play){play.disabled=!valid;play.textContent=!valid?'Audio wird geladen …':v.playing?'Ⅱ Pause':'▶ Film starten';}
  if($('#vp-status')){
   if(!valid)$('#vp-status').textContent='Audio wird vorbereitet. Bei Problemen online starten oder die MP3 über Offline & Audio importieren.';
   else if(v.remote)$('#vp-status').textContent='Thorsten High · Online-Audio · '+(v.playing?'Wiedergabe läuft':'bereit');
   else $('#vp-status').textContent='Thorsten High · lokal gespeicherte MP3 · '+(v.playing?'Wiedergabe läuft':'bereit');
  }
  if(dur>0)rootElement.querySelectorAll('[data-vp-time]').forEach(e=>{
   const p=times[Number(e.dataset.vpTime)]?.pct||0;
   e.textContent=formatTime(dur*p);
  });
 };
 const seekTo=seconds=>{
  const current=api.getState();if(current.loaded&&current.lessonId===ID)api.seek(seconds-current.current);
  sync();
 };
 $('#vp-play')?.addEventListener('click',()=>{
  const s=api.getState();
  if(!s.loaded||s.lessonId!==ID)return;
  if(s.playing)api.pause();else{
   // play() runs immediately in the user's click gesture, also on iPhone.
   api.play().catch(e=>{const st=$('#vp-status');if(st)st.textContent='Audio konnte nicht starten: '+e.message;});
  }
  sync();
 });
 $('#vp-back')?.addEventListener('click',()=>{api.seek(-15);sync()});
 $('#vp-forward')?.addEventListener('click',()=>{api.seek(15);sync()});
 $('#vp-seek')?.addEventListener('change',e=>{
  const s=api.getState();if(s.duration>0)seekTo(s.duration*Number(e.target.value)/1000);
 });
 rootElement.querySelectorAll('[data-vp-chapter]').forEach(b=>b.addEventListener('click',()=>{
  const s=api.getState();if(s.duration<=0)return;
  seekTo(s.duration*times[Number(b.dataset.vpChapter)].pct);
 }));
 $('#vp-speed')?.addEventListener('change',e=>{
  const rate=Number(e.target.value);
  if(![.8,1,1.15,1.3,1.5].includes(rate))return;
  api.setRate(rate);
  state.settings.rate=rate;
  actions.save();
 });
 $('#vp-expand')?.addEventListener('click',()=>{
  rootElement.classList.toggle('vp-expanded');
  const expanded=rootElement.classList.contains('vp-expanded');
  $('#vp-expand').textContent=expanded?'Verkleinern':'Bildschirm füllen';
 });
 const onKey=e=>{
  if(e.key==='Escape'&&rootElement?.classList.contains('vp-expanded')){
   rootElement.classList.remove('vp-expanded');$('#vp-expand').textContent='Bildschirm füllen';
  }
 };
 rootElement.addEventListener('keydown',onKey);
 sync();
 ticker=setInterval(sync,270);
 // Source is loaded prior to tapping Play; the audio element has one owner.
 void actions.audioLoad().then(()=>{if(!disposed)sync()}).catch(err=>{
  const st=$('#vp-status');if(st)st.textContent='Audio konnte nicht geladen werden: '+err.message;
 });
}
window.ElektroVideoPilot={ID,render,bind,halt,makeTimeline,sceneMarkup,sceneCount:CUES.length};
})();