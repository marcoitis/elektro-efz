#!/usr/bin/env python3
"""Prepare a clean GitHub Pages artifact, including only valid MP3 tracks."""
from pathlib import Path
import argparse,json,shutil,subprocess
ROOT=Path(__file__).resolve().parent.parent
CORE=['index.html','styles.css','data.js','storage.js','reviews.js','exercises.js','audio-engine.js','cloud.js','offline.js','trainer.js','simulator.js','norms.js','norm-course.js','app.js','sw.js','manifest.webmanifest','icon-192.png','icon-512.png']
VOICE='Piper de_DE-thorsten-high (CC0 Dataset)'

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',default='.audio-cache');p.add_argument('--site',default='dist');p.add_argument('--mode',choices=['all','probe'],default='all');args=p.parse_args()
 site=ROOT/args.site;site.mkdir(parents=True,exist_ok=True)
 for name in CORE:
  f=ROOT/name
  if not f.is_file():raise SystemExit('Erforderliche App-Datei fehlt: '+name)
  shutil.copy2(f,site/name)
 audio_src=ROOT/args.source;audio_dst=site/'audio';audio_dst.mkdir(exist_ok=True)
 scripts=sorted((ROOT/'tts_scripts').glob('*.txt'))
 audio={}
 for f in scripts:
  source=audio_src/(f.stem+'.mp3')
  if not source.is_file() or source.stat().st_size<4096:continue
  dest=audio_dst/source.name
  shutil.copy2(source,dest)
  audio[f.stem]='./audio/'+source.name
 if args.mode=='all' and len(audio)!=len(scripts):
  raise SystemExit(f'Unvollständige Produktion: {len(audio)} von {len(scripts)} Audiodateien – Veröffentlichung abgebrochen.')
 if args.mode=='probe' and len(audio)<3:raise SystemExit('Nicht alle drei Pilot-Dateien erzeugt')
 manifest={'version':'0.8','voice':VOICE,'generated':len(audio),'description':'Kostenfreie offline-geeignete MP3-Dateien.','tracks':audio}
 (site/'audio-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
 size=sum(f.stat().st_size for f in (audio_dst.glob('*.mp3')))
 print(f'Fertig: {len(audio)} MP3s, {size/1024**2:.1f} MiB, App-Dateien: {len(CORE)}')
 print('Die eigentlichen Audiodateien müssen nicht in das Git-Repository commitet werden.')

if __name__=='__main__':main()
