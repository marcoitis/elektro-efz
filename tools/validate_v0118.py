#!/usr/bin/env python3
"""v0.11.8 data consistency, model calculation, file integrity; no fachliche Normenfreigabe."""
from pathlib import Path
import json,math,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parent.parent
IDS=['1.11-C','2.03-C','2.04-B','2.04-C','2.05-A','2.05-B','2.05-C','2.06-A','N-V05','N-V06','N-V07','N-V08']
def js(n):return json.loads((R/n).read_text(encoding='utf-8').split('=',1)[1].strip(' ;\n'))
lectures=js('lecture-scripts.js');slides=js('lesson-long-slides.js');audit=js('lesson-audit.js');q=json.loads((R/'quality-review.json').read_text(encoding='utf-8'));qr={x['id']:x for x in q['lessons']};books={x['id']:x for x in json.loads((R/'lesson-workbooks.json').read_text(encoding='utf-8'))}
assert q['version']=='v0.11.8'
assert len(lectures)==len(audit)==len(qr)==len(books)==len(slides)==178
assert len(list((R/'tts_scripts').glob('*.txt')))==178
assert len(list((R/'visuals').glob('*.svg')))==len(list((R/'learning-visuals').glob('*.svg')))==178
assert len(js('data.js')['lessons'])==145 and len(json.loads((R/'norm_course.json').read_text())['lessons'])==33
counts={p.stem:len(p.read_text(encoding='utf-8').split()) for p in (R/'tts_scripts').glob('*.txt')}
assert len(counts)==178
assert all(1950<=n<=3900 for n in counts.values()),[(lid,n) for lid,n in counts.items() if not 1950<=n<=3900]
for lid in counts:
 n=counts[lid];txt=(R/'tts_scripts'/f'{lid}.txt').read_text(encoding='utf-8');
 assert lectures[lid]==txt.strip(),lid
 assert books[lid]['fullManuscript']==txt,lid
 assert qr[lid]['script_words']==audit[lid]['script_words']==books[lid]['ttsWords']==n,lid
 assert qr[lid]['15_to_30_minute_target'] is audit[lid]['15_to_30_minute_target'] is True,lid
 assert not qr[lid]['normaussagen_freigegeben'] and not qr[lid]['fachliche_einzelpruefung'],lid
for lid in IDS:
 txt=(R/'tts_scripts'/f'{lid}.txt').read_text(encoding='utf-8');n=counts[lid]
 assert txt==(R/'editorial_v0118'/f'{lid}.txt').read_text(encoding='utf-8')
 assert len(slides[lid])>=15 and all(len(s['text'].split())<=145 for s in slides[lid]),(lid,len(slides[lid]))
 assert sum(len(s['text'].split())+len(s['heading'].split()) for s in slides[lid])>=.98*n,(lid,'slide coverage')
 wb=(R/'workbooks'/f'{lid}.md').read_text(encoding='utf-8');assert 'Individuell redigiertes Fachmanuskript (v0.11.8)' in wb
 for folder in ['visuals','learning-visuals']:
  f=R/folder/f'{lid}.svg';ET.parse(f)
  assert 'Didaktisches' in f.read_text(encoding='utf-8')
assert 'elektro-efz-shell-v0118-github-ready-1' in (R/'sw.js').read_text()
assert 'elektro-efz-shell-v0118-github-ready-1' in (R/'offline.js').read_text()
checks={
 'I2t 5000A for 0.1s':((5000**2)*.1,2500000),
 'I2t 5000A for 0.2s':((5000**2)*.2,5000000),
 'fault model 230/0.023':(230/.023,10000),
 'contact heat 100A at 1.5milliohm':(100**2*.0015,15),
 'thermal model 3 devices':(12+18+25,55),
 'assembly losses':(18+6*5+20,68),
 'EV 4 times 11kW':(4*11,44),
 'charge limited to 22kW fraction':(22/44,.5),
 '2300W/230V':(2300/230,10),
 'resistance ratio 60m vs 10m':(60/10,6),
 'RCD current 25A in minus out':(25-25,0),
 'BJT saturation 0.2V at 0.5A':(.2*.5,.1),
 'BJT poor 2V at 0.5A':(2*.5,1),
 'TN 230V / 0.5ohm':(230/.5,460),
 'TT 230V / 200ohm':(230/200,1.15),
 'overload power ratio':(14**2/10**2,1.96),
}
for label,(actual,expected) in checks.items():assert math.isclose(actual,expected,rel_tol=1e-8),label
print('PASS v0.11.8: 178/178 TTS texts in 1950–3900 word range')
print('PASS 12 editorial/audio/lecture/slides/workbook/audit/SVG consistency sets')
print('PASS 16 numeric model checks; manual editorial/norm approval remains open')
print('Long slide sections',sum(len(v) for v in slides.values()),'regular lesson count',len(counts))
