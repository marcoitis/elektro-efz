#!/usr/bin/env python3
"""v0.11.7 completeness/editorial QA, NOT independent electrician/norm approval."""
from pathlib import Path
import json,math,re,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parent.parent
IDS=['N-W05','N-P01','N-P02','N-P03','N-P04','N-P05','N-P06','N-P07','N-V01','N-V02','N-V03','N-V04']
J=lambda n:json.loads((R/n).read_text(encoding='utf-8'))
JS=lambda n:json.loads((R/n).read_text(encoding='utf-8').split('=',1)[1].strip(' ;\n'))
lecture=JS('lecture-scripts.js');slides=JS('lesson-long-slides.js');audit=JS('lesson-audit.js');q=J('quality-review.json');qrows={row['id']:row for row in q['lessons']}
books={row['id']:row for row in J('lesson-workbooks.json')}
assert q['version']=='v0.11.7'
assert len(lecture)==len(audit)==len(qrows)==len(books)==178
assert len(list((R/'tts_scripts').glob('*.txt')))==178
assert len(list((R/'visuals').glob('*.svg')))==len(list((R/'learning-visuals').glob('*.svg')))==178
assert len(JS('data.js')['lessons'])==145 and len(J('norm_course.json')['lessons'])==33
for lid in IDS:
 path=R/'tts_scripts'/(lid+'.txt');t=path.read_text(encoding='utf-8');n=len(t.split())
 assert 1950<=n<=3900,(lid,n)
 assert t==(R/'editorial_v0117'/(lid+'.txt')).read_text(encoding='utf-8')
 assert lecture[lid]==t.strip()
 assert qrows[lid]['script_words']==audit[lid]['script_words']==books[lid]['ttsWords']==n
 assert books[lid]['fullManuscript']==t
 assert qrows[lid]['15_to_30_minute_target']==audit[lid]['15_to_30_minute_target'] is True
 assert not qrows[lid]['normaussagen_freigegeben'] and not qrows[lid]['fachliche_einzelpruefung']
 assert len(slides[lid])>=24 and all(len(s['text'].split())<=145 for s in slides[lid]),(lid,'slide length')
 # Each heading belongs to a section; headings count too.
 assert sum(len(s['text'].split())+len(s['heading'].split()) for s in slides[lid])>=.98*n,(lid,'slide coverage')
 wb=(R/'workbooks'/(lid+'.md')).read_text(encoding='utf-8')
 assert 'Individuell redigiertes Fachmanuskript (v0.11.7)' in wb
 for folder in ['visuals','learning-visuals']:
  f=R/folder/(lid+'.svg');ET.parse(f)
  assert 'Didaktisches' in f.read_text(encoding='utf-8')
assert sum(1950<=len(p.read_text(encoding='utf-8').split())<=3900 for p in (R/'tts_scripts').glob('*.txt'))==166
assert 'elektro-efz-shell-v0117-twelve-lessons' in (R/'sw.js').read_text(encoding='utf-8')
assert 'elektro-efz-shell-v0117-twelve-lessons' in (R/'offline.js').read_text(encoding='utf-8')
checks={
 'storage AC energy 9kWh * .85':(9*.85,7.65),
 'storage runtime 8kWh * .92 / 2kW':(8*.92/2,3.68),
 'PV 30 modules x 420Wp':(30*420/1000,12.6),
 'PV 12 modules x 41V STC':(12*41,492),
 'PV 12 modules x 41V at -15C':(12*41*(1+.0028*40),547.104),
 'PV 14 modules 44V at -10C':(14*44*(1+.003*35),680.68),
 'PV MPP 34V*12.2A':(34*12.2,414.8),
 'PV FF 414.8/(42*13)':(414.8/(42*13),.7597069597),
 'PV FF 410/(41.5*13.2)':(410/(41.5*13.2),.7484483388),
 'ISO 500V/5Mohm mA':(500/5000000*1000,.1),
 'contact heat 50A*2milliohm':(50**2*.002,5),
 'contact heat 100A*2milliohm':(100**2*.002,20),
 '80A at 3milliohm':(80**2*.003,19.2),
 'PV three strings parallel':(3*11.8,35.4),
 'power loss 240W output 90pct input':(240/.9-240,26.6666667),
 'therm increase 40W * .8K/W':(40*.8,32)
}
for name,(a,b) in checks.items():assert math.isclose(a,b,rel_tol=1e-4,abs_tol=1e-4),(name,a,b)
print('PASS v0.11.7: 12 TTS/editorial/lecture/slides/workbook/audit/SVG integrations, 166/178 manuscripts >=1950 words')
print('Folienkapitel in 12 neuen Lektionen:',sum(len(slides[lid]) for lid in IDS),'insgesamt Langkapitel',sum(map(len,slides.values())))
print('Mathematical model checks:',len(checks))
print('Remaining:',[(p.stem,len(p.read_text().split())) for p in sorted((R/'tts_scripts').glob('*.txt')) if len(p.read_text().split())<1950])
