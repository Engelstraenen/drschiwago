#!/usr/bin/env python3
"""4K-Motive -> WebP für die Seite + assets/js/img.js.

Quelle: Dropbox /CLAUDE/Content/DRSCHIWAGO/motive/DSM-xx.(jpg|png)
Ziel:   site/assets/img/<name>-l.webp (groß) und <name>-s.webp (Handy)
Start:  python3 tools/assets.py
"""
import json
import os
import time
from PIL import Image

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.expanduser("~/Library/CloudStorage/Dropbox-FAVELAClothing/CLAUDE/Content/DRSCHIWAGO/motive")
OUT = os.path.join(HERE, "site", "assets", "img")
JS = os.path.join(HERE, "site", "assets", "js", "img.js")

MAP = {
    "DSM-01": "hero", "DSM-01m": "hero-m", "DSM-02": "saal-abend", "DSM-03": "saal-nacht", "DSM-04": "garten",
    "DSM-05a": "bar-terrasse", "DSM-05b": "bar-saal", "DSM-05c": "bar-karaoke",
    "DSM-06": "mikro", "DSM-07": "textur",
    "DSM-08a": "dress-manschette", "DSM-08b": "dress-schuhe", "DSM-08c": "dress-glaeser",
}

os.makedirs(OUT, exist_ok=True)
stamp = str(int(time.time()))
data = {}
for sid, name in MAP.items():
    src = next((os.path.join(SRC, sid + e) for e in (".jpg", ".png") if os.path.exists(os.path.join(SRC, sid + e))), None)
    if not src:
        continue
    im = Image.open(src).convert("RGB")
    w, h = im.size
    landscape = w >= h
    big = 3840 if landscape else 1800   # Breite
    small = 1800 if landscape else 900
    entry = {"w": w, "h": h}
    for tag, tw in (("l", big), ("s", small)):
        tw = min(tw, w)
        th = round(h * tw / w)
        path = os.path.join(OUT, f"{name}-{tag}.webp")
        im.resize((tw, th), Image.LANCZOS).save(path, "WEBP", quality=80 if tag == "l" else 76, method=6)
        entry[tag] = f"assets/img/{name}-{tag}.webp?v={stamp}"
        entry[tag + "w"] = tw
        print(f"{name}-{tag}.webp {tw}x{th} {os.path.getsize(path)//1024} KB")
    data[name] = entry

with open(JS, "w") as f:
    f.write("window.IMG = " + json.dumps(data, indent=1) + ";\n")
print("img.js:", ", ".join(data))
