# kpy-coincidence-audit

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23906360.svg)](https://doi.org/10.5281/zenodo.23906360)

Code and derived data supporting the manuscript *"Reference-set dependence in reported co-annotation of lysine acylations"* (Liu, Li and Feng). The concept DOI above always resolves to the latest release; each release also has its own version DOI on its record page.

Using a published map of 88 lysine pyruvylation sites across 63 proteins, the archive supports comparisons of four reference designs, protein-stratified analyses across the nine catalogued acylations, structural and annotation-evidence analyses, and an audit of reporting practice in 33 primary studies and nine reviews. These analyses concern catalogue co-annotation, not molecular co-occupancy or biological competition.

## Where to start

    README.md   this file
    VERIFY.md   the command and the expected output behind each reported number
    tools/      one script per entry point
    data/       the inputs those scripts read
    artifacts/  coding sheets, agreement statistics, signed adjudication log,
                sampling frame, derived tables
    figs/       rendered figures and submission exports

## Recalculating a number

Two kinds of entry point are kept apart, because they need different inputs.

| From the archived derived tables (no raw data needed) | From the upstream records (raw snapshot needed) |
|---|---|
| `python tools/pubmed_provenance.py --summary` | `python tools/pubmed_provenance.py` |
| `python tools/regen_s3.py` | `python tools/make_protein_table.py` |
| `python tools/table_s4.py` | `python tools/make_fig2.py` |
| `python tools/exact_ci.py` | `python tools/table_s1.py` |
| `python tools/leave_one_out.py` | `python tools/make_figS1.py` |

Scripts that re-extract from a raw snapshot check that it is complete before writing, and exit without touching an archived table when it is not.

## Inputs that are not redistributed

CPLM 4.0 per-modification tables and the AlphaFold models are large and their terms differ from this repository's licence, so they are fetched rather than shipped. `tools/fetch_uniprot.py`, `tools/fetch_af.py` and the CPLM download page recreate them under `data/`. The UniProt snapshot the analysis used is small enough to be included, and it is.

## Citing

Cite the archived release, not the repository alone: `CITATION.cff` carries the title, the three authors and the concept DOI. The version DOI for the release you used is printed on its Zenodo record.
