
import os, glob, json, random, math
from collections import defaultdict
import pandas as pd
BASE = os.environ.get("KPY_BASE", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
base = os.path.join(BASE, "data")
files = sorted(glob.glob(os.path.join(base, "cplm", "*", "*.txt")))
site_mods = defaultdict(set); gene_of = {}
for f in files:
    mod = os.path.basename(os.path.dirname(f))
    df = pd.read_csv(f, sep="\t", header=None, usecols=[1,2,4,5], names=["acc","pos","gene","sp"], dtype=str, on_bad_lines="skip")
    df = df[df["sp"].fillna("").str.contains("Homo sapiens", na=False)].dropna(subset=["acc","pos"])
    df = df[df["pos"].str.match(r"^\d+$", na=False)]
    for a,p,g in zip(df["acc"].str.strip(), df["pos"].astype(int), df["gene"].fillna("")):
        site_mods[(a,p)].add(mod); gene_of.setdefault(a, g.strip())
import re

import os
HIST = re.compile(r"^(H1|H2A|H2B|H2AX|H3|H4|HIST|CENP)", re.I)
hist_acc = {a for a,g in gene_of.items() if HIST.match(g)}

kpy = pd.read_csv(os.path.join(base, "kpy_sites.csv"))
kpy["acc"] = kpy["Uniprot ID"].astype(str).str.strip(); kpy["pos"] = kpy["Positions within proteins"].astype(int)
ks = list(zip(kpy["acc"], kpy["pos"]))

def stratified_null(sites, iters=2000, seed=7):
    by_prot = defaultdict(list)
    for a,p in sites:
        if (a,p) in site_mods: by_prot[a].append(p)
    ann = {a: [s for s in site_mods if s[0]==a] for a in by_prot}
    obs = sum(1 for a,ps in by_prot.items() for p in ps if len(site_mods[(a,p)])>=2)
    random.seed(seed); nulls=[]
    for _ in range(iters):
        c=0
        for a,ps in by_prot.items():
            pool = ann[a]
            if not pool: continue
            draws = random.sample(pool, min(len(ps), len(pool)))
            c += sum(1 for s in draws if len(site_mods[s])>=2)
        nulls.append(c)
    m = sum(nulls)/iters
    p = sum(1 for x in nulls if x>=obs)/iters
    return len(by_prot), sum(len(v) for v in by_prot.values()), obs, round(m,1), p

print("== within-protein stratified null (annotated lysines only) ==")
for lbl, group in [("all Kpy", ks), ("non-histone", [s for s in ks if s[0] not in hist_acc]), ("histone", [s for s in ks if s[0] in hist_acc])]:
    npro, nsite, obs, exp, p = stratified_null(group)
    print("%-12s proteins=%2d annotated_sites=%2d  multi_obs=%2d  null_mean=%.1f  p=%.3f" % (lbl, npro, nsite, obs, exp, p))

print()
print("== young-modification benchmark ==")
hist_all = [s for s in site_mods if s[0] in hist_acc]
hist_multi = sum(1 for s in hist_all if len(site_mods[s])>=2)
def fisher(a,b,c,d):
    n=a+b+c+d; r1=a+b; c1=a+c
    def pmf(x): return math.comb(c1,x)*math.comb(n-c1,r1-x)/math.comb(n,r1)
    obs=pmf(a); tot=0.0
    for x in range(max(0,c1-(n-r1)), min(r1,c1)+1):
        v=pmf(x)
        if v<=obs*(1+1e-7): tot+=v
    return tot
kla = [s for s,v in site_mods.items() if "Lactylation" in v]
kla_multi = sum(1 for s in kla if len(site_mods[s])>=2)
print("Lactylation: %d sites (histone %d), multi=%d (%.0f%%) vs histone base %.1f%%, p=%.4f" % (
    len(kla), len([s for s in kla if s[0] in hist_acc]), kla_multi, 100*kla_multi/len(kla),
    100*hist_multi/len(hist_all), fisher(kla_multi, len(kla)-kla_multi, hist_multi, len(hist_all)-hist_multi)))
hib = [s for s,v in site_mods.items() if "2-Hydroxyisobutyrylation" in v]
hib_multi = sum(1 for s in hib if len(site_mods[s])>=2)
print("2-Hydroxyisobutyrylation: %d sites, multi=%d (%.0f%%)" % (len(hib), hib_multi, 100*hib_multi/len(hib)))
