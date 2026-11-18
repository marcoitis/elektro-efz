# Update auf Elektro EFZ v0.9.7 – nur über die GitHub-Weboberfläche

## Vor der Aktualisierung

1. Bestehende Lernplattform öffnen und den **Lernstand als JSON-Datei exportieren**. Auch die Notizen in «Unterrichtsmappen» über deren eigenen Export sichern.
2. Die bisher funktionierenden Offline-MP3s nicht voreilig löschen. Diese werden erst nach erfolgreichem Neu-Deploy bewusst ersetzt.
3. Auf https://github.com/marcoitis/elektro-efz unter **Code** einen neuen Branch `test-v097` aus `main` erstellen. Die bisherige Website bleibt damit unverändert, bis die Dateien getestet wurden.

## Welche Datei hochladen?

- Wenn auf GitHub **v0.9.6** vollständig installiert ist: `Elektro_EFZ_v0.9.7_Patch_ab_v0.9.6.zip` entpacken und **alle darin enthaltenen Dateien unter ihren angegebenen Pfaden** hochladen. Die ZIP-Datei selbst nicht als Ersatz für Dateien committen.
- Wenn auf GitHub noch v0.8 oder eine andere Version läuft: `Elektro_EFZ_v0.9.7_Vollstaendiger_Quellcode.zip` entpacken und den vorhandenen Repository-Inhalt auf einem Testbranch mit den enthaltenen Dateien konsistent aktualisieren. **Nicht** den v0.9.6-Patch auf v0.8 anwenden.
- GitHub-Weboberfläche: `Add file` → `Upload files`. Wichtig: Unterordner wie `tools/`, `tts_scripts/`, `visuals/`, `learning-visuals/`, `editorial_v097/` und `.github/workflows/` müssen korrekt erhalten bleiben. Bereits vorhandene Dateien müssen überschrieben werden. GitHub bietet eine ZIP-Datei nicht automatisch als Repository-Ordner an.

## Test und Veröffentlichung

1. Im Testbranch prüfen: `tts_scripts/1.08-B.txt`, `visuals/1.08-B.svg` und `tools/verify_montage_measurement_v097.py` vorhanden.
2. Neu hinzugefügte Build-Dateien prüfen, besonders `.github/workflows/publish.yml`.
3. Testbranch via Pull Request in `main` übernehmen, **nachdem alle Dateien hochgeladen sind**. Der Workflow startet dann automatisch und generiert nur die geänderten Audios neu, wenn der Cache erfolgreich wiederhergestellt wird.
4. Unter https://github.com/marcoitis/elektro-efz/actions den vollständigen grünen Abschluss prüfen. Ein grünes Pages-Build allein beweist noch nicht, dass die neue Multimedia-Audio-Version aktuell ist.
5. Lernplattform im Browser neu öffnen, `v0.9.7` prüfen und die Lektionen 1.07-A bis 1.08-C testen.
6. Im Bereich **Offline & Audio** das App-Paket neu laden und erst danach «Gespeicherte MP3s durch neue Fassung ersetzen» bestätigen. Anschliessend Flugmodus-Test durchführen.

### Fehlerfall

- Alter Lernstand bleibt durch dieselben Lektionen-IDs und Speicherschlüssel grundsätzlich kompatibel; Sicherheitskopien müssen dennoch separat vorhanden sein.
- Wenn der Workflow scheitert, Branch, Commit und Fehlermeldung prüfen; `main` nicht auf Verdacht zurücksetzen.
- Fachlich noch nicht final: Die nicht vollständig vorhandenen Normen und 151 individuellen Langlektionen bleiben als offen dokumentiert.
