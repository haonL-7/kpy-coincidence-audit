
import os, glob, math
from collections import defaultdict
import pandas as pd

import os
BASE = os.environ.get("KPY_BASE", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
base = os.path.join(BASE, "data")
files = sorted(glob.glob(os.path.join(base, "cplm", "*", "*.txt")))
site_mods = defaultdict(set)
for f in files:
    mod = os.path.basename(os.path.dirname(f))
    df = pd.read_csv(f, sep="\t", header=None, usecols=[1,2,5], names=["acc","pos","sp"], dtype=str, on_bad_lines="skip")
    df = df[df["sp"].fillna("").str.contains("Homo sapiens", na=False)].dropna(subset=["acc","pos"])
    df = df[df["pos"].str.match(r"^\d+$", na=False)]
    for a,p in zip(df["acc"].str.strip(), df["pos"].astype(int)):
        site_mods[(a,p)].add(mod)
per_prot_ann = defaultdict(int)
for (a,p) in site_mods: per_prot_ann[a]+=1

def audit(modname, sites):
    if not sites: return None
    by_prot = defaultdict(int)
    for a,p in sites: by_prot[a]+=1
    others = {s: (v - {modname}) for s,v in site_mods.items()}
    obs = sum(1 for s in sites if others.get(s))
    per_prot_other = defaultdict(int)
    for (a,p),v in others.items():
        if v: per_prot_other[a]+=1
    E=0.0; V=0.0
    for a,n in by_prot.items():
        N = per_prot_ann[a]; m = per_prot_other[a]
        if N==0: continue
        r = m/N; E += n*r
        if N>1: V += n*r*(1-r)*(N-n)/(N-1)
    z = (obs-E)/math.sqrt(V) if V>0 else 0.0
    p = 0.5*math.erfc(z/math.sqrt(2)) if z>0 else 1-0.5*math.erfc(z/math.sqrt(2))
    return dict(mod=modname, n=len(sites), proteins=len(by_prot), obs_other=obs,
                obs_rate=round(100*obs/len(sites),1), exp_rate=round(100*E/len(sites),1),
                z=round(z,2), p=round(p,4))

rows=[]
for f in files:
    mod = os.path.basename(os.path.dirname(f))
    r = audit(mod, [s for s,v in site_mods.items() if mod in v])
    if r: rows.append(r)
kpy = pd.read_csv(os.path.join(base, "kpy_sites.csv"))
kpy["acc"]=kpy["Uniprot ID"].astype(str).str.strip(); kpy["pos"]=kpy["Positions within proteins"].astype(int)
rows.append(audit("Kpy (this study)", [(a,p) for a,p in zip(kpy["acc"],kpy["pos"])]))

df = pd.DataFrame([r for r in rows if r]).sort_values("n", ascending=False)
pd.set_option("display.width", 220)
print("Co-occupancy with OTHER modifications; expectation from per-protein annotated-lysine rates")
print()
print(df.to_string(index=False))
df.to_csv(os.path.join(base,"audit_other.csv"), index=False, encoding="utf-8-sig")
print()
print("saved audit_other.csv ; rows:", len(df))
