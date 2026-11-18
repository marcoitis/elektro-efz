#!/usr/bin/env python3
"""Traceability, not certification. No automatic system may sign off Swiss norms."""
from __future__ import annotations
import json,re,csv,datetime
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent.parent
D=json.loads((R/'data.js').read_text(encoding='utf-8').split('=',1)[1].strip(' ;\n'))
N=json.loads((R/'norm_course.json').read_text(encoding='utf-8'))
V=json.loads((R/'lesson-visuals.json').read_text(encoding='utf-8'))
# File completeness was established from 14 user-provided PDFs. Technical compliance has NOT been approved.
FULL=[
 ('Werkvorschriften CH 2025','20251204-be-werkvorschriften-ch.pdf','WV-CH 2025',64),
 ('SN 414022:2024','SN414022{2024}2f.pdf','SN 414022',68),
 ('SN 414113:2024-12','SN414113{2024-12}f.pdf','SN 414113',24),
 ('SN EN 50110-1:2023','SNEN50110-1{2023}e.pdf','50110-1',57),
 ('SN EN 50110-2:2023','SNEN50110-2{2023}e.pdf','50110-2',52),
 ('SN EN IEC 61439-1:2021','SNEN_IEC_61439-1_2021.pdf','61439-1',180),
 ('SN EN IEC 61439-2:2021','SNEN_IEC_61439-2_2021.pdf','61439-2',61),
 ('SN EN 61439-4:2013','SNEN61439-4{2013}D.pdf','61439-4',34),
 ('SN EN 62446-1:2016+A1:2018','SNEN_62446-1_2016+A1_2018.pdf','62446-1',45)
]
PARTIAL=[('SN EN IEC 61439-3:2024','SNENIEC61439-3{2024}dX.pdf','61439-3',6),('SN EN IEC 61439-5:2023','SNENIEC61439-5{2023}dX.pdf','61439-5',5),('SN EN IEC 61439-7:2023','SNENIEC61439-7{2023}dX.pdf','61439-7',5),('SN EN 61439-6:2012','SNEN61439-6{2012}DX.pdf','61439-6',6),('SN EN IEC 62446-2:2020','SNENIEC62446-2{2020}DX.pdf','62446-2',5)]
W=R.parent
src_file_status=[]
try:
 import fitz
 for cat,entries in [('full',FULL),('excerpt',PARTIAL)]:
  for name,fn,key,count in entries:
   fp=W/fn;pages=len(fitz.open(fp)) if fp.exists() else 0
   src_file_status.append({'title':name,'filename':fn,'coverage':cat,'expected_pages':count,'actual_pages':pages,'page_count_matches':pages==count,'published':False})
except ImportError:
 for cat,entries in [('full',FULL),('excerpt',PARTIAL)]:
  for name,fn,key,count in entries:src_file_status.append({'title':name,'filename':fn,'coverage':cat,'expected_pages':count,'actual_pages':None,'page_count_matches':None,'published':False})

