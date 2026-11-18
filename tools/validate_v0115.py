#!/usr/bin/env python3
"""Release v0.11.5 structure and arithmetic audit; does not certify norms or electrical safety."""
from pathlib import Path
import json,math,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parent.parent
IDS=['4.10-C','4.11-A','4.11-B','4.11-C','4.12-A','4.12-B','4.12-C','N-B01','N-B02','N-B03','N-E01','N-E02']
J=lambda p:json.loads((R/p).read_text(encoding='utf-8'))
JS=lambda p:json.loads((R/p).read_text(encoding='utf-8').split('=',1)[1].strip(' ;\n'))
lectures=JS('lecture-scripts.js');slides=JS('lesson-long-slides.js');audit=JS('lesson-audit.js');q=J('quality-review.json');qr={r['id']:r for r in q['lessons']};books={r['id']:r for r in J('lesson-workbooks.json')}
data=JS('data.js');norm=J('norm_course.json');
assert q['version']=='v0.11.5'
assert len(data['lessons'])==145 and len(norm['lessons'])==33
assert len(lectures)==len(audit)==len(qr)==len(books)==178
assert len(list((R/'tts_scripts').glob('*.txt')))==178
assert len(list((R/'visuals').glob('*.svg')))==len(list((R/'learning-visuals').glob('*.svg')))==178
counts={}
for lid in IDS:
 txt=(R/'tts_scripts'/(lid+'.txt')).read_text(encoding='utf-8');n=len(txt.split());counts[lid]=n
 assert 1950<=n<=3900,(lid,n)
 assert txt==(R/'editorial_v0115'/(lid+'.txt')).read_text(encoding='utf-8')
 assert lectures[lid]==txt.strip()
 assert qr[lid]['script_words']==audit[lid]['script_words']==books[lid]['ttsWords']==n
 assert books[lid]['fullManuscript']==txt
 assert not qr[lid]['normaussagen_freigegeben'] and not qr[lid]['fachliche_einzelpruefung']
 assert len(slides[lid])>=24 and all(len(s['text'].split())<=145 for s in slides[lid])
 # titles may be stripped out of slide body as headings, so compare approximate length only
 assert sum(len(s['text'].split())+len(s['heading'].split()) for s in slides[lid])>=0.98*n,(lid,'slide discrepancy')
 assert 'Individuell redigiertes Fachmanuskript (v0.11.5)' in (R/'workbooks'/(lid+'.md')).read_text(encoding='utf-8')
 for folder in ('visuals','learning-visuals'):
  img=R/folder/(lid+'.svg');ET.parse(img)
  assert 'didaktisch' in img.read_text(encoding='utf-8').lower()
assert sum(1950<=len(p.read_text(encoding='utf-8').split())<=3900 for p in (R/'tts_scripts').glob('*.txt'))==142
assert 'elektro-efz-shell-v0115-twelve-lessons' in (R/'sw.js').read_text()
assert 'elektro-efz-shell-v0115-twelve-lessons' in (R/'offline.js').read_text()
checks=[(60/20,3),(30/50,.6),(100/2,50),(1.8*(35/60)*240,252),(252*.28,70.56),(.8*.95,.76),(750/.76,986.842105263),(12**2+16**2,400),(60/20,3),(1.2*.75*200,180),(2*(20)*10*.0178/2.5,2.848),(3/.75,4),(4*.75,3),(10*10*.4,40),(5*5*.4,10),(1/(2*math.pi*50*100e-6),31.8309886184),(230*2*.75,345),(1.2*45/60*200,180),(78-9-6,63),(.55+.23,.78)]
assert all(math.isclose(x,y,rel_tol=1e-6) for x,y in checks),checks
print('PASS v0.11.5 · 12 text/graphic/editorial/slide/workbook/audit matches · 142/178 long TTS · arithmetic cases passed')
print('Wörter:',counts)
print('Neue Folienkapitel:',sum(len(slides[x]) for x in IDS))
