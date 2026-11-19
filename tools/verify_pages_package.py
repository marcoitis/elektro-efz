#!/usr/bin/env python3
"""Asserts Pages artifact includes every key page + both complete SVG sets.
Not a browser test, audio certification or NIN normative review.
"""
from pathlib import Path
import argparse,json,sys,re
p=argparse.ArgumentParser();p.add_argument('--site',default='dist');a=p.parse_args()
r=Path(__file__).resolve().parent.parent;site=r/a.site
required=['index.html','kurskompass.html','vertiefung-151.html','fachvertiefung-151.html','sw.js','offline.js','video-pilot.js','video-pilot.css','audio-manifest.json','version.json','manifest.webmanifest','.nojekyll']
errors=[]
for f in required:
 if not (site/f).is_file():errors.append('Missing '+f)
for name in ['visuals','learning-visuals']:
 n=len(list((site/name).glob('*.svg')))
 if n!=178:errors.append(f'{name}: {n} instead of 178 SVG')
for name in ('index.html','kurskompass.html','vertiefung-151.html','fachvertiefung-151.html'):
 if (site/name).exists() and (site/name).stat().st_size<2000:errors.append('Suspicious small page '+name)
manifest=json.loads((site/'audio-manifest.json').read_text(encoding='utf-8'))
if manifest.get('tracks') and not manifest.get('baseUrl') and not all((site/entry).is_file() for entry in manifest['tracks'].values()):errors.append('manifest points at missing MP3')
sw=(site/'sw.js').read_text(encoding='utf-8')
for f in ('kurskompass.html','vertiefung-151.html','fachvertiefung-151.html','audio-manifest.json'):
 if f not in sw:errors.append('SW missing '+f)
if "new URL('./',location.href)" not in (site/'offline.js').read_text(encoding='utf-8'):errors.append('Offline base path no longer relative')
keys=[]
for fn in ('sw.js','offline.js'):
 m=re.search(r'elektro-efz-shell-github-[0-9a-f]{14}',(site/fn).read_text(encoding='utf8'))
 if not m:errors.append('Pages cache not fingerprinted in '+fn)
 else:keys.append(m.group(0))
if len(set(keys))>1:errors.append('Mismatched SW/offline cache keys')
if not (site/'manifest.webmanifest').is_file():errors.append('Missing PWA manifest')
print(f'Pages package: {sum(p.stat().st_size for p in site.rglob("*") if p.is_file())/1024**2:.1f} MiB')
print('Pages package checks:',len(errors),'errors')
for e in errors:print('ERROR:',e)
if errors:sys.exit(1)
