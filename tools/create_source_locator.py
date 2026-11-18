#!/usr/bin/env python3
"""Find PDF page candidates for norm-chapter anchors; do not certify the clauses."""
from pathlib import Path
import csv,re,json,fitz
R=Path(__file__).resolve().parent.parent
ROOT=R.parent
N=json.loads((R/'norm_course.json').read_text(encoding='utf-8'))['lessons']
standards={
 'WV-CH':'20251204-be-werkvorschriften-ch.pdf',
 '50110-1':'SNEN50110-1{2023}e.pdf','50110-2':'SNEN50110-2{2023}e.pdf',
 '62446-1':'SNEN_62446-1_2016+A1_2018.pdf',
 '61439-1':'SNEN_IEC_61439-1_2021.pdf','61439-2':'SNEN_IEC_61439-2_2021.pdf','61439-4':'SNEN61439-4{2013}D.pdf',
 '414113':'SN414113{2024-12}f.pdf','414022':'SN414022{2024}2f.pdf'
}
texts={}
for k,name in standards.items():
 d=fitz.open(ROOT/name)
 texts[k]=[p.get_text('text') for p in d]

def keys(source):
 matches=[k for k in standards if k in source]
 # unqualified '-2:2021' in I02 source means part 2
 if ' / -2:' in source and '61439-1' in source and '61439-2' not in matches:matches.append('61439-2')
 return matches

def targets(spec):
 # Identify chapter numbers without treating years/standard numbers as chapters.
 s=re.sub(r'\b(?:61439-1|61439-2|62446-1|50110-1|414022|414113|WV-CH)\s*:\s*','',spec)
 if 'Anhang' in s or 'Dateiumfang' in s or 'fehlt' in s:return []
 return list(dict.fromkeys(re.findall(r'(?<!\d)(?:\d{1,2}\.){0,4}\d{1,3}(?!\d)',s)))

def page_hits(key,section):
 candidates=[]
 # Literal numbers can appear in the running text; identify *probable* clause heading only.
 p=re.compile(r'(?m)^\s*'+re.escape(section)+r'(?![\d.])(?:\s|$|\s*[-—])')
 for i,text in enumerate(texts[key]):
  if p.search(text):candidates.append(i+1)
 return candidates[:12]
rows=[]
for l in N:
 ks=keys(l['source'])
 for spec in l['sections']:
  toks=targets(spec)
  if not toks:
   rows.append((l['id'],l['title'],l['source'],spec,', '.join(ks),'','', 'Anhang/Text oder unklare Kapitelangabe: manuell prüfen'))
   continue
  for sec in toks:
   kl=next((k for k in ks if k in spec),None)
   relevant=[kl] if kl else ks
   for k in relevant:
    hits=page_hits(k,sec)
    rows.append((l['id'],l['title'],l['source'],spec,k,sec,', '.join(map(str,hits)),
                'Fundstellen-Kandidaten – inhaltliche Normenaussage NICHT überprüft' if hits else 'Keine Überschrift gefunden; Kapitel/Edition manuell prüfen'))
out=R/'norm-abschnitt-fundstellen.csv'
with out.open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,delimiter=';');w.writerow(['Normen-Lektion','Titel','Norm(en)','Ursprünglicher Verweis','PDF-Zuordnung','Gesuchte Kapitelzahl','Mögliche PDF-Seiten (1-basiert)','Prüfbedeutung']);w.writerows(rows)
print('Norm lesson section locator rows',len(rows),'chapters with headings',sum(bool(x[6]) for x in rows),'unresolved',sum(not x[6] for x in rows))
