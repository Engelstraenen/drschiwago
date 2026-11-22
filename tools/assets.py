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
    "DSM-53a": "gang-vorspeisen", "DSM-53b": "gang-salate", "DSM-53c": "gang-haupt", "DSM-53d": "gang-beilagen", "DSM-53e": "gang-dessert",
    "DSM-22": "hochzeit", "DSM-23": "veranda",
}
FOTOS = {f"buffet-{i}": f"foto-buffet-{i}" for i in range(1, 8)}
FOTOS.update({"karussell_buffet-01": "foto-salat", "karussell_buffet-03": "foto-canapes", "karussell_cocktail-1": "foto-cocktail-1", "karussell_cocktail-3": "foto-cocktail-3"})

os.makedirs(OUT, exist_ok=True)
stamp = str(int(time.time()))
data = {}


def build(src, name, big, small):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    entry = {"w": w, "h": h}
    for tag, tw in (("l", big), ("s", small)):
        tw = min(tw, w)  # nie hochskalieren
        th = round(h * tw / w)
        path = os.path.join(OUT, f"{name}-{tag}.webp")
        im.resize((tw, th), Image.LANCZOS).save(path, "WEBP", quality=80 if tag == "l" else 76, method=6)
        entry[tag] = f"assets/img/{name}-{tag}.webp?v={stamp}"
        entry[tag + "w"] = tw
    print(f"{name}: {entry['lw']}/{entry['sw']} px")
    data[name] = entry


# Fallback, solange ein neues Motiv noch rendert (altes Motiv bleibt sichtbar, keine Lücke)
FALLBACK = {"DSM-41": "DSM-31", "DSM-44": "DSM-34", "DSM-45": "DSM-35", "DSM-37": "DSM-12"}
find = lambda i: next((os.path.join(BASE, "motive", i + e) for e in (".jpg", ".png") if os.path.exists(os.path.join(BASE, "motive", i + e))), None)
for sid, name in MOTIVE.items():
    src = find(sid) or (find(FALLBACK[sid]) if sid in FALLBACK else None)
    if src:
        w, h = Image.open(src).size
        build(src, name, (2400 if w == h else 3840) if w >= h else 1800, (1200 if w == h else 1800) if w >= h else 900)
for sid, name in FOTOS.items():
    src = os.path.join(BASE, "original-fotos", sid + ".jpg")
    if os.path.exists(src):
        build(src, name, 1800, 900)

# alte, nicht mehr genutzte WebP entfernen (nur erzeugte Dateien)
for f in glob.glob(os.path.join(OUT, "*-[ls].webp")):
    if os.path.basename(f).rsplit("-", 1)[0] not in data:
        os.remove(f)
        print("entfernt:", os.path.basename(f))

with open(JS, "w") as f:
    f.write("window.IMG = " + json.dumps(data, indent=1) + ";\n")
print("img.js:", len(data), "Bilder")
