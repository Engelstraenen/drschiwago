# PROJEKT-MASTERFILE – DRSCHIWAGO
Gilt zusätzlich zur globalen Masterfile (~/.claude/CLAUDE.md).

## 1. Ziel und Endprodukt
Moderne neue Webseite für Dr. Schiwago (Restaurant/Samstagabend-Location in Duisburg, gehört Eugens Bruder). Inhalte von drschiwago.de übernehmen (`inhalte.md`). Ziel: Reservierungen + Geburtstage + Catering-Anfragen.

## 2. Qualitätsanspruch & Referenzen
Awwwards-Niveau, Scroll-Erlebnis, fotorealistisch. Echte Räume (Onyxwand, MIRRORS, Kong Garten, Veranda) müssen erkennbar bleiben. Referenz-Collage: `konzepte/referenz-echte-raeume.jpg`.

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
- Vorschau: `python3 tools/serve.py 4381` → http://localhost:4381
- Motive → WebP: `python3 tools/assets.py`
- Prüfen: `python3 tools/check.py http://localhost:4381/ /tmp/drs-check 390x844 "hero:0,abend:.7"`
- Veröffentlichen: `git subtree split --prefix site -b gh-pages && git push -f origin gh-pages`

## 8. Offene Fragen
- Höher aufgelöste Originalfotos vom Bruder? (alte Seite nur ca. 760–1350 px)
- Russische Sprachversion gewünscht?

## 9. Entschieden
- 20.11.2026: Projekt angelegt, Inhalte übernommen, 3 Storyboards DSSB-1 „Eine Nacht“, DSSB-2 „Die Tafel“, DSSB-3 „Goldene Nacht“ gestartet.
- 20.11.2026: Storyboards fertig und gezeigt, Wahl offen (Empfehlung 1 „Eine Nacht“).
- 20.11.2026: Eugen wählt 3 „Goldene Nacht“. „Kong Garten“-Name unverständlich → Umbenennung offen (Empfehlung „Garten & Terrasse“).
- 20.11.2026: Demo auf GitHub Pages: engelstraenen.github.io/drschiwago/ (noindex).

## 10. Ablage
- Code: Dropbox /CLAUDE/Projekte/DRSCHIWAGO
- Medien: Dropbox /CLAUDE/Content/DRSCHIWAGO
