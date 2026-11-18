#!/usr/bin/env python3
"""Package v0.9.7, compare changed files to the authoritative full v0.9.6 archive.
No protected norm PDFs, test audio, or downloaded voice-model files are published.
"""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from base64 import b64encode
import hashlib,json,csv
R=Path(__file__).resolve().parent.parent; O=R.parent
BASE=O/'Elektro_EFZ_v0.9.6_Vollstaendiger_Quellcode.zip'
ids=['1.07-A','1.07-B','1.07-C','1.08-A','1.08-B','1.08-C']
EXCLUDED={'.audio-cache','.voice-cache','.probe-audio-v096','.probe-audio-v097','dist','dist-v096-probe','dist-v097-probe','__pycache__','.git','.pytest_cache','node_modules'}
allfiles=[]
for f in R.rglob('*'):
 if not f.is_file():continue
 rp=f.relative_to(R)
 if any(p in EXCLUDED for p in rp.parts):continue
 if f.name.startswith(('preview_','testshot_','norm_check_')):continue
 if f.suffix.lower() in {'.pdf','.onnx','.mp3','.pyc','.jpeg','.jpg','.webp'}:continue
 allfiles.append(rp)
allfiles=sorted(set(allfiles))
with ZipFile(BASE) as old:
 baseline={info.filename:hashlib.sha256(old.read(info.filename)).digest() for info in old.infolist() if not info.is_dir()}
changed=[p for p in allfiles if hashlib.sha256((R/p).read_bytes()).digest()!=baseline.get(p.as_posix())]
# A complete package with all 178 lessons must be correctly covered
assert len(list((R/'tts_scripts').glob('*.txt')))==178
assert len(list((R/'visuals').glob('*.svg')))==178
assert len(list((R/'learning-visuals').glob('*.svg')))==178
review=json.loads((R/'quality-review.json').read_text())['lessons']
assert len(review)==178 and sum(x['15_to_30_minute_target'] for x in review)==27

def pack(name,paths):
 paths=sorted(set(Path(x) for x in paths))
 out=O/name
 with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=6) as z:
  for p in paths:
   f=R/p
   if not f.is_file():raise FileNotFoundError(f)
   z.write(f,str(p))
 with ZipFile(out) as z:
  assert z.testzip() is None
  assert len(z.namelist())==len(paths)
 print(out.name,len(paths),'files',round(out.stat().st_size/1024),'KiB')
 return out
pack('Elektro_EFZ_v0.9.7_Vollstaendiger_Quellcode.zip',allfiles)
pack('Elektro_EFZ_v0.9.7_Patch_ab_v0.9.6.zip',changed)
webfiles=[p for p in changed if len(p.parts)==1 or p.parts[0]=='workbooks']
voicefiles=[p for p in changed if p.parts[0] in ('editorial_v097','tts_scripts')]
visualfiles=[p for p in changed if p.parts[0] in ('visuals','learning-visuals')]
toolfiles=[p for p in changed if p.parts[0] in ('tools','.github')]
pack('Elektro_EFZ_v0.9.7_Web_und_Lernmappen.zip',webfiles)
pack('Elektro_EFZ_v0.9.7_Neue_Sprechertexte.zip',voicefiles)
pack('Elektro_EFZ_v0.9.7_Fachgrafiken.zip',visualfiles)
pack('Elektro_EFZ_v0.9.7_Werkzeuge_und_Workflow.zip',toolfiles)
# portable preview: embed all the learn visual images rather than relying on adjacent folders
html=(R/'kurskompass.html').read_text('utf8')
for f in sorted((R/'learning-visuals').glob('*.svg')):
 html=html.replace('./learning-visuals/'+f.name,'data:image/svg+xml;base64,'+b64encode(f.read_bytes()).decode())
(O/'Elektro_EFZ_v0.9.7_Unterricht_Offline_Vorschau.html').write_text(html,'utf8')
with (O/'Elektro_EFZ_v0.9.7_Status_aller_178_Lektionen.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,delimiter=';')
 w.writerow(['Lektion','Titel','Wörter','Geschätzte Sprecherzeit bei 130 W/min','15–30-Minuten-Ziel','Neue Fachzeichnung v0.9.7','Normativ freigegeben'])
 for x in review:w.writerow([x['id'],x['title'],x['script_words'],x['tts_minutes_estimate_130wpm'],'ja' if x['15_to_30_minute_target'] else 'nein','ja' if x['id'] in ids else 'bestehende Zeichnung','nein'])
(O/'Elektro_EFZ_v0.9.7_Qualitaetsbericht.md').write_text((R/'RELEASE_v097_DE.md').read_text('utf8'),'utf8')
(O/'Elektro_EFZ_v0.9.7_GitHub_Update_Anleitung.md').write_text((R/'UPDATE_v097_DE.md').read_text('utf8'),'utf8')
(O/'Elektro_EFZ_v0.9.7_Workflow.txt').write_text((R/'.github/workflows/publish.yml').read_text('utf8'),'utf8')
print('Changed file count:',len(changed))
print('Standalone preview bytes:',(O/'Elektro_EFZ_v0.9.7_Unterricht_Offline_Vorschau.html').stat().st_size)
print('Sample changed:',*[str(p) for p in changed[:36]],sep='\n - ')
