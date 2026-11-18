#!/usr/bin/env python3
"""Six subject-specific SVG teaching graphics for idealized low-voltage theory, not installation designs."""
from pathlib import Path
from xml.etree import ElementTree as ET
from math import sin,pi,sqrt,exp
from html import escape
R=Path(__file__).resolve().parent.parent
CSS='''<style>text{font-family:DejaVu Sans,Arial,sans-serif;fill:#173042}.title{font-size:22px;font-weight:700}.sub{font-size:13px;fill:#486478}.lab{font-size:15px;font-weight:600}.tiny{font-size:12px;fill:#456278}.line{stroke:#176d85;stroke-width:3;stroke-linecap:round;stroke-linejoin:round;fill:none}.thin{stroke:#789aa9;stroke-width:1.4;fill:none}.accent{stroke:#df8732;stroke-width:3;fill:none}.dashed{stroke:#df8732;stroke-width:2;stroke-dasharray:7 5;fill:none}.panel{fill:#fff;stroke:#d5e4eb;stroke-width:1.5}.formula{font-size:20px;font-weight:700;fill:#bd691e}</style>'''
def S(title,desc,body):
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 460" role="img" aria-label="{escape(title)}"><title>{escape(title)}</title><desc>{escape(desc)}</desc>{CSS}<rect width="960" height="460" rx="16" fill="#f3f8fb"/><text x="28" y="38" class="title">{escape(title)}</text><text x="28" y="61" class="sub">Didaktisches Physikmodell – nur Simulation oder geeignete Kleinspannung, keine Installationsplanung</text>{body}<text x="28" y="443" class="tiny">Modellannahmen gelten nur unter den genannten idealisierten Bedingungen.</text></svg>'
def T(x,y,s,cl='lab',anchor='middle'):
 return f'<text x="{x}" y="{y}" class="{cl}" text-anchor="{anchor}">{escape(s)}</text>'
def P(d,cl='line'):return f'<path d="{d}" class="{cl}"/>'
def L(x1,y1,x2,y2,cl='line'):return P(f'M{x1} {y1} L{x2} {y2}',cl)
def Rect(x,y,w,h,cls='panel'):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" class="{cls}"/>'
def arrow(x,y,dx,dy):
 return f'<path d="M{x} {y} l{dx} {dy} l{-8 if dx else -5} {-6 if dy==0 else -8} m{8 if dx else 5} {6 if dy==0 else 8} l{-8 if dx else 5} {6 if dy==0 else -8}" class="accent"/>'
def plot(x0,y0,w,h,fun, xmax, ymin,ymax,n=150):
 pts=[]
 for i in range(n+1):
  x=xmax*i/n;y=fun(x)
  px=x0+w*i/n;py=y0+h*(ymax-y)/(ymax-ymin)
  pts.append(f'{px:.1f},{py:.1f}')
 return '<polyline points="'+' '.join(pts)+'" fill="none" stroke="#176d85" stroke-width="3"/>'
# 1 electric field and capacitor
b=Rect(35,95,530,295)+T(280,127,'Plattenkondensator – vereinfachtes Feld')
b+=f'<rect x="130" y="155" width="18" height="166" fill="#df8732"/><rect x="410" y="155" width="18" height="166" fill="#176d85"/>'
for y in range(170,320,30): b+=L(151,y,403,y,'thin')+'<path d="M390 '+str(y-6)+' l12 6 l-12 6" class="thin"/>'
b+=T(115,146,'+ + +','lab')+T(435,146,'− − −','lab')+T(280,218,'E ≈ U / d','formula')+T(280,349,'Plattenabstand d = 5 mm','tiny')
b+=Rect(595,95,325,295)+T(755,130,'Modellbeispiel')+T(750,176,'U = 10 V, d = 0,005 m','tiny')+T(748,213,'E ≈ 2000 V/m','formula')+T(750,258,'C = 470 µF, U = 12 V','tiny')+T(750,292,'W = ½ · C · U²','formula')+T(750,322,'W = 0,03384 J','formula')+T(750,356,'Feldenergie bleibt nach Abschalten möglich','tiny')
graph={'1.09-A':S('1.09-A · Elektrisches Feld und Kondensator','Elektrische Feldlinien zwischen idealen Platten, E ungefähr U geteilt durch d, Beispiel 2000 Volt pro Meter; gespeicherte Kondensatorenergie bei 470 Mikrofarad und 12 Volt 0,03384 Joule.',b)}
# 2 coil fields + RL response
b=Rect(35,95,545,300)+T(307,123,'Spule: Änderung des Stromes erzeugt Spannung')
b+=L(85,230,145,230)+L(430,230,505,230)
for i in range(6):
 x=145+i*47
 b+=P(f'M{x} 230 C{x+7} 186,{x+40} 186,{x+47} 230')