full_patterns={name:re.compile(re.escape(key),re.I) for name,_,key,_ in FULL}
partial_patterns={name:re.compile(re.escape(key),re.I) for name,_,key,_ in PARTIAL}
keys=[k for _,_,k,_ in FULL+PARTIAL]
rows=[]
vis={x['id']:x for x in V}
for l,norm in [(x,False) for x in D['lessons']]+[(x,True) for x in N['lessons']]:
 lid='N-'+l['id'] if norm else l['id']
 refs=[l['source']] if norm else l.get('references',[])
 ref_text='; '.join(refs)
 available=[name for name,p in full_patterns.items() if p.search(ref_text)]
 partial=[name for name,p in partial_patterns.items() if p.search(ref_text)]
 missing=[]
 if 'NIN' in ref_text.upper() or '411000' in ref_text: missing.append('NIN SN 411000:2025 Volltext + Corrigendum')
 # Avoid accidentally treating a number of a standard as a different part of the series
 if re.search(r'61439(?![-\d])',ref_text,re.I) and not available and not partial: missing.append('Konkreter Teil der SN EN IEC 61439-Reihe klären')
 if re.search(r'\bESTI\b',ref_text,re.I):missing.append('ESTI-Weisung in aktueller amtlicher Fassung verifizieren')
 if re.search(r'\bNIV\b|\bElG\b',ref_text,re.I):missing.append('Aktuellen amtlichen Fedlex-Stand/Artikel prüfen')
 if re.search(r'60617|61010|60529|61851|62305|60364',ref_text,re.I):missing.append('Genannte externe Fachnorm nicht im PDF-Bestand')
 if re.search(r'BiVo2015|Lehrplan|Bildungsplan',ref_text,re.I):missing.append('BiVo 2015/2026: zutreffenden QV-Zweig mit Kanton klären')
 if norm and not available and not partial:missing.append('Quellenzuordnung nicht eindeutig aus vorhandenem PDF-Bestand')
 p=(R/'tts_scripts'/f'{lid}.txt')
 words=len(p.read_text(encoding='utf-8').split()) if p.exists() else 0
 dur=round(words/130,1)
 # 15 min requires ~1950 words at ~130 words/min; assumption documented.
 status='AUSSTEHEND – fachliche Einzelprüfung durch Elektrofachperson'
 rec={
  'id':lid,'title':l['title'],'course':('Normen' if norm else str(l['moduleId'])[0]+'. Lehrjahr'),
  'references':refs,'source_pdf_present':available,'source_pdf_excerpt_only':partial,'missing_or_followup':sorted(set(missing)),
  'normaussagen_freigegeben':False,'fachliche_einzelpruefung':False,'grafik_fachlich_abgenommen':False,
  'manual_script_editorial':any((R/folder/(lid+'.txt')).exists() for folder in ('editorial_v092','editorial_v094','editorial_v095','editorial_v096','editorial_v097')),'manual_schematic_editorial':any((R/f/(lid+'.txt')).exists() for f in ('editorial_v094','editorial_v095','editorial_v096','editorial_v097')),
  'technical_review_status':status,
  'script_words':words,'tts_minutes_estimate_130wpm':dur,'15_to_30_minute_target':bool(words>=1950 and words<=3900),
  'visual':vis[lid]['file'],'visual_type':vis[lid]['visual_type'],
  'warning':'Nur didaktische Lernunterlage. Keine Installationsfreigabe oder normengeprüfte Ausführungsplanung.'
 }
 rows.append(rec)
report={'version':'0.9.7-preflight','created':'2026-11-17','curriculum':'BiVo 2015 (Altstand); Neuordnung 2026 noch zuzuordnen',
 'norm_statement':'Keine Normenkonformität bestätigt: NIN 2025 Volltext fehlt, 5 Norm-PDFs sind nur Kurzfassungen.',
 'standards_pdfs':src_file_status,'lessons':rows}
