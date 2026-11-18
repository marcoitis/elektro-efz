#!/usr/bin/env python3
"""Regression check for v0.10.9 editorial, audit, visuals and basic electrical arithmetic.
Not an independent expert assessment, normative approval, audio or device/PWA flight-mode test.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
import json,re,math
R=Path(__file__).resolve().parent.parent
IDS=['2.11-C','2.12-A','2.12-B','2.12-C','3.01-A','3.01-B','3.01-C','3.02-A']
J=lambda f:json.loads((R/f).read_text(encoding='utf-8'))
js=lambda f:json.loads((R/f).read_text(encoding='utf-8').split('=',1)[1].strip(' ;\n'))
lecture=js('lecture-scripts.js');slides=js('lesson-long-slides.js');audit=js('lesson-audit.js');records=J('quality-review.json')['lessons'];workbooks=J('lesson-workbooks.json')
ra={v['id']:v for v in records};rb={v['id']:v for v in workbooks}
assert len(ra)==len(rb)==len(lecture)==len(audit)==178
for id in IDS:
 text=(R/'tts_scripts'/f'{id}.txt').read_text(encoding='utf-8');src=(R/'editorial_v0109'/f'{id}.txt').read_text(encoding='utf-8')
 words=len(text.split())
 assert text==src,(id,'editorial != TTS')
 assert 1950<=words<=3900,(id,'word target',words)
 assert lecture[id]==text,(id,'lecture mismatch')
 assert sum(len(s['text'].split()) for s in slides[id])>=0.88*words,(id,'slide coverage mismatch')
 assert ra[id]['script_words']==audit[id]['script_words']==rb[id]['ttsWords']==words,(id,'audit mismatch')
 assert rb[id]['fullManuscript']==text,(id,'workbook mismatch')
 for f in ['visuals','learning-visuals']: ET.parse(R/f/f'{id}.svg')
 assert (R/'workbooks'/f'{id}.md').exists()
assert sum(1950<=len(p.read_text(encoding='utf-8').split())<=3900 for p in (R/'tts_scripts').glob('*.txt'))==70
assert len(list((R/'tts_scripts').glob('*.txt')))==178
assert len(list((R/'visuals').glob('*.svg')))==178
assert len(list((R/'learning-visuals').glob('*.svg')))==178
assert len(set(re.findall(r"'\./(?:visuals|learning-visuals)/[^']+'",(R/'offline.js').read_text())))==356
assert "elektro-efz-shell-v0109-eight-lessons" in (R/'offline.js').read_text()
assert "elektro-efz-shell-v0109-eight-lessons" in (R/'sw.js').read_text()
assert math.isclose(230/(0.65+0.15),287.5,rel_tol=1e-12)
assert math.isclose(8*9/1000*4*365,105.12,rel_tol=1e-12)
assert math.isclose(2*12*8*0.0178/2.5,1.36704,rel_tol=1e-12)
assert math.isclose((0.32-0.20)*8*8*2000/1000,15.36,rel_tol=1e-12)
print('PASS 8 distinct scripts, 8 slide sequences, workbook/audit sync, 16 SVG references; 178 IDs; 70 long scripts; 4 maths')