b+=arrow(210,168,30,0)+T(306,165,'magnetische Flussrichtung (schematisch)','tiny')+T(300,289,'uL = L · ΔI / Δt','formula')+T(300,323,'L = 0,20 H · ΔI = 0,50 A · Δt = 0,010 s','tiny')+T(300,355,'uL = 10 V','formula')
b+=Rect(610,95,315,300)+T(767,130,'Magnetische Energie')+T(765,175,'W = ½ · L · I²','formula')+T(765,214,'L = 0,10 H','tiny')+T(765,240,'I = 0,50 A','tiny')+T(765,287,'W = 0,0125 J','formula')+T(765,327,'Abschalten: Energieabbau beachten','tiny')
graph['1.09-B']=S('1.09-B · Spule, Induktion und Energie','Sechswindungs-Spulensymbol und ein ideales Induktionsbeispiel mit L 0,2 Henry, Stromänderung 0,5 Ampere in 0,01 Sekunden; induktive Spannung 10 Volt; Energiebeispiel 12,5 Millijoule.',b)
# 3 RC curve
b=Rect(35,95,575,310)+T(316,128,'Kondensatorladung, UQuelle = 12 V, τ = 1 s')
ax_x,ax_y,w,h=105,175,425,170
b+=L(ax_x,ax_y,ax_x,ax_y+h,'thin')+L(ax_x,ax_y+h,ax_x+w,ax_y+h,'thin')
for j in range(0,6):
 x=ax_x+w*j/5;b+=L(x,ax_y+h,x,ax_y+h+5,'thin')+T(round(x),370,f'{j} s','tiny')
for v in (0,6,12):
 y=round(ax_y+h*(12-v)/12);b+=L(ax_x-5,y,ax_x,y,'thin')+T(73,y+4,str(v)+' V','tiny')
b+=plot(ax_x,ax_y,w,h,lambda t:12*(1-exp(-t)),5,0,12)
x=ax_x+w/5;y=ax_y+h*(12-12*(1-exp(-1)))/12
b+=P(f'M{x:.1f} {ax_y+h} V{y:.1f}','dashed')+f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#df8732"/>'
b+=T(340,214,'nach τ ≈ 63,2 %','tiny')
b+=Rect(650,95,275,310)+T(790,140,'Zeitkonstante')+T(790,178,'τ = R · C','formula')+T(790,210,'10 kΩ · 100 µF','tiny')+T(790,246,'τ = 1 s','formula')+T(790,292,'bei t = 1 s:','tiny')+T(790,326,'UC ≈ 7,585 V','formula')+T(790,366,'nach 5τ etwa 99,3 %','tiny')
graph['1.09-C']=S('1.09-C · RC-Ladefunktion','Exponentielle Ladekurve eines RC-Glieds mit 12 Volt, zehn Kiloohm und 100 Mikrofarad. Nach einer Sekunde 63,2 Prozent der Endspannung beziehungsweise rund 7,585 Volt.',b)
# 4 sine 50 Hz 0-40ms
b=Rect(35,95,595,305)+T(330,129,'u(t) = 10 V · sin(2π · 50 Hz · t)')
ax_x,ax_y,w,h=100,180,475,154
b+=L(ax_x,ax_y+h/2,ax_x+w,ax_y+h/2,'thin')+L(ax_x,ax_y,ax_x,ax_y+h,'thin')
for j in range(0,5):
 x=ax_x+w*j/4;b+=L(x,ax_y+h/2,x,ax_y+h/2+5,'thin')+T(int(x),360,str(10*j)+' ms','tiny')
