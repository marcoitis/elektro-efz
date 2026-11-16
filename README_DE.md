# Elektro-EFZ Lernplattform 0.8 – Normen-Akademie

## Neu in dieser Version

- 33 vertiefte Normenlektionen mit zusammen 99 neuen Kontrollfragen, 33 Fallstudien, Musterlösungen und selbst formulierten Rechen-/Denkbeispielen.
- In die bestehenden 48 Module passend verlinkt. 145 Basislektionen bleiben unverändert.
- Automatische Fortschrittsspeicherung für Normenlektionen und Notizen, Version 0.3–0.7-Backups bleiben kompatibel.
- Offline-Textpaket berücksichtigt die neue `norm-course.js`.
- Kostenlose Piper-Audios werden jetzt für 178 Lektionen vorbereitet (145 Basis + 33 Normen). Noch nicht erzeugte MP3s sind kein Programmfehler.

## Quellen

Die Unterrichtsinhalte sind eigenständig formuliert anhand der vom Nutzer hochgeladenen Normtexte. Die Originalnormen dürfen NICHT ins öffentliche GitHub-Repository.
Die technische Volltextprüfung war bei SN EN IEC 61439-3, -5, -6, -7 und SN EN IEC 62446-2 nicht möglich, da die bereitgestellten Dateien nur 5–6 Seiten Titel und Einleitung enthalten. Die NIN SN 411000:2025 fehlt.

## Installation / Upgrade

1. In der bisherigen App **Audio & Datensicherung → JSON exportieren**.
2. GitHub-Paket entpacken; alle Dateien samt `.github`, `tools`, `tts_scripts` und der neuen Datei `norm-course.js` nach `marcoitis/elektro-efz` hochladen.
3. GitHub Pages bleibt unter derselben URL; Deployment bei GitHub Actions kontrollieren.
4. PWA Update in der Anwendung bestätigen, im Menü **Normen-Akademie** starten.
5. Unter **Offline & Audio** das Textpaket neu verifizieren. Die Audio-Produktion verwendet den vorhandenen GitHub-Workflow.

**Sicherheit:** Keine Elektroinstallationsberechtigung durch die Inhalte. Reale Prüfungen an Netzspannung/PV-DC sind keine Selbstlernversuche.
# Elektroinstallateur EFZ – Version 0.7.1 (GitHub-Audioautomatik)

**Ziel:** 145 gesprochene Lektionen mit einer **kostenlosen männlichen deutschen Stimme**, automatisch über GitHub Actions erstellt und unter der bestehenden GitHub-Pages-Adresse veröffentlicht. Dazu die bestehenden 48 Module, 435 Quizfragen, 25 Vertiefungsaufgaben, Offline-Lernmodus, Speicherfunktion, Lernkontrollen, Simulator und Normenregister.

Die Sprachstimme ist `Piper de_DE-thorsten-high` (kostenloses offenes Modell, Dataset CC0). Es ist **nicht** die Stimme von ChatGPT und noch nicht auf natürliche Aussprache aller technischen Fachbegriffe geprüft.

## Was Du in GitHub einmalig erledigst

1. **Vorher Lernstand sichern:** Bestehende App öffnen → `Audio & Datensicherung` → JSON-Export. Datei ausserhalb des Browsers ablegen.
2. GitHub Desktop installieren, falls noch nicht vorhanden: https://desktop.github.com/ . Dein Repository `marcoitis/elektro-efz` klonen (File → Clone repository). Alternativ Repository im Web bearbeiten; für über 145 Dateien ist GitHub Desktop einfacher.
3. Dieses ZIP **entpacken**. **Den Inhalt** – nicht den übergeordneten Ordner – ins geklonte Repository kopieren. Die versteckte `.github`-Ordnerstruktur unbedingt mitkopieren. Vorhandene App-Dateien überschreiben. Den Git-Ordner `.git` nicht löschen.
4. In GitHub Desktop Änderungen kontrollieren → Commit, z. B. `v0.7.1: gratis Audio mit GitHub Actions` → Push origin.
5. Auf https://github.com/marcoitis/elektro-efz → **Settings → Pages → Build and deployment → Source: GitHub Actions** umstellen. Nicht mehr `Deploy from a branch`. Die bereits eingerichtete Website-Adresse bleibt gleich.
6. Unter **Actions** den Workflow **Elektro EFZ – kostenlose MP3-Erzeugung und GitHub Pages** öffnen. Wenn der Commit bereits einen Lauf gestartet hat, diesen zuerst prüfen. Sonst: **Run workflow** → Branch `main` → `audio_mode = all` → **Run workflow**.
7. Nach **grünem Workflow** Deine Adresse https://marcoitis.github.io/elektro-efz/ öffnen. Eventuelles Update der App bestätigen. Auf dem iPhone unter `Offline & Audio` → `Gesamten Lernstoff herunterladen` und `Verfügbare Audios herunterladen` tippen.
8. Prüfe, dass **145/145** MP3-Dateien angezeigt werden. App schliessen, Flugmodus einschalten, wieder öffnen und eine Lektion anhören. Der erste Download braucht Internet und ausreichend freien Speicherplatz.

