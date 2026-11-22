#!/usr/bin/env python3
"""Sammelt alle sichtbaren Texte (und alt/aria-label/title/meta) der deutschen Seiten.

Start: python3 tools/i18n_extract.py  → listet Texte, die in i18n/ru.json noch fehlen.
"""
import html.parser
import json
import os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ['index.html', 'catering.html', 'rundgang.html']
SKIP_TAGS = {'script', 'style'}
ATTRS = ('alt', 'aria-label', 'title', 'placeholder')


class P(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []; self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in SKIP_TAGS:
            self.skip += 1
        a = dict(attrs)
        for k in ATTRS:
            if a.get(k, '').strip():
                self.out.append(a[k].strip())
        if tag == 'meta' and a.get('name') == 'description':
            self.out.append(a.get('content', '').strip())

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS:
            self.skip -= 1

    def handle_data(self, d):
        t = ' '.join(d.split())
        if t and not self.skip and any(c.isalpha() for c in t):
            self.out.append(t)


def texts():
    seen = []
    for pg in PAGES:
        p = P(); p.feed(open(os.path.join(HERE, 'site', pg)).read())
        for t in p.out:
            if t not in seen:
                seen.append(t)
    return seen


if __name__ == '__main__':
    path = os.path.join(HERE, 'i18n', 'ru.json')
    have = json.load(open(path)) if os.path.exists(path) else {}
    miss = [t for t in texts() if t not in have]
    print(json.dumps(miss, ensure_ascii=False, indent=0))
    print(len(miss), 'fehlen von', len(texts()))