b+=plot(ax_x,ax_y,w,h,lambda t:10*sin(2*pi*50*t/1000),40,-11,11)
b+=T(70,187,'+10 V','tiny')+T(70,258,'0 V','tiny')+T(70,334,'−10 V','tiny')
b+=Rect(665,95,260,305)+T(795,139,'Periodendauer')+T(795,179,'T = 1 / f','formula')+T(795,212,'f = 50 Hz','tiny')+T(795,250,'T = 20 ms','formula')+T(795,302,'nach 5 ms: +10 V','tiny')+T(795,328,'nach 15 ms: −10 V','tiny')
graph['1.10-A']=S('1.10-A · Frequenz und Sinus','Zwei Perioden einer idealen Sinusspannung von 50 Hertz und 10 Volt Spitze zwischen 0 und 40 Millisekunden; Periodendauer 20 Millisekunden.',b)
# 5 RMS
b=Rect(35,95,610,310)+T(338,130,'Sinus mit Spitzenwert 100 V')
ax_x,ax_y,w,h=110,177,475,166
b+=L(ax_x,ax_y+h/2,ax_x+w,ax_y+h/2,'thin')+L(ax_x,ax_y,ax_x,ax_y+h,'thin')
b+=plot(ax_x,ax_y,w,h,lambda t:100*sin(2*pi*t),1,-110,110)
for v in (-100/sqrt(2),100/sqrt(2)):
 y=ax_y+h*(110-v)/220;b+=P(f'M{ax_x} {y:.1f} H{ax_x+w}','dashed')
b+=T(65,183,'+100 V','tiny')+T(69,261,'0 V','tiny')+T(65,342,'−100 V','tiny')+T(360,365,'gestrichelt: ± Ueff = ± 70,7 V','tiny')
b+=Rect(670,95,255,310)+T(797,145,'Effektivwert')+T(797,186,'Ueff = Û / √2','formula')+T(797,222,'Û = 100 V','tiny')+T(797,266,'Ueff ≈ 70,7 V','formula')+T(797,325,'gilt für idealen Sinus','tiny')
graph['1.10-B']=S('1.10-B · Spitzen- und Effektivwert','Ideal sinusförmige Wechselspannung mit 100 Volt Spitzenwert und ungefähr 70,7 Volt Effektivwert. Sinuskurve und RMS-Hilfslinien.',b)
# 6 load profile
b=Rect(35,95,595,313)+T(326,126,'Fiktiver 24-Stunden-Lastgang (6-h-Mittelwerte)')
ax_x,ax_y,w,h=95,180,485,166
b+=L(ax_x,ax_y+h,ax_x+w,ax_y+h,'thin')+L(ax_x,ax_y,ax_x,ax_y+h,'thin')
segments=[(2,0,6),(8,6,12),(6,12,18),(3,18,24)]
for power,start,end in segments:
 x=ax_x+w*start/24;ww=w*(end-start)/24;hh=h*power/9
 b+=f'<rect x="{x:.1f}" y="{ax_y+h-hh:.1f}" width="{ww:.1f}" height="{hh:.1f}" fill="#bcdfe7" stroke="#176d85" stroke-width="1.4"/>'
 b+=T(round(x+ww/2),round(ax_y+h-hh-9),str(power)+' kW','tiny')
for j in range(0,5):
 x=ax_x+w*j/4;b+=T(round(x),366,str(j*6)+' h','tiny')
b+=Rect(665,95,260,313)+T(795,142,'Tagesenergie')+T(795,184,'E = Σ (P · Δt)','formula')+T(795,221,'6 h · (2 + 8 + 6 + 3)','tiny')+T(795,260,'E = 114 kWh','formula')+T(795,303,'mittlere Leistung:','tiny')+T(795,333,'4,75 kW','formula')+T(795,377,'6-h-Mittel, keine Spitzenmessung','tiny')
graph['1.10-C']=S('1.10-C · Lastprofil und Energie','Fiktives Lastprofil mit vier sechs Stunden langen Abschnitten: 2, 8, 6 und 3 Kilowatt. Tagesenergie 114 Kilowattstunden, Tagesmittel 4,75 Kilowatt.',b)
for lid,svg in graph.items():
 ET.fromstring(svg)
 for folder in ('visuals','learning-visuals'):(R/folder/(lid+'.svg')).write_text(svg,encoding='utf8')
 print(lid,'svg',len(svg))
