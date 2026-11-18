#!/usr/bin/env python3
"""Six bespoke explanatory electrical diagrams. These are ideal-model teaching circuits, NOT approved installation drawings."""
from pathlib import Path
from xml.etree import ElementTree as ET
import shutil
R=Path(__file__).resolve().parent.parent
CSS='''<style>text{font-family:DejaVu Sans,Arial,sans-serif;fill:#173042} .title{font-size:22px;font-weight:700} .sub{font-size:13px;fill:#486478} .lab{font-size:14px;font-weight:600} .tiny{font-size:12px;fill:#456278} .wire{stroke:#176d85;stroke-width:3;stroke-linecap:round;stroke-linejoin:round;fill:none} .component{stroke:#176d85;stroke-width:3;fill:#fff;stroke-linejoin:round} .accent{stroke:#e28a32;stroke-width:2.5;fill:none} .node{fill:#176d85} .panel{fill:white;stroke:#d5e4eb;stroke-width:1.5} .formula{font-size:17px;font-weight:bold;fill:#c1681a}</style>'''

def base(title,description,body):
 return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 440" role="img" aria-label="{title}"><title>{title}</title><desc>{description}</desc>{CSS}<rect x="0" y="0" width="960" height="440" rx="16" fill="#f3f8fb"/><text x="28" y="38" class="title">{title}</text><text x="28" y="60" class="sub">Didaktisches Ersatzschaltbild · idealisierte Gleichstrommodelle · keine Installationsplanung</text>{body}<text x="28" y="423" class="tiny">Nur für Rechen- und Verständnisübungen an sicheren, strombegrenzten Kleinspannungsmodellen.</text></svg>'''

def T(x,y,s,cls='lab',anchor='middle'):
 import html
 return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{html.escape(s)}</text>'
def line(x1,y1,x2,y2,cls='wire'):return f'<path class="{cls}" d="M{x1} {y1} L{x2} {y2}"/>'
def path(d,cls='wire'):return f'<path class="{cls}" d="{d}"/>'
def node(x,y):return f'<circle cx="{x}" cy="{y}" r="4" class="node"/>'
def source(x,y,label='12 V'):
 return f'<circle cx="{x}" cy="{y}" r="23" class="component"/>'+T(x,y-5,'+', 'lab')+T(x,y+17,'−','lab')+T(x-38,y+40,label,'tiny')
def resistor_h(x1,x2,y,label):
 return line(x1,y,x1+9,y)+f'<rect class="component" x="{x1+9}" y="{y-12}" width="{max(4,x2-x1-18)}" height="24" rx="1"/>'+line(x2-9,y,x2,y)+T((x1+x2)/2,y-24,label)
def resistor_v(x,y1,y2,label):
 return line(x,y1,x,y1+6)+f'<rect class="component" x="{x-12}" y="{y1+6}" width="24" height="{max(4,y2-y1-12)}" rx="1"/>'+line(x,y2-6,x,y2)+T(x+35,(y1+y2)/2+4,label,'tiny', 'start')
def pill(x,y,w,txt):
 return f'<rect x="{x}" y="{y}" width="{w}" height="35" rx="9" fill="#fff2e4" stroke="#edc399"/>'+T(x+w/2,y+23,txt,'formula')

body=''.join([
 source(92,194,'5 V'), line(92,85,92,171),line(92,217,92,300),line(92,85,320,85),resistor_h(320,435,85,'R = 1 kΩ'),line(435,85,602,85),line(602,85,602,300),line(602,300,92,300),node(302,85),node(456,85),
 path('M302 86 L302 144 L456 144 L456 86','accent'),T(380,165,'U = 5 V', 'lab'),T(240,74,'I = 5 mA →', 'lab'),T(695,170,'Ladung und Strom:','lab', 'start'),T(695,199,'Q = I · t','formula','start'),T(695,229,'t = 20 s → Q = 0,1 C','tiny','start'),pill(665,275,245,'I = U / R = 5 mA')])
svg1=base('1.03-A · Grundgrössen', '5 Volt Gleichspannungsquelle und idealer 1-kOhm-Widerstand in einer geschlossenen Schleife, fünf Milliampere Strom und eine Zeitleistung der Ladung.',body)

body=''.join([source(92,194,'12 V'),line(92,85,92,171),line(92,217,92,305),line(92,85,320,85),resistor_h(320,435,85,'R = 24 Ω'),line(435,85,602,85),line(602,85,602,305),line(602,305,92,305),T(230,74,'I = 0,5 A →'),T(700,125,'Leistung:','lab','start'),T(700,150,'P = U · I', 'formula','start'),T(700,180,'P = 12 V · 0,5 A = 6 W','tiny','start'),T(700,228,'Energie in 10 min:','lab','start'),T(700,252,'E = 6 W · 1/6 h','tiny','start'),pill(680,268,230,'E = 1 Wh'),T(365,335,'Bei gleichem R gilt P ∝ I²', 'lab'),T(365,357,'Doppelter Strom → vierfache Verlustleistung','tiny')])
svg2=base('1.03-C · Leistung und Energie','12-Volt-Modell mit 24-Ohm-Last, Strom 0,5 Ampere, Leistung 6 Watt, Energie 1 Wattstunde in 10 Minuten.',body)

