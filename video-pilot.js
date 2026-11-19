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
/* Director V2: one large teaching surface rather than a competing sidebar.
 * SVG movement depicts conventional current direction. Text in the original
 * Thorsten transcript governs the topics; no invented simultaneous voiceover.
 */
const PALETTE={teal:'#6ce4d0',blue:'#75c5f0',green:'#95eab4',white:'#f1f8fb',muted:'#afc7d6',dark:'#14354a'};
function svg(content,label='Didaktische Visualisierung'){
 return '<svg class="vp-svg vp-master-svg" viewBox="0 0 800 420" role="img" aria-label="'+escapeHtml(label)+'">'+
 '<defs><linearGradient id="vp-glow" x1="0" x2="1"><stop offset="0%" stop-color="#238b9e"/><stop offset="100%" stop-color="#63e0c3"/></linearGradient>'+
 '<marker id="vp-dir" markerWidth="11" markerHeight="11" refX="8" refY="5" orient="auto"><path d="M0 0 L0 10 L10 5z" fill="#92eacf"/></marker></defs>'+content+'</svg>';
}
function text(x,y,content,size=29,fill=PALETTE.white,anchor='middle',weight=600){
 return '<text x="'+x+'" y="'+y+'" font-family="Inter,system-ui,Arial,sans-serif" font-size="'+size+'" font-weight="'+weight+'" fill="'+fill+'" text-anchor="'+anchor+'">'+escapeHtml(content)+'</text>';
}
function rect(x,y,w,h,fill=PALETTE.dark,stroke='#447489',r=16){
 return '<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="'+r+'" fill="'+fill+'" stroke="'+stroke+'" stroke-width="1.5"/>';
}
function caption(x,y,content){return text(x,y,content,16,PALETTE.muted);}
function currentDots(path,duration=4,offset=0){
 let items='';
 for(let k=0;k<5;k++){
  items+='<circle class="vp-current-dot" r="6" fill="'+(k%2?PALETTE.green:PALETTE.teal)+'">'+
   '<animateMotion dur="'+duration+'s" begin="'+(-k*duration/5-offset).toFixed(2)+'s" repeatCount="indefinite" path="'+path+'"/></circle>';
 }
 return items;
}
function circuit(config={},phase=1){
 const x={u:'12 V',r:'120 Ω',i:'100 mA',...config};
 let a='';
 const trace='M152 177 V85 H640 V308 H152 V246';
 a+='<path d="M152 177 V85 H500 M622 85 H640 V308 H152 V246" fill="none" stroke="#7babc2" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>';
 a+='<path d="M122 177 H182 M133 246 H171" stroke="#e8fafc" stroke-width="6" stroke-linecap="round"/>';
 a+=rect(500,61,122,48,'#1a4456','#a9f7e2',8)+text(561,93,'R = '+x.r,19);
 a+=text(100,186,'+',24,PALETTE.green)+text(100,256,'−',24,PALETTE.blue);
 if(phase>=0)a+=rect(77,322,205,64,'#1a4054','#4e7c8d',13)+caption(179,346,'Spannung')+text(179,376,'U = '+x.u,27);
 if(phase>=1){a+=currentDots(trace);a+=text(398,60,'Technische Stromrichtung',18,PALETTE.green);a+='<path d="M312 121 H460" stroke="'+PALETTE.green+'" stroke-width="4" marker-end="url(#vp-dir)"/>';}
 if(phase>=2)a+=rect(517,322,215,64,'#124b55','#53c4ab',13)+caption(622,345,'Strom')+text(622,376,'I = '+x.i,25);
 return svg(a,'DC-Modellstromkreis: technische Stromrichtung ausserhalb der Quelle von Plus über einen Widerstand nach Minus');
}
function formulas(phase){
 const eq=['U = R × I','I = U / R','R = U / I'];
 let a=caption(400,52,'DREI SCHREIBWEISEN · EIN GESETZ');
 eq.forEach((f,i)=>{
  const active=i===phase;
  a+=rect(154,77+i*105,492,85,active?'#136973':'#12364d',active?'#9af1d7':'#4b7287',18);
  a+=text(400,133+i*105,f,active?43:31,active?PALETTE.white:'#a9c4d1');
 });
 return svg(a,'Die drei Formeln des Ohmschen Gesetzes; die aktuelle wird hervorgehoben');
}
function steps(phase){
 const steps=['Aufgabe verstehen','Werte mit Einheiten','Gesuchte Grösse','Formel einsetzen','Ergebnis prüfen'];
 let a=caption(400,48,'RECHENWEG · SCHRITT FÜR SCHRITT');
 steps.forEach((str,i)=>{
  const active=i<=Math.floor((phase+1)*5/3)-1;
  const x=95+(i%3)*215,y=91+Math.floor(i/3)*142;
  a+=rect(x,y,194,113,active?'#174e60':'#142e43',active?'#82ead0':'#496b80',15);
  a+=text(x+26,y+40,String(i+1).padStart(2,'0'),26,active?PALETTE.green:'#648797','start');
  a+=text(x+97,y+76,str,15,active?PALETTE.white:'#98b4c6');
 });
 return svg(a,'Fünf Rechenschritte von Aufgabe über Formel bis Plausibilitätskontrolle');
}
function example(phase){
 let a=circuit({u:'12 V',r:'120 Ω',i:'100 mA'},Math.min(2,phase));
 const calculation=['U = 12 V    ·    R = 120 Ω','I = U / R = 12 V / 120 Ω','I = 0,1 A = 100 mA'][phase];
 // Keep the connected circuit as the central illustration. Add one current calculation,
 // not a column of unrelated facts.
 a=a.replace('</svg>',rect(245,213,340,67,'#102f47','#81d9c6',13)+
  text(415,255,calculation,phase===1?24:23,PALETTE.white)+'</svg>');
 return a;
}
function graph(nonlinear,phase){
 let a='<path d="M104 344 V58 M104 344 H712" stroke="#bcd9e7" stroke-width="3"/>';
 for(let i=1;i<=4;i++){a+='<path d="M104 '+(344-i*62)+' H712" stroke="#ffffff" stroke-opacity=".1"/>';}
 a+=text(407,402,'Spannung U (V)',20,PALETTE.muted)+text(55,55,'I',23,PALETTE.muted);
 if(nonlinear){
  a+='<path d="M110 344 L671 92" fill="none" stroke="'+PALETTE.blue+'" stroke-width="3" stroke-dasharray="10 7"/>';
  a+='<path d="M110 344 C371 344 520 344 572 287 S655 133 697 64" fill="none" stroke="'+PALETTE.green+'" stroke-width="7" stroke-linecap="round" class="vp-trace-reveal"/>';
  if(phase>=1)a+=text(500,60,'LED: nichtlinear',23,PALETTE.green);
  if(phase>=2)a+=text(288,197,'Ohmscher Widerstand',21,PALETTE.blue);
 }else{
  a+='<path d="M104 344 L682 96" fill="none" stroke="'+PALETTE.teal+'" stroke-width="7" stroke-linecap="round" class="vp-trace-reveal"/>';
  const pts=[[3,25],[6,50],[12,100]];
  pts.slice(0,phase+1).forEach(([u,i])=>{
   const x=104+u/12*578,y=344-i/100*248;
   a+='<circle cx="'+x+'" cy="'+y+'" r="9" fill="#e2fff6"/>'+text(x,y-22,u+' V · '+i+' mA',17);
  });
 }
 return svg(a,nonlinear?'Nichtlineare LED-Kennlinie verglichen mit einem ohmschen Widerstand':'Lineare U-I-Kennlinie bei konstantem Widerstand von 120 Ohm');
}
function bars(type,phase){
 const power=type==='quad';
 const data=power?[['12 V',1.2,'1,2 W'],['24 V',4.8,'4,8 W']]:[['60 Ω',200,'200 mA'],['120 Ω',100,'100 mA'],['240 Ω',50,'50 mA']];
 const max=Math.max(...data.map(x=>x[1]));
 let a=caption(400,45,power?'GLEICHER WIDERSTAND · LEISTUNGSVERGLEICH':'GLEICHE SPANNUNG · STROMVERGLEICH');
 data.forEach(([label,n,value],i)=>{
  const shown=i<=phase,base=328,height=shown?n/max*236:0;
  const x=power?234+i*230:130+i*214;
  a+=rect(x,base-height,130,height||2,i%2?PALETTE.green:PALETTE.blue,'none',9);
  a+=text(x+65,361,label,24);
  if(shown)a+=text(x+65,base-height-17,value,25,PALETTE.white);
 });
 return svg(a,power?'Leistung vervierfacht sich bei doppelter Spannung und gleichem Widerstand':'Strom sinkt bei erhöhtem Widerstand und gleicher Spannung');
}
function twoWays(phase){
 const entries=[['Spannung berechnen','U = 470 Ω × 0,02 A','9,4 V'],['Widerstand berechnen','R = 9 V / 0,03 A','300 Ω'],['Einheiten umrechnen','2,2 kΩ = 2 200 Ω','5 mA bei 11 V']];
 const d=entries[phase];
 return svg(rect(100,73,600,264,'#12394f','#68c7b7',23)+caption(400,124,d[0])+text(400,202,d[1],36)+text(400,294,d[2],44,PALETTE.green),'Eine Umformung des Ohmschen Gesetzes mit konkretem Rechenbeispiel');
}
function power(phase){
 const rows=[['Leistung','P = U × I','Watt'],['12 V · 0,1 A','P = 1,2 W','Wärmeabgabe beachten'],['Mit Ohm kombiniert','P = I² × R','auch P = U² / R']];
 const r=rows[phase];
 return svg(rect(122,72,556,268,'#12384d','#6bd8bd',20)+caption(400,120,r[0])+text(400,211,r[1],47)+text(400,293,r[2],24,PALETTE.green),'Leistungsformeln und konkrete Werte für einen ohmschen Verbraucher');
}
function series(phase,exam=false){
 const values=exam?{u:'10 V',r1:'180 Ω',r2:'320 Ω',i:'20 mA',v1:'3,6 V',v2:'6,4 V',sum:'500 Ω'}:
 {u:'12 V',r1:'100 Ω',r2:'200 Ω',i:'40 mA',v1:'4 V',v2:'8 V',sum:'300 Ω'};
 let a='<path d="M123 185 V100 H240 M375 100 H465 M600 100 H683 V316 H123 V251" stroke="#82bbce" stroke-width="6" fill="none" stroke-linecap="round"/>';
 a+='<path d="M94 185 H152 M103 251 H144" stroke="#fff" stroke-width="6"/>'+
 text(77,193,'+',25,PALETTE.green)+text(77,261,'−',25,PALETTE.blue);
 a+=rect(240,75,135,50,'#1d4256','#a5f1dc',7)+text(307,106,'R1 = '+values.r1,18);
 a+=rect(465,75,135,50,'#1d4256','#a5f1dc',7)+text(533,106,'R2 = '+values.r2,18);
 a+=currentDots('M123 185 V100 H683 V316 H123 V251',5);
 a+=text(156,374,'U = '+values.u,25);
 if(phase>=1)a+=text(309,169,'U1 = '+values.v1,22,PALETTE.green)+text(532,169,'U2 = '+values.v2,22,PALETTE.green);
 if(phase>=2)a+=text(477,303,'I = '+values.i+'    ·    Rges = '+values.sum,22,PALETTE.white);
 return svg(a,'Serienschaltung: gleicher Strom, Teilspannungen '+values.v1+' und '+values.v2+' addieren sich zur Gesamtspannung');
}
function parallel(phase){
 let a='<path d="M115 185 V96 H268 M268 96 H375 M508 96 H646 V320 H115 V250 M268 96 V278 H375 M508 278 H646" fill="none" stroke="#8ebed0" stroke-width="6" stroke-linejoin="round"/>';
 // Two resistors are placed between the exact shared node pairs.
 a+='<path d="M90 185 H141 M101 250 H130" stroke="#fff" stroke-width="6"/>'+
 text(70,196,'+',24,PALETTE.green)+text(70,266,'−',24,PALETTE.blue);
 // Both resistors connect to the same two nodes (268 and 646).
 // Top resistor occupies 375..508 at y=96; bottom resistor 375..508 at y=278.
 a+=rect(375,72,133,48,'#173c54','#85e6d1',8)+text(441,104,'R1 = 120 Ω',18);
 a+=rect(375,254,133,48,'#173c54','#85e6d1',8)+text(441,285,'R2 = 240 Ω',18);
 // Current path branches; never depict conductors bridging a resistor.
 a+=currentDots('M115 185 V96 H646 V320 H115 V250',4);
 if(phase>=0)a+=text(185,376,'U = 12 V',24);
 if(phase>=1)a+=text(445,160,'I1 = 100 mA',21,PALETTE.green);
 if(phase>=2)a+=text(445,358,'I2 = 50 mA',21,PALETTE.green)+text(615,392,'Iges = 150 mA',20);
 return svg(a,'Parallelschaltung: gleiche Spannung an beiden Widerständen, Teilströme 100 und 50 Milliampere');
}
function measure(phase){
 const labels=[['Berechneter Strom','100 mA'],['Beispielmessung','95 mA'],['Abweichung','−5 mA']];
 let a=caption(400,51,'NENNWERT IST NICHT ZWANGSLÄUFIG MESSWERT');
 labels.forEach(([label,val],i)=>{
  a+=rect(122,82+i*100,556,81,i===phase?'#186474':'#14364b',i===phase?'#8bedcf':'#476e82',14);
  a+=text(178,130+i*100,label,21,PALETTE.muted,'start');
  a+=text(613,133+i*100,val,30,i===phase?PALETTE.green:PALETTE.white,'end');
 });
 return svg(a,'Beispiel zur Messabweichung zwischen berechneten 100 und gemessenen 95 Milliampere');
}
function balance(phase){
 const vals=[['R1','0,072 W'],['R2','0,128 W'],['Gesamt','0,200 W']];
 let a=caption(400,49,'DIE SUMME DER TEILLEISTUNGEN STIMMT');
 vals.forEach(([name,value],i)=>{
  a+=rect(107+i*212,104,184,178,i<=phase?'#155063':'#133348',i===phase?'#85f0d3':'#41687d',14);
  a+=text(199+i*212,164,name,23,PALETTE.muted);
  if(i<=phase)a+=text(199+i*212,231,value,26,PALETTE.white);
 });
 if(phase>=2)a+=text(400,360,'0,072 W + 0,128 W = 0,200 W',28,PALETTE.green);
 return svg(a,'Rechnerische Leistungsbilanz, die Gesamtleistung entspricht den beiden Teil-Leistungen');
}
function mistakes(phase){
 const errors=[['Einheit prüfen','1 A = 1 000 mA'],['Schaltung beachten','Serie ≠ parallel'],['Modell beachten','LED ≠ konstanter R']];
 const item=errors[phase];
 return svg(rect(105,78,590,268,'#14374e','#83dfcd',24)+caption(400,126,'DENKFEHLER ERKENNEN')+
 text(400,208,item[0],39)+text(400,282,item[1],32,PALETTE.green),'Typischer Denkfehler wird einzeln und übersichtlich hervorgehoben');
}
function finish(phase){
 const problems=[['400 Ω · 8 V','I = 20 mA'],['5 V · 10 mA','R = 500 Ω'],['LED-Kennlinie','Nichtlinear · Temperatur beachten']];
 const d=problems[phase];
 return svg(rect(95,67,610,292,'#143a50','#73d9c6',23)+
 caption(400,124,'LERNKONTROLLE · AUFGABE '+(phase+1)+' VON 3')+
 text(400,209,d[0],38)+text(400,295,d[1],30,PALETTE.green),'Kontrollfragen erscheinen erst im ausdrücklich gesprochenen Abschlussabschnitt');
}
function slidesFor(c,phase){
 switch(c.kind){
 case 'opening':return circuit({},2);
 case 'overview':case 'definitions':return circuit({},phase);
 case 'formula':return formulas(phase);
 case 'steps':return steps(phase);
 case 'example':return example(phase);
 case 'resistance':return bars('resistance',phase);
 case 'twoways':return twoWays(phase);
 case 'graph':return graph(false,phase);
 case 'nonlinear':return graph(true,phase);
 case 'power':return power(phase);
 case 'quad':return bars('quad',phase);
 case 'series':return series(phase);
 case 'parallel':return parallel(phase);
 case 'measure':return measure(phase);
 case 'exam':return series(phase,true);
 case 'balance':return balance(phase);
 case 'mistakes':return mistakes(phase);
 case 'finish':return finish(phase);
 default:return circuit({},phase);
 }
}
function sceneMarkup(c,phase,index){
 // Deliberately no secondary facts list or "Während Thorsten erklärt" header:
 // the full visual area is reserved for one explanation at a time.
 return '<div class="vp-scene vp-scene-fade"><div class="vp-scene-header">'+
 '<span class="vp-kicker">LEKTION 1.03-B · KAPITEL '+String(index+1).padStart(2,'0')+' / '+CUES.length+'</span>'+
 '<h3>'+escapeHtml(c.title)+'</h3></div>'+
 '<div class="vp-canvas">'+slidesFor(c,phase)+'</div>'+
 '<div class="vp-safe">Didaktisches Modell · nur für Simulation und geeignete Schutzkleinspannung</div></div>';
}
function dcAcMarkup(){
 // This segment is demonstrative and deliberately NOT synchronized to
 // Ohm's law narration: the original audio does not explain AC/DC.
 const axis=(y)=>'<path d="M100 '+y+' H700" stroke="#668ba0" stroke-width="8" stroke-linecap="round"/>';
 const dc=svg(axis(215)+
  '<path d="M160 156 H620" stroke="#83e9cf" stroke-width="4" marker-end="url(#vp-dir)"/>'+
  currentDots('M105 215 H695',3)+
  text(400,91,'GLEICHSTROM (DC)',33)+text(400,305,'Stromrichtung bleibt gleich',23,PALETTE.muted),
  'Gleichstrom als zeitlich gerichtete konventionelle Stromrichtung');
 const ac=svg(axis(215)+
  '<path d="M130 155 H670" stroke="#8dd4fb" stroke-width="2" stroke-dasharray="9 9"/>'+
  '<path class="vp-ac-right" d="M245 177 H565" stroke="#8dd4fb" stroke-width="5" marker-end="url(#vp-dir)"/>'+
  '<path class="vp-ac-left" d="M555 176 H232" stroke="#8dd4fb" stroke-width="5" marker-end="url(#vp-dir)"/>'+
  '<circle r="9" fill="#93e8fa"><animateMotion dur="4s" repeatCount="indefinite" path="M130 215 H670 H130"/></circle>'+
  '<path d="M160 356 H640" stroke="#708ba0" stroke-width="2"/>'+
  '<path d="M160 356 C200 310 240 310 280 356 S360 402 400 356 S480 310 520 356 S600 402 640 356" stroke="#8dd4fb" stroke-width="3" fill="none"/>'+
  text(400,91,'WECHSELSTROM (AC)',33)+text(400,305,'Richtung wechselt periodisch',23,PALETTE.muted),
  'Wechselstrom als langsam hin- und hergehende konventionelle Stromrichtung');
 return '<section id="vp-dc-ac" class="vp-demonstration"><div class="vp-demo-intro">'+
 '<div><span class="vp-demo-kicker">ZUSÄTZLICHE ANIMATION · AUSSERHALB DER SPRECHERLEKTION</span>'+
 '<h3>Gleichstrom und Wechselstrom vergleichen</h3>'+
 '<p>Die Animation zeigt die technische Stromrichtung schematisch in Zeitlupe. Bei Wechselstrom kehrt sich die Richtung periodisch um. Die Bewegung ist nicht massstabsgetreu und stellt keine einzelnen Elektronenbahnen dar.</p></div>'+
 '<button type="button" class="btn" id="vp-demo-toggle" aria-expanded="false" aria-controls="vp-demo-grid">Vergleich ansehen</button></div>'+
 '<div id="vp-demo-grid" class="vp-demo-grid" hidden><div>'+dc+'</div><div>'+ac+'</div></div></section>';
}
function render(l,state){
 if(l?.id!==ID)return '';
 return '<section id="video-pilot" class="vp-shell" aria-label="Audiovisueller Pilotunterricht" data-vp-id="'+ID+'">'+
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
 dcAcMarkup()+
 '<p class="vp-fallback"><a class="btn teal" href="./video-103-b.html" target="_blank" rel="noopener noreferrer">Videolektion im separaten Safari-Player starten</a></p>'+
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
  const stage=$('#vp-stage');
  if(stage){
   stage.classList.toggle('vp-is-playing',Boolean(v.playing));
   stage.querySelectorAll('svg').forEach(visual=>{
    try{if(typeof visual.pauseAnimations==='function'){
     if(v.playing)visual.unpauseAnimations();else visual.pauseAnimations();
    }}catch(_){/* SVG animation not supported: static diagram remains */}
   });
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
  const target=s.duration*times[Number(b.dataset.vpChapter)].pct;
  seekTo(Math.min(s.duration-.25,Math.max(0,target+1.3)));
 }));
 $('#vp-speed')?.addEventListener('change',e=>{
  const rate=Number(e.target.value);
  if(![.8,1,1.15,1.3,1.5].includes(rate))return;
  api.setRate(rate);
  state.settings.rate=rate;
  actions.save();
 });
 $('#vp-demo-toggle')?.addEventListener('click',()=>{
  const container=$('#vp-demo-grid'),button=$('#vp-demo-toggle');
  if(!container||!button)return;
  const opening=container.hidden;
  container.hidden=!opening;
  button.setAttribute('aria-expanded',String(opening));
  button.textContent=opening?'Vergleich schliessen':'Vergleich ansehen';
  container.querySelectorAll('svg').forEach(v=>{
   try{if(opening)v.unpauseAnimations();else v.pauseAnimations();}catch(_){}
  });
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