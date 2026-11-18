#!/usr/bin/env python3
"""Repeatable browser-upload archive preparation for v0.9.6; excludes copyrighted PDFs and test audio."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from base64 import b64encode
import json,csv
R=Path(__file__).resolve().parent.parent; O=R.parent
IDS=['1.05-A','1.05-B','1.05-C','1.06-A','1.06-B','1.06-C']
EXCLUDE={'.audio-cache','.voice-cache','.probe-audio','.probe-audio-v096','dist','dist-v094-probe','dist-v095-probe','dist-v096-probe','__pycache__','.git','.pytest_cache','node_modules'}
def pack(name,paths):
 paths=sorted(set(Path(x) for x in paths))
 dest=O/name
 with ZipFile(dest,'w',ZIP_DEFLATED,compresslevel=6) as z:
  for path in paths:
   f=R/path
   if not f.is_file():raise FileNotFoundError(f)
   z.write(f,str(path))
 with ZipFile(dest) as z:assert z.testzip() is None,name
 print(name,len(paths),'files',round(dest.stat().st_size/1024),'KiB')
 return dest
allfiles=[]
for f in R.rglob('*'):
 if not f.is_file():continue
 rp=f.relative_to(R)
 if any(p in EXCLUDE for p in rp.parts):continue
 if f.name.startswith(('preview_','testshot_')):continue
 if f.suffix.lower() in {'.pdf','.onnx','.mp3','.pyc','.jpeg','.jpg','.webp'}:continue
 allfiles.append(rp)
pack('Elektro_EFZ_v0.9.6_Vollstaendiger_Quellcode.zip',allfiles)
core=['index.html','app.js','sw.js','offline.js','lesson-long-slides.js','lecture-scripts.js','lesson-audit.js','kurskompass.html','lesson-workbooks.json','quality-review.json','quality-review.csv','RELEASE_v096_DE.md','FACHQUELLEN_ABGLEICH_v096.md','v096-materials-documents-check.json','UPDATE_v096_DE.md']
pack('Elektro_EFZ_v0.9.6_Web_Root.zip',core)
texts=[Path(sub)/(id+'.txt') for sub in ('editorial_v096','tts_scripts') for id in IDS]
pack('Elektro_EFZ_v0.9.6_Sprechertexte.zip',texts)
charts=[Path(sub)/(id+'.svg') for sub in ('visuals','learning-visuals') for id in IDS]
pack('Elektro_EFZ_v0.9.6_Grafiken.zip',charts)
tools=[Path('tools')/f for f in ('install_editorial_samples.py','create_long_slides.py','create_quality_matrix.py','create_178_workbooks.py','create_schematics_v096.py','build_course_compass.py','build_site.py','integrate_v096.py','verify_materials_docs_v096.py','verify_physics_v095.py','test_v096_browser.py','quality_check_multimedia.py')]
pack('Elektro_EFZ_v0.9.6_Build_Werkzeuge.zip',tools+[Path('.github/workflows/publish.yml')])
patch=set(map(Path,core))|set(texts)|set(charts)|set(tools)|{Path('.github/workflows/publish.yml'),Path('QUALITAETSMATRIX_README.md')}
pack('Elektro_EFZ_v0.9.6_Patch_ab_v0.9.5.zip',patch)
preview=(R/'kurskompass.html').read_text('utf8')
for f in sorted((R/'learning-visuals').glob('*.svg')):
 preview=preview.replace('./learning-visuals/'+f.name,'data:image/svg+xml;base64,'+b64encode(f.read_bytes()).decode())
(O/'Elektro_EFZ_v0.9.6_Unterricht_Offline_Vorschau.html').write_text(preview.replace('← Zur Lernplattform','Lokale Offline-Vorschau'),'utf8')
rows=json.loads((R/'quality-review.json').read_text('utf8'))['lessons']
with (O/'Elektro_EFZ_v0.9.6_Status_178_Lektionen.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,delimiter=';');w.writerow(['Lektion','Titel','Woerter','Sprechdauer_130_WpM','Ziel_15_bis_30_Min','Individuelle_SVG_Fachtafel_v096','Normativ_unabhaengig_freigegeben'])
 for x in rows:w.writerow([x['id'],x['title'],x['script_words'],x['tts_minutes_estimate_130wpm'],'ja' if x['15_to_30_minute_target'] else 'nein','ja' if x['id'] in IDS else 'bisherige', 'nein'])
(O/'Elektro_EFZ_v0.9.6_Workflow.txt').write_text((R/'.github/workflows/publish.yml').read_text('utf8'),'utf8')
(O/'Elektro_EFZ_v0.9.6_Qualitaetsbericht.md').write_text((R/'RELEASE_v096_DE.md').read_text('utf8'),'utf8')
(O/'Elektro_EFZ_v0.9.6_Update_Anleitung.md').write_text((R/'UPDATE_v096_DE.md').read_text('utf8'),'utf8')
assert len(rows)==178 and sum(x['15_to_30_minute_target'] for x in rows)==21
print('Standalone preview size MiB:',round((O/'Elektro_EFZ_v0.9.6_Unterricht_Offline_Vorschau.html').stat().st_size/1024**2,2))
