#!/usr/bin/env python3
"""Lesbarkeit der Navigation über dem Startbild messen (helle Leuchter hinter heller Schrift).

Start: python3 tools/nav_check.py <name> [url]   → konzepte/nav-vorschau/<name>-<breite>.jpg + Helligkeit
Gemessen wird die Helligkeit des Hintergrunds hinter den Menüpunkten (Mittel und 90-%-Wert, 0–255).
Gut lesbar ist helle Schrift, wenn der 90-%-Wert deutlich unter ~110 liegt.
"""
import os
import sys
from io import BytesIO

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
name = sys.argv[1] if len(sys.argv) > 1 else 'test'
base = sys.argv[2] if len(sys.argv) > 2 else 'http://localhost:4381/'
out = os.path.join(HERE, 'konzepte', 'nav-vorschau'); os.makedirs(out, exist_ok=True)
VIEWS = [(1920, 1000), (1600, 900), (1440, 900), (1366, 768), (390, 844)]
with sync_playwright() as p:
    b = p.chromium.launch()
    for page in ['index.html', 'ru/index.html']:
        for (w, h) in VIEWS:
            mob = w < 900
            ctx = b.new_context(viewport={'width': w, 'height': h}, is_mobile=mob, has_touch=mob)
            pg = ctx.new_page(); pg.goto(base + page, wait_until='networkidle'); pg.wait_for_timeout(2600)
            boxes = pg.evaluate("""() => [...document.querySelectorAll('.nav__links a, .nav__burger, .nav__lang')].filter(e => e.offsetWidth > 0)
                .map(e => { const r = e.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom]; })""")
            # Hintergrund ohne Schrift: Menütexte kurz unsichtbar machen
            pg.add_style_tag(content='.nav__links a, .nav__lang, .nav__burger span { color: transparent !important; border-color: transparent !important; background: transparent !important; text-shadow: none !important; }')
            pg.wait_for_timeout(200)
            bg = Image.open(BytesIO(pg.screenshot())).convert('L')
            vals = []
            for (l, t, r, bt) in boxes:
                vals += list(bg.crop((int(l), int(t), int(r), int(bt))).getdata())
            vals.sort()
            mean = sum(vals) / len(vals) if vals else 0
            p90 = vals[int(len(vals) * .9)] if vals else 0
            pg.evaluate("document.querySelectorAll('style').forEach(s => { if (s.textContent.includes('color: transparent !important')) s.remove(); })")
            pg.wait_for_timeout(200)
            tag = page.replace('/', '-').replace('.html', '')
            if page == 'index.html' or w == 1920:
                Image.open(BytesIO(pg.screenshot(clip={'x': 0, 'y': 0, 'width': w, 'height': min(h, 260 if not mob else 420)}))).convert('RGB').save(os.path.join(out, f'{name}-{tag}-{w}.jpg'), quality=82)
            print(f'{page} {w}x{h}: hintergrund mittel {mean:.0f} · 90% {p90}')
            ctx.close()
    b.close()
