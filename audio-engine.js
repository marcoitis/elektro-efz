/* v0.4: Optional locally imported narration with browser media controls.
 * Audio files never leave the user's browser; they are not in JSON progress exports.
 * Existing speechSynthesis remains the fallback for all lessons. */
(function(){'use strict';
const DB='elektro-efz-lesson-audio',VER=1,STORE='clips';
let dbPromise=null;
let onTrackEnded=()=>{};
function db(){if(!dbPromise)dbPromise=new Promise((resolve,reject)=>{if(!('indexedDB'in window)){reject(Error('IndexedDB nicht verfügbar'));return}const r=indexedDB.open(DB,VER);r.onupgradeneeded=()=>{if(!r.result.objectStoreNames.contains(STORE))r.result.createObjectStore(STORE)};r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error||Error('Audio-Speicher konnte nicht geöffnet werden'))});return dbPromise}
async function transact(type,id,value){const d=await db();return new Promise((resolve,reject)=>{const t=d.transaction(STORE,type);const o=t.objectStore(STORE),r=type==='readonly'?o.get(id):value===null?o.delete(id):o.put(value,id);r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error||Error('Fehler beim Lesen der Audio-Datei'));t.onerror=()=>reject(t.error)})}
const media=new Audio();media.preload='metadata';let lessonId=null,blobUrl=null,loaded=false,notify=()=>{},position=()=>{};
function unload(){media.pause();media.removeAttribute('src');media.load();if(blobUrl)URL.revokeObjectURL(blobUrl);blobUrl=null;lessonId=null;loaded=false;notify()}
async function prepare(id,cb,savePosition,initial=0){if(lessonId===id&&loaded)return true;unload();lessonId=id;notify=cb||(()=>{});position=savePosition||(()=>{});try{const v=await transact('readonly',id);if(!v?.file){loaded=false;notify();return false}if(lessonId!==id)return false;blobUrl=URL.createObjectURL(v.file);media.src=blobUrl;media.playbackRate=1;loaded=true;media.addEventListener('loadedmetadata',()=>{if(lessonId===id&&initial>0&&Number.isFinite(media.duration))media.currentTime=Math.min(initial,Math.max(0,media.duration-1))},{once:true});notify();return true}catch(e){loaded=false;notify(e.message);return false}}
media.addEventListener('timeupdate',()=>{if(loaded&&lessonId)position(lessonId,media.currentTime,media.duration)});
media.addEventListener('play',()=>{if('mediaSession'in navigator){navigator.mediaSession.playbackState='playing'}notify()});
media.addEventListener('pause',()=>{if('mediaSession'in navigator){navigator.mediaSession.playbackState='paused'}notify()});
media.addEventListener('ended',()=>{if(lessonId)position(lessonId,0,media.duration);notify();try{onTrackEnded(lessonId)}catch(e){console.warn('Automatische Folgelektion:',e)}});
media.addEventListener('error',()=>notify('Audio-Datei kann nicht abgespielt werden'));
if('mediaSession'in navigator){try{navigator.mediaSession.setActionHandler('play',()=>{void media.play()});navigator.mediaSession.setActionHandler('pause',()=>media.pause());navigator.mediaSession.setActionHandler('seekbackward',d=>seek(-Math.abs(d.seekOffset||15)));navigator.mediaSession.setActionHandler('seekforward',d=>seek(Math.abs(d.seekOffset||15)));navigator.mediaSession.setActionHandler('seekto',d=>{if(Number.isFinite(d.seekTime))media.currentTime=d.seekTime})}catch(_){}}
function seek(seconds){if(!loaded)return;media.currentTime=Math.min(Number.isFinite(media.duration)?media.duration:1e8,Math.max(0,media.currentTime+seconds));notify()}
async function importFile(id,file){if(!/^audio\//.test(file.type)&&!/\.(mp3|m4a|wav|ogg|aac)$/i.test(file.name))throw Error('Bitte eine Audio-Datei (MP3, M4A, WAV) wählen');if(file.size>80*1024*1024)throw Error('Maximal 80 MB pro Lektion');await transact('readwrite',id,{file,name:file.name,bytes:file.size,added:new Date().toISOString()});if(lessonId===id){unload()}return true}
async function remove(id){await transact('readwrite',id,null);if(lessonId===id)unload()}
async function has(id){try{return !!(await transact('readonly',id))}catch(_){return false}}
async function list(){try{const d=await db();return await new Promise((resolve,reject)=>{const r=d.transaction(STORE,'readonly').objectStore(STORE).getAllKeys();r.onsuccess=()=>resolve(r.result||[]);r.onerror=()=>reject(r.error)})}catch(_){return []}}
async function count(){return (await list()).length}
async function importMany(files,knownIDs,onProgress=()=>{}){
 let done=0,skipped=[],errors=[];for(const file of files){const id=file.name.replace(/\.(mp3|m4a|wav|ogg|aac)$/i,'');if(!knownIDs.includes(id)){skipped.push(file.name)}else{try{await importFile(id,file)}catch(e){errors.push(file.name+': '+e.message)}}done++;onProgress(done,files.length,file.name)}return {done,skipped,errors}
}
function setMetadata(title){if(!('mediaSession'in navigator)||!window.MediaMetadata)return;try{navigator.mediaSession.metadata=new MediaMetadata({title,artist:'Elektroinstallateur EFZ – Dozent',album:'Digitale Fachschule'})}catch(_){}}
function isPlaying(){return loaded&&!media.paused&&!media.ended}
function setOnEnded(callback){onTrackEnded=typeof callback==='function'?callback:()=>{}}
window.ElektroAudio={prepare,setOnEnded,importFile,importMany,remove,has,list,count,unload,seek,play:()=>media.play(),pause:()=>media.pause(),setRate:v=>{media.playbackRate=v},setMetadata,getState:()=>({lessonId,loaded,playing:isPlaying(),current:media.currentTime||0,duration:Number.isFinite(media.duration)?media.duration:0})};
})();
