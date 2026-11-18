#!/usr/bin/env python3
"""Generate 178 lesson-specific educational SVGs from the actually authored course data.

Visuals are labeled conceptual diagrams, NOT professional installation drawings,
and may not be used to justify conformity with Swiss standards.
"""
from __future__ import annotations
import json, re, html, textwrap
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parent.parent
REG=json.loads((ROOT/'data.js').read_text(encoding='utf-8').split('=',1)[1].strip(' ;\n'))['lessons']
NORM=json.loads((ROOT/'norm_course.json').read_text(encoding='utf-8'))['lessons']
V=ROOT/'visuals';V.mkdir(exist_ok=True)

def esc(t):return html.escape(str(t),quote=True)
def wrap(s,limit=37):
 s=re.sub(r'\s+',' ',str(s)).strip()
 return textwrap.shorten(s,width=limit,placeholder=' …')
def text(x,y,t,size=21,color='#223d52',weight=500,anchor='start'):
 return f'<text x="{x}" y="{y}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{esc(t)}</text>'
def multiline(x,y,s, maxchars=32, rows=3, step=28, size=20, color='#1c3d53'):
 s=re.sub(r'\s+',' ',str(s))
 parts=textwrap.wrap(s,width=maxchars,break_long_words=False,break_on_hyphens=False)[:rows]
 return ''.join(text(x,y+i*step,p,size,color) for i,p in enumerate(parts))
def path(d,stroke='#237e9c',thick=5,extra=''):
 return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{thick}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'
def line(x1,y1,x2,y2,stroke='#237e9c',thick=4):return path(f'M{x1} {y1}L{x2} {y2}',stroke,thick)
def rect(x,y,w,h,r=12,fill='#edf7fb',stroke='#8eb5c2',width=2):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'
def circ(x,y,r=24,stroke='#237e9c',fill='#fff',thick=4):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{thick}"/>'
def arrow(x1,y1,x2,y2,stroke='#237e9c'):
 return line(x1,y1,x2,y2,stroke,4)+path(f'M{x2-12} {y2-9} L{x2} {y2} L{x2-12} {y2+9}',stroke,3)

