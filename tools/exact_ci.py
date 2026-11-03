import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kpydata import load_sites, load_kpy
from collections import defaultdict
from math import comb

site = load_sites()
KS = load_kpy()


def kpy_strata():
    strata = defaultdict(lambda: [0, 0, 0, 0])
    for s, v in site.items():
        q = s in KS
        o = len(v) >= 2
        c = strata[s[0]]
        if q and o: c[0] += 1
        elif q: c[1] += 1
        elif o: c[2] += 1
        else: c[3] += 1
    return {k: tuple(v) for k, v in strata.items()
            if sum(v) > 1 and (v[0] + v[1]) > 0 and (v[2] + v[3]) > 0}


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
    return num, den, E, V, O


def total_dist(cells, psi):
    dist = {0: 1.0}
    for (a, b, c, d) in cells:
        n = a + b + c + d
        R1, C1 = a + b, a + c
        lo, hi = max(0, R1 + C1 - n), min(R1, C1)
        w = {}
        z = 0.0
        for x in range(lo, hi + 1):
            w[x] = comb(C1, x) * comb(n - C1, R1 - x) * (psi ** x)
            z += w[x]
        for x in w:
            w[x] /= z
        new = defaultdict(float)
        for t, pt in dist.items():
            for x, px in w.items():
                new[t + x] += pt * px
        dist = dict(new)
    return dist


def p_two_sided(cells, obs, psi):
    d = total_dist(cells, psi)
    po = d.get(obs, 0.0)
    return sum(p for p in d.values() if p <= po * (1 + 1e-12))


def invert(cells, obs, lo_psi, hi_psi, side):
    for _ in range(50):
        mid = math.sqrt(lo_psi * hi_psi)
        p = p_two_sided(cells, obs, mid)
        compat = p > 0.05
        if side == "lower":
            if compat: hi_psi = mid
            else: lo_psi = mid
        else:
            if compat: lo_psi = mid
            else: hi_psi = mid
    return math.sqrt(lo_psi * hi_psi)


cells = list(kpy_strata().values())
obs = sum(c[0] for c in cells)
num, den, E, V, O = mh(cells)
OR = num / den
print("strata: %d | observed multi among Kpy sites: %d | MH OR = %.2f" % (len(cells), obs, OR))
print("exact two-sided P at psi = 1: %.3f" % p_two_sided(cells, obs, 1.0))
lo = invert(cells, obs, 0.05, OR, "lower")
hi = invert(cells, obs, OR, 500.0, "upper")
print("exact conditional 95%% CI for the common OR: %.2f - %.2f" % (lo, hi))
