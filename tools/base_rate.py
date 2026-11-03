
import os, glob, json, re
from collections import defaultdict, Counter
import pandas as pd

base = r"C:\Users\Administrator\Desktop\丙酮酰化\data"
files = sorted(glob.glob(os.path.join(base, "cplm", "*", "*.txt")))

site_mods = defaultdict(set)
gene_of = {}
for f in files:
    mod = os.path.basename(os.path.dirname(f))
    df = pd.read_csv(f, sep="\t", header=None, usecols=[1,2,3,4,5],
                     names=["acc","pos","modcol","gene","sp"], dtype=str, on_bad_lines="skip")
    df = df[df["sp"].fillna("").str.contains("Homo sapiens", na=False)].dropna(subset=["acc","pos"])
    df = df[df["pos"].str.match(r"^\d+$", na=False)]
    for acc, pos, gene in zip(df["acc"].str.strip(), df["pos"].astype(int), df["gene"].fillna("")):
        site_mods[(acc, pos)].add(mod)
        if acc not in gene_of: gene_of[acc] = gene.strip()

print("unique human lysine sites (>=1 mod):", len(site_mods))
nmod = Counter(len(v) for v in site_mods.values())
tot = len(site_mods)
multi = sum(c for k, c in nmod.items() if k >= 2)
print("mods-per-site distribution:", dict(sorted(nmod.items())))
print("multi-mod (>=2) base rate: %d/%d = %.1f%%" % (multi, tot, 100*multi/tot))

HIST = re.compile(r"^(H1|H2A|H2B|H2AX|H3|H4|HIST|CENP)", re.I)
def is_hist(acc):
    g = gene_of.get(acc, "")
    return bool(HIST.match(g))
def is_hist_by_name(acc):
    return bool(HIST.match(gene_of.get(acc, "")))

# global histone vs non-histone base rates
hist_sites = {s: v for s, v in site_mods.items() if is_hist(s[0])}
non_sites  = {s: v for s, v in site_mods.items() if not is_hist(s[0])}
for label, d in [("histone", hist_sites), ("non-histone", non_sites)]:
    m = sum(1 for v in d.values() if len(v) >= 2)
    print("%s: sites=%d multi=%d rate=%.1f%%" % (label, len(d), m, 100*m/len(d)))

# Kpy
kpy = pd.read_csv(os.path.join(base, "kpy_sites.csv"))
kpy["acc"] = kpy["Uniprot ID"].astype(str).str.strip()
kpy["pos"] = kpy["Positions within proteins"].astype(int)
kpy_sites = list(zip(kpy["acc"], kpy["pos"]))
kpy_hist = [s for s in kpy_sites if is_hist_by_name(s[0]) or s[0] in {x[0] for x in hist_sites}]
print()
print("KPY histone-ish sites:", len(kpy_hist), "of", len(kpy_sites))
for lbl, group in [("ALL", kpy_sites), ("histone", kpy_hist), ("non-histone", [s for s in kpy_sites if s not in set(kpy_hist)])]:
    ann = [s for s in group if s in site_mods]
    m = [s for s in ann if len(site_mods[s]) >= 2]
    print("Kpy %-12s n=%3d annotated=%3d (%.0f%%) multi-mod=%2d (%.0f%% of annotated)" %
          (lbl, len(group), len(ann), 100*len(ann)/len(group), len(m), 100*len(m)/len(ann) if ann else 0))

# matched comparator: same 63 proteins
kpy_prots = {a for a, _ in kpy_sites}
matched = [s for s in site_mods if s[0] in kpy_prots]
mm = sum(1 for s in matched if len(site_mods[s]) >= 2)
print()
print("comparator: annotated lysines in the 63 Kpy proteins -> %d sites, multi=%d (%.1f%%)" % (len(matched), mm, 100*mm/len(matched)))
json.dump({"total_sites": tot, "multi_base_rate": round(100*multi/tot,1),
           "hist_sites": len(hist_sites), "hist_multi_rate": round(100*sum(1 for v in hist_sites.values() if len(v)>=2)/len(hist_sites),1),
           "non_sites": len(non_sites), "non_multi_rate": round(100*sum(1 for v in non_sites.values() if len(v)>=2)/len(non_sites),1),
           "matched_sites": len(matched), "matched_multi_rate": round(100*mm/len(matched),1)},
          open(os.path.join(base, "base_rate.json"), "w"))
print("saved base_rate.json")
