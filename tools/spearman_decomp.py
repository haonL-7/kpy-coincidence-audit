
import sys, os, glob, math, itertools
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import pandas as pd
from collections import defaultdict
BASE = os.environ.get("KPY_BASE", r"C:\Users\Administrator\Desktop\丙酮酰化")
data = os.path.join(BASE, "data")

site = defaultdict(set)
for f in sorted(glob.glob(os.path.join(data, "cplm", "*", "*.txt"))):
    mod = os.path.basename(os.path.dirname(f))
    df = pd.read_csv(f, sep="\t", header=None, usecols=[1,2,4,5], names=["acc","pos","g","sp"], dtype=str, on_bad_lines="skip")
    df = df[df["sp"].fillna("").str.contains("Homo sapiens", na=False)].dropna(subset=["acc","pos"])
    df = df[df["pos"].str.match(r"^\d+$", na=False)]
    for a, p, g in zip(df.acc.str.strip(), df.pos.astype(int), df.g.fillna("")):
        site[(a, p)].add(mod)

import re
HIST = re.compile(r"^(H1|H2A|H2B|H2AX|H3|H4|HIST|CENP)", re.I)
gene = {}
for f in sorted(glob.glob(os.path.join(data, "cplm", "*", "*.txt"))):
    df = pd.read_csv(f, sep="\t", header=None, usecols=[1,2,4], names=["acc","pos","g"], dtype=str, on_bad_lines="skip")
    for a, g in zip(df.acc.str.strip(), df.g.fillna("")):
        gene.setdefault(a, g.strip())
hist = {a for a, g in gene.items() if HIST.match(g)}

rows = []
for m in ["Acetylation","Crotonylation","2-Hydroxyisobutyrylation","Malonylation","Succinylation",
          "Butyrylation","Lactylation","Glutarylation","Propionylation"]:
    ms = [s for s, v in site.items() if m in v]
    n = len(ms); multi = sum(1 for s in ms if len(site[s]) >= 2)
    h = sum(1 for s in ms if s[0] in hist) / n
    rows.append(dict(mod=m, n=n, rate=100*multi/n, hfrac=100*h))
df = pd.DataFrame(rows).sort_values("n", ascending=False)
print(df.to_string(index=False, float_format=lambda x: "%.1f" % x))

def rank(v):
    s = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0]*len(v)
    i = 0
    while i < len(s):
        j = i
        while j+1 < len(s) and v[s[j+1]] == v[s[i]]: j += 1
        avg = (i+j)/2 + 1
        for k in range(i, j+1): r[s[k]] = avg
        i = j+1
    return r

def pearson(x, y):
    mx = sum(x)/len(x); my = sum(y)/len(y)
    num = sum((a-mx)*(b-my) for a, b in zip(x, y))
    den = math.sqrt(sum((a-mx)**2 for a in x)*sum((b-my)**2 for b in y))
    return num/den

x = [math.log10(n) for n in df.n]; y = list(df.rate); z = list(df.hfrac)
rx, ry, rz = rank(x), rank(y), rank(z)
rho = pearson(rx, ry)
rz_x = [a - pearson(rx, rz)*b for a, b in zip(rx, rx)]
# partial Spearman (control for histone share) on ranks
ex = [a - b for a, b in zip(rx, [pearson(rx, rz)*c for c in rz])]
ey = [a - b for a, b in zip(ry, [pearson(ry, rz)*c for c in rz])]
prho = pearson(ex, ey)
print("\nSpearman(log10 n, multi-rate): rho = %.3f  (n=9)" % rho)
print("Spearman(histone share, multi-rate): rho = %.3f" % pearson(rz, ry))
print("partial Spearman controlling histone share: rho = %.3f" % prho)
# permutation p for rho
import random
random.seed(7)
cnt = 0; N = 20000
for _ in range(N):
    yy = y[:]; random.shuffle(yy)
    if abs(pearson(rx, rank(yy))) >= abs(rho): cnt += 1
print("permutation P (two-sided) = %.4f" % (cnt/N))

# ---- decomposition of the A-set excess ----
print("\n-- decomposition of A (15/23 = 65.2% vs global 22.1%) --")
obs = 65.2; within = 100*12.84/23; global_ = 22.1
print("global baseline           : %.1f%%" % global_)
print("expected, same proteins   : %.1f%%  (within-protein permutation, 12.84/23)" % within)
print("observed                  : %.1f%%" % obs)
gap = obs - global_
print("gap                        : %.1f points" % gap)
print("composition share          : %.1f points (%.0f%%)" % (within-global_, 100*(within-global_)/gap))
print("within-protein residual    : %.1f points (%.0f%%)" % (obs-within, 100*(obs-within)/gap))
