/* Elektro EFZ · 1.01-C · didaktische Sicherheits- und PV-Systemgrafiken. Keine Schalt- oder Arbeitsanleitung. */
(()=>{'use strict';
const scenes={
 intro:['SICHERHEITSREGELN','Arbeitsvorbereitung und Schutz','intro'],
 overview:['5 + 5 LEBENSWICHTIGE REGELN','Organisation plus spannungsfreies Arbeiten','overview'],
 rules_sequence:['DIE FÜNF SICHERHEITSREGELN','Fünf Schritte – eine zusammenhängende Schutzfolge','sequence'],
 rule1:['1 · VOLLSTÄNDIG FREISCHALTEN','Alle relevanten Quellen und Einspeisungen erfassen','rule1'],
 rule2:['2 · GEGEN WIEDEREINSCHALTEN SICHERN','Unbeabsichtigtes Wiedereinschalten verhindern','rule2'],
 rule3:['3 · SPANNUNGSFREIHEIT FESTSTELLEN','Nachweis statt Annahme','rule3'],
 rule4:['4 · ERDEN UND KURZSCHLIESSEN','Soweit erforderlich – nur im passenden Verfahren','rule4'],
 rule5:['5 · BENACHBARTE TEILE SCHÜTZEN','Arbeitsbereich und Umgebung gemeinsam betrachten','rule5'],
 plus5:['DIE FÜNF ORGANISATORISCHEN REGELN','Auftrag · Personal · Arbeitsmittel · PSA · Kontrolle','plus5'],
 order:['KEINE REGEL WIRKT ALLEIN','Arbeitsauftrag, Anlage und Arbeitsverfahren bestimmen die Umsetzung','order'],
 sources:['ENERGIEQUELLEN IM PV-SYSTEM','Module · Netz · Speicher · weitere Einspeisungen','sources'],
 pv_modules:['PV-MODULE BEI LICHT','Photovoltaikgenerator als DC-Energiequelle','modules'],
 acdc:['AC AUS ≠ DC SPANNUNGSFREI','Getrennte Systemseiten und unterschiedliche Zustände','acdc'],
 inverter:['WECHSELRICHTER UND RESTENERGIE','Gespeicherte Energie und Herstellerwartezeit','inverter'],
 battery:['BATTERIESPEICHER','Eine zusätzliche, eigenständige Energiequelle','battery'],
 multiple:['MEHRERE EINSPEISUNGEN','Das gesamte System und alle Quellen berücksichtigen','multiple'],
 dc_arc:['DC-LICHTBOGEN','Gleichstrom kann einen Lichtbogen aufrechterhalten','arc'],
 stop:['STOPP BEI UNKLARHEIT','Nicht berühren · nicht improvisieren · zuständige Fachperson','stop'],
 scenario:['FALLBEISPIEL','AC aus · Tageslicht · Speicher vorhanden','scenario'],
 evidence:['BEOBACHTUNG ≠ NACHWEIS','Anzeigezustand ist keine Spannungsfreiheitsfeststellung','evidence'],
 planning:['SICHERE ARBEITSVORBEREITUNG','Auftrag · Zuständigkeit · Unterlagen · Freigabe','planning'],
 task:['THEORETISCHE CHECKLISTE','Quellen und offene Fragen dokumentieren','task'],
 question:['LERNKONTROLLE','Ist die DC-Seite automatisch spannungsfrei?','question'],
 answer:['ANTWORT: NEIN','PV-Module können bei Licht weiterhin Spannung liefern','answer']
};
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const text=(x,y,t,n=24,color='#e8f5fa')=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" font-family="Arial,sans-serif" font-size="'+n+'" font-weight="700" fill="'+color+'">'+esc(t)+'</text>';
const rect=(x,y,w,h,fill='#173e53',stroke='#7ddcc6')=>'<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="16" fill="'+fill+'" stroke="'+stroke+'" stroke-width="3"/>';
const line=(x1,y1,x2,y2,color='#7ddcc6',width=5)=>'<path d="M'+x1+' '+y1+' L'+x2+' '+y2+'" stroke="'+color+'" stroke-width="'+width+'" fill="none" stroke-linecap="round"/>';
const circle=(x,y,r,fill='#173e53',stroke='#7ddcc6')=>'<circle cx="'+x+'" cy="'+y+'" r="'+r+'" fill="'+fill+'" stroke="'+stroke+'" stroke-width="4"/>';
const arrow=(x,y,X,Y,c='#ffca79')=>line(x,y,X,Y,c,6)+'<path d="M'+X+' '+Y+' l-17 -9 v18 Z" fill="'+c+'"/>';
const bolt=(x,y)=>'<path d="M'+x+' '+(y-54)+' l-33 70 h28 l-10 58 62 -87 h-31 l18 -41 Z" fill="#ffd17c" stroke="#eaa95c" stroke-width="3"/>';
function panel(k){
 let s='';
 if(k==='intro'){s+=circle(260,265,92,'#173f54')+bolt(260,260)+rect(430,170,300,190)+text(580,245,'SICHERHEIT',30)+text(580,300,'VOR BEGINN',25)+arrow(360,265,420,265);}
 if(k==='overview'){['AUFTRAG','PERSONAL','ARBEITSMITTEL','PSA','KONTROLLE'].forEach((v,i)=>{let x=90+i*165;s+=rect(x,180,145,150,i===0?'#28566a':'#173e53')+text(x+72,250,v,17);});s+=text(480,395,'+',45,'#ffcb79')+text(480,450,'FÜNF SICHERHEITSREGELN',24);}
 if(k==='sequence'){let labels=['FREISCHALTEN','SICHERN','PRÜFEN','ERDEN*','SCHÜTZEN'];labels.forEach((v,i)=>{let x=65+i*170;s+=circle(x+65,250,42,i===0?'#285c6b':'#173e53')+text(x+65,260,String(i+1),28)+text(x+65,330,v,16);if(i<4)s+=arrow(x+110,250,x+160,250);});s+=text(480,420,'* SOWEIT ERFORDERLICH',19,'#ffcb79');}
 if(k==='rule1'){['PV','NETZ','SPEICHER'].forEach((v,i)=>{let x=110+i*260;s+=rect(x,175,180,135)+text(x+90,250,v,25);});s+=arrow(480,330,480,390)+text(480,440,'ALLE RELEVANTEN QUELLEN',24);}
 if(k==='rule2'){s+=rect(155,185,240,150)+text(275,255,'GETRENNT',24)+rect(565,185,240,150,'#3b3437','#ffbe7b')+text(685,255,'GESICHERT',24)+line(395,260,565,260,'#ffbe7b',8)+text(480,410,'KEIN UNBEABSICHTIGTES WIEDEREINSCHALTEN',19);}
 if(k==='rule3'){s+=rect(170,170,230,190)+text(285,245,'ANNAHME',25,'#ffbd7b')+text(285,300,'≠',40)+rect(560,170,230,190,'#194d4a')+text(675,245,'NACHWEIS',25)+text(675,300,'✓',40,'#a6f1d4');}
 if(k==='rule4'){s+=circle(280,250,62)+text(280,260,'ERDEN',20)+circle(680,250,62)+text(680,260,'KURZ',18)+line(342,250,618,250,'#ffcb79',7)+text(480,390,'NUR WENN ERFORDERLICH',23,'#ffcb79');}
 if(k==='rule5'){s+=rect(185,175,260,185,'#194d4a')+text(315,250,'ARBEITSBEREICH',21)+rect(515,175,260,185,'#44383a','#ffbd7b')+text(645,250,'NACHBARFELD',21)+text(480,420,'GRENZE UND UMGEBUNG SCHÜTZEN',22);}
 if(k==='plus5'){let labels=['AUFTRAG','SCHULUNG','WERKZEUG','SCHUTZ','KONTROLLE'];labels.forEach((v,i)=>{let x=95+i*160;s+=circle(x+50,235,42)+text(x+50,245,String(i+1),25)+text(x+50,330,v,16);});}
 if(k==='order'){s+=circle(480,255,125,'#214d5d')+text(480,245,'SICHERES',27)+text(480,285,'ARBEITEN',27);['TECHNIK','ORGANISATION','FACHKUNDE'].forEach((v,i)=>{let x=120+i*280;s+=rect(x,390,190,65)+text(x+95,432,v,18);});}
 if(k==='sources'||k==='multiple'){let labels=k==='sources'?['MODULE','WECHSELRICHTER','NETZ','SPEICHER']:['PV','NETZ','BATTERIE','NOTSTROM'];labels.forEach((v,i)=>{let x=75+i*205;s+=rect(x,180,165,115)+text(x+82,245,v,20)+arrow(x+82,300,480,365);});s+=rect(350,365,260,80,'#214e60')+text(480,415,'GESAMTSYSTEM',22);}
 if(k==='modules'){for(let i=0;i<4;i++)s+=rect(120+i*145,190,120,135,'#234c70','#87c9e8')+line(135+i*145,210,225+i*145,300,'#87c9e8',2);s+=arrow(700,255,820,255,'#ffcb79')+text(480,410,'LICHT → DC-SPANNUNG',26,'#ffcb79');}
 if(k==='acdc'){s+=rect(130,170,260,170)+text(260,240,'AC-SEITE',27)+text(260,290,'AUS',30,'#ffbd7b')+rect(570,170,260,170,'#1d4a61')+text(700,240,'DC-SEITE',27)+bolt(700,290)+text(480,420,'ZWEI UNTERSCHIEDLICHE ZUSTÄNDE',21);}
 if(k==='inverter'){s+=rect(360,140,240,260,'#1d4b60')+text(480,215,'INVERTER',27)+circle(480,290,50,'#384452','#ffbf78')+text(480,300,'C',35,'#ffbf78')+text(480,455,'RESTENERGIE MÖGLICH',22,'#ffbf78');}
 if(k==='battery'){s+=rect(280,180,400,180)+rect(680,230,30,80,'#ffcb79','#ffcb79')+text(480,255,'BATTERIESPEICHER',27)+text(480,310,'EIGENE ENERGIEQUELLE',20)+bolt(480,390);}
 if(k==='arc'){s+=rect(175,180,210,180)+rect(575,180,210,180)+bolt(480,265)+line(385,270,445,270,'#ffbd79',7)+line(515,270,575,270,'#ffbd79',7)+text(480,420,'DC-LICHTBOGEN KANN ANHALTEN',22,'#ffbd79');}
 if(k==='stop'){s+=circle(480,260,120,'#783f40','#ffb0a2')+text(480,285,'STOPP',58);}
 if(k==='scenario'){s+=rect(110,180,210,170)+text(215,250,'AC AUS',25)+rect(375,180,210,170,'#214e70','#83c7e8')+text(480,250,'TAGESLICHT',21)+rect(640,180,210,170)+text(745,250,'SPEICHER',21)+text(480,425,'WAS IST NACHGEWIESEN?',22);}
 if(k==='evidence'){s+=rect(155,175,260,170)+text(285,245,'DISPLAY: AUS',22,'#ffbd79')+rect(545,175,260,170,'#194d4a')+text(675,245,'DC-ZUSTAND?',22)+text(480,420,'KEIN AUTOMATISCHER SCHLUSS',21);}
 if(k==='planning'){['AUFTRAG','ANLAGE','ROLLEN','FREIGABE'].forEach((v,i)=>{let x=105+i*190;s+=rect(x,200,155,125)+text(x+77,270,v,20);if(i<3)s+=arrow(x+155,260,x+185,260);});}
 if(k==='task'){s+=rect(170,160,620,250)+['QUELLEN','OFFENE FRAGEN','ZUSTÄNDIGKEIT','NACHWEISE'].map((v,i)=>'<text x="230" y="'+(220+i*48)+'" font-family="Arial" font-size="23" fill="#e8f5fa">□ '+v+'</text>').join('');}
 if(k==='question'){s+=circle(480,255,105)+text(480,295,'?',100,'#ffcb79');}
 if(k==='answer'){s+=circle(480,255,112,'#194d4a')+text(480,285,'NEIN',58,'#a6f1d4')+bolt(670,250);}
 return s;
}
function render(key){const d=scenes[key]||scenes.intro;return '<svg class="mc-illustration" viewBox="0 0 960 540" role="img" aria-label="'+esc(d[0]+'. '+d[1])+'"><rect width="960" height="540" rx="20" fill="#0b293e"/>'+text(480,82,d[0],d[0].length>29?25:32,'#93e7d2')+panel(d[2])+text(480,500,d[1],d[1].length>48?19:23,'#d0e5ed')+'</svg>';}
window.EFZ_MasterRenderers=window.EFZ_MasterRenderers||{};
window.EFZ_MasterRenderers['1.01-C']={render,groups:Object.fromEntries(Object.keys(scenes).map((k,i)=>[k,i<10?'SICHERHEITSREGELN':i<17?'PV-SYSTEM UND DC':i<22?'SICHERE ENTSCHEIDUNG':'LERNKONTROLLE']))};
})();