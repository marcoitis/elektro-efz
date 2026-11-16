/* Kleinspannungs-Lernsimulation with linear resistors, NOT a safety design tool. */
(function(){'use strict';
function solve(U,R1,R2,mode='series'){
 U=Math.max(1,Math.min(24,Number(U)||12));R1=Math.max(1,Math.min(500,Number(R1)||10));R2=Math.max(1,Math.min(500,Number(R2)||20));
 const R=mode==='parallel'?1/(1/R1+1/R2):R1+R2,I=U/R;
 const I1=mode==='parallel'?U/R1:I,I2=mode==='parallel'?U/R2:I;
 return {U,R1,R2,mode,R,I,I1,I2,U1:I1*R1,U2:I2*R2,P:U*I,check:mode==='series'?`U₁ + U₂ = ${(I1*R1).toFixed(2)} V + ${(I2*R2).toFixed(2)} V = ${U} V`:`I₁ + I₂ = ${I1.toFixed(3)} A + ${I2.toFixed(3)} A = ${I.toFixed(3)} A`};
}
function diagram(v){const parallel=v.mode==='parallel';return `<svg viewBox="0 0 640 290" class="circuit-svg" role="img" aria-label="${parallel?'Parallelschaltung':'Reihenschaltung'} mit zwei Widerständen"><g fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">${parallel?'<path d="M88 70 H185 V40 H455 V70 H560 V218 H88 V70 M185 70 V218 M455 70 V218"/>':'<path d="M88 70 H560 V218 H88 V70"/>'}</g><g fill="var(--teal,#1d9d82)" stroke="none"><circle cx="88" cy="144" r="8"/><circle cx="560" cy="144" r="8"/></g><g fill="var(--surface,#fff)" stroke="currentColor" stroke-width="3"><rect x="${parallel?'225':'220'}" y="${parallel?'18':'52'}" width="80" height="40" rx="4"/><rect x="${parallel?'350':'370'}" y="${parallel?'200':'52'}" width="80" height="40" rx="4"/></g><g fill="currentColor" font-size="19" font-family="system-ui"><text x="18" y="125">${v.U} V</text><text x="${parallel?'240':'230'}" y="${parallel?'45':'80'}">R1</text><text x="${parallel?'364':'380'}" y="${parallel?'228':'80'}">R2</text><text x="205" y="277">${parallel?'Parallelschaltung':'Reihenschaltung'} · DC-Simulation</text></g></svg>`}
window.ElektroSimulator={solve,diagram};
})();
