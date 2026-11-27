import { chromium, webkit } from 'playwright';
import { createServer } from 'node:http';
import { createReadStream, statSync } from 'node:fs';
import { resolve, sep, extname } from 'node:path';

const root=process.cwd();
const mime={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8',
  '.css':'text/css; charset=utf-8','.json':'application/json; charset=utf-8',
  '.mp3':'audio/mpeg','.svg':'image/svg+xml'};
const server=createServer((req,res)=>{
  try {
    let pathname=decodeURIComponent(new URL(req.url,'http://127.0.0.1').pathname);
    let file=resolve(root,'.'+pathname);
    if(file!==root&&!file.startsWith(root+sep)){res.writeHead(403).end();return;}
    let stat=statSync(file);
    if(stat.isDirectory()){file=resolve(file,'index.html');stat=statSync(file);}
    const headers={'Content-Type':mime[extname(file)]||'application/octet-stream',
      'Accept-Ranges':'bytes','Cache-Control':'no-store'};
    const range=req.headers.range;
    if(range){
      const match=/^bytes=(\d*)-(\d*)$/.exec(range);
      if(!match){res.writeHead(416,{'Content-Range':'bytes */'+stat.size}).end();return;}
      let start=match[1]?Number(match[1]):Math.max(0,stat.size-Number(match[2]));
      let end=match[2]&&match[1]?Math.min(Number(match[2]),stat.size-1):stat.size-1;
      if(start>end||start>=stat.size){res.writeHead(416,{'Content-Range':'bytes */'+stat.size}).end();return;}
      headers['Content-Range']=`bytes ${start}-${end}/${stat.size}`;
      headers['Content-Length']=end-start+1;
      res.writeHead(206,headers);
      createReadStream(file,{start,end}).pipe(res);
    }else{
      headers['Content-Length']=stat.size;
      res.writeHead(200,headers);
      createReadStream(file).pipe(res);
    }
  }catch(_){res.writeHead(404).end();}
});
await new Promise((resolveListen,reject)=>{
  server.once('error',reject);
  server.listen(8765,'127.0.0.1',resolveListen);
});
try {
  const health=await fetch('http://127.0.0.1:8765/masterclass.html');
  if(!health.ok) throw new Error('Local HTTP server did not serve masterclass.html');
  for (const [name,engine] of [['chromium',chromium],['webkit',webkit]]) {
    const browser=await engine.launch({headless:true});
    try {
      for (const width of [390,1280]) {
        const page=await browser.newPage({viewport:{width,height:844}});
        const errors=[], failedRequests=[], badResponses=[];
        page.on('pageerror',e=>errors.push(e.message));
        page.on('requestfailed',r=>failedRequests.push(r.url()+': '+(r.failure()?.errorText||'failed')));
        page.on('response',r=>{if(r.status()>=400)badResponses.push(r.status()+' '+r.url())});
        await page.goto('http://127.0.0.1:8765/masterclass.html?lesson=1.01-B',{waitUntil:'domcontentloaded'});
        try {
          await page.waitForFunction(()=>window.ElektroMaster?.getTimeline()?.beats?.length===24,null,{timeout:30000});
        } catch(e) {
          const state=await page.evaluate(()=>({
            status:document.querySelector('#mc-status')?.textContent,
            lesson:document.body.dataset.masterLesson,
            renderer:!!window.EFZ_MasterRenderers?.['1.01-B'],
            engine:!!window.ElektroMaster,
            timeline:window.ElektroMaster?.getTimeline()?.beats?.length??null
          }));
          throw new Error(name+' '+width+': timeline initialization failed; '+JSON.stringify({state,errors,failedRequests,badResponses})+'; '+e.message);
        }
        try {
          await page.waitForFunction(()=>document.querySelector('#mc-audio')?.readyState>=1,null,{timeout:30000});
        } catch(e) {
          const state=await page.evaluate(()=>{
            const a=document.querySelector('#mc-audio');
            return {status:document.querySelector('#mc-status')?.textContent,src:a?.currentSrc||a?.src,
              readyState:a?.readyState,networkState:a?.networkState,error:a?.error?.message||a?.error?.code||null,
              duration:a?.duration,timeline:window.ElektroMaster?.getTimeline()?.beats?.length??null};
          });
          throw new Error(name+' '+width+': audio metadata did not load; '+JSON.stringify({state,errors,failedRequests,badResponses})+'; '+e.message);
        }
        const info=await page.evaluate(()=>{
          const a=document.querySelector('#mc-audio'), t=window.ElektroMaster.getTimeline();
          return {duration:a.duration,beats:t.beats.length,svg:!!document.querySelector('#mc-stage svg'),
            overflow:document.documentElement.scrollWidth>document.documentElement.clientWidth,
            question:t.beats.at(-2),answer:t.beats.at(-1)};
        });
        if(!Number.isFinite(info.duration)||info.duration<110||info.duration>450) throw new Error(name+' '+width+': invalid MP3 duration '+info.duration);
        if(info.beats!==24||!info.svg||info.overflow) throw new Error(name+' '+width+': renderer, beat count or viewport check failed '+JSON.stringify(info));
        const quiz=await page.evaluate(async()=>{
          const a=document.querySelector('#mc-audio'), q=window.ElektroMaster.getTimeline().beats.at(-2);
          const target=Math.max(0,q.end-.05);
          if(Math.abs(a.currentTime-target)>.2){
            await new Promise((resolve,reject)=>{
              const timer=setTimeout(()=>reject(new Error('Audio seek did not finish before quiz-boundary test')),15000);
              a.addEventListener('seeked',()=>{clearTimeout(timer);resolve()},{once:true});
              a.currentTime=target;
            });
          }
          a.dispatchEvent(new Event('timeupdate'));
          return {paused:a.paused,currentTime:a.currentTime,questionEnd:q.end,questionVisual:q.visual,
            answerHidden:document.querySelector('#mc-answer').hidden,status:document.querySelector('#mc-status').textContent};
        });
        if(!quiz.paused||quiz.answerHidden) throw new Error(name+' '+width+': quiz pause failed '+JSON.stringify(quiz));
        if(errors.length) throw new Error(name+' '+width+': '+errors.join('; '));
        console.log('PASS '+name+' '+width+'px: '+info.duration.toFixed(2)+'s, 24 beats, SVG, quiz pause, no overflow');
        await page.close();
      }
    } finally { await browser.close(); }
  }
} finally { server.close(); }
