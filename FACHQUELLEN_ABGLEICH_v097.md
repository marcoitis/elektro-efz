# Quellen- und Qualitätsabgleich · Elektro EFZ v0.9.7

**Prüfdatum:** 17. November 2026 · **Status:** fachlich redigierte Lernmodelle, **keine unabhängige Normenfreigabe**.

## Gegenstand

- `1.07-A`: Mechanische Befestigung, Lastpfad, Werkzeugwahl, Aufmass und Dokumentation
- `1.07-B`: Räumliche Leitungswege, Biegeradien, Wärmeeinfluss, Brandschutzabklärung und Koordination
- `1.07-C`: Gefährdungsbeurteilung, Altbauten, Schadstoffe, Brandabschnitte und Arbeitsstopp
- `1.08-A`: Messgrössen, Messgeräteanschlüsse, CAT-Angaben, Geräte- und Leitungsprüfung
- `1.08-B`: Messgerätebelastung, Spannungsteiler, Messunsicherheit, Messprotokoll
- `1.08-C`: Fehlerhypothesen, Fehlerbaum, Ohmsches Modell, Gegenprüfung und Dokumentation

## Quellen (ohne Übernahme lizenzierter Normtexte)

1. **EIT.swiss, Elektroinstallateur:in EFZ, Grundbildung:** https://www.eit.swiss/de/bildung/grundbildung/elektroinstallateurin-efz — berufliche Ausbildungsbasis, BiVo-2015-Unterlagen und Verweis auf BiVo-2026-Plattform; Auswahl des konkreten Art.-32-Prüfungszweigs offen.
2. **Suva, Branchenregeln Fachkräfte der Gebäudetechnik (84053.D, 2024):** https://www.suva.ch/de-ch/download/regeln-und-tipps/lebenswichtige-regeln-asbest--fachkraft-fuer-gebaeudetechnik--84053.D — fachlicher Hintergrund zum Erkennen von Asbestgefahren.
3. **Suva, Asbest-Checkliste Hauseigentümerschaft (88355.D, 2025):** https://www.suva.ch/de-ch/download/checklisten/asbest--checkliste-fuer-hauseigentuemer-innen--88355.d — vor 1990 errichtete Gebäude und Risiken beim Umbau.
4. **IEC, IEC 61010-2-030:2023, offizieller Publikationseintrag:** https://webstore.iec.ch/en/publication/75915 — Anwendungsbereich und veröffentlichte Übersicht zur Messgerätesicherheit; **nicht Volltext des Standards**.
5. **Fluke, sicherer Umgang mit Digitalmultimetern:** https://www.fluke.com/de-de/mehr-erfahren/blog/sicherheit/multimeter-leitfaden — erläuternde Herstellerinformation zu Messkategorien und Messausrüstung; **keine amtliche Norm**.

## Geprüfte Rechnungen

- Hebelmoment `M=F*l`: 20 N × 0,10 m = 2 Nm.
- Musterbefestigung: 2,4 m / 0,6 m = 4 Intervalle; bei beidseitigen Endpunkten 5 Befestigungspunkte. **0,6 m ist eine fiktive Produktannahme, keine zulässige Normdistanz.**
- Geometrie: 2,4 m + 1,8 m = 4,2 m; 4,8 m bei 2-m-Stangen ergibt ohne Verschnitt mindestens 3 Stangen.
- DC-Modellleitung: 20 m Gesamtlänge × 0,01724 Ω·mm²/m / 2,5 mm² = 0,13792 Ω; bei 4 A: 0,55168 V und 2,20672 W.
- Ohmscher Modellverbraucher: 12 V / 120 Ω = 0,1 A; 12²/120 = 1,2 W; zwei 120-Ω-Widerstände in Reihe ergeben 0,05 A und je 6 V.
- Spannungsteiler 10 kΩ + 10 kΩ an 12 V: ideal 6,000 V; mit Eingangswiderstand 1 MΩ ca. 5,970 V, mit 100 kΩ ca. 5,714 V.
- Differenzmodell: (5,88−6,00)/6,00 = −2 %; (5,97−6,00)/6,00 = −0,5 %.

Die arithmetischen Modellwerte wurden mit `tools/verify_montage_measurement_v097.py` überprüft. Die geometrische Darstellung wurde einzeln als SVG gerendert und visuell geprüft. Diese Prüfungen ersetzen **weder** eine aktuelle Schweizer Normenprüfung noch eine unabhängige fachliche Freigabe.

## Weiterhin fehlende Freigabegrundlagen

- Vollständige **NIN 2025**, Korrekturen und fallbezogene Prüfung der Ausgaben und Geltungsbereiche
- Brandschutzkonzept, Brandschutzsystemnachweise und konkrete Herstellerdaten für reale Leitungsdurchdringungen
- Konkrete Kabel-, Befestigungs- und Installationsproduktdaten für reale Dimensionierung
- Volltext erforderlicher Messgerätenormen, Gerätezertifikate und Gerätezubehörangaben für reale Anwendung
- Bestätigung der BiVo-/Art.-32-Prüfungsordnung durch die zuständige Berufsbildungsstelle
- Unabhängige fachliche Überprüfung sämtlicher sicherheits- und normenrelevanter Einzelaussagen

**0 von 178 Lektionen** sind als normativ unabhängig freigegeben gekennzeichnet.
