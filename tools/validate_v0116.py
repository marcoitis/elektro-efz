#!/usr/bin/env python3
"""v0.11.6 structural, editorial and arithmetic checks; NO normative technical approval."""
from pathlib import Path
import json,math,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parent.parent
IDS=['N-E03','N-I01','N-I02','N-I03','N-S01','N-S02','N-S03','N-S04','N-W01','N-W02','N-W03','N-W04']
J=lambda p:json.loads((R/p).read_text(encoding='utf-8'))
JS=lambda p:json.loads((R/p).read_text(encoding='utf-8').split('=',1)[1].strip(' ;\n'))
lectures=JS('lecture-scripts.js');slides=JS('lesson-long-slides.js');audit=JS('lesson-audit.js');q=J('quality-review.json');qr={r['id']:r for r in q['lessons']};books={r['id']:r for r in J('lesson-workbooks.json')}
data=JS('data.js');norm=J('norm_course.json')
assert q['version']=='v0.11.6'
assert len(data['lessons'])==145 and len(norm['lessons'])==33
assert len(lectures)==len(audit)==len(qr)==len(books)==178
assert len(list((R/'tts_scripts').glob('*.txt')))==178
assert len(list((R/'visuals').glob('*.svg')))==len(list((R/'learning-visuals').glob('*.svg')))==178
counts={}
for lid in IDS:
 txt=(R/'tts_scripts'/(lid+'.txt')).read_text(encoding='utf-8');n=len(txt.split());counts[lid]=n
 assert 1950<=n<=3900,(lid,n)
 assert txt==(R/'editorial_v0116'/(lid+'.txt')).read_text(encoding='utf-8')
 assert lectures[lid]==txt.strip()
 assert qr[lid]['script_words']==audit[lid]['script_words']==books[lid]['ttsWords']==n
 assert books[lid]['fullManuscript']==txt
 assert not qr[lid]['normaussagen_freigegeben'] and not qr[lid]['fachliche_einzelpruefung']
 assert len(slides[lid])>=24 and all(len(s['text'].split())<=145 for s in slides[lid])
 assert sum(len(s['text'].split())+len(s['heading'].split()) for s in slides[lid])>=.98*n,(lid,'slide discrepancy')
 assert 'Individuell redigiertes Fachmanuskript (v0.11.6)' in (R/'workbooks'/(lid+'.md')).read_text(encoding='utf-8')
 for folder in ('visuals','learning-visuals'):
  img=R/folder/(lid+'.svg');ET.parse(img)
  assert 'didaktisch' in img.read_text(encoding='utf-8').lower()
assert sum(1950<=len(p.read_text(encoding='utf-8').split())<=3900 for p in (R/'tts_scripts').glob('*.txt'))==154
assert 'elektro-efz-shell-v0116-twelve-lessons' in (R/'sw.js').read_text()
assert 'elektro-efz-shell-v0116-twelve-lessons' in (R/'offline.js').read_text()
checks={
 'PV power 24*430W kWp':(24*.430,10.32),
 'PV STC voltage 12*50':(12*50,600),
 'PV cold voltage 600*(1+.0028*35)':(600*(1+.0028*35),658.8),
 'PV strings STC MPP 12*42':(12*42,504),
 'PV annual energy 10.32*950':(10.32*950,9804),
 '80A contact 80^2*.001':(80**2*.001,6.4),
 'therm. rise 250/8':(250/8,31.25),
 'PV storage efficiency 7.2/8':(7.2/8,.9),
 'PV day balance 25-8-6':(25-8-6,11),
 '15-min grid injection .5/4':(.5/4,.125),
 '3ph apparent power sqrt3*400*12':(math.sqrt(3)*400*12/1000,8.313843876),
 '3ph active at cos phi .95':(math.sqrt(3)*400*12*.95/1000,7.898151682),
 'machine load simplified 18+12+9+2':(18+12+9+2,41),
 'meter divider 12*5/(10+5)':(12*5/(10+5),4),
 'storage loss 6-5.4':(6-5.4,.6)
}
assert all(math.isclose(x,y,rel_tol=1e-6,abs_tol=1e-6) for x,y in checks.values()),checks
print('PASS v0.11.6: 12 editorial/TTS/slide/workbook/audit/SVG synchronisations; 154/178 long manuscripts.')
print('Words',counts)
print('New slide sections',sum(len(slides[lid]) for lid in IDS),'total',sum(map(len,slides.values())))
print('Arithmetic models passed:',len(checks))
