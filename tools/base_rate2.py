
import os, glob, re, json, math
from collections import defaultdict, Counter
import pandas as pd
base = r"C:\Users\Administrator\Desktop\丙酮酰化\data"

files = sorted(glob.glob(os.path.join(base, "cplm", "*", "*.txt")))
site_mods = defaultdict(set); gene_of = {}
for f in files:
    mod = os.path.basename(os.path.dirname(f))
    df = pd.read_csv(f, sep="\t", header=None, usecols=[1,2,4,5], names=["acc","pos","gene","sp"], dtype=str, on_bad_lines="skip")
    df = df[df["sp"].fillna("").str.contains("Homo sapiens", na=False)].dropna(subset=["acc","pos"])
    df = df[df["pos"].str.match(r"^\d+$", na=False)]
    for acc, pos, gene in zip(df["acc"].str.strip(), df["pos"].astype(int), df["gene"].fillna("")):
        site_mods[(acc,pos)].add(mod)
        gene_of.setdefault(acc, gene.strip())

HIST = re.compile(r"^(H1|H2A|H2B|H2AX|H3|H4|HIST|CENP)", re.I)
hist_acc = {a for a,g in gene_of.items() if HIST.match(g)}

def fisher(a,b,c,d):
    # two-sided Fisher via scipy if available
    try:
        from scipy.stats import fisher_exact
        return fisher_exact([[a,b],[c,d]])[1]
    except Exception:
        # hypergeometric two-sided approx (log-space)
        n = a+b+c+d; r1 = a+b; c1 = a+c
        def lp(x): return math.lgamma(r1+1)-math.lgamma(x+1)-math.lgamma(r1-x+1)+math.lgamma(n-r1+1)-math.lgamma(c1-x+1)-math.lgamma(n-r1-c1+x+1)-math.lgamma(n+1)
        obs = lp(a); tot = 0.0
        for x in range(max(0, c1-(n-r1)), min(r1, c1)+1):
            v = lp(x)
            if v <= obs + 1e-9: tot += math.exp(v)
        return min(1.0, tot)

kpy = pd.read_csv(os.path.join(base, "kpy_sites.csv"))
kpy["acc"] = kpy["Uniprot ID"].astype(str).str.strip(); kpy["pos"] = kpy["Positions within proteins"].astype(int)
ks = list(zip(kpy["acc"], kpy["pos"]))
kpy_hist = [s for s in ks if s[0] in hist_acc]

def stats(group, label):
    ann = [s for s in group if s in site_mods]
    m = [s for s in ann if len(site_mods[s])>=2]
    return len(group), len(ann), len(m)

h = stats(kpy_hist, "h"); nh = stats([s for s in ks if s not in set(kpy_hist)], "nh"); al = stats(ks, "all")
hist_all = [s for s in site_mods if s[0] in hist_acc]
hist_multi = sum(1 for s in hist_all if len(site_mods[s])>=2)

print("== Fisher tests: Kpy multi-mod rate vs CPLM base rate (conditional on being annotated) ==")
p1 = fisher(9, 1, hist_multi, len(hist_all)-hist_multi)
print("histone      : Kpy 9/10 (90%%) vs CPLM histone %d/%d (%.1f%%)  p=%.4f" % (hist_multi, len(hist_all), 100*hist_multi/len(hist_all), p1))
non_all = [s for s in site_mods if s[0] not in hist_acc]
non_multi = sum(1 for s in non_all if len(site_mods[s])>=2)
p2 = fisher(nh[2], nh[1]-nh[2], non_multi, len(non_all)-non_multi)
print("non-histone  : Kpy %d/%d (%.0f%%) vs CPLM non-histone %d/%d (%.1f%%)  p=%.4f" % (nh[2], nh[1], 100*nh[2]/nh[1], non_multi, len(non_all), 100*non_multi/len(non_all), p2))
p3 = fisher(al[2], al[1]-al[2], hist_multi+non_multi, len(hist_all)+len(non_all)-(hist_multi+non_multi))
print("all          : Kpy %d/%d (%.0f%%) vs CPLM all %d/%d (%.1f%%)  p=%.4f" % (al[2], al[1], 100*al[2]/al[1], hist_multi+non_multi, len(site_mods), 100*(hist_multi+non_multi)/len(site_mods), p3))

print()
print("== annotation rate of Kpy sites (the confounder) ==")
print("histone Kpy annotated: %d/%d = %.0f%%" % (h[1], h[0], 100*h[1]/h[0]))
print("non-hist Kpy annotated: %d/%d = %.0f%%" % (nh[1], nh[0], 100*nh[1]/nh[0]))

print()
print("== young-modification benchmark: Lactylation ==")
kla = {(s) for s,v in site_mods.items() if "Lactylation" in v}
kla_hist = [s for s in kla if s[0] in hist_acc]
kla_multi = sum(1 for s in kla if len(site_mods[s])>=2)
print("Kla sites in CPLM: %d, histone %d (%.0f%%), multi-mod %d (%.0f%%)" %
      (len(kla), len(kla_hist), 100*len(kla_hist)/len(kla), kla_multi, 100*kla_multi/len(kla)))

print()
print("== proteins ranked by annotation density (annotated Lys / total Lys) ==")
import urllib.request, urllib.parse
accs = sorted({a for a,_ in ks})
seqs = {}
for i in range(0, len(accs), 25):
    q = " OR ".join("accession:"+a for a in accs[i:i+25])
    url = "https://rest.uniprot.org/uniprotkb/search?query=" + urllib.parse.quote(q) + "&fields=accession,sequence&format=tsv&size=500"
    txt = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent":"dsh/1.0"}), timeout=90).read().decode()
    for line in txt.splitlines()[1:]:
        p = line.split("\t")
        if len(p)>=2: seqs[p[0].strip()] = p[1].strip()
rows = []
for a in accs:
    K = seqs[a].count("K") if a in seqs else 0
    ann = sum(1 for s in site_mods if s[0]==a)
    rows.append((a, gene_of.get(a,""), K, ann, ann/K if K else 0))
rows.sort(key=lambda x: -x[4])
for r in rows[:8]:
    print("  %-10s %-8s Lys=%3d annotated=%3d density=%.2f %s" % (r[0], r[1][:8], r[2], r[3], r[4], "<- histone" if r[0] in hist_acc else ""))
dens_all = [r[4] for r in rows if r[2] > 0]
print("median density across 63 Kpy proteins: %.3f" % (sorted(dens_all)[len(dens_all)//2]))
json.dump({"hist_p":p1,"non_p":p2,"all_p":p3}, open(os.path.join(base,"fisher.json"),"w"))
