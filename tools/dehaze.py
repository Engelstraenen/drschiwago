#!/usr/bin/env python3
"""Entfernt den grauen Schleier aus den Fotos der alten Seite (angehobener Schwarzpunkt).

Nichts wird erfunden: nur Tonwerte (Schwarz-/Weißpunkt), etwas Sättigung und leichte Schärfe.
Quelle: Dropbox /CLAUDE/Content/DRSCHIWAGO/original-fotos  →  Ziel: .../rundgang/<name>.jpg
Start: python3 tools/dehaze.py
"""
import os
from PIL import Image, ImageEnhance, ImageFilter

BASE = os.path.expanduser("~/Library/CloudStorage/Dropbox-FAVELAClothing/CLAUDE/Content/DRSCHIWAGO")
SRC = os.path.join(BASE, "original-fotos")
OUT = os.path.join(BASE, "rundgang")
FOTOS = ["karussell_foyer-1", "karussell_saal-1", "karussell_saal-2", "saal-tafel", "karussell_saalvibes-1", "karussell_saalvibes-2",
         "karussell_saalvibes-3", "karussell_karaoke-1", "karussell_karaoke-2", "karussell_karaoke-3", "bars_bar-saal", "bars_bar-karaoke",
         "bars_bar-terrasse", "karussell_cocktail-1", "karussell_cocktail-2", "karussell_terrasse-1", "karussell_terrasse-4",
         "karussell_terrasse-6", "karussell_terrassedunkel-1", "karussell_terrassedunkel-3", "karussell_terrassedunkel-5",
         "karussell_shisha-1", "karussell_shisha-2", "karussell_blumen-1", "karussell_blumen-2", "foto-97", "foto-101"]
os.makedirs(OUT, exist_ok=True)


def pct(hist, n, q):
    acc = 0
    for i, h in enumerate(hist):
        acc += h
        if acc >= n * q:
            return i
    return 255


for f in FOTOS:
    src = os.path.join(SRC, f + ".jpg")
    if not os.path.exists(src):
        print("fehlt:", f); continue
    im = Image.open(src).convert("RGB")
    g = im.convert("L"); hist = g.histogram(); n = sum(hist)
    lo, hi = pct(hist, n, .004), pct(hist, n, .997)
    lo = min(lo, 70); hi = max(hi, 200)
    scale = 255 / max(1, hi - lo)
    lut = [max(0, min(255, round((i - lo) * scale))) for i in range(256)]
    im = im.point(lut * 3)
    im = ImageEnhance.Color(im).enhance(1.08)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=40, threshold=2))
    name = f.replace("karussell_", "").replace("bars_", "")
    im.save(os.path.join(OUT, name + ".jpg"), quality=93)
    print(f"{name:20s} schwarz {lo:3d} → 0, weiß {hi:3d} → 255  {im.size[0]}x{im.size[1]}")