def diagram(kind, labels, title):
 # All diagrams are conceptual, with schematic elements only for extra-low-voltage learning.
 # Main drawing box: x=42..658, y=150..455.
 o=''
 if kind=='dc':
  o+=path('M125 218H530V375H125V218 M125 276V295 M125 328V375',thick=5)
  o+=line(108,295,142,295,'#d16d40',5)+line(115,316,135,316,'#d16d40',5)
  o+=rect(327,203,86,30,3,'#fff2da','#b27639')
  o+=text(345,225,'R',20,'#7e552f',700)
  o+=arrow(206,190,292,190)+text(231,177,'I',21,'#18768d',700)
  o+=text(74,325,'U',22,'#c15e39',700)
  o+=text(179,430,'Schutzkleinspannungs-Modell',19,'#45677b')
  o+=text(332,281,labels[0],17,'#234',500)
 elif kind=='ac':
  o+=path('M90 325H583 M100 178V409',thick=3)
  pts=[]
  import math
  for k in range(150):
   x=100+3.1*k;y=323-91*math.sin(2*math.pi*k/60)
   pts.append(f'{x:.1f},{y:.1f}')
  o+=f'<polyline points="{" ".join(pts)}" fill="none" stroke="#197f9f" stroke-width="6"/>'
  o+=text(113,166,'u(t)',20,'#1b667d',700)+text(554,350,'t',20)
  o+=text(120,445,labels[0],18,'#345669')
 elif kind=='three':
  o+=circ(332,299,123,'#c5dce2','#f7fbfc',3)
  import math
  for angle,c,lab in [(-90,'#1879a5','L1'),(30,'#c36f32','L2'),(150,'#62945f','L3')]:
   px=332+111*math.cos(math.radians(angle));py=299+111*math.sin(math.radians(angle))
   o+=line(332,299,round(px),round(py),c,6)
   o+=text(round(px+18),round(py-4),lab,21,c,700)
  o+=text(192,445,'Drei Phasoren – idealisiert, 120°',18,'#35566b')
 elif kind=='pv':
  o+=rect(84,216,118,140,7,'#e1f5fb','#3c819d',3)
  for yy in [252,291,328]:o+=line(92,yy,194,yy,'#7aafc1',3)
  for xx in [120,160]:o+=line(xx,224,xx,347,'#7aafc1',3)
  o+=arrow(208,284,287,284)
  o+=rect(293,233,127,103,12,'#fef1dd','#c08946',3)+text(356,281,'DC/AC',24,'#855526',700,'middle')
  o+=arrow(426,284,500,284)
  o+=rect(504,233,111,103,9,'#e3f4e7','#689970',3)+text(560,284,'NETZ',22,'#387349',700,'middle')
  o+=text(98,195,'PV-MODUL',19,'#316b84',700)
  o+=text(292,378,'Systemgrenzen und Rückspeisung prüfen',18,'#445e6e','')
 elif kind=='safety':
  for i,(x,lab,col) in enumerate([(90,'STOP','#c15d42'),(285,'KLÄREN','#c58f33'),(480,'FREIGABE','#34866c')]):
   o+=rect(x,235,150,106,13,'#fff',col,4)+text(x+75,295,lab,21,col,700,'middle')
  o+=arrow(247,288,275,288,'#60768b')+arrow(442,288,472,288,'#60768b')
  o+=text(95,391,'Rollen · Gefahren · Dokumentation',22,'#325368')
 elif kind=='protection':
  o+=rect(75,203,158,126,12,'#f2f7fb','#557f9a',3)+text(154,255,'FEHLER',23,'#405e7c',700,'middle')+text(154,283,'erkennen',18,'#405e7c',500,'middle')
  o+=arrow(241,260,304,260)
  o+=rect(318,203,140,126,12,'#fff0e4','#bd784d',3)+text(388,256,'SCHUTZ',21,'#a85d35',700,'middle')
  o+=arrow(466,260,510,260)
  o+=rect(518,203,117,126,12,'#edf7ef','#6eaa83',3)+text(578,257,'SICHER',20,'#3d8164',700,'middle')
  o+=text(81,398,'Schutzkonzept ≠ einzelnes Gerät',22,'#36576b')
 elif kind=='rc':
  o+=path('M108 270H214 M247 270H295 M325 270H540 M108 335H540 M108 270V335 M540 270V335',thick=4)
  o+=rect(213,257,35,26,2,'#fff1da','#c18b48',3)
  o+=line(298,244,298,296,'#326a86',5)+line(322,244,322,296,'#326a86',5)
  o+=text(219,243,'R',21,'#96582d',700)+text(306,233,'C',22,'#326a86',700)
  o+=text(135,390,'R · C = Zeitkonstante τ',24,'#315d75',700)
 elif kind=='logic':
  for x,lab in [(73,'Sensor'),(281,'Logik'),(491,'Aktor')]:
   o+=rect(x,230,133,109,9,'#e7f3f9','#4785a5',3)+text(x+66,292,lab,23,'#386a85',700,'middle')
  o+=arrow(212,283,272,283)+arrow(420,283,483,283)
  o+=text(112,402,'Funktion und Zustände dokumentieren',22,'#345669')
 elif kind=='motor':
  o+=circ(332,275,92,'#427b9b','#ecf8fc',5)
  o+=text(332,289,'M',68,'#23658a',700,'middle')
  o+=line(424,275,559,275,'#7e93a0',10)
  o+=path('M495 259L545 275L495 291','#c37f3b',3)
  o+=text(119,401,'Drehzahl · Drehmoment · Energie',22,'#346179')
 elif kind=='plan':
  o+=path('M90 184H587V396H90ZM90 287H343 M343 184V396 M343 336H587',thick=5)
  for x,y in [(183,235),(448,238),(179,340),(449,367)]:
   o+=circ(x,y,17,'#3c7b9b','none',3)
   o+=path(f'M{x-11} {y-11}L{x+11} {y+11}M{x+11} {y-11}L{x-11} {y+11}',stroke='#3c7b9b',thick=2)
  o+=text(109,426,'Grundrissprinzip – ohne Leitungsführung',18,'#496879')
 elif kind=='measurement':
  o+=rect(240,189,219,174,18,'#f1f7fb','#3e799b',4)
  o+=rect(276,217,146,58,4,'#e0eed9','#71946a',2)
  o+=text(350,255,'12.00',30,'#376148',700,'middle')
  o+=circ(348,319,23,'#5e8398','#f7fbfc',3)
  o+=path('M240 343L190 405M458 343L508 405',thick=4)
  o+=text(177,440,'Sollwert · Messwert · Abweichung',18,'#385971')
 elif kind=='network':
  o+=rect(269,228,139,90,11,'#e6effa','#5276ad',4)
  o+=text(340,282,'SWITCH',22,'#426fa0',700,'middle')
  for x,y in [(117,170),(550,171),(116,384),(550,383)]:
   o+=line(340,274,x,y,'#79a2b8',4)+rect(x-38,y-28,76,58,7,'#f5fbff','#6c97ac',3)
  o+=text(180,433,'Signalwege und Netzsegmentierung',19,'#435f73')
 elif kind=='transformer':
  for x in [275,408]:
   for y in [227,257,287,317]:
    o+=f'<path d="M{x} {y+24}a18 18 0 1 1 0 -24" fill="none" stroke="#327b9d" stroke-width="4"/>'
  o+=line(342,224,342,345,'#c07942',5)+line(354,224,354,345,'#c07942',5)
  o+=text(180,401,'Magnetischer Fluss · Übersetzung',22,'#416074')
 elif kind=='power':
  o+=path('M174 388V204L490 388Z',stroke='#5f89a6',thick=6)
  o+=text(155,302,'Q',24,'#a56b34',700)
  o+=text(332,420,'P',24,'#337ba4',700)
  o+=text(344,276,'S',24,'#487d5e',700)
  o+=text(225,449,'Leistungsdreieck, sinusförmiges Modell',18,'#416378')
 elif kind=='earthing':
  o+=rect(157,183,358,93,11,'#eaf4f8','#678b98',3)
  for xx in [210,310,410,490]:o+=line(xx,276,xx,354,'#7b9e78',5)
  o+=line(138,354,534,354,'#c29156',8)
  for xx in [199,287,385,477]:o+=path(f'M{xx} 363L{xx-20} 388M{xx} 363L{xx+20} 388',stroke='#c29156',thick=3)
  o+=text(198,421,'Potenzialausgleich und Erdungskonzept',21,'#315a69')
 elif kind=='formula':
  o+=rect(101,185,486,175,15,'#edf8fc','#7dafc4',3)
  o+=text(344,243,'Gegeben → Gesucht → Formel',29,'#286e8d',700,'middle')
  o+=line(143,269,537,269,'#bad9e5',2)
  o+=text(344,309,'Einheit → Rechnung → Kontrolle',28,'#266a7a',600,'middle')
  o+=text(120,415,'Grössen und Annahmen sauber trennen',21,'#426a7a')
 else:
  for i,(x,t) in enumerate([(74,'ANALYSIEREN'),(274,'BEGRÜNDEN'),(474,'PRÜFEN')]):
   o+=rect(x,234,141,98,12,'#eaf6f9','#648da3',3)+text(x+70,288,t,18,'#38647b',700,'middle')
   if i<2:o+=arrow(x+148,283,x+192,283)
  o+=text(96,399,'Annahmen → Schlussfolgerung → Grenzen',20,'#345a6e')
 return o