**Bei einem fehlgeschlagenen Workflow:** Unter GitHub `Actions` den roten Lauf anklicken; fehlerhaften Schritt aufklappen. Die zuletzt erfolgreiche Website bleibt die sichere Ausgangslage. Fehlerprotokoll sichern und hier bereitstellen; keine kostenpflichtigen Erweiterungen kaufen.

## Kostenlos, aber mit Grenzen

- GitHub Actions ist für öffentliche Repositorys mit Standard-Runnern derzeit kostenlos. Wenn Du das Repository später privat machst oder GitHub sein Preismodell ändert, können andere Regeln gelten.
- Das Modell `de_DE-thorsten-high` wird beim Build heruntergeladen, die MP3s automatisch erzeugt und als Pages-Artefakt hochgeladen. Du brauchst **keinen eigenen API-Schlüssel**, **kein ElevenLabs**, **keine zusätzliche Windows-Software**.
- Die Audioerzeugung erfolgt auf einem GitHub-Rechner. Die MP3-Dateien sind öffentlich zugänglich; persönliche Lernstände werden **nicht** mitveröffentlicht.
- Nach dem ersten Build enthalten alle Lektionen eine echte MP3-Datei; die Vorlese-Stimme ist nicht identisch mit ChatGPT und klingt je nach Fachbegriff unterschiedlich natürlich.
- Vorproduzierte MP3s können auf dem iPhone offline verfügbar gemacht werden; für die Hintergrundwiedergabe bei gesperrtem Display kann iOS Einschränkungen setzen.
- Bei geänderten Skripten regeneriert der Workflow nur betroffene Dateien, soweit der GitHub-Actions-Cache verfügbar ist. Wenn der Cache verloren geht, erzeugt GitHub die Audios erneut (weiterhin ohne API-Gebühren).
- Die App speichert Lernstand lokal. Vor Versionswechseln Lernstand als JSON sichern. Die Audiodateien sind **nicht** im JSON-Backup enthalten.
- Keine geschützten Normen oder Fachbücher sind im Paket enthalten. Die fachliche Version bleibt vorläufig; insbesondere NIN 2025 und ESTI-Details sind noch nicht vollständig mit Originalquellen validiert.

## Technischer Aufbau

- `.github/workflows/publish.yml`: Kostenloses Erzeugen und automatisches Veröffentlichen auf GitHub Pages bei neuen Änderungen oder manuell.
- `tts_scripts/*.txt`: 145 sprechgerecht normalisierte Texte (unabhängig von den Lektionstexten in der App).
- `tools/generate_audio.py`: Piper-Text-zu-WAV + FFmpeg-WAV-zu-MP3, Prüfsummen, Cache und Fehlerbehandlung.
- `tools/build_site.py`: Baut einen sicheren, vollständigen Veröffentlichungsordner, inklusive Manifest mit nur vorhandenen MP3-Dateien. Der komplette Lauf wird bei weniger als 145 MP3s abgebrochen.
- `audio-manifest.json`: im ZIP ein Platzhalter. Im **veröffentlichten Pages-Artefakt** automatisch mit den 145 tatsächlichen Audio-URLs gefüllt.
- `sw.js` / `offline.js`: App-Core für offline vorhalten und prüfen; 145 MP3s werden separat in IndexedDB gespeichert.

## Alternative: Windows-PC

Falls GitHub Actions wider Erwarten kein Modell herunterladen kann, steht die vorherige kostenlose Windows-Variante zur Verfügung. Sie ist für den eigentlichen GitHub-Audioaufbau nicht erforderlich.

## Quellen und Lizenzen

- Piper CLI: https://github.com/rhasspy/piper
- Piper Thorsten High / Dataset-Lizenz CC0: https://huggingface.co/rhasspy/piper-voices/tree/main/de/de_DE/thorsten/high
- GitHub Pages mit Actions: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- GitHub Actions Preisregeln: https://docs.github.com/en/actions/concepts/billing-and-usage
