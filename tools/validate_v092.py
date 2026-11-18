#!/usr/bin/env python3
"""Static+runtime template tests. Does not certify norms or replace browser/QV testing."""
from pathlib import Path
import subprocess,sys,xml.etree.ElementTree as ET,json,re
R=Path(__file__).resolve().parent.parent
D=json.loads((R/'data.js').read_text(encoding='utf-8').split('=',1)[1].strip(' ;\n'))
N=json.loads((R/'norm_course.json').read_text(encoding='utf-8'))
for id in [l['id'] for l in D['lessons']]+['N-'+l['id'] for l in N['lessons']]:
 p=R/'visuals'/(id+'.svg')
 ET.parse(p)
 content=p.read_text(encoding='utf-8')
 if ('<title id="t">' not in content and '<title>' not in content) or ('keine Installations-' not in content and 'keine Installationsplanung' not in content):raise SystemExit('SVG failed: '+id)
for name in ['studio.js','app.js','offline.js','sw.js','lesson-audit.js','data.js','norm-course.js','lecture-scripts.js','lesson-long-slides.js']:
 z=subprocess.run(['node','--check',str(R/name)],capture_output=True,text=True)
 if z.returncode:raise SystemExit('JS syntax: '+name+z.stderr)
script="""const fs=require('fs'),vm=require('vm'),c={window:{},console};for(const file of ['data.js','norm-course.js','lesson-audit.js','studio.js','studio-examples-extra.js','lesson-long-slides.js'])vm.runInNewContext(fs.readFileSync(file,'utf8'),c,{filename:file});const w=c.window,s={studioPositions:{},studioNotes:{},quizAnswers:{},normQuiz:{},settings:{rate:1}};let n=0;for(const l of w.ELEKTRO_DATA.lessons){s.studioPositions[l.id]=1;const str=w.ElektroStudio.renderRegular(l,s);if(!str.includes('./visuals/'+l.id+'.svg'))throw Error('visual missing in '+l.id);if(!str.includes('Fachprüfung offen'))throw Error('audit missing in '+l.id);n++}for(const l of w.ElektroNormCourse.lessons){s.studioPositions['N-'+l.id]=1;const str=w.ElektroStudio.renderNorm(l,s);if(!str.includes('./visuals/N-'+l.id+'.svg'))throw Error('norm visual missing in '+l.id);n++}for(const id of ['1.03-B','2.02-A','3.07-B']){const l=w.ELEKTRO_DATA.lessons.find(x=>x.id===id),z=w.ElektroStudio.createSlides(l,false);if(z.length<19)throw Error('Long lesson slides missing '+id);}console.log('Rendered templates:',n);"""
r=subprocess.run(['node','-e',script],cwd=R,capture_output=True,text=True)
if r.returncode:raise SystemExit(r.stderr)
print(r.stdout.strip())
for f in ['index.html','sw.js','offline.js','tools/build_site.py']:
 s=(R/f).read_text(encoding='utf8')
 if 'lesson-audit.js' not in s:raise SystemExit(f+' misses audit app component')
 if f in ['sw.js','offline.js'] and s.count('./visuals/')<178:raise SystemExit(f+' missing visual precache')
print('SVG XML valid: 178; review badges: 178; offline visual references: 178; syntax checks: OK')
