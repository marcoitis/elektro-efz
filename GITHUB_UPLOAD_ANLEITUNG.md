# GitHub-Upload – vollständige Schritt-für-Schritt-Anleitung (v0.11.8)

**Ziel:** Die komplette Lernplattform als GitHub-Repository sichern und
kostenfrei über GitHub Pages bereitstellen. Die Website enthält zunächst **alle
178 Textlektionen, Bilder, Übungen und Quizfragen – aber keine vorproduzierten
MP3-Audioaufnahmen**. Damit bleibt die Sprachproduktion kontrollierbar.

## A. Was bereits vorbereitet ist

Die Datei `Elektro_EFZ_GitHub_Ready_v0.11.8.zip` enthält:

- Die ganze Anwendung mit `index.html`, CSS, JavaScript, 178 Lernbildern,
  178 Sprechskripten, Unterrichtsmappen und Qualitätsdaten.
- `.github/workflows/publish.yml`: automatischer Text-/Offline-Build mit Tests.
- `.github/workflows/check-pull-request.yml`: Prüfung vorgeschlagener Änderungen.
- `.gitignore`: verhindert die versehentliche Übernahme von Stimme-Modellen,
  Rohaufnahmen, Geheimnissen, Cache-Dateien und generierten `dist`-Dateien.
- `tools/build_site.py`: erstellt die GitHub-Pages-Fassung ohne Audiozwang.
- `audio-plan/batches.csv`: 178 Zeilen mit Skriptprüfsummen und Chargennummer.
- `AUDIO_MEHRSTUFENPLAN.md`: Ausspracheprobe, Kleinstserie, Freigabe und Rollout.

**Ein wichtiger behobener Fehler:** Die Offline-Navigation bedient nun auch
`vertiefung-151.html` und `fachvertiefung-151.html` korrekt. Zuvor führte die
Service-Worker-Navigation bei diesen Seiten fälschlich zu `index.html`.

## B. Vor der Veröffentlichung – ca. zehn Kontrollpunkte

1. Prüfe, ob das Repository öffentlich werden darf. GitHub Pages ist eine
   öffentlich erreichbare Website; ein privates Repository schützt nicht
   automatisch die veröffentlichte Seite.
2. Lies `VOR_VERÖFFENTLICHUNG_PRÜFEN.md`. Entferne alle urheberrechtlich
   geschützten Normen-PDFs, Lizenzmaterialien, Kundendaten und Zugangsschlüssel.
3. Starte die bestehende App auf dem iPhone und exportiere bei **Einstellungen
   → Datensicherung** den bisherigen Lernstand als JSON. Sichere die Datei in
   Dateien/iCloud Drive oder auf dem PC, nicht nur im Browser.
4. Stelle sicher, dass eine neue Version von `index.html` mit der vorhandenen
   URL veröffentlicht wird. Ein Wechsel von Repository-Namen, Benutzername
   oder Domain führt zu einer **anderen Browser-Storage-Origin**. Der bisherige
   Fortschritt zieht dann nicht automatisch mit um.
5. Falls du schon eine GitHub-Pages-Adresse nutzt, notiere sie und verwende
   möglichst wieder **dieselbe Repository-Adresse**. In alten Projektunterlagen
   steht `marcoitis/elektro-efz`; verifiziere bitte selbst, ob das noch dein
   aktuelles Repository ist.

## C. Einfachster Upload mit GitHub Desktop (Windows)

