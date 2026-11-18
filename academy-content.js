/* Elektro EFZ v0.9: Eigenständige Übungsinhalte, keine amtliche Prüfung/Normwiedergabe. */
(function(){'use strict';
const glossary=[
['Spannung U','Potenzialdifferenz zwischen zwei Punkten; Einheit Volt (V).'],
['Stromstärke I','Elektrische Ladung pro Zeit, die durch einen Leiterquerschnitt fliesst; Einheit Ampere (A).'],
['Elektrische Ladung Q','Elektrische Grundgrösse in Coulomb (C); Q = I · t bei konstantem Strom.'],
['Widerstand R','Verhältnis von Spannung und Strom bei ohmschem Verhalten; Einheit Ohm (Ω).'],
['Leitwert G','Kehrwert des Widerstands; G = 1/R, Einheit Siemens (S).'],
['Leistung P','Energieumsatz je Zeit; bei Gleichstrom P = U · I, Einheit Watt (W).'],
['Energie W','Übertragene Energie; W = P · t, übliche Verbrauchseinheit kWh.'],
['Wirkungsgrad η','Verhältnis der nutzbaren Ausgangsleistung zur zugeführten Leistung.'],
['Reihenschaltung','Bauteile liegen im selben Strompfad. Durch alle fliesst derselbe Strom.'],
['Parallelschaltung','Bauteile liegen zwischen denselben Knoten; an allen liegt dieselbe Spannung.'],
['Kirchhoffsche Knotenregel','Summe aller zufliessenden Ströme entspricht der Summe aller abfliessenden Ströme.'],
['Kirchhoffsche Maschenregel','Algebraische Summe aller Spannungen entlang einer geschlossenen Masche ist null.'],
['Leiterquerschnitt','Querschnittsfläche eines Leiters, meist in mm² angegeben.'],
['Spezifischer Widerstand ρ','Werkstoffkennwert des elektrischen Widerstands; beeinflusst Leiterwiderstand.'],
['Spannungsfall','Differenz zwischen Einspeise- und Verbraucherspannung infolge des Leitungswiderstands.'],
['Effektivwert RMS','Gleichspannungsäquivalenter Wert hinsichtlich Wärmeleistung an einem ohmschen Widerstand.'],
['Frequenz f','Anzahl periodischer Schwingungen pro Sekunde; Einheit Hertz (Hz).'],
['Blindwiderstand X','Frequenzabhängiger Widerstandsanteil durch Induktivität oder Kapazität.'],
['Impedanz Z','Gesamter Wechselstromwiderstand als komplexe Grösse; Betrag in Ohm.'],
['Phasenverschiebung φ','Winkel zwischen zwei sinusförmigen Grössen gleicher Frequenz.'],
['Wirkfaktor cos φ','Verhältnis von Wirkleistung zu Scheinleistung bei sinusförmigen Grössen.'],
['Wirkleistung P (AC)','Bei sinusförmigem Einphasenbetrieb P = U · I · cos φ.'],
['Scheinleistung S','Produkt aus Effektivspannung und Effektivstrom; Einheit VA.'],
['Blindleistung Q (AC)','Bei sinusförmigem Einphasenbetrieb Q = U · I · sin φ; Einheit var.'],
['Sternschaltung','Drei Stränge treffen an einem Sternpunkt zusammen. Im symmetrischen Netz ist die Strangspannung ULL/√3.'],
['Dreieckschaltung','Drei Stränge sind zu einem geschlossenen Dreieck verbunden; Strangspannung = Leiterspannung.'],
['Neutralleiter N','Leiter, der im System bestimmungsgemäss Strom führen kann.'],
['Schutzleiter PE','Leiter zur Schutzerdung; er dient nicht als regulärer Betriebsstromleiter.'],
['PEN-Leiter','Kombinierter Schutz- und Neutralleiter in dafür zulässigen Systemen.'],
['Überstromschutz','Schutz gegen zu hohe Ströme durch Überlast oder Kurzschluss, abhängig von Koordination und Auslegung.'],
['RCD / FI','Fehlerstrom-Schutzeinrichtung; vergleicht die Ströme der aktiven Leiter und kann bei Differenz abschalten.'],
['Selektivität','Koordination von Schutzorganen, sodass bei einem Fehler möglichst nur der betroffene Stromkreis abgeschaltet wird.'],
['Kurzschluss','Unbeabsichtigte niederohmige Verbindung zwischen Punkten verschiedener Potenziale.'],
['Schutztrennung','Schutzmassnahme durch elektrische Trennung unter normativ festgelegten Bedingungen.'],
['Schutzkleinspannung','Schutzmassnahme mit begrenzter Spannung und weiteren Anforderungen; kein Synonym für beliebige kleine Spannung.'],
['Isolationswiderstand','Widerstand zwischen leitenden Teilen durch die Isolation; Messung nur mit geeigneter Fachkompetenz.'],
['Durchgängigkeit','Elektrische Kontinuität eines Leitungswegs, beispielsweise eines Schutzleiters.'],
['Erstprüfung','Prüfung einer Anlage vor Übergabe nach den hierfür gültigen Anforderungen, inkl. Besichtigen, Erproben und Messen.'],
['Messprotokoll','Nachvollziehbare Dokumentation von Messverfahren, Messpunkten, Messresultaten und Beurteilung.'],
['Prüfmittel','Messgerät oder Hilfsmittel, dessen Eignung und Zustand für eine konkrete Messung feststehen muss.'],
['IP-Schutzart','Kennzeichnung gegen Zugang/Fremdkörper und Wasser gemäss einschlägigem Normensystem.'],
['Potenzialausgleich','Leitende Verbindung von Teilen zur Verringerung gefährlicher Potenzialunterschiede.'],
['Erdungsanlage','System leitender Teile zur elektrischen Verbindung mit Erde, abhängig von Anlagen- und Schutzkonzept.'],
['Fundamenterder','In oder im Zusammenhang mit Fundamenten angeordnete Erdungseinrichtung nach dafür geltenden Regeln.'],
['Blitzschutz','Massnahmen zum Umgang mit Auswirkungen von Blitzeinschlägen; äusserer und innerer Schutz gehören zusammen.'],
['Photovoltaik-Modul','Bauteil, das Lichtenergie in elektrische Energie wandelt; es kann bei Lichteinfall Spannung liefern.'],
['PV-String','Elektrische Reihenschaltung mehrerer PV-Module, oft mit erhöhter Gleichspannung.'],
['Wechselrichter','Wandelt elektrische Gleich- in Wechselgrössen; Sicherheits- und Netzanforderungen beachten.'],
['Rückspeisung','Energiefluss entgegen der üblichen Einspeiserichtung, z. B. durch PV oder Speichersystem.'],
['Netzanschlusspunkt','Vereinbarter elektrischer Übergabepunkt zwischen Anschlussnehmer und Netzbetreiber.'],
['Werkvorschriften','Regeln der Netzbetreiber bzw. Branchenvorgaben für den Anschluss an Verteilnetze; Ausgabe und Geltung prüfen.'],
['NIN','Schweizer Niederspannungs-Installationsnorm SN 411000; aktuelle Originalausgabe zur Detailprüfung erforderlich.'],
['NIV','Schweizer Niederspannungs-Installationsverordnung SR 734.27; regelt u. a. Bewilligungen und Kontrollen.'],
['BiVo','Bildungsverordnung: rechtlicher Rahmen einer beruflichen Grundbildung.'],
['Bildungsplan','Konkretisiert Handlungskompetenzen und Leistungsziele der Ausbildung.'],
['QV','Qualifikationsverfahren; Abschlussbeurteilung nach den geltenden Vorgaben.'],
['Risikoanalyse','Strukturierte Betrachtung möglicher Gefährdungen, Ursachen und Schutzmassnahmen.'],
['Fünf Sicherheitsregeln','Grundsätzliche Abfolge für spannungsfreie Arbeiten; Anwendung nur mit erforderlicher Befähigung und Berechtigung.'],
['Stromlaufplan','Darstellung elektrischer Funktion und Verbindungen unabhängig vom räumlichen Einbauort.'],
['Installationsplan','Räumliche Zuordnung von Betriebsmitteln, Leitungswegen und Installationspunkten.'],
['Stückliste','Zusammenstellung der geplanten oder benötigten Teile mit Mengen und Bezeichnungen.'],
['Revision','Dokumentierte Änderung an einem Plan oder einer technischen Unterlage.'],
['Wartung','Massnahmen zur Erhaltung einer bestimmungsgemässen Funktion.'],
['Instandsetzung','Massnahmen zur Wiederherstellung einer Funktion nach festgestelltem Mangel.'],
['Diagnose','Systematisches Eingrenzen von Ursachen anhand dokumentierter Symptome und Messdaten.'],
['Lernkompetenz','Anwendbare Fähigkeit, nicht nur Erinnern einer isolierten Information.']
];
const hazards=[
{q:'Eine PV-Anlage ist bei Tageslicht vom Wechselrichter getrennt. Darf die DC-Seite deshalb automatisch als spannungsfrei betrachtet werden?',opts:['Ja, weil kein Wechselstrom eingespeist wird.','Nein, die Module können weiterhin DC-Spannung erzeugen.','Ja, sobald die App offline ist.'],answer:1,why:'PV-Module können bei Beleuchtung Spannung liefern. Die konkrete sichere Vorgehensweise gehört in fachkundige Hände.',category:'PV'},
{q:'An einer alten Installation sind Aderfarben uneinheitlich. Wie gehst Du bei der Beurteilung vor?',opts:['Funktion allein aus der Farbe ableiten.','Vorhandene Dokumentation, Kennzeichnung und fachgerechte Identifikation heranziehen; bei Unklarheit nicht freigeben.','Bei jeder schwarzen Ader von einem Neutralleiter ausgehen.'],answer:1,why:'Farben allein reichen bei Altanlagen nicht als sicherer Funktionsnachweis.',category:'Altbau'},
{q:'Ein RCD löst wiederholt aus. Welche Aussage trifft am ehesten zu?',opts:['RCD durch stärkeres Gerät ersetzen.','Ursache systematisch durch eine befähigte Person klären lassen.','Schutzleiter vorübergehend unterbrechen.'],answer:1,why:'Eine wiederholte Auslösung ist ein Diagnoseanlass. Schutzfunktionen dürfen nicht umgangen werden.',category:'Schutz'},
{q:'Ein Messgerät hat eine beschädigte Prüfleitung. Wie ist vorzugehen?',opts:['Isolierband genügt dauerhaft.','Messung unterlassen und geeignetes, geprüftes Messmittel einsetzen.','Nur die Anzeige weniger stark belasten.'],answer:1,why:'Beschädigte Messmittel sind kein zulässiger Ersatz für sichere Prüfmittel.',category:'Messen'},
{q:'Auf einem Baustellenplan fehlt eine aktuelle Revisionsnummer. Was ist richtig?',opts:['Änderungen ohne Nachverfolgung umsetzen.','Dokumentenstand vor der Ausführung klären und nachvollziehbar dokumentieren.','Immer die älteste Zeichnung verwenden.'],answer:1,why:'Anlagenverantwortung erfordert nachvollziehbaren Dokumentenstand.',category:'Dokumentation'},
{q:'Jemand möchte an einer geöffneten Verteilung eine Leiterzuordnung ausprobieren. Was ist korrekt?',opts:['Bei wenig Betrieb kann man improvisieren.','Ohne erforderliche Befähigung und Sicherheitsverfahren keine Arbeiten durchführen.','Nur die nicht beschrifteten Leiter anfassen.'],answer:1,why:'Offene Verteilungen bergen erhebliche Gefahren. Praktische Arbeiten sind fachkundig zu organisieren.',category:'Sicherheit'},
{q:'Eine beschädigte Leitung fällt bei der visuellen Prüfung auf. Wie wird sie behandelt?',opts:['Wenn sie noch funktioniert, akzeptieren.','Als Mangel dokumentieren, Risiko beurteilen und fachgerecht beheben lassen.','Lediglich im Lernprotokoll erwähnen.'],answer:1,why:'Die blosse Funktion beweist keine Sicherheit.',category:'Prüfung'},
{q:'Ein PV-Wechselrichter zeigt keine Einspeiseleistung. Ist die DC-Seite damit zwangsläufig ungefährlich?',opts:['Ja.','Nein. Ohne geeignete Prüfung und Sicherheitsverfahren darf das nicht angenommen werden.','Nur bei niedriger Aussentemperatur.'],answer:1,why:'Fehlende Einspeisung beweist keine sichere elektrische Trennung aller Quellen.',category:'PV'},
{q:'Bei einer Messung an einem Modellkreis weichen Soll- und Ist-Werte ab. Was ist die bessere erste Reaktion?',opts:['Fehlwert ignorieren.','Messaufbau, Einheiten, Messbereich und Modellannahmen prüfen.','Sofort höhere Spannung anlegen.'],answer:1,why:'Plausibilitätsprüfung geht vor Änderungen am Versuchsaufbau.',category:'Diagnose'},
{q:'Eine Steckdose wurde umgebaut. Darf ihre sichere Funktion nur durch einen Verbraucher-Test bestätigt werden?',opts:['Ja.','Nein, dafür sind die für die Anlage vorgeschriebenen Prüfungen und Nachweise zu beachten.','Ja, falls der Verbraucher klein ist.'],answer:1,why:'Funktionstest und elektrische Sicherheitsprüfung sind nicht gleichzusetzen.',category:'Prüfung'},
{q:'In einem Stromlaufplan stimmen Sicherungsbezeichnung und Stückliste nicht überein. Was jetzt?',opts:['Die grösste Sicherung wählen.','Abweichung klären und konsistent dokumentieren, bevor eine Freigabe erfolgt.','Die Stückliste ohne Prüfung ändern.'],answer:1,why:'Widersprüchliche Unterlagen sind ein technischer Klärungsbedarf.',category:'Planung'},
{q:'Ein Stromkreis fällt unter Last aus. Welches Vorgehen ist für die theoretische Diagnose sinnvoll?',opts:['Schutzorgan dauerhaft überbrücken.','Symptom dokumentieren und systematisch mögliche Ursachen prüfen.','Unbekannte Komponenten auf Verdacht austauschen.'],answer:1,why:'Diagnose basiert auf Hypothesen, Prüfplan und geeigneten Nachweisen.',category:'Diagnose'}
];
const project=[
{year:1,title:'Gebäudedaten und Anforderungen aufnehmen',input:'Nutzungsprofil, Räume, Verbraucher und Annahmen in einem Pflichtenheft festhalten.',check:['Anforderungen getrennt von Annahmen','Räume und Nutzungen vollständig erfasst','Offene Fragen dokumentiert']},
{year:1,title:'Einfachen Lichtkreis skizzieren',input:'Für ein Zimmer eine konzeptionelle Funktionsskizze ohne Installationsausführung zeichnen.',check:['Symbole erklärt','Bedienfunktion beschrieben','Lernmodell als ungefährlich gekennzeichnet']},
{year:1,title:'Energiebedarf überschlagen',input:'Tages- und Jahresverbrauch von fünf ausgewählten Verbrauchern schätzen.',check:['Einheiten stimmen','Annahmen nachvollziehbar','Plausibilitätsprüfung durchgeführt']},
{year:2,title:'Stromkreise auf einem Grundriss planen',input:'Einen Installationsplan als Papier- oder CAD-Übung erstellen; keine reale Ausführung.',check:['Raumzuordnung plausibel','Stromkreise konsistent benannt','Legende und Revision vorhanden']},
{year:2,title:'Drehstromlasten konzeptionell erfassen',input:'Symmetrische und unsymmetrische Lastfälle unterscheiden, Leitungswerte theoretisch berechnen.',check:['Leiter-/Stranggrössen unterschieden','Rechenweg nachvollziehbar','Grenzen der Modellrechnung benannt']},
{year:2,title:'Schutzkonzept als Fragenkatalog formulieren',input:'Welche Schutzmassnahmen, Standortdaten und Normanforderungen müssen Fachpersonen klären?',check:['Keine unbestätigten Normwerte','Prüfpflichten erkannt','Zuständigkeiten notiert']},
{year:3,title:'Verteilung schematisch dokumentieren',input:'Ein einpoliges Übersichtsschema mit Stromkreiskennzeichnung als Entwurf erstellen.',check:['Einspeisungen dargestellt','Abgänge beschriftet','Unterlagenstand nachvollziehbar']},
{year:3,title:'PV-Anlage konzeptionell planen',input:'Dachfläche, Ausrichtung, Verbraucherprofil und Schnittstellen zu Netzbetreiber betrachten.',check:['DC-Risiken identifiziert','Netzanschlussfragen aufgeführt','Keine Eigeninstallation geplant']},
{year:3,title:'Prüfplan als theoretische Checkliste',input:'Die Arten und Zwecke von Besichtigen, Erproben und Messen anhand der Quellen beschreiben.',check:['Messaufgabe begründet','Prüfmittel-Anforderungen bedacht','Fachkompetenzgrenzen ausgewiesen']},
{year:4,title:'Technische Dokumentation zusammenstellen',input:'Grundriss, Stromkreisverzeichnis, Schema, Stückliste und Revisionsverlauf logisch bündeln.',check:['Dokumente konsistent','Änderungen nachvollziehbar','Offene Punkte transparent']},
{year:4,title:'Fehlerfall im Gebäude analysieren',input:'Ein fiktives Störungsszenario anhand von Symptomen, Hypothesen und Diagnoseplan lösen.',check:['Hypothesen priorisiert','Gefahrensituation erkannt','Keine gefährliche Feldanweisung']},
{year:4,title:'Projekt vor Expertengespräch verteidigen',input:'Entscheidungen mit Berechnungen, Annahmen und offenen Normpunkten begründen.',check:['Berechnungen plausibel','Quellenstatus dokumentiert','Grenzen eigener Befugnisse erklärt']}
];
const deep={
 '1.03-A':{
  intro:'Ein Stromkreis ist ein physikalisches System. Die richtige Rechnung beginnt mit einer eindeutigen Skizze und der Frage, welche Grösse gesucht ist.',
  blocks:[
   ['Grundgrössen auseinanderhalten','Spannung beschreibt den Potenzialunterschied zwischen zwei Punkten. Strom ist transportierte Ladung pro Zeit. Widerstand verbindet diese Grössen bei einem ohmschen Bauteil. Einheiten: Volt, Ampere und Ohm.'],
   ['Formel und Annahme','Für einen ideal ohmschen Widerstand gilt U = R · I. Die Formel allein macht noch keine Aussage darüber, ob ein reales Betriebsmittel im gesamten Betriebsbereich ohmsch ist. Temperaturen und nichtlineare Kennlinien können das Modell verändern.'],
   ['Durchgerechnetes Beispiel','Ein 120-Ω-Widerstand liegt an einer idealen 12-V-Gleichspannungsquelle. I = 12 V / 120 Ω = 0,10 A. Seine umgesetzte Leistung ist P = 12 V · 0,10 A = 1,2 W. Ein realer Widerstand muss für diese Verlustleistung geeignet sein.'],
   ['Plausibilität','Verdoppelt sich bei gleichem Widerstand die Spannung, verdoppelt sich der Strom. Die umgesetzte Leistung steigt dann auf das Vierfache: P = U²/R. Diese Abhängigkeit ist für Wärmeentwicklung zentral.'],
   ['Messung als Lernmodell','An einem geeigneten, strombegrenzten Kleinspannungs-Modell misst ein Voltmeter parallel und ein Amperemeter im vorgesehenen Strompfad. Messbereiche und Gerätesicherheit müssen auch bei Kleinspannung zum Aufbau passen.'],
   ['Typische Fehler','Ampere und Milliampere verwechseln; Formeln ohne Einheiten rechnen; 12 V × 120 Ω statt 12 V / 120 Ω; Spannung und Strom als identische Grössen behandeln.']
  ],
  challenge:{q:'Ein idealer 100-Ω-Widerstand liegt an 5 V. Wie gross ist seine elektrische Leistung?',value:0.25,unit:'W',method:'I = 5 V / 100 Ω = 0,05 A. P = U · I = 5 V · 0,05 A = 0,25 W.'}
 },
 '2.02-A':{
  intro:'Drehstrom erfordert die konsequente Unterscheidung von Leiter- und Stranggrössen. Die Formeln gelten nur unter den angegebenen Modellannahmen.',
  blocks:[
   ['Phasenlage','Drei sinusförmige Phasenspannungen gleicher Frequenz haben im symmetrischen Drehstromsystem eine gegenseitige Phasenverschiebung von 120°.'],
   ['Sternschaltung','In der symmetrischen Sternschaltung ist die Leiterspannung √3-mal so gross wie die Strangspannung. Bei 400 V zwischen Aussenleitern ergeben sich rund 230,9 V je Strang.'],
   ['Dreieckschaltung','Im Dreieck liegt an jedem Strang die Leiterspannung. Der Leiterstrom ist bei symmetrischer Last √3-mal so gross wie der Strangstrom.'],
   ['Wirkleistung','Bei symmetrischer sinusförmiger Last gilt P = √3 · U_LL · I_L · cos φ. Ohne Kenntnis von cos φ darf Scheinleistung nicht einfach als Wirkleistung ausgegeben werden.'],
   ['Beispiel','Bei 400 V, 5 A und cos φ = 0,8 ergibt sich P ≈ 1,732 · 400 · 5 · 0,8 = 2771 W. Das ist ein idealisiertes Rechenbeispiel, keine Leitungsdimensionierung.'],
   ['Fehlervermeidung','Nicht 400 V als Strangspannung einer symmetrischen Sternschaltung annehmen. Die Formeln nicht ungeprüft auf unsymmetrische Anlagen übertragen.']
  ],
  challenge:{q:'Welche Strangspannung ergibt sich in einer symmetrischen Sternschaltung bei 400 V Leiterspannung? (auf 1 Dezimalstelle)',value:230.9,unit:'V',method:'U_Str = U_LL / √3 = 400 V / 1,732 ≈ 230,9 V.'}
 },
 '1.02-B':{
  intro:'Sicheres Formelumstellen ist die Grundlage für jede spätere Dimensionierungs- und Messaufgabe.',
  blocks:[
   ['Gleichgewichtsprinzip','Eine Gleichung bleibt gleichwertig, wenn auf beiden Seiten dieselbe zulässige Rechenoperation ausgeführt wird.'],
   ['Beispiel Umstellen','Aus P = U · I wird I = P/U, sofern U nicht null ist. Bei P = 60 W und U = 12 V folgt I = 5 A.'],
   ['Einheitenkontrolle','W/V ergibt A. Die Einheit hilft, offensichtliche Fehler im Rechenweg zu finden.'],
   ['Plausibilitätskontrolle','Bei gleicher Leistung führt eine höhere Spannung zu einem geringeren Strom.'],
   ['Fehlervermeidung','Formel nicht nur auswendig lernen, sondern Rechenschritte hinschreiben; keine Einheiten vorzeitig streichen.']
  ],
  challenge:{q:'Ein Gerät mit 36 W wird idealisiert mit 12 V versorgt. Wie gross ist der Strom?',value:3,unit:'A',method:'Aus P = U · I folgt I = P/U = 36 W / 12 V = 3 A.'}
 }
};
hazards.forEach((h,i)=>{const shift=i%3; if(shift===1){h.opts.push(h.opts.shift());h.answer=(h.answer+2)%3}else if(shift===2){h.opts.unshift(h.opts.pop());h.answer=(h.answer+1)%3}});
window.ElektroAcademyContent={glossary,hazards,project,deep};
})();
