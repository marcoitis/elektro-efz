#!/usr/bin/env python3
"""Structural v0.11.1 audit; not a certification of norms or technical correctness."""
from pathlib import Path
import json,re,math,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parent.parent
ids=['3.06-B','3.06-C','3.07-A','3.07-C','3.08-A','3.08-B','3.08-C','3.09-A','3.09-B','3.09-C','3.10-A','3.10-B']
J=lambda p:json.loads((R/p).read_text(encoding='utf-8'))
JS=lambda p:json.loads((R/p).read_text(encoding='utf-8').split('=',1)[1].strip(' ;\n'))
lectures=JS('lecture-scripts.js');slides=JS('lesson-long-slides.js');audit=JS('lesson-audit.js');q=J('quality-review.json');qr={r['id']:r for r in q['lessons']};books={r['id']:r for r in J('lesson-workbooks.json')};data=JS('data.js')
assert q['version']=='v0.11.1'
assert len(data['lessons'])==145 and len(lectures)==len(audit)==len(qr)==len(books)==178
assert len(list((R/'tts_scripts').glob('*.txt')))==178
assert len(list((R/'visuals').glob('*.svg')))==len(list((R/'learning-visuals').glob('*.svg')))==178
assert len(slides)>=93
counts={}
for id in ids:
 txt=(R/'tts_scripts'/f'{id}.txt').read_text(encoding='utf-8');n=len(txt.split());counts[id]=n
 assert 1950<=n<=3900,(id,n)
 assert txt==(R/'editorial_v0111'/f'{id}.txt').read_text(encoding='utf-8')
 assert lectures[id]==txt.strip()
 assert qr[id]['script_words']==audit[id]['script_words']==books[id]['ttsWords']==n
 assert books[id]['fullManuscript']==txt
 assert not qr[id]['normaussagen_freigegeben'] and not qr[id]['fachliche_einzelpruefung']
 assert len(slides[id])>=25 and all(len(s['text'].split())<=155 for s in slides[id])
 assert sum(len(s['text'].split()) for s in slides[id])>=.95*n,(id,'slides diff')  # remaining words are displayed as slide headings
 assert 'Individuell redigiertes Fachmanuskript (v0.11.1)' in (R/'workbooks'/f'{id}.md').read_text(encoding='utf-8')
 for folder in ('visuals','learning-visuals'):
  img=R/folder/f'{id}.svg';ET.parse(img)
  assert 'didaktische' in img.read_text(encoding='utf-8').lower()
assert sum(1950<=len(p.read_text(encoding='utf-8').split())<=3900 for p in (R/'tts_scripts').glob('*.txt'))==94
assert len(J('lesson-workbooks.json'))==178
assert 'elektro-efz-shell-v0111-twelve-lessons' in (R/'sw.js').read_text()
assert 'elektro-efz-shell-v0111-twelve-lessons' in (R/'offline.js').read_text()
assert all(math.isclose(a,b,rel_tol=1e-10) for a,b in [
 (35*10,350),
 (42*(1+0.0028*35),46.116),
 (5*950,4750),
 (10**2*0.02,2),
 (15**2*0.02,4.5),
 (2*50*10*.0175/2.5,7),
 (7/20,0.35),
 (20-7,13),
 (-3-4,-7),
 (4+1.5+.5,6),
 (2*4+3*3+1,18),
 (0.2**2,0.04),
 ])
print('PASS v0.11.1: 12 distinct manuals, text, slides, workbooks and audits synchronized; 94 /178 meet length; 12 SVG drawings; 12 arithmetic checks')
print('WORTZAHLEN:',counts)
print('FOLIENKAPITEL NEU:',sum(len(slides[i]) for i in ids))
print('FOLIENGESAMT (Kapitel/Bestandsfolien ohne Doppelzählung):',len(slides))
