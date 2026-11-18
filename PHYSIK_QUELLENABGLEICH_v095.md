# Fachliche Quellen- und Rechenprüfung – v0.9.5

Stand: 17. November 2026. **Dies ist KEINE unabhängige Fachfreigabe, kein Normenkonformitätsnachweis und keine Installationsanleitung.**

## Umfang

Die sechs zusätzlichen Langfassungen behandeln physikalische Grundlagen mit vereinfachten Modellschaltungen. Die Zahlenbeispiele wurden durch 44 separate automatisierte Rechenaussagen geprüft (`v095-physics-check.json`). Alle sechs SVG-Zeichnungen wurden als XML validiert und visuell auf Plausibilität betrachtet. Die ursprünglichen 178 Lektionen bleiben im Projekt.

| ID | Fachgegenstand | Unabhängig herangezogene Grundlagenquelle | Prüfschwerpunkt | Normenstatus |
|---|---|---|---|---|
| 1.09-A | Ladung, Kapazität, Feld, Kondensatorenergie | OpenStax, Physics, 18.5 Capacitors and Dielectrics; College Physics, 19.7 | C=Q/U, W=½CU², Plattenmodell, Parallel-/Serienmodelle | Keine NIN-/Anlagenfreigabe |
| 1.09-B | Induktion, Spulen, Magnetenergie | OpenStax, University Physics Vol. 2, 14.3 Energy in a Magnetic Field; 14.4 RL Circuits | u≈L·ΔI/Δt, W=½LI², τ=L/R, idealisiertes RL-Verhalten | Keine EN-50110-Fachfreigabe |
| 1.09-C | RC-Zeitkonstante und Verlauf | OpenStax, University Physics Vol. 2, RC Circuits / Zeitkonstanten | τ=RC, exponentielle Lade-/Entladefunktion, 63.2%, f=1/(2πRC) | Keine normative Zeitvorgabe |
| 1.10-A | Frequenz, Sinus, Phase | OpenStax, College Physics 2e, 20.5 Alternating Current versus Direct Current | f=1/T, u(t)=Û sin(2πft+φ), Sinuswerte | Keine Gerätespezifikation |
| 1.10-B | RMS, Peak, verzerrte Signale | OpenStax, College Physics 2e, 20.5; University Physics Vol. 2, 15.4 | RMS=√Mittelwert(u²), Sinus RMS=Û/√2, Pulsform | Keine Aussage über Messkategorien |
| 1.10-C | Leistung, Energie, Effizienz und Last | OpenStax, College Physics 2e, 20.4 Electric Power and Energy | W=P·t, kWh, fiktive Lastprofile, Wirkungsgradketten | Keine Bemessung von Installationen |

## Quellenverweise

- https://openstax.org/books/physics/pages/18-5-capacitors-and-dielectrics
- https://openstax.org/books/college-physics/pages/19-7-energy-stored-in-capacitors
- https://openstax.org/books/university-physics-volume-2/pages/14-3-energy-in-a-magnetic-field
- https://openstax.org/books/university-physics-volume-2/pages/14-4-rl-circuits
- https://openstax.org/books/university-physics-volume-2/pages/15-4-power-in-an-ac-circuit
- https://openstax.org/books/college-physics-2e/pages/20-5-alternating-current-versus-direct-current
- https://openstax.org/books/college-physics-2e/pages/20-4-electric-power-and-energy

## Schweizer Ausbildung und Normstatus

EIT.swiss führt Lernmaterial und Informationen für Lernende nach BiVo 2015 und BiVo 2026 getrennt. Ein konkreter Art.-32-BBV-Prüfungsweg wurde für den Nutzer noch nicht bestätigt.

- https://www.eit.swiss/de/bildung/grundbildung/elektroinstallateurin-efz
- https://www.eit.swiss/de/bildung/berufsentwicklung/projekt-bivo2022
- https://www.electrosuisse.ch/de/nin-2025/

Die vollständige NIN 2025 sowie mehrere Normenvolltexte liegen in diesem Projekt nicht vor. Es wäre sachlich falsch, auf dieser Grundlage **178 Lektionen als normengeprüft** zu kennzeichnen. Bei sämtlichen normbezogenen Anforderungen bleiben gültige Ausgabe, spezielle Randbedingungen und eine separate qualifizierte Fachprüfung offen. Kein lizenzierter Normvolltext wird in die öffentliche Website oder das Git-Archiv kopiert.

## Korrektheit und verbleibende Grenzen

Die automatisierten Tests prüfen konkrete Rechenwege, keine unabhängige Aussage über die gesamte fachliche Richtigkeit aller Sätze. Die modellierten Felder, Spulen und RC-Kurven setzen lineare ideale Verhältnisse voraus. Bei realen Bauteilen sind Grenzwerte, Toleranzen, Datenblätter und Gefahren gesondert zu beurteilen. Kein Nutzer soll die didaktischen SVG-Schemata als ausführungsreife Anlagenplanung verwenden.
