#!/usr/bin/env python3
"""Creates a static Pages artifact. NEVER synthesizes audio or installs a model.
Modes: text (default); partial (only manually approved MP3); all (requires 178 MP3).
"""
from pathlib import Path
import argparse,json,shutil,sys,hashlib,re
ROOT=Path(__file__).resolve().parent.parent
CORE=['index.html','styles.css','studio.css','kurskompass.html','vertiefung-151.html','fachvertiefung-151.html','data.js','storage.js','reviews.js','exercises.js','audio-engine.js','cloud.js','offline.js','trainer.js','simulator.js','norms.js','norm-course.js','academy-content.js','chapters.js','academy.js','studio.js','studio-examples-extra.js','lecture-scripts.js','lesson-audit.js','lesson-long-slides.js','app.js','sw.js','version.json','manifest.webmanifest','icon-192.png','icon-512.png','404.html','.nojekyll']

def build(mode='text',audio_dir='public-audio',site_dir='dist'):
 dest=ROOT/site_dir
 if dest.resolve()==ROOT:raise SystemExit('Refusing to overwrite repository root')
 if dest.exists():shutil.rmtree(dest)
 dest.mkdir(parents=True)
 for fn in CORE:
  f=ROOT/fn
  if not f.is_file():raise SystemExit('Required app file missing: '+fn)
  shutil.copy2(f,dest/fn)
 # Change cache identity whenever published application source changes, even if
 # an editor forgets to edit the Service Worker version manually. This is
 # applied only to dist/; the source tree keeps its validated release marker.
 fp=hashlib.sha256()
 for fn in sorted(CORE):
  if (ROOT/fn).is_file():fp.update(fn.encode()+b'\0'+(ROOT/fn).read_bytes())
 cache_key='elektro-efz-shell-github-'+fp.hexdigest()[:14]
 for fn in ('sw.js','offline.js'):
  page=dest/fn;value=page.read_text(encoding='utf8')
  value,n=re.subn(r'elektro-efz-shell-v0118-github-ready-1',cache_key,value)
  if n!=1:raise SystemExit('Expected exactly one old cache key in '+fn)
  page.write_text(value,encoding='utf8')
 for folder in ('visuals','learning-visuals'):
  assets=sorted((ROOT/folder).glob('*.svg'))
  if len(assets)!=178:raise SystemExit(f'Expected 178 SVGs in {folder}; found {len(assets)}')
  (dest/folder).mkdir()
  for f in assets:shutil.copy2(f,dest/folder/f.name)
 known={f.stem for f in (ROOT/'tts_scripts').glob('*.txt')}
 if len(known)!=178:raise SystemExit('178 TTS source texts required')
 tracks={};audio_root=ROOT/audio_dir
 if mode in ('partial','all'):
  if not audio_root.is_dir():raise SystemExit('Approved audio directory missing: '+str(audio_root))
  for f in sorted(audio_root.glob('*.mp3')):
   if f.stem not in known:raise SystemExit('Unknown audio lesson: '+f.name)
   if f.stat().st_size<4096:raise SystemExit('Audio unexpectedly small: '+f.name)
   with f.open('rb') as fp:prefix=fp.read(3)
   if prefix!=b'ID3' and (len(prefix)<2 or prefix[0]!=255 or prefix[1]&224!=224):raise SystemExit('Invalid MP3 header: '+f.name)
   (dest/'audio').mkdir(exist_ok=True)
   shutil.copy2(f,dest/'audio'/f.name);tracks[f.stem]='./audio/'+f.name
 if mode=='all' and len(tracks)!=178:raise SystemExit(f'Audio is incomplete: {len(tracks)}/178')
 if mode=='remote':
  manifest_source=json.loads((ROOT/'audio-manifest.json').read_text(encoding='utf8'))
  from urllib.parse import urlparse
  base=manifest_source.get('baseUrl','')
  if not base or urlparse(base).scheme!='https':raise SystemExit('Remote audio requires HTTPS baseUrl in audio-manifest.json')
  if any(k not in known for k in manifest_source.get('tracks',{})):raise SystemExit('Remote audio manifest has unknown lesson IDs')
  tracks=manifest_source.get('tracks',{})
 manifest={'version':'0.11.9','voice':manifest_source.get('voice','Thorsten High (automatisch vertont)') if mode=='remote' else ('Lokale, freigegebene MP3s' if tracks else 'Noch keine freigegebene Aufnahme'),'generated':len(tracks),'status':manifest_source.get('status','rendered-not-acoustically-reviewed') if mode=='remote' else ('partial' if tracks and len(tracks)<178 else ('complete' if tracks else 'text-first')), 'baseUrl':manifest_source['baseUrl'] if mode=='remote' else '', 'tracks':tracks}
 (dest/'audio-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 total=sum(p.stat().st_size for p in dest.rglob('*') if p.is_file())
 if total>900*1024**2:raise SystemExit('Pages upload would exceed prudent 900 MiB limit. Use remote object storage for audio.')
 print(f'Pages-Website bereit: {dest}; {total/1024**2:.1f} MiB; {len(tracks)}/178 MP3; Modus={mode}')
 return dest

if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--mode',choices=['text','partial','all','remote'],default='text')
 p.add_argument('--audio-dir',default='public-audio')
 p.add_argument('--site',default='dist')
 a=p.parse_args();build(a.mode,a.audio_dir,a.site)
