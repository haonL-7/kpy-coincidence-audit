# Submission figure package

Journal of Proteome Research (Article). All files exported from `tools/make_fig*.py`.
PDF for review, TIFF (600 dpi, LZW, RGB) for production.

| File | Figure | Content | Size |
|---|---|---|---|
| `Fig1.pdf` / `Fig1.tif` | Figure 1 | (a) how each reference set samples lysines; (b) observed vs expected under A, B, D; (c) reference set C; (d) catalogue coverage by protein class | 7.00 x 3.95 in |
| `Fig2.pdf` / `Fig2.tif` | Figure 2 | (a) annotation density across the 63 proteins; (b) multi-modification rate by acylation against catalogue size | 7.00 x 2.80 in |
| `Fig3.pdf` / `Fig3.tif` | Figure 3 | three-item reporting protocol: claim, three controls, interpretable or not | 7.00 x 1.90 in |
| `FigS1.pdf` / `FigS1.tif` | Supplementary Figure S1 | structural context: RSA and pLDDT distributions, multi-modification rate by exposure, within-protein paired comparison | 7.00 x 2.30 in |
| `FigS2.pdf` / `FigS2.tif` | Supplementary Figure S2 | curated UniProt evidence by class, query included (filled) and query excluded (open) | 3.40 x 2.00 in |
| `TOC_Graphic.pdf` / `.tif` | TOC graphic | the journal maximum | 3.25 x 1.75 in |

Checks applied
- Width <= 504 pt (7.00 in) and height <= 660 pt for every main-text figure: passed.
- TIFF: 600 dpi, LZW, RGB, no alpha channel, 4200 px wide for the full-width figures.
- Fonts: Arial throughout, text preserved as text in the PDFs.
- Colour: each panel legible in greyscale.

Numbering note
The protocol figure is **Figure 3** in the manuscript and is exported from
`tools/make_fig4.py`, which keeps its historical filename. The structural analysis
it displaced is Supplementary Figure S1. Files are named by final number, not by
script name.
