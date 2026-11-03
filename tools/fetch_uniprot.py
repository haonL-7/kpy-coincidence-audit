
import os, json, urllib.request, gzip
import pandas as pd
BASE = os.environ.get("KPY_BASE", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
base = os.path.join(BASE, "data")
out = os.path.join(base, "uniprot"); os.makedirs(out, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
kpy = pd.read_csv(os.path.join(base, "kpy_sites.csv"))
accs = sorted(set(kpy["Uniprot ID"].astype(str).str.strip()))
ok=0; fail=[]
for a in accs:
    dest = os.path.join(out, a + ".json")
    if os.path.exists(dest) and os.path.getsize(dest) > 500: ok+=1; continue
    try:
        req = urllib.request.Request("https://rest.uniprot.org/uniprotkb/" + a + ".json",
                                     headers={"User-Agent":UA, "Accept-Encoding":"gzip"})
        r = urllib.request.urlopen(req, timeout=60)
        raw = r.read()
        if r.headers.get("Content-Encoding") == "gzip": raw = gzip.decompress(raw)
        open(dest,"wb").write(raw); ok+=1
    except Exception as e:
        fail.append((a, str(e)[:50]))
print("fetched:", ok, "/", len(accs), "| failed:", fail[:5])
# sample check
import glob

import os
f = os.path.join(out, "P62805.json")
if os.path.exists(f):
    j = json.load(open(f, encoding="utf-8"))
    mods = [x for x in j.get("features", []) if x.get("type") == "Modified residue"]
    print("P62805 MOD_RES features:", len(mods))
    for m in mods[:6]:
        print("  pos", m["location"]["start"]["value"], "|", m["description"][:45], "| evidences:", len(m.get("evidences", [])))
