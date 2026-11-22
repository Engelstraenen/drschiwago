#!/usr/bin/env python3
"""Erzeugt die russischen Seiten site/ru/*.html aus den deutschen Seiten.

Texte kommen aus i18n/ru.json (Schlüssel = deutscher Text, wie tools/i18n_extract.py ihn liest).
Start: python3 tools/build_ru.py   (nach jeder Änderung an den deutschen Seiten)
Fehlt eine Übersetzung, bricht das Skript ab und nennt die Texte.
"""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ['index.html', 'catering.html', 'rundgang.html']
ATTRS = ('alt', 'aria-label', 'title', 'placeholder')
TR = json.load(open(os.path.join(HERE, 'i18n', 'ru.json')))
missing = []


def norm(s):
    return ' '.join(html.unescape(s).split())


def tr_text(seg):
    t = norm(seg)
    if not t or not any(c.isalpha() for c in t):
        return seg
    if t not in TR:
        missing.append(t); return seg
    lead = seg[:len(seg) - len(seg.lstrip())]
    trail = seg[len(seg.rstrip()):]
    return lead + html.escape(TR[t], quote=False) + trail


def tr_attr(m):
    name, q, val = m.group(1), m.group(2), m.group(3)
    t = norm(val)
    if not t:
        return m.group(0)
    if t not in TR:
        missing.append(t); return m.group(0)
    return f'{name}={q}{html.escape(TR[t], quote=True)}{q}'


def tr_tag(tag):
    if tag.startswith('<!--') or tag.startswith('<!'):
        return tag
    tag = re.sub(r'\b(' + '|'.join(ATTRS) + r')=(["\'])(.*?)\2', tr_attr, tag)
    if re.match(r'<meta\b', tag) and re.search(r'name=["\']description["\']', tag):
        tag = re.sub(r'\b(content)=(["\'])(.*?)\2', tr_attr, tag)
    # Pfade: russische Seiten liegen eine Ebene tiefer
    tag = re.sub(r'((?:href|src|srcset|poster|content)=["\'])assets/', r'\1../assets/', tag)
    tag = re.sub(r'(srcset=["\'][^"\']*)', lambda m: re.sub(r'(,\s*)assets/', r'\1../assets/', m.group(1)), tag)
    tag = re.sub(r'url\((["\']?)assets/', r'url(\1../assets/', tag)
    return tag


def build(page):
    src = open(os.path.join(HERE, 'site', page)).read()
    # Sprachumschalter: auf der russischen Seite zurück zur deutschen
    src = re.sub(r'<a class="nav__lang"[^>]*>RU</a>',
                 f'<a class="nav__lang" href="../{page}" hreflang="de" lang="de" aria-label="Deutsche Version">DE</a>', src)
    out, i = [], 0
    for m in re.finditer(r'<script\b.*?</script>|<style\b.*?</style>|<!--.*?-->|<[^>]+>', src, re.S):
        out.append(tr_text(src[i:m.start()]))
        tok = m.group(0)
        if tok.startswith('<script') or tok.startswith('<style'):
            open_tag = re.match(r'<[^>]+>', tok).group(0)
            tok = tr_tag(open_tag) + tok[len(open_tag):]
            tok = tok.replace("url(assets/", "url(../assets/")
        elif tok.startswith('<html'):
            tok = re.sub(r'lang="de"', 'lang="ru" data-base="../"', tok)
        elif not tok.startswith('<!--'):
            # aria-label des Umschalters ist schon deutsch, nicht übersetzen
            if 'class="nav__lang"' in tok:
                pass
            else:
                tok = tr_tag(tok)
        out.append(tok)
        i = m.end()
    out.append(tr_text(src[i:]))
    return ''.join(out)


def main():
    os.makedirs(os.path.join(HERE, 'site', 'ru'), exist_ok=True)
    res = {}
    for pg in PAGES:
        res[pg] = build(pg)
    if missing:
        print('Fehlende Übersetzungen in i18n/ru.json:')
        for t in dict.fromkeys(missing):
            print(' -', t)
        sys.exit(1)
    for pg, s in res.items():
        open(os.path.join(HERE, 'site', 'ru', pg), 'w').write(s)
        print('site/ru/' + pg, len(s))


if __name__ == '__main__':
    main()
