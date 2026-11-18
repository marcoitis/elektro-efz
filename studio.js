/* Elektro EFZ Multimedia Studio v0.9.1 · no external dependencies or network.
   All teaching slide prose is derived from previously published course data.
   Calculations are small didactic examples, NOT installation designs. */
(function(){'use strict';
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const plain=v=>String(v??'').replace(/<[^>]+>/g,'').trim();
const key=(id,norm)=>norm?'N-'+id:id;
let sayToken=0, revealed={}, inited=false;
const EXAMPLES={
 '1.02':{topic:'SI-Vorsätze',givens:'2,4 kW sollen in Watt angegeben werden.',steps:['Ein Kilowatt entspricht 1 000 Watt.','Den Wert 2,4 mit 1 000 multiplizieren.','Ergebnis: 2 400 W. Die Einheit muss zur Rechnung passen.'],check:'2,4 kW = 2 400 W, nicht 240 W.'},
 '1.03':{topic:'Ohmsches Gesetz',givens:'Ein Lernwiderstand von 60 Ω wird mit einer sicheren Modellspannung von 12 V betrieben.',steps:['Gesucht ist die Stromstärke I.','Formel: I = U / R.','Einsetzen: I = 12 V / 60 Ω = 0,2 A.','Plausibilität: Höherer Widerstand bedeutet bei gleicher Spannung weniger Strom.'],check:'I = 0,2 A. Nur für einen geeigneten Kleinspannungs-Modellkreis.'},
 '1.04':{topic:'Zwei Widerstände in Serie',givens:'R₁ = 10 Ω, R₂ = 20 Ω, Versorgung 12 V DC.',steps:['Gesamtwiderstand: Rges = R₁ + R₂ = 30 Ω.','Strom: I = U / Rges = 12 / 30 = 0,4 A.','Teilspannungen: U₁ = 4 V, U₂ = 8 V.','Kontrolle: 4 V + 8 V = 12 V.'],check:'Die Summe der Teilspannungen entspricht der Versorgungsspannung.'},
 '1.08':{topic:'Messwert überprüfen',givens:'Ein Modellkreis hat 12 V DC und einen Widerstand von 120 Ω.',steps:['Vor der Messung Stromkreis und Messaufgabe definieren.','Sollwert: I = 12 V / 120 Ω = 0,1 A.','Geeignetes Messmittel und den korrekten Anschluss wählen – nur am Kleinspannungsmodell.','Istwert und Toleranz dokumentieren; Abweichungen systematisch prüfen.'],check:'Der rechnerische Sollstrom beträgt 100 mA.'},
 '1.09':{topic:'Induktiver Blindwiderstand',givens:'Eine ideale Induktivität L = 0,10 H wird mit f = 50 Hz betrachtet.',steps:['Formel: Xₗ = 2 · π · f · L.','Einsetzen: 2 · π · 50 Hz · 0,10 H.','Ergebnis: Xₗ ≈ 31,4 Ω.','Grenze: Das Modell ignoriert den ohmschen Wicklungswiderstand.'],check:'Das ist der idealisierte induktive Blindwiderstand, kein Schutzleiternachweis.'},
 '1.10':{topic:'Elektrische Energie',givens:'Ein Verbraucher nimmt 2 kW während 3 Stunden auf.',steps:['Leistung und Zeit unterscheiden: P = 2 kW, t = 3 h.','Formel: E = P · t.','Einsetzen: 2 kW · 3 h = 6 kWh.','Die Energiemenge ist nicht mit 6 kW zu verwechseln.'],check:'E = 6 kWh.'},
 '1.12':{topic:'12-Volt-Lichtmodell',givens:'Eine 12-V-Leuchte nimmt 6 W auf (didaktische Modellannahme).',steps:['Nur ein geeignetes, strombegrenztes Lernnetzteil verwenden.','Formel: I = P / U.','Einsetzen: 6 W / 12 V = 0,5 A.','Funktion und Sicherheitsgrenzen im Planschema dokumentieren.'],check:'Modellstrom 0,5 A; keine reale Gebäudeinstallation.'},
 '2.01':{topic:'Sinusförmige Wechselspannung',givens:'Eine sinusförmige Spannung hat einen Scheitelwert von 325 V.',steps:['Für eine ideale Sinusform gilt Ueff = Û / √2.','325 V durch √2 teilen.','Ergebnis Ueff ≈ 230 V.','Achtung: Dies ist eine Rechenübung, kein Aufruf zu Messungen an Netzspannung.'],check:'Ueff ≈ 230 V.'},
 '2.02':{topic:'Symmetrisches Drehstromsystem',givens:'Ein symmetrisches Drehstromsystem hat 400 V zwischen den Aussenleitern.',steps:['Sternschaltung: Strangspannung Ustr = ULL / √3.','Einsetzen: 400 V / √3.','Ergebnis: Ustr ≈ 231 V.','Wichtig: Das gilt für die gezeigte symmetrische Sternbeziehung.'],check:'Ungefähr 230 V pro Strang in Stern.'},
 '2.03':{topic:'Idealer Transformator',givens:'N₁ = 1 000 Windungen, N₂ = 100 Windungen, U₁ = 230 V.',steps:['Ideales Übersetzungsverhältnis: U₂ / U₁ = N₂ / N₁.','N₂ / N₁ = 100 / 1 000 = 0,1.','U₂ = 230 V · 0,1 = 23 V.','In der Praxis gibt es Verluste und zusätzliche Sicherheitsanforderungen.'],check:'U₂ = 23 V im idealen Modell.'},
 '2.04':{topic:'Spannungsteiler als Sensorsignal',givens:'Zwei gleiche Widerstände mit je 10 kΩ liegen an einer sicheren Modellspannung von 5 V.',steps:['Für gleiche Widerstände teilt sich die Spannung gleichmässig.','Uaus = Uin · R₂ / (R₁ + R₂).','Uaus = 5 V · 10 / 20 = 2,5 V.','Ein belasteter Spannungsteiler kann von diesem Idealwert abweichen.'],check:'Uaus = 2,5 V unbelastet.'},
 '2.06':{topic:'Verlustleistung im Leiter (Modell)',givens:'Ein Leiter hat modellhaft 0,05 Ω Widerstand; Strom 16 A.',steps:['Spannungsfall: ΔU = I · R.','ΔU = 16 A · 0,05 Ω = 0,8 V.','Wärmeverlust: P = I² · R = 256 · 0,05 = 12,8 W.','Für reale Leitungen sind Verlegebedingungen, Temperaturen und Normanforderungen zusätzlich nötig.'],check:'ΔU = 0,8 V; P = 12,8 W – keine Leitungsfreigabe.'},
 '2.08':{topic:'Lichtstrom und Beleuchtungsstärke',givens:'Eine ideal gleichmässig beleuchtete Fläche ist 20 m² gross; Sollwert im Modell 300 lx.',steps:['Modellbeziehung: Beleuchtungsstärke E = Lichtstrom Φ / Fläche A.','Φ = E · A = 300 lx · 20 m².','Idealisiert: Φ = 6 000 lm auf der Nutzfläche.','Echte Lichtplanung berücksichtigt Leuchten, Raumgeometrie und Wartungsfaktoren.'],check:'6 000 lm ist nur der idealisierte Ausgangswert.'},
 '2.09':{topic:'Tagesenergie eines Geräts',givens:'Ein Gerät mit 2 kW läuft 30 Minuten pro Tag.',steps:['30 Minuten entsprechen 0,5 Stunden.','E = P · t = 2 kW · 0,5 h.','Ergebnis E = 1 kWh pro Tag.','Jahreswerte erfordern ein realistisches Nutzungsprofil.'],check:'E = 1 kWh pro Tag.'},
 '3.04':{topic:'Mechanische Leistung im Motor',givens:'Drehmoment 10 N·m bei 1 500 min⁻¹.',steps:['Winkelgeschwindigkeit: ω = 2π · n / 60.','ω = 2π · 1500 / 60 ≈ 157 rad/s.','Mechanische Leistung: P = M · ω.','P ≈ 10 · 157 = 1,57 kW.'],check:'Abgabeleistung rund 1,57 kW; elektrische Eingangsleistung ist bei realen Motoren höher.'},
 '3.07':{topic:'PV-Jahresertrag überschlagen',givens:'Eine Beispielanlage hat 6 kWp. Als ausdrückliche Annahme gilt 900 kWh/kWp pro Jahr.',steps:['Modellannahme und Anlagenleistung getrennt notieren.','Ertrag = 6 kWp · 900 kWh/(kWp·a).','Ergebnis: 5 400 kWh pro Jahr.','Realer Ertrag hängt von Standort, Ausrichtung, Verschattung, Verlusten und Betrieb ab.'],check:'5 400 kWh/a – eine Rechenannahme, keine Ertragsgarantie.'},
 '3.12':{topic:'Modulleistungen addieren',givens:'Acht PV-Module besitzen je 430 Wp Nennleistung.',steps:['Modulanzahl und Nennleistung multiplizieren.','8 · 430 Wp = 3 440 Wp.','Umrechnung: 3 440 Wp = 3,44 kWp.','DC-Nennleistung ist nicht gleich momentaner AC-Einspeiseleistung.'],check:'3,44 kWp DC-Nennleistung.'},
 '4.01':{topic:'Wirkleistung im symmetrischen Drehstrom',givens:'UL-L = 400 V, I = 10 A, Leistungsfaktor cos φ = 0,8.',steps:['Für symmetrische Drehstromlasten: P = √3 · U · I · cos φ.','Einsetzen: √3 · 400 V · 10 A · 0,8.','Ergebnis: P ≈ 5,54 kW.','Bei unsymmetrischen Lasten sind die Stränge getrennt zu betrachten.'],check:'P ≈ 5,54 kW.'},
 '4.03':{topic:'Ideale Ladezeit',givens:'Ein Speicher benötigt 44 kWh; die konstante Ladeleistung sei 11 kW.',steps:['Ideale Zeit: t = E / P.','Einsetzen: 44 kWh / 11 kW = 4 h.','Reale Ladeleistungen können sich ändern; Ladeverluste kommen hinzu.','Damit ist die Rechnung nur eine theoretische Untergrenze.'],check:'4 h im idealisierten Modell.'}
};
function createSlides(l,norm){
 const title=l.title, obj=norm?[`Anwendung der Quelle ${l.source}`,`Fall analysieren und begründen`,`Sicherheits- und Kompetenzgrenzen erkennen`]:l.objectives;
 const slides=[{type:'intro',eyebrow:'Lernziele und Einordnung',title,body:norm?l.lead:`Nach dieser Lektion kannst Du die folgenden Ziele anhand technischer Beispiele erklären.`,items:obj.slice(0,5),speaker:norm?l.lead:`Wir erarbeiten ${title}. Prüfe die Lernziele und notiere, was Du bereits verstanden hast.`}];
 const sections=norm?l.blocks:(window.ElektroLongSlides?.[l.id]||l.parts);
 sections.forEach((p,i)=>slides.push({type:'concept',eyebrow:`Unterrichtsteil ${i+1} von ${sections.length}`,title:p.heading,body:p.text,formula:norm?'':p.formula,slideNo:i,items:[],speaker:`${p.heading}. ${p.text}` }));
 const mid=norm?l.calculation:'';const ex=EXAMPLES[l.moduleId]||null;
 slides.push({type:'worked',eyebrow:norm?'Fachliches Denkmodell':'Nachvollziehbares Anwendungsbeispiel',title:norm?'Beispiel Schritt für Schritt':ex?ex.topic:'Fachliche Entscheidung begründen',body:norm?mid:ex?.givens||`Ausgangsfrage: ${l.quiz?.[0]?.question||l.task}`,steps:norm?[
 'Die Ausgangslage und die vorhandenen Angaben vollständig erfassen.',mid,'Die Konsequenzen für die Praxis anhand der Quelle und des Falles erklären.']:(ex?.steps||['Frage und Randbedingungen sauber erfassen.',l.quiz[0].why,'Die Begründung auf das Praxisbeispiel übertragen und offene Angaben kennzeichnen.']),
 check:norm?'Das Beispiel ist eine didaktische Einordnung, keine Installationsfreigabe.':ex?.check||'Begründe die Entscheidung mit den im Unterricht erklärten Zusammenhängen.',speaker:norm?mid:[ex?.givens,...(ex?.steps||[l.quiz[0].why]),ex?.check].filter(Boolean).join(' ')});
 slides.push({type:'practice',eyebrow:'Anwendung und Transfer',title:norm?'Fallstudie – erst entscheiden, dann vergleichen':'Dein sicherer Praxisauftrag',body:norm?l.scenario:l.task,solution:norm?l.model:`Prüfe den Auftrag anhand dieser Lernziele: ${obj.slice(0,3).join('; ')}. Dokumentiere Annahmen, einen nachvollziehbaren Lösungsweg und eine Plausibilitätskontrolle.`,speaker:norm?l.scenario:`Bearbeite den Übungsauftrag auf Papier, in einer Simulation oder an einem geeigneten Schutzkleinspannungs-Lernmodell. ${l.task}`});
 const quiz=norm?l.quiz:l.quiz;
 quiz.forEach((q,i)=>slides.push({type:'quiz',eyebrow:`Wissenskontrolle ${i+1}/${quiz.length}`,title:q.question||q.q,body:'Wähle eine Antwort. Danach erscheint die fachliche Begründung.',options:q.answers,correct:q.correct,why:q.why,qindex:i,speaker:`Kontrollfrage ${i+1}: ${q.question||q.q}` }));
 slides.push({type:'review',eyebrow:'Zusammenfassung und Transfer',title:'Verstanden oder nur wiedererkannt?',body:'Erkläre das Thema ohne Unterlagen und halte fest, welche Annahmen, Risiken und Nachweise für reale Anwendungen fehlen.',items:[`Fachlicher Kern: ${sections[0]?.heading||title}`,`Übertragung: ${norm?l.check:l.task}`,`Begrenze die Anwendung auf Papier, Simulation und geeignete sichere Lernmodelle.`],speaker:`Fasse zusammen, was Du in dieser Lektion gelernt hast. Stelle einen Zusammenhang zur Praxis her und notiere offene Fragen.`});
 return slides
}
function typeFor(l,norm){const name=[l.title,l.moduleId||'',norm?l.subject:''].join(' ').toLowerCase();
 if(/photovoltaik|pv-|wechselrichter|solarmodul|energiespeicher/.test(name))return 'pv';
 if(/sicherheit|bewilligung|personenschutz|risik|schutzkonzept|unfall|fünf sicherheitsregeln/.test(name))return 'safety';
 if(/drehstrom|dreieckschaltung|sternschaltung|drehfeld/.test(name))return 'three';
 if(/wechselstrom|sinus|frequenz|blindleistung|transformator|induktiv|kapazitiv|phasor/.test(name))return 'ac';
 if(/ohmsch|widerstand|elektrische grösse|stromkreis|stromteiler|spannungsteiler/.test(name))return 'dc';
 if(/messen|erstprüfung|fehler|diagnos|instandhaltung|prüfung/.test(name))return 'check';
 if(/bus|steuerung|regelung|knx|sensor|kommunikation|motor|signale/.test(name))return 'logic';
 if(/installation|haus|wohnung|beleuchtung|pläne|plan|schema|dokumentation/.test(name))return 'plan';
 return 'flow'
}
function diagram(l,norm){
 const id=key(l.id,norm);
 // The file is generated from the actual lecture title and learning goals, not an executable wiring diagram.
 const safeid=encodeURIComponent(id);
 const caption='Individuelle didaktische Grafik zu '+l.title+' – keine Installationsplanung';
 return `<figure class="studio-figure studio-individual-figure"><img src="./visuals/${safeid}.svg" loading="lazy" decoding="async" alt="${esc(caption)}"><figcaption>${esc(caption)}</figcaption></figure>`;
}
function reviewPanel(l,norm){
 const id=key(l.id,norm),r=window.ElektroLessonAudit?.[id];
 if(!r)return '';
 const sources=(r.references||[]).map(x=>`<li>${esc(x)}</li>`).join('');
 const gaps=(r.missing_or_followup||[]).map(x=>`<li>${esc(x)}</li>`).join('');
 const duration=Number(r.tts_minutes_estimate_130wpm||0).toFixed(1);
 const lengthStatus=r['15_to_30_minute_target']?'Skript erreicht rechnerisch 15–30 Minuten':'Skript noch kürzer als das 15-Minuten-Ziel';
 return `<details class="studio-review"><summary>Fachprüfung offen · Sprechertext ca. ${duration} Min. · Quellenstatus anzeigen</summary>
 <div class="studio-review-content"><p><strong>Prüfstatus:</strong> ${esc(r.technical_review_status)}</p>
 <p><strong>Länge:</strong> ${esc(lengthStatus)}. Berechnungsannahme: 130 Wörter/Minute, keine gemessene MP3-Dauer.</p>
 <p><strong>Zuordnung aus dem Arbeitsplan:</strong></p><ul>${sources}</ul>
 <p><strong>Noch abzuklären:</strong></p>${gaps?`<ul>${gaps}</ul>`:'<p>Keine explizite Dateilücke erkannt. Die fachliche Einzelprüfung ist trotzdem offen.</p>'}
 <p class="studio-review-caution">Die Grafik dient dem Verständnis. Sie ist weder ein normgeprüfter Schaltplan noch eine Installationsfreigabe.</p>
 </div></details>`;
}

function render(l,norm,state){const id=key(l.id,norm),slides=createSlides(l,norm),pos=Math.min(Math.max(0,+(state.studioPositions?.[id]||0)),slides.length-1),s=slides[pos],done=pos===slides.length-1,steps=s.steps||[];
 const solved=(norm?state.normQuiz?.[l.id]:state.quizAnswers?.[l.id])?.[s.qindex],answered=Number.isInteger(solved),reveal=!!revealed[id],nsteps=Math.min(steps.length,+(revealed[id+':step']||0));
 const desc=`<div class="studio-paragraph">${esc(s.body)}</div>`;
 const intro=s.type==='intro'?`<ul class="studio-objectives">${s.items.map(v=>`<li>${esc(v)}</li>`).join('')}</ul>`:'';
 const concept=s.type==='concept'?`<div class="studio-concept-grid">${diagram(l,norm)}<div class="studio-concept-text">${desc}${s.formula?`<div class="studio-formula">${esc(s.formula)}</div>`:''}<div class="studio-tip"><strong>Vertiefung</strong><p>Erkläre in eigenen Worten, wofür dieses Konzept verwendet wird und wo seine Grenzen liegen.</p></div></div></div>`:'';
 const worked=s.type==='worked'?`${desc}<div class="studio-steps">${steps.map((v,i)=>`<div class="studio-step ${i<nsteps?'visible':''}"><span class="studio-count">${i+1}</span><p>${i<nsteps?esc(v):'Schritt noch verdeckt – zuerst selbst überlegen.'}</p></div>`).join('')}</div><div class="studio-actions">${nsteps<steps.length?`<button type="button" class="btn teal" data-st="step">Nächsten Schritt zeigen (${nsteps+1}/${steps.length})</button>`:`<div class="studio-success">Alle Schritte sind eingeblendet.</div>`}<button type="button" class="btn" data-st="steps-reset">Rechenweg zurücksetzen</button></div>${nsteps===steps.length?`<p class="studio-conclusion">${esc(s.check)}</p>`:''}`:'';
 const practice=s.type==='practice'?`${desc}<div class="studio-prompt">Bevor Du die Musterlösung ansiehst: Welche Randbedingungen fehlen? Welche Annahmen machst Du? Wie prüfst Du Dein Ergebnis?</div><label class="studio-notelabel">Mein Lösungsansatz<textarea class="studio-input" data-st-note placeholder="Eigene Entscheidung, Rechnung, Annahmen und offene Fragen …">${esc(state.studioNotes?.[id]||'')}</textarea></label><button type="button" class="btn teal" data-st="reveal">${reveal?'Musterlösung ausblenden':'Musterlösung und Prüfkriterien anzeigen'}</button>${reveal?`<div class="studio-solution"><strong>Begründete Musterlösung / Beurteilungskriterien</strong><p>${esc(s.solution)}</p></div>`:''}`:'';
 const quiz=s.type==='quiz'?`${desc}<div class="studio-options">${s.options.map((v,i)=>`<button type="button" class="studio-option ${answered?(i===s.correct?'correct':i===solved?'wrong':''):''}" data-st-answer="${i}"><span>${'ABCD'[i]||i+1}</span>${esc(v)}</button>`).join('')}</div>${answered?`<div class="studio-feedback"><strong>${solved===s.correct?'Richtig':'Noch nicht richtig'}.</strong> ${esc(s.why)}</div>`:''}`:'';
 const review=s.type==='review'?`${desc}<ul class="studio-objectives">${s.items.map(v=>`<li>${esc(v)}</li>`).join('')}</ul><div class="studio-safe">Das Bestehen digitaler Lernkontrollen ersetzt keine unter Aufsicht nachgewiesene Praxis oder behördliche Bewilligung.</div>`:'';
 const label=s.type==='concept'?'Fachtext':s.type==='worked'?'Schrittfolge':s.type==='quiz'?'Verständnisprüfung':s.type==='practice'?'Praxisfall':'Lernabschnitt';
 return `<section class="studio-root" data-studio="${esc(id)}" aria-label="Multimedialer Unterricht">${reviewPanel(l,norm)}<div class="studio-top"><div><div class="eyebrow">Multimedialer Unterricht · ${esc(label)}</div><h2>Foliensatz: ${esc(l.title)}</h2></div><span class="studio-counter">${pos+1} / ${slides.length}</span></div><div style="margin:10px 0 16px"><a href="./kurskompass.html#${encodeURIComponent(id)}" class="btn" style="display:inline-block;text-decoration:none">▤ Individuelle Unterrichtsmappe öffnen</a></div><div class="studio-track"><span style="width:${(pos+1)*100/slides.length}%"></span></div><article class="studio-screen"><div class="studio-slide-heading"><span>${esc(s.eyebrow)}</span><h3>${esc(s.title)}</h3></div>${s.type==='intro'?desc+intro:''}${concept}${worked}${practice}${quiz}${s.type==='review'?review:''}</article><div class="studio-controls"><button class="btn" type="button" data-st="prev" ${pos===0?'disabled':''}>← Zurück</button><button class="btn" type="button" data-st="speak">▶ Folie vorlesen</button><button class="btn" type="button" data-st="stop">■ Stopp</button><button class="btn teal" type="button" data-st="next" ${done?'disabled':''}>Weiter →</button></div><p class="studio-note">Gesprochene Folie: Gerätestimme (abhängig vom Gerät). Separat gespeicherte Thorsten-MP3s bleiben erhalten, sind aber nicht automatisch mit neuen Folien synchron. Die Fachtexte und Grafiken funktionieren offline.</p><nav class="studio-dots" aria-label="Folien direkt aufrufen">${slides.map((v,i)=>`<button type="button" data-st-goto="${i}" class="${i===pos?'active':''}" aria-label="Folie ${i+1}: ${esc(v.eyebrow)}" title="Folie ${i+1}: ${esc(v.eyebrow)}">${i+1}</button>`).join('')}</nav></section>`;
}
function halt(){sayToken++;try{window.speechSynthesis?.cancel()}catch(_){} }
function bind(state,actions){const root=document.querySelector('.studio-root');if(!root)return;const id=root.dataset.studio,norm=id.startsWith('N-');const l=norm?window.ElektroNormCourse.lessons.find(x=>'N-'+x.id===id):window.ELEKTRO_DATA.lessons.find(x=>x.id===id);if(!l)return;const slides=createSlides(l,norm);const current=()=>Math.min(slides.length-1,Math.max(0,+(state.studioPositions[id]||0)));const rerender=()=>{actions.save();actions.render()};
 root.querySelectorAll('[data-st-goto]').forEach(b=>b.addEventListener('click',()=>{halt();state.studioPositions[id]=+b.dataset.stGoto;rerender()}));
 root.querySelectorAll('[data-st]').forEach(b=>b.addEventListener('click',()=>{const action=b.dataset.st;
 if(action==='prev'||action==='next'){halt();state.studioPositions[id]=Math.max(0,Math.min(slides.length-1,current()+(action==='next'?1:-1)));rerender();return}
 if(action==='step'){revealed[id+':step']=Math.min(slides[current()].steps.length,(revealed[id+':step']||0)+1);actions.render();return}
 if(action==='steps-reset'){revealed[id+':step']=0;actions.render();return}
 if(action==='reveal'){revealed[id]=!revealed[id];actions.render();return}
 if(action==='stop'){halt();b.textContent='■ Gestoppt';return}
 if(action==='speak'){halt();const s=slides[current()];if(!('speechSynthesis'in window)){alert('Die Gerätestimme ist in diesem Browser nicht verfügbar. Die bestehenden MP3s können weiterhin abgespielt werden.');return}const tok=++sayToken;const utter=new SpeechSynthesisUtterance(plain(s.speaker||[s.title,s.body].join('. ')));utter.lang='de-CH';utter.rate=Number(state.settings?.rate)||1;const v=window.speechSynthesis.getVoices().find(v=>/^de-CH/i.test(v.lang))||window.speechSynthesis.getVoices().find(v=>/^de/i.test(v.lang));if(v)utter.voice=v;utter.onend=()=>{if(tok===sayToken){const play=root.querySelector('[data-st="speak"]');if(play)play.textContent='▶ Nochmals vorlesen'}};window.speechSynthesis.speak(utter);b.textContent='▶ Wiedergabe läuft';return}
 }));
 root.querySelectorAll('[data-st-answer]').forEach(b=>b.addEventListener('click',()=>{const q=slides[current()].qindex,j=+b.dataset.stAnswer;if(norm){state.normQuiz[l.id]??={};state.normQuiz[l.id][q]=j;rerender()}else actions.recordQuiz(q,j)}));
 root.querySelector('[data-st-note]')?.addEventListener('input',e=>{state.studioNotes[id]=e.target.value.slice(0,15000);actions.save()});
}
window.ElektroStudio={renderRegular:(l,s)=>render(l,false,s),renderNorm:(l,s)=>render(l,true,s),bind,halt,createSlides,examples:EXAMPLES};
})();
