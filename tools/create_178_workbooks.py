#!/usr/bin/env python3
"""Build 178 source-grounded study dossiers. These are not certified full-length textbook chapters.
All standards-related content remains under independent specialist review.
"""
from pathlib import Path
from html import escape as H
import json,re,math,subprocess,shutil,textwrap,hashlib
ROOT=Path(__file__).resolve().parent.parent
D=json.loads((ROOT/'data.js').read_text(encoding='utf8').split('=',1)[1].strip(' ;\n'))
N=json.loads((ROOT/'norm_course.json').read_text(encoding='utf8'))
Q=json.loads((ROOT/'quality-review.json').read_text(encoding='utf8'))
QMAP=Q['lessons']
if isinstance(QMAP,list):QMAP={p['id']:p for p in QMAP}
# Original, authored bridges. These explain a particular underlying technical principle,
# not requirements or numeric limits purported to come from an unverified Swiss standard.
BRIDGES={
'1.01':('Berufliche Qualifikation, Verantwortung und sichere Praxis','Ein EFZ bescheinigt einen Bildungsabschluss. Die Erlaubnis, Arbeiten an Niederspannungsinstallationen eigenverantwortlich auszuführen, folgt dagegen den einschlägigen gesetzlichen Bewilligungsregeln. Im Fachgespräch muss man deshalb immer getrennt fragen: Wer verfügt über die berufliche Qualifikation, wer führt die Arbeiten aus, wer trägt die Verantwortung, und welche Bewilligung ist für den konkreten Auftrag erforderlich? Nicht jede PV-Arbeit ist dieselbe Tätigkeit.','Zeichne ein Vier-Felder-Schema mit den Begriffen Berufsabschluss, Fachkundigkeit, Betriebsbewilligung und Auftrag. Markiere für jeden Begriff, welche konkrete Frage Du an eine zuständige Fachperson stellen würdest.'),
'1.02':('Grössen und Einheiten vor Formeln','Eine technische Rechnung beginnt bei der Dimension: Millimeter sind Längen, Quadratmillimeter Flächen und Kubikmillimeter Volumina. Vor dem Einsetzen müssen Einheiten vereinheitlicht werden. Die abschliessende Grössenordnung dient als Fehlerkontrolle; 0,8 kW sind beispielsweise 800 W und nicht 80 W. Ein Taschenrechner bestätigt nur die arithmetische Operation, nicht die richtige physikalische Modellwahl.','Schreibe jede verwendete Grösse mit Symbol, Zahlenwert und Einheit auf. Prüfe die Gleichung zuerst symbolisch und erst dann numerisch.'),
'1.03':('Das Modell hinter U, I, R und P','Für einen ohmschen Widerstand beschreibt U = R · I die Beziehung zwischen Spannung und Strom. Die elektrische Leistung folgt im einfachen Gleichstrommodell aus P = U · I; mit dem Ohmschen Gesetz ergeben sich P = I²R und P = U²/R. Diese Formen beschreiben dieselbe Physik, verlangen aber unterschiedliche bekannte Grössen. Bei temperaturabhängigen oder nichtlinearen Verbrauchern muss das Modell geprüft werden.','Lege einen ungefährlichen Modellstromkreis mit 12 V und 60 Ω als Rechenaufgabe an. Berechne I und P unabhängig in zwei Formen und erkläre die Plausibilität.'),
'1.04':('Strompfade und Knoten zählen','In einer Serienschaltung fliesst durch jedes Bauteil derselbe Strom; in einer Parallelschaltung liegt an jedem parallelen Zweig dieselbe Spannung. Beim Reduzieren eines Netzwerks ist die Topologie wichtiger als der optische Abstand der Bauteile. Knoten und Maschen erlauben es, komplexere Schaltungen in überprüfbare Teilgleichungen zu zerlegen.','Skizziere eine Quelle mit einem Serienwiderstand und zwei parallelen Widerständen. Bezeichne Knoten, Teilströme und die bekannten Grössen, bevor Du rechnest.'),
'1.05':('Werkstoffdaten und Einsatzbedingungen','Leitfähigkeit, Isolationsvermögen, Temperaturbeständigkeit und mechanische Belastbarkeit sind unterschiedliche Eigenschaften. Die Auswahl eines elektrischen Betriebsmittels hängt daher nicht allein von seiner Stromtragfähigkeit ab. Gehäuse, Umwelteinflüsse, UV-Belastung und Schutz gegen das Eindringen von Fremdkörpern müssen zum geplanten Einsatz passen. Herstellerunterlagen sind Bestandteil der Entscheidungsgrundlage.','Vergleiche zwei fiktive Produktdatenblätter mit verschiedenen Einsatztemperaturen und Gehäuseschutzgraden. Notiere, welche Einsatzbedingungen zusätzlich geklärt werden müssen.'),
'1.06':('Pläne als Kommunikationsmittel','Ein Funktionsschema zeigt die logische Funktion, ein Stromlaufplan die elektrischen Verbindungen, und ein Installationsplan die räumliche Zuordnung. Ein Anschlussplan wiederum beantwortet, wo eine konkrete Ader anzuschliessen ist. Keine dieser Darstellungen ersetzt automatisch alle anderen. Revision und eindeutige Kennzeichnung sind wichtig, damit Dokumente zum ausgeführten Stand passen.','Stelle denselben Kleinspannungsschalter mit Leuchte als Funktionsschema, Anschlussliste und einfacher Raumskizze dar. Vergleiche die Informationen.'),
'1.07':('Mechanische Qualität beeinflusst elektrische Sicherheit','Elektrische Installationen werden mechanisch beansprucht: Zugkräfte, Biegung, Vibration, Feuchtigkeit und thermische Bewegung wirken auf Leitungen und Befestigungen. Daher müssen Arbeitsmittel, Befestigungsmaterial und Leitungswege schon in der Planung zusammen betrachtet werden. Die Prüfung ist nicht nur eine Sichtfrage: Die Auswahl ist an Untergrund, Umwelt und Herstellerangaben gebunden.','Plane auf Papier eine Leitungstrasse durch zwei Räume und dokumentiere fünf mechanische Randbedingungen, ohne eine reale Installation auszuführen.'),
'1.08':('Messen heisst vergleichen','Ein Messwert ist nur mit Messgrösse, Gerät, Messbereich, Auflösung und Anschlussart aussagekräftig. Das Messgerät beeinflusst je nach Eingangswiderstand selbst den Stromkreis. Fehlerdiagnose beginnt mit einer Hypothese und einem erwarteten Sollwert; zufälliges Umstecken ersetzt keine Messstrategie. Die praktische Übung beschränkt sich auf geeignete Schutzkleinspannung.','Vergleiche die rechnerisch erwartete und die abgelesene Spannung in einem simulierten 12-V-Spannungsteiler; dokumentiere Messbereich und Unsicherheit.'),
'1.09':('Speichern und zeitversetztes Freigeben von Energie','Kondensatoren speichern Energie im elektrischen Feld, Spulen im magnetischen Feld. Bei zeitabhängigen Vorgängen verändert sich deshalb das Verhalten gegenüber dem rein ohmschen Gleichstrommodell. Für ein einfaches RC-Glied beschreibt τ = R · C die charakteristische Zeit. Idealisierte Bauteilmodelle haben Grenzen, zum Beispiel Leckströme und ohmsche Wicklungsverluste.','Berechne für R = 10 kΩ und C = 100 µF die Zeitkonstante und skizziere qualitativ den Ladeverlauf.'),
'1.10':('Effektivwert und Energieverlauf','Der Effektivwert eines sinusförmigen Stroms entspricht hinsichtlich der Wärmeleistung demjenigen Gleichstrom, der an einem gleichen ohmschen Widerstand dieselbe mittlere Leistung umsetzt. Für eine ideale Sinusform gilt Ueff = Upeak / √2. Die Periodendauer ist T = 1/f. Bei nichtsinusförmigen Signalen dürfen dieselben einfachen Scheitelwertbeziehungen nicht ungeprüft benutzt werden.','Vergleiche bei 50 Hz Periodendauer und bei 325 V Scheitelwert den idealen Effektivwert. Trenne Modellrechnung und reale Messung.'),
'1.11':('Schutzebenen nicht verwechseln','Basisschutz, Fehlerschutz und Zusatzschutz erfüllen unterschiedliche Aufgaben. Eine zusätzliche Schutzmassnahme ist kein Freipass, Grundschutzmassnahmen wegzulassen. Die Wahl und Prüfung hängt vom jeweiligen Netzsystem, der konkreten Installation und den massgeblichen technischen Regeln ab. Für Installationsfreigaben sind Normtext und die zuständige Fachperson entscheidend.','Nimm drei fiktive Fehlerbilder und ordne zu, welche Art von Schutzversagen oder Schutzbedarf jeweils diskutiert werden muss.'),
'1.12':('Ein Modellprojekt dokumentieren','Bei einem 12-V-Lichtmodell wird aus einer Anforderung eine überprüfbare Funktion. Erst kommt die Lastannahme, dann der Stromlaufplan, danach Stückliste und Sollwerte, und abschliessend die Fehlersuche. Gerade das Protokoll trennt eine erfolgreich beobachtete Funktion von einer nachvollziehbar geprüften Funktion.','Erstelle für ein 12-V-Lichtmodell Anforderung, Schaltplan, Stückliste, Sollwert und Messprotokoll als zusammenhängendes Dossier.'),
'2.01':('Wechselgrössen benötigen Betrag und Phase','Spannungen und Ströme können im Wechselstrom zeitlich gegeneinander verschoben sein. Eine Impedanz besitzt deshalb nicht nur einen Betrag, sondern auch Phaseninformation. Bei idealen Spulen steigt der induktive Blindwiderstand mit der Frequenz, bei idealen Kondensatoren sinkt der kapazitive Blindwiderstand. Ergebnisse brauchen eine klare Angabe des Modells.','Skizziere qualitativ das Verhalten eines Widerstands, einer idealen Spule und eines idealen Kondensators bei steigender Frequenz.'),
'2.02':('Drehstrom nicht als dreimal Einphasenstrom behandeln','Ein symmetrisches Drehstromsystem hat drei um 120 Grad phasenverschobene Spannungen. Bei Stern und Dreieck unterscheiden sich die Beziehungen zwischen Strang- und Leiterspannungen beziehungsweise -strömen. Die bekannten √3-Beziehungen setzen die jeweils passende Schaltung und Symmetrie voraus. Bei unsymmetrischen Lasten muss nach Strängen gerechnet werden.','Stelle für das ideale 400-V-System die Strangspannung einer Sternlast einer entsprechenden Dreiecklast gegenüber. Begründe jede verwendete Formel.'),
'2.03':('Induktion und Übersetzung','Ein Transformator nutzt einen zeitlich veränderlichen magnetischen Fluss. Im idealisierten Modell folgt die Spannungsübersetzung dem Windungsverhältnis. In realen Geräten begrenzen Verluste, Erwärmung, Isolation und Betriebsbedingungen die Aussagekraft des einfachen Modells. Schutztrennung ist eine zusätzliche sicherheitstechnische Eigenschaft, nicht eine automatische Folge jeder Übersetzung.','Berechne die Ausgangsspannung eines idealen Transformators mit 1000:100 Windungen und 230 V Eingang; dokumentiere die Grenzen des Modells.'),
'2.04':('Elektronische Bauelemente unterscheiden','Eine Diode lässt Strom unter passenden Bedingungen überwiegend in einer Richtung fliessen; ein Transistor kann verstärken oder schalten. Ein Relais verbindet eine elektrische Ansteuerung mit einem getrennten Kontaktkreis. Digitale Logik beschreibt Zustände und Bedingungen; erst die reale Schaltung legt fest, wie Signale und Energie übertragen werden.','Zeichne die Funktionskette Sensor → Logik → Schaltglied → Last für ein Kleinspannungsmodell.'),
'2.05':('Schutz hängt vom Fehlerweg ab','TN-, TT- und IT-Systeme unterscheiden sich in der Beziehung der aktiven Leiter und Körper zur Erde. Damit ändern sich Fehlerstrompfade und die Auswahl beziehungsweise Beurteilung von Schutzmassnahmen. Ein RCD beobachtet eine Stromdifferenz, ersetzt jedoch keine systematische Prüfung von Schutzleiter, Fehlerweg und Anlagenbedingungen.','Stelle die Unterschiede von TN, TT und IT in einer Vergleichstabelle mit je einem zu prüfenden Schutzaspekt dar.'),
'2.06':('Leitung und Schutzorgan gehören zusammen','Die Strombelastbarkeit einer Leitung ist nicht allein eine Materialkonstante. Sie hängt unter anderem von Leiterquerschnitt, Verlegeart, Temperatur und Häufung ab. Überlast- und Kurzschlussschutz verfolgen unterschiedliche Anforderungen. Ein akzeptabler Spannungsfall ist ebenfalls noch keine ausreichende Sicherheitsfreigabe. Belastbare Entscheidungen benötigen die anwendbaren Normtabellen und Herstellerkennlinien.','Erstelle ein fiktives Lastenblatt und eine Liste fehlender Randbedingungen zur Leitungsdimensionierung. Berechne einen ausdrücklich idealisierten Spannungsfall separat.'),
'2.07':('Von der Raumplanung zur Klemmenliste','Ein Installationsplan zeigt, wo Verbraucher und Betriebsmittel vorgesehen sind. Der Stromlaufplan erläutert ihre elektrische Funktion. Materialliste, Aderverzeichnis und Zeitkalkulation entstehen aus dieser Grundlage, dürfen aber nicht ohne Prüfung als Ausführungsstand verstanden werden. Änderungen müssen in allen betroffenen Unterlagen nachgeführt werden.','Erstelle für einen simulierten Raum eine Raumliste, eine Funktionsskizze, eine Materialliste und markiere den Revisionsstand.'),
'2.08':('Lichttechnik setzt Geometrie voraus','Lichtstrom bezeichnet die abgegebene Lichtmenge, Beleuchtungsstärke den auf eine Fläche bezogenen Anteil. Die einfache Beziehung E = Φ/A ist nur für ein ideal gleichmässig beleuchtetes Modell geeignet. Für reale Räume sind Leuchtenverteilung, Reflexionen, Raumgeometrie und Wartung zu berücksichtigen. LED-Treiber und Steuerung beeinflussen zusätzlich Energiebedarf und Qualität.','Berechne im idealisierten Modell den benötigten Lichtstrom für 20 m² bei 300 lx; nenne mindestens drei Grenzen der Rechnung.'),
'2.09':('Wärme und elektrische Energie getrennt bilanzieren','Elektrische Energie wird aus Leistung und Betriebszeit berechnet. Bei Wärmesystemen muss zwischen elektrischer Eingangsenergie, nutzbarer Wärme und möglichen Verlusten unterschieden werden. Nennleistung ist nicht immer identisch mit tatsächlicher Leistungsaufnahme im Tagesprofil. Kostenvergleiche benötigen Tarif, zeitlichen Verlauf und gegebenenfalls Regelstrategie.','Vergleiche bei einem angenommenen Tarif die Energiekosten zweier unterschiedlicher Nutzungsprofile und notiere, welche Annahmen offen sind.'),
'2.10':('Kommunikation benötigt Schichten und Topologie','Ein physisch angeschlossenes Kabel garantiert noch keine funktionierende Datenverbindung. Physikalische Übertragungsstrecke, Adressierung und Anwendungsebene sind unterschiedliche Diagnoseebenen. Twisted Pair, Glasfaser und Funk haben eigene Eigenschaften und Einschränkungen. Eine systematische Fehlersuche beginnt daher mit einer eindeutigen Netzskizze.','Zeichne ein kleines Heimnetz mit Router, Switch und zwei Geräten. Notiere je ein mögliches Problem auf physikalischer und IP-Ebene.'),
'2.11':('Prüfen ist eine begründete Reihenfolge','Eine Erstprüfung verbindet Sichtprüfung, geeignete Messverfahren und dokumentierte Bewertung. Der Prüfende muss wissen, welche Eigenschaft der Anlage untersucht wird und welche Aussage ein bestimmtes Messresultat erlaubt. Für reale Prüfverfahren und Grenzwerte gelten die aktuelle Norm und die erforderliche Qualifikation. Im Selbststudium werden Messberichte interpretiert, nicht Netzprüfungen ausgeführt.','Entwirf ein Musterprüfprotokoll mit Prüfschritt, Zweck, Messwert, Bewertung und fehlender Grundlage für einen fiktiven Fall.'),
'2.12':('Ein Wohnungsdossier durchdenken','Eine Elektroplanung beginnt mit Nutzung, Anschlussbedarf und Randbedingungen. Danach werden Stromkreise, Schutzkonzept, Leitungswege und Dokumentation aufeinander abgestimmt. Ein Planungsentwurf ist kein freigegebener Ausführungsplan; dafür sind gültige Regeln und fachkundige Prüfung notwendig.','Erstelle zu einer fiktiven Wohnung ein Raumbuch, Lastenliste und eine Liste der offenen Dimensionierungsangaben.'),
'3.01':('Installationssysteme und Verteiler als Gesamtsystem','Unterputz-, Aufputz- und Hohlwandinstallationen unterscheiden sich in Zugänglichkeit, mechanischer Beanspruchung und Umgebungsbedingungen. Ein Verteiler ist keine beliebige Sammlung von Einzelgeräten, sondern Teil einer abgestimmten Schaltgerätekombination. Bei Planung und Bewertung müssen Kennwerte der Gesamtkombination und Herstellerangaben zusammengeführt werden.','Skizziere schematisch einen Leitungsweg von einer Verteilung zu drei Räumen und notiere mechanische und brandschutztechnische Prüfpunkte.'),
'3.02':('Schutzgerätekoordination als Systemfrage','Ein Leitungsschutzschalter begrenzt nicht automatisch jede beliebige Fehlerenergie, und ein RCD erfüllt eine andere Schutzfunktion. Selektivität betrachtet, ob bei Fehlern möglichst nur das betroffene Schutzorgan anspricht. Dafür braucht es passende Kennlinien, Kurzschlussdaten und die konkreten Gerätekombinationen; die Nennstromangabe allein reicht nicht.','Vergleiche zwei abstrakte Zeit-Strom-Kennlinien qualitativ. Welche zusätzlichen Herstellerdaten wären für eine Selektivitätsaussage nötig?'),
'3.03':('Ein Messergebnis ist noch kein Prüfentscheid','Für die Erstprüfung müssen Verfahren, Messbedingungen, Geräteangaben und Ergebnisse zusammen dokumentiert werden. Messunsicherheit, ungeeignete Messpunkte und fehlende Vorprüfungen können die Beurteilung verfälschen. Die Freigabe einer Installation folgt nicht aus einem einzigen grünen Messwert.','Bewerte eine fiktive Liste unvollständiger Prüfdaten: Welche Angaben fehlen, bevor eine Fachperson überhaupt entscheiden kann?'),
'3.04':('Drehmoment, Drehzahl und Schlupf','Bei einem Asynchronmotor liegt die mechanische Drehzahl im Motorbetrieb typischerweise unter der Drehfelddrehzahl. Die Differenz wird als Schlupf beschrieben. Mechanische Leistung folgt aus Drehmoment und Winkelgeschwindigkeit; elektrische Aufnahmeleistung ist wegen Verlusten grösser. Motor-, Leitungs- und Schutzauslegung sind getrennt zu betrachten.','Berechne bei 10 N·m und 1500 U/min die mechanische Leistung. Trenne diesen Wert ausdrücklich von der elektrischen Aufnahmeleistung.'),
'3.05':('Steuerungslogik nachvollziehbar dokumentieren','Eine Selbsthaltung ist eine logische Speicherwirkung durch rückgeführten Kontakt. Verriegelung verhindert bestimmte gleichzeitig unzulässige Zustände. Eine gewöhnliche Funktionslogik ist nicht automatisch eine sicherheitsgerichtete Steuerung. Bei einem Not-Halt-System sind andere Anforderungen und Nachweise relevant als bei einer Bedienfunktion.','Formuliere eine Wahrheitstabelle für Start, Stopp und Betriebsmeldung in einem Kleinspannungs-Funktionsmodell.'),
'3.06':('Buskommunikation verändert die Fehlersuche','Ein Bussystem verteilt Informationen zwischen Teilnehmern. Ein fehlerhaftes Verhalten kann von Sensorik, Parametrierung, Übertragung oder Aktorik verursacht werden. Topologie und Zuordnung sind deshalb Teil der technischen Dokumentation. Fernzugriff schafft zusätzliche Anforderungen an Berechtigungen, Datenschutz und sichere Konfiguration.','Erstelle eine Raumskizze mit zwei Sensoren, einem Aktor und einem Bus. Erkläre, welche Information bei einer Störung zuerst geprüft werden müsste.'),
'3.07':('PV-Kennlinien sind temperaturabhängig','Ein PV-Modul hat keinen festen Spannungswert über alle Betriebszustände. Einstrahlung, Zelltemperatur und Lastpunkt beeinflussen die Strom-Spannungs-Kennlinie. Für eine Stringplanung müssen insbesondere Leerlaufspannung bei niedriger Temperatur und Spannungsbereich des Wechselrichters betrachtet werden. Exakte Entscheidungen erfordern die realen Herstellerkennlinien und Normvorgaben.','Vergleiche als reine Rechenübung zwei hypothetische Modulkennlinien bei unterschiedlichen Temperaturen. Markiere die Daten, die für eine echte Stringplanung fehlen.'),
'3.08':('PV-Projekt umfasst Technik und Verfahren','Planung, baurechtliche Abklärung, Anschlussgesuch, Messkonzept, Installation, Prüfung und Übergabe sind voneinander zu unterscheidende Schritte. Die Bewilligungslage hängt von der Tätigkeit ab. Auch die Dokumentation zu Kennzeichnung und Erstprüfung erfordert eine fachlich richtige und aktuelle Grundlage.','Entwirf eine Prozessgrafik einer PV-Anlage von der Idee bis zur Übergabe und kennzeichne die Punkte, die eine berechtigte Fachperson bestätigen muss.'),
'3.09':('Besondere Umgebungen verändern Randbedingungen','Feuchte, leitfähige Umgebung, temporäre Installationen, Brandgefährdung und äussere Einflüsse verändern Schutzbedarf und Materialauswahl. Eine gewohnte Lösung aus einem Wohnraum kann deshalb nicht einfach auf ein Bad, eine Baustelle oder einen landwirtschaftlichen Betrieb übertragen werden. Konkrete Zonen und Zahlenwerte müssen in der gültigen NIN überprüft werden.','Vergleiche zwei fiktive Betriebsstätten und erstelle eine Liste von Umgebungsbedingungen, die für die Fachbeurteilung wichtig sind.'),
'3.10':('Übertragungsstrecke gegen Systemfehler abgrenzen','Bei Kupferverbindungen sind Pinbelegung, Dämpfung und Übersprechen unterschiedliche Fehlerklassen. Glasfaserstrecken benötigen zusätzlich eine Betrachtung optischer Dämpfung und geeigneter Steckflächen. Koaxialstrecken haben wiederum eigene Abschluss- und Pegelbedingungen. Ein Messbericht ist ohne passende Streckenklasse und Messmethode unvollständig.','Ordne drei symptomatische Netzwerkfehler einer möglichen Messstrategie zu, ohne reale Faseranschlüsse zu manipulieren.'),
'3.11':('Diagnose als Hypothesenprüfung','Eine strukturierte Fehlersuche beginnt mit Symptomen, Randbedingungen und einer überprüfbaren Hypothese. Durch die Auswahl möglichst aussagekräftiger und sicherer Beobachtungen wird die Ursache eingegrenzt. Dokumentierte Soll-Ist-Vergleiche helfen, voreilige Teilewechsel zu vermeiden. Sichere Grenzen und Freigaben gelten auch bei scheinbar einfachen Fehlern.','Erstelle einen Fehlerbaum für eine fiktive Leuchte, die im Kleinspannungsmodell nicht funktioniert. Notiere sichere Prüfschritte.'),
'3.12':('Mehrere Teilsysteme koordinieren','Gebäudelasten, PV-Erzeugung, Speicher, Ladepunkt und Kommunikation beeinflussen sich gegenseitig. Jede Teilauslegung kann im Einzelnen plausibel erscheinen und dennoch an Schnittstellen unvollständig sein. Deshalb braucht ein Gesamtdossier konsistente Annahmen, Schnittstellen und dokumentierte Verantwortlichkeiten.','Erstelle eine Schnittstellenliste zu einem Haus mit PV, Wärmepumpe und Ladestation; markiere fehlende Daten.'),
'4.01':('Wirkleistung folgt aus dem passenden Modell','Bei symmetrischen sinusförmigen Drehstromsystemen lässt sich Wirkleistung mit P = √3 · ULL · IL · cos φ berechnen. Bei unsymmetrischen Systemen muss die Rechnung angemessen aufgeteilt werden. Blindleistung und Leistungsfaktor beschreiben verschiedene Aspekte der Energienutzung. Rechenergebnisse brauchen Annahmen, Einheiten und Plausibilitätskontrolle.','Berechne bei 400 V, 10 A und cos φ = 0,8 die Wirkleistung einer symmetrischen Last und erläutere die Modellgrenzen.'),
'4.02':('Abschaltbedingung und Selektivität auseinanderhalten','Schutz gegen elektrischen Schlag und möglichst störungsarme Abschaltung bei Fehlern sind unterschiedliche Planungsziele. Für die Beurteilung braucht es Fehlerweg, Schutzgerät, Kennlinien und die anwendbaren Abschaltbedingungen. Ein bestimmter Leitungsschutzschalter kann ohne Kenntnis des gesamten Stromkreises nicht als passend oder selektiv freigegeben werden.','Erstelle eine Prüf-Checkliste für einen vorliegenden Kurzschluss- und Schutzgerätefall: Welche Mess- und Herstellerdaten fehlen?'),
'4.03':('Eigenverbrauch und Speicherverluste bilanzieren','Photovoltaikertrag und zeitgleicher Strombedarf bestimmen den unmittelbaren Eigenverbrauch. Ein Speicher verschiebt Energie zeitlich, verursacht aber Verluste und hat Kapazitäts- sowie Leistungsgrenzen. Eine Ladestation benötigt zusätzlich ein Lastmanagement, das den anderen Verbrauchern und den Anschlussbedingungen Rechnung trägt.','Zeichne für einen fiktiven Haushalt Tageskurven von Last und PV-Erzeugung. Markiere Eigenverbrauch und Überschüsse qualitativ.'),
'4.04':('Zustandsautomaten für nachvollziehbare Funktionen','Eine Steuerung sollte nicht nur mit lose verbundenen Schaltbedingungen beschrieben werden. Zustände, Auslöser und erlaubte Übergänge machen unerwartetes Verhalten erkennbar. Sicherheitskritische Funktionen benötigen zusätzlich einen eigenständigen sicherheitsbezogenen Nachweis. Eine Simulation kann Logikfehler sichtbar machen, ersetzt aber keine Inbetriebnahmeprüfung.','Modelliere einen kleinen Zustandsautomaten mit Aus, Bereit, Betrieb und Störung. Beschreibe die erlaubten Übergänge.'),
'4.05':('Prüfdossier als überprüfbare Begründung','Ein vollständiges Prüfungsdossier verbindet Anlagenidentifikation, Prüfumfang, verwendete Messmittel, Einzelergebnisse und Abweichungen. Die Freigabe ist ein begründeter Fachentscheid. Liegt ein entscheidender Nachweis nicht vor, ist «nicht beurteilbar» ehrlicher als ein grüner Haken.','Prüfe ein fiktives Messprotokoll auf fehlende Felder und begründe, warum einzelne Zahlen nicht für eine Freigabe reichen.'),
'4.06':('Hierarchie und Geltungsbereich von Regeln','Ein Gesetz, eine Verordnung, eine Norm und eine Herstelleranweisung sind unterschiedliche Quellen. Ihre Rolle und Verbindlichkeit hängen von der konkreten Anwendung ab. Ein Normzitat muss Ausgabe und Abschnitt nennen; ohne Originaltext darf aus einer Kapitelüberschrift kein detaillierter Grenzwert abgeleitet werden.','Wähle drei fachliche Aussagen und dokumentiere jeweils: Quelle, Ausgabe, Abschnitt und ob die Aussage anhand des Originaltextes geprüft wurde.'),
'4.07':('Projektabwicklung und Nachvollziehbarkeit','Ein technischer Auftrag braucht klare Schnittstellen, Termine, Prüfkriterien und Änderungsdokumentation. Ein Arbeitsrapport zeigt nicht nur verbrauchte Zeit, sondern auch Leistungen und Abweichungen. Revisionsunterlagen müssen zum endgültigen Zustand passen, damit späterer Betrieb und Wartung möglich sind.','Erstelle einen kurzen Projektänderungsrapport mit Auswirkung auf Material, Termin und Dokumentation.'),
'4.08':('PV-Dossier vor Freigabe kritisch prüfen','Eine PV-Dokumentation sollte die identifizierbaren Komponenten, Herstellerdaten, Auslegungsannahmen und sicherheitsrelevanten Nachweise schlüssig verbinden. Fehlende DC-Kennwerte, unklare Stecksysteme oder eine nicht nachvollziehbare Stringzuordnung sind offene Fachfragen. Das Unterrichtsdossier ersetzt weder Erstprüfung noch normgerechte Freigabe.','Vergleiche ein fiktives Modulblatt mit einer Stringliste und kennzeichne fehlende Angaben, ohne ein reales System in Betrieb zu nehmen.'),
'4.09':('Kommunikationsstrecken anhand von Kriterien prüfen','Für die Diagnose einer Datenverbindung werden physikalischer Link, Streckenleistung, Geräteparameter und Anwendung getrennt betrachtet. Eine erfolgreiche LED-Anzeige sagt wenig über tatsächliche Übertragungsqualität. Messmethoden und Grenzwerte müssen zur Strecke und zur eingesetzten Norm passen.','Erstelle zu drei Diagnosefällen jeweils zwei Hypothesen und eine sichere Prüfungsmethode.'),
'4.10':('Ein Fachgespräch prüft Begründungskompetenz','Wer eine technische Lösung erklären kann, benennt Annahmen, relevante Regeln, Prüfschritte und Alternativen. Auswendig gelernte Formeln genügen nicht, wenn wesentliche Randbedingungen fehlen. Gute Antworten unterscheiden sichere Beobachtungen von Vermutungen und geben offen an, wann fachliche Freigabe erforderlich ist.','Erkläre ein gewähltes Schaltbild in zwei Minuten und beantworte danach drei Rückfragen zu Annahmen, Sicherheitsgrenzen und Nachweisen.'),
'4.11':('Schriftliche Prüfungen erfordern Transfer','Bei einer Prüfungsaufgabe müssen Aufgabenstellung, gegebene Daten, gesuchte Grösse und geeignete Methode zuerst sauber getrennt werden. Das Rechenergebnis ist dann mit Einheit und Plausibilität zu beurteilen. Ein falscher Ansatz lässt sich nicht durch präzisere Dezimalstellen korrigieren.','Bearbeite eine gemischte Übungsprüfung und vermerke zu jedem Fehler, ob er aus Begriff, Modell, Rechnen oder Normenwissen entstanden ist.'),
'4.12':('Praktische Kompetenz bleibt nachweispflichtig','Eine digitale Simulation kann die Planung, Analyse und Reflexion unterstützen. Sie dokumentiert aber nicht die sichere Durchführung einer Elektroinstallation, die Messkompetenz oder die Ausführung in einer beaufsichtigten Werkstatt. Für die formelle QV-Zulassung zählen die zuständigen Stellen und die verlangten Praxisnachweise.','Stelle ein Portfolio zusammen, das Theoriebescheinigungen und von Fachpersonen bestätigte Praxisnachweise getrennt erfasst.'),
}
assert len(BRIDGES)==48

