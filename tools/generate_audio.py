#!/usr/bin/env python3
"""Offline-lesson audio for a GitHub Pages artifact; no paid TTS or credentials.

Works with Piper CLI + a separately downloaded, CC0 Thorsten voice model.
Only builds changed/missing tracks. All audio is 64kbit/s mono MP3.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

VOICE = "de_DE-thorsten-high"
PILOT = {"1.01-A", "1.03-B", "3.07-A"}

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scripts", default="tts_scripts")
    parser.add_argument("--model", default=f".voice-cache/{VOICE}.onnx")
    parser.add_argument("--config", default=f".voice-cache/{VOICE}.onnx.json")
    parser.add_argument("--output", default=".audio-cache")
    parser.add_argument("--mode", choices=["all", "probe"], default="probe")
    parser.add_argument("--ids", default="", help="Comma-separated lesson IDs for a reviewed small batch")
    parser.add_argument("--piper", default="piper")
    parser.add_argument("--ffmpeg", default="ffmpeg")
    args = parser.parse_args()
    inp, out = Path(args.scripts), Path(args.output)
    model, cfg = Path(args.model), Path(args.config)
    if not model.is_file() or not cfg.is_file():
        raise SystemExit("Fehler: Stimmmodell oder zugehörige JSON-Konfiguration fehlt.")
    files = sorted(inp.glob("*.txt"))
    if len(files) != 178:
        raise SystemExit(f"178 Unterrichtsskripte erwartet, {len(files)} gefunden")
    if args.ids:
        selected={x.strip() for x in args.ids.split(",") if x.strip()}
        files=[f for f in files if f.stem in selected]
        if len(files)!=len(selected):raise SystemExit("Unknown lesson IDs in --ids")
    elif args.mode == "probe":
        files = [f for f in files if f.stem in PILOT]
        if len(files) != len(PILOT):
            raise SystemExit("Drei Pilotlektionen fehlen")
    out.mkdir(parents=True, exist_ok=True)
    index_path=out/'build-index.json'
    try: index=json.loads(index_path.read_text(encoding='utf-8'))
    except (FileNotFoundError,json.JSONDecodeError): index={}
    if not isinstance(index,dict):index={}
    nextindex=dict(index)
    failures=[]
    done=0
    for k,f in enumerate(files,1):
        lid=f.stem
        content=f.read_bytes()
        text=content.decode('utf-8-sig').strip()
        key=sha(content+VOICE.encode()+b'|lesson-audio-v080')
        path=out/(lid+'.mp3')
        if path.exists() and path.stat().st_size>=4096 and index.get(lid)==key:
            print(f"[{k}/{len(files)}] {lid}: bereits vorhanden",flush=True)
            continue
        print(f"[{k}/{len(files)}] {lid}: erzeuge MP3 ...",flush=True)
        try:
            with tempfile.TemporaryDirectory(prefix='efz-tts-') as td:
                wav=Path(td)/'lesson.wav'
                tts=subprocess.run([args.piper,'--model',str(model),'--config',str(cfg),'--output_file',str(wav)],input=text.encode('utf-8'),stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=900)
                if tts.returncode!=0 or not wav.is_file() or wav.stat().st_size<2048:
                    raise RuntimeError('Piper fehlgeschlagen: '+tts.stderr.decode('utf-8','replace')[-1500:])
                candidate=out/(lid+'.new.mp3')
                cmd=[args.ffmpeg,'-nostdin','-hide_banner','-loglevel','error','-y','-i',str(wav),'-af','loudnorm=I=-18:LRA=9:TP=-2','-ac','1','-ar','24000','-codec:a','libmp3lame','-b:a','64k',str(candidate)]
                enc=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=300)
                if enc.returncode!=0 or not candidate.exists() or candidate.stat().st_size<4096:
                    raise RuntimeError('FFmpeg fehlgeschlagen: '+enc.stderr.decode('utf8','replace')[-1500:])
                os.replace(candidate,path)
                nextindex[lid]=key
                index_path.write_text(json.dumps(nextindex,ensure_ascii=False,sort_keys=True,indent=2),encoding='utf8')
                done+=1
        except Exception as err:
            failures.append((lid,str(err)))
            print(f"ERROR {lid}: {err}",file=sys.stderr,flush=True)
    index_path.write_text(json.dumps(nextindex,ensure_ascii=False,sort_keys=True,indent=2),encoding='utf8')
    print(f"Neu erstellt: {done}; gültige MP3-Dateien: {len(list(out.glob('*.mp3')))}; Fehler: {len(failures)}")
    if failures:
        raise SystemExit('Audioerzeugung unvollständig: '+', '.join(k for k,_ in failures))

if __name__ == '__main__':main()
