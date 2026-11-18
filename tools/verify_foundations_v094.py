#!/usr/bin/env python3
"""Verify exact arithmetic of selected authored examples and structural editorial requirements.
Does NOT certify NIN compliance, electrical safety, devices or suitability for installation.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
import json,math
R=Path(__file__).resolve().parent.parent
NEW=['1.03-A','1.03-C','1.03-D','1.04-A','1.04-B','1.04-C']
for lid in NEW:
 p=R/'editorial_v094'/(lid+'.txt')
 assert p.is_file(),lid
 words=len(p.read_text(encoding='utf-8').split())
 assert 1950<=words<=3900,(lid,words)
 assert (R/'tts_scripts'/(lid+'.txt')).read_bytes()==p.read_bytes(),lid
 for dir in ['visuals','learning-visuals']:
  f=R/dir/(lid+'.svg');assert f.is_file();ET.parse(f)
  s=f.read_text('utf8');assert 'keine Installationsplanung' in s and '<desc>' in s

def approx(label,value,expected,tol=1e-3):
 if not math.isclose(value,expected,rel_tol=tol,abs_tol=tol):raise AssertionError((label,value,expected))
 return {'proof':label,'calculated':round(value,6),'expected':expected,'status':'PASS'}
tests=[]
tests.append(approx('1.03-A: 5 V / 1000 Ohm = 5 mA',5/1000,.005))
tests.append(approx('1.03-A: 5 mA * 20 s = 0.1 C',.005*20,.1))
tests.append(approx('1.03-C: 12 V / 24 Ohm = 0.5 A',12/24,.5))
tests.append(approx('1.03-C: 6 W / 6 = 1 Wh',6/6,1))
tests.append(approx('1.03-C: 12 V at 6.3 Ohm = 1.90476 A',12/6.3,1.904762))
tests.append(approx('1.03-C: line loss = 1.088W',(12/6.3)**2*.3,1.088435))
tests.append(approx('1.03-D: 1M parallel 10M = 0.909 MOhm',(1*10)/(1+10),.9090909))
tests.append(approx('1.03-D: loaded divider = 4.7619 V',10*((1*10)/(1+10))/(1+(1*10)/(1+10)),4.76190476))
tests.append(approx('1.03-D: 12V/121 Ohm = 99.17 mA',12/121,.09917355))
tests.append(approx('1.04-A: series 100+200 = 300 Ohm',100+200,300))
tests.append(approx('1.04-A: 9V parallel 100||200 = 135 mA',9*(1/100+1/200),.135))
tests.append(approx('1.04-A: 6||3 = 2 Ohm',6*3/(6+3),2))
tests.append(approx('1.04-B: unloaded divider (12V 2k+1k) = 4 V',12*1000/(2000+1000),4))
tests.append(approx('1.04-B: loaded divider (1k||1k) = 2.4 V',12*500/(2000+500),2.4))
tests.append(approx('1.04-B: 10 V loaded (1k||2k) = 4 V',10*(1000*2000/(1000+2000))/(1000+1000*2000/(1000+2000)),4))
tests.append(approx('1.04-C: copper 20m at 1.5mm² = 0.23733 Ohm',.0178*20/1.5,.2373333))
tests.append(approx('1.04-C: 2A line drop = .47467 V',2*.0178*20/1.5,.4746667))
tests.append(approx('1.04-C: 2A line loss = .9493 W',4*.0178*20/1.5,.9493333))
tests.append(approx('1.04-C: 12/6.3 Ohm model = 1.90476 A',12/6.3,1.9047619))
tests.append(approx('1.04-C: copper at 60C from 20C = 0.23144 Ohm',.2*(1+.00393*40),.23144))
data=json.loads((R/'quality-review.json').read_text('utf8'))
assert len(data['lessons'])==178
assert sum(1 for x in data['lessons'] if x['15_to_30_minute_target'])>=9
assert all(not x['normaussagen_freigegeben'] and not x['fachliche_einzelpruefung'] for x in data['lessons'])
(R/'v094-math-check.json').write_text(json.dumps({'count':len(tests),'scope':'Rechenmodelle und exemplarische arithmetische Werte, nicht Normenkonformität','tests':tests},indent=2,ensure_ascii=False),'utf8')
print('PASS:',len(NEW),'editorial 15–30min scripts, six XML drawings,',len(tests),'numerical verifications; 178 open expert signoffs')
