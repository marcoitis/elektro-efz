/* Individuelle schematische Unterrichtsgrafiken – keine Arbeitsfreigabe. */
(function(){'use strict';
const scenes={
"intro":["DREI ELEKTRISCHE GEFAHREN","shock,arc,heat","Körperstrom · Lichtbogen · Überhitzung"],
"sources":["WANN ENTSTEHT GEFAHR?","source","Quelle + Zugang + Exposition"],
"shock":["KÖRPERDURCHSTRÖMUNG","person","Stromweg durch den Körper"],
"path":["STROMWEG","paths","Hand–Hand und Hand–Fuss unterscheiden"],
"duration":["EINWIRKDAUER","time","Dauer beeinflusst die Folgen"],
"conditions":["KONTAKTBEDINGUNGEN","wet","Feuchte und Kontaktfläche sind relevant"],
"noformula":["MODELL IST KEINE FREIGABE","formula","U = R · I ist kein Sicherheitsnachweis"],
"arc":["LICHTBOGEN","arc","Hitze · Strahlung · Druck"],
"distance":["GEFAHR OHNE BERÜHRUNG","arc-distance","Ein Lichtbogen kann auf Distanz verletzen"],
"heat":["THERMISCHE ÜBERLASTUNG","heat","Übergangswiderstand und Erwärmung"],
"comparison":["SCHADENSMECHANISMEN","comparison","Drei unterschiedliche Wirkungen"],
"protection":["MEHRERE SCHUTZEBENEN","layers","Technik · Organisation · Fachkunde"],
"barriers":["GEHÄUSE ALS BARRIERE","barrier","Abdeckung entfernt: Gefährdung verändert"],
"not_off":["STILLSTAND ≠ SPANNUNGSFREI","storage","Restenergie und Fremdeinspeisung"],
"pv":["PV: DC-QUELLE BLEIBT","pv","AC-Schalter allein reicht nicht"],
"devices":["SCHUTZGERÄTE","devices","Unterschiedliche Schutzaufgaben"],
"model":["ENERGIE IM LERNMODELL","energy","20 W × 30 s = 600 J"],
"timeenergy":["ENERGIE STEIGT MIT ZEIT","graph","E = P · t bei konstanter Leistung"],
"scenario":["OFFENE VERTEILUNG","cabinet","Unbekannte Einspeisungen"],
"stop":["SICHERE ENTSCHEIDUNG","stop","Nicht berühren · Arbeit unterbrechen"],
"assessment":["BEOBACHTUNG ≠ NACHWEIS","evidence","Vermutung ersetzt keine Prüfung"],
"recap":["DIE WICHTIGSTEN FAKTOREN","recap","Stromweg · Zeit · Energie · Barrieren"],
"question":["LERNKONTROLLE","question","Dunkle Anzeige = spannungsfrei?"],
"answer":["ANTWORT: NEIN","answer","Stillstand beweist keine Spannungsfreiheit"]
};
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const line=(x1,y1,x2,y2,c='#80ddc9',w=5)=>'<path d="M'+x1+' '+y1+' L'+x2+' '+y2+'" stroke="'+c+'" stroke-width="'+w+'" fill="none" stroke-linecap="round"/>';
const rect=(x,y,w,h,c='#173f54',stroke='#80ddc9')=>'<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="13" fill="'+c+'" stroke="'+stroke+'" stroke-width="3"/>';
const circle=(x,y,r,c='#173f54',stroke='#80ddc9')=>'<circle cx="'+x+'" cy="'+y+'" r="'+r+'" fill="'+c+'" stroke="'+stroke+'" stroke-width="4"/>';
const txt=(x,y,t,size=26,c='#e8f5fa')=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" font-family="Arial,sans-serif" font-size="'+size+'" font-weight="700" fill="'+c+'">'+esc(t)+'</text>';
const bolt=(x,y)=>'<path d="M'+x+' '+(y-65)+' l-34 72 h28 l-13 66 64-90 h-31 l20-48 Z" fill="#ffd17d" stroke="#f4aa53" stroke-width="3"/>';
const person=(x,y)=>circle(x,y-92,24,'#284c61')+line(x,y-66,x,y+55)+line(x,y-24,x-62,y+15)+line(x,y-24,x+62,y+15)+line(x,y+55,x-44,y+123)+line(x,y+55,x+44,y+123);
const arrow=(x1,y1,x2,y2,c='#f4c36e')=>line(x1,y1,x2,y2,c,5)+'<path d="M'+x2+' '+y2+' l-15 -8 v16 Z" fill="'+c+'"/>';
const power=()=>rect(130,175,140,160)+txt(200,245,'QUELLE',22)+bolt(200,290)+line(270,255,370,255)+rect(370,205,180,100)+txt(460,264,'ZUGANG',24)+line(550,255,655,255)+person(755,260);
function graphic(type){
 let s='';
 if(type==='person'||type==='paths'||type==='wet'){s+=person(480,255)+bolt(325,265);if(type==='paths'){s+=line(418,270,542,270,'#f5b66f',7)+line(418,270,436,378,'#f5b66f',7);}else if(type==='wet'){s+=circle(645,240,45,'#16485c')+txt(645,250,'H₂O',24);}else{s+=line(355,270,420,270,'#f5b66f',7);}}
 else if(type==='source')s+=power();
 else if(type==='shock,arc,heat'||type==='comparison'){s+=person(250,245)+bolt(250,245)+bolt(480,265)+rect(620,215,170,105)+txt(705,275,'WÄRME',24);}
 else if(type==='arc'||type==='arc-distance'){s+=rect(175,175,150,185)+rect(640,175,150,185)+bolt(480,270);s+=line(325,270,415,270,'#ffbd70',6)+line(545,270,640,270,'#ffbd70',6);if(type==='arc-distance')s+=person(830,245);}
 else if(type==='heat'){s+=line(170,270,790,270,'#9fc8df',22)+circle(480,270,55,'#7b3c30','#ffb36b')+txt(480,280,'HOT',22);}
 else if(type==='time'||type==='graph'){s+=line(195,360,780,360)+line(195,360,195,165);s+='<path d="M200 352 Q430 320 750 180" stroke="#ffbf70" stroke-width="8" fill="none"/>'+txt(770,405,'ZEIT',23)+txt(150,165,type==='graph'?'E':'RISIKO',22);}
 else if(type==='formula'||type==='energy'){s+=rect(230,170,500,185)+txt(480,255,type==='formula'?'U = R · I':'E = P · t',55)+txt(480,320,type==='formula'?'KEINE FREIGABE':'600 J',30,'#ffcf7b');}
 else if(type==='layers'){for(let i=0;i<3;i++){s+=rect(210+i*35,170+i*64,470-i*70,54,i===0?'#225366':'#163d51')+txt(445,205+i*64,['TECHNIK','ORGANISATION','FACHKUNDE'][i],24);}}
 else if(type==='barrier'){s+=rect(185,170,220,190)+rect(560,170,220,190,'#382e35','#ffbd78')+bolt(670,260)+txt(295,400,'GESCHLOSSEN',22)+txt(670,400,'OFFEN',22);}
 else if(type==='storage'){s+=rect(185,175,250,175)+txt(310,255,'STOPP',33)+rect(550,175,220,175)+bolt(660,260)+txt(660,400,'RESTENERGIE',22);}
 else if(type==='pv'){for(let i=0;i<3;i++)s+=rect(100+i*115,185,100,115,'#244f70','#79bde1');s+=line(440,250,565,250,'#ffbe6f',7)+rect(565,195,170,110)+txt(650,255,'INVERTER',22)+txt(335,365,'DC',30,'#ffbe6f');}
 else if(type==='devices'){s+=rect(180,175,260,175)+rect(525,175,260,175)+txt(310,250,'LS',45)+txt(655,250,'RCD',45)+txt(310,300,'ÜBERSTROM',21)+txt(655,300,'FEHLERSTROM',21);}
 else if(type==='cabinet'){s+=rect(330,145,300,235,'#253a4b','#ffbb77')+line(480,145,480,380,'#ffbb77')+bolt(480,260)+txt(480,415,'UNBEKANNTER ZUSTAND',21);}
 else if(type==='stop'){s+=circle(480,270,112,'#813d3c','#ffb0a2')+txt(480,288,'STOP',64);}
 else if(type==='evidence'){s+=rect(190,175,260,165)+rect(515,175,260,165)+txt(320,255,'VERMUTET',24)+txt(645,255,'GEPRÜFT?',24)+txt(480,400,'≠',44,'#ffcf7b');}
 else if(type==='recap'){s+=person(260,260)+bolt(475,270)+rect(635,205,150,130)+txt(710,275,'SCHUTZ',22);}
 else if(type==='question'){s+=rect(300,170,360,185)+txt(480,280,'?',115,'#ffce7b');}
 else if(type==='answer'){s+=circle(480,260,110,'#234e4e')+txt(480,286,'NEIN',66,'#a6f3d2');}
 return s;
}
function render(key){
 const d=scenes[key]||scenes.intro;
 return '<svg class="mc-illustration" viewBox="0 0 960 540" role="img" aria-label="'+esc(d[0]+'. '+d[2])+'"><rect width="960" height="540" rx="20" fill="#0b293e"/>'+txt(480,90,d[0],d[0].length>27?27:33,'#93e7d2')+graphic(d[1])+txt(480,480,d[2],d[2].length>43?21:25,'#d0e5ed')+'</svg>';
}
window.EFZ_MasterRenderers=window.EFZ_MasterRenderers||{};
window.EFZ_MasterRenderers['1.01-B']={render,groups:Object.fromEntries(Object.keys(scenes).map((k,i)=>[k,i<7?'KÖRPERSTROM':i<11?'LICHTBOGEN UND BRAND':i<18?'SCHUTZ':i<22?'ENTSCHEIDUNG':'LERNKONTROLLE']))};
})();
