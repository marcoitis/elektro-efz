# Elektro EFZ – v0.9.1 Multimedialer Unterricht

Stand: 16. November 2026

## Inhalt und tatsächlicher Ausbaustand

- **178 Unterrichtslektionen**: 145 reguläre und 33 Normenlektionen, IDs unverändert.
- **1'925 HTML-Folien**: regulär je 11, Normen je 10; Lernziele, Fachtexte, technische Lernbilder, Schrittfolgen, Praxisfall, 3 Quizfragen mit Begründung und Abschluss.
- **178 erweiterte Sprecher-Manuskripte**: rund **96'000 Wörter insgesamt** bzw. durchschnittlich 539 Wörter pro Lektion. Sie sind innerhalb der App als Text aufklappbar und werden neu als Ausgangsmaterial für die kostenlose GitHub-TTS-Generierung verwendet.
- **35 Modulbeispiele** mit Zahlen-/Logikaufgaben; bei übrigen Modulen wird ein nicht-numerischer fachlicher Entscheidungsweg eingesetzt. Nicht jede der 178 Lektionen enthält eine eigene numerische Aufgabe.
- **Technische Lernbilder** sind SVG-Darstellungen mit neun Grundmustern je nach Themenfeld. Sie sind **keine ausführbaren Schaltpläne** oder vollständigen technischen Konstruktionszeichnungen. Ergänzt um schrittweise eingeblendete Rechenwege und eine einfache visualisierte Stromkreis-Animation.
- **Quizantworten** aus den Folien fliessen in das bestehende Quizsystem. Die bisherigen IDs, Notizen, Fortschritte, Backups und lokal gespeicherten MP3s werden nicht bewusst zurückgesetzt.
- **Audio**: Neu eingefügte Erklärtexte sind noch nicht in den bisherigen lokal heruntergeladenen MP3s. Der neue GitHub-Build vertont die geänderten 178 Skripte mit Piper/Thorsten. Erst nach erfolgreichem Build kann man im Offline-Zentrum per ausdrücklich bestätigtem Button die alten MP3s durch die längeren Versionen ersetzen.

### Was ausdrücklich noch offen ist

- Kein professionell/redaktionell von Elektrofachpersonen **fachlich einzeln geprüftes 178-Lektionen-Kompendium**.
- Die durchschnittliche Sprechlänge entspricht bei ca. 539 Wörtern eher 4–6 Minuten, **nicht 15–30 Minuten pro Lektion**.
- Für alle 178 Lektionen gibt es einen Foliensatz; die **Diagramme sind didaktische Grundgrafiken**, keine 178 eigens von Hand konstruierten Maschinen- oder Installationspläne.
- Die Folien-Audioausgabe durch die Gerätestimme ist **nicht zeitlich mit MP3s synchronisiert**.
- Die NIN 2025 wurde nicht hochgeladen und ist nicht im Detail normengeprüft. Bei unvollständigen Norm-PDFs keine technische Detailaussage daraus ableiten.
- Die App bietet theoretische Übung, **keine praktische Bewilligung und keine Bestätigung vollständiger EFZ-Handlungskompetenz**.

## Update auf GitHub nur mit Browser – sicherer Weg über einen Branch

**Vorher:** Bestehende App öffnen → Einstellungen → *JSON exportieren*. Sicherung unabhängig vom Browser speichern. Bestehende Offline-Audios bleiben in diesem Browser erhalten, aber die Sicherungsdatei enthält **keine MP3s**.

