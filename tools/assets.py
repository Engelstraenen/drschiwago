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
    "DSM-11a": "gericht-schaschlik", "DSM-11b": "gericht-piroschki", "DSM-11c": "gericht-canapes",
    "DSM-11d": "gericht-hering", "DSM-11e": "gericht-plov", "DSM-11f": "gericht-napoleon",
    "DSM-12": "catering",
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


for sid, name in MOTIVE.items():
    src = next((os.path.join(BASE, "motive", sid + e) for e in (".jpg", ".png") if os.path.exists(os.path.join(BASE, "motive", sid + e))), None)
    if src:
        w, h = Image.open(src).size
        build(src, name, 3840 if w >= h else 1800, 1800 if w >= h else 900)
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
