/* Elektro EFZ v0.8 · versioned offline shell. Old cache is retained unless new install succeeds. */
const CACHE='elektro-efz-shell-v080-1';
const PREFIX='elektro-efz-shell-';
const CORE=['./','./index.html','./styles.css','./data.js','./storage.js','./reviews.js','./exercises.js','./audio-engine.js','./cloud.js','./offline.js','./trainer.js','./simulator.js','./norms.js','./norm-course.js','./app.js','./manifest.webmanifest','./icon-192.png','./icon-512.png'];
self.addEventListener('install',event=>{event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(CORE)))});
self.addEventListener('activate',event=>{event.waitUntil((async()=>{const keys=await caches.keys();await Promise.all(keys.filter(k=>k.startsWith(PREFIX)&&k!==CACHE).map(k=>caches.delete(k)));await self.clients.claim()})())});
self.addEventListener('message',event=>{if(event.data?.type==='SKIP_WAITING')self.skipWaiting();if(event.data?.type==='GET_VERSION')event.source?.postMessage({type:'APP_VERSION',version:'0.8',cache:CACHE})});
self.addEventListener('fetch',event=>{
 const req=event.request,url=new URL(req.url);if(req.method!=='GET'||url.origin!==self.location.origin)return;
 if(req.mode==='navigate'){
  event.respondWith((async()=>{const cache=await caches.open(CACHE);const result=await cache.match('./index.html');if(result)return result;try{return await fetch(req)}catch(_){return new Response('Offline-Paket fehlt. Bitte die App online öffnen.',{status:503,headers:{'Content-Type':'text/plain; charset=utf-8'}})}})());return;
 }
 if(CORE.some(x=>new URL(x,self.registration.scope).pathname===url.pathname)){
  event.respondWith((async()=>{const cache=await caches.open(CACHE),result=await cache.match(req,{ignoreSearch:true});if(result)return result;return fetch(req)})());return;
 }
 // Other files (e.g. optional audio) use ordinary network; the audio player saves explicitly to IndexedDB.
});
