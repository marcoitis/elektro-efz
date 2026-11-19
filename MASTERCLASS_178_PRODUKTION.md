# 178 Masterclasses – sequenzielle Produktion und Qualitätsstandard

## Ziel
Aus allen **178 bestehenden Elektro-EFZ-Lektionen** nacheinander eigenständige audiovisuelle Unterrichtsfilme im Stil der vom Nutzer gutgeheissenen Master-Sequenz `1.03-B` (v0.14.0) herstellen. Keine automatische Umwandlung der alten 178 Audiolektionen in generische Folienvideos.

## Massgebende Quellen
- Reihenfolge: `audio-plan/batches.json` (15 Batches; 178 eindeutige IDs).
- Status: `masterclasses/catalog.json` (genau 178 IDs).
- Der Inhalt je Lektion: `data.js`, `tts_scripts/<ID>.txt`, falls vorhanden Normen-/Kursdaten.
- Rechtliche und sicherheitsrelevante Sachverhalte zusätzlich anhand von ESTI, BFE und geltender NIV prüfen und Normenfreigabe nicht fingieren.
- Referenzfilm: `master-103-b.html`; wiederverwendbarer neuer Player: `masterclass.html?lesson=<ID>`.

## Reihenfolge pro Lektion – immer nur eine
1. Nächsten Eintrag mit `status: "pending"` auswählen. Ist ein Eintrag noch `in_production`, ihn zuerst vollständig prüfen oder gezielt reparieren, statt die Produktion zu überholen.
2. Quellen der **konkreten Lektion vollständig lesen**. 18–30 kurze, aufeinander aufbauende Sprecherbausteine mit fachlicher Logik, anschaulichem Beispiel und Abschlussfrage samt erst danach gesprochenen Antwort verfassen. Zielgrösse ungefähr 2–4 Minuten je Master-Sequenz. Spezialthemen können mehr benötigen.
3. Als `masterclasses/<ID>/script.json` speichern, Felder `id: "<ID>-master"`, `lesson_id`, `title`, `source`, `source_urls`, `beats` mit `id, visual, text`.
4. **Einzigartige Visualisierung** in `masterclasses/<ID>/visuals.js` erstellen, die `window.EFZ_MasterRenderers[ID]={groups,render}` registriert. SVG fachlich kontrollieren: Schaltpläne müssen elektrisch korrekt verbunden sein, Polarität und Stromrichtung sauber bezeichnen, Wechselstrom nur mit passender gesprochener Erklärung animieren. Bei rechtlichen Themen keine unsachgemässen Schaltungen und kein irreführendes Ausnahmerecht darstellen.
5. Skript einzeln mit Piper `de_DE-thorsten-high` (festgelegter Modellhash) und `tools/render_masterclass_sequential.py --lesson <ID>` vertonen. Jede Szene separat als PCM-WAV, Audiodaten zu einer durchgehenden MP3 zusammenführen und Timecodes aus der tatsächlichen Anzahl Samples erzeugen; **keine Wortzahlschätzung als Synchronisation**.
6. Mit `python tools/check_sequential_master.py --lesson <ID>`, Repository-Preflight, `node --check`, Build und Browsern WebKit/Safari und Chromium auf 390px und Desktop prüfen. Dazu Szenen wie Inhaltsgrafiken, Animationen, Pausieren, Kapitelsprünge und vor der Antwort stoppende Lernkontrolle. TTS-Akustik-/Fachabnahme bleibt bis zur persönlichen Prüfung als offen gekennzeichnet.
7. Version und Catalog aktualisieren. Nur wenn **alle technischen Prüfungen erfolgreich** und GitHub Pages veröffentlicht sind, Eintrag auf `ready` setzen und `href: ./masterclass.html?lesson=<ID>` vergeben. Niemals allein wegen existierender MP3 auf `ready` setzen.
8. Link und Anzahl fertiger Lektionen zurückmelden. Danach bei der nächsten planmässigen Arbeit die **nächste** Lektion bearbeiten.

## Nicht akzeptabel
- Dasselbe generische Schaltbild für nicht zusammengehörige Fachthemen wiederverwenden.
- Die 17-Minuten-Piper-Audiolektionen mit geschätzten Timings als angeblich exakte Videosequenz verkaufen.
- Beliebige hintereinander eingeblendete Textlisten anstelle erklärender Visualisierung.
- Fehlende Quellen, erdachte Messwerte, ungesicherte Arbeitsanweisungen, behauptete Normenfreigaben.
- Als fertig ausweisen, bevor der Masterclass-Player im realen Browser funktioniert.

## Releasestatus
`ready` bedeutet veröffentlichte, technisch geprüfte audiovisuelle Master-Sequenz, **nicht** automatisch unabhängige normative Begutachtung oder menschliche Sprach-/Unterrichtsabnahme.

Die bestehenden vollständigen 178 Audio-/Textlektionen sowie alle Lernfortschritte bleiben unverändert.

## Speicherkonzept
Die alte Sprachbibliothek (~2,9 GB) bleibt extern. Neue kurze Masterclasses werden zunächst einzeln als GitHub-Pages-MP3 abgelegt; bei wachsendem Volumen frühzeitig Speicherkonzept prüfen (Releases oder geeignete CORS-kompatible Objektspeicherung). Die komplette Filmbibliothek darf nicht ungefragt auf dem iPhone zwischengespeichert werden.
