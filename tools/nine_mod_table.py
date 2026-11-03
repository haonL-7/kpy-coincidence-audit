
import sys, os, glob, math, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import pandas as pd
from collections import defaultdict
from math import comb
B = os.environ.get("KPY_BASE", r"C:\Users\Administrator\Desktop\丙酮酰化")
site = defaultdict(set); gene = {}
for f in sorted(glob.glob(os.path.join(B, "data", "cplm", "*", "*.txt"))):
    m = os.path.basename(os.path.dirname(f))
    df = pd.read_csv(f, sep="\t", header=None, usecols=[1,2,4,5], names=["acc","pos","g","sp"], dtype=str, on_bad_lines="skip")
    df = df[df["sp"].fillna("").str.contains("Homo sapiens", na=False)].dropna(subset=["acc","pos"])
    df = df[df["pos"].str.match(r"^\d+$", na=False)]
    for a,p,g in zip(df.acc.str.strip(), df.pos.astype(int), df.g.fillna("")):
        site[(a,p)].add(m); gene.setdefault(a, (g or "").strip())
HIST = re.compile(r"^(H1|H2A|H2B|H2AX|H3|H4|HIST|CENP)", re.I)
hist = {a for a,g in gene.items() if HIST.match(g)}
N = len(site); NM = sum(1 for s in site if len(site[s]) >= 2)
base = NM/N

def hyper_upper(k, n, K, Ntot):
    # P(X >= k) with X ~ Hypergeom(Ntot, K, n)
    tot = 0.0
    for x in range(k, min(n, K)+1):
        tot += comb(K, x)*comb(Ntot-K, n-x)/comb(Ntot, n)
    return tot

def analyse(query, label, exact_p=None):
    q = sorted(query)
    n = len(q); k = sum(1 for s in q if len(site.get(s, ()))>=2)
    pA = hyper_upper(k, n, NM, N)
    qh = [s for s in q if s[0] in hist]; qn = [s for s in q if s[0] not in hist]
    kh = sum(1 for s in qh if len(site.get(s,()))>=2); kn = sum(1 for s in qn if len(site.get(s,()))>=2)
    Kh = sum(1 for s in site if s[0] in hist and len(site[s])>=2); Nh = sum(1 for s in site if s[0] in hist)
    Kn = NM - Kh; Nn = N - Nh
    pBh = hyper_upper(kh, len(qh), Kh, Nh) if qh else float("nan")
    pBn = hyper_upper(kn, len(qn), Kn, Nn) if qn else float("nan")
    # D: within-protein MH
    strata = defaultdict(lambda: [0,0,0,0])
    qs = set(q)
    for s, v in site.items():
        if s[0] not in gene: continue
        a_ = s[0]; isq = s in qs; ism = len(v) >= 2; c = strata[a_]
        if isq and ism: c[0]+=1
        elif isq: c[1]+=1
        elif ism: c[2]+=1
        else: c[3]+=1
    num=den=E=V=O=0.0; K=0
    for a_,(a,b,c,d) in strata.items():
        nn = a+b+c+d
        if nn < 2 or (a+b)==0 or (c+d)==0: continue
        K += 1; R1,C1 = a+b, a+c
        num += a*d/nn; den += b*c/nn; E += R1*C1/nn
        V += (R1*(c+d)*C1*(b+d))/(nn*nn*(nn-1)); O += a
    OR = num/den if den else float("nan")
    z = (O-E)/math.sqrt(V) if V > 0 else float("nan")
    pD = math.erfc(abs(z)/math.sqrt(2)) if V > 0 else float("nan")
    return dict(label=label, n=n, k=k, rate=100*k/n, pA=pA, pBh=pBh, pBn=pBn, strata=K, OR=OR, pD=pD, exact=exact_p)

mods = ["Acetylation","Crotonylation","2-Hydroxyisobutyrylation","Malonylation","Succinylation",
        "Butyrylation","Lactylation","Glutarylation","Propionylation"]
rows = []
for m in mods:
    rows.append(analyse([s for s,v in site.items() if m in v], m, None))
kpy = pd.read_csv(os.path.join(B, "data", "kpy_sites.csv"))
kpy["acc"] = kpy["Uniprot ID"].astype(str).str.strip(); kpy["pos"] = kpy["Positions within proteins"].astype(int)
ks = [(a,int(p)) for a,p in zip(kpy.acc, kpy.pos)]
rows.append(analyse([s for s in ks if s in site], "Kpy", 0.224))

print("%-26s %6s %5s %6s %6s %6s %7s %5s %6s %7s" % ("modification","n","multi","rate%","P_A","P_Bh","P_Bn","K","MH OR","P_D"))
for r in rows:
    print("%-26s %6d %5d %6.1f %6s %6s %6s %5d %6.2f %7.3f" % (
        r["label"], r["n"], r["k"], r["rate"],
        ("%.1e"%r["pA"]) if r["pA"]==r["pA"] else "-",
        ("%.3f"%r["pBh"]) if r["pBh"]==r["pBh"] else "-",
        ("%.3f"%r["pBn"]) if r["pBn"]==r["pBn"] else "-",
        r["strata"], r["OR"], r["pD"]))
