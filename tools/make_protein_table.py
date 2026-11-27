"""Per-protein lysine table (Figure 1 densities, Figure 2 labels).

Numeric columns are re-extracted from the raw UniProt snapshot in data/uniprot/.
The gene symbol is a retained annotation input: it is read from the archived
data/protein_lysines.csv when that file is present, because the symbols were
originally taken from the CPLM downloads, which are not part of the archive.
Recomputing them from UniProt would add 16 symbols and rename one (GATD3A to
GATD3), which changes which proteins carry a histone-like label.

The script refuses to write when the raw snapshot is missing or does not cover
every protein carrying a Kpy site, and when a retained symbol would be lost.
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

kept_gene = {}
if os.path.exists(OUT):
    with open(OUT, encoding='utf-8-sig') as fh:
        for r in pd.read_csv(fh).itertuples(index=False):
            kept_gene[str(r.acc)] = '' if pd.isna(r.gene) else str(r.gene)

cplm_gene = {}
for f in sorted(glob.glob(os.path.join(DATA, 'cplm', '*', '*.txt'))):
    df = pd.read_csv(f, sep='\t', header=None, usecols=[1, 4], names=['acc', 'g'],
                     dtype=str, on_bad_lines='skip')
    for a, g in zip(df.acc.astype(str).str.strip(), df.g.fillna('')):
        cplm_gene.setdefault(a, g.strip())


HAS_ARCHIVE = bool(kept_gene)


def gene_for(acc, rec):
    if HAS_ARCHIVE:
        return kept_gene.get(acc, '')
    if cplm_gene.get(acc): return cplm_gene[acc]
    for gene in rec.get('genes', []) or []:
        nm = (gene.get('geneName') or {}).get('value') or ''
        if nm: return nm
    return ''


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
    rows.append(dict(acc=acc, gene=gene_for(acc, rec), seq_len=len(seq), n_lys=seq.count('K'),
                     n_catalogued=sum(1 for p in range(1, len(seq) + 1) if (acc, p) in site)))

if missing or bad_seq or not rows:
    sys.exit('raw records incomplete: %d proteins absent, %d with an unusable sequence;'
             ' %s left untouched' % (len(missing), len(bad_seq), OUT))

df = pd.DataFrame(rows)
if len(df) != len(targets) or (df.n_lys <= 0).any():
    sys.exit('table would not cover every target protein; %s left untouched' % OUT)

lost = [r['acc'] for r in rows if kept_gene.get(r['acc']) and not r['gene']]
if lost:
    sys.exit('retained gene symbols would be lost for %d proteins; %s left untouched' % (len(lost), OUT))

tmp = OUT + '.tmp'
df.to_csv(tmp, index=False)
os.replace(tmp, OUT)
print('proteins written:', len(df), '| genes non-empty: %d' % (df.gene.astype(str).str.len() > 0).sum())
print(df.head(4).to_string(index=False))
print('median density: %.3f' % (df.n_catalogued / df.n_lys).median())