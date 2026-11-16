# Cloud-Synchronisierung – freiwillige Einrichtung

Die Lernplattform funktioniert **vollständig lokal**, auch ohne Cloud-Konto. Die Bereitstellung eines Supabase-Servers und des Hostings kann nicht allein durch das Herunterladen der HTML-Datei erfolgen. Diese Anleitung beschreibt den Betriebsweg für v0.6.

## Schritte zur Einrichtung

1. Sichere den bisherigen Lernstand über **Einstellungen → JSON exportieren** in eine Datei ausserhalb des Browsers.
2. Erstelle ein eigenes Supabase-Projekt unter <https://supabase.com>. Prüfe die Gebühren und Datenschutzbedingungen. Wähle ein passendes Datenregion-Rechenzentrum, sofern verfügbar.
3. Öffne Supabase → SQL Editor und führe `supabase_schema.sql` aus. Das Script erstellt `public.efz_progress` und aktiviert Row Level Security (jeder angemeldete Nutzer darf nur seinen Datensatz lesen oder verändern).
4. Unter Supabase → Authentication aktiviere den gewünschten E-Mail-Login. Bei aktivierter E-Mail-Bestätigung müssen neue Benutzer den Bestätigungslink öffnen. Passe E-Mail-Redirect/Site-URL an die gehostete App an, falls nötig.
5. Unter **Project Settings → API** die **Project URL** und den **öffentlichen Publishable-Key** oder `anon`-Key kopieren. Niemals den geheimen `service_role`-Key verwenden.
6. Veröffentliche die PWA über eine feste HTTPS-Adresse (z. B. Cloudflare Pages oder GitHub Pages). Die einzelne HTML-Datei ist nur für Tests geeignet, weil lokale Browser-Origin und deren Speichergarantien unzuverlässig sein können.
7. In der App **Cloud & Geräte** öffnen, Projekt-URL und öffentlichen Key speichern. Mit E-Mail/Passwort ein Konto registrieren beziehungsweise anmelden.
8. Vor dem ersten Upload wähle bewusst **Lokalen Stand hochladen**. Auf dem zweiten Gerät mit demselben Konto anmelden, dann **Cloud übernehmen**.
9. Bei gleichzeitig bearbeiteten Ständen stoppt die App bei einem Cloud-Revisionskonflikt. Unter **Cloud & Geräte** nach Kontrolle **Cloud übernehmen**, **Lokal hochladen** oder **Zusammenführen** wählen. Ein Backup vor einer solchen Wahl ist ratsam.

## Einschränkungen

- Die Synchronisierung ist **optional** und vor der Konfiguration nicht aktiv. Sie wurde automatisiert mit einem simulierten Backend getestet; für die reale Cloud braucht es Dein eigenes Supabase-Projekt und einen anschliessenden End-to-End-Test.
- Notizen, Antworten, Lektionen, Audio-Positionen und Übungsstatus werden als Fortschritts-JSON synchronisiert. **Importierte MP3/M4A-Dateien** verbleiben aus Datenschutz- und Grössengründen lokal auf dem jeweiligen Gerät und müssen dort separat bereitgestellt werden.
- Die App speichert das Auth-Refresh-Token zur Wiederanmeldung im Browser. Verwende ein starkes Passwort und ein vertrauenswürdiges Gerät. In diesem Modell werden die Cloud-Daten nicht Ende-zu-Ende verschlüsselt.
- Die App nutzt eine Versionsprüfung; sie ist keine vollständige Echtzeit-Kollaborationsplattform. Bei längerem Offlinearbeiten und gleichzeitiger Bearbeitung mehrerer Geräte muss der Konflikt bewusst aufgelöst werden.
- Der Lernstand bleibt unabhängig von der Cloud lokal gesichert. Lokale Speicherung ist kein Ersatz für regelmässige externe JSON-Sicherungen.
- Authentifizierung, Cloud-Projekt und Webhosting erfordern eine Internetverbindung; normale Lektionen können weiterhin offline genutzt werden, sobald die PWA auf einem kompatiblen Gerät geladen wurde.
