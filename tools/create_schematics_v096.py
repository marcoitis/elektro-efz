#!/usr/bin/env python3
"""Six independently composed vector diagrams for lessons 1.05-1.06.
Illustrative, not IEC-symbol certified or executable installation schematics.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
from html import escape
from math import pi
R=Path(__file__).resolve().parent.parent
CSS='''<style>text{font-family:DejaVu Sans,Arial,sans-serif;fill:#18364b}.title{font-size:24px;font-weight:700}.sub{font-size:12px;fill:#527083}.lab{font-size:15px;font-weight:600}.tiny{font-size:12px;fill:#4d6677}.formula{font-size:19px;fill:#b86b19;font-weight:700}.small{font-size:14px}.wire{stroke:#11718e;stroke-width:3;fill:none;stroke-linecap:round;stroke-linejoin:round}.thin{stroke:#8da7b6;stroke-width:1.5;fill:none;stroke-linecap:round}.dash{stroke:#db8928;stroke-width:2;stroke-dasharray:6 5;fill:none}.box{fill:white;stroke:#d7e5eb;stroke-width:1.8}</style>'''
def text(x,y,s,cls='lab',anchor='middle'): return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}">{escape(str(s))}</text>'
def rect(x,y,w,h,fill='white',stroke='#b9d0dc',r=10,sw=1.5):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def line(x1,y1,x2,y2,cls='wire'): return f'<path d="M{x1} {y1} L{x2} {y2}" class="{cls}"/>'
def circ(x,y,r,fill='white',stroke='#11718e',sw=2):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def title(t,d,b): return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 560" role="img" aria-label="{escape(t)}"><title>{escape(t)}</title><desc>{escape(d)}</desc>{CSS}<rect x="0" y="0" width="1100" height="560" rx="20" fill="#f2f7fa"/>{text(30,40,t,'title','start')}{text(30,62,'Didaktisches Fachmodell · keine Installationsplanung · keine Ausführungsplanung · Schweizer Normenprüfung offen','sub','start')}{b}{text(30,540,'Bezeichnungen und Modellwerte nur für Unterricht; Produkte, Normen und Installation gesondert prüfen.','sub','start')}</svg>'''
G={}
# 1.05-A: two different material resistivities with same geometry and an explicit copper-return example
b=rect(28,89,650,417)+rect(703,89,367,417)
b+=text(353,124,'Einzel-Leiter: l = 20 m, A = 2,5 mm²')
for y,mat,rho,color,width,Rohm in [(185,'Kupfer',0.01724,'#cb7c3d',410,0.13792),(275,'Aluminium',0.02826,'#6c8daa',410,0.22608)]:
 b+=f'<rect x="130" y="{y-21}" width="{width}" height="25" rx="10" fill="{color}"/>'
 b+=text(90,y,mat,'small')+text(350,y+34,f'ρ = {rho:.5f} Ω·mm²/m | R = {Rohm:.5f} Ω','small')
b+=text(353,353,'Bei gleichen Abmessungen: Aluminium ≈ 1,64 × R(Cu)','formula')
b+=line(144,395,537,395,'thin')+text(353,423,'Doppelte Länge → doppelter Widerstand','small')+text(353,450,'Doppelter Querschnitt → halber Widerstand','small')
b+=text(882,127,'Hin- und Rückweg, Modell')
b+=text(882,170,'2 × 20 m Cu, 2,5 mm²','small')+text(882,215,'R = 0,27584 Ω','formula')
b+=text(882,255,'I = 4 A','small')+text(882,298,'ΔU ≈ 1,10 V','formula')+text(882,338,'P = I² · R','small')+text(882,380,'P ≈ 4,41 W','formula')+text(882,444,'Kontakt- und Wärmefragen offen','tiny')
G['1.05-A']=title('1.05-A · Leiterwerkstoffe und Widerstand','Kupfer mit 0,01724 und Aluminium mit 0,02826 Ohm Quadratmillimeter pro Meter, je 20 m und 2,5 mm²; Widerstände Kupfer 0,13792 Ohm und Aluminium 0,22608 Ohm. Vierzig Meter Hin- und Rückleiter aus Kupfer 0,27584 Ohm, bei vier Ampere 1,10 Volt Spannungsfall und 4,41 Watt Verlust.',b)
# 1.05-B: clear cutaway schematic, safe color functional labels, explicitly not terminal proof
b=rect(28,90,632,418)+rect(688,90,382,418)
b+=text(344,126,'Schematischer Querschnitt einer 3-adrigen Leitung')
b+=circ(345,300,158,'#eef3f6','#587e90',8)
for x,y,ins,lab,lc in [(345,220,'#735033','L / braun','#ffffff'),(275,360,'#386daa','N / blau','#ffffff'),(415,360,'#5ba54b','PE / grün-gelb','#101c18')]:
 b+=circ(x,y,61,ins,'#253d48',2)+circ(x,y,31,'#cf8c54','#815332',2)
 if lab.startswith('PE'):
  b+=f'<path d="M{x-52} {y-29} L{x+52} {y+29}" stroke="#ecd23c" stroke-width="19"/>'
  b+=circ(x,y,31,'#cf8c54','#815332',2)  # metal conductor must not be striped
 b+=text(x,y+76,lab,'tiny')
b+=text(345,470,'Mantel, Aderisolation und metallische Leiter getrennt bewerten','tiny')
b+=text(878,130,'Kennzeichnung ≠ Spannungsnachweis')
b+=text(878,174,'N: Neutralleiter – blau','small')+text(878,212,'PE: Schutzleiter – grün/gelb','small')+text(878,251,'L: Aussenleiter (Beispiel)','small')
b+=rect(724,292,310,140,'#fff8ec','#e0b97b')
b+=text(880,323,'Zusätzliche Produktprüfung','lab')+text(880,354,'Leiterklasse / Klemme / Material','tiny')+text(880,380,'Temperatur / UV / Anwendung','tiny')+text(880,408,'Herstellerdaten erforderlich','tiny')
G['1.05-B']=title('1.05-B · Kabelaufbau und Leiterfarben','Vereinfachter dreiadriger Kabelquerschnitt mit Kupferkernen und brauner, blauer und grün-gelber Aderisolation. Farbkennzeichnung ist kein Beweis für Spannungsfreiheit, weitere Produktauswahl und NIN-Prüfung erforderlich.',b)
# 1.05-C IP classification and what it excludes
b=rect(28,90,580,415)+rect(635,90,435,415)
b+=text(310,129,'Beispiel: IP65 ist keine Allzweck-Freigabe')
for x,c,xx in [(88,'IP','Bezeichnung'),(213,'6','Fremdkörper / Staub'),(347,'5','Wasserstrahl-Prüfung')]:
 b+=rect(x,178,114,95,'#e1edf3','#91adbf',10,2)+text(x+57,240,c,'title')+text(x+57,300,xx,'tiny')
b+=text(310,347,'Ziffern beschreiben definierte Prüfbedingungen','small')
b+=text(310,391,'X bedeutet: Kennziffer hier nicht angegeben','small')
b+=text(310,436,'Nicht jede höhere Ziffer ersetzt andere Prüfarten','small')
b+=text(852,130,'Zusätzliche Umweltfragen')
labels=[('UV / Sonne','Produktnachweis erforderlich'),('Temperatur / Kondensat','Einbausituation prüfen'),('Chemikalien / Salz','Werkstoffverträglichkeit'),('Schlag / Vibration','mechanischen Nachweis prüfen'),('Verschraubung / Dichtung','Gesamtsystem beurteilen')]
for i,(a,bb) in enumerate(labels):
 yy=171+i*61
 b+=circ(665,yy-5,5,'#d88d32','#d88d32')+text(685,yy,a,'small','start')+text(685,yy+19,bb,'tiny','start')
G['1.05-C']=title('1.05-C · Schutzarten und Umwelteinflüsse','Erläuterung IP 65 mit erster Kennziffer für Staub, zweiter Kennziffer für Wasserprüfung. UV, Temperatur, Kondensat, Chemikalien, Stösse, Kabelverschraubung und Dichtungen brauchen gesonderte Nachweise.',b)
# 1.06-A 3 views of same conceptual model
b=rect(24,87,345,422)+rect(381,87,345,422)+rect(738,87,338,422)
b+=text(197,122,'1 · Raumansicht: Wo?')
b+=rect(84,155,225,264,'#f8fbfd','#3c718f',2,3)
b+=rect(84,303,42,72,'#f2f7fa','#f2f7fa',0,0) # opening door drawn as gap
b+=circ(208,271,22,'#fae9ba','#ce9631',3)+text(208,278,'L','lab')
b+=rect(110,331,27,25,'#dfebf1','#356b85',2)+text(123,350,'S','tiny')
b+=rect(260,180,30,36,'#c6e6ec','#42788e',3)+text(275,204,'Q','tiny')
b+=text(197,450,'4 × 5 m · Planlage (nicht skaliert)','tiny')
b+=text(553,122,'2 · Stromlauf: Wie?')
b+=line(420,213,502,213)+line(570,213,595,213)+line(645,213,680,213)
b+=line(680,213,680,372)+line(680,372,420,372)+line(420,372,420,313)+line(420,271,420,213)
b+=circ(420,292,20)+text(420,299,'Q','small')
b+=circ(502,213,4,'#11718e','#11718e')+circ(570,213,4,'white','#11718e')+line(502,213,558,189)
b+=text(535,177,'S offen (Modell)','tiny')
b+=circ(620,213,25,'#fff4cf','#a47c2f')+text(620,219,'L','small')
b+=text(553,449,'Symbolische 12-V-Funktion, nicht normativ','tiny')
b+=text(908,122,'3 · Übersicht: Was?')
for y,lab in [(185,'Quelle Q'),(280,'Schalter S'),(375,'Leuchte L')]:
 b+=rect(802,y,211,54,'#e6f2f6','#7aaabd',6)+text(907,y+34,lab,'lab')
b+=line(907,239,907,280,'thin')+line(907,334,907,375,'thin')
b+=text(907,465,'gleiche Gerätekennung in allen Plänen','tiny')
G['1.06-A']=title('1.06-A · Planarten und ihre Perspektiven','Links symbolischer Raumgrundriss mit Quelle Q, Schalter S und Leuchte L. Mitte abstrakter Kleinspannungsstromkreis. Rechts Funktionsübersicht. Die Pläne zeigen Ort, elektrische Verbindung und Struktur.',b)
# 1.06 B: split two representations and terminal references; not IEC compliant
b=rect(26,89,640,414)+rect(694,89,380,414)
b+=text(343,127,'Eine Funktion, zwei Darstellungsorte')
b+=text(200,172,'Blatt 1 · Steuerung','small')+text(515,172,'Blatt 2 · Anzeige','small')
b+=line(72,288,138,288)+line(262,288,312,288)+line(421,288,435,288)+line(535,288,609,288)
b+=circ(200,288,61,'#f2f7fa','#19728e',3)+text(200,284,'K-MODELL','small')+text(200,305,'Spule','tiny')
b+=rect(435,263,100,52,'#e7f0f4','#39748a',4)+text(485,284,'Kontakt','small')+text(485,306,'(Modell)','tiny')
b+=line(289,216,440,216,'dash')+text(366,204,'gleiche Gerätekennung','tiny')
b+=text(340,350,'Zwischen Blättern kein durchgehender Leiter','tiny')
b+=text(341,379,'Zusammenhang per Kennung / Querverweis','small')+text(341,424,'Kein Netzanschluss; Schema nicht IEC-validiert','tiny')
b+=text(886,134,'Klemmenliste (Übung)')
for y,lab in [(184,'Q1:+  → S1:1'),(227,'S1:2  → X1:1'),(270,'X1:1  → L1:+'),(313,'L1:−  → Q1:−')]:
 b+=rect(733,y-27,305,35,'#eef4f7','#c6d9e4',5)+text(885,y-5,lab,'small')
b+=text(883,397,'Kennungen frei erfunden','tiny')+text(883,423,'Anschlussidentität ≠ Spannungsfreiheit','tiny')
G['1.06-B']=title('1.06-B · Klemmen, Querverweise und Symbole','Didaktisches Spulen-Kontakt-Modell mit Querverweis über zwei Blattorte, und fiktive Klemmenliste einer Kleinspannungsleuchte. Kennungen nicht normativ, nicht zur Ausführung.',b)
# 1.06 C revisions and scale
b=rect(25,88,624,420)+rect(675,88,398,420)
b+=text(335,126,'Änderungsfolgenanalyse · Modellbeleuchtung')
b+=rect(88,169,205,58,'#e3f1f6','#5f9fb6')+text(188,203,'Revision A · 1 Leuchte')
b+=rect(367,169,210,58,'#faebd6','#c98d3d')+text(471,203,'Revision B · 2 Leuchten')
b+=line(293,198,367,198,'thin')
for y,lab in [(279,'Grundriss · Position ergänzen'),(318,'Stromlaufplan · Funktion ändern'),(357,'Stückliste · Menge aktualisieren'),(396,'Prüfblatt · Revisionsstand neu prüfen')]:
 b+=circ(104,y-5,6,'#d18b37','#d18b37')+text(127,y,lab,'small','start')
b+=text(336,468,'Beide Fassungen müssen eindeutig zuordenbar sein','tiny')
b+=text(875,126,'Massstab nur im gültigen Ausgabeformat')
b+=text(875,176,'8,4 cm im Plan · 1 : 50','small')+text(875,216,'= 4,2 m real','formula')
b+=text(875,266,'Ausdruck auf 70 % verkleinert','small')+text(875,308,'8,4 cm → 5,88 cm','formula')
b+=text(875,348,'Alte Skala wäre dann falsch','small')
b+=text(875,420,'Massangaben sind sicherer als Abmessen','tiny')
G['1.06-C']=title('1.06-C · Revision, Massstab und Stückliste','Änderungsfolgen einer zusätzlichen Kleinspannungsmodell-Leuchte: Grundriss, Stromlauf, Stückliste, Prüfrevision. Massstabsbeispiel 8,4 cm bei 1:50 bedeutet 4,2 Meter, Verkleinerung auf 70 Prozent ergibt 5,88 cm im Ausdruck.',b)
assert len(G)==6
for lid,svg in G.items():
 ET.fromstring(svg)
 for folder in ('visuals','learning-visuals'):(R/folder/(lid+'.svg')).write_text(svg,encoding='utf8')
 print(lid, len(svg),'svg bytes')
