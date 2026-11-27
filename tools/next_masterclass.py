#!/usr/bin/env python3
"""Resolve exactly one next pending masterclass from catalog + audio batch order."""
import json, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
catalog=json.loads((ROOT/"masterclasses/catalog.json").read_text(encoding="utf-8"))
plan=json.loads((ROOT/"audio-plan/batches.json").read_text(encoding="utf-8"))
status={x["id"]:x["status"] for x in catalog["lessons"]}
ordered=[lesson for batch in sorted(plan["batches"],key=lambda x:x["number"]) for lesson in batch["ids"]]
if len(ordered)!=catalog["total"] or len(set(ordered))!=len(ordered):
    raise SystemExit("FAIL: batches must contain exactly 178 unique lesson IDs")
if set(ordered)!=set(status):
    raise SystemExit("FAIL: catalog and audio batch IDs differ")
pending=[x for x in ordered if status[x]!="ready"]
if not pending:
    print("ALL_READY")
    raise SystemExit(0)
lesson=pending[0]
base=ROOT/"masterclasses"/lesson
required=[base/"script.json",base/"visuals.js",ROOT/"tts_scripts"/(lesson+".txt"),ROOT/"data.js",ROOT/"masterclass.html",ROOT/"masterclasses"/"player.js",ROOT/"tools"/"render_masterclass_sequential.py"]
missing=[str(p.relative_to(ROOT)) for p in required if not p.is_file()]
if missing:
    raise SystemExit("BLOCKED: missing required production inputs: "+", ".join(missing))
script=json.loads((base/"script.json").read_text(encoding="utf-8"))
if script.get("lesson_id")!=lesson or len(script.get("beats",[]))<15:
    raise SystemExit("BLOCKED: lesson script identity or beat count invalid")
if not re.fullmatch(r"(?:[1-4]\\.\\d{2}-[A-Z]|N-[A-Z]\\d{2})",lesson):
    raise SystemExit("BLOCKED: invalid lesson ID")
print(lesson)
