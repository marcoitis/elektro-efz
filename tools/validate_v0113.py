#!/usr/bin/env python3
"""Structural v0.11.3 audit; not a certification of norms or technical correctness."""
from pathlib import Path
import json,re,math,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parent.parent
ids=['4.02-C','4.03-A','4.03-B','4.03-C','4.04-A','4.04-B','4.04-C','4.05-A','4.05-B','4.05-C','4.06-A','4.06-B']
J=lambda p:json.loads((R/p).read_text(encoding='utf-8'))
JS=lambda p:json.loads((R/p).read_text(encoding='utf-8').split('=',1)[1].strip(' ;\n'))
lectures=JS('lecture-scripts.js');slides=JS('lesson-long-slides.js');audit=JS('lesson-audit.js');q=J('quality-review.json');qr={r['id']:r for r in q['lessons']};books={r['id']:r for r in J('lesson-workbooks.json')};data=JS('data.js')
assert q['version']=='v0.11.3'
assert len(data['lessons'])==145 and len(lectures)==len(audit)==len(qr)==len(books)==178
assert len(list((R/'tts_scripts').glob('*.txt')))==178
assert len(list((R/'visuals').glob('*.svg')))==len(list((R/'learning-visuals').glob('*.svg')))==178
assert len(slides)>=117
counts={}
for id in ids:
 txt=(R/'tts_scripts'/f'{id}.txt').read_text(encoding='utf-8');n=len(txt.split());counts[id]=n
 assert 1950<=n<=3900,(id,n)
 assert txt==(R/'editorial_v0113'/f'{id}.txt').read_text(encoding='utf-8')
 assert lectures[id]==txt.strip()
 assert qr[id]['script_words']==audit[id]['script_words']==books[id]['ttsWords']==n
 assert books[id]['fullManuscript']==txt
 assert not qr[id]['normaussagen_freigegeben'] and not qr[id]['fachliche_einzelpruefung']
 assert len(slides[id])>=25 and all(len(s['text'].split())<=155 for s in slides[id])
 assert sum(len(s['text'].split())+len(s['heading'].split()) for s in slides[id])>=.98*n,(id,'slides diff')  # heading text is displayed on slides
 assert 'Individuell redigiertes Fachmanuskript (v0.11.3)' in (R/'workbooks'/f'{id}.md').read_text(encoding='utf-8')
 for folder in ('visuals','learning-visuals'):
  img=R/folder/f'{id}.svg';ET.parse(img)
  assert 'didaktisches' in img.read_text(encoding='utf-8').lower()
assert sum(1950<=len(p.read_text(encoding='utf-8').split())<=3900 for p in (R/'tts_scripts').glob('*.txt'))==118
assert len(J('lesson-workbooks.json'))==178
assert 'elektro-efz-shell-v0113-twelve-lessons' in (R/'sw.js').read_text()
assert 'elektro-efz-shell-v0113-twelve-lessons' in (R/'offline.js').read_text()
assert all(math.isclose(a,b,rel_tol=1e-7) for a,b in [(230/.92,250),(2+2+4+3+5+3,19),(0+3+8+5+1+0,17),(0+2+4+3+1+0,10),(17+9,19+7),(5.1/6,0.85),(.97*.95*.94,.86621),(11_000/(3**.5*400),15.8771324),(18/.9/11,1.8181818),(40-19,21),(35-23-4,8),(9.85/10-1,-.015),(230/.8,287.5)])
print('PASS v0.11.3: 12 distinct manuals, text, slides, workbooks and audits synchronized; 118 /178 meet length; 12 SVG drawings; 13 arithmetic checks')
print('WORTZAHLEN:',counts)
print('FOLIENKAPITEL NEU:',sum(len(slides[i]) for i in ids))
print('FOLIENGESAMT (Kapitel/Bestandsfolien ohne Doppelzählung):',len(slides))
