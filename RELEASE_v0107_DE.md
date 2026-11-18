# Elektro EFZ – Release v0.10.7

Stand: 17.11.2026

## Acht neu bearbeitete Lektionen

- **2.06-B – Leitungsdimensionierung und Spannungsfall**: 2032 Wörter, rechnerisch 15.6 Minuten bei 130 Wörtern/Minute.
- **2.06-C – Schutzkoordination und Selektivität als Einstieg**: 2015 Wörter, rechnerisch 15.5 Minuten bei 130 Wörtern/Minute.
- **2.07-A – Lichtschaltungen im Funktionsschema**: 2103 Wörter, rechnerisch 16.2 Minuten bei 130 Wörtern/Minute.
- **2.07-B – Anschlussplan, Aderliste und Betriebsmittelkennzeichen**: 2023 Wörter, rechnerisch 15.6 Minuten bei 130 Wörtern/Minute.
- **2.07-C – Material- und Zeitkalkulation eines fiktiven Grundrisses**: 2081 Wörter, rechnerisch 16.0 Minuten bei 130 Wörtern/Minute.
- **2.08-A – Lichtstrom, Beleuchtungsstärke und Lichtstärke**: 1980 Wörter, rechnerisch 15.2 Minuten bei 130 Wörtern/Minute.
- **2.08-B – LED-Treiber, Lichtqualität und Effizienz**: 1972 Wörter, rechnerisch 15.2 Minuten bei 130 Wörtern/Minute.
- **2.08-C – Lichtsteuerung und Präsenzanwendungen**: 1971 Wörter, rechnerisch 15.2 Minuten bei 130 Wörtern/Minute.

## Gesamtstand

- 178 Lektionen, 534 Quizfragen und 178 Sprecherdateien erhalten.
- 61 Lektionen im Projekt redaktionell ausgebaut (historische Projektzählung).
- **54 von 178** erreichen anhand tatsächlich gezählter Wörter die 15-Minuten-Schwelle (1’950 Wörter).
- **124** unterschreiten die Mindestwortzahl.
- 178 didaktische SVG-Dateien parsebar; die neuen acht sind Wirk-/Begriffsdiagramme und keine ausführungsreifen Stromlaufpläne.
- 178 Foliensätze und 2’572 Folien erzeugt.

## Technische Tests

- `tools/quality_check.py`: 0 Fehler, 0 Warnungen.
- `tools/quality_check_multimedia.py`: 0 Strukturfehler.
- `tools/validate_v092.py`: 178 SVGs, Render-, Cache-Referenz- und JS-Prüfungen erfolgreich.
- `tools/validate_v093.py`: 178 Unterrichtsmappen und 534 Quizfragen vorhanden.
- Vorherige Audit-Metadaten zu Wortlängen aktualisiert. Die alte Prüfung prüft nun auch neue Editorial-Ordner.

## Grenzen

- Keine vollständige fachliche Einzelprüfung oder unabhängige Normenfreigabe.
- NIN 2025 nicht vollständig abgeglichen.
- Keine echte Audio-Neuvertonung und kein realer iPhone-Offline-Test durchgeführt.
- Geschätzte Sprechdauer ist keine Garantie der späteren Audio-Spieldauer.
