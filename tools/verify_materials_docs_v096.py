#!/usr/bin/env python3
"""Independent numerical checks and duplication guard for v0.9.6 teaching examples.
Not a Swiss electrical standards certification.
"""
from pathlib import Path
from collections import Counter
from xml.etree import ElementTree as ET
from math import isclose
import json
R=Path(__file__).resolve().parent.parent
ids=('1.05-A','1.05-B','1.05-C','1.06-A','1.06-B','1.06-C')
for lid in ids:
 p=R/'editorial_v096'/(lid+'.txt')
 assert p.is_file(),lid
 s=p.read_text('utf8');n=len(s.split())
 assert 1950<=n<=3900,(lid,n)
 assert (R/'tts_scripts'/(lid+'.txt')).read_bytes()==p.read_bytes(),lid
 pgs=[x.strip() for x in s.split('\n\n') if len(x.strip())>150]
 duplicates=[x[:60] for x,v in Counter(pgs).items() if v>1]
 assert not duplicates,(lid,duplicates)
 assert s.count('Frage eins:')>=1,(lid,'missing reasoned review questions')
 for folder in ('visuals','learning-visuals'):
  f=R/folder/(lid+'.svg');root=ET.parse(f).getroot()
  assert root.attrib.get('viewBox')=='0 0 1100 560',(lid,'wrong graphic dimensions')
  desc=root.find('{http://www.w3.org/2000/svg}desc')
  assert desc is not None and len(desc.text)>100,(lid,'missing semantic description')
checks=[]
def check(name,value,expected,rtol=1e-4):
 assert isclose(value,expected,rel_tol=rtol,abs_tol=1e-5),(name,value,expected)
 checks.append({'name':name,'calculated':round(value,8),'expected':expected})
# metal conductors, Ohm mm²/m, geometrical resistivity model
cu=.01724;al=.02826
check('Cu 20 m / 2.5 mm²',cu*20/2.5,.13792)
check('Al 20 m / 2.5 mm²',al*20/2.5,.22608)
check('Al/Cu resistivity ratio',al/cu,1.63921,1e-4)
check('Cu 40 m / 2.5 mm²',cu*40/2.5,.27584)
check('Cu 40 m / 5 mm²',cu*40/5,.13792)
check('Cu 4 A voltage drop',4*.27584,1.10336)
check('Cu 4 A line loss',4**2*.27584,4.41344)
check('Cu 8 A line loss',8**2*.27584,17.65376)
check('Cu 50K temperature change 20C to 70C',.1*(1+.00393*50),.11965)
check('Cu example 30 m return loop 1.5 mm²',cu*30/1.5,.3448)
check('Cu example 30m 2A voltage drop',2*.3448,.6896)
check('Cu example 30m 2A line loss',2**2*.3448,1.3792)
check('example Cu 100m 1 mm²',cu*100/1,1.724)
# plan scale
check('8.4cm 1:50 real meters',8.4*50/100,4.2)
check('8.4cm at 70% print size',8.4*.70,5.88)
check('wrong length after resized print, 1:50',5.88*50/100,2.94)
# model circuits and revisions
check('12V 24ohm current',12/24,.5)
check('12V 24ohm power',12**2/24,6)
check('two 24-ohm parallel at 12V current',12/(1/(1/24+1/24)),1)
check('two 24-ohm parallel at 12V power',12*1,12)
# source audit is NOT a certificate
q=json.loads((R/'quality-review.json').read_text('utf8'))
assert len(q['lessons'])==178
assert sum(x['15_to_30_minute_target'] for x in q['lessons'])>=21
assert all(not x['normaussagen_freigegeben'] for x in q['lessons'])
assert all(not x['fachliche_einzelpruefung'] for x in q['lessons'])
report={'version':'0.9.6','status':'limited automated tests; NO normative release', 'new_lessons':list(ids),'arithmetic_checks':checks,'total_lecture_minutes':{id:round(len((R/'tts_scripts'/(id+'.txt')).read_text('utf8').split())/130,1) for id in ids}, 'normative_approval':False}
(R/'v096-materials-documents-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf8')
print('PASS: 6 new individual >1950-word manuscripts, 6 distinct graphics,',len(checks),'arithmetical assertions, 21/178 full-length; independent norm approval remains open')
