#!/usr/bin/env python3
"""Motive + echte Fotos -> WebP für die Seite + assets/js/img.js.

Motive (4K, sjinn): Dropbox /CLAUDE/Content/DRSCHIWAGO/motive/DSM-xx.(jpg|png) -> <name>-l.webp (3840 / Hochformat 1800) + -s.webp (1800 / 900)
Echte Fotos (alte Seite): Dropbox /CLAUDE/Content/DRSCHIWAGO/original-fotos -> nie hochskaliert, max. 1800 / 900
Start: python3 tools/assets.py
"""
import glob
import json
import os
import time
from PIL import Image

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.expanduser("~/Library/CloudStorage/Dropbox-FAVELAClothing/CLAUDE/Content/DRSCHIWAGO")
OUT = os.path.join(HERE, "site", "assets", "img")
JS = os.path.join(HERE, "site", "assets", "js", "img.js")

MOTIVE = {
    "DSM-01": "kronleuchter", "DSM-01m": "kronleuchter-m",
    "DSM-02": "saal-abend", "DSM-02T": "saal-tag", "DSM-03": "saal-nacht", "DSM-04": "terrasse",
    "DSM-05a": "bar-terrasse", "DSM-05b": "bar-saal", "DSM-05c": "bar-karaoke",
    "DSM-06": "mikro", "DSM-07": "textur",
    "DSM-08d": "dress-herr", "DSM-08e": "dress-dame", "DSM-08f": "dress-schuhe",
    "DSM-10": "essen", "DSM-10m": "essen-m",
    "DSM-41": "gericht-schaschlik", "DSM-32": "gericht-canapes", "DSM-33": "gericht-hering",
    "DSM-44": "gericht-plov", "DSM-45": "gericht-napoleon",
    "DSM-37": "catering",
    "DSM-20": "saal-kronleuchter", "DSM-20m": "saal-kronleuchter-m",
    "DSM-51a": "karte-grill", "DSM-51b": "karte-vorspeisen", "DSM-51c": "karte-salate", "DSM-51d": "karte-haupt", "DSM-51e": "karte-dessert",
    "DSM-52a": "teller-stroganoff", "DSM-52b": "teller-olivier", "DSM-52c": "teller-forelle",
    "DSM-54": "tafel", "DSM-54m": "tafel-m",
    "DSM-55a": "karte-grill-2", "DSM-55b": "karte-vorspeisen-2", "DSM-55c": "karte-salate-2", "DSM-55d": "karte-haupt-2", "DSM-55e": "karte-dessert-2",
    "DSM-56a": "event-geburtstag", "DSM-56b": "event-firma", "DSM-56c": "event-familie", "DSM-58": "catering-bg", "DSM-58m": "catering-bg-m",
    "DSM-53a": "gang-vorspeisen", "DSM-53b": "gang-salate", "DSM-53c": "gang-haupt", "DSM-53d": "gang-beilagen", "DSM-53e": "gang-dessert",
    "DSM-22": "hochzeit", "DSM-23": "veranda",
    "DSM-60": "tuer", "DSM-60m": "tuer-m",
    "DSM-61a": "rg4k-foyer", "DSM-61b": "rg4k-saal", "DSM-61c": "rg4k-nacht", "DSM-61d": "rg4k-mirrors", "DSM-61e": "rg4k-bar", "DSM-61g": "rg4k-terrasse",
}
FOTOS = {f"buffet-{i}": f"foto-buffet-{i}" for i in range(1, 8)}
FOTOS.update({"karussell_buffet-01": "foto-salat", "karussell_buffet-03": "foto-canapes", "karussell_cocktail-1": "foto-cocktail-1", "karussell_cocktail-3": "foto-cocktail-3"})

os.makedirs(OUT, exist_ok=True)
stamp = str(int(time.time()))
data = {}


CACHE_F = os.path.join(HERE, "tools", ".assets_cache.json")
try:
    CACHE = json.load(open(CACHE_F))
except Exception:
    CACHE = {}


