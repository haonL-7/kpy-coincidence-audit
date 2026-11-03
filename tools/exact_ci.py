
import sys, os, glob, math
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import pandas as pd
from collections import defaultdict
from math import comb
root = os.environ.get("KPY_BASE", r"C:\Users\Administrator\Desktop\丙酮酰化")
data = os.path.join(root, "data")

site = defaultdict(set)
for f in sorted(glob.glob(os.path.join(data, "cplm", "*", "*.txt"))):
    mod = os.path.basename(os.path.dirname(f))
    df = pd.read_csv(f, sep="\t", header=None, usecols=[1,2,5], names=["acc","pos","sp"], dtype=str, on_bad_lines="skip")
    df = df[df["sp"].fillna("").str.contains("Homo sapiens", na=False)].dropna(subset=["acc","pos"])
    df = df[df["pos"].str.match(r"^\d+$", na=False)]
    for a, p in zip(df.acc.str.strip(), df.pos.astype(int)):
        site[(a, p)].add(mod)

kpy = pd.read_csv(os.path.join(data, "kpy_sites.csv"))
kpy["acc"] = kpy["Uniprot ID"].astype(str).str.strip()
kpy["pos"] = kpy["Positions within proteins"].astype(int)
ks = set((a, int(p)) for a, p in zip(kpy.acc, kpy.pos))

strata = defaultdict(lambda: [0,0,0,0])
for s in site:
    a = s[0]; k = s in ks; m = len(site[s]) >= 2; c = strata[a]
    if k and m: c[0] += 1
    elif k: c[1] += 1
    elif m: c[2] += 1
    else: c[3] += 1

usable = {k: v for k, v in strata.items() if sum(v) > 1 and (v[0]+v[1]) > 0 and (v[2]+v[3]) > 0}
obs = sum(v[0] for v in usable.values())
tabs = []
num = den = 0.0
for k, (a,b,c,d) in usable.items():
    n = a+b+c+d; R1 = a+b; C1 = a+c
    lo = max(0, R1+C1-n); hi = min(R1, C1)
    tabs.append((n, R1, C1, lo, hi))
    num += a*d/n; den += b*c/n
OR = num/den
print("strata:", len(tabs), "| observed multi among Kpy sites:", obs, "| MH OR = %.2f" % OR)

def total_dist(psi):
    dist = {0: 1.0}
    for (n, R1, C1, lo, hi) in tabs:
        w = {}
        z = 0.0
        for x in range(lo, hi+1):
            w[x] = comb(C1, x) * comb(n-C1, R1-x) * (psi ** x)
            z += w[x]
        for x in w: w[x] /= z
        new = defaultdict(float)
        for t, pt in dist.items():
            for x, px in w.items():
                new[t+x] += pt*px
        dist = dict(new)
    return dist

def p_two_sided(psi):
    d = total_dist(psi)
    po = d.get(obs, 0.0)
    return sum(p for p in d.values() if p <= po*(1+1e-12))

print("exact two-sided P at psi = 1: %.3f" % p_two_sided(1.0))

def invert(lo_psi, hi_psi, side):
    for _ in range(50):
        mid = math.sqrt(lo_psi*hi_psi)
        p = p_two_sided(mid)
        compat = p > 0.05
        if side == "lower":
            if compat: hi_psi = mid
            else: lo_psi = mid
        else:
            if compat: lo_psi = mid
            else: hi_psi = mid
    return math.sqrt(lo_psi*hi_psi)

lo_ci = invert(0.05, OR, "lower")
hi_ci = invert(OR, 500.0, "upper")
print("exact conditional 95%% CI for the common OR: %.2f - %.2f" % (lo_ci, hi_ci))
