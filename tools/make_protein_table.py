"""Per-protein lysine table (Table 1 inputs, Figure 2 densities).

This is a re-extraction entry point: it needs the raw UniProt snapshot in
data/uniprot/. It refuses to write when that snapshot is missing or does not
cover every protein carrying a Kpy site, so a partial run cannot truncate the
table the other entry points read.
"""
import sys, os, glob, gzip, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, 'tools'))
from kpydata import load_sites, load_kpy, DATA
import pandas as pd

OUT = os.path.join(DATA, 'protein_lysines.csv')

site = load_sites(); ks = load_kpy()
targets = sorted({a for a, _ in ks})

raw = glob.glob(os.path.join(DATA, 'uniprot', '*.json'))
if not raw:
    sys.exit('no raw UniProt records in data/uniprot; %s left untouched' % OUT)

gene = {}
for f in sorted(glob.glob(os.path.join(DATA, 'cplm', '*', '*.txt'))):
    df = pd.read_csv(f, sep='\t', header=None, usecols=[1, 4], names=['acc', 'g'],
                     dtype=str, on_bad_lines='skip')
    for a, g in zip(df.acc.astype(str).str.strip(), df.g.fillna('')):
        gene.setdefault(a, g.strip())


def load_uniprot(acc):
    p = os.path.join(DATA, 'uniprot', acc + '.json')
    if not os.path.exists(p): return None
    blob = open(p, 'rb').read()
    if blob[:2] == b'\x1f\x8b': blob = gzip.decompress(blob)
    return json.loads(blob.decode('utf-8'))


rows, missing, bad_seq = [], [], []
for acc in targets:
    rec = load_uniprot(acc)
    if rec is None:
        missing.append(acc); continue
    seq = (rec.get('sequence') or {}).get('value') or ''
    if not seq or not seq.isalpha() or not seq.isupper():
        bad_seq.append(acc); continue
    rows.append(dict(acc=acc, gene=gene.get(acc, ''), seq_len=len(seq), n_lys=seq.count('K'),
                     n_catalogued=sum(1 for p in range(1, len(seq) + 1) if (acc, p) in site)))

if missing or bad_seq or not rows:
    sys.exit('raw records incomplete: %d proteins absent, %d with an unusable sequence;'
             ' %s left untouched' % (len(missing), len(bad_seq), OUT))

df = pd.DataFrame(rows)
if len(df) != len(targets) or (df.n_lys <= 0).any():
    sys.exit('table would not cover every target protein; %s left untouched' % OUT)

tmp = OUT + '.tmp'
df.to_csv(tmp, index=False)
os.replace(tmp, OUT)
print('proteins written:', len(df), '| size KB: %.1f' % (os.path.getsize(OUT) / 1e3))
print(df.head(4).to_string(index=False))
print('median density: %.3f' % (df.n_catalogued / df.n_lys).median())