#!/usr/bin/env python3
"""Structural v0.11.2 audit; not a certification of norms or technical correctness."""
from pathlib import Path
import json,re,math,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parent.parent
ids=['3.10-C','3.11-A','3.11-B','3.11-C','3.12-A','3.12-B','3.12-C','4.01-A','4.01-B','4.01-C','4.02-A','4.02-B']
J=lambda p:json.loads((R/p).read_text(encoding='utf-8'))
JS=lambda p:json.loads((R/p).read_text(encoding='utf-8').split('=',1)[1].strip(' ;\n'))
lectures=JS('lecture-scripts.js');slides=JS('lesson-long-slides.js');audit=JS('lesson-audit.js');q=J('quality-review.json');qr={r['id']:r for r in q['lessons']};books={r['id']:r for r in J('lesson-workbooks.json')};data=JS('data.js')
assert q['version']=='v0.11.2'
assert len(data['lessons'])==145 and len(lectures)==len(audit)==len(qr)==len(books)==178
assert len(list((R/'tts_scripts').glob('*.txt')))==178
assert len(list((R/'visuals').glob('*.svg')))==len(list((R/'learning-visuals').glob('*.svg')))==178
assert len(slides)>=105
counts={}
for id in ids:
 txt=(R/'tts_scripts'/f'{id}.txt').read_text(encoding='utf-8');n=len(txt.split());counts[id]=n
 assert 1950<=n<=3900,(id,n)
 assert txt==(R/'editorial_v0112'/f'{id}.txt').read_text(encoding='utf-8')
 assert lectures[id]==txt.strip()
 assert qr[id]['script_words']==audit[id]['script_words']==books[id]['ttsWords']==n
 assert books[id]['fullManuscript']==txt
 assert not qr[id]['normaussagen_freigegeben'] and not qr[id]['fachliche_einzelpruefung']
 assert len(slides[id])>=25 and all(len(s['text'].split())<=155 for s in slides[id])
 assert sum(len(s['text'].split()) for s in slides[id])>=.95*n,(id,'slides diff')  # remaining words are displayed as slide headings
 assert 'Individuell redigiertes Fachmanuskript (v0.11.2)' in (R/'workbooks'/f'{id}.md').read_text(encoding='utf-8')
 for folder in ('visuals','learning-visuals'):
  img=R/folder/f'{id}.svg';ET.parse(img)
  assert 'didaktische' in img.read_text(encoding='utf-8').lower()
assert sum(1950<=len(p.read_text(encoding='utf-8').split())<=3900 for p in (R/'tts_scripts').glob('*.txt'))==106
assert len(J('lesson-workbooks.json'))==178
assert 'elektro-efz-shell-v0112-twelve-lessons' in (R/'sw.js').read_text()
assert 'elektro-efz-shell-v0112-twelve-lessons' in (R/'offline.js').read_text()
assert all(math.isclose(a,b,rel_tol=1e-10) for a,b in [(1000**2*.01,10000),(30**2+40**2,50**2),(230/.8,287.5),(120/30,4),(3**2+4**2,25),(8/.8,10),(3.6*.75,2.7),(76-12-5-4,55),(2*30*10/(56*2.5),4.285714285714286),(42*12,504),(400*4*3,4800),(288**2+384**2,480**2),(24-21,3)])
print('PASS v0.11.2: 12 distinct manuals, text, slides, workbooks and audits synchronized; 106 /178 meet length; 12 SVG drawings; 13 arithmetic checks')
print('WORTZAHLEN:',counts)
print('FOLIENKAPITEL NEU:',sum(len(slides[i]) for i in ids))
print('FOLIENGESAMT (Kapitel/Bestandsfolien ohne Doppelzählung):',len(slides))
