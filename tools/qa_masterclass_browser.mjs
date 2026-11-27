import { chromium, webkit } from 'playwright';
import { spawn } from 'node:child_process';
import { setTimeout as sleep } from 'node:timers/promises';

const server = spawn('python3', ['-m','http.server','8765','--bind','127.0.0.1'], {stdio:'ignore'});
try {
  let ready=false;
  for(let i=0;i<40;i++){
    try { const r=await fetch('http://127.0.0.1:8765/masterclass.html'); if(r.ok){ready=true;break;} } catch {}
    await sleep(250);
  }
  if(!ready) throw new Error('Local HTTP server did not start');
  for (const [name,engine] of [['chromium',chromium],['webkit',webkit]]) {
    const browser=await engine.launch({headless:true});
    try {
      for (const width of [390,1280]) {
        const page=await browser.newPage({viewport:{width,height:844}});
        const errors=[];
        page.on('pageerror',e=>errors.push(e.message));
        await page.goto('http://127.0.0.1:8765/masterclass.html?lesson=1.01-B',{waitUntil:'networkidle'});
        await page.waitForFunction(()=>window.ElektroMaster?.getTimeline()?.beats?.length===24,{timeout:30000});
        await page.waitForFunction(()=>document.querySelector('#mc-audio')?.readyState>=1,{timeout:30000});
        const info=await page.evaluate(()=>{
          const a=document.querySelector('#mc-audio'), t=window.ElektroMaster.getTimeline();
          return {duration:a.duration,beats:t.beats.length,svg:!!document.querySelector('#mc-stage svg'),
            overflow:document.documentElement.scrollWidth>document.documentElement.clientWidth,
            question:t.beats.at(-2),answer:t.beats.at(-1)};
        });
        if(!Number.isFinite(info.duration)||info.duration<110||info.duration>450) throw new Error(name+' '+width+': invalid MP3 duration '+info.duration);
        if(info.beats!==24||!info.svg||info.overflow) throw new Error(name+' '+width+': renderer, beat count or viewport check failed '+JSON.stringify(info));
        await page.evaluate(()=>{
          const a=document.querySelector('#mc-audio'), q=window.ElektroMaster.getTimeline().beats.at(-2);
          a.currentTime=Math.max(0,q.end-.05); a.dispatchEvent(new Event('timeupdate'));
        });
        await page.waitForFunction(()=>document.querySelector('#mc-audio').paused && !document.querySelector('#mc-answer').hidden,{timeout:5000});
        if(errors.length) throw new Error(name+' '+width+': '+errors.join('; '));
        console.log('PASS '+name+' '+width+'px: '+info.duration.toFixed(2)+'s, 24 beats, SVG, quiz pause, no overflow');
        await page.close();
      }
    } finally { await browser.close(); }
  }
} finally { server.kill('SIGTERM'); }
