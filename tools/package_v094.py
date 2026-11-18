#!/usr/bin/env python3
"""Publish safe code bundles only: no third-party norms, no test MP3, no downloaded models."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,csv,base64,shutil
R=Path(__file__).resolve().parent.parent
O=Path('/mnt/data')
LID=['1.03-A','1.03-C','1.03-D','1.04-A','1.04-B','1.04-C']

def pack(fn,paths):
 paths=sorted(set(Path(p) for p in paths))
 with ZipFile(O/fn,'w',compression=ZIP_DEFLATED,compresslevel=8) as z:
  for p in paths:
   assert (R/p).is_file(),(fn,p)
   assert p.suffix.lower() not in ('.pdf','.mp3','.onnx'),p
   z.write(R/p,arcname=str(p))
  assert z.testzip() is None
 print(fn,len(paths),'files',round((O/fn).stat().st_size/1024),'KiB')

all_scripts=sorted((R/'tts_scripts').glob('*.txt'))
assert len(all_scripts)==178
all_svg=sorted((R/'visuals').glob('*.svg'))
assert len(all_svg)==178
all_folios=sorted((R/'learning-visuals').glob('*.svg'))
assert len(all_folios)==178
paths=[p.relative_to(R) for p in R.rglob('*') if p.is_file() and not any(q in ['.probe-audio','.audio-cache','dist-v094-probe','dist-probe','.voice-cache','__pycache__','.git'] for q in p.relative_to(R).parts) and p.suffix.lower() not in ('.png','.pdf','.mp3','.onnx') and p.name not in ('50110-1-extracted.txt','test-inline.js')]
# Icons need to remain in the full archive; only generic screenshot PNGs are excluded.
paths += [Path('icon-192.png'),Path('icon-512.png')]
pack('Elektro_EFZ_v0.9.4_Vollstaendiger_Quellcode.zip',paths)
app=['index.html','styles.css','studio.css','kurskompass.html','data.js','storage.js','reviews.js','exercises.js','audio-engine.js','cloud.js','offline.js','trainer.js','simulator.js','norms.js','norm-course.js','academy-content.js','chapters.js','academy.js','studio.js','studio-examples-extra.js','lecture-scripts.js','lesson-audit.js','lesson-long-slides.js','app.js','sw.js','manifest.webmanifest','icon-192.png','icon-512.png','lesson-visuals.json','quality-review.json','quality-review.csv','norm_course.json','lesson-workbooks.json']
pack('Elektro_EFZ_v0.9.4_Web_App.zip',app)
pack('Elektro_EFZ_v0.9.4_Build_Werkzeuge.zip',[p.relative_to(R) for p in (R/'tools').glob('*.py')])
pack('Elektro_EFZ_v0.9.4_Fachmanuskripte.zip',[p.relative_to(R) for d in ['editorial_v092','editorial_v094'] for p in (R/d).glob('*.txt')])
pack('Elektro_EFZ_v0.9.4_Sprechertexte_A.zip',[p.relative_to(R) for p in all_scripts[:89]])
pack('Elektro_EFZ_v0.9.4_Sprechertexte_B.zip',[p.relative_to(R) for p in all_scripts[89:]])
# Both the full learning schematics and normal visual links are included.
pack('Elektro_EFZ_v0.9.4_Grafiken_A.zip',[p.relative_to(R) for p in all_svg[:89]+all_folios[:89]])
pack('Elektro_EFZ_v0.9.4_Grafiken_B.zip',[p.relative_to(R) for p in all_svg[89:]+all_folios[89:]])
patch=['index.html','sw.js','offline.js','manifest.webmanifest','lecture-scripts.js','lesson-long-slides.js','quality-review.json','quality-review.csv','lesson-audit.js','lesson-workbooks.json','kurskompass.html','.github/workflows/publish.yml']
patch += [Path('visuals')/(lid+'.svg') for lid in LID]
patch += [Path('learning-visuals')/(lid+'.svg') for lid in LID]
patch += [Path('tts_scripts')/(lid+'.txt') for lid in LID]
patch += [Path('editorial_v094')/(lid+'.txt') for lid in LID]
patch += [Path('tools')/p for p in ['create_schematics_v094.py','install_editorial_samples.py','create_long_slides.py','create_quality_matrix.py','create_178_workbooks.py','build_course_compass.py','build_site.py','quality_check_multimedia.py','validate_v092.py','validate_v093.py','verify_foundations_v094.py']]
pack('Elektro_EFZ_v0.9.4_Patch_ab_v0.9.3.zip',patch)

# Complete and image-embedded offline preview for reviewing study maps.
preview=(R/'kurskompass.html').read_text('utf8')
for art in all_folios:
 raw=art.read_bytes()
 preview=preview.replace('./learning-visuals/'+art.name,'data:image/svg+xml;base64,'+base64.b64encode(raw).decode())
preview=preview.replace('← Zur Lernplattform','Lokale Offline-Vorschau')
(O/'Elektro_EFZ_v0.9.4_Unterricht_Offline_Vorschau.html').write_text(preview,'utf8')

rows=json.loads((R/'quality-review.json').read_text('utf8'))['lessons']
with (O/'Elektro_EFZ_v0.9.4_Status_178_Lektionen.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,delimiter=';')
 w.writerow(['Lektion','Titel','Woerter','Sprechdauer_130_Woerter_Min','15-30min_Text','Unabhaengige_Normenfreigabe','Schaltbildstatus'])
 for x in rows:
  status='Fachliche Lernschaltung konstruiert, nicht unabhängig freigegeben' if x['id'] in LID else 'Lernbild oder bisherige Visualisierung, nicht unabhängig freigegeben'
  w.writerow([x['id'],x['title'],x['script_words'],x['tts_minutes_estimate_130wpm'],'Ja' if x['15_to_30_minute_target'] else 'Nein','Nein',status])
assert sum(x['15_to_30_minute_target'] for x in rows)==9
print('Standalone preview KiB',round((O/'Elektro_EFZ_v0.9.4_Unterricht_Offline_Vorschau.html').stat().st_size/1024))