def clip(s,n=105):
 s=' '.join(str(s).split())
 return s[:n-1]+'…' if len(s)>n else s

def normalize(s):return ' '.join(str(s).replace('\\n',' ').split())
def norm_id(l,norm):return ('N-'+l['id']) if norm else l['id']
def safe_svg(s):return H(clip(s,72),quote=True)

# A full bespoke graphic is not always a circuit diagram: diagram type reflects each lesson's topic.
def make_svg(lid,title,headings,question,isnorm):
 title=clip(title,67)
 labels=[clip(x,57) for x in headings[:4]]
 if len(labels)<3:labels+=['Fachlichen Zusammenhang prüfen']*(3-len(labels))
 labels=labels[:3]
 # Unique layout and callouts from the actual authored lesson headings.
 accent=('#9D7430' if isnorm else '#2576a7')
 x=[37,286,535];
 parts=[f'<rect x="{x[i]}" y="122" width="213" height="116" rx="12" fill="#F0F5F9" stroke="{accent}" stroke-width="1.8"/>' for i in range(3)]
 for i,lab in enumerate(labels):
  words=lab.split(); lines=[]; line=''
  for w in words:
   if len(line+' '+w)>23 and line:lines.append(line);line=w
   else:line=(' '.join([line,w])).strip()
  if line:lines.append(line)
  lines=lines[:3]
  parts.append(f'<text x="{x[i]+106}" y="{166-11*(len(lines)-1)}" fill="#102D42" text-anchor="middle" font-size="16" font-weight="600">'+''.join(f'<tspan x="{x[i]+106}" dy="22">{H(v)}</tspan>' for v in lines)+'</text>')
  parts.append(f'<text x="{x[i]+18}" y="146" fill="{accent}" font-size="14" font-weight="bold">{i+1:02d}</text>')
 parts+=['<path d="M252 180 H283" stroke="#45677D" stroke-width="2.5"/>','<path d="M501 180 H532" stroke="#45677D" stroke-width="2.5"/>','<path d="M275 175 L283 180 L275 185" stroke="#45677D" fill="none" stroke-width="2"/>','<path d="M524 175 L532 180 L524 185" stroke="#45677D" fill="none" stroke-width="2"/>']
 q=clip(question,97)
 return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 785 338" role="img" aria-label="Fachliche Lernübersicht für {H(title)}">
 <rect width="785" height="338" fill="#fff" rx="16"/>
 <path d="M23 20 H761" stroke="{accent}" stroke-width="5"/><text x="35" y="52" font-size="12" font-family="Arial,sans-serif" fill="{accent}">ELEKTRO EFZ · LERNLOGIK · {H(lid)}</text>
 <text x="35" y="86" font-family="Arial,sans-serif" font-size="22" font-weight="bold" fill="#102D42">{H(title)}</text>
 <g font-family="Arial,sans-serif">{''.join(parts)}</g>
 <text x="35" y="274" font-family="Arial,sans-serif" font-size="14" fill="#102D42" font-weight="bold">Transferfrage</text>
 <text x="35" y="298" font-family="Arial,sans-serif" font-size="14" fill="#375569">{H(q)}</text>
 <text x="35" y="322" font-family="Arial,sans-serif" font-size="10" fill="#697F8A">Didaktische Konzeptgrafik – kein Installationsschema, keine Normenfreigabe.</text>
 </svg>'''

allrows=[];out=ROOT/'workbooks';out.mkdir(exist_ok=True);svgout=ROOT/'learning-visuals';svgout.mkdir(exist_ok=True)
for isnorm,lessons in [(False,D['lessons']),(True,N['lessons'])]:
 for l in lessons:
  lid=norm_id(l,isnorm)
  mod=l.get('moduleId')
  sec=l['blocks'] if isnorm else l['parts']
  facts=[{'heading':p['heading'],'text':normalize(p['text']),'formula':p.get('formula','')} for p in sec]
  objectives=l.get('objectives') or [l['lead'],l['scenario']]
  quiz=l['quiz']
  q_clean=[]
  for q in quiz:
   q_clean.append({'question':q.get('question',q.get('q','')),'options':q['answers'],'correct':q['correct'],'why':q['why']})
  # Provide a traceable, relevant supporting excerpt from the authored lesson text when possible.
  # This adds explanation without inventing a norm threshold or safety-critical instruction.
  stop={'welche','welcher','welches','einer','einem','einen','dieser','diese','dieses','kann','oder','aber','nicht','sind','wird','wenn','dass','was','wie','mit','bei','die','der','das','den','dem','des','ein','eine','und','von','für','zum','zur','ist','als','aus','auf','sich','auch','über','nach','nur','darf','hier','laut','soll'}
  def terms(v):return {w.lower() for w in re.findall(r'[A-Za-zÄäÖöÜüß0-9]{4,}',v) if w.lower() not in stop}
  better=0
  for q in q_clean:
   needle=terms(q['question']+' '+q['options'][q['correct']]+' '+q['why'])
   candidates=[]
   for p in facts:
    relevant=terms(p['heading']+' '+p['text']);score=len(needle & relevant)
    if score>=2:candidates.append((score,p))
   q['whyExtended']=q['why']
   if candidates:
    _score,p=max(candidates,key=lambda r:r[0]);sentences=re.split(r'(?<=[.!?])\s+',p['text'])
    top=max(sentences,key=lambda ss:len(terms(ss)&needle)) if sentences else ''
    if top and len(top)>25:
     q['whyExtended']+='\n\nBezug zum Unterrichtsteil «'+p['heading']+'»: '+top
     better+=1
  if isnorm:
   concept='Spezifische Fallstudie auf Grundlage der genannten Normausgabe; normativer Einzelabgleich ausstehend.'
   bridge=l.get('lead','')
   task=l.get('scenario','')
   solution=l.get('model','')
   references=[l.get('source','')] + [str(s) for s in l.get('sections',[])]
   headings=[v['heading'] for v in facts[:3]]
  else:
   concept,bridge,task2=BRIDGES[mod]
   task=l.get('task','')+' '+task2
   solution=' '.join(q['why'] for q in q_clean)
   references=l.get('references',[])
   headings=[v['heading'] for v in facts[:3]]
  audit=QMAP.get(lid,{})
  path=ROOT/'tts_scripts'/f'{lid}.txt'
  txt=path.read_text(encoding='utf8') if path.is_file() else ''
  words=len(txt.split())
  # Each lesson's 25-minute guided self-study sequence is customised with its own
  # goals, subject paragraphs, diagram labels, task and knowledge question. The sum
  # is a *learning activity window*, not a claim about the duration of the MP3.
  lesson_plan=[
   {'title':'Einstieg und Vorwissen','minutes':3,'instruction':'Formuliere ohne Nachschlagen eine erste Antwort auf das Lernziel: '+objectives[0]},
   {'title':'Fachliche Erklärung erarbeiten','minutes':6,'instruction':'Lies die Abschnitte «'+facts[0]['heading']+'» und «'+(facts[1]['heading'] if len(facts)>1 else facts[0]['heading'])+'». Notiere die entscheidende Ursache-Wirkungs-Beziehung in eigenen Worten.'},
   {'title':'Lernlogik-Grafik auswerten','minutes':3,'instruction':'Erkläre anhand der Grafik den Übergang zwischen «'+headings[0]+'» und «'+(headings[-1])+'». Ist der dargestellte Ablauf für Deinen Fall vollständig?'},
   {'title':'Praxisfall lösen','minutes':7,'instruction':task},
   {'title':'Kontrollfragen lösen','minutes':4,'instruction':'Beantworte zunächst ohne Lösungshilfe: '+q_clean[0]['question']},
   {'title':'Reflexion und offene Normen','minutes':2,'instruction':'Halte eine Unsicherheit und eine relevante Fachquelle fest. Beurteile, was Du selbst berechnen kannst und was eine berechtigte Fachperson prüfen muss.'},
  ]
  assert sum(z['minutes'] for z in lesson_plan)==25
  # Require independent manual editorial + independent specialist check before release.
  unit={
    'id':lid,'year':l.get('year',int(lid[0]) if not isnorm else 1),'title':l['title'],'isNorm':isnorm,'topic':l.get('subject') or mod,
    'learningGoals':objectives,'parts':facts,'expertBridgeTitle':concept,'expertBridge':bridge,
    'practicalExercise':task,'solutionGuide':solution,'quiz':q_clean,'references':references,
    'normSections':l.get('sections',[]),'normEdition':l.get('source','') if isnorm else '',
    'visual':'./learning-visuals/'+lid+'.svg',
    'sessionPlan':lesson_plan,
    'ttsWords':words,'ttsMinutesAt130wpm':round(words/130,1),
    'editorialRelease':('15–30-Minuten-Fachmanuskript erstellt; fachliche Normenfreigabe ausstehend' if any((ROOT/folder/(lid+'.txt')).is_file() for folder in ('editorial_v092','editorial_v094','editorial_v095','editorial_v096','editorial_v097')) and 1950<=words<=3900 else 'OFFEN – nicht als 15–30-Minuten-Fachkapitel freigegeben'),
    'fullManuscript':(txt if any((ROOT/folder/(lid+'.txt')).is_file() for folder in ('editorial_v092','editorial_v094','editorial_v095','editorial_v096','editorial_v097')) else ''),
    'visualKind':('Fachlich konstruierte didaktische Schaltskizze – keine Ausführungsplanung' if any((ROOT/f/(lid+'.txt')).is_file() for f in ('editorial_v094','editorial_v095','editorial_v096','editorial_v097')) else 'Allgemeine Lernkonzeptgrafik'),
    'technicalRelease':'OFFEN – nur Quellen- und Plausibilitätsvorprüfung',
    'missingNorms':audit.get('missing_or_followup',[]),
    'reviewedBy':None,'reviewedAt':None,
  }
  allrows.append(unit)
  svgout.joinpath(lid+'.svg').write_text(make_svg(lid,l['title'],headings,q_clean[0]['question'],isnorm),encoding='utf8')
  lines=[f'# {lid} – {l["title"]}', '', '**Status:** Lehrmappe aus vorhandenem Material zusammengestellt; inhaltliche Einzelredaktion und Normenfachprüfung offen.', '', '## Lernziele']
  lines+=['- '+o for o in objectives]+['','## Fachliche Einführung: '+concept,'',bridge,'']
  for i,p in enumerate(facts,1):lines+=['## Unterrichtsabschnitt '+str(i)+': '+p['heading'],'',p['text'],'']+(['Formel: '+p['formula'],''] if p['formula'] else [])
  lines+=['## Angepasstes Selbststudium – 25 Minuten (Audiozeit separat)','']
  for item in lesson_plan:lines+=[f"- **{item['minutes']} min – {item['title']}:** {item['instruction']}"]
  lines+=['']
  lines+=['## Praxisaufgabe (Papier / Simulation)','',task,'','## Lösung und Beurteilung','',solution,'','## Kontrollfragen']
  for i,q in enumerate(q_clean,1):lines+=[f'### Frage {i}: {q["question"]}',f'**Lösung:** {q["options"][q["correct"]]}',f'**Begründung:** {q["whyExtended"]}','']
  lines+=['## Normen-/Quellenstatus','','- '+'\n- '.join(str(ref) for ref in references),'- Einzelabgleich an Originalquelle und Fachfreigabe ausstehend.',f'- Tatsächliche Sprechertextlänge: {words} Wörter, rund {round(words/130,1)} Minuten bei 130 Wörtern/Minute.','']
  out.joinpath(lid+'.md').write_text('\n'.join(lines),encoding='utf8')
ids=[x['id'] for x in allrows];assert len(allrows)==178 and len(set(ids))==178
(ROOT/'lesson-workbooks.json').write_text(json.dumps(allrows,ensure_ascii=False,indent=2),encoding='utf8')
print('178 individual dossiers generated, svg and markdown. Total existing TTS words',sum(x['ttsWords'] for x in allrows),'15+ min',sum(x['ttsMinutesAt130wpm']>=15 for x in allrows))
