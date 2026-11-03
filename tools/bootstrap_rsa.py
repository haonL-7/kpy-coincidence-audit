
import sys, os, glob, math, random
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import pandas as pd, numpy as np
from collections import defaultdict
BASE = os.environ.get("KPY_BASE", r"C:\Users\Administrator\Desktop\丙酮酰化")
site = defaultdict(set)
for f in sorted(glob.glob(os.path.join(BASE,"data","cplm","*","*.txt"))):
    m = os.path.basename(os.path.dirname(f))
    df = pd.read_csv(f, sep="\t", header=None, usecols=[1,2,5], names=["acc","pos","sp"], dtype=str, on_bad_lines="skip")
    df = df[df["sp"].fillna("").str.contains("Homo sapiens", na=False)].dropna(subset=["acc","pos"])
    df = df[df["pos"].str.match(r"^\d+$", na=False)]
    for a,p in zip(df.acc.str.strip(), df.pos.astype(int)): site[(a,p)].add(m)
rsa = pd.read_csv(os.path.join(BASE,"data","rsa_table.csv"))
lys = rsa[rsa.resname=="LYS"].copy()
lys["nmod"] = [len(site.get((a,int(p)),())) for a,p in zip(lys.acc, lys.resseq)]
m = lys[lys.nmod>=2]; s1 = lys[lys.nmod==1]
obs = m.rsa.median() - s1.rsa.median()
rng = np.random.default_rng(5)
boot = []
for _ in range(4000):
    a = m.rsa.sample(len(m), replace=True, random_state=int(rng.integers(1e9)))
    b = s1.rsa.sample(len(s1), replace=True, random_state=int(rng.integers(1e9)))
    boot.append(a.median()-b.median())
boot = np.array(boot)
print("median RSA: multi %.3f single %.3f diff %+.3f  bootstrap 95%% CI %+.3f to %+.3f" % (
    m.rsa.median(), s1.rsa.median(), obs, np.percentile(boot,2.5), np.percentile(boot,97.5)))
dm = (m.plddt<50).mean()*100; ds = (lys.plddt<50).mean()*100
print("disordered: multi %.1f%% | all lysines %.1f%%" % (dm, ds))
