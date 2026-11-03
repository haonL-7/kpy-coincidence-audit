
import sys, os, glob, math
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import pandas as pd
from collections import defaultdict
BASE = os.environ.get("KPY_BASE", r"C:\Users\Administrator\Desktop\丙酮酰化")
data = os.path.join(BASE, "data")

site = defaultdict(set)
for f in sorted(glob.glob(os.path.join(data, "cplm", "*", "*.txt"))):
    mod = os.path.basename(os.path.dirname(f))
    df = pd.read_csv(f, sep="\t", header=None, usecols=[1,2,5], names=["acc","pos","sp"], dtype=str, on_bad_lines="skip")
    df = df[df["sp"].fillna("").str.contains("Homo sapiens", na=False)].dropna(subset=["acc","pos"])
    df = df[df["pos"].str.match(r"^\d+$", na=False)]
    for a, p in zip(df.acc.str.strip(), df.pos.astype(int)):
        site[(a, p)].add(mod)

def conditional(mods_of_query, label):
    """query = lysines carrying any of mods_of_query; outcome = carries any other modification"""
    qset = {s for s, v in site.items() if v & mods_of_query}
    strata = defaultdict(lambda: [0,0,0,0])
    for s, v in site.items():
        a_ = s[0]
        q = s in qset
        other = bool((v - mods_of_query))
        c = strata[a_]
        if q and other: c[0] += 1
        elif q: c[1] += 1
        elif other: c[2] += 1
        else: c[3] += 1
    num = den = 0.0; E = 0.0; V = 0.0; O = 0; k = 0
    for a_, (a,b,c,d) in strata.items():
        n = a+b+c+d
        if n < 2 or (a+b) == 0 or (c+d) == 0: continue
        k += 1
        R1, C1 = a+b, a+c
        num += a*d/n; den += b*c/n
        E += R1*C1/n
        V += (R1*(c+d)*C1*(b+d))/(n*n*(n-1))
        O += a
    if den == 0 or V <= 0:
        return dict(label=label, n=len(qset), strata=k, O=O, E=E, OR=float("nan"), z=float("nan"), P=float("nan"))
    z = (O - E)/math.sqrt(V)
    return dict(label=label, n=len(qset), strata=k, O=O, E=round(E,1), OR=round(num/den,2), z=round(z,2),
                P=round(math.erfc(abs(z)/math.sqrt(2)), 3))

rows = []
for m in ["Acetylation","Crotonylation","2-Hydroxyisobutyrylation","Succinylation","Malonylation",
          "Butyrylation","Lactylation","Propionylation","Glutarylation"]:
    rows.append(conditional({m}, m))
# Kpy: query = Kpy sites (not in the catalogue), outcome = carries any modification
kpy = pd.read_csv(os.path.join(data, "kpy_sites.csv"))
kpy["acc"] = kpy["Uniprot ID"].astype(str).str.strip(); kpy["pos"] = kpy["Positions within proteins"].astype(int)
ks = set((a, int(p)) for a, p in zip(kpy.acc, kpy.pos))
strata = defaultdict(lambda: [0,0,0,0])
for s, v in site.items():
    a_ = s[0]; q = s in ks; other = bool(v); c = strata[a_]
    if q and other: c[0]+=1
    elif q: c[1]+=1
    elif other: c[2]+=1
    else: c[3]+=1
num=den=E=V=O=0; k=0
for a_,(a,b,c,d) in strata.items():
    n=a+b+c+d
    if n<2 or (a+b)==0 or (c+d)==0: continue
    k+=1; R1,C1=a+b,a+c
    num+=a*d/n; den+=b*c/n; E+=R1*C1/n
    V+=(R1*(c+d)*C1*(b+d))/(n*n*(n-1)); O+=a
print("DEBUG k=%d O=%d E=%.2f V=%.4f" % (k, O, E, V))
z=(O-E)/math.sqrt(V) if V > 0 else float('nan')
rows.append(dict(label="Kpy", n=len(ks), strata=k, O=O, E=round(E,1), OR=round(num/den,2) if den else float('nan'),
                 z=round(z,2) if V>0 else float('nan'), P=round(math.erfc(abs(z)/math.sqrt(2)),3) if V>0 else float('nan')))

print("%-26s %6s %6s %5s %6s %7s %6s %6s" % ("query modification","n_sites","strata","obs","exp","MH OR","z","P"))
for r in rows:
    print("%-26s %6d %6d %5d %6.1f %7.2f %6.2f %6.3f" % (r["label"], r["n"], r["strata"], r["O"], r["E"], r["OR"], r["z"], r["P"]))
