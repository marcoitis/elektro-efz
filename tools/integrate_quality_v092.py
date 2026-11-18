#!/usr/bin/env python3
"""Patch the existing working v0.9.1 frontend without changing local progress IDs."""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parent.parent
viz=json.loads((R/'lesson-visuals.json').read_text(encoding='utf8'))
assets=['./'+x['file'] for x in viz]
# Replace only image component with an individually authored SVG file, retain other studio features.
p=R/'studio.js';s=p.read_text(encoding='utf8')
start=s.index('function diagram(l,norm){');end=s.index('\nfunction render(l,norm,state){',start)
s=s[:start]+'''function diagram(l,norm){
 const id=key(l.id,norm);
 // The file is generated from the actual lecture title and learning goals, not an executable wiring diagram.
 const safeid=encodeURIComponent(id);
 const caption='Individuelle didaktische Grafik zu '+l.title+' – keine Installationsplanung';
 return `<figure class="studio-figure studio-individual-figure"><img src="./visuals/${safeid}.svg" loading="lazy" decoding="async" alt="${esc(caption)}"><figcaption>${esc(caption)}</figcaption></figure>`;
}
function reviewPanel(l,norm){
 const id=key(l.id,norm),r=window.ElektroLessonAudit?.[id];
 if(!r)return '';
 const sources=(r.references||[]).map(x=>`<li>${esc(x)}</li>`).join('');
 const gaps=(r.missing_or_followup||[]).map(x=>`<li>${esc(x)}</li>`).join('');
 const duration=Number(r.tts_minutes_estimate_130wpm||0).toFixed(1);
 const lengthStatus=r['15_to_30_minute_target']?'Skript erreicht rechnerisch 15–30 Minuten':'Skript noch kürzer als das 15-Minuten-Ziel';
 return `<details class="studio-review"><summary>Fachprüfung offen · Sprechertext ca. ${duration} Min. · Quellenstatus anzeigen</summary>
 <div class="studio-review-content"><p><strong>Prüfstatus:</strong> ${esc(r.technical_review_status)}</p>
 <p><strong>Länge:</strong> ${esc(lengthStatus)}. Berechnungsannahme: 130 Wörter/Minute, keine gemessene MP3-Dauer.</p>
 <p><strong>Zuordnung aus dem Arbeitsplan:</strong></p><ul>${sources}</ul>
 <p><strong>Noch abzuklären:</strong></p>${gaps?`<ul>${gaps}</ul>`:'<p>Keine explizite Dateilücke erkannt. Die fachliche Einzelprüfung ist trotzdem offen.</p>'}
 <p class="studio-review-caution">Die Grafik dient dem Verständnis. Sie ist weder ein normgeprüfter Schaltplan noch eine Installationsfreigabe.</p>
 </div></details>`;
}
''' +s[end:]
old='`<section class="studio-root" data-studio="${esc(id)}" aria-label="Multimedialer Unterricht"><div class="studio-top">'
new='`<section class="studio-root" data-studio="${esc(id)}" aria-label="Multimedialer Unterricht">${reviewPanel(l,norm)}<div class="studio-top">'
if old not in s: raise SystemExit('studio root fragment not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf8')
# styles
p=R/'studio.css';s=p.read_text(encoding='utf8')
s+='''\n/* v0.9.2: individual illustrations and visibly pending expert review */
.studio-individual-figure{width:100%;max-width:700px}.studio-individual-figure img{display:block;width:100%;height:auto;aspect-ratio:1200/610;border-radius:12px;border:1px solid #dae8ed;background:#edf4f6}.studio-review{margin:0 0 15px;border:1px solid #e7d3af;background:#fbf7ed;border-radius:12px;padding:11px 15px;color:#704e22;font-size:13px}.studio-review summary{font-weight:750;cursor:pointer;line-height:1.5}.studio-review-content{margin-top:11px;line-height:1.6}.studio-review-content p{margin:7px 0}.studio-review-content ul{margin:5px 0 9px;padding-left:20px}.studio-review-caution{font-weight:700;color:#8b4c1b}.studio-figure figcaption{line-height:1.5}
@media(min-width:721px){.studio-individual-figure{min-width:0}.studio-concept-grid{grid-template-columns:minmax(270px,1.25fr) minmax(250px,1fr)}}
'''
p.write_text(s,encoding='utf8')
# HTML
p=R/'index.html';s=p.read_text(encoding='utf8')
s=s.replace('Elektroinstallateur EFZ v0.9.1:','Elektroinstallateur EFZ v0.9.2:')
s=s.replace('<script src="./studio.js"></script>','<script src="./lesson-audit.js"></script>\n <script src="./studio.js"></script>')
s=s.replace('Lernwerkstatt v0.9<','Lernwerkstatt v0.9.2<')
p.write_text(s,encoding='utf8')
# site build
p=R/'tools/build_site.py';s=p.read_text(encoding='utf8')
s=s.replace("'lecture-scripts.js','app.js'","'lecture-scripts.js','lesson-audit.js','app.js'")
s=s.replace('  shutil.copy2(f,site/name)\n',"  shutil.copy2(f,site/name)\n visual_dir=site/'visuals';visual_dir.mkdir(exist_ok=True)\n for art in sorted((ROOT/'visuals').glob('*.svg')): shutil.copy2(art,visual_dir/art.name)\n if len(list(visual_dir.glob('*.svg')))!=178: raise SystemExit('Nicht alle 178 SVG-Grafiken vorhanden')\n")
s=s.replace("'version':'0.9.1'","'version':'0.9.2'")
p.write_text(s,encoding='utf8')
# service worker
p=R/'sw.js';s=p.read_text(encoding='utf8')
s=s.replace('elektro-efz-shell-v091-multimedia-1','elektro-efz-shell-v092-quality-1')
s=s.replace("'./lecture-scripts.js','./app.js'","'./lecture-scripts.js','./lesson-audit.js','./app.js'")
needle="'./icon-512.png'];"
if needle not in s:raise SystemExit('sw core list end missing')
s=s.replace(needle,"'./icon-512.png',\n"+'\n'.join('  '+repr(x)+',' for x in assets[:-1])+"\n  "+repr(assets[-1])+'];')
s=s.replace("version:'0.9.1'","version:'0.9.2'")
p.write_text(s,encoding='utf8')
# offline progressive cache download
p=R/'offline.js';s=p.read_text(encoding='utf8')
s=s.replace('elektro-efz-shell-v091-multimedia-1','elektro-efz-shell-v092-quality-1')
s=s.replace("'./lecture-scripts.js','./app.js'","'./lecture-scripts.js','./lesson-audit.js','./app.js'")
needle="'./icon-512.png'];"
if needle not in s:raise SystemExit('offline FILES list end missing')
s=s.replace(needle,"'./icon-512.png',\n"+'\n'.join('  '+repr(x)+',' for x in assets[:-1])+"\n  "+repr(assets[-1])+'];')
p.write_text(s,encoding='utf8')
# Currently the audio refresh button verifies an exact old version; make it accept later complete 178-track manifests.
p=R/'app.js';s=p.read_text(encoding='utf8')
s=s.replace("info.version!=='0.9.1'","!['0.9.1','0.9.2'].includes(info.version)")
s=s.replace('Die neue Vertonung v0.9.1 ist noch nicht vollständig veröffentlicht.','Die Vertonung ist noch nicht vollständig veröffentlicht.')
p.write_text(s,encoding='utf8')
print('Integrated 178 individual visual assets, learner audit panel, offline and site packaging')
