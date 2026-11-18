#!/usr/bin/env python3
"""Turn manually edited manuscripts into short, readable slide segments, without changing their wording."""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parent.parent
out={}
for file in sorted([* (R/'editorial_v092').glob('*.txt'), * (R/'editorial_v094').glob('*.txt'), * (R/'editorial_v095').glob('*.txt'), * (R/'editorial_v096').glob('*.txt'), * (R/'editorial_v097').glob('*.txt')]):
 content=file.read_text(encoding='utf8')
 paragraphs=[p.strip() for p in content.split('\n\n') if p.strip()]
 if not paragraphs:continue
 groups=[];heading='Einführung';parts=[]
 def flush():
  if parts:groups.append((heading,'\n\n'.join(parts)))
 for p in paragraphs:
  if re.match(r'^(Abschnitt\s+\w+\.|Einleitung|Einstieg:|Abschluss)',p,re.I) and len(p)<110:
   flush();heading=p.rstrip('.');parts=[]
  else:parts.append(p)
 flush()
 slides=[]
 for h,body in groups:
  if not body:continue
  # Keep paragraphs intact where possible; split long paragraphs at sentence boundaries.
  items=[]
  for p in body.split('\n\n'):
   if len(p.split())<185:items.append(p);continue
   pieces=re.split(r'(?<=[.!?])\s+(?=[A-ZÄÖÜ0-9])',p)
   chunk=[];total=0
   for sent in pieces:
    n=len(sent.split())
    if total+n>160 and chunk:items.append(' '.join(chunk));chunk=[];total=0
    chunk.append(sent);total+=n
   if chunk:items.append(' '.join(chunk))
  chunk=[];length=0;segs=[]
  for item in items:
   n=len(item.split())
   if length+n>180 and chunk:
    segs.append('\n\n'.join(chunk));chunk=[];length=0
   chunk.append(item);length+=n
  if chunk:segs.append('\n\n'.join(chunk))
  for i,text in enumerate(segs,1):
   name=h+(f' · {i}/{len(segs)}' if len(segs)>1 else '')
   slides.append({'heading':name,'text':text,'formula':''})
 out[file.stem]=slides
 print(file.stem,'lesson chapter slides',len(slides),'words',sum(len(s['text'].split()) for s in slides))
(R/'lesson-long-slides.js').write_text('/* Hand-edited chapter slides for selected 15–30-minute lessons. */\nwindow.ElektroLongSlides='+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf8')
