#!/usr/bin/env python3
"""Six carefully authored didactic SVGs for lessons 1.07 and 1.08.
These are illustrative teaching figures, NOT certified installation drawings.
"""
from pathlib import Path
from html import escape as E
from xml.etree import ElementTree as ET
ROOT=Path(__file__).resolve().parent.parent
STYLE='''<style>text{font-family:Arial,DejaVu Sans,sans-serif;fill:#173247}.t{font-size:24px;font-weight:700}.s{font-size:13px;fill:#547084}.h{font-size:17px;font-weight:600}.n{font-size:15px}.f{font-size:20px;font-weight:700;fill:#a15f1e}.wire{fill:none;stroke:#117394;stroke-width:3;stroke-linecap:round;stroke-linejoin:round}.soft{fill:#fff;stroke:#c5d9e4;stroke-width:1.5}.warn{fill:#fff7ea;stroke:#ddb77a;stroke-width:1.5}</style>'''
def label(x,y,t,cls='n',anchor='middle'): return f'<text class="{cls}" text-anchor="{anchor}" x="{x}" y="{y}">{E(str(t))}</text>'
def rect(x,y,w,h,cls='soft',rx=10):return f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/>'
def line(x1,y1,x2,y2,stroke='#117394',sw=3,dash=''):return f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{stroke}" stroke-width="{sw}" {f"stroke-dasharray=\"{dash}\"" if dash else ""}/>'
def circle(x,y,r,fill='#fff',stroke='#117394',sw=2): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def svg(t,desc,b):return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 550" role="img" aria-label="{E(t)}"><title>{E(t)}</title><desc>{E(desc)}</desc>{STYLE}<rect width="1100" height="550" rx="18" fill="#f4f8fa"/>{label(29,41,t,'t','start')}{label(29,63,'Didaktisches Modell · keine Installationsplanung und keine normative Freigabe','s','start')}{b}{label(29,531,'Nur Kleinspannungs- und Planungssimulation; für reale Anlagen gelten zusätzliche Nachweise und Fachzuständigkeiten.','s','start')}</svg>'''
G={}
# 1.07-A mounting channel + force model
b=rect(25,87,660,414)+rect(711,87,365,414)
b+=label(350,119,'Übung: Kanal 2,4 m · fiktiver Herstellerabstand 0,6 m','h')
b+=f'<rect x="85" y="177" width="520" height="72" rx="8" fill="#d7e5ee" stroke="#608496" stroke-width="2"/>'
for i in range(5):
 x=90+i*128;b+=circle(x,212,8,'#ad7e49','#83613c',2);b+=line(x,251,x,292,'#7c9aab',1.6);b+=label(x,316,str(i+1),'n')
 for j in []:pass
