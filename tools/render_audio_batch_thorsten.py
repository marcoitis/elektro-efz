#!/usr/bin/env python3
"""Render one of 15 preplanned audio batches using the approved Thorsten High setup.

The source scripts are not edited. Outputs are separate MP3s plus a technical
manifest containing duration, bitrate, source hash and model hash.
Acoustic/fachliche Freigabe is explicitly *not* implied by a successful render.
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
import time
import zipfile

ROOT = Path(__file__).resolve().parent.parent
MODEL = ROOT / ".voice-cache" / "de_DE-thorsten-high.onnx"
CONFIG = ROOT / ".voice-cache" / "de_DE-thorsten-high.onnx.json"
MODEL_SHA256 = "9df1c43c61149ef9b39e618e2b861fbe41e1fcea9390b2dac62e8761573ea4f1"
OUT_ROOT = ROOT / ".audio-production"
RATE = "128k"
VERSION = "elektro-efz-v0.11.8"
VOICE = "de_DE-thorsten-high"

def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as file:
        for buf in iter(lambda: file.read(1024 * 1024), b""):
            h.update(buf)
    return h.hexdigest()

def command(args: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(args, check=True, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, **kwargs)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=int, required=True, help="Batch 1..15")
    args = parser.parse_args()

    plan = json.loads((ROOT / "audio-plan" / "batches.json").read_text(encoding="utf-8"))
    batches = plan["batches"]
    ids = [lesson_id for batch in batches for lesson_id in batch["ids"]]
    sources = sorted((ROOT / "tts_scripts").glob("*.txt"))
    assert len(batches) == 15, f"Expected 15 batches, got {len(batches)}"
    assert len(ids) == 178 and len(set(ids)) == 178, "Plan must cover 178 unique IDs"
    assert {f.stem for f in sources} == set(ids), "Plan/script set mismatch"
    if not 1 <= args.batch <= len(batches):
        raise SystemExit("Batch out of range")

    assert sha_file(MODEL) == MODEL_SHA256, "Unexpected Piper model SHA256"
    assert CONFIG.stat().st_size > 1000, "Missing Piper model configuration"
    print("Authentic Thorsten High model SHA256 verified", flush=True)

    batch = batches[args.batch - 1]
    assert batch["number"] == args.batch
    batch_ids = batch["ids"]
    num = f"{args.batch:02d}"
    out = OUT_ROOT / f"batch-{num}"
    out.mkdir(parents=True, exist_ok=True)
    total = len(batch_ids)
    manifest = {
        "project": VERSION,
        "batch": args.batch,
        "batches_total": len(batches),
        "batch_expected": total,
        "audio_status": "rendered_not_acoustically_approved",
        "voice": VOICE,
        "model_sha256": MODEL_SHA256,
        "encoding": "MP3, 128 kbit/s, mono, 22050 Hz",
        "synthesis": {"length_scale": 1.04, "sentence_silence": 0.35},
        "files": [],
    }

    for idx, lid in enumerate(batch_ids, 1):
        input_file = ROOT / "tts_scripts" / (lid + ".txt")
        output_file = out / (lid + ".mp3")
        raw = input_file.read_text(encoding="utf-8-sig").strip()
        words = len(raw.split())
        if words < 1000:
            raise RuntimeError(f"{lid} seems incomplete: {words} words")
        print(f"[{idx}/{total}] Rendering {lid}: {words} words", flush=True)
        start = time.monotonic()
        with tempfile.TemporaryDirectory(prefix="thorsten-high-") as tmp:
            wave = Path(tmp) / "lesson.wav"
            try:
                command(
                    [
                        "piper", "--model", str(MODEL), "--config", str(CONFIG),
                        "--output_file", str(wave),
                        "--length_scale", "1.04",
                        "--sentence_silence", "0.35",
                    ],
                    input=raw.encode("utf-8"), timeout=2400,
                )
                if not wave.exists() or wave.stat().st_size < 100000:
                    raise RuntimeError("Piper returned no usable WAV file")
                command(
                    [
                        "ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y",
                        "-i", str(wave), "-af", "loudnorm=I=-18:LRA=9:TP=-2",
                        "-ac", "1", "-ar", "22050", "-codec:a", "libmp3lame",
                        "-b:a", RATE, str(output_file),
                    ],
                    timeout=900,
                )
                if not output_file.is_file() or output_file.stat().st_size < 100000:
                    raise RuntimeError("No valid MP3 output")
                probe = json.loads(
                    command(
                        [
                            "ffprobe", "-v", "error", "-show_entries",
                            "format=duration,size:stream=codec_name,channels,sample_rate",
                            "-of", "json", str(output_file)
                        ],
                        timeout=30,
                    ).stdout.decode("utf-8")
                )
                duration = float(probe["format"]["duration"])
                streams = probe["streams"]
                if duration < 180 or streams[0]["codec_name"] != "mp3":
                    raise RuntimeError("MP3 duration or codec invalid")
                if int(streams[0]["channels"]) != 1:
                    raise RuntimeError("MP3 is not mono")
                entry = {
                    "id": lid,
                    "file": output_file.name,
                    "source_words": words,
                    "source_sha256": sha_file(input_file),
                    "mp3_sha256": sha_file(output_file),
                    "duration_seconds": round(duration, 2),
                    "size_bytes": output_file.stat().st_size,
                    "render_seconds": round(time.monotonic()-start, 1),
                    "technical_check": "passed",
                    "acoustic_review": "pending",
                }
                manifest["files"].append(entry)
                print(f"PASS {lid}: {duration / 60:.1f} min, {entry['size_bytes'] / 1048576:.1f} MiB",
                      flush=True)
            except Exception as exc:
                print(f"FAILED {lid}: {exc}", file=sys.stderr, flush=True)
                if isinstance(exc, subprocess.CalledProcessError):
                    print(exc.stderr.decode("utf-8", "replace")[-2500:], file=sys.stderr)
                raise

        (out / f"manifest-{num}.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    assert len(manifest["files"]) == total
    archive = OUT_ROOT / f"Audio_Thorsten_High_Batch_{num}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_STORED, allowZip64=True) as z:
        for entry in manifest["files"]:
            z.write(out / entry["file"], entry["file"])
        z.write(out / f"manifest-{num}.json", f"manifest-{num}.json")

    with zipfile.ZipFile(archive, "r") as z:
        assert z.testzip() is None
        assert len(z.namelist()) == total + 1
    print(f"COMPLETE batch {args.batch}/{len(batches)}: {total} tracks; "
          f"ZIP {archive.stat().st_size/1048576:.1f} MiB", flush=True)

if __name__ == "__main__":
    main()
