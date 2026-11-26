#!/usr/bin/env python3
"""Google Fonts lokal einbinden (schneller, keine Datenübertragung an Google).

Liest die von Google gelieferte CSS (Datei als 1. Argument), lädt die woff2-Dateien
(nur latin, latin-ext, cyrillic, cyrillic-ext) nach site/assets/fonts/ und schreibt
site/assets/css/fonts.css. Ersetzt in allen Seiten die Google-Font-Links.
Start: python3 tools/fonts_local.py <google.css>
"""
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(HERE, 'site', 'assets', 'fonts')
KEEP = {'latin', 'latin-ext', 'cyrillic', 'cyrillic-ext'}
os.makedirs(FONTS, exist_ok=True)
css = open(sys.argv[1]).read()
blocks = re.findall(r'/\* ([a-z-]+) \*/\s*(@font-face \{.*?\})', css, re.S)
out, files, hero = [], {}, None
for subset, block in blocks:
    if subset not in KEEP:
        continue
    fam = re.search(r"font-family: '([^']+)'", block).group(1)
    style = re.search(r'font-style: (\w+)', block).group(1)
    url = re.search(r'url\((https://[^)]+\.woff2)\)', block).group(1)
    name = files.get(url)
    if not name:
        name = f"{fam.lower().replace(' ', '-')}-{style}-{subset}.woff2"
        if name in files.values():
            name = name.replace('.woff2', f'-{len(files)}.woff2')
        files[url] = name
        path = os.path.join(FONTS, name)
        if not os.path.exists(path):
            urllib.request.urlretrieve(url, path)
    out.append(f'/* {subset} */\n' + block.replace(url, '../fonts/' + name))
    if fam == 'Cormorant Garamond' and style == 'normal' and subset == 'latin':
        hero = name
open(os.path.join(HERE, 'site', 'assets', 'css', 'fonts.css'), 'w').write(
    '/* Schriften lokal (vorher Google Fonts), erzeugt mit tools/fonts_local.py */\n' + '\n'.join(out) + '\n')
print(len(out), 'Schriftschnitte,', len(files), 'Dateien, Titel-Schrift:', hero)

link_re = re.compile(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">\n<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\n'
                     r'(?:<link rel="preload" as="style" href="https://fonts\.googleapis\.com/[^"]+" onload="[^"]*">\n<noscript><link rel="stylesheet" href="https://fonts\.googleapis\.com/[^"]+"></noscript>'
                     r'|<link href="https://fonts\.googleapis\.com/[^"]+" rel="stylesheet">)')
for f in ['index.html', 'catering.html', 'rundgang.html', 'rundgang-fahrt.html', 'rundgang-tueren.html', 'anfrage.html']:
    p = os.path.join(HERE, 'site', f)
    s = open(p).read()
    new = (f'<link rel="preload" as="font" type="font/woff2" href="assets/fonts/{hero}" crossorigin>\n'
           '<link rel="stylesheet" href="assets/css/fonts.css">')
    s2, n = link_re.subn(new, s, count=1)
    open(p, 'w').write(s2)
    print(f, 'ersetzt' if n else 'NICHT ersetzt')
