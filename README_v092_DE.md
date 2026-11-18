# Elektro EFZ 0.9.2 – Qualitätssicherung und individuellere Unterrichtseinheiten

**Stand:** 17. November 2026. Dieses Paket baut auf v0.9.1 auf. Es wird nicht automatisch auf GitHub veröffentlicht.

## Was tatsächlich fertig ist

- 178 vorhandene Lektionen (145 reguläre + 33 Normen) mit unveränderten IDs und bisherigen Quiz-/Speicherfunktionen.
- 178 individuell beschriftete, eigenständige SVG-Lerngrafiken, aus den tatsächlichen Titeln und Lernzielen erzeugt. 17 Zeichenkategorien, themenspezifische Kennzeichnungen. **Keine 178 einzeln von Elektroplanern konstruierten und abgenommenen Schaltpläne.**
- 3 einzeln geschriebene Lang-Manuskripte mit 15–30 Minuten erwarteter Vorlesedauer: 1.03-B, 2.02-A und 3.07-B. Diese verfügen zusätzlich über 14–20 foliengerechte längere Kapitelabschnitte.
- Insgesamt 100'945 Wörter über alle 178 Sprecher-Manuskripte; 175 Lektionen erreichen das 15-Minuten-Ziel weiterhin **nicht**.
- 1'966 Inhaltsfolien einschliesslich der drei redaktionellen Langfassungen.
- 178 dokumentierte Quellen- und Fachprüfungsstände; kein unbelegtes grünes Häkchen «normenkonform».
- 14 vorhandene Norm-PDFs anhand tatsächlicher Seitenzahlen auf Dateiumfang kontrolliert: 9 vollständig, 5 nur Titel-/Einleitungsseiten.
- 33 Normenlektionen mit 121 automatischen Kapitelabgleichen; in 112 Fällen mögliche PDF-Seiten gefunden, aber damit wurde noch **keine** Aussage fachlich validiert.
- Anzeige des noch offenen Norm- und Fachprüfungsstatus je Lektion in der multimedialen Ansicht.
- Grafiken und Quellenstatus werden für Offlinebenutzung zwischengespeichert; alte lokale MP3s und Lernstände werden nicht bewusst überschrieben.

## Was NICHT fertig ist

1. Keine vollständig einzeln redigierten 15–30-Minuten-Unterrichtseinheiten für die übrigen 175 Lektionen.
2. Keine 178 individuell konstruierte normgeprüfte Stromlauf-/Installationsschaltpläne. Es handelt sich um eigene didaktische SVGs.
3. Keine vollständige Normkonformitätsbestätigung aller 178 Lektionen. Die NIN 2025 samt Corrigendum liegt uns nicht als Volltext vor. Fünf Norm-PDFs sind unvollständig; weitere Fachnormen und aktuelle amtliche Weisungen müssen beschafft und geprüft werden.
4. Keine neue 178er-MP3-Produktion im lokalen Umfeld: Die neuen Lang-Manuskripte können erst über den GitHub-Workflow mit Thorsten erzeugt werden.
5. Keine nachgewiesene Zulassung zu einem EFZ-QV gemäss Art. 32 BBV. Seit 2026 gilt eine neue BiVo; der korrekte QV-Zweig ist mit dem Kanton zu klären.
6. Keine Fachabnahme der didaktischen Grafiken; keine realen Netzspannungs- oder PV-DC-Arbeiten als Hausaufgabe.

## Welche Dateien für welche Aufgabe?

- `quality-review.csv`, `quality-review.json`: konkrete Befunde/Fehlstellen zu sämtlichen 178 Lektionen.
- `norm-abschnitt-fundstellen.csv`: mögliche PDF-Seiten für einzelne Abschnittsverweise der Normen-Akademie (kein Rechts- oder Konformitätsnachweis).
- `lesson-visuals.json` und `visuals/*.svg`: die 178 Visualisierungen.
- `editorial_v092/*.txt`: redaktionell erweiterte Fachtexte für drei Musterlektionen.
- `tts_scripts/*.txt`: tatsächlich von der GitHub-TTS zu sprechende Manuskripte (178 Dateien).
- `lesson-long-slides.js`: auf die neuen Texte abgestimmte Folien für die drei längeren Lektionen.
- `lesson-audit.js`: Prüfstatus und Quelle je Lektion für die Offline-App.
- `tools/validate_v092.py`: strukturelle QA für die 178 Grafiken/Quellenpanels.

**Wichtig:** Ein Dokument oder eine Tabelle, in der eine Norm genannt wird, ersetzt kein überprüftes Normoriginal und keine fachkundige Freigabe. Die geschützten Norm-PDFs gehören NICHT in das GitHub-Repository.