def kind(title):
 t=title.lower()
 ordered=[('transformer',r'transformator|induktionsgesetz'),('motor',r'motor|schlupf|anlaufarten|frequenzumrichter'),('three',r'drehstrom|sternschaltung|dreieck|neutralleiter|phasor'),('rc',r'kondensator|rc-|rlc-|impedanz|spulen'),('dc',r'ohmsch|stromkreis|widerstand|spannungsteiler|kirchhoff|leistung.*verlustwärme'),('pv',r'photovoltaik|pv-|string|wechselrichter|solarmodul|batteriespeicher|eigenverbrauch|netzeinspeisung'),('earthing',r'fundamenterder|erdung|blitzschutz|potentialausgleich'),('network',r'glasfaser|netzwerk|datenübertrag|patchfeld|twisted|ip-adressen|koax'),('safety',r'arbeitssicherheit|sicherheitsregeln|gefähr|sicherheitsfach|risiko|bewilligung|rechtsquellen|rechts- und'),('protection',r'rcd|fi-|schutz|fehlerstrom|kurzschluss|überstrom|selektiv|polarisierung|abschalt'),('measurement',r'messen|messung|prüf|multimeter|diagnos|sichtprüfung|fehleranalyse|messstrategie|messprotokoll'),('logic',r'automation|logik|steuerung|sensor|aktor|relais|selbsthaltung|verriegelung|kop/fup|knx|zeitglied|schaltplan'),('ac',r'wechselstrom|sinus|effektivwert|scheitelwert|frequenz|phas|energie'),('plan',r'installations|grundriss|plan|rohbau|leitungstrasse|stückliste|dokumentation|lichtkreis|raum|schema'),('power',r'leistungsdreieck|blindleistung|scheinleistung|wirkung|energiefluss'),('formula',r'si-|einheit|formeln|mathematik|prozent|wirkungsgrad|energie')]
 for k,p in ordered:
  if re.search(p,t):return k
 return 'process'

