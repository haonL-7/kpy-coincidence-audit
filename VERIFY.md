# Verifying that the archived code reproduces the manuscript

Run these checks against a **fresh download** of the archive, not against a
working copy. The point is to confirm that what a reader gets from the DOI is
enough to regenerate the reported numbers.

## 1. Get the archive

Open <https://doi.org/10.5281/zenodo.23915860> and use **Download all**, or take
the single `.zip` / `.tar.gz`. Unpack somewhere outside any existing clone:

    mkdir ~/verify && cd ~/verify
    unzip <downloaded archive>.zip

Expected top level: `tools/`, `data/`, `figs/`, `README.md`, `CITATION.cff`,
`requirements.txt`, `LICENSE`.

## 2. Check what is and is not in the archive

`data/` holds **derived** tables only — `kpy_sites.csv`, `rsa_table.csv`,
`uniprot_lysines.csv`, `audit_table.csv` and the result JSONs. The primary
databases (CPLM 4.0, AlphaFold models, UniProt records) are deliberately not
redistributed; nothing below needs them.

    ls data tools

## 3. Environment

    python -m venv .venv
    .venv/bin/pip install -r requirements.txt      # Windows: .venv\Scripts\pip

Python 3.12, numpy, pandas, matplotlib, pillow. No network access is required
for the checks below.

## 4. Four checks against numbers in the manuscript

| Command | Expected output | Where the manuscript states it |
|---|---|---|
| `python tools/exact_ci.py` | `MH OR = 2.60`, `exact two-sided P ... 0.224`, `95% CI ... 0.60 - 10.25` | Results 1; Abstract |
| `python tools/leave_one_out.py` | nine odds ratios from 1.97 to 65.12, then `Kpy ... OR=2.60 P=0.182` | Table S1 |
| `python tools/power_sim.py` | `power at OR 2.6 = 0.18`, `x2 ... 0.45`, `x4 ... 0.56` | Results 5; Methods, Power |
| `python tools/power_scale.py` | `power at OR 5.19 = 0.50`, `power at OR 10.25 = 0.80` (about 2 points of Monte Carlo noise) | Results 5 |

On Windows set `PYTHONIOENCODING=utf-8` first; the scripts print no non-ASCII
except the typographic minus in a few table cells.

## 5. Reading the result

An archive is usable when all four hold:

1. every script referenced in the Methods is present;
2. each runs to completion without network access;
3. its output matches the number printed in the manuscript;
4. the figures can be regenerated — `python tools/make_fig1.py` and the rest
   write into `figs/` and `figs/submission/`.

If a number moved between versions, the version that reproduces it is the one to
cite, and the Methods should name that version explicitly.

## 6. Coverage by version

| Item | v1.1 | v1.2.1 | v1.3 |
|---|---|---|
| `tools/exact_ci.py` — exact conditional OR and interval | yes | yes |
| `tools/leave_one_out.py` — nine modifications, one estimator | yes | yes |
| `tools/power_sim.py` — power at OR 2.60, and the 2x / 4x projection | yes | yes |
| `tools/power_scale.py` — power at 3.0, 5.19, 8.0 and 10.25 | **no** | yes |
| `tools/table_s1.py` — generator for Table S1 | **no** | yes |
| `tools/kpydata.py` — portable data loader | **no** | **no** | yes |
| `data/cplm_sites.tsv.gz` — 66,790 sites, so the archive runs without the 233 MB raw download | **no** | **no** | yes |
| `verify.py` — cross-platform check runner | **no** | **no** | yes |
| `VERIFY.md` — this file | **no** | yes | yes |

Cite the version that contains what you are checking. The five power values in
Results 5 and every row of Table S1 need v1.2; the odds ratio and its exact
interval, and the power at 2.60, are reproducible from either.
