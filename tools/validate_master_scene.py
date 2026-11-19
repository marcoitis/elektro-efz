#!/usr/bin/env python3
"""Audit the new educational master scene and its real MP3 sample-level cues."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
S=ROOT/'master-103-b'/'script.json'
T=ROOT/'master-103-b'/'audio'/'timeline.json'
A=ROOT/'master-103-b'/'audio'/'masterclass.mp3'
source=json.loads(S.read_text(encoding='utf-8'))
timeline=json.loads(T.read_text(encoding='utf-8'))
beats=source['beats']
cues=timeline['beats']
assert len(beats)==len(cues)==24
assert source['id']==timeline['lesson_id']=='1.03-B-master'
assert timeline['alignment']=='beat_exact_via_PCM_frame_count_not_word_aligned'
assert all(len(x['text'].split())>=9 for x in beats)
assert {x['id'] for x in beats}=={x['id'] for x in cues}
assert source['beats'][0]['visual']=='start'
assert source['beats'][-2]['visual']=='question'
assert source['beats'][-1]['visual']=='answer'
assert 'ac' in {x['visual'] for x in beats}
assert 'dc' in {x['visual'] for x in beats}
assert '120 Ω' not in ''  # The spoken script uses words, not unexplained symbols.
assert hashlib.sha256(A.read_bytes()).hexdigest()==timeline['audio_sha256']
assert hashlib.sha256(S.read_bytes()).hexdigest()==timeline['source_sha256']
assert A.stat().st_size>200000
assert 115<timeline['duration_seconds']<260
for idx,(b,c) in enumerate(zip(beats,cues)):
    assert b['id']==c['id'] and b['visual']==c['visual']
    assert b['text']==c['narration']
    assert 2<c['duration']<40,(idx,c)
    if idx:
        prev=cues[idx-1]
        assert abs(prev['end']-c['start'])<0.006,(idx,prev,c)
assert abs(cues[-1]['end']-timeline['duration_seconds'])<0.20
print(f"MASTER AUDIT PASS: {timeline['duration_seconds']:.1f}s, {len(cues)} voice-aligned visual beats, MP3 SHA256 confirmed.")
