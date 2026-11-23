# PROJEKT-MASTERFILE – DRSCHIWAGO
Gilt zusätzlich zur globalen Masterfile (~/.claude/CLAUDE.md).

## 1. Ziel und Endprodukt
Moderne neue Webseite für Dr. Schiwago (Restaurant/Samstagabend-Location in Duisburg, gehört Eugens Bruder). Inhalte von drschiwago.de übernehmen (`inhalte.md`). Ziel: Reservierungen + Geburtstage + Catering-Anfragen.

## 2. Qualitätsanspruch & Referenzen
Awwwards-Niveau, Scroll-Erlebnis, fotorealistisch. Seit V3: edel und ruhig (Schwarz, Elfenbein, Champagner-Haarlinien, Cormorant Garamond), Essen nur als einzelne Teller. Echte Räume (Onyxwand, MIRRORS, Kong Garten, Veranda) müssen erkennbar bleiben. Referenz-Collage: `konzepte/referenz-echte-raeume.jpg`.

## 3. Regeln
- Konzepte nur als Storyboard-Bild (sjinn Nano Banana 2.1, 16:9, 2K, Unlimited, 0 Credits).
- Bezahlte Läufe nur nach Eugens OK.
- Live-Domain drschiwago.de nur nach OK. Demo auf GitHub Pages (Engelstraenen).

## 4. Skills, Plugins, Agenten, MCP
| Name | wofür |
|---|---|
| claude-in-chrome | sjinn.ai |
| firecrawl | Inhalte der alten Seite |

## 5. Zugänge
- sjinn.ai (Chrome eingeloggt) ✅ · GitHub gh ✅ (prüfen) · Google-Reservierungslink vorhanden

## 6. Workflow & Freigabepunkte
1. 3 Konzept-Storyboards → Eugen wählt
2. Motive 4K + Filme (Drafts) → Freigabe
3. Bau, Prüfung Desktop/Handy, GitHub Pages
4. Übergabe an Bruder / Live-Domain nach OK

## 7. Befehle
- Fertige sjinn-Bilder laden: `tools/fetch.sh DSM-xx=<url> ...` (danach `python3 tools/assets.py`)
- Vorschau: `python3 tools/serve.py 4381` → http://localhost:4381
- Motive → WebP: `python3 tools/assets.py` (rechnet nur geänderte Bilder, Cache `tools/.assets_cache.json`; alles neu: Cache löschen)
- Prüfen: `python3 tools/check.py http://localhost:4381/ /tmp/drs-check 390x844 "hero:0,abend:.7"`
- Pflichtprüfung alle Größen: `python3 tools/check_all.py http://localhost:4381/ /tmp/drs-all`
- Doppelte Bilder prüfen (vor jeder Veröffentlichung): `python3 tools/check_dupes.py`
- Russische Seiten neu erzeugen (nach jeder Änderung an DE-Seiten): `python3 tools/assets.py && python3 tools/build_ru.py` (Texte: `i18n/ru.json`, Fehlendes: `python3 tools/i18n_extract.py`)
- Veröffentlichen: `git subtree split --prefix site -b gh-pages && git push -f origin gh-pages`

## 8. Offene Fragen
- Höher aufgelöste Originalfotos vom Bruder? (alte Seite nur ca. 760–1350 px)
- Instagram-Auto-Feed: Behold-Link vom Konto-Inhaber steht aus (Eugen 21.11.: „später“), Anleitung docs/instagram.md.
- Vor Livegang drschiwago.de: Cookie-Einwilligung für Instagram-Einbettung.
- Echter Grundriss vom Bruder/Angerhof? Dann Lageplan maßstabsgetreu. Ist der Kleine Saal das MIRRORS?
- Rundgang-Varianten `rundgang-fahrt.html` / `rundgang-tueren.html` behalten oder löschen (Eugen: „Ist gut bei Rundgang“)?
- Echte Bewertungstexte nur offiziell (Google Places API mit Schlüssel oder Widget mit Konto des Inhabers). Tripadvisor-Profil beanspruchen?

