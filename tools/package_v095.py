#!/usr/bin/env python3
"""Split release archives for browser-based GitHub uploads. No norm PDFs or licensed full text."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from base64 import b64encode
import json,csv,hashlib
R=Path(__file__).resolve().parent.parent
O=R.parent
IDS=('1.09-A','1.09-B','1.09-C','1.10-A','1.10-B','1.10-C')
SKIP={'.audio-cache','.voice-cache','.probe-audio','dist','dist-v095-probe','dist-v094-probe','dist-probe','.git','__pycache__','.pytest_cache','node_modules'}
def pack(name,items):
 dest=O/name
 names=sorted(set(str(p) for p in items))
 with ZipFile(dest,'w',compression=ZIP_DEFLATED,compresslevel=6) as z:
  for path in names:
   p=R/path
   if not p.is_file():raise FileNotFoundError(p)
   z.write(p,path)
 with ZipFile(dest) as z:
  bad=z.testzip()
  if bad:raise RuntimeError((name,bad))
 print(name,'files',len(names),'KiB',round(dest.stat().st_size/1024))
all_files=[p.relative_to(R) for p in R.rglob('*') if p.is_file() and not any(c in SKIP for c in p.relative_to(R).parts) and not p.name.startswith('preview_') and p.suffix.lower() not in {'.pdf','.png','.mp3','.onnx','.pyc'}]
# Package only owned, unlicensed code, teaching and public-source notes. No full standards.
all_files += [Path('icon-192.png'),Path('icon-512.png')]
pack('Elektro_EFZ_v0.9.5_Vollstaendiger_Quellcode.zip',all_files)
web=['index.html','app.js','sw.js','offline.js','manifest.webmanifest','lecture-scripts.js','lesson-long-slides.js','lesson-audit.js','lesson-workbooks.json','kurskompass.html','quality-review.json','quality-review.csv','v095-physics-check.json','PHYSIK_QUELLENABGLEICH_v095.md','RELEASE_v095_DE.md']
pack('Elektro_EFZ_v0.9.5_Web_App.zip',web)
pack('Elektro_EFZ_v0.9.5_Sprechertexte.zip',[Path('editorial_v095')/(id+'.txt') for id in IDS]+[Path('tts_scripts')/(id+'.txt') for id in IDS])
pack('Elektro_EFZ_v0.9.5_Abbildungen.zip',[Path(sub)/(id+'.svg') for id in IDS for sub in ('visuals','learning-visuals')])
tools=['install_editorial_samples.py','create_long_slides.py','create_quality_matrix.py','create_178_workbooks.py','create_schematics_v095.py','quality_check_multimedia.py','build_course_compass.py','build_site.py','verify_foundations_v094.py','verify_physics_v095.py','test_v095_browser.py']
pack('Elektro_EFZ_v0.9.5_Werkzeuge.zip',[Path('tools')/name for name in tools]+[Path('.github/workflows/publish.yml')])
patch=set(web)|{'.github/workflows/publish.yml','QUALITAETSMATRIX_README.md','UPDATE_v095_DE.md'}
patch.update(str(p) for p in [Path('tools')/name for name in tools]);patch.update(str(Path('editorial_v095')/(id+'.txt')) for id in IDS);patch.update(str(Path('tts_scripts')/(id+'.txt')) for id in IDS);patch.update(str(Path(sub)/(id+'.svg')) for id in IDS for sub in ('visuals','learning-visuals'))
pack('Elektro_EFZ_v0.9.5_Patch_ab_v0.9.4.zip',patch)
# standalone workbook preview: link SVGs are embedded as data URIs. Only preview, not an install package.
preview=(R/'kurskompass.html').read_text('utf8')
for f in sorted((R/'learning-visuals').glob('*.svg')):
 uri='data:image/svg+xml;base64,'+b64encode(f.read_bytes()).decode()
 preview=preview.replace('./learning-visuals/'+f.name,uri)
preview=preview.replace('← Zur Lernplattform','Lokale Offline-Vorschau')
(O/'Elektro_EFZ_v0.9.5_Unterricht_Offline_Vorschau.html').write_text(preview,'utf8')
rows=json.loads((R/'quality-review.json').read_text('utf8'))['lessons']
with (O/'Elektro_EFZ_v0.9.5_Status_178_Lektionen.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,delimiter=';');w.writerow(['Lektion','Titel','Woerter','Sprechdauer_130_WpM','Ziel_15_bis_30_Min','Eigene_Fachzeichnung_in_v095','Normativ_einzeln_freigegeben'])
 for x in rows:w.writerow([x['id'],x['title'],x['script_words'],x['tts_minutes_estimate_130wpm'],'Ja' if x['15_to_30_minute_target'] else 'Nein','Ja' if x['id'] in IDS else 'Vorhandene Grafik','Nein'])
assert len(rows)==178
assert sum(x['15_to_30_minute_target'] for x in rows)==15
assert len(list((R/'visuals').glob('*.svg')))==178
print('v095 preview MiB',round((O/'Elektro_EFZ_v0.9.5_Unterricht_Offline_Vorschau.html').stat().st_size/1024**2,2))