b+=label(350,356,'Vier Intervalle à 0,6 m → 5 Befestigungspunkte','f')
b+=label(350,394,'Nur Geometrie: Befestigungsabstand muss produktbezogen geprüft werden','s')
b+=label(350,431,'Untergrund · Lastpfad · Randabstand · Verbinder · Kanten','n')
b+=label(890,129,'Auskragender Modellhalter','h')
b+=line(776,160,776,396,'#657f93',7)+line(776,206,962,206,'#657f93',6)
b+=line(942,206,942,316,'#bb7431',3)+label(967,287,'20 N','h','start')
b+=label(878,188,'Hebelarm 0,10 m','s')+label(892,359,'M = F · l','f')+label(892,395,'= 2,0 N·m','f')+label(890,443,'Keine Dübelbemessung!','s')
G['1.07-A']=svg('1.07-A · Befestigung und Lastpfad','2,4 Meter Kanal mit fünf modellhaften Befestigungspunkten im maximalen Raster 0,6 Meter. Ein auskragender Halter mit 20 Newton Last und Hebelarm 0,10 Meter erzeugt ein Moment von 2 Newtonmeter.',b)
# 1.07-B route comparison
b=rect(25,87,670,416)+rect(714,87,361,416)
b+=label(360,118,'Fiktiver Grundriss: zwei mögliche Leitungswege','h')
b+=f'<rect x="82" y="148" width="540" height="284" fill="#fff" stroke="#456d83" stroke-width="2"/>'
b+=line(352,149,352,433,'#bd6d43',7)+label(351,457,'Brandabschnitt?','s')
b+=rect(99,355,108,60)+label(152,391,'Technikraum','s')
b+=rect(512,180,98,60)+label(561,214,'Ziel','s')
b+=f'<path d="M207 390 H293 V206 H513" fill="none" stroke="#bb682e" stroke-width="6" stroke-dasharray="10 8"/>'
b+=f'<path d="M207 390 V465 H664 V265 H561 V240" fill="none" stroke="#167b80" stroke-width="6"/>'
b+=label(299,191,'Route A: 10 m (Modell)','s')+label(478,483,'Route B: 13 m (Modell)','s')
b+=label(892,131,'Variantenentscheidung','h')
for yy,tx in [(190,'A: kürzer, Durchdringung offen'),(233,'B: länger, Fassadendurchtritte offen'),(279,'Höhenlage gesondert prüfen'),(322,'Biegeradien nach Hersteller'),(365,'Häufung / Wärme nach NIN'),(412,'Koordination vor Ausführung')]:b+=label(738,yy,tx,'n','start')
G['1.07-B']=svg('1.07-B · Leitungswege vergleichen','Fiktiver zweidimensionaler Grundriss mit zwei Trassenvarianten. Route A 10 Meter mit offener Brandabschnittsdurchdringung; Route B 13 Meter als alternative Aussenumfahrung mit noch ungeklärten Gebäudehüllendurchdringungen. Keine Bewertung der tatsächlichen brandschutztechnischen Zulässigkeit.',b)
# 1.07-C safety decision matrix
b=rect(25,88,1050,414)
for i,(n,h,a,d) in enumerate([('1','Altbauwand','Asbestverdacht: Stoppen','Suva / Schadstoffabklärung'),('2','Brandabschnitt','Systemnachweis fehlt','Brandschutzplanung einbeziehen'),('3','Nähe PV-Anlage','Energiezustand ungeklärt','Elektrofachperson zuständig')]):
 y=124+i*117
 b+=rect(62,y,969,92,'warn');b+=circle(105,y+42,22,'#f1ca7a','#bd7a28');b+=label(105,y+49,n,'h');b+=label(160,y+27,h,'h','start')+label(160,y+52,a,'n','start')+label(602,y+54,d,'n','start')
