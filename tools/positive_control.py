
import sys, os, glob, math
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import pandas as pd
from collections import defaultdict
B = os.environ.get("KPY_BASE", r"C:\Users\Administrator\Desktop\丙酮酰化")
site = defaultdict(set)
for f in sorted(glob.glob(os.path.join(B, "data", "cplm", "*", "*.txt"))):
    m = os.path.basename(os.path.dirname(f))
    df = pd.read_csv(f, sep="\t", header=None, usecols=[1,2,5], names=["acc","pos","sp"], dtype=str, on_bad_lines="skip")
    df = df[df["sp"].fillna("").str.contains("Homo sapiens", na=False)].dropna(subset=["acc","pos"])
    df = df[df["pos"].str.match(r"^\d+$", na=False)]
    for a,p in zip(df.acc.str.strip(), df.pos.astype(int)): site[(a,p)].add(m)

rsa = pd.read_csv(os.path.join(B, "data", "rsa_table.csv"))
lys = rsa[rsa.resname=="LYS"]
allk = defaultdict(set)
for a,p in zip(lys.acc, lys.resseq.astype(int)): allk[a].add(p)
print("proteins with full lysine lists:", len(allk))

def mh_full(protein_universe, query_mod, outcome_mod):
    strata = defaultdict(lambda: [0,0,0,0]); K=0
    for a_, positions in protein_universe.items():
        q_pos = {p for p in positions if query_mod in site.get((a_,p),())}
        o_pos = {p for p in positions if outcome_mod in site.get((a_,p),())}
        if not q_pos and not o_pos: continue
        a = len(q_pos & o_pos); b = len(q_pos - o_pos)
        c = len(o_pos - q_pos); d = len(positions - q_pos - o_pos)
        if a+b == 0 or c+d == 0: continue
        K += 1
        strata[a_] = [a,b,c,d]
    num=den=E=V=O=0.0
    for k,(a,b,c,d) in strata.items():
        n=a+b+c+d; R1,C1=a+b,a+c
        num+=a*d/n; den+=b*c/n; E+=R1*C1/n
        V+=(R1*(c+d)*C1*(b+d))/(n*n*(n-1)); O+=a
    if den==0 or V<=0: return None
    OR=num/den; z=(O-E)/math.sqrt(V); p=math.erfc(abs(z)/math.sqrt(2)); se=math.sqrt(V)/num
    return dict(K=K,O=int(O),E=round(E,1),OR=OR,lo=math.exp(math.log(OR)-1.96*se),hi=math.exp(math.log(OR)+1.96*se),p=p)

for q,o in [("Crotonylation","Acetylation"),("Acetylation","Crotonylation"),
            ("Succinylation","Acetylation"),("2-Hydroxyisobutyrylation","Acetylation")]:
    r = mh_full(allk, q, o)
    if r:
        print("%-24s -> %-14s K=%2d obs=%4d exp=%7.1f OR=%6.2f CI %5.2f-%-7.1f P=%.2e" % (
            q,o,r["K"],r["O"],r["E"],r["OR"],r["lo"],r["hi"],r["p"]))
    else:
        print("%-24s -> %-14s : no usable strata" % (q,o))
