
import os, glob, json, math
from collections import defaultdict
import pandas as pd
base = r"C:\Users\Administrator\Desktop\丙酮酰化\data"
files = sorted(glob.glob(os.path.join(base, "cplm", "*", "*.txt")))
site_mods = defaultdict(set); gene_of = {}
for f in files:
    mod = os.path.basename(os.path.dirname(f))
    df = pd.read_csv(f, sep="\t", header=None, usecols=[1,2,4,5], names=["acc","pos","gene","sp"], dtype=str, on_bad_lines="skip")
    df = df[df["sp"].fillna("").str.contains("Homo sapiens", na=False)].dropna(subset=["acc","pos"])
    df = df[df["pos"].str.match(r"^\d+$", na=False)]
    for a,p,g in zip(df["acc"].str.strip(), df["pos"].astype(int), df["gene"].fillna("")):
        site_mods[(a,p)].add(mod); gene_of.setdefault(a, g.strip())

tot = len(site_mods)
base_rate = sum(1 for v in site_mods.values() if len(v)>=2)/tot
per_prot_ann = defaultdict(int); per_prot_multi = defaultdict(int)
for (a,p),v in site_mods.items():
    per_prot_ann[a]+=1
    if len(v)>=2: per_prot_multi[a]+=1

def audit(modname):
    sites = [s for s,v in site_mods.items() if modname in v]
    by_prot = defaultdict(int)
    for a,p in sites: by_prot[a]+=1
    obs = sum(1 for s in sites if len(site_mods[s])>=2)
    E=0.0; V=0.0
    for a,n in by_prot.items():
        N = per_prot_ann[a]; m = per_prot_multi[a]
        if N==0: continue
        p_ = m/N; E += n*p_
        if N>1: V += n*p_*(1-p_)*(N-n)/(N-1)
    z = (obs-E)/math.sqrt(V) if V>0 else 0.0
    # one-sided normal p
    p_val = 0.5*math.erfc(z/math.sqrt(2))
    dens = [per_prot_ann[a]/max(1,per_prot_ann[a]) for a in by_prot]
    return dict(mod=modname, n=len(sites), proteins=len(by_prot),
                obs_multi=obs, obs_rate=round(100*obs/max(1,len(sites)),1),
                exp_multi=round(E,1), exp_rate=round(100*E/max(1,len(sites)),1),
                z=round(z,2), p=round(p_val,4),
                global_rate=round(100*base_rate,1))

rows=[]
for modname in ["Acetylation","2-Hydroxyisobutyrylation","Crotonylation","Succinylation","Malonylation","Butyrylation","Lactylation","Propionylation","Glutarylation"]:
    rows.append(audit(modname))
df = pd.DataFrame(rows)
df = df.sort_values("n", ascending=False)
pd.set_option("display.width", 200)
print("CPLM 4.0 human sites, protein-stratified audit (multi-mod = >=2 distinct mods at same lysine)")
print("global base rate: %.1f%%  (n=%d lysine sites)" % (100*base_rate, tot))
print()
print(df.to_string(index=False))
df.to_csv(os.path.join(base, "audit_table.csv"), index=False, encoding="utf-8-sig")
print()
print("saved audit_table.csv")

# Kpy audit via same protocol
kpy = pd.read_csv(os.path.join(base, "kpy_sites.csv"))
kpy["acc"]=kpy["Uniprot ID"].astype(str).str.strip(); kpy["pos"]=kpy["Positions within proteins"].astype(int)
ks=[(a,p) for a,p in zip(kpy["acc"],kpy["pos"]) if (a,p) in site_mods]
by_prot=defaultdict(int)
for a,p in ks: by_prot[a]+=1
obs=sum(1 for s in ks if len(site_mods[s])>=2); E=0.0; V=0.0
for a,n in by_prot.items():
    N=per_prot_ann[a]; m=per_prot_multi[a]; p_=m/N; E+=n*p_
    if N>1: V+=n*p_*(1-p_)*(N-n)/(N-1)
z=(obs-E)/math.sqrt(V) if V>0 else 0
print()
print("Kpy (88 sites, 23 annotated) via same protocol: obs_multi=%d exp=%.1f z=%.2f p=%.3f" % (obs, E, z, 0.5*math.erfc(z/math.sqrt(2))))