body=''.join([
 source(92,204,'12 V'),line(92,85,92,181),line(92,227,92,310),line(92,85,234,85),
 line(234,85,249,85),f'<circle cx="274" cy="85" r="24" class="component"/>'+T(274,92,'A'),line(298,85,455,85),line(455,85,455,154),resistor_v(455,154,243,'R = 120 Ω'),line(455,243,455,310),line(455,310,92,310),
 node(455,129),node(455,272),line(455,129,581,129),line(581,129,581,182),f'<circle cx="581" cy="207" r="24" class="component"/>'+T(581,213,'V'),line(581,231,581,272),line(581,272,455,272),
 T(272,127,'Strommessung: in Reihe','tiny'),T(590,92,'Spannungsmessung: parallel','tiny'),T(680,205,'I ≈ 0,10 A','formula','start'),T(680,235,'U = 12 V','formula','start'),T(680,285,'Ohmmessung nur am','tiny','start'),T(680,307,'von Quellen getrennten Bauteil','tiny','start'),
 ])
svg3=base('1.03-D · Messen am Modell','Amperemeter in Reihe, Voltmeter parallel zu einem 120-Ohm-Widerstand, idealisierte 12-Volt-Quelle. Keine Netzspannungsmessung.',body)

body=''.join([
 '<rect class="panel" x="25" y="83" width="433" height="295" rx="14"/><rect class="panel" x="482" y="83" width="452" height="295" rx="14"/>',T(242,113,'Serie: gleicher Strom'),T(709,113,'Parallel: gleiche Spannung'),
 source(77,236,'9 V'),line(77,161,77,213),line(77,259,77,326),line(77,161,141,161),resistor_h(141,237,161,'100 Ω'),line(237,161,284,161),resistor_h(284,381,161,'200 Ω'),line(381,161,408,161),line(408,161,408,326),line(408,326,77,326),T(240,198,'I = 30 mA →','tiny'),pill(114,337,298,'R ges = 300 Ω'),
 source(529,233,'9 V'),line(529,161,529,210),line(529,256,529,326),line(529,161,829,161),line(529,326,829,326),line(653,161,653,197),resistor_v(653,197,287,'100 Ω'),line(653,287,653,326),line(829,161,829,197),resistor_v(829,197,287,'200 Ω'),line(829,287,829,326),node(653,161),node(829,161),node(653,326),node(829,326),pill(566,337,287,'R ges ≈ 66,7 Ω')
 ])
svg4=base('1.04-A · Serie und Parallel','Links 100 und 200 Ohm in Reihe an 9 Volt, Ersatzwiderstand 300 Ohm. Rechts 100 und 200 Ohm parallel an 9 Volt, Ersatzwiderstand rund 66,7 Ohm.',body)

body=''.join([
 '<rect class="panel" x="25" y="83" width="432" height="316" rx="14"/><rect class="panel" x="480" y="83" width="455" height="316" rx="14"/>',T(241,112,'Unbelasteter Teiler'),T(704,112,'Belasteter Teiler'),
 source(86,232,'12 V'),line(86,146,86,209),line(86,255,86,328),line(86,146,312,146),line(86,328,312,328),line(312,146,312,169),resistor_v(312,169,217,'R1 = 2 kΩ'),line(312,217,312,241),resistor_v(312,241,298,'R2 = 1 kΩ'),line(312,298,312,328),node(312,228),line(312,228,406,228),T(406,216,'U aus','tiny'),pill(135,350,288,'U aus = 4,0 V'),
 source(535,232,'12 V'),line(535,146,535,209),line(535,255,535,327),line(535,146,752,146),line(535,327,864,327),line(752,146,752,169),resistor_v(752,169,217,'R1 = 2 kΩ'),line(752,217,752,242),resistor_v(752,242,298,'R2 = 1 kΩ'),line(752,298,752,327),node(752,229),line(752,229,861,229),line(861,229,861,245),resistor_v(861,245,299,'')+T(860,212,'Last = 1 kΩ','tiny'),line(861,299,861,327),pill(559,351,277,'U aus = 2,4 V')
 ])
svg5=base('1.04-B · Spannungsteiler mit Last','12 Volt Quelle, R1 zwei Kiloohm, R2 ein Kiloohm; unbelastet 4,0 V, mit 1-kOhm-Last parallel zu R2 sind es 2,4 V.',body)

body=''.join([source(87,219,'Quelle'),line(87,116,87,196),line(87,242,87,314),line(87,116,270,116),resistor_h(270,387,116,'Hinleiter 10 m'),line(387,116,581,116),line(581,116,581,164),resistor_v(581,164,261,'Modelllast'),line(581,261,581,314),line(581,314,387,314),resistor_h(270,387,314,'Rückleiter 10 m'),line(270,314,87,314),T(240,102,'I = 2 A →'),T(708,143,'ρ Cu (Modell): 0,0178 Ω·mm²/m','tiny','start'),T(708,172,'l hin + l rück = 20 m','tiny','start'),T(708,201,'A = 1,5 mm²','tiny','start'),T(708,244,'R Leitung ≈ 0,237 Ω','lab','start'),T(708,270,'ΔU ≈ 0,475 V','lab','start'),pill(673,312,245,'P Verlust ≈ 0,95 W')])
svg6=base('1.04-C · Widerstand und Leitungsweg','Zweiaderiger Stromkreis mit Hin- und Rückleiter je zehn Meter. Bei 1,5 Quadratmillimeter Kupfer-Modellwert, Strom 2 Ampere, Schleifenwiderstand etwa 0,237 Ohm und Spannungsabfall rund 0,475 Volt.',body)

for lid,content in [('1.03-A',svg1),('1.03-C',svg2),('1.03-D',svg3),('1.04-A',svg4),('1.04-B',svg5),('1.04-C',svg6)]:
 try:ET.fromstring(content)
 except Exception as e:raise ValueError((lid,e))
 for folder in ['visuals','learning-visuals']:
  (R/folder/(lid+'.svg')).write_text(content,encoding='utf8')
 print(lid,'svg ready',len(content))
