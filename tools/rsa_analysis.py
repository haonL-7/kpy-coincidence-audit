
import os, glob, numpy as np, pandas as pd, math
from collections import defaultdict
base = r"C:\Users\Administrator\Desktop\丙酮酰化\data"
rsa = pd.read_csv(os.path.join(base, "rsa_table.csv"))
rsa_key = {(a,p): (r, l) for a,p,r,l in zip(rsa.acc, rsa.resents if "resents" in rsa else rsa.resents_num, rsa.rsa, rsa.plddt)} if False else None
rsa_key = {(a,int(p)): (rr, ld) for a,p,rr,ld in zip(rsa.acc, rsa.resseq, rsa.rsa, rsa.plddt)}

files = sorted(glob.glob(os.path.join(base, "cplm", "*", "*.txt")))
site_mods = defaultdict(set)
keep = set(rsa.acc)
for f in files:
    mod = os.path.basename(os.path.dirname(f))
    df = pd.read_csv(f, sep="\t", header=None, usecols=[1,2,5], names=["acc","pos","sp"], dtype=str, on_bad_lines="skip")
    df = df[df["sp"].fillna("").str.contains("Homo sapiens", na=False)].dropna(subset=["acc","pos"])
    df = df[df["acc"].isin(keep) & df["pos"].str.match(r"^\d+$", na=False)]
    for a,p in zip(df["acc"].str.strip(), df["pos"].astype(int)):
        site_mods[(a,p)].add(mod)

lys_all = [(a,int(p)) for a,p,rn in zip(rsa.acc, rsa.resseq, rsa.resname) if rn == "LYS"]
kpy = pd.read_csv(os.path.join(base, "kpy_sites.csv"))
kpy["acc"]=kpy["Uniprot ID"].astype(str).str.strip(); kpy["pos"]=kpy["Positions within proteins"].astype(int)
kpy_sites = [(a,int(p)) for a,p in zip(kpy["acc"],kpy["pos"]) if (a,int(p)) in rsa_key]
ann = [s for s in lys_all if s in site_mods]
multi = [s for s in ann if len(site_mods[s])>=2]
print("lysines in structures:", len(lys_all), "| annotated:", len(ann), "| multi-mod:", len(multi), "| Kpy sites:", len(kpy_sites))

def summ(name, group):
    if not group: return None
    v = np.array([rsa_key[s][0] for s in group]); d = np.array([rsa_key[s][1] for s in group])
    return dict(group=name, n=len(v), med_rsa=round(float(np.median(v)),3),
                pct_exposed=round(100*float((v>0.5).mean()),1),
                pct_buried=round(100*float((v<0.25).mean()),1),
                med_plddt=round(float(np.median(d)),1),
                pct_disordered=round(100*float((d<50).mean()),1))
rows = [summ("all Lys", lys_all), summ("CPLM-annotated", ann), summ("multi-mod", multi), summ("Kpy sites", kpy_sites)]
print()
print(pd.DataFrame([r for r in rows if r]).to_string(index=False))

def ranksum(x, y):
    x=np.array(x); y=np.array(y); n1,n2=len(x),len(y)
    allv=np.concatenate([x,y]); r=pd.Series(allv).rank().values
    R1=r[:n1].sum(); U=R1-n1*(n1+1)/2
    mu=n1*n2/2
    _,cnt=np.unique(allv,return_counts=True)
    tie=(cnt**3-cnt).sum()
    N=n1+n2
    var=n1*n2/12*((N+1)-tie/(N*(N-1)))
    z=(U-mu)/math.sqrt(var) if var>0 else 0
    p=2*(1-0.5*math.erfc(abs(z)/math.sqrt(2)))
    return round(z,2), round(p,4)

rx=lambda g:[rsa_key[s][0] for s in g]
print()
print("RSA comparisons (rank-sum):")
print("  Kpy vs other Lys        z,p =", ranksum(rx(kpy_sites), rx([s for s in lys_all if s not in set(kpy_sites)])))
print("  multi vs single (annot) z,p =", ranksum(rx(multi), rx([s for s in ann if s not in set(multi)])))
print("  Kpy vs multi            z,p =", ranksum(rx(kpy_sites), rx(multi)))
print("  Kpy vs annotated-single z,p =", ranksum(rx(kpy_sites), rx([s for s in ann if s not in set(multi)])))

print()
print("multi-mod rate by RSA bin (annotated lysines):")
bins=[0,0.15,0.3,0.45,0.6,1.01]
for lo,hi in zip(bins[:-1],bins[1:]):
    g=[s for s in ann if lo<=rsa_key[s][0]<hi]
    if g: print("  RSA %.2f-%.2f  n=%4d  multi=%.1f%%" % (lo,hi,len(g),100*sum(1 for s in g if len(site_mods[s])>=2)/len(g)))

print()
print("pLDDT-ordered subset (Kpy sites) restated vs all lysines:", )
rsa.to_csv(os.path.join(base,"rsa_table.csv"), index=False)
