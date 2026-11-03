"""Reproduce the numbers reported in Results 2, 3 and 4.

Everything here reads from data/, which the archive ships: the compact site
table, the structural table, the UniProt curation table and the per-protein
lysine counts. No network and no raw database download is required.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd

from kpydata import load_sites, load_kpy, DATA

MODS = ["Acetylation", "Crotonylation", "2-Hydroxyisobutyrylation", "Malonylation",
        "Succinylation", "Butyrylation", "Lactylation", "Glutarylation", "Propionylation"]


def fisher_tail(rows):
    """Two-sided Fisher exact P for a 2x2 table given as (a, b, c, d)."""
    a, b, c, d = rows
    n = a + b + c + d

    def lc(x):
        return math.lgamma(x + 1)

    def p_of(a2):
        b2, c2, d2 = a + b - a2, a + c - a2, n - a2 - (a + b - a2) - (a + c - a2)
        if min(b2, c2, d2) < 0:
            return 0.0
        return math.exp(lc(a + b) + lc(c + d) + lc(a + c) + lc(b + d)
                        - lc(n) - lc(a2) - lc(b2) - lc(c2) - lc(d2))

    p0 = p_of(a)
    lo, hi = max(0, (a + b) - (c + d)), min(a + b, a + c)
    return sum(p for x in range(lo, hi + 1) for p in [p_of(x)] if p <= p0 * (1 + 1e-9))


def section2(site):
    prot = pd.read_csv(os.path.join(DATA, "protein_lysines.csv"))
    dens = (prot.n_catalogued / prot.n_lys).replace([float("inf")], float("nan")).dropna()
    print("  annotation density: median %.3f across %d proteins" % (dens.median(), len(dens)))
    for acc, label in [("P62805", "H4C1"), ("P68431", "H3C1"), ("P62807", "H2BC4")]:
        row = prot[prot.acc == acc]
        if len(row):
            r = row.iloc[0]
            print("    %-6s %d/%d" % (label, r.n_catalogued, r.n_lys))
    sizes, rates = [], []
    for m in MODS:
        sites = [s for s, v in site.items() if m in v]
        sizes.append(len(sites))
        rates.append(100 * sum(1 for s in sites if len(site[s]) >= 2) / len(sites))
    print("  catalogue size range %d-%d; multi-modification rate range %.1f%%-%.1f%%"
          % (min(sizes), max(sizes), min(rates), max(rates)))
    rank = lambda v: pd.Series(v).rank().tolist()
    x, y = rank([math.log10(s) for s in sizes]), rank(rates)
    rho = pd.Series(x).corr(pd.Series(y))
    print("  Spearman(log10 catalogue size, multi-modification rate) = %.2f (n = %d)" % (rho, len(rates)))


def section3(site):
    rsa = pd.read_csv(os.path.join(DATA, "rsa_table.csv"))
    lys = rsa[rsa.resname == "LYS"].copy()
    lys["nmod"] = [len(site.get((a, int(p)), ())) for a, p in zip(lys.acc, lys.resseq)]
    multi, single = lys[lys.nmod >= 2], lys[lys.nmod == 1]
    print("  modelled lysines %d | single %d | multi %d" % (len(lys), len(single), len(multi)))
    print("  median RSA: multi %.3f | single %.3f | all %.3f"
          % (multi.rsa.median(), single.rsa.median(), lys.rsa.median()))
    print("  disordered (pLDDT < 50): multi %.1f%% | all lysines %.1f%%"
          % (100 * (multi.plddt < 50).mean(), 100 * (lys.plddt < 50).mean()))
    rows = []
    for acc, g in lys[lys.nmod > 0].groupby("acc"):
        m, s1 = g[g.nmod >= 2], g[g.nmod == 1]
        if len(m) and len(s1):
            rows.append((m.plddt.mean() - s1.plddt.mean(), m.rsa.mean() - s1.rsa.mean()))
    if rows:
        d_p = [r[0] for r in rows]
        d_r = [r[1] for r in rows]
        print("  within-protein (%d proteins): d_pLDDT %+.2f | d_RSA %+.3f"
              % (len(rows), sum(d_p) / len(d_p), sum(d_r) / len(d_r)))


def section4(site, ks):
    up = pd.read_csv(os.path.join(DATA, "uniprot_lysines.csv"))
    up["nmod"] = [len(site.get((a, int(p)), ())) for a, p in zip(up.acc, up.pos)]
    up["iskpy"] = [(a, int(p)) in ks for a, p in zip(up.acc, up.pos)]
    print("  lysines %d | with curated evidence %d" % (len(up), int((up.up_refs > 0).sum())))
    for label, df in [("all catalogued", up), ("query excluded", up[~up.iskpy])]:
        m, s1 = df[df.nmod >= 2], df[df.nmod == 1]
        a = int((m.up_refs > 0).sum()); b = len(m) - a
        c = int((s1.up_refs > 0).sum()); d = len(s1) - c
        print("  %-15s multi %d/%d | single %d/%d | Fisher P = %.1e"
              % (label, a, a + b, c, c + d, fisher_tail((a, b, c, d))))


def main():
    site = load_sites()
    ks = load_kpy()
    print("== Results 2: annotation density and catalogue unevenness ==")
    section2(site)
    print("== Results 3: structural context ==")
    section3(site, )
    print("== Results 4: curation depth ==")
    section4(site, ks)
    return 0


if __name__ == "__main__":
    sys.exit(main())
