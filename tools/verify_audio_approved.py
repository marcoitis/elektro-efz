#!/usr/bin/env python3
"""Basic approved-file preflight: checks IDs, MP3 headers, approximate size and ffprobe if present.
NOT a substitute for listening, pronunciation review or producer release.
"""
from pathlib import Path
import argparse,subprocess,shutil,sys
R=Path(__file__).resolve().parent.parent
p=argparse.ArgumentParser();p.add_argument('--directory',default='public-audio');a=p.parse_args()
base=R/a.directory;files=list(base.glob('*.mp3')) if base.exists() else []
valid={p.stem for p in (R/'tts_scripts').glob('*.txt')};errors=[]
for f in sorted(files):
 if f.stem not in valid:errors.append('Unbekannte Lektion: '+f.name)
 if f.stat().st_size<4096:errors.append('Zu klein: '+f.name)
 with f.open('rb') as fp:h=fp.read(3)
 if h!=b'ID3' and (len(h)<2 or h[0]!=255 or h[1]&224!=224):errors.append('Kein MP3-Kopf: '+f.name)
 if shutil.which('ffprobe'):
  pr=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(f)],capture_output=True,text=True)
  if pr.returncode!=0:errors.append('FFprobe Fehler: '+f.name)
  else:
   try:
    duration=float(pr.stdout.strip());print(f'{f.name}: {duration/60:.1f} min, {f.stat().st_size/1024**2:.1f} MiB')
    if duration<5*60 or duration>45*60:errors.append('Unplausible Länge: '+f.name)
   except ValueError:errors.append('Kein Duration-Wert: '+f.name)
print(f'Audio preflight: {len(files)} MP3 files; {len(errors)} errors; acoustic approval remains manual')
for e in errors:print('ERROR',e)
if errors:sys.exit(1)
