import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kpydata import load_sites, load_kpy
from collections import defaultdict
from math import comb

site = load_sites()
KS = load_kpy()
MODS = ["Acetylation", "Crotonylation", "2-Hydroxyisobutyrylation", "Malonylation",
        "Succinylation", "Butyrylation", "Lactylation", "Glutarylation", "Propionylation"]


def cells_for(Y, kpy_mode=False):
    """Stratified 2x2 counts. For a catalogued modification Y the outcome counts
    modifications other than Y, so the query's own mark never enters the outcome."""
    strata = defaultdict(lambda: [0, 0, 0, 0])
    nsite = 0
    for s, v in site.items():
        if kpy_mode:
            q = s in KS
            others = len(v)
        else:
            y = Y in v
            if y:
                nsite += 1
            others = len(v) - (1 if y else 0)
            q = y and others >= 1
        o = others >= 2
        c = strata[s[0]]
        if q and o: c[0] += 1
        elif q: c[1] += 1
        elif o: c[2] += 1
        else: c[3] += 1
    keep = {k: tuple(v) for k, v in strata.items()
            if sum(v) > 1 and (v[0] + v[1]) > 0 and (v[2] + v[3]) > 0}
    return keep, nsite


def mh(cells):
    num = den = E = V = 0.0
    O = 0
    for (a, b, c, d) in cells:
        n = a + b + c + d
        R1, C1 = a + b, a + c
        num += a * d / n
        den += b * c / n
        E += R1 * C1 / n
        V += (R1 * (c + d) * C1 * (b + d)) / (n * n * (n - 1))
        O += a
    if den == 0 or V <= 0:
        return None
    OR = num / den
    z = (O - E) / math.sqrt(V)
    return OR, z, O, E

print("%-26s %6s %6s %5s %8s %8s" % ("modification", "sites", "query", "K", "MH OR", "P"))
for m in MODS:
    keep, ns = cells_for(m)
    r = mh(list(keep.values()))
    nq = sum(a + b for a, b, c, d in keep.values())
    p = math.erfc(abs(r[1]) / math.sqrt(2))
    print("%-26s %6d %6d %5d %8.2f %8.1e" % (m, ns, nq, len(keep), r[0], p))

keep, ns = cells_for(None, kpy_mode=True)
r = mh(list(keep.values()))
nq = sum(a + b for a, b, c, d in keep.values())
print("\nKpy (same specification): query=%d K=%d obs=%d OR=%.2f P=%.3f" % (
    nq, len(keep), r[2], r[0], math.erfc(abs(r[1]) / math.sqrt(2))))
ors = [mh(list(cells_for(m)[0].values()))[0] for m in MODS]
print("nine LOO OR range: %.2f - %.2f" % (min(ors), max(ors)))
