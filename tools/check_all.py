#!/usr/bin/env python3
"""Handy-Pflichtprüfung (Masterfile V2.25): alle Seiten in 390x844, 360x740, 430x932, 844x390 (+ Desktop).

Start: python3 tools/check_all.py [basis-url] [ausgabe]
Prüft je Viewport: Querscrollen, Konsolenfehler, Text < 14 px, Tipp-Flächen < 44 px; Screenshots an Scroll-Stellen.
"""
import os
import sys
from playwright.sync_api import sync_playwright

base = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:4381/"
out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/drs-all"
os.makedirs(out, exist_ok=True)
VIEWS = [(390, 844), (360, 740), (430, 932), (844, 390), (1440, 900)]
PAGES = {
    "index.html": "hero:0,abend:0,buffet:.06,buffet:.3,buffet:.97,karte:.2,kueche:0,abend:.8,bars:.3,feiern:0,catering:0,instagram:0,bewertungen:0,bewertungen:.6,reservieren:0,kontakt:0",
    "catering.html": "top:0,baukasten:.05,anfrage:0,galerie:0,bewertungen:0,kontakt:0",
    "rundgang.html": "top:0,saal:0,mirrors:0,bars-rg:0,terrasse-rg:0,garten:0,kontakt:0",
    "ru/index.html": "hero:0,buffet:.97,karte:.2,abend:.8,feiern:0,catering:0,bewertungen:0,reservieren:0,kontakt:0",
    "ru/catering.html": "top:0,baukasten:.05,anfrage:0,kontakt:0",
    "ru/rundgang.html": "top:0,saal:0,garten:0,kontakt:0",
    "rundgang-fahrt.html": "top:0,fahrt:.2,fahrt:.45,fahrt:.7,fahrt:.99,kontakt:0",
    "rundgang-tueren.html": "top:0,tour:.1,tour:.3,tour:.62,tour:.97,kontakt:0",
}
if len(sys.argv) > 3:
    PAGES = {k: v for k, v in PAGES.items() if k in sys.argv[3].split(",")}
AUDIT = r"""() => {
  const vis = el => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' && +cs.opacity > 0.05 && !el.closest('.is-missing,[hidden]'); };
  const small = new Map(), taps = new Map();
  for (const el of document.querySelectorAll('body *')) {
    if (!vis(el)) continue;
    const own = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 1);
    if (own) { const fs = parseFloat(getComputedStyle(el).fontSize); if (fs < 14) { const k = el.tagName.toLowerCase() + '.' + [...el.classList].join('.') + ' ' + fs + 'px'; small.set(k, (small.get(k) || 0) + 1); } }
    if (el.matches('a, button, select, input, summary')) { const r = el.getBoundingClientRect(); if (r.height < 44 || r.width < 44) { if (el.closest('.foot__legal, .faq__list')) continue; const k = el.tagName.toLowerCase() + '.' + [...el.classList].join('.') + ' ' + Math.round(r.width) + 'x' + Math.round(r.height); taps.set(k, (taps.get(k) || 0) + 1); } }
  }
  return { ox: document.documentElement.scrollWidth - innerWidth, small: [...small].slice(0, 25), taps: [...taps].slice(0, 25) };
}"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for page, spots in PAGES.items():
        for (w, h) in VIEWS:
            errs = []
            mob = w < 900
            ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, is_mobile=mob, has_touch=mob)
            pg = ctx.new_page()
            pg.on("console", lambda m: errs.append(m.text[:120]) if m.type == "error" and "ErrorUtils" not in m.text else None)
            pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)[:120]))
            pg.goto(base + page, wait_until="networkidle")
            pg.wait_for_timeout(2500)
            oxmax = 0
            for s in spots.split(","):
                sid, frac = s.split(":")
                y = pg.evaluate("""([id, f]) => { const el = id === 'top' ? document.body : document.getElementById(id); if (!el) return -1;
                    const top = el.getBoundingClientRect().top + scrollY; const run = Math.max(0, el.offsetHeight - innerHeight);
                    return id === 'top' ? 0 : top + run * f; }""", [sid, float(frac)])
                if y < 0:
                    continue
                pg.evaluate("y => { document.documentElement.style.scrollBehavior='auto'; scrollTo(0, y); }", y)
                pg.wait_for_timeout(1100)
                oxmax = max(oxmax, pg.evaluate("document.documentElement.scrollWidth - innerWidth"))
                pg.screenshot(path=os.path.join(out, f"{page.replace('/', '-').split('.')[0]}-{w}x{h}-{sid}{frac}.jpg"), quality=60, type="jpeg")
            a = pg.evaluate(AUDIT)
            print(f"{page} {w}x{h}: querscroll {max(a['ox'], oxmax)} px | fehler {len(errs)} {errs[:2]}")
            if a["small"]:
                print("   klein:", a["small"])
            if a["taps"]:
                print("   tippen:", a["taps"])
            ctx.close()
    b.close()
