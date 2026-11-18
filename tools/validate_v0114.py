#!/usr/bin/env python3
"""Structural audit for v0.11.4 – not electrical, legal or normative certification."""
from pathlib import Path
import json,xml.etree.ElementTree as ET, math
R=Path(__file__).resolve().parent.parent
IDS=['4.06-C','4.07-A','4.07-B','4.07-C','4.08-A','4.08-B','4.08-C','4.09-A','4.09-B','4.09-C','4.10-A','4.10-B']
J=lambda p:json.loads((R/p).read_text(encoding='utf-8'))
JS=lambda p:json.loads((R/p).read_text(encoding='utf-8').split('=',1)[1].strip(' ;\n'))
lectures=JS('lecture-scripts.js');slides=JS('lesson-long-slides.js');audit=JS('lesson-audit.js');q=J('quality-review.json');qr={r['id']:r for r in q['lessons']};books={r['id']:r for r in J('lesson-workbooks.json')};data=JS('data.js')
assert q['version']=='v0.11.4';assert len(data['lessons'])==145
assert len(lectures)==len(audit)==len(qr)==len(books)==178
assert len(list((R/'tts_scripts').glob('*.txt')))==178
assert len(list((R/'visuals').glob('*.svg')))==len(list((R/'learning-visuals').glob('*.svg')))==178
counts={}
for lid in IDS:
 txt=(R/'tts_scripts'/(lid+'.txt')).read_text(encoding='utf-8');n=len(txt.split());counts[lid]=n
 assert 1950<=n<=3900,(lid,n)
 assert txt==(R/'editorial_v0114'/(lid+'.txt')).read_text(encoding='utf-8')
 assert lectures[lid]==txt.strip()
 assert qr[lid]['script_words']==audit[lid]['script_words']==books[lid]['ttsWords']==n
 assert books[lid]['fullManuscript']==txt
 assert not qr[lid]['normaussagen_freigegeben'] and not qr[lid]['fachliche_einzelpruefung']
 assert len(slides[lid])>=25 and all(len(s['text'].split())<=155 for s in slides[lid])
 assert sum(len(s['text'].split())+len(s['heading'].split()) for s in slides[lid])>=.98*n,(lid,'slide discrepancy')
 assert 'Individuell redigiertes Fachmanuskript (v0.11.4)' in (R/'workbooks'/(lid+'.md')).read_text(encoding='utf-8')
 for folder in ('visuals','learning-visuals'):
  img=R/folder/(lid+'.svg');ET.parse(img)
  assert 'didaktisches' in img.read_text(encoding='utf-8').lower()
assert sum(1950<=len(p.read_text(encoding='utf-8').split())<=3900 for p in (R/'tts_scripts').glob('*.txt'))==130
assert 'elektro-efz-shell-v0114-twelve-lessons' in (R/'sw.js').read_text()
assert 'elektro-efz-shell-v0114-twelve-lessons' in (R/'offline.js').read_text()
assert all(math.isclose(a,b,rel_tol=1e-6) for a,b in [
 (86*1.08,92.88),(1850+32*78,4346),(2400+28*82+6*95+320,5586),
 (42*(1+.0028*35),46.116),(41*(1+.003*30)*12,536.28),
 (10*32*18,5760),(2100/6000,.35),(2100/8400,.25),
 (78-9-6,63),(24/100*40,9.6),(230*4*.8,736),
 (230*4*.6,552),(400*8*.85*3**.5,4711.178),
 (24/12,2),(24/.9,26.6666666667)])
print('PASS v0.11.4: 12 manuscripts synchronized with source, TTS, slides, workbooks and audit; 130/178 at target length; 12 valid SVGs; arithmetic checks passed')
print('WORD COUNTS:',counts)
print('NEW SLIDE CHAPTERS:',sum(len(slides[x]) for x in IDS))
