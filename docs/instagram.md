# Instagram auf der Seite – automatisch neue Videos

Stand 21.11.2026. Jetzt zeigt die Seite die 6 neuesten Reels von @dr.schiwago_restaurant per offizieller Instagram-Einbettung.
Damit neue Videos **von selbst** erscheinen, braucht die Seite einen Feed-Link. Den kann nur der Inhaber des Instagram-Kontos anlegen (einmalig, ca. 3 Minuten).

## Anleitung für den Konto-Inhaber
1. Am Computer **behold.so** öffnen und auf **Sign up** klicken (kostenlos, Konto mit E-Mail anlegen).
2. **Connect Instagram account** klicken und mit dem Konto **dr.schiwago_restaurant** anmelden. Passwort selbst eintippen.
3. **Add feed** klicken, als Typ **JSON** wählen, speichern.
4. Den angezeigten Feed-Link kopieren (beginnt mit `https://feeds.behold.so/`) und an Claude schicken.

## Was Claude danach macht
- Link in `site/index.html` bei `window.DRS_IG_FEED = "…"` eintragen.
- Die Seite lädt dann die neuesten Beiträge selbst, Videos laufen stumm im Bild, Klick öffnet den Beitrag bei Instagram.
- Ohne Link (oder wenn Behold nicht erreichbar ist) zeigt die Seite automatisch wieder die offizielle Einbettung.

## Vor dem Livegang auf drschiwago.de
- Instagram-Inhalte übertragen Daten an Meta. Die Seite braucht dafür eine Einwilligung im Cookie-Banner (wie die alte Seite es für Google Maps macht).
