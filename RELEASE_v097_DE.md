# Elektroinstallateur EFZ – Release v0.9.7

Stand: 17.11.2026

## Neu im Vergleich zu v0.9.6

Sechs eigenständig fachlich verfasste Langlektionen (alle 15–16 Minuten geschätzt):

| ID | Lektion | Wörter | Minuten (130 W/min) |
|---|---|---:|---:|
| 1.07-A | Werkzeugwahl, Befestigung und mechanische Qualität | 2037 | 15,7 |
| 1.07-B | Trassenplanung, Leitungsführung und Reserve | 1955 | 15,0 |
| 1.07-C | Arbeitssicherheit auf Baustellen und Brandabschottung | 1975 | 15,2 |
| 1.08-A | Multimeter, Messbuchsen und Messkategorien | 2030 | 15,6 |
| 1.08-B | Messabweichung, Innenwiderstand und Protokolle | 1991 | 15,3 |
| 1.08-C | Systematische Fehlersuche am Kleinspannungsmodell | 1987 | 15,3 |

Je Lektion gibt es eine eigenständige SVG-Fachtafel, einen begründeten Praxisfall und fachlich berechnete Modellwerte. Zeichnungen stehen in `visuals/` und `learning-visuals/`. Sprechertexte in `editorial_v097/` und `tts_scripts/`; Folien aus dem v0.9.7-Build in `lesson-long-slides.js`.

**Zusätzliche Reparaturen:** Offline-Cache-Namen und **383 App-Dateieinträge** in `offline.js` und `sw.js` abgeglichen; Offline-MP3-Aktualisierung akzeptiert veröffentlichte Manifeste ab v0.9.1 innerhalb der 0.9.x-Reihe, statt versehentlich nur 0.9.1/0.9.2.

## Stand

- 48 Module und 178 Lektionen (145 regulär, 33 Normen) unverändert
- 27 von 178 Lektionen mit mindestens 1’950 Wörtern Fachsprechertext
- 151 weitere Langlektionen noch ausstehend
- 178 vorhandene Unterrichtsmappen und 534 Quizfragen
- Unabhängige Normenfreigabe: **0 von 178**; die NIN 2025 liegt nicht vollständig vor
- Neuvertonung der geänderten sechs Audios erfolgt erst mit dem GitHub-Workflow

## Test und Freigabegrenzen

- Statische Qualitätsprüfung und Javascript-Syntax bestanden.
- Beide Offline-Dateilisten sind identisch und referenzieren 383 App-Dateien. Der vollständige Offline-PWA-Browsertest auf `localhost` wurde hier durch eine Zugriffssperre der Testumgebung verhindert; ein realer iPhone-Flugmodus-Test steht noch aus.
- 178 SVGs parsebar; sechs neue Fachgrafiken visuell gerendert und geprüft.
- Rechenmodelle und sechs neue Manuskripte per automatisierten Test kontrolliert.
- Mobile/Desktop-Browsertest für alle sechs neuen Lektionen bestanden.
- GitHub-Pages-Probe-Build mit drei Test-MP3s: gesondert protokolliert.
- Keine Live-Veröffentlichung auf dem Benutzer-Repository; keine realen iPhone-/Piper-Tests.
- Fachlicher Detailnachweis siehe `FACHQUELLEN_ABGLEICH_v097.md`.

**Sicherheitsgrenze:** Keine Netzspannungsübungen, kein eigenständiges Arbeiten an bestehenden Installationen, keine Abnahme oder Installationsbewilligung durch die App.
