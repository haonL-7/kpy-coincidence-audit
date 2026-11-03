
import sys, os, glob, math, random
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import pandas as pd
from collections import defaultdict
from math import comb
BASE = os.environ.get("KPY_BASE", r"C:\Users\Administrator\Desktop\丙酮酰化")
site = defaultdict(set)
for f in sorted(glob.glob(os.path.join(BASE, "data", "cplm", "*", "*.txt"))):
    m = os.path.basename(os.path.dirname(f))
    df = pd.read_csv(f, sep="\t", header=None, usecols=[1,2,5], names=["acc","pos","sp"], dtype=str, on_bad_lines="skip")
    df = df[df["sp"].fillna("").str.contains("Homo sapiens", na=False)].dropna(subset=["acc","pos"])
    df = df[df["pos"].str.match(r"^\d+$", na=False)]
    for a, p in zip(df.acc.str.strip(), df.pos.astype(int)): site[(a,p)].add(m)
kpy = pd.read_csv(os.path.join(BASE, "data", "kpy_sites.csv"))
kpy["acc"] = kpy["Uniprot ID"].astype(str).str.strip(); kpy["pos"] = kpy["Positions within proteins"].astype(int)
ks = set((a,int(p)) for a,p in zip(kpy.acc, kpy.pos))

strata = defaultdict(lambda: [0,0,0,0])
for s,v in site.items():
    a_ = s[0]; q = s in ks; mm = len(v) >= 2; c = strata[a_]
    if q and mm: c[0]+=1
    elif q: c[1]+=1
    elif mm: c[2]+=1
    else: c[3]+=1
usable = {k:v for k,v in strata.items() if sum(v)>1 and (v[0]+v[1])>0 and (v[2]+v[3])>0}
print("strata:", len(usable), "| query sites:", sum(v[0]+v[1] for v in usable.values()))

def margins(scale=1.0):
    out = []
    for k,(a,b,c,d) in usable.items():
        n = a+b+c+d; R1 = a+b; C1 = a+c
        R1s = max(1, int(round(R1*scale)))
        R1s = min(R1s, n-1) if n > R1s else R1s
        out.append((n, R1s, C1))
    return out

def power(psi, scale=1.0, reps=1500, seed=11):
    random.seed(seed); marg = margins(scale); rej = 0
    for _ in range(reps):
        O = 0.0; E = 0.0; V = 0.0
        for (n, R1, C1) in marg:
            lo = max(0, R1+C1-n); hi = min(R1, C1)
            w = {}
            for x in range(lo, hi+1):
                w[x] = comb(C1,x)*comb(n-C1,R1-x)*(psi**x)
            tot = sum(w.values())
            r = random.random()*tot; acc = 0.0; pick = lo
            for x in sorted(w):
                acc += w[x]
                if acc >= r: pick = x; break
            O += pick; E += R1*C1/n
            V += (R1*(n-C1)*C1*(n-R1))/(n*n*(n-1)) if n > 1 else 0
        z = (O-E)/math.sqrt(V) if V > 0 else 0
        if abs(z) > 1.96: rej += 1
    return rej/reps

for scale in (1.0, 2.0, 4.0):
    print("query sites x%.0f (n~%d): power at OR 2.6 = %.2f | at OR 2.0 = %.2f" % (
        scale, int(round(23*scale)), power(2.6, scale), power(2.0, scale)))