b+=label(544,478,'Arbeitsfreigabe erst nach dokumentierter Klärung der relevanten Gefahren','f')
G['1.07-C']=svg('1.07-C · Baustellen-Stoppentscheidungen','Drei beispielhafte Stopppunkte: Asbestverdacht an einer Altbauwand, ungeklärte Brandabschnittsdurchdringung und unklarer Energiezustand nahe einer PV-Anlage.',b)
# 1.08-A voltmeter parallel to known resistor; source separated
b=rect(25,88,693,416)+rect(741,88,334,416)
b+=label(376,122,'Strombegrenztes 12-V-DC-Modell: Messpunkt M1–M0','h')
b+=line(139,193,544,193)+line(544,193,544,410)+line(544,410,139,410)+line(139,410,139,341)
b+=line(139,262,139,193)+circle(139,303,38,'#fff6df','#c98a3a')+label(139,309,'12 V','h')
b+=line(544,193,544,275)+line(544,328,544,410)
b+=f'<rect x="530" y="275" width="28" height="53" fill="#d9ebf2" stroke="#117394" stroke-width="3"/>'
b+=label(605,306,'120 Ω','h','start')
b+=line(544,247,407,247)+line(407,247,407,365)+line(407,365,544,365)
b+=circle(407,305,26,'white','#b77530',2)+label(407,313,'V','h')
b+=label(376,452,'Voltmeter parallel · Quelle mit geeigneter Strombegrenzung','s')
b+=label(903,130,'Ideale Rechnungswerte','h')+label(903,192,'I = 12 V / 120 Ω','n')+label(903,231,'= 0,100 A','f')+label(903,289,'P = U² / R','n')+label(903,329,'= 1,20 W','f')+label(905,395,'Bauteilleistung prüfen!','s')+label(905,433,'Kein Netzanschluss.','s')
G['1.08-A']=svg('1.08-A · Spannungsmessung am Modell','Separater strombegrenzter Gleichspannungsstromkreis mit 12 Volt, 120 Ohm Last und parallel angeschlossenem symbolischen Voltmeter. Rechnerisch 100 Milliampere und 1,2 Watt.',b)
# 1.08-B divider and meter impedance
b=rect(25,88,597,416)+rect(642,88,432,416)
b+=label(320,124,'12 V und zwei Widerstände à 10 kΩ','h')
b+=line(225,160,225,213)+line(225,259,225,327)+line(225,373,225,433)
b+=f'<rect x="210" y="212" width="30" height="47" fill="#dcecf4" stroke="#117394" stroke-width="3"/>'
b+=f'<rect x="210" y="327" width="30" height="47" fill="#dcecf4" stroke="#117394" stroke-width="3"/>'
b+=label(305,240,'R1 = 10 kΩ','n','start')+label(305,358,'R2 = 10 kΩ','n','start')
b+=circle(225,292,6,'#bf8036','#bf8036')+line(231,292,435,292)+label(365,281,'Messpunkt M1','n')
b+=line(225,433,435,433)+label(358,451,'M0 (Bezug)','n')
b+=circle(435,362,23,'#fff9ea','#c07a2a');b+=label(435,369,'V','h')+line(435,292,435,338)+line(435,385,435,433)
b+=label(165,174,'+12 V','n')+label(165,452,'0 V','n')
b+=label(855,125,'Einfluss der Messeingangsimpedanz','h')
for yy,tx in [(190,'Ideal, unbelastet: 6,000 V'),(246,'1 MΩ Voltmeter: ≈ 5,970 V'),(303,'100 kΩ Voltmeter: ≈ 5,714 V'),(373,'U = 12 · (R2||Rm) / (R1+(R2||Rm))')]: b+=label(671,yy,tx,'n','start')
b+=label(855,430,'Eingangsimpedanz belastet den Teiler','s')
G['1.08-B']=svg('1.08-B · Messgerät belastet den Spannungsteiler','Zwei 10-Kiloohm-Widerstände an 12 Volt. Ausgangsspannung ideal 6 Volt; mit Voltmeter-Eingangswiderstand 1 Megaohm etwa 5,970 Volt, mit 100 Kiloohm etwa 5,714 Volt.',b)
# 1.08-C fault tree+ numeric
b=rect(25,88,658,415)+rect(708,88,366,415)
b+=label(354,127,'Ausgangssymptom: 12-V-Modellleuchte dunkel','h')
b+=rect(205,151,297,54);b+=label(354,185,'Unklare Fehlerursache','h')
b+=line(354,205,354,242)+line(115,242,595,242)
for i,(x,title,sub) in enumerate([(115,'Quelle','Sollspannung?'),(352,'Pfad','Kontakt offen?'),(590,'Last','Verbraucher?')]):
 b+=line(x,242,x,266);b+=rect(x-90,270,180,86);b+=label(x,298,title,'h')+label(x,326,sub,'s')
b+=label(354,403,'Beobachtung → Hypothese → sichere Prüfung','f')
b+=label(354,447,'Änderung nur im sicheren Modellzustand','s')
b+=label(885,130,'Berechenbarer Ersatzkreis','h')
b+=label(885,183,'12 V · 120 Ω + 120 Ω','n')
b+=label(885,238,'Rges = 240 Ω','n')
b+=label(885,290,'I = 0,050 A','f')
b+=label(885,346,'U1 = U2 = 6 V','f')
b+=label(885,419,'Ohne absichtlichen Kurzschluss','s')
G['1.08-C']=svg('1.08-C · Fehlerbaum am Kleinspannungsmodell','Eine dunkle 12-Volt-Modellleuchte kann von Quelle, Strompfad oder Verbraucher herrühren. Modellrechnung mit zwei 120-Ohm-Widerständen in Reihe: 50 Milliampere und jeweils 6 Volt Spannungsabfall.',b)
assert len(G)==6
for lid,body in sorted(G.items()):
 ET.fromstring(body)
 for folder in ('visuals','learning-visuals'):(ROOT/folder/(lid+'.svg')).write_text(body,encoding='utf-8')
 print(lid,len(body),'bytes')
