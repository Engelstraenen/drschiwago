#!/usr/bin/env python3
"""Headless-Prüfung: Konsolenfehler, Querscrollen, Screenshots an Scroll-Stellen.

Start: python3 tools/check.py [url] [ausgabe] [BxH] [stellen]
  stellen = kommagetrennt "id:anteil" (Anteil der Sticky-Strecke), z. B. hero:0,location:.3,abend:.8
"""
import os
import sys
from playwright.sync_api import sync_playwright

url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:4381/"
out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/drs-check"
w, h = (int(x) for x in (sys.argv[3] if len(sys.argv) > 3 else "1440x900").split("x"))
spots = (sys.argv[4] if len(sys.argv) > 4 else "hero:0").split(",")
os.makedirs(out, exist_ok=True)
errs = []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1, is_mobile=w < 600, has_touch=w < 600)
    pg.on("console", lambda m: errs.append(f"{m.type}: {m.text}") if m.type == "error" or (m.type == "warning" and "Permissions-Policy" not in m.text) else None)
    pg.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
    pg.goto(url, wait_until="networkidle")
    pg.wait_for_timeout(3500)
    for s in spots:
        sid, frac = s.split(":")
        y = pg.evaluate("""([id, f]) => { const el = document.getElementById(id); if (!el) return -1;
            const top = el.getBoundingClientRect().top + scrollY; const run = Math.max(0, el.offsetHeight - innerHeight);
            return top + run * f; }""", [sid, float(frac)])
        if y < 0:
            print("fehlt:", sid); continue
        pg.evaluate("y => { document.documentElement.style.scrollBehavior='auto'; scrollTo(0, y); }", y)
        pg.wait_for_timeout(1400)
        pg.screenshot(path=os.path.join(out, f"{w}-{sid}-{frac}.jpg"), quality=70, type="jpeg")
    ox = pg.evaluate("document.documentElement.scrollWidth - innerWidth")
    hidden = pg.evaluate("[...document.querySelectorAll('.is-missing')].map(e => e.dataset.need || e.dataset.img || e.className)")
    b.close()
print("Querscrollen px:", ox)
print("ausgeblendet (Motiv fehlt):", hidden)
print("Konsole:", errs if errs else "keine Fehler")
