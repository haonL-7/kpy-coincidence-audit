"""Shared loader for the Kpy coincidence audit.

Resolution order for the data directory:
  1. the KPY_BASE environment variable
  2. the repository root that contains this file

The modification table is read from data/cplm/*/*.txt when those raw downloads
are present, and otherwise from the compact data/cplm_sites.tsv.gz that ships
with the archive, so every analysis below runs from the archive alone.
"""
import glob
import gzip
import os
from collections import defaultdict

import pandas as pd

ROOT = os.environ.get("KPY_BASE") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
FIGS = os.path.join(ROOT, "figs")


def load_sites():
    """Return {(uniprot, position): set(modification)} for the human catalogue."""
    site = defaultdict(set)
    raw = sorted(glob.glob(os.path.join(DATA, "cplm", "*", "*.txt")))
    if raw:
        for f in raw:
            mod = os.path.basename(os.path.dirname(f))
            df = pd.read_csv(f, sep="\t", header=None, usecols=[1, 2, 5],
                             names=["acc", "pos", "sp"], dtype=str, on_bad_lines="skip")
            df = df[df["sp"].fillna("").str.contains("Homo sapiens", na=False)].dropna(subset=["acc", "pos"])
            df = df[df["pos"].str.match(r"^\d+$", na=False)]
            for a, p in zip(df.acc.str.strip(), df.pos.astype(int)):
                site[(a, p)].add(mod)
        return site
    compact = os.path.join(DATA, "cplm_sites.tsv.gz")
    if not os.path.exists(compact):
        raise SystemExit("No modification table found: expected data/cplm/ or data/cplm_sites.tsv.gz")
    with gzip.open(compact, "rt", encoding="utf-8") as fh:
        next(fh)
        for line in fh:
            a, p, mods = line.rstrip("\n").split("\t")
            site[(a, int(p))] = set(mods.split(",")) if mods else set()
    return site


def load_kpy():
    """Return the set of (uniprot, position) for the 88 pyruvylation sites."""
    kpy = pd.read_csv(os.path.join(DATA, "kpy_sites.csv"))
    kpy["acc"] = kpy["Uniprot ID"].astype(str).str.strip()
    kpy["pos"] = kpy["Positions within proteins"].astype(int)
    return {(a, int(p)) for a, p in zip(kpy.acc, kpy.pos)}
