'use strict';
/* Regression test for iOS "Load failed": retry only the missing MP3 without
 * overwriting the 177 good tracks. This tests the actual offline.js function. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const ids=['1.01-A','1.01-B'];
const payload=new Uint8Array(7000);
payload.set([73,68,51],0);
let attempts=0,manifestFetches=0,imports=[],present=new Set(['1.01-B']);
let failAll=false;
const ctx={
 URL,Uint8Array,Blob,File,TextEncoder,Promise,setTimeout,
 location:{href:'https://marcoitis.github.io/elektro-efz/index.html',origin:'https://marcoitis.github.io'},
 window:{
  ELEKTRO_DATA:{lessons:ids.map(id=>({id}))},
  ElektroNormCourse:{lessons:[]},
  ElektroAudio:{
   has:async id=>present.has(id),
   importFile:async (id,file)=>{assert.equal(file.size,payload.length);present.add(id);imports.push(id)},
   count:async ()=>present.size,
  }
 },
 fetch:async url=>{
  const target=String(url);
  if(target.includes('audio-manifest.json')){
   manifestFetches++;
   return {ok:true,json:async()=>({baseUrl:'https://github.com/marcoitis/elektro-efz/releases/download/thorsten-high-v0118-audio-20261118/',tracks:{'1.01-A':'1.01-A.mp3','1.01-B':'1.01-B.mp3'}})};
  }
  if(target.endsWith('/1.01-A.mp3')){
   attempts++;
   if(failAll||attempts===1)throw new TypeError('Load failed');
  } else if(target.endsWith('/1.01-B.mp3')){
   throw Error('Already present track must not be fetched');
  } else throw Error('Unexpected URL '+target);
  return {ok:true,blob:async()=>new Blob([payload],{type:'application/octet-stream'})};
 }
};
vm.runInNewContext(fs.readFileSync('offline.js','utf8'),ctx,{filename:'offline.js'});
(async()=>{
 const api=ctx.window.ElektroOffline;
 const first=await api.audioDownloadAll();
 assert.equal(first.total,2);
 assert.equal(first.downloaded,1);
 assert.equal(first.skipped,1);
 assert.deepEqual([...first.failedIds],[]);
 assert.equal(attempts,2,'failed Safari load must be retried');
 assert.deepEqual(imports,['1.01-A']);
 // Targeted repair: even replaceExisting=true must touch only selected ID.
 attempts=0;
 const again=await api.audioDownloadAll(()=>{},true,['1.01-A']);
 assert.equal(again.total,1);
 assert.equal(again.downloaded,1);
 assert.equal(again.errors.length,0);
 assert.deepEqual(imports,['1.01-A','1.01-A']);
 // Terminal transient failure: existing audio must remain saved, show failed ID.
 attempts=0;failAll=true;
 const fail=await api.audioDownloadAll(()=>{},true,['1.01-A']);
 assert.equal(fail.downloaded,0);
 assert.equal(fail.errors.length,1);
 assert.deepEqual([...fail.failedIds],['1.01-A']);
 assert.ok(present.has('1.01-A'));
 assert.ok(present.has('1.01-B'));
 assert.equal(attempts,3);
 assert.ok(manifestFetches>=3);
 console.log('PASS: transient retry, 1-ID selective repair, preserve 177 existing tracks, 3-attempt limit');
})().catch(e=>{console.error(e);process.exitCode=1});
