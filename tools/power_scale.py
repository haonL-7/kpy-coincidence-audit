
import sys, os, glob, math, random
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import pandas as pd
from collections import defaultdict
from math import comb
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
ks = {(a,int(p)) for a,p in zip(kpy.acc,kpy.pos)}
strata = defaultdict(lambda: [0,0,0,0])
for s,v in site.items():
    q = s in ks; o = len(v)>=2; c = strata[s[0]]
    if q and o: c[0]+=1
    elif q: c[1]+=1
    elif o: c[2]+=1
    else: c[3]+=1
usable = {k:tuple(v) for k,v in strata.items() if sum(v)>1 and (v[0]+v[1])>0 and (v[2]+v[3])>0}
print("Kpy usable strata:", len(usable), "| query sites in them:", sum(a+b for a,b,c,d in usable.values()))
print("strata detail (a,b,c,d):", sorted(usable.items(), key=lambda kv: -(kv[1][0]))[:6])

def power(psi, reps=1500, seed=11):
    random.seed(seed); marg=[(sum(v), v[0]+v[1], v[0]+v[2]) for v in usable.values()]
    rej=0
    for _ in range(reps):
        O=E=V=0.0
        for (n,R1,C1) in marg:
            lo=max(0,R1+C1-n); hi=min(R1,C1)
            w={x: comb(C1,x)*comb(n-C1,R1-x)*(psi**x) for x in range(lo,hi+1)}
            tot=sum(w.values()); r=random.random()*tot; acc=0.0; pick=lo
            for x in sorted(w):
                acc+=w[x]
                if acc>=r: pick=x; break
            O+=pick; E+=R1*C1/n
            V+= (R1*(n-C1)*C1*(n-R1))/(n*n*(n-1)) if n>1 else 0
        z=(O-E)/math.sqrt(V) if V>0 else 0
        if abs(z)>1.96: rej+=1
    return rej/reps
for psi in (2.60, 3.0, 5.19, 8.0, 10.25):
    print("power at OR %.2f = %.2f" % (psi, power(psi)))

# propionylation strata
def loo_detail(Y):
    out=[]
    for s,v in site.items():
        if Y not in v: continue
        others = len(v)-1
        if others < 1: continue
        out.append((s[0], others>=2))
    agg=defaultdict(lambda:[0,0])
    for p,o in out:
        agg[p][1]+=1
        if o: agg[p][0]+=1
    return agg
agg = loo_detail("Propionylation")
print("\npropionylation query strata (both-multi / query):", dict(agg))
