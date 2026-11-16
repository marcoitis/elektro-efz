/* Offline manager v0.8. All lesson content is contained in data.js. */
(function(){'use strict';
const CACHE='elektro-efz-shell-v080-1';
const FILES=['./','./index.html','./styles.css','./data.js','./storage.js','./reviews.js','./exercises.js','./audio-engine.js','./cloud.js','./offline.js','./trainer.js','./simulator.js','./norms.js','./norm-course.js','./app.js','./manifest.webmanifest','./icon-192.png','./icon-512.png'];
const root=()=>new URL('./',location.href);
const abs=f=>new URL(f,root()).href;
const isSupported=()=>!!(window.caches&&'serviceWorker'in navigator&&location.protocol==='https:')||location.hostname==='localhost';
const tell=(done,total,what)=>window.dispatchEvent(new CustomEvent('elektro-offline-progress',{detail:{done,total,what}}));
async function status(){
 if(!('caches'in window))return {supported:false,complete:false,stored:0,total:FILES.length,missing:FILES.slice()};
 try{const cache=await caches.open(CACHE),missing=[];for(const f of FILES){if(!(await cache.match(abs(f),{ignoreSearch:true})))missing.push(f)}
 return {supported:isSupported(),complete:missing.length===0,stored:FILES.length-missing.length,total:FILES.length,missing};}
 catch(e){return {supported:false,complete:false,stored:0,total:FILES.length,missing:FILES.slice(),error:e.message}}
}
async function download(){
 if(!isSupported())throw Error('Offline-Paket benötigt HTTPS oder localhost und Service Worker.');
 if(!navigator.onLine)throw Error('Verbinde Dich zum Herunterladen zuerst mit dem Internet.');
 const cache=await caches.open(CACHE);let done=0;let errors=[];for(const file of FILES){
   const url=abs(file);try{
     const found=await cache.match(url,{ignoreSearch:true});
     if(!found){const response=await fetch(url,{cache:'no-store'});if(!response.ok||response.type==='opaque')throw Error('HTTP '+response.status);await cache.put(url,response.clone());}
   }catch(e){errors.push(file+': '+e.message)}done++;tell(done,FILES.length,file);
 }
 const result=await status();if(errors.length||!result.complete)throw Error('Unvollständiges Paket: '+errors.join('; ')+(result.missing.length?' · Fehlend: '+result.missing.join(', '):''));
 return result;
}
async function verify(){const s=await status();if(!s.complete)throw Error('Offline-Paket unvollständig: '+s.missing.join(', '));
 // Checking each cache entry makes failure visible, without trying to toggle the system network.
 const cache=await caches.open(CACHE);for(const f of FILES){const r=await cache.match(abs(f),{ignoreSearch:true});if(!r?.ok)throw Error('Nicht lesbar: '+f);if(['./data.js','./app.js','./index.html'].includes(f)){const body=await r.text();if(body.length<3000)throw Error('Unplausibel kleine Datei: '+f)}}
 return s;
}
async function audioManifest(){try{const r=await fetch(abs('./audio-manifest.json'),{cache:'no-store'});if(!r.ok)throw Error('Manifest nicht gefunden');const j=await r.json();return j?.tracks||{}}catch(_){return {}}}
async function audioCount(){return window.ElektroAudio.count?.()??0}
async function audioDownloadAll(onProgress=()=>{}){const tracks=await audioManifest();const names=Object.entries(tracks);let done=0,errors=[];if(!names.length)return {total:0,done:0,errors:[],message:'Keine externen Audioaufnahmen veröffentlicht. Du kannst eigene MP3/M4A-Dateien importieren.'};
 for(const [id,path] of names){if(!(window.ELEKTRO_DATA.lessons.some(l=>l.id===id)||window.ElektroNormCourse?.lessons.some(l=>"N-"+l.id===id))){errors.push('Unbekannte Lektion '+id);continue;}
  try{if(!(await window.ElektroAudio.has(id))){const url=new URL(path,root());if(url.origin!==location.origin)throw Error('Datei liegt nicht auf demselben Server');const r=await fetch(url.href);if(!r.ok)throw Error('HTTP '+r.status);const b=await r.blob();if(!/^audio\//.test(b.type))throw Error('Kein Audioformat');if(b.size>80*1024*1024)throw Error('Datei > 80 MB');const file=new File([b],id+'.mp3',{type:b.type});await window.ElektroAudio.importFile(id,file);}}catch(e){errors.push(id+': '+e.message)}done++;onProgress(done,names.length,id);
 }return {total:names.length,done,errors};}
window.ElektroOffline={CACHE,FILES,status,download,verify,audioManifest,audioCount,audioDownloadAll};
})();
