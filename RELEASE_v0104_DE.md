# Elektro EFZ v0.10.4 – Status und Grenzen

Vier neue individuell formulierte Langlektionen ab Quellstand v0.10.3:

| ID | Thema | Wörter | geschätzte Minuten bei 130 W/min |
|---|---|---:|---:|
| 1.01-A | Berufsabschluss, Rollen und Bewilligungsgrenzen | 2026 | 15.6 |
| 1.01-B | Elektrische Gefahren systematisch beurteilen | 1991 | 15.3 |
| 1.01-C | Sicherheitsorganisation und PV-Mehrquellensysteme | 1988 | 15.3 |
| 1.11-B | Basisschutz, Fehlerschutz und Zusatzschutz differenzieren | 2013 | 15.5 |

Ausgeführt: Fachmanuskripte in `tts_scripts/` und `editorial_v0104/`, die vorhandenen Einleitungen beibehalten, 12 neue themenspezifische Foliensätze pro Lektion und 4 einzeln erstellte SVG-Fachgrafiken in beiden visuellen Ordnern.

Sicherheitsabgrenzung: Illustrationen dienen nur der Theorie. Keine praktische Anleitung für Arbeiten an Netzspannung oder PV-DC. Die vollständige NIN 2025 und eine externe Fachabnahme stehen nicht zur Verfügung. Daher keine normative Freigabe.

Nicht durchgeführt: echte Piper-Vertonung, Browser-/iPhone-Test, unabhängige Prüfung des gesamten Kursbestands.

## Gesamtstand und automatische Prüfung

- 41 von 178 Sprechertexten erreichen mindestens 1’950 Wörter; 137 stehen weiter aus.
- `tools/quality_check.py`: 0 Warnungen / 0 Fehler.
- `tools/validate_v093.py`: 178 Lernmappen, 178 SVG-Lernübersichten, 534 Quizfragen.
- `tools/quality_check_multimedia.py`: 178 Foliensätze, 2’419 Folien, 0 strukturelle Fehler; Hinweis «stale audit for 1.01-A» (Audit-Datensatz muss für die neue Redaktion nachgeführt werden).
- Javascript-Syntax der zwei neu generierten Dateien, XML der acht SVG-Dateien und ZIP-Integrität bestanden.
