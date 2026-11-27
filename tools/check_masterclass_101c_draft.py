#!/usr/bin/env python3
"""Draft-specific integrity checks for masterclass 1.01-C."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
lesson='1.01-C'
script=json.loads((ROOT/'masterclasses'/lesson/'script.json').read_text(encoding='utf-8'))
beats=script['beats']
assert script['id']==lesson+'-master' and script['lesson_id']==lesson
assert len(beats)==24
assert [b['id'] for b in beats]==[f'{i:02}' for i in range(1,25)]
assert beats[-2]['visual']=='question' and beats[-1]['visual']=='answer'
assert all(len(b['text'].split())>=14 for b in beats)
assert len({b['visual'] for b in beats})==24
visuals=(ROOT/'masterclasses'/lesson/'visuals.js').read_text(encoding='utf-8')
for beat in beats:
    assert re.search(r"['\"]"+re.escape(beat['visual'])+r"['\"]\s*:",visuals), beat['visual']
assert "EFZ_MasterRenderers['1.01-C']" in visuals
assert 'Keine Anleitung' in script['safety_note']
assert script['normative_review']['status']=='pending_independent_expert_review'
assert any('ESTI_407_0526' in u for u in script['source_urls'])
assert any('84042.D' in u for u in script['source_urls'])
print('PASS 1.01-C draft integrity: 24 unique beats, final question/answer, lesson-specific renderer and source metadata')
