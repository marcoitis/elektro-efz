#!/usr/bin/env python3
"""Create a deterministic 15-batch audio review plan; NO voice model or MP3 generated.
Works locally, no pip dependencies. For a pilot, prepare text segments for approval.
"""
from pathlib import Path
import argparse,csv,json,hashlib,re
R=Path(__file__).resolve().parent.parent
PILOT=['1.01-A','2.05-B','N-P02']
def catalog():
 data=json.loads((R/'data.js').read_text(encoding='utf8').split('=',1)[1].strip(' ;\n'))
 norm=json.loads((R/'norm_course.json').read_text(encoding='utf8'))
 lessons=[{'id':x['id'],'title':x['title']} for x in data['lessons']]
 lessons.extend({'id':'N-'+x['id'],'title':x['title']} for x in norm['lessons'])
 if len(lessons)!=178 or len({x['id'] for x in lessons})!=178:raise SystemExit('Expected exactly 178 unique lessons')
 for item in lessons:
  content=(R/'tts_scripts'/(item['id']+'.txt')).read_bytes()
  item['words']=len(content.decode('utf8').split());item['sha256']=hashlib.sha256(content).hexdigest()
 return lessons

def segments(text,max_words=180):
 # Split on paragraph boundaries and hard-split only long paragraphs.
 paras=[p.strip() for p in re.split(r'\n\s*\n',text) if p.strip()]
 out=[];buf=[];count=0
 def flush():
  nonlocal buf,count
  if buf:out.append('\n\n'.join(buf));buf=[];count=0
 for p in paras:
  n=len(p.split())
  if n>max_words:
   flush();words=p.split()
   for i in range(0,n,max_words):out.append(' '.join(words[i:i+max_words]))
  elif count+n>max_words:
   flush();buf=[p];count=n
  else:buf.append(p);count+=n
 flush();return out

def main():
 p=argparse.ArgumentParser();p.add_argument('--size',type=int,default=12);p.add_argument('--pilot',action='store_true');p.add_argument('--batch',type=int);p.add_argument('--ids',default='');p.add_argument('--segment-words',type=int,default=180);a=p.parse_args()
 if a.size<1 or a.segment_words<60:raise SystemExit('Invalid batch or segment size')
 items=catalog();batches=[items[i:i+a.size] for i in range(0,len(items),a.size)]
 out=R/'audio-plan';out.mkdir(exist_ok=True)
 with (out/'batches.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.writer(f,delimiter=';');w.writerow(['Batch','ID','Thema','Wörter','Skript_SHA256','Status','Aussprache_geprüft','Audio_Abnahme','Bemerkungen'])
  for i,b in enumerate(batches,1):
   for x in b:w.writerow([i,x['id'],x['title'],x['words'],x['sha256'],'Skript fertig – AUDIO OFFEN','','',''])
 (out/'batches.json').write_text(json.dumps({'project':'Elektro EFZ v0.11.8','wordcount':sum(x['words'] for x in items),'total_lessons':178,'batch_size':a.size,'pilot':PILOT,'batches':[{'number':i,'ids':[x['id'] for x in b]} for i,b in enumerate(batches,1)]},ensure_ascii=False,indent=2),encoding='utf8')
 print(f'Plan: {len(batches)} batches / {len(items)} lessons, stored in audio-plan/')
 ids=PILOT if a.pilot else ([x['id'] for x in batches[a.batch-1]] if a.batch and 1<=a.batch<=len(batches) else [])
 if a.ids:ids=[x.strip() for x in a.ids.split(',') if x.strip()]
 if not ids:return
 known={x['id'] for x in items}
 if any(x not in known for x in ids):raise SystemExit('Unknown lesson in selection')
 review=R/'audio-review'/'pilot' if a.pilot else R/'audio-review'/('batch-'+str(a.batch or 'custom').zfill(2))
 review.mkdir(parents=True,exist_ok=True)
 with (review/'abnahme.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.writer(f,delimiter=';');w.writerow(['ID','Segment','Prüfung','Aussprache','Zahlen_Einheiten','Pausen','Stimme','Freigabe_ja_nein','Notizen'])
  for lid in ids:
   text=(R/'tts_scripts'/(lid+'.txt')).read_text(encoding='utf8')
   for n,part in enumerate(segments(text,a.segment_words),1):
    folder=review/lid;folder.mkdir(exist_ok=True)
    (folder/(str(n).zfill(3)+'.txt')).write_text(part+'\n',encoding='utf8')
    w.writerow([lid,n,'offen','offen','offen','offen','offen','NEIN',''])
 print(f'Audio review text segments prepared for {len(ids)} lessons: {review}')
if __name__=='__main__':main()
