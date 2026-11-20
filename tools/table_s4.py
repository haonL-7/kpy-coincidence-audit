"""Table S4: crude and stratified odds ratios on the same informative strata."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kpydata import load_sites, load_kpy
from collections import defaultdict

site = load_sites(); KS = load_kpy()
MODS = ["Acetylation", "Crotonylation", "2-Hydroxyisobutyrylation", "Malonylation",
        "Succinylation", "Butyrylation", "Lactylation", "Glutarylation", "Propionylation"]


def cells(Y, kpy=False):
    st = defaultdict(lambda: [0, 0, 0, 0])
    for s, v in site.items():
        if kpy:
            y = s in KS; others = len(v)
        else:
            y = Y in v; others = len(v) - (1 if y else 0)
            if y and others == 0:
                continue                      # Y-only lysines enter neither row
        o = others >= 2
        q = y if kpy else (y and others >= 1)
        c = st[s[0]]
        if q and o: c[0] += 1
        elif q: c[1] += 1
        elif o: c[2] += 1
        else: c[3] += 1
    return {k: v for k, v in st.items()
            if sum(v) > 1 and (v[0] + v[1]) > 0 and (v[2] + v[3]) > 0}


def mh(cl):
    num = den = 0.0
    for a, b, c, d in cl:
        n = a + b + c + d
        num += a * d / n; den += b * c / n
    return num / den


def crude(cl):
    a = sum(x[0] for x in cl); b = sum(x[1] for x in cl)
    c = sum(x[2] for x in cl); d = sum(x[3] for x in cl)
    return (a * d) / (b * c)


print('%-26s %6s %8s %8s %8s' % ('modification', 'strata', 'crude', 'MH', 'shift'))
for m in MODS:
    cl = list(cells(m).values())
    print('%-26s %6d %8.2f %8.2f %8.2f' % (m, len(cl), crude(cl), mh(cl), mh(cl) / crude(cl)))
cl = list(cells(None, kpy=True).values())
print('%-26s %6d %8.2f %8.2f %8.2f' % ('Pyruvylation (Kpy)', len(cl), crude(cl), mh(cl), mh(cl) / crude(cl)))