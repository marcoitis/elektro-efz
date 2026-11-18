# Elektro EFZ v0.9.4 – Sechs zusätzliche vollständig redigierte Grundlagenlektionen

Stand: 17. November 2026.

## Tatsächliche Ergebnisse

- 178 Lektionen bleiben vollständig verfügbar (145 reguläre + 33 Normenlektionen).
- **6 neue, einzeln formulierte Fachmanuskripte**, jedes zwischen 2'017 und 2'081 Wörtern, entsprechend rechnerisch 15.5–16.0 Minuten bei der angenommenen Sprechgeschwindigkeit 130 Wörter/Minute.
- Die bisherigen 3 individuell formulierten Langmanuskripte bleiben bestehen. **9 von 178** erreichen nun das Ziel von mindestens 15 Minuten Sprechertext, **169 fehlen**.
- **6 neue, fachlich passend konstruierte didaktische SVG-Stromlaufbilder**, als separate Zeichnungen in `visuals/` und `learning-visuals/` integriert. Diese zeigen physikalische Lernmodelle und sind **keine normativ freigegebenen Installationspläne**.
- 20 Rechenwerte der sechs neuen Lektionen in `v094-math-check.json` automatisch nachgerechnet; jedes neue SVG als XML geprüft und für 178 Lektionen in der App referenziert.
- Die neuen Manuskripte erscheinen im Folienmodus und innerhalb der Unterrichtsmappe. Bei offen bleibenden Lektionen wird keine künstliche Sprecherzeit behauptet.
- Gesamtstand 178 Unterrichtsmappen, 178 Sprechertexte, 2'039 Unterrichtsfolien, 534 Quizfragen.
- **Teilweiser Primärquellenabgleich** einzelner sicherheitsbezogener Aussagen mit SN EN 50110-1:2023, vier dokumentierte Prüfstellen; keine unabhängige Freigabe.

## Die sechs neuen Lektionen

| ID | Fachthema | Manuskript-Wörter |
|---|---|---:|
| 1.03-A | Spannung, Strom, Ladung und Widerstand | 2'081 |
| 1.03-C | Leistung, Verlustwärme und Energie | 2'073 |
| 1.03-D | Messgrundlagen am Kleinspannungsmodell | 2'017 |
| 1.04-A | Serien- und Parallelschaltung | 2'046 |
| 1.04-B | Kirchhoffsche Regeln und Spannungsteiler | 2'063 |
| 1.04-C | Leitungswiderstand, Länge und Querschnitt | 2'050 |

## Noch offen

1. 169 individuell redigierte 15–30-Minuten-Lektionen.
2. Individuell technisch ausgearbeitete und unabhängig geprüfte Zeichnungen für die anderen 172 Lektionen sowie unabhängige Fachfreigabe der sechs neuen Zeichnungen.
3. Vollständige Normenprüfung aller 178 Lektionen. NIN 2025 Volltext fehlt; fünf hochgeladene Normdateien sind nur Auszüge.
4. Tatsächlicher GitHub-Actions-MP3-Build für die sechs geänderten Sprechertexte und Live-Offline-Test auf dem iPhone.

## Technische Prüfung

Die Entwicklung verwendet denselben Kursdatensatz und dieselben Lektionen-IDs. Kein absichtliches Löschen der bestehenden Fortschrittsdaten. Versionswechsel im Service-Worker-Cache von v093 auf v094. Vor Installation den bestehenden Lernstand und die Zusatznotizen exportieren.

Bitte die [GitHub-Updateanleitung](Elektro_EFZ_v0.9.4_GitHub_Update_Anleitung.md) beachten. Norm-PDFs sind lizenzrechtlich geschützt und gehören nicht zum Verteilungspaket.
