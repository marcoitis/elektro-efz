#!/usr/bin/env python3
"""Draft-only consistency audit for lesson 1.01-B; not a normative or listening approval."""
import hashlib
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
lesson = "1.01-B"
base = root / "masterclasses" / lesson
script = json.loads((base / "script.json").read_text(encoding="utf-8"))
timeline = json.loads((base / "audio" / "timeline.json").read_text(encoding="utf-8"))
visuals = (base / "visuals.js").read_text(encoding="utf-8")
catalog = json.loads((root / "masterclasses" / "catalog.json").read_text(encoding="utf-8"))
beats = script["beats"]
assert script["lesson_id"] == lesson
assert "24-beat masterclass narration" in script["source"]
assert "long-form course manuscript reference" in script["source"]
assert timeline["lesson_id"] == script["id"]
assert timeline["voice"] == "Piper de_DE-thorsten-high"
assert timeline["alignment"] == "beat_exact_via_PCM_frame_count_not_word_aligned"
assert timeline["approval"] == "technical_verified_not_acoustically_or_normatively_signed_off"
assert timeline["tts_source_sha256"] == hashlib.sha256((root / "tts_scripts/1.01-B.txt").read_bytes()).hexdigest()
assert timeline["course_data_sha256"] == hashlib.sha256((root / "data.js").read_bytes()).hexdigest()
assert timeline["duration_samples"] == timeline["beats"][-1]["end_sample"]
assert script["normative_review"]["status"] == "pending_independent_expert_review"
assert "ESTI_407_0526_d.pdf" in script["source_urls"][0]
narration_text = " ".join(b["text"].lower() for b in beats)
assert "kein nachweis dafür, dass eine berührung ungefährlich wäre" in narration_text
# The required negated sentence above prevents a false safety guarantee.
assert len(beats) == len(timeline["beats"]) == 24
assert len({b["visual"] for b in beats}) == 24
assert all(b["id"] == f"{i:02}" for i, b in enumerate(beats, 1))
assert all(b["text"].strip() == t["narration"].strip() and b["visual"] == t["visual"]
           for b, t in zip(beats, timeline["beats"]))
assert all(re.search(r'["\']' + re.escape(b["visual"]) + r'["\']\s*:', visuals)
           for b in beats), "A scene key is missing in visuals.js"
assert all(b["duration"] > 0 for b in timeline["beats"])
for previous, current in zip(timeline["beats"], timeline["beats"][1:]):
    assert previous["end_sample"] == current["start_sample"]
    assert abs(current["start"] - current["start_sample"] / timeline["sample_rate"]) < 1e-7
assert abs(timeline["beats"][-1]["end"] - timeline["pcm_duration_seconds"]) < 1e-7
assert abs(timeline["beats"][-1]["end"] - timeline["duration_seconds"]) < 0.25
# Assert the actual lesson-specific renderer contract, not obsolete CSS/SVG
# class names from an earlier prototype. The scene keys above are the source
# of truth and each beat must resolve to a dedicated scene.
assert "window.EFZ_MasterRenderers['1.01-B']" in visuals
assert "function render(key)" in visuals
assert 'viewBox="0 0 960 540"' in visuals
assert 'role="img"' in visuals and 'aria-label=' in visuals
# Scene-key coverage is already checked above with both quote styles; do not duplicate it with an over-escaped regex.
assert "mc-illustration" in visuals
assert all(x in visuals for x in ["mc-flow","mc-arc","mc-draw","mc-pulse"])
assert "prefers-reduced-motion:reduce" in visuals
audio = (base / "audio" / "masterclass.mp3")
assert audio.stat().st_size > 100_000
assert hashlib.sha256(audio.read_bytes()).hexdigest() == timeline["audio_sha256"]
entry = next(x for x in catalog["lessons"] if x["id"] == lesson)
assert entry["status"] == "pending", "Draft must not be published before manual approval"
assert entry["audio_review"] == "pending_manual"
assert entry["didactic_review"] == "pending_manual"
print(f"{lesson}: 24 narrated scenes and PCM timeline consistent; manual approvals still pending")
