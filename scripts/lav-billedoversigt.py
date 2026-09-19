# -*- coding: utf-8 -*-
"""
Bygger src/billedoversigt.html: alle billeder paa en side med filnavn,
maal og hvor de bruges. Vaerktoej til at se, om et billede gaar igen to
steder, eller om et foto er for lille til den ramme, det staar i.

Siden er KUN til lokalt brug. Den staar i .gitignore og skal ikke med i
produktion. Se den paa http://localhost:8013/billedoversigt/

Koeres med:  python scripts/lav-billedoversigt.py
"""
import glob, io, json, os
from PIL import Image

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROD)

brug = {}
for f in sorted(glob.glob('src/_data/*.json')):
    d = json.load(io.open(f, encoding='utf-8'))
    for k, v in d.items():
        if isinstance(v, str) and v.startswith('/billeder/'):
            brug.setdefault(os.path.basename(v), []).append(os.path.basename(f)[:-5] + '.' + k)

kort = []
for f in sorted(glob.glob('src/billeder/*.jpg')):
    n = os.path.basename(f)
    w, h = Image.open(f).size
    steder = brug.get(n, [])
    klasse = 'ubrugt' if not steder else ('genbrugt' if len(steder) > 1 else '')
    hvor = ', '.join(steder) or 'UBRUGT'
    kort.append('<figure><img src="/billeder/%s"><figcaption><b>%s</b><br>%dx%d %s<br>'
                '<span class="%s">%s</span></figcaption></figure>'
                % (n, n, w, h, 'staaende' if h > w else 'liggende', klasse, hvor))

io.open('src/billedoversigt.html', 'w', encoding='utf-8').write(
    '''<!DOCTYPE html><html lang="da"><head><meta charset="utf-8">
<meta name="robots" content="noindex"><title>Billedoversigt</title>
<style>body{font:14px system-ui;margin:20px;background:#f6f2ea}
.g{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}
figure{margin:0;background:#fff;border-radius:10px;padding:8px}
img{width:100%;height:150px;object-fit:contain;background:#eee}
figcaption{font-size:11px;line-height:1.35;margin-top:6px}
.ubrugt{color:#b9743a;font-weight:700}.genbrugt{color:#c00;font-weight:700}</style>
</head><body><h1>Alle billeder og hvor de bruges</h1><div class="g">'''
    + '\n'.join(kort) + '</div></body></html>')

genbrugt = [n for n, s in brug.items() if len(s) > 1]
print('%d billeder. Genbrugte: %s' % (len(kort), ', '.join(genbrugt) if genbrugt else 'ingen'))
