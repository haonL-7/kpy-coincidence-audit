
import sys, os, glob, math, random
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import pandas as pd
from collections import defaultdict
B = r"C:\Users\Administrator\Desktop\丙酮酰化"
site = defaultdict(set)
for f in sorted(glob.glob(os.path.join(B,"data","cplm","*","*.txt"))):
    m = os.path.basename(os.path.dirname(f))
    df = pd.read_csv(f, sep="\t", header=None, usecols=[1,2,5], names=["acc","pos","sp"], dtype=str, on_bad_lines="skip")
    df = df[df["sp"].fillna("").str.contains("Homo sapiens", na=False)].dropna(subset=["acc","pos"])
    df = df[df["pos"].str.match(r"^\d+$", na=False)]
    for a,p in zip(df.acc.str.strip(), df.pos.astype(int)): site[(a,p)].add(m)
kpy = pd.read_csv(os.path.join(B,"data","kpy_sites.csv"))
kpy["acc"]=kpy["Uniprot ID"].astype(str).str.strip(); kpy["pos"]=kpy["Positions within proteins"].astype(int)
KS = {(a,int(p)) for a,p in zip(kpy.acc,kpy.pos)}

def build(Y, kpy_mode=False):
    strata=defaultdict(lambda:[0,0,0,0]); nsites=0
    for s,v in site.items():
        if kpy_mode:
            q = s in KS; others = len(v)
        else:
            if Y in v: nsites += 1
            others = len(v) - (1 if Y in v else 0)
            q = (Y in v) and others >= 1
        o = others >= 2
        c = strata[s[0]]
        if q and o: c[0]+=1
        elif q: c[1]+=1
        elif o: c[2]+=1
        else: c[3]+=1
    return {k:tuple(v) for k,v in strata.items() if sum(v)>1 and (v[0]+v[1])>0 and (v[2]+v[3])>0}, nsites

def mh(cells):
    num=den=E=V=0.0; O=0
    for (a,b,c,d) in cells:
        n=a+b+c+d; R1,C1=a+b,a+c
        num+=a*d/n; den+=b*c/n; E+=R1*C1/n
        V+=(R1*(c+d)*C1*(b+d))/(n*n*(n-1)); O+=a
    if den==0 or V<=0: return None
    return num/den, (O-E)/math.sqrt(V), O, E

def boot(cells, reps=800, seed=5):
    random.seed(seed); vals=[]
    for _ in range(reps):
        samp=[cells[random.randrange(len(cells))] for _ in cells]
        r=mh(samp)
        if r and r[0] > 0 and math.isfinite(r[0]): vals.append(math.log(r[0]))
    vals.sort()
    return math.exp(vals[int(0.025*len(vals))]), math.exp(vals[int(0.975*len(vals))-1])

mods=["Acetylation","Crotonylation","2-Hydroxyisobutyrylation","Malonylation","Succinylation","Butyrylation","Lactylation","Glutarylation","Propionylation"]
lines=["| Modification | Catalogue sites | Query sites | Informative strata | MH OR | 95% CI | P |",
       "| --- | --- | --- | --- | --- | --- | --- |"]
rows=[]
for m in mods:
    cells, ns = build(m)
    r = mh(list(cells.values()))
    lo,hi = boot(list(cells.values()))
    rows.append(("%-26s %6d %6d %5d OR=%8.2f CI=%6.2f-%-7.2f P=%.1e" % (m, ns, sum(a+b for a,b,c,d in cells.values()), len(cells), r[0], lo, hi,
         math.erfc(abs(r[1])/math.sqrt(2)))))
for line in rows: print(line)
cells, ns = build(None, kpy_mode=True)
r = mh(list(cells.values())); lo,hi = boot(list(cells.values()))
print("%-26s %6d %6d %5d OR=%8.2f CI=%6.2f-%-7.2f P=%.1e" % ("Kpy", 88, sum(a+b for a,b,c,d in cells.values()), len(cells), r[0], lo, hi,
      math.erfc(abs(r[1])/math.sqrt(2))))
