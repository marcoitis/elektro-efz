'use strict';
/* No-browser regression test: chapter alignment to exact narrator manuscript,
 * 19 distinct SVG chapters and app route wiring. */
const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const manuscript=fs.readFileSync('tts_scripts/1.03-B.txt','utf8').trim();
const state={settings:{rate:1},audioTime:{},studioPositions:{}};
const context={window:{ElektroLectures:{'1.03-B':manuscript}},console,URL,Uint8Array};
vm.runInNewContext(fs.readFileSync('video-pilot.js','utf8'),context,{filename:'video-pilot.js'});
const pilot=context.window.ElektroVideoPilot;
assert(pilot);
assert.equal(pilot.ID,'1.03-B');
const points=pilot.makeTimeline(manuscript);
assert.equal(points.length,19,'Expected 19 illustrated sections');
assert.equal(pilot.sceneCount,19);
assert.equal(points[0].pct,0);
assert(points.at(-1).pct>.88);
for(let i=1;i<points.length;i++)
 assert(points[i].pct>points[i-1].pct,'Chapter boundaries must be monotone');
const html=pilot.render({id:'1.03-B'},state);
assert(html.includes('id="video-pilot"'));
assert(!html.includes(' data-lesson='),'Video controls must not trigger existing [data-lesson] navigation handler');
assert(html.includes('data-vp-id="1.03-B"'));
assert(html.includes('Thorsten'));
assert(html.includes('vp-seek'));
assert(html.includes('vp-expand'));
assert(html.includes('vp-speed'));
assert.equal((html.match(/data-vp-chapter=/g)||[]).length,19);
for(let index=0;index<19;index++){
 for(let phase=0;phase<3;phase++){
  const scene=pilot.sceneMarkup(
   [{marker:'',title:'Test',sub:'Educational diagram',kind:['graph','series','parallel','example','measure','quad'][index%6],points:['a','b','c']}][0],
   phase,index
  );
  assert(scene.includes('<svg'));
  assert(scene.includes('Didaktisches Modell'));
 }
}
const app=fs.readFileSync('app.js','utf8'),
 index=fs.readFileSync('index.html','utf8'),
 sw=fs.readFileSync('sw.js','utf8'),
 offline=fs.readFileSync('offline.js','utf8'),
 build=fs.readFileSync('tools/build_site.py','utf8');
for(const str of ['videoPilot.render(l,state)','videoPilot?.bind(state,{save,audioLoad})',
  "params.get('lesson')==='1.03-B'","data-tab=\"video\""])
 assert(app.includes(str),'App missing '+str);
for(const file of [index,sw,offline,build]){
 assert(file.includes('video-pilot.js'),'Pilot source missing from shell');
 assert(file.includes('video-pilot.css'),'Pilot styles missing from shell');
}
const version=JSON.parse(fs.readFileSync('version.json','utf8'));
assert.equal(version.build,'0.12.0-video-pilot-1');
console.log('PASS 19/19 voice-script chapter markers, 57 SVG states, app integration, PWA files and version');