## 9. Entschieden
- 20.11.2026: Projekt angelegt, Inhalte übernommen, 3 Storyboards DSSB-1 „Eine Nacht“, DSSB-2 „Die Tafel“, DSSB-3 „Goldene Nacht“ gestartet.
- 20.11.2026: Storyboards fertig und gezeigt, Wahl offen (Empfehlung 1 „Eine Nacht“).
- 20.11.2026: Eugen wählt 3 „Goldene Nacht“. „Kong Garten“-Name unverständlich → Umbenennung offen (Empfehlung „Garten & Terrasse“).
- 20.11.2026: Demo auf GitHub Pages: engelstraenen.github.io/drschiwago/ (noindex).
- 20.11.2026: Kapitel 4 = „Die Terrasse“ (Eugen wählt Option 2, kein Gorilla, kein „Kong“). Motiv DSM-04 = echte Terrasse (Ref terrasse-1).
- 20.11.2026 (Eugen, harte Kritik V1): Essen ist das Kerngeschäft → V2: Hero = Buffet (DSM-10), Buffet-Scrollytelling mit 6 Gerichten (DSM-11a–f), horizontale Fahrt mit echten Buffet-Fotos, Zähler. Spotlight-Kapitel gestrichen („kompletter Scheiß“). Split = links TAG (DSM-02T), rechts NACHT (DSM-03). Neues Kapitel Eventlocation (Hochzeiten etc., Angebot über angerhof-duisburg.de/angebot, Samstag = Dr. Schiwago). Catering als eigene Seite `catering.html` mit allen 61 Gerichten und Buffet-Baukasten (Auswahl → mailto). Dresscode jung: „Schick. Nicht sportlich.“ (DSM-08d/e/f), keine Manschetten/Lackschuhe. Echtes Logo (gold eingefärbt, `site/assets/img/logo-gold.svg`).
- 21.11.2026: Küche = russisch, georgisch, armenisch (Eugen). Echte Fotos haben Vorrang: alle Essens-/Cocktailfotos der alten Seite + Instagram-Kapitel (@dr.schiwago_restaurant, 6 neueste Reels; Auto-Feed über Behold vorbereitet, `DRS_IG_FEED`).
- 21.11.2026: V2 gesichert (Tag v2-2026-11-21 + ZIP in versionen/). Eugen will V3 „edler, hochwertiger“: Landing Page ohne Essensfoto/nicht überladen mit Essen („wirkt billig“); Essen nur als einzelne edle Teller. Storyboards DSSB-4/5/6 gestartet.
- 21.11.2026: Eugen wählt V3 „Schwarzer Samt“ (Storyboard konzepte/5-schwarzer-samt.jpg). Gebaut und live (Tag v3-2026-11-21). V2 bleibt als Tag v2-2026-11-21 abrufbar.
- 22.11.2026: Bewertungsbereich nach Masterfile-Regel: echte Zitate raus, Google 4,6 (489) + Tripadvisor 3,0 (1, Nr. 242 von 687) bewegt, Stand 22.11.2026, Beispielkarten markiert. Trustpilot ohne Profil → weggelassen. Werte bei Updates neu nachschlagen.
- 22.11.2026 (Eugen): Bewertungen nur Google (4,6 · 489), Tripadvisor raus (3,0 aus 1 Bewertung zieht runter). Gilt hier vor der globalen Regel „Google + Tripadvisor“.
- 22.11.2026: Gerichtsbilder neu (echt + frisch, Kundenfotos als Referenz/Edit), Piroschki von der Startseite entfernt (gibt es nicht), Zähler 0→50 ersetzt durch vorbeiziehende Gerichtsnamen. Szenen: Schaschlik, Canapés, Hering, Plov, Napoleon.
- 22.11.2026 (Eugen): Piroschki bleiben im Catering-Baukasten (nur auf der Startseite/Samstagsbuffet raus).
- 22.11.2026 (Eugen): Kein Gericht doppelt auf der Seite (Bild und Name). Verteilung siehe verlauf/2026-11-22.md. Bilder im Rahmen immer im Seitenverhältnis des Rahmens erzeugen (Gericht ganz sichtbar).
- 23.11.2026 (Eugen): Rundgang durchs Haus als eigene Unterseite im Header (`rundgang.html`), echte Fotos der alten Seite ohne grauen Nebel-Filter (`tools/dehaze.py`).
- 23.11.2026 (Eugen): Seite zweisprachig Deutsch/Russisch mit Umschalter im Header (`site/ru/`, erzeugt per `tools/build_ru.py`).
- 23.11.2026 (Eugen): „Tisch reservieren“ überall blutrot gefüllt (`.line-btn--blood`, #9a0c12).
- 23.11.2026 (Eugen): Garten aus dem Rundgang entfernt (die Terrasse ist der Garten).
- 23.11.2026 (Eugen): „Feier anfragen“ führt auf `anfrage.html` = Kopie von angerhof-duisburg.de/angebot (5 Schritte: Anlass, Gäste, Termin mit gesperrten Samstagen, Wünsche, Kontakt), für alle Anlässe (`?anlass=`), im Angerhof-Look mit Angerhof-Logo oben links. Versand per E-Mail-Programm an kontakt@angerhof-restaurant.de.
- 23.11.2026 (Eugen): Lageplan im Rundgang (wichtig für Firmenfeiern), Eingang rechts am Foyer (Eugen-Korrektur), schematisch, Flächen/Gäste laut angerhof-duisburg.de: Großer Saal 260 m² bis 200, Terrasse ca. 150 m² bis 100, Foyer & Lounge ca. 100 m² mit Bar, Kleiner Saal ca. 70 m² bis 50 (= MIRRORS, Annahme). Bereiche kombinierbar (Flächensumme).

## 10. Ablage
- Code: Dropbox /CLAUDE/Projekte/DRSCHIWAGO
- Medien: Dropbox /CLAUDE/Content/DRSCHIWAGO
