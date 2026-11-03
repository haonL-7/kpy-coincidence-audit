
import os, glob, json, random, urllib.request
import pandas as pd
base = r"C:\Users\Administrator\Desktop\丙酮酰化\data"
kpy = pd.read_csv(os.path.join(base, "kpy_sites.csv"))
kpy["acc"] = kpy["Uniprot ID"].astype(str).str.strip()
kpy["pos"] = kpy["Positions within proteins"].astype(int)
sites = list(zip(kpy["acc"], kpy["pos"]))

files = sorted(glob.glob(os.path.join(base, "cplm", "*", "*.txt")))
allsites = set()
for f in files:
    df = pd.read_csv(f, sep="\t", header=None, usecols=[1,2,5], names=["acc","pos","sp"], dtype=str, on_bad_lines="skip")
    df = df[df["sp"].fillna("").str.contains("Homo sapiens", na=False)].dropna(subset=["acc","pos"])
    df = df[df["pos"].str.match(r"^\d+$", na=False)]
    allsites |= set(zip(df["acc"].str.strip(), df["pos"].astype(int)))

accs = sorted({a for a, _ in sites})
seqs = {}
for i in range(0, len(accs), 25):
    q = " OR ".join("accession:" + a for a in accs[i:i+25])
    url = ("https://rest.uniprot.org/uniprotkb/search?query=" + urllib.parse.quote(q) +
           "&fields=accession,sequence&format=tsv&size=500")
    txt = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent":"dsh/1.0"}), timeout=90).read().decode()
    for line in txt.splitlines()[1:]:
        p = line.split("\t")
        if len(p) >= 2: seqs[p[0].strip()] = p[1].strip()

lys = {a: [i+1 for i, c in enumerate(s) if c == "K"] for a, s in seqs.items()}
obs = sum(1 for s in sites if s in allsites)
random.seed(42)
N = 2000
null = []
hitlists = {a: [p for p in lys[a] if (a, p) in allsites] for a in lys}
for _ in range(N):
    cnt = 0
    for a, _p in sites:
        if not lys[a]: continue
        if random.choice(lys[a]) in set(hitlists[a]): cnt += 1
    null.append(cnt)
mean_null = sum(null)/N
p = sum(1 for x in null if x >= obs)/N
prot_lys = sum(len(v) for v in lys.values())
prot_hit = sum(len(hitlists[a]) for a in lys)
per_gene_k = {}
for a, _p in sites: per_gene_k[a] = per_gene_k.get(a,0)+1
print("Kpy sites:", len(sites), "| with >=1 other acylation:", obs)
print("background: lysines in same proteins:", prot_lys, "with >=1 acylation:", prot_hit, "= %.1f%%" % (100*prot_hit/prot_lys))
print("null mean:", round(mean_null,1), "| empirical p(obs>=null) =", round(p,4))
print("proteins:", len(lys), "| multi-site proteins:", sum(1 for v in per_gene_k.values() if v>1))
print("top multi-site:", sorted(per_gene_k.items(), key=lambda x:-x[1])[:5])
json.dump({"kpy":len(sites),"with_any":obs,"null_mean":round(mean_null,1),"p":p,
           "bg_total":prot_lys,"bg_hit":prot_hit,"bg_pct":round(100*prot_hit/prot_lys,1),
           "proteins":len(lys)}, open(os.path.join(base,"perm_result.json"),"w"))
print("saved perm_result.json")
