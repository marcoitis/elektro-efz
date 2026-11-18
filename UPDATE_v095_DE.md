# Installation von Elektro EFZ v0.9.5 über GitHub im Browser

## Vorab

1. Öffne die aktuell installierte App und exportiere Deinen Lernstand als JSON-Datei. Speichere auch Notizen aus dem Kurskompass separat.
2. Die Versionsnummer auf Deinem GitHub prüfen. Wenn dort **v0.9.4** vollständig installiert ist, genügt das Patchpaket `Elektro_EFZ_v0.9.5_Patch_ab_v0.9.4.zip`. Wenn dort **v0.8**, **v0.9.1**, **v0.9.2** oder **v0.9.3** läuft, nimm das vollständige v0.9.5-Paket.
3. Auf GitHub möglichst einen **neuen Branch `fachlektionen-v095`** erstellen. Alle Dateien auf diesem Branch sammeln. Der Workflow für die MP3-Dateien läuft nach der Zusammenführung in `main` an. So entstehen nicht mehrere unnötig lange Audioläufe.

## Vollständige Variante

1. `Elektro_EFZ_v0.9.5_Vollstaendiger_Quellcode.zip` lokal entpacken. **Nicht die ZIP-Datei selbst hochladen.**
2. GitHub `https://github.com/marcoitis/elektro-efz` öffnen und den vorbereiteten Branch wählen.
3. Den Inhalt des entpackten Projektordners mit gleicher Unterordnerstruktur in das bestehende Repository übertragen: `index.html`, `app.js`, `tts_scripts/`, `editorial_v095/`, `visuals/`, `learning-visuals/`, `tools/`, `.github/workflows/publish.yml` und die übrigen mitgelieferten Dateien. Bestehende Dateinamen dabei ersetzen.
4. Dateien auf `main` zusammenführen und den neuen GitHub-Actions-Lauf abwarten.

## Patch ab vollständig installiertem v0.9.4

1. `Elektro_EFZ_v0.9.5_Patch_ab_v0.9.4.zip` entpacken.
2. Alle im ZIP enthaltenen Dateien an ihrem entsprechenden GitHub-Pfad ersetzen/ergänzen. Dazu gehören sechs `editorial_v095/*.txt` und sechs überarbeitete `tts_scripts/*.txt`, die SVGs, die Qualitätsdateien und neue/angepasste Python-Werkzeuge.
3. `.github/workflows/publish.yml` ersetzen. Der Workflow übernimmt die Neuberechnung der Mappen und Audiofiles. Niemals den Fortschrittsspeicher des iPhones für den Upload löschen.

## GitHub Actions

`https://github.com/marcoitis/elektro-efz/actions` öffnen. Der Workflow braucht die kostenlose Piper-Stimme und erstellt geänderte MP3s; wenn der bisherige Cache vorhanden ist, sollten die anderen unveränderten Aufnahmen weiterverwendet werden. Ein grüner Lauf ist zunächst **nur** der technische Veröffentlichungsnachweis, keine fachliche Normenfreigabe.

## Testen auf dem iPhone

1. App schliessen und erneut öffnen; Versionsangabe v0.9.5 prüfen.
2. `1.09-A`, `1.09-C`, `1.10-A`, `1.10-B` öffnen. Die Manuskripte sollten ausführlich, die neuen SVGs sichtbar und die Folien nutzbar sein.
3. MP3 dieser Lektionen abspielen und bei Bedarf die vorhandenen Offline-MP3s **bestätigt** durch die neue Fassung ersetzen.
4. Flugmodus einschalten, die Inhalte erneut öffnen und auf Offlinefunktion testen.
5. Bisherige Kursstände und Quizresultate kontrollieren. Falls Daten fehlen, mit der vorher exportierten Sicherung wiederherstellen.

## Wichtiger Hinweis

Nur sechs weitere Fachlektionen wurden individuell verlängert; insgesamt 15 von 178 erfüllen den geforderten Umfang. Alle Normenprüfungen durch eine unabhängige qualifizierte Fachperson sind noch ausstehend.
