#!/usr/bin/env python3
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,base64,hashlib,csv,shutil
root=Path(__file__).resolve().parent.parent
out=Path('/mnt/data');items=json.loads((root/'lesson-workbooks.json').read_text('utf8'))
assert len(items)==178
# Self-contained file, including all drawings as data URLs. No third-party scripts.
standalone=(root/'kurskompass.html').read_text('utf8')
for x in items:
 path='./learning-visuals/'+x['id']+'.svg'
 svg=(root/'learning-visuals'/(x['id']+'.svg')).read_bytes()
 standalone=standalone.replace(path,'data:image/svg+xml;base64,'+base64.b64encode(svg).decode())
standalone=standalone.replace('<a href="./index.html">← Zur Lernplattform</a>','<span>ELEKTRO EFZ · lokale Offline-Vorschau</span>').replace('<a href="./index.html">Zur App</a>','')
preview=out/'Elektro_EFZ_v0.9.3_178_Unterrichtsmappen_Offline.html';preview.write_text(standalone,'utf8')
# Comprehensive review report, no unsupported claims of normative verification.
counts={'lectures':len(items),'regular':sum(not r['isNorm'] for r in items),'norms':sum(r['isNorm'] for r in items),'source_total_words':sum(x['ttsWords'] for x in items),'t15':sum(x['ttsMinutesAt130wpm']>=15 for x in items),'long_pending':sum(x['ttsMinutesAt130wpm']<15 for x in items),'expert_pending':len(items),'quiz_total':sum(len(x['quiz']) for x in items),'expanded_reasons':sum(q['why']!=q.get('whyExtended') for x in items for q in x['quiz'])}
report=f'''# Fachliche Qualitätsbilanz – Elektro EFZ v0.9.3

Stand: 17. November 2026. Quelle: Originaldateien der Version 0.9.2 sowie die 14 bereitgestellten Norm-PDFs im lokalen, **nicht veröffentlichten** Arbeitsbestand.

## Was neu erstellt wurde

- **{counts['lectures']} Unterrichtsmappen:** {counts['regular']} reguläre Lektionen, {counts['norms']} Normenlektionen. Jede Mappe enthält eigene Lernziele, die vorhandenen Fachabschnitte der entsprechenden Lektion, fallbezogene Aufgaben, drei Prüfungsfragen, Musterbegründungen und die Quellen-/Lückenliste.
- **48 neu verfasste thematische Vertiefungstexte:** jeweils zum Fachthema des Moduls, ergänzt mit einer sicheren Aufgabe; in den 145 regulären Lektionen thematisch zugeordnet.
- **178 individuell mit dem jeweiligen Lektionstext beschriftete SVG-Lernlogikdiagramme** (Konzeptgrafiken, keine 178 fachtechnisch eigens konstruierte Installationsschaltbilder).
- **{counts['expanded_reasons']} von {counts['quiz_total']} Quizbegründungen** mit zusätzlichem, automatisch ausgewähltem Bezug auf den bereits vorhandenen Unterrichtstext; dieser Bezug ist kein extern geprüfter Fachnachweis.
- **178 individuell aus den Lernzielen, Fachabschnitten, Praxisfällen und Prüfungsfragen zusammengestellte 25-Minuten-Lernabläufe** mit sechs abhakbaren Arbeitsphasen. Dies sind Lernzeit-Empfehlungen für aktive Arbeit, **keine** durchgehend 25 Minuten gesprochener Unterricht.
- **Ein durchsuchbarer Unterrichtsmappen-Browser** mit lokalen Notizen, separatem Notizen- und Phasen-Backup, Papier-/PDF-Druck und Offline-Dateikatalog.

## Qualitätslücken (entscheidend)

| Ziel | nachweisbarer Stand | Bewertung |
|---|---:|---|
| 178 eigenständig redigierte Kapitel mit je 15–30 Min gesprochener Lehre | {counts['t15']} von {counts['lectures']} vorhanden | **{counts['long_pending']} fehlen** |
| Individuell konstruierte, fachlich geprüfte Installationsschaltbilder | 0 von 178 formal freigegeben | **Offen**; Lernlogikgrafiken ≠ Fachschaltpläne |
| Normen-/Sicherheitsfachprüfung je Lektion | 0 von 178 unabhängig freigegeben | **Offen** |
| Quellenlage NIN 2025 | Volltext nicht bereitgestellt | **Unvollständig** |
| Audioerzeugung für neue Unterrichtstexte | keine neuen Langmanuskripte in v0.9.3 | die bestehenden MP3s können weiterverwendet werden |

Weder durch die automatische Prüfung noch durch die vorliegenden Norm-PDF-Ausschnitte dürfen die Lehrmappen als normenkonforme Ausführungsanleitung freigegeben werden. Sie sind eine didaktische Arbeitsfassung, **keine** vollständig ausgearbeitete, einzeln redigierte EFZ-Fachausbildung.

## Nachweisbare Tests

- 178 Markdown-Mappen / 178 SVG (XML) / 178 strukturierte Datensätze
- Alle Mappen mit mindestens zwei fachlichen Abschnitten, drei Quizfragen und sechs individuellen Lernphasen mit insgesamt 25 Minuten empfohlener aktiver Lernzeit
- Alle Statusfelder für unabhängige Fachredaktion und Normenabgleich korrekt auf OFFEN
- Javascript-Syntaxprüfung, Strukturprüfungen von v0.9.2 sowie v0.9.3 bestanden
- GitHub-Pages-Probe-Build mit drei **künstlichen** Test-MP3-Dateien bestanden; diese werden **nicht** verteilt
- DOM-Funktionstest in Chromium (HTML-Injektion statt Netz-Zugriff): Suche, Quizauflösung und mobile Grundansicht ohne Javascript-Laufzeitfehler
- Vollständiger Live-Deploy, Service-Worker-Lauf im iPhone und reales Thorsten-TTS hier **nicht** getestet

## Fachliche Einordnung

Die Kursstruktur beruht weiterhin vorwiegend auf dem bisherigen BiVo-2015-Lehrstoff. Eine gesicherte Zuordnung zu den Lernzielen der BiVo 2026 und zum Art.-32-Qualifikationsverfahren steht aus. Die aktuelle NIN 2025 sowie Korrekturen/Amendments müssen anhand rechtmässig verfügbarer, vollständiger Originalausgaben abgeglichen werden.

Die im Arbeitsbestand vorhandenen Norm-PDFs werden aus Lizenzgründen nicht in das öffentliche Repository oder das Downloadpaket übernommen.
'''
(out/'Elektro_EFZ_v0.9.3_Qualitaetsbericht.md').write_text(report,'utf8')
# CSV: per-lesson editorial status, truthful.
with (out/'Elektro_EFZ_v0.9.3_Status_aller_178_Lektionen.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,delimiter=';');w.writerow(['ID','Jahr','Titel','Normenlektion','Sprechertext_Woerter','Sprechdauer_130WpM','Langkapitel_15min','Lernmappe','Lernlogikdiagramm','Inhaltliche_Einzelredaktion','Normenfachpruefung'])
 for x in items:w.writerow([x['id'],x['year'],x['title'],'Ja' if x['isNorm'] else 'Nein',x['ttsWords'],x['ttsMinutesAt130wpm'],'Ja' if x['ttsMinutesAt130wpm']>=15 else 'Nein','Erstellt','Erstellt – Konzeptgrafik','Ausstehend','Ausstehend'])

def pack(dest,paths):
 with ZipFile(out/dest,'w',ZIP_DEFLATED,compresslevel=8) as z:
  for p in paths:
   f=root/p
   assert f.is_file(),str(f)
   z.write(f,arcname=str(p))
  bad=z.testzip();assert bad is None,(dest,bad)
 print(dest,len(paths),'files',round((out/dest).stat().st_size/1024),'KB')
# Narrow patch for repositories that already run v0.9.2.
patch=['index.html','studio.js','sw.js','tools/build_site.py','tools/create_178_workbooks.py','tools/build_course_compass.py','tools/validate_v093.py','.github/workflows/publish.yml']
pack('Elektro_EFZ_v0.9.3_Patch_ab_v0.9.2.zip',patch)
# Browser upload partitions for users upgrading from an older release.
rootfiles=['index.html','app.js','styles.css','studio.css','manifest.webmanifest','icon-192.png','icon-512.png','sw.js','data.js','storage.js','reviews.js','exercises.js','audio-engine.js','cloud.js','offline.js','trainer.js','simulator.js','norms.js','norm-course.js','academy-content.js','chapters.js','academy.js','studio.js','studio-examples-extra.js','lecture-scripts.js','lesson-audit.js','lesson-long-slides.js','lesson-visuals.json','quality-review.json','norm_course.json','kurskompass.html']
pack('Elektro_EFZ_v0.9.3_Webdateien.zip',rootfiles)
pack('Elektro_EFZ_v0.9.3_Werkzeuge.zip',[Path('tools')/p.name for p in sorted((root/'tools').glob('*.py')) if p.name not in ('package_v093.py','test_compass_browser.py')])
scripts=sorted((root/'tts_scripts').glob('*.txt'))
pack('Elektro_EFZ_v0.9.3_Sprechertexte_A.zip',[x.relative_to(root) for x in scripts[:89]])
pack('Elektro_EFZ_v0.9.3_Sprechertexte_B.zip',[x.relative_to(root) for x in scripts[89:]])
oldvs=sorted((root/'visuals').glob('*.svg'))
pack('Elektro_EFZ_v0.9.3_Lernbilder_A.zip',[x.relative_to(root) for x in oldvs[:89]])
pack('Elektro_EFZ_v0.9.3_Lernbilder_B.zip',[x.relative_to(root) for x in oldvs[89:]])
# Whole reproducible source archive: exclude transient/compiled artifacts and proprietary standards.
allpaths=[p.relative_to(root) for p in root.rglob('*') if p.is_file() and not any(q in ['.audio-cache','dist-probe','.voice-cache','__pycache__','.git'] for q in p.relative_to(root).parts) and p.name not in ['preview_v093_mobile.png','preview_v093_desktop.png']]
pack('Elektro_EFZ_v0.9.3_Vollstaendiger_Quellcode.zip',allpaths)
# Installation text; use branch to avoid destructive upload to main.
instructions='''# Elektro EFZ v0.9.3 – Aktualisierung über GitHub-Webseite

## Vorher
- Bestehende App öffnen und **Lernfortschritt als JSON exportieren**.
- Falls vorhanden: Die bisherige GitHub-Version und den Browser-Cache nicht vorzeitig löschen.
- Repository: https://github.com/marcoitis/elektro-efz
- Nicht alle Quellen und Normen sind für einen öffentlichen Upload lizenziert. Norm-PDFs deshalb **nicht** hochladen.

## A: Wenn v0.9.2 bereits im Repository liegt

1. Auf GitHub einen neuen Branch `kurskompass-v093` von `main` erstellen.
2. `Elektro_EFZ_v0.9.3_Patch_ab_v0.9.2.zip` lokal entpacken.
3. Auf GitHub die sieben Web- und Werkzeugdateien in ihre vorhandenen Ordner übertragen und `.github/workflows/publish.yml` ersetzen.
4. Sicherstellen, dass unter `tools/` die drei neuen Skripte `create_178_workbooks.py`, `build_course_compass.py`, `validate_v093.py` vorhanden sind.
5. Branch in `main` übernehmen. Der Workflow erzeugt `kurskompass.html` sowie 178 neue Lernlogikgrafiken während des Builds automatisch.
6. `Actions` prüfen; auf der Webseite `.../kurskompass.html` öffnen und offline testen.

## B: Wenn v0.9.2 NOCH NICHT installiert ist (z. B. v0.8)

1. Neues GitHub-Branch anlegen und Lernstand sichern (wie oben).
2. Die ZIP-Dateien `Webdateien`, `Werkzeuge`, `Sprechertexte_A/B` und `Lernbilder_A/B` **lokal entpacken**.
3. Die enthaltenen Dateien unter Beibehaltung der Ordnerstruktur `tools/`, `tts_scripts/` und `visuals/` auf GitHub hochladen. ZIP-Dateien nicht als ZIP im Repository belassen – GitHub Pages entpackt sie nicht.
4. `.github/workflows/publish.yml` aus dem **Patch-Paket** übernehmen.
5. Committen, Merge nach `main`; GitHub Actions abwarten und Ergebnisse prüfen.

## Hinweise zu Audio und Offline
- v0.9.3 ersetzt keine 175 Kurzmanuskripte durch 15–30-Minuten-Langfassungen. Die vorhandenen MP3s bleiben gültig, sofern sich die zugrunde liegenden `tts_scripts/*.txt` nicht geändert haben.
- Die neuen Unterrichtsmappen erhalten ein separates JSON-Backup für die dort gespeicherten Notizen. Diese werden noch nicht automatisch vom bisherigen App-Export erfasst.
- Die Lernlogikgrafiken sind Konzepterklärungen, **keine** geprüften Installationspläne.
- Bei einem fehlgeschlagenen GitHub-Action-Lauf nicht die vorhandene Live-Version löschen. Fehlerprotokoll prüfen.

## Schnelltest
- 178 Einträge im Kurskompass, darunter 33 Normenlektionen; sechs abhakbare Lernphasen je Lektion.
- Bei `1.03-B` und `N-S01` wird die entsprechende Grafik angezeigt.
- Quizantwort zeigen; Notiz schreiben und nach erneutem Öffnen wiederfinden.
- Offlinefunktion zuerst mit aktivem Internet öffnen, danach Flugmodus testen.
- Bestand der alten Lektionen, bisherigen Notizen und MP3s kontrollieren.
'''
(out/'Elektro_EFZ_v0.9.3_GitHub_Update_Anleitung.md').write_text(instructions,'utf8')
print('Standalone bytes:',preview.stat().st_size)
print('Counts',counts)
