/* Elektro EFZ 0.3: IndexedDB primary store + synchronous local checkpoint.
   All data stays on this origin/device. A downloaded JSON is the only off-device backup. */
(function(){'use strict';
const DATABASE='elektro-efz-progress', VERSION=1, PROGRESS='records', SNAPSHOTS='snapshots';
const LEGACY_LOCAL='elektro-efz-lernstand-v1', LOCAL_CHECKPOINT='elektro-efz-checkpoint-v2';
let db=null, idbAvailable=false, localAvailable=false, lastError='', lastSaved='', pending=null, timer=null;
let chain=Promise.resolve();
const copy=x=>JSON.parse(JSON.stringify(x));
const time=x=>{const t=Date.parse(x?.updated||'');return Number.isFinite(t)?t:0};
function checkLocal(){try{localStorage.setItem('efz-probe-v03','1');localStorage.removeItem('efz-probe-v03');return true}catch(_){return false}}
function readLocal(key){if(!localAvailable)return null;try{return JSON.parse(localStorage.getItem(key)||'null')}catch(e){lastError='Lokale Daten unlesbar: '+e.message;return null}}
function openDb(){return new Promise((resolve,reject)=>{
 if(!('indexedDB' in window))return reject(Error('IndexedDB nicht vorhanden'));
 let r;try{r=indexedDB.open(DATABASE,VERSION)}catch(e){reject(e);return}
 r.onupgradeneeded=()=>{const x=r.result;if(!x.objectStoreNames.contains(PROGRESS))x.createObjectStore(PROGRESS);if(!x.objectStoreNames.contains(SNAPSHOTS))x.createObjectStore(SNAPSHOTS,{keyPath:'at'})};
 r.onsuccess=()=>{r.result.onversionchange=()=>{r.result.close();db=null;idbAvailable=false;lastError='Datenbankversion geändert: Seite neu laden'};resolve(r.result)};
 r.onerror=()=>reject(r.error||Error('IndexedDB konnte nicht geöffnet werden'));
 r.onblocked=()=>reject(Error('Ein anderer Tab blockiert die Datenbank'));
})}
function readDb(key){return new Promise((resolve,reject)=>{if(!db)return resolve(null);try{const r=db.transaction(PROGRESS,'readonly').objectStore(PROGRESS).get(key);r.onsuccess=()=>resolve(r.result??null);r.onerror=()=>reject(r.error)}catch(e){reject(e)}})}
function writeDb(key,val){return new Promise((resolve,reject)=>{if(!db)return reject(Error('IndexedDB ist nicht verfügbar'));try{const tx=db.transaction(PROGRESS,'readwrite');tx.objectStore(PROGRESS).put(copy(val),key);tx.oncomplete=()=>resolve();tx.onerror=()=>reject(tx.error||Error('IndexedDB-Speicherfehler'));tx.onabort=()=>reject(tx.error||Error('IndexedDB-Transaktion abgebrochen'))}catch(e){reject(e)}})}
function writeLocal(value){if(!localAvailable)return false;try{localStorage.setItem(LOCAL_CHECKPOINT,JSON.stringify(value));return true}catch(e){localAvailable=false;lastError='Lokaler Checkpoint fehlgeschlagen: '+e.message;return false}}
function quality(){return {mode:idbAvailable?'indexeddb':localAvailable?'localstorage':'memory',indexedDB:idbAvailable,checkpoint:localAvailable,lastError,lastSaved,pending:!!pending||timer!==null}}
async function init(){localAvailable=checkLocal();try{db=await openDb();idbAvailable=true}catch(e){lastError='IndexedDB: '+e.message}
 const all=[readLocal(LEGACY_LOCAL),readLocal(LOCAL_CHECKPOINT)];
 if(idbAvailable){try{all.push(await readDb('progress'))}catch(e){lastError='IndexedDB lesen: '+e.message;idbAvailable=false}}
 const candidates=all.filter(x=>x&&typeof x==='object'&&[1,2].includes(x.version)&&Array.isArray(x.lessonDone));
 candidates.sort((a,b)=>time(b)-time(a));
 const recent=candidates[0];if(!recent)return null;
 const migrated={...recent,version:2};
 // Persist a migration copy before the UI is made interactive.
 writeLocal(migrated);
 if(idbAvailable){try{await writeDb('progress',migrated);lastSaved=migrated.updated||''}catch(e){idbAvailable=false;lastError='Migration: '+e.message}}
 return copy(migrated)
}
function queueWrite(){if(!pending||!idbAvailable)return chain;
 const s=pending;pending=null;
 chain=chain.catch(()=>{}).then(async()=>{try{await writeDb('progress',s);lastSaved=s.updated||new Date().toISOString()}catch(e){idbAvailable=false;lastError='IndexedDB-Schreiben fehlgeschlagen: '+e.message;pending=s}});
 return chain
}
function save(value){const s=copy({...value,version:2});const checkpointOk=writeLocal(s);pending=s;
 if(idbAvailable){if(timer!==null)clearTimeout(timer);timer=setTimeout(()=>{timer=null;queueWrite()},180)}
 else if(!checkpointOk)lastError='Kein dauerhafter Datenspeicher verfügbar';
 return quality()
}
async function flush(){if(timer!==null){clearTimeout(timer);timer=null}if(idbAvailable)await queueWrite();await chain;
 // A save may have happened while an earlier IndexedDB transaction was pending.
 if(idbAvailable&&pending)await queueWrite();
 return quality()
}
function listSnapshots(){if(!idbAvailable)return Promise.resolve([]);return new Promise((resolve,reject)=>{try{const r=db.transaction(SNAPSHOTS,'readonly').objectStore(SNAPSHOTS).getAll();r.onsuccess=()=>resolve((r.result||[]).sort((a,b)=>b.at.localeCompare(a.at)));r.onerror=()=>reject(r.error)}catch(e){reject(e)}})}
async function snapshot(current,reason='manuell'){
 if(!idbAvailable)return false;
 try{await flush();const payload={at:new Date().toISOString(),reason,state:copy({...current,version:2})};
  await new Promise((resolve,reject)=>{const tx=db.transaction(SNAPSHOTS,'readwrite');tx.objectStore(SNAPSHOTS).put(payload);tx.oncomplete=resolve;tx.onerror=()=>reject(tx.error)});
  const list=await listSnapshots();for(const old of list.slice(5)){await new Promise((resolve,reject)=>{const tx=db.transaction(SNAPSHOTS,'readwrite');tx.objectStore(SNAPSHOTS).delete(old.at);tx.oncomplete=resolve;tx.onerror=()=>reject(tx.error)})}
  return true
 }catch(e){lastError='Lokale Sicherung: '+e.message;return false}
}
async function weeklySnapshot(current){if(!idbAvailable)return;try{const list=await listSnapshots();if(!list.length||Date.now()-Date.parse(list[0].at)>=7*86400000)await snapshot(current,'automatische Wochenkopie')}catch(e){lastError='Wochensicherung: '+e.message}}
async function requestPersistence(){try{return !!(navigator.storage?.persist&&await navigator.storage.persist())}catch(_){return false}}
async function storageEstimate(){try{return navigator.storage?.estimate?await navigator.storage.estimate():null}catch(_){return null}}
window.ElektroStorage={init,save,flush,quality,listSnapshots,snapshot,weeklySnapshot,requestPersistence,storageEstimate,LEGACY_LOCAL,LOCAL_CHECKPOINT};
})();
