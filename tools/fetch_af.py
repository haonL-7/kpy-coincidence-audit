
import os, json, urllib.request, gzip
import pandas as pd
base = r"C:\Users\Administrator\Desktop\丙酮酰化\data"
out = os.path.join(base, "alphafold"); os.makedirs(out, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
def get(u, t=60):
    return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent":UA}), timeout=t).read()
kpy = pd.read_csv(os.path.join(base, "kpy_sites.csv"))
accs = sorted(set(kpy["Uniprot ID"].astype(str).str.strip()))
ok=0; fail=[]
for a in accs:
    dest = os.path.join(out, a + ".pdb")
    if os.path.exists(dest) and os.path.getsize(dest) > 1000: ok+=1; continue
    try:
        j = json.loads(get("https://alphafold.ebi.ac.uk/api/prediction/" + a).decode())
        pdb = j[0].get("pdbUrl")
        raw = get(pdb, 120)
        if pdb.endswith(".gz"): raw = gzip.decompress(raw)
        open(dest,"wb").write(raw); ok+=1
    except Exception as e:
        fail.append((a, str(e)[:40]))
print("downloaded/available:", ok, "/", len(accs), " failed:", len(fail))
print("first fails:", fail[:5])
