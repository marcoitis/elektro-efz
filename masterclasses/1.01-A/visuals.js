/* Elektro EFZ · 1.01-A · individually directed visual scenes.
   Distinguishes technical qualification, responsibility and NIV authorisation.
   This is diagrammatic education, not advice on performing electrical work.
   Source: tts_scripts/1.01-A.txt; ESTI/BFE NIV guidance.
*/
(function(){'use strict';
const C={ink:'#eef8fc',muted:'#a8c6d7',mint:'#85ebc9',blue:'#82c6ee',gold:'#ecc58b',red:'#f0aa9d',panel:'#143b51',border:'#467587'};
const esc=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const t=(x,y,label,size=26,color=C.ink,weight=650,anchor='middle')=>'<text x="'+x+'" y="'+y+'" text-anchor="'+anchor+'" fill="'+color+'" font-size="'+size+'" font-family="-apple-system,Arial,sans-serif" font-weight="'+weight+'">'+esc(label)+'</text>';
const rect=(x,y,w,h,fill=C.panel,stroke=C.border,r=16)=>'<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="'+r+'" fill="'+fill+'" stroke="'+stroke+'" stroke-width="1.7"/>';
const line=(d,color=C.mint,width=4,extra='')=>'<path d="'+d+'" stroke="'+color+'" stroke-width="'+width+'" fill="none" stroke-linecap="round" stroke-linejoin="round" '+extra+'/>';
const pill=(x,y,s,accent=C.mint)=>rect(x-97,y-30,194,51,'#173e51',accent,13)+t(x,y+4,s,18);
const svg=(art,desc)=>'<svg class="mc-illustration" viewBox="0 0 960 540" role="img" aria-label="'+esc(desc)+'">'+
 '<defs><marker id="e-arrow" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto"><path d="M0 0 L9 5 L0 10z" fill="'+C.mint+'"/></marker>'+
 '<linearGradient id="e-grad" x1="0" x2="1"><stop offset="0%" stop-color="#225b6c"/><stop offset="100%" stop-color="#318a84"/></linearGradient></defs>'+art+'</svg>';
const headings={
 intro:'DREI BEGRIFFE – DREI FRAGEN',ladder:'DREI VERSCHIEDENE EBENEN',
 efz:'EIDGENÖSSISCHES FÄHIGKEITSZEUGNIS',skills:'AUSBILDUNG',
 practice:'PRAXIS UND AUFSICHT',responsibility:'VERANTWORTUNGSKETTE',
 niv:'RECHTLICHER RAHMEN',permit:'BEWILLIGUNGSPFLICHT',
 esti:'ZUSTÄNDIGE STELLE',person:'BEWILLIGUNG FÜR PERSONEN',
 company:'BEWILLIGUNG FÜR BETRIEBE',limits:'BEGRENZTE BEWILLIGUNGEN',
 pv:'BEISPIEL PHOTOVOLTAIK',exception:'GESETZLICHE AUSNAHMEN',
 exception2:'WICHTIGE NUANCE',owner:'EIGENTUM IST NICHT BEWILLIGUNG',
 scope:'AUFTRAG ZUERST KLÄREN',safe:'SICHERHEIT GEHT VOR',
 decision:'ENTSCHEIDUNGSWEG',responsible:'ROLLEN ZUORDNEN',
 summary:'WAS GEHÖRT ZUSAMMEN?',question:'LERNKONTROLLE',answer:'LERNKONTROLLE',
 closing:'KERNBOTSCHAFT'
};
const group={
 intro:'EINSTIEG',ladder:'EINSTIEG',efz:'AUSBILDUNG',skills:'AUSBILDUNG',
 practice:'BERUFSPRAXIS',responsibility:'VERANTWORTUNG',niv:'NIV',
 permit:'NIV',esti:'NIV',person:'BEWILLIGUNGEN',company:'BEWILLIGUNGEN',
 limits:'BEWILLIGUNGEN',pv:'BEWILLIGUNGEN',exception:'AUSNAHMEN',
 exception2:'AUSNAHMEN',owner:'AUSNAHMEN',scope:'PRAXISBEISPIEL',
 safe:'SICHERHEIT',decision:'SICHERHEIT',responsible:'SICHERHEIT',
 summary:'ZUSAMMENFASSUNG',question:'LERNKONTROLLE',answer:'LERNKONTROLLE',
 closing:'ABSCHLUSS'
};
function top(k){return t(480,106,headings[k]||'ELEKTRO EFZ',25,C.mint,790)}
function trio(k){
 const stages=[['AUSBILDUNG','Kompetenz','EFZ'],['BERUFSPRAXIS','Erfahrung','Anleitung'],['BERECHTIGUNG','Rechtlicher Rahmen','NIV']];
 const focus=({efz:0,skills:0,practice:1,responsibility:1,permit:2,niv:2,ladder:3,intro:3,summary:3,closing:3})[k]??3;
 let a=top(k);
 stages.forEach(([name,sub,last],i)=>{
  const x=70+i*293,focusOn=i===focus||focus===3;
  const fill=focusOn?'#164e5a':'#113247',stroke=focusOn?C.mint:'#54718a';
  a+=rect(x,162,236,216,fill,stroke,20);
  a+=t(x+118,211,String(i+1).padStart(2,'0'),37,focusOn?C.mint:C.muted,780);
  a+=line('M'+(x+74)+' 234 H'+(x+162),focusOn?C.mint:C.border,3);
  a+=t(x+118,282,name,23,C.ink,780);
  a+=t(x+118,329,sub,21,C.muted,520);
  a+=t(x+118,354,last,17,focusOn?C.mint:C.muted,550);
  if(i<2)a+=line('M'+(x+240)+' 270 H'+(x+284),C.muted,3);
 });
 a+=t(480,457,'Nicht automatisch gleichgestellt',22,C.gold,650);
 return svg(a,'Ausbildung, Berufspraxis und rechtliche Berechtigung bilden drei getrennte Ebenen');
}
function diploma(k){
 let a=top(k);
 a+=rect(234,144,492,286,'#14394f','#75b9c9',25);
 a+=line('M300 215 H659',C.border,2);
 a+=t(480,217,'EFZ',77,C.ink,790);
 a+=t(480,291,'Anerkannter Berufsabschluss',26,C.muted,590);
 a+=line('M327 325 H633',C.mint,3);
 a+=t(480,382,k==='skills'?'Wissen · Sicherheit · Fachkompetenz':'Qualifikation ≠ pauschale Bewilligung',23,k==='skills'?C.mint:C.gold);
 a+=line('M692 164 L717 192 L687 212',C.mint,5);
 return svg(a,'Ein EFZ-Zeugnis bestätigt berufliche Qualifikation, nicht automatisch alle Installationsberechtigungen');
}
function supervision(k){
 let a=top(k);
 const cols=[['AUSFÜHRUNG','Fachlich zugewiesen'],['AUFSICHT','Fachlich geleitet'],['KONTROLLE','Verantwortlich geprüft']];
 cols.forEach(([title,sub],i)=>{
  const x=64+i*300;
  a+=rect(x,173,247,211,i===1?'#164c56':'#13384d',i===1?C.mint:C.border,18);
  a+='<circle cx="'+(x+123)+'" cy="239" r="26" fill="none" stroke="'+C.blue+'" stroke-width="4"/>';
  a+=line('M'+(x+70)+' 316 Q'+(x+121)+' 270 '+(x+176)+' 316',C.blue,4);
  a+=t(x+123,349,title,22,C.ink,730);
  a+=t(x+123,374,sub,15,C.muted,490);
  if(i<2)a+=line('M'+(x+252)+' 275 H'+(x+292),C.mint,3,'marker-end="url(#e-arrow)"');
 });
 a+=t(480,463,'Rollen und Zuständigkeiten vor Beginn klären',22,C.mint);
 return svg(a,'Ausführung, fachkundige Aufsicht und erforderliche Kontrolle haben unterschiedliche Rollen');
}
function niv(k){
 let a=top(k);
 a+=rect(91,142,448,292,'#13394e','#71bdbb',21);
 a+=t(310,228,'NIV',91,C.ink,800);
 a+=t(310,284,'SR 734.27',28,C.mint,730);
 a+=t(310,339,'Niederspannungs-',23,C.muted);
 a+=t(310,369,'Installationsverordnung',23,C.muted);
 a+=rect(588,166,276,81,'#194f57',C.mint,13);
 a+=t(726,217,'Arbeit',28,C.ink);
 a+=rect(588,270,276,81,'#194f57',C.mint,13);
 a+=t(726,321,'Bewilligung',28,C.ink);
 a+=line('M546 297 H575',C.mint,4,'marker-end="url(#e-arrow)"');
 return svg(a,'Niederspannungs-Installationsverordnung regelt Installationsarbeiten, Bewilligungen und Kontrollen');
}
function permit(k){
 let a=top(k);
 a+=rect(91,203,319,161,'#13384d',C.border,19)+t(251,258,'Technisches Können',26,C.ink)+t(251,316,'allein ≠ Erlaubnis',25,C.gold);
 a+=rect(539,176,332,213,'#12515b',C.mint,19);
 a+=t(705,235,'Berechtigung prüfen',27,C.ink,760);
 a+=t(705,289,'Tätigkeit · Person',20,C.muted);
 a+=t(705,327,'Anlage · Umfang',20,C.muted);
 a+=line('M431 282 H513',C.mint,6,'marker-end="url(#e-arrow)"');
 return svg(a,'Vor bewilligungspflichtigen Arbeiten sind konkrete Tätigkeit, Person und Berechtigung zu prüfen');
}
function esti(){
 let a=top('esti');
 a+=rect(100,166,760,221,'#154456','#70b9bc',22);
 a+=t(480,247,'ESTI',76,C.ink,810);
 a+=t(480,302,'Eidgenössisches Starkstrominspektorat',29,C.muted,550);
 a+=t(480,358,'Bewilligungen prüfen und erteilen',27,C.mint);
 return svg(a,'Das Eidgenössische Starkstrominspektorat prüft und erteilt gesetzliche Installationsbewilligungen');
}
function variants(k){
 const data={
 person:['NATÜRLICHE PERSON','Allgemeine Bewilligung','Fachkundigkeit nach NIV','Art. 7 und 8 NIV'],
 company:['BETRIEB','Allgemeine Bewilligung','Fachkundige Leitung','Art. 9 und 10 NIV'],
 limits:['BESONDERE TÄTIGKEIT','Eingeschränkte Bewilligung','Nur für definierten Bereich','NIV Art. 12 ff.'],
 pv:['PHOTOVOLTAIK','Anlagen mit Spezialkenntnissen','Bewilligungsumfang prüfen','Art. 14 NIV']
 };
 let d=data[k],a=top(k);
 a+=rect(145,149,670,272,'#154457','#7ecec5',22);
 a+=t(480,221,d[0],42,C.ink,780);
 a+=line('M272 245 H688',C.mint,3);
 a+=t(480,297,d[1],30,C.ink,660);
 a+=t(480,345,d[2],23,C.muted,550);
 a+=t(480,398,d[3],22,C.mint,730);
 if(k==='pv'){
  a+=line('M100 213 L100 295 L141 295',C.blue,3);
  a+=line('M93 214 H140 L154 240 H107 Z',C.blue,3);
 }
 return svg(a,'Bewilligungsart und Geltungsbereich nach NIV unterscheiden: '+d[1]);
}
function exception(k){
 let a=top(k);
 a+=rect(123,145,714,275,'#163d50','#8ddfc8',22);
 a+=t(480,230,'NIV · Artikel 16',49,C.ink,800);
 a+=t(480,292,k==='exception'?'Gesetzlich geregelte Ausnahmen':'EFZ und eigene Wohnräume?',32,C.mint,680);
 a+=t(480,353,k==='exception'?'Nur innerhalb genau definierter Bedingungen':'Ausnahme möglich – Voraussetzungen prüfen',24,C.muted);
 a+=line('M235 388 H725',C.border,2);
 return svg(a,'Artikel 16 NIV sieht konkrete Ausnahmen von der Installationsbewilligungspflicht vor');
}
function property(){
 let a=top('owner');
 a+=line('M221 247 L353 154 L485 247',C.blue,8)+line('M264 243 V375 H442 V243',C.blue,7);
 a+=rect(304,302,83,73,'#15445b','#83aabd',7);
 a+=t(354,422,'Eigentum',30,C.ink,730);
 a+=t(556,284,'≠',78,C.gold,750);
 a+=rect(671,173,171,180,'#143e52','#8dd9c9',20);
 a+=t(756,243,'Rechtliche',23,C.ink);
 a+=t(756,284,'Erlaubnis',23,C.ink);
 a+=t(756,325,'prüfen',21,C.mint);
 return svg(a,'Eigentum an einer elektrischen Anlage ersetzt keine Prüfung der gesetzlichen Berechtigung');
}
function job(k){
 let a=top(k);
 a+=rect(73,147,330,284,'#13364a',C.border,18);
 a+=t(238,205,'AUFTRAG',27,C.mint,780);
 a+=rect(185,238,105,145,'#23566a','#9ac2d0',12);
 a+=t(238,318,'?',72,C.ink,750);
 a+=rect(492,167,392,81,'#174456',C.blue,15)+t(689,220,'Welche Installation?',26,C.ink);
 a+=rect(492,263,392,81,'#174456',C.blue,15)+t(689,315,'Wer ist zuständig?',26,C.ink);
 a+=rect(492,359,392,73,'#174456',C.gold,15)+t(689,406,'Welche Berechtigung?',25,C.ink);
 return svg(a,'Ein scheinbar einfacher Steckdosenauftrag erfordert zuerst Klärung von Art, Zuständigkeit und Berechtigung');
}
function stop(){
 let a=top('safe');
 a+='<polygon points="380,145 580,145 704,269 704,383 580,485 380,485 256,383 256,269" fill="#713e43" stroke="'+C.red+'" stroke-width="9"/>';
 a+=t(480,346,'STOP',85,C.ink,840);
 a+=t(480,519,'Unklarer Auftrag → fachkundig klären lassen',21,C.muted);
 return svg(a,'Stoppen ist korrekt, wenn die Arbeit, Zuständigkeit oder sichere Ausführung unklar ist');
}
function decision(){
 let a=top('decision');
 const items=[['1','Tätigkeit','bestimmen'],['2','Berechtigung','prüfen'],['3','Sicherheit','planen'],['4','Ausführung','organisieren']];
 items.forEach(([n,w,sub],i)=>{
  const x=35+i*237;
  a+=rect(x,187,206,193,'#144559','#7ac9c5',18)+t(x+103,239,n,39,C.mint,760)+t(x+103,289,w,21,C.ink,720)+t(x+103,324,sub,19,C.muted);
  if(i<3)a+=line('M'+(x+209)+' 286 H'+(x+233),C.mint,3,'marker-end="url(#e-arrow)"');
 });
 a+=t(480,448,'Nicht ohne Klärung losarbeiten',23,C.gold);
 return svg(a,'Vier Schritte der Sicherheitsentscheidung: Tätigkeit, Berechtigung, Sicherheit, Ausführung');
}
function review(k){
 const levels=[['EFZ','Abschluss'],['PRAXIS','Erfahrung'],['NIV','Berechtigung']];
 let a=top(k);
 levels.forEach(([name,sub],i)=>{
  const x=72+i*295;
  a+=rect(x,179,244,194,'#14475a','#6fcfc2',20);
  a+=t(x+122,245,name,40,C.ink,790);
  a+=line('M'+(x+45)+' 265 H'+(x+199),C.border,3);
  a+=t(x+122,313,sub,23,C.muted);
 });
 a+=t(480,450,'Drei verschiedene Antworten – keine automatische Gleichsetzung',20,C.gold);
 return svg(a,'Ausbildung, Berufspraxis und rechtliche Installationsberechtigung müssen getrennt beurteilt werden');
}
function question(k){
 let a=top(k);
 a+=rect(76,166,808,257,'#163b51','#65bcbb',22);
 a+=t(480,246,'EFZ',73,C.ink,810);
 a+=t(480,311,'= automatische',31,C.muted);
 a+=t(480,372,'allgemeine Bewilligung?',40,C.ink,700);
 return svg(a,'Lernkontrolle: Führt das EFZ allein zu einer allgemeinen Installationsbewilligung?');
}
function answer(){
 let a=top('answer');
 a+=t(480,240,'NEIN',102,C.gold,850);
 a+=t(480,318,'EFZ allein genügt nicht.',38,C.ink,710);
 a+=line('M278 353 H682',C.mint,4);
 a+=t(480,404,'NIV-Ausnahmen, z. B. Art. 16, separat prüfen.',24,C.muted);
 return svg(a,'Antwort: Nein, das EFZ allein erteilt keine allgemeine Bewilligung; Ausnahmen separat prüfen');
}
function render(v){
 if(['intro','ladder','efz','skills','practice','responsibility','summary','closing'].includes(v)){
  if(v==='efz'||v==='skills')return diploma(v);
  if(v==='responsibility'||v==='practice')return supervision(v);
  return trio(v);
 }
 if(v==='niv')return niv(v);
 if(v==='permit')return permit(v);
 if(v==='esti')return esti();
 if(['person','company','limits','pv'].includes(v))return variants(v);
 if(['exception','exception2'].includes(v))return exception(v);
 if(v==='owner')return property();
 if(v==='scope')return job(v);
 if(v==='safe')return stop();
 if(v==='decision'||v==='responsible')return decision();
 if(v==='question')return question(v);
 if(v==='answer')return answer();
 return trio('intro');
}
window.EFZ_MasterRenderers=window.EFZ_MasterRenderers||{};
window.EFZ_MasterRenderers['1.01-A']={render,groups:group};
})();