1. Öffne **https://desktop.github.com/** und installiere GitHub Desktop.
2. Starte GitHub Desktop und melde dich mit deinem GitHub-Konto an.
3. Öffne **File → Clone repository**, wähle dein bestehendes Repository (oder
   erstelle auf **https://github.com/new** eines) und wähle einen lokalen Ordner.
4. Entpacke das **GitHub-Ready-ZIP** vollständig in einen temporären Ordner.
5. Öffne den geklonten Repository-Ordner im Windows-Explorer (**Repository →
   Show in Explorer**). Kopiere **den Inhalt** des entpackten GitHub-Ready-Ordners
   hinein, **nicht den übergeordneten ZIP-Ordner**. Vorhandene Projektdateien
   überschreiben. **Das versteckte Verzeichnis `.git` des geklonten Repositorys
   niemals löschen oder ersetzen.**
6. Kopiere auch das Verzeichnis **`.github`** mit seinen Workflows. In Windows
   ggf. **Ansicht → Einblenden → Ausgeblendete Elemente** aktivieren.
7. Kontrolliere in GitHub Desktop die geänderten Dateien. Erwartet sind u. a.
   `index.html`, `app.js`, `sw.js`, `offline.js`, `tools/build_site.py`,
   `tts_scripts/`, `visuals/` und `.github/workflows/publish.yml`.
8. **Nicht hochladen:** `dist/`, `.voice-cache/`, `.audio-cache/`,
   `audio-review/`, eigene API-Schlüssel, Normen-PDFs, lokale MP3-Rohfassungen.
9. Commit-Nachricht, zum Beispiel:
   `v0.11.8 – 178 Langmanuskripte und textbasierter GitHub-Pages-Build`.
10. **Commit to main** klicken, danach **Push origin**.

**Neues Repository:** Beim Erstellen darf zunächst „Private“ gewählt werden,
solange Quellenrechte oder Inhalte noch geklärt werden. Die spätere öffentliche
Pages-Verfügbarkeit hängt von den gewählten GitHub-Einstellungen und deinem
Plan ab. Veröffentliche nur freigegebene Inhalte.

## D. GitHub Pages aktivieren

1. Im Browser das Repository auf **github.com** öffnen.
2. **Settings → Pages** öffnen.
3. Unter **Build and deployment → Source** die Option **GitHub Actions** wählen.
4. Im Tab **Actions** den Workflow **Elektro EFZ – GitHub Pages (Text, Folien,
   PWA)** suchen. Bei einem Push auf `main` startet er automatisch; sonst
   **Run workflow → Branch: main → Run workflow**.
5. Nach grünem Durchlauf **Settings → Pages → Visit site** anklicken.
6. Bei einem Projekt-Repository sollte die URL ungefähr so aussehen:

   `https://BENUTZERNAME.github.io/REPOSITORY/`

   Für das in älteren Projektdateien genannte Repository wäre es **nur falls
   unverändert** `https://marcoitis.github.io/elektro-efz/`.

Die GitHub-Aktion prüft die Lektionen, baut ein ca. **15 MB** grosses statisches
Textpaket und veröffentlicht es über HTTPS. Sie startet **keine Piper-Stimme**,
lädt **kein Sprachmodell** herunter und erzeugt **keine 178 MP3s**. Bei einem
neuen Commit wird die Website mit demselben Ablauf aktualisiert. Der
Build erzeugt automatisch eine zur App-Version passende Cachekennung;
im iPhone-Offlinemodus muss das neue Paket nach dem Update trotzdem erst
vollständig geladen werden.

**GitHub-Dokumentation:**
- https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
- https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits

## E. Lokale technische Prüfung vor dem Push (optional, empfohlen)

Windows: Python 3.11 installieren und im Terminal **im Repository-Ordner**:

```powershell
py -3.11 tools/check_github_release.py
py -3.11 tools/quality_check.py
py -3.11 tools/quality_check_multimedia.py
py -3.11 tools/validate_v0118.py
py -3.11 tools/build_site.py --mode text
py -3.11 tools/verify_pages_package.py --site dist
py -3.11 -m http.server 8000 --directory dist
```

Dann `http://localhost:8000/` im Browser aufrufen. Bei fehlendem Python
brauchst du diese Prüfung nicht selbst zu starten: GitHub Actions führt die
relevanten Tests beim Upload aus und zeigt Fehler im Protokoll an.

`dist/` ist nur das erzeugte Website-Paket. Der Quellcode bleibt im Repository.
Die Datei `audio-manifest.json` enthält initial **0 MP3-Dateien**. Die App
kann weiterhin den Geräte-Sprachdienst verwenden und manuell importierte
Audios lokal in IndexedDB speichern.

## F. Funktionsprüfung nach Veröffentlichung

**PC oder Mac:**
1. Startseite öffnen; Module, Unterrichtsmappen und Lernbilder aufrufen.
2. `kurskompass.html`, `vertiefung-151.html` und
   `fachvertiefung-151.html` über die Navigation öffnen.
3. Prüfen, ob ein Kapitel, eine Quizfrage und die gespeicherte Position
   funktionieren. Ein Browser-Neuladen darf keine 404-Fehler erzeugen.
4. Unter **Offline & Audio** den vollständigen Textbestand herunterladen
   beziehungsweise Offline-Status prüfen.
5. Den Browser kurz offline schalten und Seiten erneut öffnen.

**iPhone / iPad:**
1. Die HTTPS-Adresse **in Safari** öffnen, nicht in einem In-App-Browser.
2. **Teilen → Zum Home-Bildschirm** und die App starten.
3. In der App **Offline & Audio** das Lernpaket laden und verifizieren.
4. iPhone in den Flugmodus setzen; danach die App neu öffnen.
5. Startseite, eine bereits geladene Lektion, Grafiken, Quiz und
   die drei weiteren Unterrichtsseiten kontrollieren.
6. Lernfortschritt testweise ändern und nach dem Neustart prüfen.
7. Die Gerätestimme und optional importierte Test-MP3s separat prüfen.
8. Für wichtige Daten zusätzlich **JSON-Backup** herunterladen.

Achtung: Safari kann Websitespeicher bei Platzmangel bereinigen. Ein
Home-Bildschirm-Icon ist kein garantiertes Langzeitbackup. Audiospeicher und
Lernfortschritt sollten auf einem echten iPhone unter Flugmodus validiert werden.

## G. Audio später in kleinen Schlaufen hinzufügen

Der Workflow bleibt anfangs auf `python tools/build_site.py --mode text`.
Sobald nach Abnahme drei echte Pilot-MP3s vorhanden sind, gibt es zwei Wege:

**Kleiner Pilot direkt über GitHub Pages:**
1. Die freigegebenen Dateien exakt `1.01-A.mp3`, `2.05-B.mp3` und
   `N-P02.mp3` nennen.
2. Bewusst in `public-audio/` kopieren und mit Git committen. Diese Dateien
   sind die einzige freigegebene MP3-Ausnahme in der `.gitignore`.
3. `python tools/verify_audio_approved.py --directory public-audio` testen.
4. Im Workflow `.github/workflows/publish.yml` den Build-Befehl auf
   `python tools/build_site.py --mode partial` ändern und pushen.
5. Die Website erhält eine passende `audio-manifest.json` und bietet die drei
   Dateien im Audio-Bereich zum **expliziten Offline-Download** an.
6. Nach einem iPhone-Pilot den Kurs nicht vorschnell auf 178 MP3s erweitern.

**Grosser Rollout über getrennten HTTPS-Speicher:**
1. Freigegebene Audio-Dateien auf einen dafür geeigneten Object Storage/CDN
   mit öffentlichen HTTPS-Links laden. Dateinamen behalten.
2. CORS muss die GitHub-Pages-Origin für `GET` und `HEAD` zulassen,
   `Content-Type` muss korrekt `audio/mpeg` sein.
3. In `audio-manifest.json` die Felder `baseUrl` (HTTPS-Verzeichnis)
   sowie `tracks` (ID → z. B. `1.01-A.mp3`) ergänzen.
4. Erst nach geprüftem Zugriff im Pages-Workflow `--mode remote` setzen.
5. Ein iPhone lädt ein Audiopaket bewusst via App herunter. Die MP3s bleiben
   nicht Teil des allgemeinen Service-Worker-Textpakets.

**Warum getrennt?** Die 178 Skripte umfassen rechnerisch ca. **47,8 Stunden
Audio**. Bei 64 kbit/s Mono sind das grob **1,38 GB MP3-Daten** – mehr als
für eine GitHub-Pages-Website sinnvoll und über der 1-GB-Seitengrenze.
Details und Freigabeformular: `AUDIO_MEHRSTUFENPLAN.md`.

## H. Updates und Fehlerbehebung

| Beobachtung | Vorgehen |
|---|---|
| Actions-Lauf rot | Actions → letzten Lauf → roten Schritt öffnen; Log sichern. Keine MP3-Produktion nötig. |
| 404 unter `/REPOSITORY/` | Pages-Quelle `GitHub Actions`, Branch `main`, Dateiname `index.html`, grünen Deploy-Lauf prüfen. |
| Alte Website-Version | App neu laden, im Offline-Zentrum Update prüfen, ggf. App neu öffnen. Lernstand vorher sichern. |
| Zusatzseite zeigt Startseite | Prüfen, ob aktualisiertes `sw.js` deployt wurde; Update bestätigen. |
| Offline-Seiten fehlen | Online Offline-Download vollständig durchlaufen lassen; Speicherstatus prüfen. |
| Keine Audio-Dateien angezeigt | Beim ersten Deploy korrekt: Manifest enthält 0 Tracks. Es gibt Gerätestimme und manuellen Import. |
| Pilot-MP3 wird nicht heruntergeladen | Schreibweise der Lektions-ID, `audio-manifest.json`, HTTPS, CORS und Dateityp prüfen. |
| Lernfortschritt nach URL-Wechsel weg | Alte JSON-Sicherung auf der neuen URL wieder importieren. |
| Im GitHub-Commit fehlen `.github`-Dateien | Explorer-Ansicht versteckter Dateien prüfen und erneut kopieren. |
| GitHub weigert sich wegen grosser Dateien | MP3s und Sprachmodelle nicht in Git; Audio in Chargen oder auf externem Storage ablegen. |

## I. Git ohne GitHub Desktop (optional)

Nur falls ein neues/leer geklontes Repository bereits vorhanden ist, im
Terminal dort die GitHub-Ready-Dateien hineinkopieren und:

```bash
git status
git add -A
git diff --cached --stat
git commit -m "v0.11.8: GitHub Pages text-first + Audio-Chargenplan"
git push origin main
```

Bei einem schon benutzten Repository **nicht** mit `git init` oder
`git push --force` experimentieren. Vorhandene Historie und `.git` erhalten.

## J. Fachliche Freigabe ist ein eigener Arbeitsschritt

Der erfolgreiche GitHub-Build bestätigt Dateistruktur, Wortanzahl und
JS-/SVG-Konsistenz. Er bestätigt **keine Normkonformität**. NIN 2025, NIV,
ESTI-Weisungen, Werkvorschriften sowie alle sicherheitsrelevanten Rechnungen
und Pläne müssen separat anhand der verbindlichen Quellen überprüft werden.
Auch die 178 Grafiken sind keine automatisch freigegebenen Bau-/Installationspläne.
