#!/usr/bin/env python3
"""No accidental secrets or all-at-once audio workflow; structural preflight."""
from pathlib import Path
import re,sys,json,hashlib
r=Path(__file__).resolve().parent.parent;errors=[]
workflow=(r/'.github/workflows/publish.yml').read_text(encoding='utf-8')
if 'tools/generate_audio.py' in workflow:errors.append('Pages action must not synthesize all audio')
if 'audio-manifest.json' not in (r/'sw.js').read_text():errors.append('SW missing audio-manifest')
if len(list((r/'tts_scripts').glob('*.txt')))!=178:errors.append('Missing TTS source files')
for file in r.rglob('*'):
 if not file.is_file() or any(x in file.parts for x in ('dist','.voice-cache','.audio-cache','.git')):continue
 if file.suffix.lower()=='.mp3' and re.fullmatch(r'masterclasses/(?:[1-4]\.\d{2}-[A-Z]|N-[A-Z]\d{2})/audio/masterclass\.mp3',file.relative_to(r).as_posix()):
  # Only the finished *lesson-specific* Torsten High MP3 is allowed here.
  # A timeline must bind the MP3 to the same manually edited source lesson.
  folder=file.parent.parent
  manifest=folder/'audio/timeline.json'
  source=folder/'script.json'
  if not source.is_file() or not manifest.is_file():
   errors.append('Masterclass audio missing source or sample timeline: '+str(folder))
  else:
   t=json.loads(manifest.read_text(encoding='utf8'))
   sc=json.loads(source.read_text(encoding='utf8'))
   if (t.get('audio_sha256')!=hashlib.sha256(file.read_bytes()).hexdigest()
       or t.get('source_sha256')!=hashlib.sha256(source.read_bytes()).hexdigest()
       or sc.get('lesson_id')!=folder.name
       or not 15<=len(t.get('beats',[]))<=50
       or not 110<float(t.get('duration_seconds',0))<450
       or file.stat().st_size>=9_000_000):
    errors.append('Masterclass MP3 SHA/timing/source mismatch: '+str(folder))
  continue
 if file.suffix.lower()=='.mp3' and file.relative_to(r).as_posix()=='master-103-b/audio/masterclass.mp3':
  # Narrow exception: one published 2:34 masterclass asset required by offline PWA.
  # Verify checksum, cue count, duration and a conservative size cap.
  manifest=r/'master-103-b/audio/timeline.json'
  if not manifest.is_file():
   errors.append('Master MP3 lacks a timeline manifest')
  else:
   m=json.loads(manifest.read_text(encoding='utf8'))
   digest=hashlib.sha256(file.read_bytes()).hexdigest()
   if (digest!=m.get('audio_sha256') or len(m.get('beats',[]))!=24 or
       not 115<float(m.get('duration_seconds',0))<260 or file.stat().st_size>6_000_000):
    errors.append('Master MP3 failed SHA/size/timing audit')
  continue
 if file.suffix.lower() in ('.pem','.p12','.pfx','.mp3','.wav','.ogg') or file.name in ('.env',):errors.append('Sensitive or raw audio file: '+str(file.relative_to(r)))
for f in ['.gitignore','.github/workflows/publish.yml','GITHUB_UPLOAD_ANLEITUNG.md','AUDIO_MEHRSTUFENPLAN.md','tools/build_site.py']:
 if not (r/f).exists():errors.append('Missing GitHub kit: '+f)
print('Repository preflight:',len(errors),'errors')
for e in errors:print('ERROR:',e)
if errors:sys.exit(1)