1. Repository öffnen: https://github.com/marcoitis/elektro-efz
2. Über die Branch-Auswahl `main` eine neue Branch `multimedia-v091` von `main` erstellen. Damit löst der zwischenzeitliche Upload **keinen langen Audio-Build** auf `main` aus.
3. **Web_Root.zip** entpacken. Alle Dateien im ZIP gehören in das Hauptverzeichnis des Repositories. In diesem Branch: `Add file` → `Upload files` → Dateien aus dem entpackten ZIP auswählen → committen. Nicht die ZIP selbst hochladen.
4. **TTS_Teil_A.zip** und **TTS_Teil_B.zip** entpacken. Im Repository den Ordner **`tts_scripts`** öffnen. Die enthaltenen `.txt`-Dateien in zwei Uploads hochladen und committen. Vorhandene Dateien werden unter dem gleichen Namen aktualisiert. Auf die vollständigen 178 Dateien achten.
5. **Tools.zip** entpacken. Den Repository-Ordner **`tools`** öffnen und die Skripte hochladen.
6. Datei **`.github/workflows/publish.yml`** auf dem Branch öffnen und ihren **gesamten Inhalt** mit `Elektro_EFZ_v0.9.1_Workflow.txt` ersetzen, Änderungen committen.
7. In `Pull requests` einen neuen PR von `multimedia-v091` nach `main` öffnen und **erst nach vollständigem Upload mergen**. Dadurch entsteht ein einzelner GitHub-Actions-Lauf für die neu zu vertonenden 178 Lektionen.
8. Unter https://github.com/marcoitis/elektro-efz/actions den neuen Lauf prüfen. Grüne Markierung bedeutet erfolgreich. Die Veröffentlichung kann aufgrund der deutlich längeren neuen Skripte länger dauern als bei v0.8. Ob ein bestimmter Lauf innerhalb der GitHub-Limits fertig wird, lässt sich nicht vorab garantieren.
9. Website https://marcoitis.github.io/elektro-efz/ öffnen, die verfügbare App-Aktualisierung bestätigen, ein Modul und die Registerkarte **Interaktive Folien** öffnen und Manuskript/Rechenweg/Quiz prüfen.
10. Nach erfolgreicher MP3-Veröffentlichung: **Offline & Audio** → **Gespeicherte MP3s durch neue Fassung ersetzen**. Gute WLAN-Verbindung und ausreichend iPhone-Speicher benutzen. Vorher kann die App weiterhin die älteren offline gespeicherten MP3-Fassungen abspielen.
11. Für Offline-Test auf dem iPhone: WLAN und mobile Daten abschalten; App öffnen; verschiedene Folien und Notizen prüfen. Danach Netz wieder aktivieren.

### Alternativ: Ohne neuen Branch

Wenn Du direkt auf `main` hochlädst, startet bei **jedem Commit**, der unter die Workflow-Trigger fällt, ein neuer Audio-/Pages-Lauf. Das ist vermeidbar und kann zu mehreren langen Läufen führen. Der Branch-Weg ist deshalb empfehlenswert.

## Prüfergebnisse dieses Pakets

- `python tools/quality_check.py`: **0 Fehler**.
- `python tools/quality_check_multimedia.py`: **0 Fehler**; alle 178 Lektionen besitzen vollständige Foliensätze; **1'925 Folien** geprüft.
- `node --check`: JavaScript-Dateien syntaktisch geprüft.
- Browser-Funktionstests in Chromium mit 390 px und 1360 px: Navigation, Folienwechsel, Rechenweg, Lösung ein-/ausblenden, Quiz und Normenlektions-Folien **ohne gemeldete JS-Fehler**.
- Testpaket (`tools/build_site.py --mode probe`) erstellt, alle neuen Appdateien enthalten; drei vorhandene alte Test-MP3s genutzt. Das ist **kein Nachweis**, dass die neue Thorsten-Vertonung bereits fertig ist.
- Ein vollständiger live GitHub-Deployment- und iPhone-Offline-Test wurde von hier **nicht durchgeführt**.

## Quellen und Sicherheit

Lehrplan-Grundlage in diesem Projekt: BiVo 2015 (bisheriger Bildungsplan). Seit Lehrbeginn 2026 gilt ein neuer Bildungsplan. Ob Dein geplanter Abschluss über Art. 32 BBV unter die alten oder neuen QV-Vorgaben fällt, muss die zuständige kantonale Behörde bestätigen.

Aktuelle Links: EIT.swiss https://www.eit.swiss/de/bildung/grundbildung/elektroinstallateurin-efz ; NIV https://www.fedlex.admin.ch/eli/cc/2002/22/de

Normtexte werden nicht in den GitHub-Paketen verbreitet. Die in der Anwendung enthaltenen Referenzen dienen Lernzwecken und sind zum Teil noch fachlich gegenzuprüfen. Keine Übungen an realen 230/400-V-Installationen, spannungsführenden PV-Strings oder Verteilungen ohne erforderliche Berechtigung und Fachaufsicht.