def create(item,isnorm):
 lid='N-'+item['id'] if isnorm else item['id']
 label=('Normen-Akademie' if isnorm else f"{str(item['id'])[0]}. Lehrjahr")
 title=item['title']
 notes=([item['lead']]+[s['heading'] for s in item['blocks']]) if isnorm else (item['objectives']+[s['heading'] for s in item['parts']])
 # use original course phrases, not invented normative requirements
 notes=[n for n in notes if n]
 k=kind(title)
 header=text(65,46,'ELEKTRO EFZ  /  '+lid,19,'#9ab7c7',700)
 header+=multiline(65,92,title,maxchars=55,rows=2,step=39,size=30,color='#fff')
 body=rect(39,161,656,308,17,'#f8fbfd','#e0eaf0',1)+diagram(k,notes,title)
 right=rect(718,161,440,308,17,'#fff','#d9e6ed',1)
 right+=text(744,206,'SCHWERPUNKTE',20,'#226a8e',700)
 for i in range(3):
  note=notes[i] if i<len(notes) else title
  right+=circ(756,246+i*73,15,'#d0e4ec','#e8f4f8',2)
  right+=text(756,252+i*73,str(i+1),17,'#337b92',700,'middle')
  right+=multiline(785,242+i*73,note,maxchars=27,rows=2,step=23,size=18)
 footer=rect(39,487,1119,85,11,'#edf4f8','#d9e6ed',1)
 footer+=multiline(61,524,'Typ: '+k+'  |  Lernbild zu '+title,maxchars=90,rows=1,size=18,color='#38576d')
 footer+=text(60,554,'Didaktische Visualisierung – keine Installations- oder Prüfanweisung.',18,'#8a5326',600)
 s=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 610" role="img" aria-labelledby="t d"><title id="t">{esc(title)}</title><desc id="d">Individuelle didaktische Darstellung zu Lektion {esc(lid)}; Schwerpunkt {esc(notes[0] if notes else title)}.</desc><rect width="1200" height="610" fill="#e5eef4"/><rect width="1200" height="147" fill="#15354d"/>{header}{body}{right}{footer}</svg>'''
 out=V/(lid+'.svg');out.write_text(s,encoding='utf-8')
 return {'id':lid,'title':title,'visual_type':k,'file':'visuals/'+out.name,'description':notes[:3], 'source':item.get('source') if isnorm else item.get('references',[])}

def main():
 rows=[create(l,False) for l in REG]+[create(l,True) for l in NORM]
 (ROOT/'lesson-visuals.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 print('Individual SVG visuals',len(rows),'categories',dict(Counter(x['visual_type'] for x in rows)))
if __name__=='__main__':main()
