# QA-Bericht v0.7.1

## Technisch geprüft
- Alle 145 Lektionstexte vorhanden und den 145 eindeutigen App-Lektionenkennungen exakt zugeordnet.
- 145 sprechgerecht vorbereitete TTS-Skripte; doppelte Titelansagen und formale Satzzeichenfehler reduziert.
- JS-Syntaxprüfung erfolgreich für App, Offline-Manager und Service Worker.
- `generate_audio.py` in einem TTS-Ersatzlauf mit drei Testlektionen erfolgreich ausgeführt: WAV, FFmpeg-MP3, Dateinamen und Prüfsummenspeicherung.
- `build_site.py` aus drei MP3-Testdateien erstellt: Manifest mit genau drei gültigen Einträgen; die Anwendung bleibt bis zur vollständigen Produktion bereit.
- Offline-Cache-Version `elektro-efz-shell-v071-1` identisch in SW und Offline-Manager; alte Lektionenkennungen und bestehender Lernspeicher unverändert.
- Öffentliches Repo-Paket enthält GitHub-Actions-Workflow, 145 Quellskripte und Generator.

## Noch extern zu prüfen
- Echte Piper-Voice-Generierung auf GitHub Actions (in dieser Arbeitsumgebung fehlt der Zugang zu Modellgewichten und es können keine externen kostenlosen Voice-Modelle geladen werden).
- Vollständiger GitHub-Run und Pages-Deployment, da kein Schreibzugriff auf das Repository vorliegt.
- Aussprachequalität der generierten MP3s, insbesondere Abkürzungen, Zahlen, Normen, Elektrotechnikformeln.
- iPhone-TTS-/MP3-Hintergrundwiedergabe, gesamte MP3-Sammlung offline und Kontrolle nach App-Neustart.
- Ein End-to-End-Browsertest der PWA war in dieser Laufzeitumgebung administrativ blockiert.

**Keine Behauptung, dass bereits 145 echte MP3s erzeugt oder auf der Website veröffentlicht wurden.**
