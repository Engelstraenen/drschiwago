#!/usr/bin/env python3
"""Prüft, dass kein Bild auf der Seite doppelt vorkommt (Startseite + Catering, auch Bilder aus catering.js).

Start: python3 tools/check_dupes.py   → Exit-Code 1, wenn ein Bild mehrfach benutzt wird.
Hochformat-Varianten (<name>-m) zählen zum selben Platz und sind erlaubt.
Zusätzlich: Liste der Gerichtsnamen, die auf der Startseite mehrfach stehen (nur Hinweis).
"""
import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
site = os.path.join(HERE, 'site')
use = collections.Counter()
where = collections.defaultdict(list)
for f in ['index.html', 'catering.html', 'rundgang.html']:
    if not os.path.exists(os.path.join(site, f)): continue
    for k in re.findall(r'data-img="([^"]+)"', open(os.path.join(site, f)).read()):
        use[k] += 1; where[k].append(f)
js = open(os.path.join(site, 'assets', 'js', 'catering.js')).read()
for group in re.findall(r"img: \[([^\]]*)\]", js):
    for k in re.findall(r"'([^']+)'", group)[:1]:
        use[k] += 1; where[k].append('catering.js')
dup = {k: v for k, v in use.items() if v > 1}
# gleiche Quelldatei unter zwei Namen?
assets = open(os.path.join(HERE, 'tools', 'assets.py')).read()
pairs = re.findall(r'"(DSM-[0-9a-zA-Z]+)": "([a-z0-9-]+)"', assets)
src = collections.defaultdict(list)
for sid, name in pairs:
    src[sid].append(name)
same_src = {sid: n for sid, n in src.items() if len(n) > 1}

print('Bilder in Benutzung:', len(use))
if dup:
    print('DOPPELT:', {k: where[k] for k in dup})
if same_src:
    print('GLEICHE QUELLE unter mehreren Namen:', same_src)

text = re.sub(r'<[^>]+>', ' ', open(os.path.join(site, 'index.html')).read())
text = re.sub(r'<details>.*?</details>', ' ', text, flags=re.S)
dishes = ['Schaschlik', 'Lule Kebab', 'Canapés', 'Hering im Pelzmantel', 'Plov', 'Napoleon', 'Golubzi', 'Medovik', 'Olivier', 'Granatapfelring',
          'Mimosa', 'Vinaigrette', 'Boeuf Stroganoff', 'Forelle', 'Zanderfilet', 'Lachsfilet', 'Fischvariation', 'Crêpe-Röllchen', 'Panna Cotta',
          'Mousse au Chocolat', 'Buchweizen', 'Bratkartoffeltaler', 'Tiramisu', 'Vitello Tonnato']
names = {d: len(re.findall(re.escape(d), text)) for d in dishes}
print('Namen mehrfach (Startseite, ohne FAQ):', {d: n for d, n in names.items() if n > 1} or 'keine')
sys.exit(1 if dup or same_src else 0)