(R/'quality-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'lesson-audit.js').write_text('/* Fachlich NICHT freigegeben; Transparenz vor Scheinpräzision. */\nwindow.ElektroLessonAudit = '+json.dumps({x['id']:{k:v for k,v in x.items() if k in ('id','references','missing_or_followup','source_pdf_present','source_pdf_excerpt_only','technical_review_status','script_words','tts_minutes_estimate_130wpm','15_to_30_minute_target','visual')} for x in rows},ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
with (R/'quality-review.csv').open('w',encoding='utf-8-sig',newline='') as f:
 wr=csv.writer(f,delimiter=';');wr.writerow(['Lektion','Titel','Skript-Wörter','Dauer bei 130 W/min','Ziel 15–30 Min','Voll-PDF vorhanden (keine Freigabe)','PDF nur Auszug','Noch ausstehende Quellen','Fachprüfung','Grafik'])
 for x in rows:wr.writerow([x['id'],x['title'],x['script_words'],x['tts_minutes_estimate_130wpm'],'ja' if x['15_to_30_minute_target'] else 'nein',', '.join(x['source_pdf_present']),', '.join(x['source_pdf_excerpt_only']),', '.join(x['missing_or_followup']),'OFFEN',x['visual']])
(R/'QUALITAETSMATRIX_README.md').write_text('''# Normen-, Fachtext- und Grafikprüfung – Transparenzbericht\n\nStand: 17.11.2026 · Version 0.9.7\n\n**Dieser Bericht ist eine Bestandsaufnahme, kein Normkonformitätsnachweis.**\n\n## Prüfstatus\n\n- 178 Lektionen erhalten eine individuelle themenbezogene SVG-Lerngrafik. Die meisten Grafiken sind didaktische Schemata und **keine** konstruktiv abgenommenen Installationspläne.\n- Jede Lektion besitzt einen referenzierten Fachtext und ein Sprechskript. Für 15–30 Minuten Sprecherzeit setzen wir als grobe Annahme 130 Wörter/Minute an: benötigt ungefähr 1'950–3'900 Wörter. Das ist ein **Zeitindikator**, kein Qualitätsnachweis.\n- Normenbasis: neun vollständige vom Nutzer bereitgestellte Fach-PDFs; fünf nur in Auszügen. Die **NIN SN 411000:2025** einschliesslich Corrigendum ist in diesem Bestand **nicht vollständig vorhanden**.\n- Auch eine vorhandene vollständige Normdatei bedeutet **keine fachlich geprüfte Einzelaussage**. Ohne clause-by-clause Kontrolle gegen die gültige Ausgabe und Freigabe durch eine befähigte Person ist keine Lektion als normengeprüft markiert.\n- Kein geschütztes Norm-PDF und kein längerer Normtext wird auf GitHub veröffentlicht.\n\n## Abklärungsbedarf\n\n1. Zulässigen Bildungs- und Prüfungsplan für den angestrebten Art.-32-BBV-Abschluss bei der zuständigen kantonalen Stelle bestätigen lassen: bisherige BiVo 2015 / Übergangsrecht / BiVo 2026.\n2. Rechtmässigen Zugriff auf NIN 2025 und deren Korrekturen sicherstellen.\n3. Fünf unvollständige Normen bei relevanten Lektionen durch rechtmässig verfügbare Vollausgaben ergänzen.\n4. Jede Normenaussage mit Norm, Ausgabe, Abschnitt, Randbedingungen und Fachfreigabe nachvollziehbar protokollieren.\n5. Jede didaktische Zeichnung separat gegen ihre physikalische Aussage prüfen und mit 'keine Ausführungsplanung' kennzeichnen.\n\n## Verfügbare Dateien\n\n- `quality-review.csv`: 178 einzelne Prüfreihen mit Wortumfang, SVG und Quellenlücken.\n- `quality-review.json`: maschinenlesbare Matrix mit Prüffeldern und Status.\n- `lesson-visuals.json`: Zeichnungsregister zu allen 178 Lektionen.\n\n## Amtliche allgemeine Ausgangspunkte\n\n- https://www.eit.swiss/de/bildung/grundbildung/elektroinstallateurin-efz\n- https://www.electrosuisse.ch/de/nin-2025/\n- https://www.fedlex.admin.ch/eli/cc/2002/22/de\n\n**Elektrische Installationsarbeiten, spannungsführende Messungen und PV-DC-Steckarbeiten erfordern die gesetzlich notwendige Berechtigung und Fachaufsicht.**\n''',encoding='utf-8')
print('Audit rows:',len(rows),'source pdf records:',len(src_file_status),'15–30-minute scripts:',sum(x['15_to_30_minute_target'] for x in rows))
print('Top missing:',Counter(k for x in rows for k in x['missing_or_followup']).most_common(6))
