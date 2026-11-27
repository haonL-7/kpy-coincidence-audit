"""Per-lysine PubMed provenance and the Results 4 counts.

Two modes:
  python tools/pubmed_provenance.py            re-extract from data/uniprot/*.json
  python tools/pubmed_provenance.py --summary  recompute the counts from
                                               data/pubmed_provenance.csv

A lysine is PubMed-linked when at least one Modified-residue feature carries an
evidence entry with source == 'PubMed' and a numeric id (the PMID). The up_refs
column of data/uniprot_lysines.csv counted distinct evidence source names and is
not this quantity; it survives as n_sources here.
"""
import os, sys, json, gzip, glob, csv
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, 'data')
ARCHIVE = os.path.join(DATA, 'pubmed_provenance.csv')


def summarize(rows):
    lk = lambda rs: sum(1 for r in rs if str(r['pubmed_linked']) == '1')
    m = [r for r in rows if int(r['cplm_mods']) >= 2]
    s = [r for r in rows if int(r['cplm_mods']) == 1]
    print('lysines %d | PubMed-linked %d' % (len(rows), lk(rows)))
    print('multi %d/%d | single %d/%d' % (lk(m), len(m), lk(s), len(s)))
    return rows, m, s


if '--summary' in sys.argv:
    if not os.path.exists(ARCHIVE):
        sys.exit('missing %s; run without --summary once, with the raw records present' % ARCHIVE)
    with open(ARCHIVE, encoding='utf-8-sig') as fh:
        summarize(list(csv.DictReader(fh)))
    sys.exit(0)

raw = glob.glob(os.path.join(DATA, 'uniprot', '*.json'))
if not raw:
    sys.exit('no raw UniProt records in data/uniprot; nothing written, %s left untouched' % ARCHIVE)

pmids, sources, mods = defaultdict(set), defaultdict(set), defaultdict(set)
accs = set()
for f in raw:
    blob = open(f, 'rb').read()
    if blob[:2] == b'\x1f\x8b': blob = gzip.decompress(blob)
    rec = json.loads(blob.decode('utf-8'))
    acc = rec.get('primaryAccession') or os.path.basename(f)[:-5]
    accs.add(acc)
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
with open(os.path.join(DATA, 'uniprot_lysines.csv'), encoding='utf-8-sig') as fh:
    for r in csv.DictReader(fh):
        cplm[(r['acc'], int(r['pos']))] = int(r['cplm_mods'] or 0)

missing = sorted({a for a, _ in cplm} - accs)
if missing or not pmids:
    sys.exit('raw records do not cover the catalogue (%d proteins absent, %d PMIDs found);'
             ' nothing written, %s left untouched' % (len(missing), len(pmids), ARCHIVE))

rows = [{'acc': k[0], 'pos': k[1], 'cplm_mods': n,
         'pubmed_linked': 1 if pmids.get(k) else 0,
         'pmids': ';'.join(sorted(pmids.get(k, ()))),
         'n_sources': len(sources.get(k, ())),
         'source_names': ';'.join(sorted(sources.get(k, ()))),
         'up_mods': ';'.join(sorted(mods.get(k, ())))} for k, n in sorted(cplm.items())]

tmp = ARCHIVE + '.tmp'
with open(tmp, 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
os.replace(tmp, ARCHIVE)

rows, m, s = summarize(rows)
excluded = [r for r in rows if int(r['n_sources']) > 0 and str(r['pubmed_linked']) == '0']
out = os.path.join(BASE, 'artifacts', 'excluded_sites.csv')
with open(out, 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh)
    w.writerow(['accession', 'position', 'modification_class', 'n_sources', 'source_names', 'reason'])
    for r in excluded:
        cls = 'multi-modified' if int(r['cplm_mods']) >= 2 else 'single-modified'
        w.writerow([r['acc'], r['pos'], cls, r['n_sources'], r['source_names'],
                    'evidence carries no source="PubMed" record with a numeric PMID'])
print('excluded sites written:', out, len(excluded))