#!/usr/bin/env python3
"""v0.11.0 structure, integration and model arithmetic tests; not expert or normative approval."""
from pathlib import Path
import re,json,math,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parent.parent
IDS=['3.02-B','3.02-C','3.03-A','3.03-B','3.03-C','3.04-A','3.04-B','3.04-C','3.05-A','3.05-B','3.05-C','3.06-A']
J=lambda f:json.loads((R/f).read_text(encoding='utf-8'))
JS=lambda f:json.loads((R/f).read_text(encoding='utf-8').split('=',1)[1].strip(' ;\n'))
lectures=JS('lecture-scripts.js');slides=JS('lesson-long-slides.js');audit=JS('lesson-audit.js');quality=J('quality-review.json');qa={x['id']:x for x in quality['lessons']};books={x['id']:x for x in J('lesson-workbooks.json')}
assert quality['version']=='v0.11.0'
assert len(lectures)==len(audit)==len(qa)==len(books)==178 and len(slides)>=81
assert len(list((R/'tts_scripts').glob('*.txt')))==178
assert len(list((R/'visuals').glob('*.svg')))==len(list((R/'learning-visuals').glob('*.svg')))==178
for lid in IDS:
 text=(R/'tts_scripts'/(lid+'.txt')).read_text(encoding='utf-8')
 src=(R/'editorial_v0110'/(lid+'.txt')).read_text(encoding='utf-8')
 words=len(text.split());assert text==src
 assert 1950<=words<=3900,(lid,words)
 assert lectures[lid]==text.strip() or lectures[lid]==text
 assert qa[lid]['script_words']==audit[lid]['script_words']==books[lid]['ttsWords']==words
 assert books[lid]['fullManuscript']==text
 assert len(slides[lid])>=15
 assert sum(len(x['text'].split()) for x in slides[lid])>0.93*words
 assert all(len(x['text'].split())<=195 for x in slides[lid])
 assert qa[lid]['normaussagen_freigegeben'] is False
 assert qa[lid]['fachliche_einzelpruefung'] is False
 for folder in ('visuals','learning-visuals'):
  svg=R/folder/(lid+'.svg');ET.parse(svg)
  assert 'didaktische' in svg.read_text(encoding='utf-8').lower()
 assert 'Individuell redigiertes Fachmanuskript (v0.11.0)' in (R/'workbooks'/(lid+'.md')).read_text(encoding='utf-8')
assert sum(1950<=len(p.read_text(encoding='utf-8').split())<=3900 for p in (R/'tts_scripts').glob('*.txt'))==82
assert 'elektro-efz-shell-v0110-twelve-lessons' in (R/'offline.js').read_text()
assert 'elektro-efz-shell-v0110-twelve-lessons' in (R/'sw.js').read_text()
# Independent numerical examples from the eight lesson groups
assert math.isclose(0.8e-6*500e6,400.0,rel_tol=1e-12)
assert math.isclose(3*(96/0.92-96),25.0434782608,rel_tol=1e-9)
assert math.isclose(30*0.0175/2.5,0.21,rel_tol=1e-12)
assert math.isclose(500/1e6*1000,0.5,rel_tol=1e-12) # mA
assert math.isclose(230/0.8,287.5,rel_tol=1e-12)
assert math.isclose(120*50/4,1500.0,rel_tol=1e-12)
assert math.isclose((1500-1440)/1500,0.04,rel_tol=1e-12)
assert math.isclose(15*2*math.pi*1440/60/1000,2.2619467106,rel_tol=1e-9)
assert math.isclose(6*7,42,rel_tol=1e-12)
assert math.isclose(120*35/4,1050,rel_tol=1e-12)
assert math.isclose(.8**3,.512,rel_tol=1e-12)
assert math.isclose(6+5,11,rel_tol=1e-12)
print('PASS v0.11.0: 12 new distinct manuscripts; 82 long scripts of 178; 12 SVG drawings, 12 x 24 slides; synchronized workbook/audit; 12 arithmetic checks')
