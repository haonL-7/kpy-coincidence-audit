"""Per-lysine PubMed provenance from the 63 raw UniProt records.

A lysine is PubMed-linked when at least one Modified-residue feature carries an
evidence entry with source == 'PubMed' and a numeric id (the PMID). The earlier
up_refs column counted distinct evidence *source names* (PubMed, UniProtKB, ...)
and is therefore not the manuscript definition; it is kept as n_sources.
"""
import os, json, gzip, glob, csv
from collections import defaultdict

BASE = os.environ.get('KPY_BASE', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
base = os.path.join(BASE, 'data')

pmids = defaultdict(set)
sources = defaultdict(set)
mods = defaultdict(set)
for f in glob.glob(os.path.join(base, 'uniprot', '*.json')):
    raw = open(f, 'rb').read()
    if raw[:2] == b'\x1f\x8b': raw = gzip.decompress(raw)
    rec = json.loads(raw.decode('utf-8'))
    acc = rec.get('primaryAccession') or os.path.basename(f)[:-5]
    for ft in rec.get('features', []):
        if ft.get('type') != 'Modified residue': continue
        pos = ft['location']['start']['value']
        mods[(acc, pos)].add((ft.get('description') or '').split(';')[0].strip())
        for ev in ft.get('evidences', []):
            src = (ev.get('source') or '').strip()
            if src: sources[(acc, pos)].add(src)
            if src == 'PubMed':
                sid = str(ev.get('id') or '').strip()
                if sid.isdigit(): pmids[(acc, pos)].add(sid)

cplm = {}
with open(os.path.join(base, 'uniprot_lysines.csv'), encoding='utf-8-sig') as fh:
    for r in csv.DictReader(fh):
        cplm[(r['acc'], int(r['pos']))] = int(r['cplm_mods'] or 0)

rows = []
for key, n in sorted(cplm.items()):
    rows.append({'acc': key[0], 'pos': key[1],
                 'cplm_mods': n,
                 'pubmed_linked': 1 if pmids.get(key) else 0,
                 'pmids': ';'.join(sorted(pmids.get(key, ()))),
                 'n_sources': len(sources.get(key, ())),
                 'up_mods': ';'.join(sorted(mods.get(key, ())))})

out = os.path.join(base, 'pubmed_provenance.csv')
with open(out, 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

linked = [r for r in rows if r['pubmed_linked']]
multi = [r for r in rows if r['cplm_mods'] >= 2]
sing = [r for r in rows if r['cplm_mods'] == 1]
lm = sum(1 for r in multi if r['pubmed_linked'])
ls = sum(1 for r in sing if r['pubmed_linked'])
print('lysines %d | PubMed-linked %d' % (len(rows), len(linked)))
print('multi %d/%d | single %d/%d' % (lm, len(multi), ls, len(sing)))
kpy = [r for r in rows if r['cplm_mods'] >= 1 and r['up_mods'] and 'pyruv' in (r['up_mods'] or '').lower()]
print('written:', out)