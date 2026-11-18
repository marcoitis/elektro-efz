# Elektroinstallateur EFZ – Lernplattform v0.11.8

**GitHub-fertige Text-/Offline-Version** mit 178 Lektionen, 534 Quizfragen,
178 SVG-Lernbildern und 178 Sprechmanuskripten. Alle Manuskripte liegen nach
syntaktischer Wortzählung zwischen 1’950 und 3’900 Wörtern. Die fachliche
Einzel- und Normenfreigabe ist noch offen.

## Sofortstart

- Einstieg in die App: `index.html` (veröffentlicht über HTTPS mit GitHub Pages).
- Upload-Anleitung: [GITHUB_UPLOAD_ANLEITUNG.md](GITHUB_UPLOAD_ANLEITUNG.md).
- Sprachproduktion in Etappen: [AUDIO_MEHRSTUFENPLAN.md](AUDIO_MEHRSTUFENPLAN.md).
- Freigabepunkte: [VOR_VERÖFFENTLICHUNG_PRÜFEN.md](VOR_VERÖFFENTLICHUNG_PRÜFEN.md).
- Quellen-/Normenstatus: `FACHQUELLEN_v0118.md` und `NORMEN_QUELLENSTATUS.md`.

**Wichtig:** Der erste GitHub-Pages-Build veröffentlicht **keine MP3-Dateien**.
Die Gerätestimme und der lokale MP3-Import funktionieren unverändert. Die
Audioproduktion erfolgt bewusst separat mit Zwischenabnahmen.

## Lokal testen

```bash
python tools/check_github_release.py
python tools/quality_check.py
python tools/quality_check_multimedia.py
python tools/validate_v0118.py
python tools/build_site.py --mode text
python tools/verify_pages_package.py --site dist
python -m http.server 8000 --directory dist
```

Danach `http://localhost:8000/` aufrufen. Ein lokaler Server ist zuverlässiger
als das direkte Öffnen einer HTML-Datei (`file://`), insbesondere wegen
Service Workern und PWA-Funktionen.

## GitHub Pages

Die `.github/workflows/publish.yml` prüft die Daten und veröffentlicht das
`dist`-Verzeichnis mit `actions/upload-pages-artifact@v3` und
`actions/deploy-pages@v4`. **Keine kosten- oder ressourcenintensive
Audio-Produktion beim Commit.** Publishing Source muss unter
**Settings → Pages → Build and deployment → GitHub Actions** aktiviert werden.

Der Pages-Build vergibt bei jeder Änderung an den App-Dateien automatisch eine
neue gemeinsame Service-Worker-Cachekennung, sodass Aktualisierungen
nicht im alten Offline-Cache steckenbleiben.

Projektseite: `https://BENUTZERNAME.github.io/REPOSITORY/`. Die PWA benutzt
relative Pfade, auch unter einer GitHub-Pages-Projektadresse.

## Audio (freiwillig, nach fachlicher Freigabe)

```bash
python tools/prepare_audio_batches.py --pilot
python tools/prepare_audio_batches.py --batch 1
```

Die erste Ausgabe enthält ein Kontrollblatt und Segmenttexte **ohne MP3s**.
Freigegebene kleine Pilot-MP3s werden später im opt-in-Ordner `public-audio/`
veröffentlicht; grössere Serien gehören auf eine getrennte HTTPS-Audioablage.

## Sicherheit und Rechte

Dies ist ein **Lern- und Übungsprodukt**, keine Installationsanweisung,
Installationsbewilligung, NIN-Konformitätsbestätigung oder amtliche QV-Vorlage.
Prüfungen und elektrische Arbeiten sind ausschliesslich von fachlich befugten
Personen unter Einhaltung der geltenden Vorgaben durchzuführen. Vor einer
öffentlichen Publikation müssen Texte, Referenzen, Zeichnungen und mögliche
Lizenzrechte geprüft werden. Originalnormen, interne Kundendokumente,
Geheimnisse und personenbezogene Daten gehören nicht ins Repository.

Es wird **bewusst keine Open-Source-Lizenz** automatisch erteilt. Über die
Lizenzierung und öffentliche Freigabe der Projektinhalte entscheidet der
Projektinhaber.
