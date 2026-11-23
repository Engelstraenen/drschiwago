#!/usr/bin/env python3
"""Screenshots der Rundgang-Varianten an festen Scroll-Ständen (für den Vergleich mit den Storyboards).

Start: python3 tools/rgv_shots.py <ausgabeordner> [url] [breitexhöhe ...]
Legt je Variante einen Kontaktbogen an: <ausgabe>/fahrt-<w>x<h>.jpg und tueren-<w>x<h>.jpg
"""
import os
import sys
from io import BytesIO

from PIL import Image
from playwright.sync_api import sync_playwright

out = sys.argv[1] if len(sys.argv) > 1 else '/tmp/rgv'
base = sys.argv[2] if len(sys.argv) > 2 else 'http://localhost:4381/'
views = [tuple(map(int, v.split('x'))) for v in sys.argv[3:]] or [(1440, 900), (390, 844)]
os.makedirs(out, exist_ok=True)
PLAN = {
    'fahrt': ('rundgang-fahrt.html', '.ride', [0, .1, .25, .36, .42, .5, .64, .73, .88, .99], None),
    'tueren': ('rundgang-tueren.html', '.walk', [0, .05, .09, .16, .24, .3, .38, .58, .7, .9, .99], '.scene.is-on .spot'),
}
with sync_playwright() as p:
    b = p.chromium.launch()
    for key, (page, sec, ts, spot) in PLAN.items():
        for (w, h) in views:
            mob = w < 900
            ctx = b.new_context(viewport={'width': w, 'height': h}, is_mobile=mob, has_touch=mob)
            pg = ctx.new_page(); errs = []
            pg.on('console', lambda m: errs.append(m.text[:120]) if m.type == 'error' else None)
            pg.on('pageerror', lambda e: errs.append('PE ' + str(e)[:120]))
            pg.goto(base + page, wait_until='networkidle'); pg.wait_for_timeout(1500)
            shots = []
            for t in ts:
                pg.evaluate("([s, t]) => { const e = document.querySelector(s); const top = e.getBoundingClientRect().top + scrollY; document.documentElement.style.scrollBehavior = 'auto'; scrollTo(0, top + (e.offsetHeight - innerHeight) * t); }", [sec, t])
                pg.wait_for_timeout(900)
                shots.append(Image.open(BytesIO(pg.screenshot())).convert('RGB'))
            if spot:  # Detail-Karte öffnen (Saal)
                pg.evaluate("([s, t]) => { const e = document.querySelector(s); const top = e.getBoundingClientRect().top + scrollY; scrollTo(0, top + (e.offsetHeight - innerHeight) * t); }", [sec, .3])
                pg.wait_for_timeout(900)
                if pg.locator(spot).count():
                    pg.locator(spot).first.click(); pg.wait_for_timeout(800)
                    shots.append(Image.open(BytesIO(pg.screenshot())).convert('RGB'))
            ox = pg.evaluate('document.documentElement.scrollWidth - innerWidth')
            cols = 4 if not mob else 6
            tw = 480 if not mob else 200
            th = int(tw * h / w)
            rows = (len(shots) + cols - 1) // cols
            C = Image.new('RGB', (cols * (tw + 6), rows * (th + 6)), (40, 40, 40))
            for i, s in enumerate(shots):
                C.paste(s.resize((tw, th)), ((i % cols) * (tw + 6), (i // cols) * (th + 6)))
            C.save(os.path.join(out, f'{key}-{w}x{h}.jpg'), quality=82)
            print(key, f'{w}x{h}', 'querscroll', ox, 'fehler', errs[:2])
            ctx.close()
    b.close()
