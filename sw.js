/* v0.6 – offline shell; wait for explicit user approval before takeover */
const CACHE='elektro-efz-shell-v06-1';
const PREFIX='elektro-efz-shell-';
const ASSETS=['./','./index.html','./styles.css','./data.js','./storage.js','./reviews.js','./exercises.js','./audio-engine.js','./cloud.js','./app.js','./manifest.webmanifest','./icon-192.png','./icon-512.png'];
self.addEventListener('install',event=>{event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(ASSETS)))});
self.addEventListener('activate',event=>{event.waitUntil((async()=>{const keys=await caches.keys();await Promise.all(keys.filter(k=>k.startsWith(PREFIX)&&k!==CACHE).map(k=>caches.delete(k)));await self.clients.claim()})())});
self.addEventListener('message',event=>{if(event.data?.type==='SKIP_WAITING')self.skipWaiting();if(event.data?.type==='GET_VERSION')event.source?.postMessage({type:'APP_VERSION',version:'0.6',cache:CACHE})});
self.addEventListener('fetch',event=>{const req=event.request,url=new URL(req.url);if(req.method!=='GET'||url.origin!==self.location.origin)return;
 if(req.mode==='navigate'){event.respondWith(caches.open(CACHE).then(async cache=>(await cache.match('./index.html'))||fetch(req)));return}
 if(ASSETS.some(a=>new URL(a,self.registration.scope).pathname===url.pathname)){
  event.respondWith(caches.open(CACHE).then(async cache=>(await cache.match(req,{ignoreSearch:true}))||fetch(req)));
 }
});
