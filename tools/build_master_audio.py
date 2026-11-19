#!/usr/bin/env python3
"""Generate one truly scene-aligned Thorsten High teaching film narration.

The input is a 24-beat *new*, compact masterclass manuscript.
Each beat is synthesized individually and decoded as WAV, so the exact
audio sample count (rather than assumed word positions) determines cue timing.
The WAVs are concatenated as PCM before encoding the continuous MP3. This
is NOT a word-for-word alignment and is labelled accordingly.

Audio output: master-103-b/audio/masterclass.mp3
Timing output: master-103-b/audio/timeline.json
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "master-103-b" / "script.json"
OUT = ROOT / "master-103-b" / "audio"
MODEL = ROOT / ".voice-cache" / "de_DE-thorsten-high.onnx"
CONFIG = ROOT / ".voice-cache" / "de_DE-thorsten-high.onnx.json"
MODEL_HASH = "9df1c43c61149ef9b39e618e2b861fbe41e1fcea9390b2dac62e8761573ea4f1"


def run(command, **kwargs):
    try:
        return subprocess.run(command, check=True, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, **kwargs)
    except subprocess.CalledProcessError as exc:
        print(exc.stderr.decode("utf-8", errors="replace")[-3000:], file=sys.stderr)
        raise


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    script = json.loads(SOURCE.read_text(encoding="utf-8"))
    beats = script["beats"]
    assert script["id"] == "1.03-B-master"
    assert len(beats) == 24 and len({b["id"] for b in beats}) == len(beats)
    assert all(len(b["text"].split()) >= 9 for b in beats)
    assert sha256(MODEL) == MODEL_HASH, "Unverified voice model!"
    assert CONFIG.is_file()
    OUT.mkdir(parents=True, exist_ok=True)
    frames_total = 0
    sample_rate = None
    timing = []
    with tempfile.TemporaryDirectory(prefix="master-103-b-") as td:
        work = Path(td)
        paths = []
        for i, beat in enumerate(beats):
            source = work / f"beat-{i+1:02}.wav"
            input_bytes = (beat["text"].strip() + "\n").encode("utf-8")
            run(["piper", "--model", str(MODEL), "--config", str(CONFIG),
                 "--output_file", str(source), "--length_scale", "1.04",
                 "--sentence_silence", "0.22"], input=input_bytes, timeout=200)
            with wave.open(str(source), "rb") as wav:
                assert wav.getnchannels() == 1
                assert wav.getsampwidth() == 2
                sr = wav.getframerate()
                assert sr in (22050, 24000), sr
                if sample_rate is None:
                    sample_rate = sr
                assert sr == sample_rate
                frames = wav.getnframes()
            if frames < sr * 2:
                raise AssertionError(f"Narration beat {beat['id']} suspiciously short")
            timing.append({
                "id": beat["id"], "visual": beat["visual"],
                "start": round(frames_total / sr, 3),
                "duration": round(frames / sr, 3),
                "end": round((frames_total + frames) / sr, 3),
                "narration": beat["text"],
            })
            frames_total += frames
            paths.append(source)
            print(f"BEAT {beat['id']}/{len(beats)}: {frames/sr:.2f}s · {beat['visual']}", flush=True)
        # Stitch *PCM samples* in order, no MP3 frame drift at internal beats.
        pcm = work / "master.wav"
        with wave.open(str(pcm), "wb") as output:
            output.setnchannels(1)
            output.setsampwidth(2)
            output.setframerate(sample_rate)
            for part in paths:
                with wave.open(str(part), "rb") as input:
                    output.writeframes(input.readframes(input.getnframes()))
        audio = OUT / "masterclass.mp3"
        run(["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y",
             "-i", str(pcm), "-af", "loudnorm=I=-18:LRA=9:TP=-2",
             "-ac", "1", "-ar", "22050", "-codec:a", "libmp3lame",
             "-b:a", "128k", str(audio)], timeout=240)
    info = json.loads(run(["ffprobe", "-v", "error", "-show_entries",
                          "format=duration,size:stream=codec_name,channels,sample_rate",
                          "-of", "json", str(audio)]).stdout.decode())
    length = float(info["format"]["duration"])
    expected = frames_total / sample_rate
    assert abs(length - expected) < 0.20, (length, expected)
    assert info["streams"][0]["codec_name"] == "mp3"
    assert int(info["streams"][0]["channels"]) == 1
    assert 115 < length < 260, "Master sequence should be a few minutes"
    assert audio.stat().st_size < 6_000_000
    timeline = {
        "version": 1,
        "lesson_id": script["id"],
        "voice": "Piper de_DE-thorsten-high",
        "model_sha256": MODEL_HASH,
        "source_sha256": sha256(SOURCE),
        "audio_sha256": sha256(audio),
        "duration_seconds": round(length, 3),
        "sample_rate": 22050,
        "alignment": "beat_exact_via_PCM_frame_count_not_word_aligned",
        "approval": "technically_verified_not_acoustically_or_didactically_signed_off",
        "beats": timing,
    }
    (OUT / "timeline.json").write_text(
        json.dumps(timeline, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    assert all(timing[i+1]["start"] >= timing[i]["end"]-0.002
               for i in range(len(timing)-1))
    print(f"MASTER COMPLETE: {length:.2f}s, {audio.stat().st_size}B, "
          f"{len(timing)} exactly aligned audio beats")


if __name__ == "__main__":
    main()
