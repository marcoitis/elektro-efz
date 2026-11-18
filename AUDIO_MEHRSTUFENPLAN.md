# Sprachdateien: kontrollierte Herstellung in mehreren Schlaufen

**Stand:** 18.11.2026 · Manuskriptbasis v0.11.8

## Ausgangslage

- 178 Textskripte in `tts_scripts/<LEKTIONS-ID>.txt`.
- Total **372’563 Wörter**. Bei 130 Wörtern pro Minute rund **47,8 Stunden** reine Sprache.
- Grobe Dateigrösse, ohne ID3-Overhead: **64 kbit/s Mono ≈ 1,38 GB**;
  **48 kbit/s Mono ≈ 1,03 GB**. Die effektive Ausgabe kann abweichen.
- In v0.11.8 sind **0 fertige MP3s enthalten**. Die `audio-manifest.json`
  bleibt deshalb initial leer.
- Bereits vorhandene TTS-Python-Datei: `tools/generate_audio.py` (optional
  Piper + FFmpeg). Keine automatische Generierung in GitHub Actions.

## Schlaufe 1 – Text- und Aussprachebasis

Die Sprechertexte wurden auf **Umfang**, nicht durchgehend auf
Sprechbarkeit/Fachrichtigkeit geprüft. Zuerst werden Abkürzungen, Einheiten,
Formeln, mathematische Vorzeichen, Trennstriche und längere Sätze überprüft.

1. `audio-plan/batches.csv` enthält alle 178 Lektions-IDs, Wortzahlen und
   SHA-256-Skripthashes in **15 Chargen** zu maximal zwölf Lektionen.
2. `audio-plan/SPRACHAUSSPRACHE.csv` ist eine vorläufige Fachwortliste mit
   absichtlich offenem Ausspracheentscheid.
3. **Wichtig:** Fachtext und Sprechfassung unterscheiden. Fachliche Formeln
   nicht ohne redaktionelle Prüfung zu ungenauen gesprochene Abkürzungen machen.
4. Vor jeder Vertonung fachliche Freigabe oder mindestens Fachkontrolle für
   die konkret vorgesehene Pilotlektion dokumentieren.

Beispiel:

```powershell
py -3.11 tools/prepare_audio_batches.py --pilot
```

Das erzeugt unter `audio-review/pilot/` etwa 180-Wörter-Textsegmente für drei
repräsentative Lektionen und die Datei `abnahme.csv`.

## Schlaufe 2 – Drei Sprachproben und Stimmenauswahl

Pilot-ID | Grund
:-- | :--
`1.01-A` | Allgemeine Einführung und ruhiges Lerntempo
`2.05-B` | Schutztechnik, Fachabkürzungen und normative Vorsicht
`N-P02` | PV-Technik, Zahlen, physikalische Einheiten und Temperaturwerte

Vergleiche nach Möglichkeit mindestens **zwei Stimmen** und die Tempi 0,95×
und 1,0×. Bewertet werden Schweizer Verständlichkeit, Zahlen, Abkürzungen,
Pausen, Aussetzer, Lautstärke und längeres ermüdungsfreies Zuhören.
Nicht freigegebene Audios bleiben ausserhalb des Repositorys.

Wenn Piper plus FFmpeg auf dem lokalen PC installiert sind und du ein legal
bezogenes Modell und dessen `.onnx.json` hast, kann die bestehende
Audioerzeugung gezielt **nur die drei Pilot-IDs** rendern:

```powershell
py -3.11 tools/generate_audio.py --ids 1.01-A,2.05-B,N-P02 --model .voice-cache/de_DE-thorsten-high.onnx --config .voice-cache/de_DE-thorsten-high.onnx.json
```

Das ist eine **vorbereitete Option**, nicht in dieser Umgebung akustisch
getestet. `piper` und `ffmpeg` müssen im `PATH` sein; der Modell-Download und
die Lizenz-/Qualitätsprüfung der Stimme sind separate Schritte. Für andere
Stimmen das eigene Modell und die passende Konfiguration einsetzen.

## Schlaufe 3 – Audiotexte korrigieren, wiederholen und freigeben

Die Probe abschnittsweise anhören. In `audio-review/pilot/abnahme.csv` jede
Stelle beurteilen. Korrekturen an einer getrennten **sprechoptimierten
Fassung** vornehmen; das technische Manuskript nur ändern, wenn der Fachtext
inhaltlich fehlerhaft war. MP3s nach Änderungen vollständig neu erzeugen.

Ein Audiotrack darf erst den Status **FREIGEGEBEN** erhalten, wenn:

- [ ] Technische Zahlen und Einheiten verständlich und korrekt vorgelesen.
- [ ] Schweizer Abkürzungen und Fachbegriffe konsistent ausgesprochen.
- [ ] Keine abgeschnittenen Sätze, Sprünge, Doppelungen oder falschen Pausen.
- [ ] Lautstärke zwischen Lektionen vergleichbar; keine hörbaren Artefakte.
- [ ] Beginn, Mitte und Ende sowie kritische Rechenschritte angehört.
- [ ] MP3-Datei trägt genau die Lektions-ID (z. B. `N-P02.mp3`).
- [ ] Mindestens eine zweite kritische Hörkontrolle für Schutz-/PV-Themen.
- [ ] Audio-Urheber- und Stimmennutzungsrechte geprüft.

