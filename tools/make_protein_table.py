
import sys, os, glob, gzip, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"C:\Users\Administrator\Desktop\丙酮酰化\tools")
from kpydata import load_sites, load_kpy, DATA
import pandas as pd

site = load_sites(); ks = load_kpy()

# gene symbols from the CPLM downloads (present on this machine only)
gene = {}
for f in sorted(glob.glob(os.path.join(DATA, "cplm", "*", "*.txt"))):
    df = pd.read_csv(f, sep="\t", header=None, usecols=[1, 4], names=["acc", "g"], dtype=str, on_bad_lines="skip")
    for a, g in zip(df.acc.astype(str).str.strip(), df.g.fillna("")):
        gene.setdefault(a, g.strip())

def load_uniprot(acc):
    p = os.path.join(DATA, "uniprot", acc + ".json")
    if not os.path.exists(p):
        return None
    with gzip.open(p, "rt", encoding="utf-8") as fh:
        return json.load(fh)

rows = []
for acc in sorted({a for a, _ in ks}):
    rec = load_uniprot(acc)
    seq = ""
    if rec:
        seq = rec.get("sequence", {}).get("value", "") or ""
    if not seq:
        continue
    rows.append(dict(acc=acc, gene=gene.get(acc, ""), seq_len=len(seq),
                     n_lys=seq.count("K"),
                     n_catalogued=sum(1 for p in range(1, len(seq)+1) if (acc, p) in site)))
df = pd.DataFrame(rows)
out = os.path.join(DATA, "protein_lysines.csv")
df.to_csv(out, index=False)
print("proteins written:", len(df), "| size KB: %.1f" % (os.path.getsize(out)/1e3))
print(df.head(4).to_string(index=False))
print("median density: %.3f" % (df.n_catalogued/df.n_lys).median())
