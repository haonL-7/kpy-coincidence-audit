
import os, glob, json, urllib.request, io
import pandas as pd
base = r"C:\Users\Administrator\Desktop\丙酮酰化\data"
ws = r"C:\Users\Administrator\Desktop\丙酮酰化"

kpy = pd.read_csv(os.path.join(base, "kpy_sites.csv"))
kpy.columns = [c.strip() for c in kpy.columns]
kpy["Uniprot ID"] = kpy["Uniprot ID"].astype(str).str.strip()
kpy["pos"] = kpy["Positions within proteins"].astype(int)
accs = sorted(set(kpy["Uniprot ID"]))
print("kpy sites:", len(kpy), "proteins:", len(accs))

# 1) sequences from UniProt
seqs = {}
for i in range(0, len(accs), 25):
    chunk = accs[i:i+25]
    q = " OR ".join("accession:" + a for a in chunk)
    url = ("https://rest.uniprot.org/uniprotkb/search?query=" + urllib.parse.quote(q) +
           "&fields=accession,sequence&format=tsv&size=500")
    req = urllib.request.Request(url, headers={"User-Agent": "dsh-analysis/1.0"})
    txt = urllib.request.urlopen(req, timeout=90).read().decode("utf-8")
    for line in txt.splitlines()[1:]:
        p = line.split("\t")
        if len(p) >= 2: seqs[p[0].strip()] = p[1].strip()
print("sequences fetched:", len(seqs))
LysCount = {a: s.count("K") for a, s in seqs.items()}
missing = [a for a in accs if a not in seqs]
print("missing seqs:", missing[:10], "n=", len(missing))

# 2) load CPLM human sites
files = sorted(glob.glob(os.path.join(base, "cplm", "*", "*.txt")))
modsites = {}; modsites_in_kpy = {}
perp = {}
for f in files:
    mod = os.path.basename(os.path.dirname(f))
    try:
        df = pd.read_csv(f, sep="\t", header=None, usecols=[1,2,5], names=["acc","pos","sp"], dtype=str, on_bad_lines="skip")
    except Exception as e:
        print("read fail", mod, e); continue
    df["sp"] = df["sp"].fillna("")
    df = df[df["sp"].str.contains("Homo sapiens", na=False)]
    df = df.dropna(subset=["acc","pos"])
    df = df[df["pos"].str.match(r"^\d+$", na=False)]
    df["pos"] = df["pos"].astype(int)
    s = set(zip(df["acc"].str.strip(), df["pos"]))
    modsites[mod] = s
    d = {}
    for a, p in s: d.setdefault(a, set()).add(p)
    perp[mod] = d
    print(mod, "human sites:", len(s), "proteins:", len(d))

# 3) overlap + expectation
res = []
kpy_site_set = set(zip(kpy["Uniprot ID"], kpy["pos"]))
any_hit = {}
for mod, s in modsites.items():
    obs = len(kpy_site_set & s)
    exp = 0.0
    for a, p in kpy_site_set:
        K = LysCount.get(a, 0)
        m = len(perp[mod].get(a, ()))
        if K > 0: exp += m / K
    hit_sites = sorted(kpy_site_set & s)
    for h in hit_sites: any_hit.setdefault(h, []).append(mod)
    res.append({"mod": mod, "human_sites": len(s), "overlap": obs, "expected": round(exp,2),
                "enrichment": round(obs/exp,2) if exp>0 else None, "sites": hit_sites})

out = pd.DataFrame(res).sort_values("overlap", ascending=False)
print()
print(out[["mod","human_sites","overlap","expected","enrichment"]].to_string(index=False))
print()
print("Kpy sites with >=1 other acylation:", len(any_hit), "/", len(kpy_site_set))
for k, v in sorted(any_hit.items(), key=lambda x: -len(x[1]))[:15]:
    print("  ", k, "->", ",".join(sorted(v)))

json.dump({"kpy_total": len(kpy_site_set), "with_any": len(any_hit),
           "by_mod": {r["mod"]: r for r in res},
           "detail": {f"{a}_{p}": v for (a,p), v in any_hit.items()}},
          open(os.path.join(base, "overlap_result.json"), "w"), indent=1)
print("saved overlap_result.json")