def build(src, name, big, small):
    """WebP l/s erzeugen. Unverändert (gleiche Quelle, gleiche Zeit, gleiche Größen) → nichts neu rechnen und
    die Quelle nicht einmal öffnen (Dropbox lädt sonst jede ausgelagerte 4K-Datei neu herunter)."""
    key = [src, os.path.getmtime(src), big, small]
    paths = {t: os.path.join(OUT, f"{name}-{t}.webp") for t in ("l", "s")}
    have = all(os.path.exists(x) and os.path.getsize(x) > 0 for x in paths.values())
    old = CACHE.get(name)
    fresh = have and old is not None and old[:4] == key and len(old) == 6
    if fresh:
        w, h = old[4], old[5]
        im = None
    else:
        im = Image.open(src).convert("RGB")
        w, h = im.size
        if have and os.environ.get("ASSETS_SEED"):
            im = None  # nur Größe merken, Dateien sind schon da
    entry = {"w": w, "h": h}
    for tag, tw in (("l", big), ("s", small)):
        tw = min(tw, w)  # nie hochskalieren
        th = round(h * tw / w)
        if im is not None:
            im.resize((tw, th), Image.LANCZOS).save(paths[tag], "WEBP", quality=80 if tag == "l" else 76, method=6)
        entry[tag] = f"assets/img/{name}-{tag}.webp?v={stamp}"
        entry[tag + "w"] = tw
    CACHE[name] = key + [w, h]
    print(f"{name}: {entry['lw']}/{entry['sw']} px" + ("" if fresh else " (neu)"))
    data[name] = entry


# Fallback, solange ein neues Motiv noch rendert (altes Motiv bleibt sichtbar, keine Lücke)
FALLBACK = {"DSM-41": "DSM-31", "DSM-44": "DSM-34", "DSM-45": "DSM-35", "DSM-37": "DSM-12"}
find = lambda i: next((os.path.join(BASE, "motive", i + e) for e in (".jpg", ".png") if os.path.exists(os.path.join(BASE, "motive", i + e))), None)
for sid, name in MOTIVE.items():
    src = find(sid) or (find(FALLBACK[sid]) if sid in FALLBACK else None)
    if src:
        c = CACHE.get(name)
        w, h = (c[4], c[5]) if c and len(c) == 6 and c[0] == src and c[1] == os.path.getmtime(src) else Image.open(src).size
        build(src, name, (2400 if w == h else 3840) if w >= h else 1800, (1200 if w == h else 1800) if w >= h else 900)
for sid, name in FOTOS.items():
    src = os.path.join(BASE, "original-fotos", sid + ".jpg")
    if os.path.exists(src):
        build(src, name, 1800, 900)
# Rundgang: echte Fotos der alten Seite, Schleier entfernt (tools/dehaze.py), nie hochskaliert
RG = os.path.join(BASE, "rundgang")
if os.path.isdir(RG):
    for f in sorted(os.listdir(RG)):
        if f.endswith(".jpg"):
            build(os.path.join(RG, f), "rg-" + f[:-4], 1800, 900)

# alte, nicht mehr genutzte WebP entfernen (nur erzeugte Dateien)
for f in glob.glob(os.path.join(OUT, "*-[ls].webp")):
    if os.path.basename(f).rsplit("-", 1)[0] not in data:
        os.remove(f)
        print("entfernt:", os.path.basename(f))

json.dump(CACHE, open(CACHE_F, "w"))
with open(JS, "w") as f:
    f.write("window.IMG = " + json.dumps(data, indent=1) + ";\n")
print("img.js:", len(data), "Bilder")

# Cache-Busting: CSS/JS-Links in den HTML-Seiten bekommen bei jedem Lauf eine neue Version,
# damit Browser nie alte Dateien mit neuem HTML mischen (Eugen 22.11.: „Seite scheint kaputt“)
import re as _re
for _page in ("index.html", "catering.html", "rundgang.html", "rundgang-fahrt.html", "rundgang-tueren.html", "anfrage.html"):
    _p = os.path.join(HERE, "site", _page)
    _s = open(_p).read()
    _s = _re.sub(r'(assets/(?:css|js)/[a-z]+\.(?:css|js))(\?v=\d+)?"', lambda m: f'{m.group(1)}?v={stamp}"', _s)
    _s = _re.sub(r'(assets/img/[a-z0-9-]+\.webp)(\?v=\d+)?(?=[" ,])', lambda m: f'{m.group(1)}?v={stamp}', _s)
    open(_p, "w").write(_s)
print("Versionsnummer in HTML:", stamp)