## Schlaufe 4 – Kleines freigegebenes Audio-Paket auf GitHub Pages

1. Nach Abnahme die drei endgültigen MP3-Dateien in `public-audio/` kopieren.
2. `py -3.11 tools/verify_audio_approved.py --directory public-audio`.
3. In `.github/workflows/publish.yml` den Befehl
   `python tools/build_site.py --mode text` auf **`--mode partial`** ändern.
4. Drei MP3-Dateien und die Workflow-Änderung committen und pushen.
5. In GitHub Actions den Deploy-Lauf abwarten.
6. Auf dem iPhone im Bereich **Offline & Audio → Fehlende Audios laden**
   bewusst laden, eine vollständige Lektion anhören und den Flugmodus testen.
7. Mit dem bekannten Lernfortschritt prüfen, ob Audiofortsetzung/Navigation
   und automatischer Lektionswechsel wie erwartet funktionieren.

Der kleine Pilot ist ausdrücklich die einzige geplante Audioausnahme im
Git-Repository. Das Quellverzeichnis `.audio-cache/` bleibt ignoriert.

## Schlaufe 5 – Serielle Produktion in kleinen Chargen

Die restlichen 175 Lektionen nach demselben Ablauf bearbeiten. Der
bereitgestellte Chargenplan umfasst 15 Chargen zu zwölf bzw. zuletzt zehn
Lektionen. Beispiel:

```powershell
py -3.11 tools/prepare_audio_batches.py --batch 1
py -3.11 tools/generate_audio.py --ids 1.01-A,1.01-B,1.01-C --model .voice-cache/de_DE-thorsten-high.onnx --config .voice-cache/de_DE-thorsten-high.onnx.json
```

Im zweiten Befehl IDs für die freizugebende Charge ersetzen. Die lokale
Erzeugung speichert Dateien in `.audio-cache/`. Übertrage nach Hörfreigabe
**nur** die abgenommenen MP3s nach `public-audio/` oder zum externen
Audiospeicher. Nie Rohfassungen ungeprüft veröffentlichen.

## Schlaufe 6 – Vollständiger Audio-Rollout auf separatem HTTPS-Speicher

**Wichtige Architekturentscheidung:** Bei ca. 1,38 GB Audio zuzüglich App
ist GitHub Pages allein kein sinnvoller Ort für die komplette 64-kbit/s-Serie.
Die öffentliche Dokumentation nennt eine Website-Grössenbegrenzung von 1 GB.
Plane eine geeignete Object-Storage/CDN-Lösung (z. B. einen kontrollierten
S3-kompatiblen Anbieter); Speicher-, Traffic- und CORS-Kosten zuerst prüfen.

Die App kann für freigegebene Titel ein `audio-manifest.json` nutzen, z. B.:

```json
{
  "version": "0.11.8",
  "voice": "geprüfte Stimme / Version",
  "generated": 2,
  "status": "partial",
  "baseUrl": "https://AUDIO-DOMAIN.example/elektro-efz/",
  "tracks": {
    "1.01-A": "1.01-A.mp3",
    "N-P02": "N-P02.mp3"
  }
}
```

`baseUrl` und die MP3-Endpunkte müssen über HTTPS erreichbar sein, und der
Server muss lesbare CORS-Header sowie einen geeigneten Audio-Content-Type
liefern. Die externen Dateinamen müssen genau passen. Nach Test auf dem
Smartphone stellt man den GitHub-Pages-Workflow von `--mode text` auf
`--mode remote`. Der Offline-Textbestand bleibt unabhängig davon klein.

**Hinweis:** Die App speichert auf ausdrücklichen Nutzerdruck heruntergeladene
MP3s lokal in IndexedDB. Offline funktionieren nur bereits erfolgreich
heruntergeladene Tracks, solange iOS die Website-Daten nicht löscht.

## Ergebnisse und Verantwortlichkeiten

| Abnahme | Artefakt | Wer entscheidet? |
|---|---|---|
| Manuskript / Fachprüfung | `tts_scripts/*.txt`, Fachkorrekturliste | Elektrofachliche Kontrolle |
| Aussprache | `audio-plan/SPRACHAUSSPRACHE.csv` | Projektverantwortung |
| Drei Pilotaufnahmen | `.audio-cache/*.mp3`, Hörprotokoll | Projektverantwortung |
| Testfreigabe | `audio-review/pilot/abnahme.csv` | Projektverantwortung |
| Veröffentlichung | `public-audio/` oder HTTPS-Audiospeicher | Repository-Verantwortliche |
| iPhone-Live-Abnahme | Geräte- und Flugmodus-Protokoll | Endgerätetest |

**Status dieser Lieferung:** Plan und Werkzeuge vorbereitet; es wurde
**keine einzige MP3-Datei produziert oder gehört**.
