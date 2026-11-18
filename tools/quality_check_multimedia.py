#!/usr/bin/env python3
"""Structural checks, not a norm compliance or professional training certification."""
from pathlib import Path
import json,subprocess,sys,re
R=Path(__file__).resolve().parent.parent
D=json.loads((R/'data.js').read_text().split('=',1)[1].strip(' ;\n'))
N=json.loads((R/'norm_course.json').read_text())
ids={l['id'] for l in D['lessons']}|{'N-'+l['id'] for l in N['lessons']}
files=set(p.stem for p in (R/'tts_scripts').glob('*.txt'))
errors=[]
if len(ids)!=178 or len(files)!=178 or ids!=files:errors.append('lesson IDs or 178 scripts mismatch')
for id in ids:
 content=(R/'tts_scripts'/f'{id}.txt').read_text(encoding='utf-8')
 if len(content.split())<350:errors.append(id+': narrator script below minimum 350 words')
 if 'Zusätzliche Unterrichtsvertiefung' not in content and not any((p/(id+'.txt')).is_file() for p in R.glob('editorial_v*') if p.is_dir()):errors.append(id+': enhancement missing')
for name in ['studio.js','studio-examples-extra.js','lecture-scripts.js','lesson-long-slides.js','studio.css']:
 if name not in (R/'index.html').read_text():errors.append(name+': not included by index')
 if name not in (R/'sw.js').read_text():errors.append(name+': not in offline worker')
 if name not in (R/'tools/build_site.py').read_text():errors.append(name+': not in build tool')
 if not (R/name).exists():errors.append(name+': missing')
if 'studioPositions' not in (R/'app.js').read_text():errors.append('missing saved slide positions')
if 'recordQuiz:answerQuiz' not in (R/'app.js').read_text():errors.append('slide answers not integrated with original quiz')
script=r'''const fs=require('fs'),vm=require('vm');const ctx={window:{},console};for(const f of ['data.js','norm-course.js','studio.js','studio-examples-extra.js','lecture-scripts.js','lesson-long-slides.js'])vm.runInNewContext(fs.readFileSync(f,'utf8'),ctx,{filename:f});const w=ctx.window;let counts=[],slides=0;for(const l of w.ELEKTRO_DATA.lessons){const a=w.ElektroStudio.createSlides(l,false);counts.push(a.length);slides+=a.length;if(a.filter(x=>x.type==='quiz').length!==3||!a.some(x=>x.type==='practice')||!a.some(x=>x.type==='worked'))throw Error('invalid lesson '+l.id);}for(const l of w.ElektroNormCourse.lessons){const a=w.ElektroStudio.createSlides(l,true);counts.push(a.length);slides+=a.length;if(a.filter(x=>x.type==='quiz').length!==3||!a.some(x=>x.type==='practice'))throw Error('invalid norm '+l.id);}if(Object.keys(w.ElektroLectures).length!==178)throw Error('lecture count');console.log('Slide decks: '+counts.length+' · slides: '+slides+' · min/max: '+Math.min(...counts)+'/'+Math.max(...counts));'''
result=subprocess.run(['node','-e',script],cwd=R,text=True,capture_output=True)
if result.returncode:errors.append('slide generation failure: '+result.stderr)
else:print(result.stdout.strip())
print('Structural errors:',len(errors))
for e in errors:print('ERROR:',e)
if errors:sys.exit(1)

# v0.9.2: each lesson has a real standalone SVG, and every review entry is still pending signoff.
audit=json.loads((R/'quality-review.json').read_text(encoding='utf-8'))
if len(audit.get('lessons',[]))!=178: raise SystemExit('audit coverage error')
visuals=list((R/'visuals').glob('*.svg'))
if len(visuals)!=178: raise SystemExit('individual drawings missing')
for a in audit['lessons']:
 if a.get('normaussagen_freigegeben'):raise SystemExit('unjustified normative approval: '+a['id'])
 if not (R/a['visual']).exists():raise SystemExit('no visual for '+a['id'])
 if a['script_words']!=len((R/'tts_scripts'/(a['id']+'.txt')).read_text(encoding='utf-8').split()):raise SystemExit('stale audit for '+a['id'])
print('Visuals/audit: 178 diagrams; 178 pending expert reviews; long editorial scripts:',sum(len((R/'tts_scripts'/(x+'.txt')).read_text(encoding='utf-8').split()) >= 1950 for x in ids))
