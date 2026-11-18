'use strict';
// Unit test of relative GitHub Pages project paths (does not test a real browser/installation).
const fs=require('fs'), vm=require('vm'),assert=require('assert');
const registry={};
const url='https://example.github.io/elektro-efz/';
const paths=['index.html','kurskompass.html','vertiefung-151.html','fachvertiefung-151.html'];
const matchCache={match:async target=>{
  const key=typeof target==='string'?target:target.url;
  for(const page of paths){if(key==='./'+page || key===url+page)return new Response('PAGE '+page,{status:200});}
  return null;
}};
const context={
  self:{location:{origin:'https://example.github.io'},registration:{scope:url},addEventListener:(name,fn)=>{registry[name]=fn}},
  caches:{open:async()=>matchCache},
  URL,Response,Promise,console,fetch:async()=>{throw Error('Unexpected network use')}
};
vm.runInNewContext(fs.readFileSync('sw.js','utf8'),context,{filename:'sw.js'});
(async()=>{
 for(const page of paths){
  let outcome;registry.fetch({request:{url:url+page,method:'GET',mode:'navigate'},respondWith:p=>outcome=p});
  assert(outcome,'No SW response for '+page);
  const result=await outcome;const body=await result.text();
  assert.strictEqual(body,'PAGE '+page,'Wrong SW page for '+page+': '+body);
 }
 console.log('PASS SW routes: 4 distinct pages under /elektro-efz/');
})().catch(e=>{console.error(e);process.exit(1)});
