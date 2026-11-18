# Update Elektro EFZ von v0.9.5 auf v0.9.6 – GitHub-Webseite

**Vorher unbedingt sichern:** In der bestehenden Lern-App die Funktion zur JSON-Sicherung des Lernfortschritts verwenden. Bei Unterrichtsmappen die separat angebotene Notizsicherung ebenfalls exportieren. Die Dateien lokal aufbewahren.

## Empfehlung: Test-Branch verwenden

1. Öffne https://github.com/marcoitis/elektro-efz und wechsle ins Repository.
2. Erstelle auf Basis von `main` einen neuen Branch `fachausbau-v096`.
3. Lade das Paket `Elektro_EFZ_v0.9.6_Patch_ab_v0.9.5.zip` herunter und entpacke es auf Deinem PC. **Die ZIP-Datei selbst nicht als Datei ins Repository hochladen.**
4. Ersetze die Dateien unter ihren ursprünglichen Pfaden: im Repository-Hauptordner die Webdateien, in `tts_scripts/` die sechs neuen Sprechertexte, in `editorial_v096/` die sechs redigierten Quellen, in `visuals/` und `learning-visuals/` die jeweiligen Grafiken, in `tools/` die aktualisierten Build- und Prüfdateien sowie `.github/workflows/publish.yml`.
5. GitHub-Weboberfläche: Öffne jeweils das betreffende Verzeichnis, wähle **Add file → Upload files**, lade die dort hingehörenden Dateien hoch und bestätige mit **Commit changes**. Du kannst Ordner vorher in GitHub anlegen. Behalte die Verzeichnisstruktur bei.
6. Vergleiche die Dateien mit den gleichnamigen Pfaden in der entpackten ZIP und prüfe, dass alle Hochladungen erfolgreich sind. Führe den Branch erst nach dieser Prüfung mit `main` zusammen.
7. Der Workflow startet bei einem Push auf `main` automatisch. Prüfe den Lauf unter https://github.com/marcoitis/elektro-efz/actions.
8. Der Job erstellt nur geänderte oder fehlende MP3s erneut, sofern der GitHub-Audiocache wiedergefunden wird. **Die neue Thorsten-Vertonung ist nicht in diesem ZIP enthalten.** Erst nach grünem Workflow-Status steht sie auf GitHub Pages bereit.
9. Installierte iPhone-App online öffnen, die angebotene neue Offline-Version installieren und die betroffenen sechs MP3-Lektionen gegebenenfalls in **Offline & Audio** mit der Funktion zum Ersetzen veralteter Aufnahmen neu herunterladen. Danach erneut im Flugmodus testen.

## Falls GitHub noch v0.8 oder eine ältere Version enthält

Das Patch-Paket reicht **nicht**. Verwende stattdessen das vollständige Quellcodearchiv und übertrage die Dateien in ihren ursprünglichen Ordnern. Wenn Du unsicher bist, lieber nicht bestehende Ordner löschen, sondern die aktualisierten Dateien gezielt ersetzen.

## Technische Grenzen

Die 178 Lektionenkennungen und das bisherige Speicherformat wurden nicht absichtlich geändert. Trotzdem ist die JSON-Sicherung vor dem Update wichtig. Keine live veröffentlichte Version oder echte MP3-Datei wurde während der lokalen Tests verändert.

NIN-Fachfreigaben und die amtliche Zulassungsfrage nach Art. 32 BBV bleiben offen. Die neuen Zeichnungen sind Lernillustrationen, keine ausführbaren Installationspläne.
