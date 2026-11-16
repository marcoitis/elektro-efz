/* Adaptive fundamentals trainer. Not a simulated official qualification exam. */
(function(){'use strict';
const pick=a=>a[Math.floor(Math.random()*a.length)];
const clean=n=>Number(n.toFixed(3));
function make(level){
 const kind=level===1?pick(['ohmI','ohmU']):level===2?pick(['ohmR','power','series']):pick(['parallel','energy','series','power']);
 let prompt='',value=0,unit='',method='';
 if(kind==='ohmI'){const R=pick([3,4,6,8,12,24]),I=pick([.5,1,2,3]),U=clean(R*I);prompt=`An einem Widerstand von ${R} Ω liegen ${U} V. Wie gross ist der Strom?`;value=I;unit='A';method=`I = U / R = ${U} V / ${R} Ω = ${I} A.`}
 else if(kind==='ohmU'){const R=pick([5,8,10,12]),I=pick([.2,.5,1,2]),U=clean(R*I);prompt=`Durch einen Widerstand von ${R} Ω fliessen ${I} A. Wie gross ist die Spannung?`;value=U;unit='V';method=`U = R · I = ${R} Ω · ${I} A = ${U} V.`}
 else if(kind==='ohmR'){const R=pick([4,6,8,12,20]),I=pick([.25,.5,1,2]),U=clean(R*I);prompt=`Bei ${U} V fliessen ${I} A. Wie gross ist der Widerstand?`;value=R;unit='Ω';method=`R = U / I = ${U} V / ${I} A = ${R} Ω.`}
 else if(kind==='power'){const U=pick([6,12,24,48]),I=pick([.25,.5,1,2]),P=clean(U*I);prompt=`Ein Kleinspannungsverbraucher benötigt ${I} A bei ${U} V. Welche elektrische Leistung wird umgesetzt?`;value=P;unit='W';method=`P = U · I = ${U} V · ${I} A = ${P} W.`}
 else if(kind==='series'){const R1=pick([2,3,6,10]),R2=pick([4,6,8,12]),I=pick([.5,1,2]),U=clean((R1+R2)*I);prompt=`Zwei Widerstände (${R1} Ω und ${R2} Ω) sind in Reihe an ${U} V angeschlossen. Wie gross ist der Strom?`;value=I;unit='A';method=`Rges = ${R1} + ${R2} = ${R1+R2} Ω; I = ${U} / ${R1+R2} = ${I} A.`}
 else if(kind==='parallel'){const R=pick([6,8,12,24]),U=pick([6,12,24]);prompt=`Zwei identische Widerstände von je ${R} Ω liegen parallel an ${U} V. Wie gross ist der Gesamtstrom?`;value=clean(U*2/R);unit='A';method=`Rges = ${R}/2 = ${R/2} Ω; I = U/Rges = ${U}/${R/2} = ${value} A.`}
 else {const P=pick([10,20,30,50,100]),h=pick([2,4,8,10]),E=clean(P*h/1000);prompt=`Ein Gerät mit ${P} W läuft ${h} Stunden. Wie viel elektrische Energie wird verbraucht?`;value=E;unit='kWh';method=`E = ${P} W · ${h} h = ${P*h} Wh = ${E} kWh.`}
 let vals=[value,clean(value*2),clean(value/2),clean(value+1)];vals=[...new Set(vals)];if(vals.length<4)vals.push(clean(value+2));vals=vals.sort(()=>Math.random()-.5);return {prompt,unit,options:vals,correct:vals.indexOf(value),explanation:method,kind,level};
}
function nextLevel(level,correct){return Math.max(1,Math.min(3,level+(correct?1:-1)))}
function summary(rows){let total=rows?.length||0,correct=(rows||[]).filter(x=>x.correct).length;return {total,correct,percent:total?Math.round(100*correct/total):0}}
window.ElektroTrainer={make,nextLevel,summary};
})();
