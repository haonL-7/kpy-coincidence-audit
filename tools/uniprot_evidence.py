
import os, json, gzip, glob, statistics as st
from collections import defaultdict
import pandas as pd
base = r"C:\Users\Administrator\Desktop\丙酮酰化\data"
up = os.path.join(base, "uniprot")
recs = {}
for f in glob.glob(os.path.join(up, "*.json")):
    raw = open(f,"rb").read()
    if raw[:2] == b"\x1f\x8b": raw = gzip.decompress(raw)
    try: recs[os.path.basename(f)[:-5]] = json.loads(raw.decode("utf-8"))
    except Exception as e: print("decode fail", os.path.basename(f), str(e)[:40])
print("entries parsed:", len(recs))
seq = {a: j.get("sequence",{}).get("value","") for a,j in recs.items()}

pos_mods = defaultdict(set); pos_refs = defaultdict(set)
for a, j in recs.items():
    for ft in j.get("features", []):
        if ft.get("type") != "Modified residue": continue
        p = ft["location"]["start"]["value"]
        pos_mods[(a,p)].add((ft.get("description") or "").split(";")[0].strip())
        for ev in ft.get("evidences", []):
            src = ev.get("source")
            sid = src.get("id") if isinstance(src, dict) else src
            if sid: pos_refs[(a,p)].add(str(sid))

lys = {a: [i+1 for i,c in enumerate(s)] if False else [i+1 for i,c in enumerate(s) if c=="K"] for a,s in seq.items()}
total_lys = sum(len(v) for v in lys.values())
annot = [k for k in pos_mods if k[1] in set(lys.get(k[0], []))]
print("lysines in 63 proteins:", total_lys, "| UniProt-annotated lysine positions:", len(annot))

kpy = pd.read_csv(os.path.join(base,"kpy_sites.csv"))
kpy["acc"]=kpy["Uniprot ID"].astype(str).str.strip(); kpy["pos"]=kpy["Positions within proteins"].astype(int)
ks = [(a,int(p)) for a,p in zip(kpy["acc"],kpy["pos"])]
in_up = [s for s in ks if s in pos_mods]
refcnt = lambda s: len(pos_refs.get(s, ()))

print()
print("Kpy sites: %d | in UniProt: %d | with PubMed refs: %d" % (len(ks), len(in_up), sum(1 for s in in_up if pos_refs.get(s))))
kpy_r = [refcnt(s) for s in ks]; all_r = [refcnt((a,p)) for a in lys for p in lys[a]]
print("refs per site  Kpy median %.1f mean %.2f | all lysines median %.1f mean %.2f" % (st.median(kpy_r), sum(kpy_r)/len(kpy_r), st.median(all_r), sum(all_r)/len(all_r)))

# multi-mod (CPLM) vs evidence depth
import glob as g2
site_mods = defaultdict(set)
for f in sorted(g2.glob(os.path.join(base,"cplm","*","*.txt"))):
    mod = os.path.basename(os.path.dirname(f))
    df = pd.read_csv(f, sep="\t", header=None, usecols=[1,2,5], names=["acc","pos","sp"], dtype=str, on_bad_lines="skip")
    df = df[df["sp"].fillna("").str.contains("Homo sapiens", na=False)].dropna(subset=["acc","pos"])
    df = df[df["acc"].isin(set(lys)) & df["pos"].str.match(r"^\d+$", na=False)]
    for a,p in zip(df["acc"].str.strip(), df["pos"].astype(int)): site_mods[(a,p)].add(mod)
ann = [s for s in site_mods if s[1] in set(lys.get(s[0],[]))]
multi = [s for s in ann if len(site_mods[s])>=2]
sing = [s for s in ann if len(site_mods[s])==1]
m_r=[refcnt(s) for s in multi]; s_r=[refcnt(s) for s in sing]
print()
print("CPLM multi-mod sites: n=%d median refs %.1f mean %.2f" % (len(multi), st.median(m_r), sum(m_r)/len(m_r)))
print("CPLM single-mod sites: n=%d median refs %.1f mean %.2f" % (len(sing), st.median(s_r), sum(s_r)/len(s_r)))
uniq = [k for k in annot if (k not in site_mods)]
print("UniProt-only annotated lysines (not in CPLM): n=%d median refs %.1f" % (len(uniq), st.median([refcnt(s) for s in uniq]) if uniq else 0))
rows=[dict(acc=a,pos=p,up_mods=";".join(sorted(pos_mods.get((a,p),()))),up_refs=refcnt((a,p)),
           cplm_mods=len(site_mods.get((a,p),()))) for a in lys for p in lys[a]]
pd.DataFrame(rows).to_csv(os.path.join(base,"uniprot_lysines.csv"), index=False)
print("saved uniprot_lysines.csv rows:", len(rows))
