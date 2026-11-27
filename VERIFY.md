# Verifying that the archived code reproduces the manuscript

Run these checks against a **fresh download** of the archive, not against a
working copy. The point is to confirm that what a reader gets from the DOI is
enough to regenerate the reported numbers.

## 1. Get the archive

Open <https://doi.org/10.5281/zenodo.23906360> and use **Download all**, or take
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

## 4. Five checks against numbers in the manuscript

Every figure in the manuscript that a reader can recompute, the command that
produces it, and the value the manuscript states. Run each from the archive root.

| Manuscript claim | Command | Expected output |
|---|---|---|
| Table S1: nine stratified ORs, range 1.39 to 64.62 | `python tools/leave_one_out.py` | `nine LOO OR range: 1.39 - 64.62`; acetylation row `2.13`; Kpy row `OR=2.60` |
| Table S1: acetylation 10,098 query sites in 1,833 strata | `python tools/leave_one_out.py` | `Acetylation ... 10098 1833 2.13` |
| Kpy: OR 2.60, exact P 0.224, CI 0.60-10.25 | `python tools/exact_ci.py` | `MH OR = 2.60`, `0.224`, `0.60 - 10.25` |
| Table S4: crude ORs 2.87 / 5.96 / 5.45 / 2.58 / 3.24 / 6.04 / 3.93 / 1.50 / 24.97 and Kpy 2.97; shifts 0.74 to 2.73 (unchanged by adjudication) | `python tools/table_s4.py` | ten rows; crude column and shift column as printed |
| Table S4: stratified column equals the Table S1 column | `python tools/table_s4.py` and `python tools/leave_one_out.py` | the two print the same nine values |
| Results 5: 17% at OR 2.60, 42% at 4.44, 50% at 5.19, 71% at 8.0, 80% at 10.25 | `python tools/power_scale.py` | `0.17`, `0.42`, `0.50`, `0.71`, `0.80` |
| Results 1: 15% at 0.042, Spearman -0.48, RSA medians | `python tools/check_sections.py` | `median 0.042`, `-0.48`, `multi 0.569 | single 0.636` |
| Results 4: 62 of 4,748 lysines PubMed-linked (42/128 multi vs 20/354 single, Fisher P 2.5e-13; query excluded 31/113 vs 19/346, P 2.3e-9) | `python tools/check_sections.py` | `lysines 4748 | PubMed-linked 62`, `multi 42/128 | single 20/354 | Fisher P = 2.5e-13` |
| Table S3: 33 primary studies and 9 reviews; C1 of 19, C2 of 19, C3 of 31 | `python tools/regen_s3.py` | `artifacts/Table_S3.md`; C1 no/partial/yes = 18/1/0, C2 = 6/8/5, C3 = 20/11/0 |
| Figure 1: query counts and catalogue coverage | `python tools/make_fig1.py` | `figs/Fig1_reference_sets.png` and `.pdf`, plus `figs/submission/Fig1.pdf` and `.tif`; A/D overall 15/23, class rows 9/10 and 6/13, coverage 10/11 and 13/77 |

Table S3 is generated from `artifacts/coding.csv` and
`artifacts/reviews_coding_final.csv`. The generator excludes not-assessable
primary records and the two duplicate preprints, and reads review outcomes
from the coding sheet. It needs only Python's standard library, not a local
manuscript or downloaded full texts. Use `--output <path>` to choose another
Markdown output file. The caption describes the adjudicated study snapshot;
if the coding changes, its narrative must also be reviewed.

Table S4 and Figure 1 use the shared catalogue loader, which falls back to
the archived `data/cplm_sites.tsv.gz` when the raw CPLM directory is absent.
Figure 1 additionally uses `data/kpy_sites.csv` and
`data/protein_lysines.csv`; its statistical labels are the reported results,
while the query and coverage counts are calculated from these inputs.

Anything that does not match is a defect in this table, not in the analysis:
the numbers above were regenerated from the same scripts at release time.

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
| `tools/check_sections.py` — Results 2-4 numbers | **no** | **no** | yes |
| `data/protein_lysines.csv` — 63 proteins with total and catalogued lysines | **no** | **no** | yes |
| `artifacts/` — coding sheets for the literature check behind Table S3, with the sampling frame | **no** | **no** | yes |
| `VERIFY.md` — this file | **no** | yes | yes |

Cite the version that contains what you are checking. The five power values in
Results 5 and every row of Table S1 need v1.2; the odds ratio and its exact
interval, and the power at 2.60, are reproducible from either.

## PubMed-linked definition

`python tools/pubmed_provenance.py --summary` recomputes the counts above from the archived `data/pubmed_provenance.csv`, offline, without any raw record.
A lysine is PubMed-linked when at least one Modified-residue feature carries an evidence entry with
`source = "PubMed"` and a numeric id (the PMID). The `up_refs` column of `data/uniprot_lysines.csv`
counted distinct evidence source names, not PMIDs, and must not be used for these counts;
`pubmed_provenance.py` supersedes it.

`python tools/pubmed_provenance.py` (no flag) re-extracts the per-lysine evidence from the raw
UniProt snapshot in `data/uniprot/`. That snapshot is required for this mode only: if it is absent,
or if the records do not cover the catalogue, the script exits with an error and leaves the
archived CSV untouched rather than overwriting it with zeros.

The twelve lysines whose evidence carries no PubMed record are listed in
`artifacts/excluded_sites.csv`, written by the same script; they are the difference between
the 74 lysines with any evidence source and the 62 that count as PubMed-linked.
