#!/usr/bin/env python3
"""Recalculate selected physics examples and check authored SVG / editorial files.
This is NOT an independent normative or installation-safety signoff.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
import json, math
R=Path(__file__).resolve().parent.parent
ids=('1.09-A','1.09-B','1.09-C','1.10-A','1.10-B','1.10-C')
for lid in ids:
 p=R/'editorial_v095'/(lid+'.txt')
 assert p.exists(),lid
 n=len(p.read_text('utf8').split());assert 1950<=n<=3900,(lid,n)
 assert (R/'tts_scripts'/(lid+'.txt')).read_bytes()==p.read_bytes(),lid
 for folder in ('visuals','learning-visuals'):
  f=R/folder/(lid+'.svg');ET.parse(f)
  s=f.read_text('utf8');assert '<desc>' in s and 'keine Installationsplanung' in s,(lid,folder)
vals=[]
def test(name,actual,expected,tol=0.001):
 assert math.isclose(actual,expected,rel_tol=tol,abs_tol=tol),(name,actual,expected)
 vals.append({'name':name,'calculated':round(actual,7),'expected':expected,'pass':True})
# 1.09 A
for name,val,expected in [
 ('E: 10V/5mm',10/.005,2000),('charge 470uF 12V',470e-6*12,.00564),
 ('energy 470uF 12V',.5*470e-6*144,.03384),('energy 1000uF 10V',.5*.001*100,.05),
 ('series 100uF 100uF',1/(1/100+1/100),50),('parallel 100uF 100uF',100+100,200),
 ('5V 100uF charge',100e-6*5,.0005)]:test('1.09-A '+name,val,expected)
# 1.09 B
for name,val,expected in [
 ('Faraday flux',200*.0005/.01,10),('coil 0.2H, current slope',.2*.5/.01,10),
 ('coil energy',.5*.1*.5**2,.0125),('coil energy at 1A',.5*.1*1**2,.05),
 ('tau 120mH 24Ohm',.12/24,.005),('final RL current',12/24,.5),
 ('RL current after tau',.5*(1-math.exp(-1)),.3160603),
 ('coil voltage 80mH, 0.4A/4ms',.08*.4/.004,8),
 ('coil energy initial',.5*.08*.2**2,.0016),('coil energy final',.5*.08*.6**2,.0144)]:test('1.09-B '+name,val,expected)
# 1.09 C
for name,val,expected in [
 ('tau',10000*100e-6,1),('charge after 1s',12*(1-math.exp(-1)),7.585447),
 ('charge after 3s',12*(1-math.exp(-3)),11.402555),
 ('discharge after 1s',12*math.exp(-1),4.414553),
 ('RC cutoff 10k 100nF',1/(2*math.pi*1e4*100e-9),159.154943),
 ('75% threshold time',-math.log(.25),1.386294),('tau 4k7 220uF',4700*220e-6,1.034)]:test('1.09-C '+name,val,expected)
# 1.10 A
for name,val,expected in [
 ('50Hz period',1000/50,20),('200Hz period',1000/200,5),
 ('50Hz omega',2*math.pi*50,314.159265),('2.5ms sine',10*math.sin(2*math.pi*50*.0025),7.071068),
 ('90degree at 50Hz',1000/(4*50),5),('10Vpeak to peak',2*10,20)]:test('1.10-A '+name,val,expected)
# 1.10 B
for name,val,expected in [
 ('100Vpeak rms',100/math.sqrt(2),70.710678),
 ('230Vrms peak',230*math.sqrt(2),325.269119),
 ('10Vpeak 20Ohm average power',(10/math.sqrt(2))**2/20,2.5),
 ('12Vrms 24Ohm power',12**2/24,6),('5V pulse at 25% rms',5*math.sqrt(.25),2.5),
 ('DC+AC 5V+2Vpeak RMS',math.sqrt(5**2+(2/math.sqrt(2))**2),math.sqrt(27)),
 ('4 discrete sample RMS',math.sqrt((0+16+0+16)/4),math.sqrt(8))]:test('1.10-B '+name,val,expected)
# 1.10 C
for name,val,expected in [
 ('daily energy',6*(2+8+6+3),114),('average daily kW',114/24,4.75),
 ('3minutes at 12kW',12*3/60,.6),('90% times 80%',.9*.8,.72),
 ('2kW output at 80% input',2/.8,2.5),('illustrative cost',114*.2,22.8),
 ('storage supplied for 2kWh delivered',2/.8,2.5)]:test('1.10-C '+name,val,expected)
quality=json.loads((R/'quality-review.json').read_text('utf8'))
assert len(quality['lessons'])==178
assert sum(x['15_to_30_minute_target'] for x in quality['lessons'])>=15
assert all(not x['normaussagen_freigegeben'] for x in quality['lessons'])
assert all(not x['fachliche_einzelpruefung'] for x in quality['lessons'])
(R/'v095-physics-check.json').write_text(json.dumps({'scope':'Selected ideal-physics equations only, NO normative review or safe-use certificate', 'chapter_count':len(ids),'checks':vals},ensure_ascii=False,indent=2),'utf8')
print('PASS',len(ids),'historical v095 chapters, six subject-specific SVG diagrams,',len(vals),'independent arithmetic assertions; normative approval remains open')
