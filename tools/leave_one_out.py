
import sys, os, glob, math
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import pandas as pd
from collections import defaultdict
B = os.environ.get("KPY_BASE", r"C:\Users\Administrator\Desktop\丙酮酰化")
site = defaultdict(set)
for f in sorted(glob.glob(os.path.join(B,"data","cplm","*","*.txt"))):
    m = os.path.basename(os.path.dirname(f))
    df = pd.read_csv(f, sep="\t", header=None, usecols=[1,2,5], names=["acc","pos","sp"], dtype=str, on_bad_lines="skip")
    df = df[df["sp"].fillna("").str.contains("Homo sapiens", na=False)].dropna(subset=["acc","pos"])
    df = df[df["pos"].str.match(r"^\d+$", na=False)]
    for a,p in zip(df.acc.str.strip(), df.pos.astype(int)): site[(a,p)].add(m)

def loo(Y):
    others = lambda v: v - {Y}
    strata = defaultdict(lambda: [0,0,0,0])
    for s, v in site.items():
        q = (Y in v) and len(others(v)) >= 1          # Y site that is also in C_{-Y}
        o = len(others(v)) >= 2                        # multi within the other eight
        c = strata[s[0]]
        if q and o: c[0]+=1
        elif q: c[1]+=1
        elif o: c[2]+=1
        else: c[3]+=1
    num=den=E=V=0.0; O=0; K=0
    for k,(a,b,c_,d) in strata.items():
        n=a+b+c_+d
        if n<2 or (a+b)==0 or (c_+d)==0: continue
        K+=1; R1,C1=a+b,a+c_
        num+=a*d/n; den+=b*c_/n; E+=R1*C1/n
        V+=(R1*(c_+d)*C1*(b+d))/(n*n*(n-1)); O+=a
    if den==0 or V<=0: return None
    OR=num/den; z=(O-E)/math.sqrt(V); se=math.sqrt(V)/num
    return dict(K=K,O=O,E=E,OR=OR,lo=math.exp(math.log(OR)-1.96*se),hi=math.exp(math.log(OR)+1.96*se),
                p=math.erfc(abs(z)/math.sqrt(2)), nq=sum(v[0]+v[1] for v in strata.values()))

mods = ["Acetylation","Crotonylation","2-Hydroxyisobutyrylation","Malonylation","Succinylation",
        "Butyrylation","Lactylation","Glutarylation","Propionylation"]
print("%-26s %6s %5s %6s %8s %8s %8s" % ("modification (leave-one-out)","query","K","obs","MH OR","CI low","CI high"))
res = {}
for m in mods:
    r = loo(m)
    if r:
        res[m] = r
        print("%-26s %6d %5d %6d %8.2f %8.2f %8.2f  P=%.1e" % (m, r["nq"], r["K"], r["O"], r["OR"], r["lo"], r["hi"], r["p"]))
    else:
        print("%-26s : degenerate" % m)

# Kpy under the same specification: query = Kpy sites in the catalogue, outcome = >=2 of the nine
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
num=den=E=V=0.0; O=0; K=0
for k,(a,b,c_,d) in strata.items():
    n=a+b+c_+d
    if n<2 or (a+b)==0 or (c_+d)==0: continue
    K+=1; R1,C1=a+b,a+c_
    num+=a*d/n; den+=b*c_/n; E+=R1*C1/n; V+=(R1*(c_+d)*C1*(b+d))/(n*n*(n-1)); O+=a
print("\nKpy (same specification): query=%d K=%d obs=%d OR=%.2f P=%.3f" % (sum(v[0]+v[1] for v in strata.values()), K, O, num/den, math.erfc(abs((O-E)/math.sqrt(V))/math.sqrt(2))))
if res:
    ors = [r["OR"] for r in res.values()]
    print("nine LOO OR range: %.2f - %.2f" % (min(ors), max(ors)))
