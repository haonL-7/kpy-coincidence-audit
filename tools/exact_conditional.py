
import sys, os, glob, math, random
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import pandas as pd
from collections import defaultdict
root = os.environ.get("KPY_BASE", r"C:\Users\Administrator\Desktop\丙酮酰化")
data = os.path.join(root, "data")

site=defaultdict(set)
for f in sorted(glob.glob(os.path.join(data,"cplm","*","*.txt"))):
    mod=os.path.basename(os.path.dirname(f))
    df=pd.read_csv(f,sep="\t",header=None,usecols=[1,2,5],names=["acc","pos","sp"],dtype=str,on_bad_lines="skip")
    df=df[df["sp"].fillna("").str.contains("Homo sapiens",na=False)].dropna(subset=["acc","pos"])
    df=df[df["pos"].str.match(r"^\d+$",na=False)]
    for a,p in zip(df.acc.str.strip(),df.pos.astype(int)): site[(a,p)].add(mod)

kpy=pd.read_csv(os.path.join(data,"kpy_sites.csv"))
kpy["acc"]=kpy["Uniprot ID"].astype(str).str.strip(); kpy["pos"]=kpy["Positions within proteins"].astype(int)
ks=set((a,int(p)) for a,p in zip(kpy.acc,kpy.pos))

strata=defaultdict(lambda:[0,0,0,0])
for s in site:
    a=s[0]; is_k=s in ks; is_m=len(site[s])>=2
    c=strata[a]
    if is_k and is_m: c[0]+=1
    elif is_k: c[1]+=1
    elif is_m: c[2]+=1
    else: c[3]+=1

usable={k:v for k,v in strata.items() if sum(v)>1 and (v[0]+v[1])>0 and (v[2]+v[3])>0}
print("usable strata:", len(usable))
obs = sum(v[0] for v in usable.values())
print("observed multi among Kpy sites:", obs)

# ---- exact conditional (CMH) test by convolution ----
from math import comb
def hyper_dist(n, R1, C1):
    lo=max(0, R1+C1-n); hi=min(R1, C1)
    tot=comb(n, R1)
    return {x: comb(C1,x)*comb(n-C1, R1-x)/tot for x in range(lo, hi+1)}, lo, hi

dist={0:1.0}
exp_total=0.0
for k,(a,b,c,d) in usable.items():
    n=a+b+c+d; R1=a+b; C1=a+c
    pd_, lo, hi = hyper_dist(n, R1, C1)
    new=defaultdict(float)
    for t,pt in dist.items():
        for x,px in pd_.items():
            new[t+x]+=pt*px
    dist=dict(new)
    exp_total += R1*C1/n

p_obs = dist.get(obs, 0.0)
p_exact = sum(p for t,p in dist.items() if p <= p_obs*(1+1e-12))
print("null mean of the total: %.2f | observed: %d" % (exp_total, obs))
print("exact conditional (CMH) two-sided P = %.3f" % min(1.0, p_exact))

# ---- MH OR with RBG variance (correct variance on the raw sum, not on log OR) ----
num=den=0.0; vsum=0.0
for k,(a,b,c,d) in usable.items():
    n=a+b+c+d; R1=a+b; R2=c+d; C1=a+c; C2=b+d
    if num is not None:
        num += a*d/n; den += b*c/n
    vsum += (R1*R2*C1*C2)/(n*n*(n-1))
OR=num/den
z=(obs-exp_total)/math.sqrt(vsum)
print("MH OR = %.2f" % OR)
print("z from raw-sum variance = %.2f -> asymptotic P = %.3f" % (z, math.erfc(abs(z)/math.sqrt(2))))

# ---- permutation, same statistic, many draws ----
def perm(iters, seed):
    random.seed(seed); cnt=0
    pool={k:[s for s in site if s[0]==k] for k in usable}
    for _ in range(iters):
        tot=0
        for k,(a,b,c,d) in usable.items():
            draws=a+b
            samp=random.sample(pool[k], draws)
            tot += sum(1 for s in samp if len(site[s])>=2)
        if tot>=obs: cnt+=1
    return cnt/iters
for seed in (1,2,3):
    print("permutation seed %d: P = %.3f" % (seed, perm(3000, seed)))
