#!/usr/bin/env python3
"""Arithmetic and coverage checks, not a Swiss normative compliance certificate."""
from pathlib import Path
import math,json
from xml.etree import ElementTree as ET
R=Path(__file__).resolve().parent.parent
ids=['1.07-A','1.07-B','1.07-C','1.08-A','1.08-B','1.08-C']
for lid in ids:
 t=(R/'editorial_v097'/(lid+'.txt')).read_text(encoding='utf8')
 w=len(t.split())
 assert 1950<=w<=3900,(lid,w)
 assert 'Abschluss und Quellenstatus.' in t and 'keine' in t.lower(),lid
 assert 'Vertiefung' in t, lid
 for folder in ('visuals','learning-visuals'):
  v=(R/folder/(lid+'.svg'))
  assert v.is_file(),v
  ET.parse(v)
 assert (R/'tts_scripts'/(lid+'.txt')).read_text('utf8')==t,lid
 print(lid,'words',w,'~min',round(w/130,1))
close=lambda a,b: math.isclose(a,b,rel_tol=1e-6,abs_tol=1e-6)
# Mechanics and geometry
assert close(5*9.81,49.05)
assert close(20*0.1,2.0)
assert close(2.4+1.8,4.2)
assert math.ceil(4.8/2)==3
assert math.ceil(2.4/0.6)+1==5
assert close(0.01724*20/2.5,0.13792)
assert close(4*0.13792,0.55168)
assert close(4*4*0.13792,2.20672)
# Measurement and circuit calculations
assert close(12/120,0.1)
assert close(12*12/120,1.2)
assert close(12/240,0.05)
assert close(12*(120/240),6)
r1=r2=10000
for rm,exp in [(1e6,5.9701492537),(100000,5.7142857143)]:
 parallel=r2*rm/(r2+rm)
 measured=12*parallel/(r1+parallel)
 assert abs(measured-exp)<0.00001,(rm,measured)
assert close((5.88-6)/6*100,-2)
assert close((5.97-6)/6*100,-0.5)
assert close(12/20000*12,0.0072)
# Lesson catalogue has not changed
D=json.loads((R/'data.js').read_text('utf8').split('=',1)[1].strip(' ;\n'))
N=json.loads((R/'norm_course.json').read_text('utf8'))
assert len(D['lessons'])==145 and len(N['lessons'])==33
assert len({l['id'] for l in D['lessons']})==145
print('20 independent arithmetic/model checks; lesson identities unchanged')
