#!/usr/bin/env python3
"""One-masterclass production gate: verifies narration and PCM cue signatures."""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main(lesson):
    assert re.fullmatch(r'(?:[1-4]\.\d{2}-[A-Z]|N-[A-Z]\d{2})',lesson)
    folder=ROOT/'masterclasses'/lesson
    sc=folder/'script.json'
    tl=folder/'audio/timeline.json'
    mp3=folder/'audio/masterclass.mp3'
    assert sc.is_file() and tl.is_file() and mp3.is_file()
    script=json.loads(sc.read_text())
    time=json.loads(tl.read_text())
    beats=script['beats']
    cues=time['beats']
    assert script['lesson_id']==lesson and time['lesson_id']==lesson+'-master'
    assert time['alignment']=='beat_exact_via_PCM_frame_count_not_word_aligned'
    assert 15<=len(beats)==len(cues)<=50
    assert time['source_sha256']==sha(sc)
    assert time['audio_sha256']==sha(mp3)
    assert 200000<mp3.stat().st_size<9000000
    assert 110<time['duration_seconds']<450
    for n,(s,c) in enumerate(zip(beats,cues)):
        assert s['id']==c['id'] and s['visual']==c['visual']
        assert s['text']==c['narration']
        assert 2<c['duration']<60
        if n:assert abs(cues[n-1]['end']-c['start'])<.006
    assert abs(cues[-1]['end']-time['duration_seconds'])<.3
    assert beats[-2]['visual']=='question' and beats[-1]['visual']=='answer'
    print(f'PASS {lesson}: {len(beats)} curated beats; {time["duration_seconds"]:.1f}s mono MP3 verified, sample-level starts')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--lesson',required=True)
    main(p.parse_args().lesson)
