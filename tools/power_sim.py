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

import random

keep, _ = cells_for(None, kpy_mode=True)
marg = [(sum(v), v[0] + v[1], v[0] + v[2]) for v in keep.values()]
print("strata: %d | query sites: %d" % (len(keep), sum(a + b for a, b, c, d in keep.values())))


def power(psi, scale=1.0, reps=6000, seed=11):
    random.seed(seed)
    rej = 0
    for _ in range(reps):
        O = E = V = 0.0
        for (n, R1, C1) in marg:
            R1 = min(max(1, int(round(R1 * scale))), n - 1) if n > 1 else R1
            lo, hi = max(0, R1 + C1 - n), min(R1, C1)
            w = {x: comb(C1, x) * comb(n - C1, R1 - x) * (psi ** x) for x in range(lo, hi + 1)}
            tot = sum(w.values())
            r = random.random() * tot
            acc = 0.0
            pick = lo
            for x in sorted(w):
                acc += w[x]
                if acc >= r:
                    pick = x
                    break
            O += pick
            E += R1 * C1 / n
            V += (R1 * (n - C1) * C1 * (n - R1)) / (n * n * (n - 1)) if n > 1 else 0
        if V > 0 and abs((O - E) / math.sqrt(V)) > 1.96:
            rej += 1
    return rej / reps


for scale in (1.0, 2.0, 4.0):
    print("query sites x%.0f (n~%d): power at OR 2.6 = %.2f | at OR 2.0 = %.2f" % (
        scale, int(round(23 * scale)), power(2.6, scale), power(2.0, scale)))
