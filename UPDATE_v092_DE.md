# GitHub-Update Elektro EFZ v0.9.2 – nur über die Webseite

**Version 0.9.2 ist ein Qualitäts-Teilupdate, keine endgültig vollständig normengeprüfte Ausbildung.**

## Vor dem Update

1. Öffne Deine bestehende Lernplattform und exportiere unter Einstellungen eine JSON-Sicherung des Lernstands. Bewahre sie ausserhalb des Browsers auf.
2. Die Offline-MP3s sind **nicht** in der JSON-Sicherungsdatei enthalten. Belasse deshalb vorläufig die bestehende App und ihren lokalen Speicher unverändert.
3. Öffne https://github.com/marcoitis/elektro-efz und erstelle von `main` einen Branch `qualitaet-v092`. Alle folgenden Uploads erfolgen **auf diesem Branch**. So startet nicht mit jedem Teil-Upload ein neuer langer MP3-Workflow.

## Upload in sechs Etappen

1. **App-Root:** ZIP `Elektro_EFZ_v0.9.2_Web_Root.zip` lokal entpacken. Die enthaltenen Dateien in das Hauptverzeichnis des Repositories hochladen. Nicht die ZIP-Datei selbst hochladen. In diesem Paket sind `lesson-long-slides.js`, `lesson-audit.js`, `quality-review.json` und `lesson-visuals.json` enthalten.
2. **Grafiken:** Den Ordner `visuals` im Repository anlegen (falls nötig zuerst eine Datei `visuals/.gitkeep` über `Add file -> Create new file` erzeugen). Die beiden ZIP-Pakete `Elektro_EFZ_v0.9.2_Visuals_A.zip` und `Elektro_EFZ_v0.9.2_Visuals_B.zip` lokal entpacken. Die SVGs aus jedem Paket innerhalb des GitHub-Ordners `visuals` hochladen. So bleibt jeder Upload mit 89 Dateien unter dem Weblimit von 100 Dateien. Abschliessend müssen im Ordner `visuals` **178 SVG-Dateien** liegen.
3. **Sprechertexte:** Beide ZIP-Dateien `Elektro_EFZ_v0.9.2_TTS_A.zip` und `_TTS_B.zip` entpacken. In den bestehenden GitHub-Ordner `tts_scripts` gehen und je Paket 89 `.txt` hochladen. Alle 178 Dateinamen müssen unverändert bleiben. Drei lange Manuskripte sind speziell erweitert; die übrigen 175 noch nicht auf 15–30 Minuten umgearbeitet.
4. **Werkzeuge:** `Elektro_EFZ_v0.9.2_Tools.zip` entpacken und die Python-Dateien in den GitHub-Ordner `tools` hochladen.
5. **Workflow:** `.github/workflows/publish.yml` auf `qualitaet-v092` öffnen. Den Inhalt durch die Datei `Elektro_EFZ_v0.9.2_Workflow.txt` ersetzen. Committen.
6. **Integrieren:** Auf GitHub Pull Request von `qualitaet-v092` nach `main` eröffnen. Erst nach Kontrolle aller Uploads mergen. Auf `main` startet ein GitHub-Actions-Lauf, der das Projekt validiert, die benötigten MP3s erzeugt und GitHub Pages veröffentlicht.

## Nach Veröffentlichung

- Status prüfen: https://github.com/marcoitis/elektro-efz/actions – nur ein **grüner** Job bestätigt die erfolgreiche Veröffentlichung.
- Lernplattform auf dem iPhone öffnen: https://marcoitis.github.io/elektro-efz/
- Eine multimodale Lektion öffnen: etwa Modul 1.03, Lektion B. Dort im Tab `Interaktive Folien` sollten die individuelle Zeichnung und der noch offene Quellenstatus erscheinen. Bei Lektion 1.03-B sollte der neue Manuskripttext rund 2'419 Wörter haben.
- Nach bestätigter Veröffentlichung und erfolgreicher Audioerzeugung `Offline & Audio` -> `Gespeicherte MP3s durch neue Fassung ersetzen` verwenden. Vorher sichern, WLAN nutzen, genügend Speicher einplanen. Bereits vorhandene MP3s werden nicht von der JSON-Datei gesichert.
- Mobile Daten und WLAN für einen Offline-Test ausschalten; Lernbilder, Folien, Lernstand und gespeicherte MP3s prüfen.

## Tatsächlicher Prüfstand vor Upload

- 178 vollständige SVG-Dateien; XML und eindeutige Kennungen getestet.
- 178 Quellenpanels in den Studio-Lektionen gerendert; alle ohne Normfreigabe.
- 178 Einzel-Lektionen und 1'966 Folien strukturell geprüft.
- JavaScript-Syntax und Paketbau im Probelauf geprüft.
- Browsernavigation in dieser aktuellen Laufzeit **nicht** erfolgreich getestet: Die grafische Testumgebung blockierte die lokale Seitennavigation. Ein GitHub-Deployment wurde nicht ausgeführt. MP3s der drei langen Manuskripte wurden noch nicht hier neu erzeugt.

## Wichtige Quellen-/Rechtsgrenzen

Die Plattform beruht weiterhin auf dem Bildungsplan 2015, während seit 2026 eine neue BiVo gilt. Art.-32-BBV-Zuordnung muss der Kanton bestätigen. Die NIN 2025 inklusive Korrekturen ist nicht vollständig vorhanden. Keine Grafiken als Ausführungsplanung verwenden. Elektrische Arbeiten an 230/400 V, Verteilungen oder PV-DC-Kreisen nur mit notwendiger Berechtigung und Fachaufsicht.
