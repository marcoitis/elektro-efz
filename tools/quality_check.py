#!/usr/bin/env python3
"""Offline QA: Validates lesson structure, IDs, quizzes, references, audio mappings.
Does not certify the professional correctness of electrical normative content.
"""
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parent.parent
warnings=[]
errors=[]
def js_data(path,marker):
 s=(ROOT/path).read_text(encoding='utf-8').strip()
 if not s.startswith(marker):errors.append('Variable changed in '+path);return {}
 try:return json.loads(s[len(marker):].rstrip(' ;\n'))
 except Exception as e: errors.append('Invalid JSON in '+path+': '+str(e));return {}
D=js_data('data.js','window.ELEKTRO_DATA = ')
N=js_data('norm_course.json','') if False else json.loads((ROOT/'norm_course.json').read_text(encoding='utf-8'))
modules=D.get('modules',[]);lessons=D.get('lessons',[])
module_ids={m['id'] for m in modules};lesson_ids={l['id'] for l in lessons}
if len(modules)!=48:errors.append(f'Expected 48 modules, got {len(modules)}')
if len(lessons)!=145:errors.append(f'Expected 145 original lessons, got {len(lessons)}')
if len(lesson_ids)!=len(lessons):errors.append('Duplicate lesson IDs')
if len(module_ids)!=len(modules):errors.append('Duplicate module IDs')
for l in lessons:
 lid=l.get('id','?')
 if l.get('moduleId') not in module_ids:errors.append(lid+': unknown module')
 if len(l.get('parts',[]))<2:errors.append(lid+': missing explanation parts')
 if len(l.get('quiz',[]))!=3:errors.append(lid+': quiz length != 3')
 for qi,q in enumerate(l.get('quiz',[])):
  if not isinstance(q.get('correct'),int) or not 0<=q['correct']<len(q.get('answers',[])):errors.append(f'{lid} quiz {qi}: invalid index')
  if not q.get('why'):warnings.append(f'{lid} quiz {qi}: no rationale')
  if len(set(q.get('answers',[])))!=len(q.get('answers',[])):warnings.append(f'{lid} quiz {qi}: duplicate answers')
for l in N.get('lessons',[]):
 for qi,q in enumerate(l.get('quiz',[])):
  if not isinstance(q.get('correct'),int) or not 0<=q['correct']<len(q.get('answers',[])):errors.append(f'norm {l["id"]} quiz {qi}: invalid index')
scripts=list((ROOT/'tts_scripts').glob('*.txt'))
if len(scripts)!=len(lessons)+len(N.get('lessons',[])):errors.append(f'Audio script count mismatch: {len(scripts)}')
for l in lessons:
 if not (ROOT/'tts_scripts'/f'{l["id"]}.txt').exists():errors.append(f'Missing narration {l["id"]}')
for l in N.get('lessons',[]):
 if not (ROOT/'tts_scripts'/f'N-{l["id"]}.txt').exists():errors.append(f'Missing norm narration N-{l["id"]}')
for p in ['academy.js','academy-content.js','app.js','styles.css','index.html','sw.js','offline.js','audio-engine.js']:
 if not (ROOT/p).is_file():errors.append('Missing '+p)
if 'academy.js' not in (ROOT/'sw.js').read_text():errors.append('New module missing from SW core')
if 'academy.js' not in (ROOT/'tools/build_site.py').read_text():errors.append('New module missing from Pages bundle')
if 'academy.js' not in (ROOT/'index.html').read_text():errors.append('New module missing from index')
if 'NIN' not in (ROOT/'norms.js').read_text():warnings.append('No apparent NIN source status')
print(f'Elektro EFZ v0.9 QA · {len(modules)} modules · {len(lessons)} + {len(N.get("lessons",[]))} lessons · {len(scripts)} scripts')
for w in warnings[:15]:print('WARN',w)
for e in errors:print('ERROR',e,file=sys.stderr)
print(f'Warnings: {len(warnings)}, errors: {len(errors)}')
if errors:sys.exit(1)
