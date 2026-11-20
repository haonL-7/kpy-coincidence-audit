# kpy-coincidence-audit

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23946747.svg)](https://doi.org/10.5281/zenodo.23946747)

Archived release: v1.3.1, DOI 10.5281/zenodo.23946747.

Code and derived tables for the manuscript *"The reference set decides the answer: annotation depth, not competition, governs lysine acylation co-occupancy"*.

The paper asks a narrow question: when two lysine modifications are said to "compete" because their sites overlap, what does the overlap actually measure? Using 88 lysine pyruvoylation (Kpy) sites as a test case, the repository reproduces four reference sets (A-D), the structural covariates, and the curation-depth comparison, and shows that the same sites yield a 1e-5 enrichment, a two-fold enrichment, or no detectable enrichment depending only on how the comparison set is defined.

## What is here

    tools/       scripts that produce every number and figure in the manuscript
    data/        small derived tables (site lists, RSA table)
    figs/        rendered figures, including submission-grade TIFF/PDF

## What is not here

The primary databases are not redistributed. They are large (CPLM 4.0 is ~260 MB unpacked) and their terms differ from this repository's licence. Re-download them into `data/` before running:

| Resource | Where | Put it in |
|---|---|---|
| CPLM 4.0 per-modification tables | https://cplm.biocuckoo.cn/Download.php (Acetylation.zip, Crotonylation.zip, Succinylation.zip, Malonylation.zip, 2-Hydroxyisobutyrylation.zip, Butyrylation.zip, Lactylation.zip, Glutarylation.zip, Propionylation.zip) | `data/cplm/<Modification>/<Modification>.txt` |
| 88 Kpy sites | Supplementary Table 1 of Song et al., *Nat. Metab.* 2026, 8, 1495-1507 (extract with `analysis/extract_sites.py`) | `data/kpy_sites.csv` (already included) |
| UniProt entries | fetched by `analysis/fetch_uniprot.py` via the REST API | `data/uniprot/*.json` |
| AlphaFold models | fetched by `analysis/fetch_af.py` (needs a browser User-Agent; the API returns 403 otherwise) | `data/alphafold/*.pdb` |

### Data provenance

The exact files this analysis was run on are recorded in
[`artifacts/cplm_provenance.csv`](artifacts/cplm_provenance.csv), one row per
downloaded CPLM archive. Field meanings:

| Field | Meaning |
|---|---|
| `source_url` | The download page the archives came from. |
| `download_date` | Date on which the archive file first existed on the local disk. **This is not an independently verified download date**: no download log was kept, so the value is derived from `archive_birth` and should be read as a lower bound of known precision. |
| `download_date_basis` | The sentence that states exactly how `download_date` was obtained. |
| `archive_sha256` | SHA-256 of the **original ZIP archive** as saved, computed over the whole file, not over any member. |
| `extracted_sha256` | SHA-256 of the **extracted `.txt` member actually read by the analysis**. All ten match the corresponding archive member byte for byte, which is what establishes that the archive and the analysed text are the same data. |
| `archive_birth` | Local file-creation timestamp, to the second, of the saved archive. Filesystem metadata, not download metadata. |
| `used_in_analysis` | `yes` for the nine acylations analysed; `no` for Formylation, which was downloaded for reference and is not part of any reported number. |

ZIP-internal timestamps are deliberately not used anywhere in this table.

Note that `archive_bytes` is the size of the compressed archive and `member_bytes` the uncompressed size of the member, so the two are not comparable across rows.

## Reproducing the results

    python tools/extract_sites.py        # 88 Kpy sites  -> data/kpy_sites.csv
    python tools/fetch_uniprot.py        # UniProt entries -> data/uniprot/
    python tools/fetch_af.py             # AlphaFold models -> data/alphafold/
    python tools/compute_rsa.py          # SASA/RSA + pLDDT -> data/rsa_table.csv
    python tools/overlap_analysis.py     # overlap with CPLM  -> data/overlap_result.json
    python tools/perm_test.py            # within-protein permutation (reference set C and D)
    python tools/base_rate.py            # multi-modification base rates
    python tools/stratified_null.py      # protein-stratified null, seed stability
    python tools/uniprot_evidence.py     # curated evidence per lysine
    python tools/uniprot_match.py        # curation depth vs annotation breadth
    python tools/make_fig1.py             # Figures 1-4 (PDF + 300 dpi PNG + submission TIFF)
    python tools/make_fig2.py
    python tools/make_fig3.py
    python tools/make_fig4.py
    python tools/consistency_check.py      # citation numbering, figure references, key numbers

Scripts resolve paths from `BASE`, which defaults to the repository root and can be overridden:

    setx KPY_BASE D:\path\to\clone      # Windows, then reopen the shell
    export KPY_BASE=/path/to/clone        # Linux/macOS

All scripts are runnable from the repository root without editing.

## Environment

Python 3.12.14 with numpy 2.3.5, pandas 3.0.1, matplotlib 3.11.2, pillow 12.3.0.
Figures use Arial at 7 pt; the smallest text is 4.8 pt at the printed size, above the 4.5 pt floor required by the journal.

## A note on what the numbers do not say

The repository deliberately reproduces a negative result. Several scripts exist to make the negative result falsifiable rather than rhetorical: `stratified_null.py` permutes within proteins, `uniprot_match.py` tests the study-depth confounder, `rsa_analysis.py` tests the structural one. None of them establishes that Kpy has no site preference; with 13 catalogued non-histone sites the power to detect a two-fold effect is 0.53.

## Licence

Code: MIT (see LICENSE). Derived tables: CC BY 4.0. The upstream databases keep their own terms.
