# Manuscript v1 — The reference set decides the answer

> Manuscript source, formatted for Journal of Proteome Research (Article type). Every number reproduced by the scripts in tools/; figures in figs/.
> JPR limits applied: abstract <=200 words; article <=8,000 words (excluding Methods/references); figures 504 pt (7.00 in) double-column maximum; lettering >=4.5 pt; Helvetica or Arial.

## Title

The reference set decides the answer: annotation depth, not competition, governs lysine acylation co-occupancy

## Abstract

Metabolite-derived lysine acylations are increasingly invoked to explain immune and metabolic phenotypes, and crosstalk between them is usually argued from a single statistic: the fraction of one modification's sites that coincide with another's. That fraction depends on the reference set against which coincidence is judged, yet the choice is rarely reported. Using a recently described modification, lysine pyruvoylation (Kpy; 88 sites in 63 proteins), together with nine catalogued acylations in CPLM 4.0, we show how strongly the conclusion follows that choice. The same sites give a 1.0 × 10⁻⁵ enrichment against a pooled baseline, two-fold enrichment in histone and non-histone strata (P = 0.011 and 0.044), and no detectable enrichment once comparison is restricted to annotated lysines within the same protein (P = 0.154-0.351; power 0.53). Annotation density differs 24-fold between protein classes, multi-modification rates span 23%-93% across acylations, and multi-modified lysines are more buried and better ordered than single-modified ones, which argues against simple detection bias. We propose three reporting controls: a declared reference set, protein-composition matching, and a power statement. Current catalogues cannot settle whether Kpy, or any other acylation, prefers particular lysines; they settle only which comparison such a claim can rest on.

**Keywords:** lysine pyruvoylation; post-translational modification crosstalk; annotation bias; reference set; curation depth; proteome annotation

## Introduction

Lysine acetylation, lactylation, crotonylation, 2-hydroxyisobutyrylation and a growing list of related acylations are metabolite-derived post-translational modifications that connect carbon flux to chromatin state and immune signalling [1-3]. Because these marks share both a chemical handle (the lysine epsilon-amine) and, in many cases, a precursor pool, their relationships are naturally described as competition: two acylations contending for the same residue, with the winner setting the downstream program.

The evidence for such competition is almost always a coincidence statistic [4]. Sites of modification X are intersected with sites of modification Y, the overlap is compared with an expectation, and a significant excess is read as shared or contested chemistry. This reasoning is only as good as the expectation. Coincidence can arise because two marks genuinely occupy the same lysine, because both were mapped in the same heavily studied proteins, or because the reference set used to compute the expectation contains a different mixture of proteins than the query set. The three explanations are not distinguished by the statistic itself, and in the two representative studies cited above [4,5] the reference set is not stated.

Three terms carry the argument and are kept separate here. A *coincidence rate* is the measured overlap between two site lists under a stated reference set. *Co-occupancy* is the biological claim that one lysine carries two marks at once, which a coincidence rate is usually taken to imply. *Multi-modified* describes the catalogue rather than the protein: a lysine annotated with two or more modification types. A high coincidence rate leaves co-occupancy untested, and it is the multi-modified lysines that supply the expectation against which both are scored.

Two properties of the underlying databases make the problem acute. First, annotation coverage is extremely uneven: a small number of proteins, above all the histones, have nearly every lysine annotated, while most proteins have a few percent at most. Second, the reference space itself reflects where work has been done rather than uniform detectability: the nine acylations analysed here differ by nearly three orders of magnitude in catalogue size, from 44 sites for propionylation to 58,672 for acetylation (Results, Figure 2b), so a newly described modification enters a space shaped by older studies [6]. Because that space is rarely stated, two papers reporting enrichment of the same modification cannot be compared with each other, and neither can be reproduced without re-deriving its background. Resources flag underrepresented modifications [7]; how annotation density distorts crosstalk conclusions has not been quantified. Any cross-protein comparison inherits both properties.

Here we take a newly described modification as a test case. Lysine pyruvoylation (Kpy) was reported in 2026 and, at the time of analysis, comprised 88 sites in 63 proteins [8,9]. We ask a deliberately narrow question: what can be inferred about Kpy site selection from the catalogues as they stand? We evaluate the same site set against four reference sets of increasing stringency, then characterise the two covariates that plausibly drive the differences: protein-level annotation density and residue-level structural context. The question we can answer is narrower and more useful: which comparisons can carry a claim about Kpy, and which cannot. We reduce that answer to a three-item reporting protocol.

## Results

### 1. The same site set yields opposite conclusions under four reference sets

We assembled the 88 Kpy sites (63 proteins) and intersected them with 66,790 human lysine sites carrying at least one of nine acylations in CPLM 4.0 [6], of which 14,754 (22.1%) carry two or more distinct modification types. Reference sets A-D and the resulting statistics are summarised in Figure 1.

Against a global baseline that ignores protein composition (reference set A), Kpy sites are strongly enriched for multi-modified lysines: 15 of the 23 Kpy sites that are catalogued at all (65.2%) are multi-modified, versus 22.1% overall (hypergeometric P = 1.0 × 10⁻⁵).

Stratifying by protein class (reference set B) weakens but does not remove the signal, and the two strata behave similarly rather than differently: histone Kpy sites are 9/10 multi-modified against a histone baseline of 371/756 (P = 0.011), non-histone Kpy sites are 6/13 against 14,383/66,034 (P = 0.044). An interpretation in which chromatin is a zone of multi-modification overlap while non-histone substrates are exclusively modified is therefore not supported: both strata are enriched roughly two-fold.

Controlling for protein composition removes the signal. Permuting Kpy sites within their own proteins against all lysines (reference set C) gives 23/88 coincident against a null mean of 21.0 (P = 0.275). Restricting the same permutation to annotated lysines (reference set D) gives 15/23 multi-modified against a null of 12.8 (P = 0.154); the non-histone subset gives 6/13 against 4.8 (P = 0.293) and the histone subset 9/10 against 8.0 (P = 0.351). Estimates are stable across random seeds (0.154, 0.160, 0.180).

The four reference sets do not estimate the same quantity, and their disagreement is the point: A asks whether Kpy sites fall in annotation-dense proteins, whereas C and D ask whether, within a protein, Kpy favours residues that carry other marks. Both can be true simultaneously. Because D conditions on prior annotation, its null is drawn from residues that are themselves well studied, which makes it conservative; a negative result under D therefore excludes enrichment beyond annotation density, and does not establish random placement.

### 2. Annotation density, not competition, dominates cross-protein comparisons

Across the 63 Kpy proteins, annotation density, defined as catalogued lysines divided by total lysines, has a median of 0.042 (Figure 2a). The histone outliers are near saturation: H4C1 11/11, H3C1 13/13, H2BC4 16/20. A comparison that pools proteins therefore compares Kpy sites, which fall disproportionately in annotation-dense proteins, with a baseline that is dominated by sparse ones.

The same unevenness applies between modifications. Within CPLM 4.0, the fraction of catalogued sites that are multi-modified ranges from 22.8% (acetylation, 58,672 sites) through 74.0% (crotonylation), 80.0% (lactylation), 86.5% (2-hydroxyisobutyrylation) to 93.2% (propionylation, 44 sites) (Figure 2b). No chemical ordering accounts for these values; they track catalogue size and the protein sets of the underlying studies instead. Lactylation illustrates the extreme: all 80 human lactylation sites in the catalogue are histone sites.

### 3. Multi-modified lysines are buried and ordered, not merely accessible

A straightforward objection is detection bias: exposed, flexible lysines might be easier to modify and to detect, so multi-modified residues would be an artefact of accessibility. We tested this using AlphaFold models for 62 of the 63 proteins (81 of 88 sites mappable), computing per-residue relative solvent accessibility (RSA) with a Shrake-Rupley implementation [10] and using the predicted local distance difference test (pLDDT) as a disorder proxy [11,12]. Accessibilities were normalised to the maximum allowed values of Tien et al. [13].

The direction is opposite to the detection-bias prediction. Multi-modified lysines are less exposed than single-modified ones (median RSA 0.569 versus 0.603; rank-sum P = 0.032) and are almost never disordered (3.1% with pLDDT < 50, versus 34.1% of all lysines in these proteins). The multi-modification rate falls monotonically with accessibility, from 36% in buried residues to 22.9% in exposed ones (Figure 3).

Kpy sites themselves are unremarkable in this respect: their RSA distribution does not differ from other lysines in the same proteins (P = 0.395), from multi-modified lysines (P = 0.246), or from catalogued single-modified lysines (P = 0.704). Structural context therefore neither explains an enrichment nor supplies one.

### 4. Curation depth co-varies with annotation breadth

We next asked how much of "multi-modified" reflects literature depth. Only 74 of the 4,748 lysines in these 63 proteins (1.6%) carry a curated UniProt MOD_RES annotation with a literature reference [14], retrieved through the UniProt REST API [15], and all 74 are also present in CPLM. Among catalogued lysines, multi-modified sites are far more likely to carry such a reference than single-modified sites: 53/128 (41%) versus 21/354 (6%) (Fisher exact P = 5.0 × 10⁻¹⁹).

The association carries two caveats. CPLM and UniProt curate the same primary literature, so the two are not independent; a residue annotated with several modification types is, almost by construction, supported by several studies. The association is therefore consistent with a study-depth confounder but does not demonstrate one (Figure 4a). What it does establish is enough for the argument: annotation breadth and study depth are coupled, so any co-occupancy claim must match on study depth before it can be interpreted.

### 5. A minimal reporting protocol

The practical consequence is small and cheap. We propose that a claim of co-occupancy drawn from a coincidence rate report three things: (i) the reference set used to compute the expectation, stated as one of the four defined above or as an explicit alternative; (ii) whether protein composition was matched, and if so how; (iii) a power statement based on the number of catalogued query sites, since the detectable effect size is set by that number and not by the total number of query sites (Figure 4b). For the present case, 13 catalogued non-histone sites give 53% power to detect a two-fold enrichment at α = 0.05; 40 such sites would give 90%.

Where these three items are reported, the statistic becomes interpretable; where they are not, the same data can be presented as evidence for competition or as evidence against it.

## Discussion

Our analysis bears on a familiar inferential habit rather than on a specific modification. Crosstalk between lysine acylations is often summarised by one overlap number, and the number is sensitive to a choice that is usually left unstated. Scoring frameworks formalise PTM interplay within proteoforms [16]; they take the site lists as given, which is the step we examine. We showed, on a single set of 88 sites, that the same data support enrichment at P = 1.0 × 10⁻⁵, two-fold enrichment in both protein classes, or no detectable enrichment, depending on the reference set. The spread is not a paradox and not a sign that one analysis is wrong; the four analyses answer different questions, and only the question being asked determines which is appropriate. What the audit establishes is that this choice is invisible in the published record, and that it is large enough to reverse a conclusion.

The finding does not argue against biological crosstalk. The argument also holds whether or not the Kpy anchor is settled. The STAT1-K201 site has been taken up in commentary [17] but not independently reproduced. It argues that the current catalogues cannot adjudicate it at the level of individual sites, because the catalogues are themselves a record of where work has been done. Our structural result sharpens this: multi-modified residues concentrate in buried, ordered regions, which is what one expects if they are the residues of well-characterised folded domains, and which is the opposite of a detection artefact. The annotation record is a record of attention as much as of chemistry.

Three limitations bound the claim. The Kpy site set comes from a single study of 88 sites in one system, so nothing here excludes a site preference that a larger, independent dataset would reveal; at 13 catalogued non-histone sites, our power to detect a two-fold effect is 53%. Curated evidence covers only 1.6% of lysines in these proteins, which is too sparse for a genuine study-depth match; that step requires site-level reference counts that neither CPLM nor the public UniProt subset provides. The mechanism itself is not specific to acylations, since any modification with an unevenly annotated catalogue will show the same dependence, but we tested only lysine acylations; the size of the effect in phosphorylation or ubiquitination data remains unmeasured. Finally, we did not correct for multiple testing across the roughly fifteen comparisons reported here; none of the conclusions depends on a borderline result except the structural comparison (P = 0.032), which should be treated as suggestive.

Dual-modification atlases are now routine [18], so the reference-set question is practical rather than hypothetical. What would settle the underlying question is not a better statistic but better data: an independent Kpy site set of a few hundred sites across cell types, and catalogs that carry per-site study counts. Until then the present data support one conclusion: Kpy site selection is not detectable, not that it is absent.

## Methods

**Modification sets.** Kpy sites were taken from the supplement of the 2026 report [9] (88 sites, 63 proteins). Human sites for nine acylations were obtained from CPLM 4.0 (acetylation, crotonylation, 2-hydroxyisobutyrylation, malonylation, succinylation, butyrylation, lactylation, glutarylation, propionylation), filtered to Homo sapiens (CPLM 4.0 downloaded November 2026). Union: 66,790 unique lysine positions, 14,754 of them carrying two or more modification types.

**Reference sets.** A: all catalogued human lysines, ignoring protein membership. B: as A, within histone and non-histone strata. C: within-protein permutation over all lysines, sampling, for each protein, as many positions as the number of Kpy sites in that protein, without replacement. D: as C but restricted to catalogued lysines. Permutation tests used 2,000 iterations for C and 500 per seed for the stability check (seeds 1, 2, 3).

**Statistics.** Hypergeometric tests were implemented directly from binomial coefficients and cross-checked against an independent implementation. Proportions shown in figures carry Wilson 95% confidence intervals, stated as such in each legend; the text reports counts with exact P values. Rank-sum tests used the normal approximation with tie correction; two-sided P values were computed as erfc(|z|/sqrt(2)). Power was computed by exact binomial under the null of the non-histone baseline (21.8%) at alpha = 0.05, one-sided.

**Structure.** AlphaFold models were retrieved programmatically for 63 accessions (62 available). Per-residue solvent accessibility was computed with a Shrake-Rupley implementation (64 sphere points, probe radius 1.4 A, element radii), normalised by Tien 2013 maximum accessibility; pLDDT was read from the B-factor field. Seven Kpy sites could not be mapped: three lie in a protein without a model and four lie beyond the modelled fragment.

**Curated evidence.** UniProt entries for the 63 proteins were retrieved through the REST API (accessed November 2026) [15]; MOD_RES features and their literature references were parsed. 74 of 4,748 lysines carry at least one curated reference.

**Code and data.** All analysis scripts and intermediate tables are archived with the manuscript.

## References

[1] Zhang, D.; Tang, Z.; Huang, H.; et al. Metabolic Regulation of Gene Expression by Histone Lactylation. *Nature* **2019**, *574* (7779), 575-580. DOI: 10.1038/s41586-019-1678-1.
[2] Tan, M.; Luo, H.; Lee, S.; et al. Identification of 67 Histone Marks and Histone Lysine Crotonylation as a New Type of Histone Modification. *Cell* **2011**, *146* (6), 1016-1028. DOI: 10.1016/j.cell.2011.08.008.
[3] Dai, L.; Peng, C.; Montellier, E.; et al. Lysine 2-Hydroxyisobutyrylation Is a Widely Distributed Active Histone Mark. *Nat. Chem. Biol.* **2014**, *10* (5), 365-370. DOI: 10.1038/nchembio.1497.
[4] Gao, M.; Wang, J.; Rousseaux, S.; et al. Metabolically Controlled Histone H4K5 Acylation/Acetylation Ratio Drives BRD4 Genomic Distribution. *Cell Rep.* **2021**, *36* (4), 109460. DOI: 10.1016/j.celrep.2021.109460.
[5] Zhang, C.; Meng, Q.; Jiao, H.; et al. HNRNPU K181 Lactylation Drives Cervical Cancer Growth by Upregulating PHGDH and Reprogramming Serine Metabolism. *Adv. Sci.* **2026**, *13* (47), e20222. DOI: 10.1002/advs.202520222.
[6] Zhang, W.; Tan, X.; Lin, S.; et al. CPLM 4.0: An Updated Database with Rich Annotations for Protein Lysine Modifications. *Nucleic Acids Res.* **2022**, *50* (D1), D451-D459. DOI: 10.1093/nar/gkab849.
[7] Molendijk, J.; Yip, R.; Parker, B. L. urPTMdb/TeaProt: Upstream and Downstream Proteomics Analysis. *J. Proteome Res.* **2023**, *22* (2), 302-310. DOI: 10.1021/acs.jproteome.2c00048.
[8] Zuo, Y.; Wang, Q.; Tian, W.; et al. Pyruvate Is a Natural Suppressor of Interferon Signaling by Inducing STAT1 Protein Pyruvylation. *Cell* **2026**, *189* (7), 1975-1989.e19. DOI: 10.1016/j.cell.2026.01.023.
[9] Song, X.; Peng, P.; Zheng, H.; et al. Lysine Pyruvylation Couples Glycolytic Flux to Epigenetic Regulation. *Nat. Metab.* **2026**, *8* (7), 1495-1507. DOI: 10.1038/s42255-026-01556-2.
[10] Shrake, A.; Rupley, J. A. Environment and Exposure to Solvent of Protein Atoms. Lysozyme and Insulin. *J. Mol. Biol.* **1973**, *79* (2), 351-371. DOI: 10.1016/0022-2836(73)90011-9.
[11] Varadi, M.; Bertoni, D.; Magana, P.; et al. AlphaFold Protein Structure Database in 2024: Providing Structure Coverage for over 214 Million Protein Sequences. *Nucleic Acids Res.* **2024**, *52* (D1), D368-D375. DOI: 10.1093/nar/gkad1011.
[12] Jumper, J.; Evans, R.; Pritzel, A.; et al. Highly Accurate Protein Structure Prediction with AlphaFold. *Nature* **2021**, *596* (7873), 583-589. DOI: 10.1038/s41586-021-03819-2.
[13] Tien, M. Z.; Peters, J. K.; Zaks, T. M.; et al. Maximum Allowed Solvent Accessibilities of Residues in Proteins. *PLoS One* **2013**, *8* (11), e80635. DOI: 10.1371/journal.pone.0080635.
[14] UniProt Consortium. UniProt: The Universal Protein Knowledgebase in 2025. *Nucleic Acids Res.* **2025**, *53* (D1), D609-D617. DOI: 10.1093/nar/gkae1010.
[15] Ahmad, S.; Jose da Costa Gonzales, L.; Bowler-Barnett, E. H.; et al. The UniProt Website API: Facilitating Programmatic Access to Protein Knowledge. *Nucleic Acids Res.* **2025**, *53* (W1), W547-W553. DOI: 10.1093/nar/gkaf394.
[16] Poncha, K. F.; Paparella, A. T.; Young, N. L. Normalized and Directional Interplay Scoring for the Interrogation of Proteoform Data. *J. Proteome Res.* **2025**, *24* (4), 1765-1777. DOI: 10.1021/acs.jproteome.4c00877.
[17] Zhang, J. Lysine Pyruvylation: Decoding the Molecular Language of Pyruvate Signaling. *EMBO Mol. Med.* **2026**, *18* (10), 3879-3882. DOI: 10.1038/s44321-026-00522-5.
[18] Sung, E.; Sim, H.; Cho, Y. C.; et al. Global Profiling of Lysine Acetylation and Lactylation in Kupffer Cells. *J. Proteome Res.* **2023**, *22* (12), 3683-3691. DOI: 10.1021/acs.jproteome.3c00156.

All references were retrieved and read (abstract level) before citation. Corresponding author lists are truncated with et al.; complete author lists are to be exported from the publisher records at submission.

## Figure legends

**Figure 1. One site set, four reference sets.** (a) How each reference set samples lysines. Each bar is a protein and each tick a lysine; filled ticks are the lysines that enter the comparison set, pale ticks are excluded. A pools all catalogued lysines across proteins; B does the same separately within histone and non-histone strata; C draws its comparison from all lysines of the protein that contains each Kpy site; D restricts that comparison to catalogued lysines. (b) Fraction of catalogued Kpy sites that are multi-modified under A, B and D. Filled circles, observed; open circles, expectation; bars, Wilson 95% CI; numbers give observed counts over catalogued Kpy sites; dashed line, global baseline of 22.1%. (c) Reference set C: fraction of all 88 Kpy sites that are catalogued at all, with its expectation from the within-protein permutation (P = 0.275). (d) Catalogue coverage of Kpy sites by protein class.

**Figure 2. Annotation density and multi-modification across the catalogue.** (a) Annotation density (catalogued lysines divided by all lysines) for the 63 Kpy proteins, computed on full-length sequences; histones are shown separately and the four histone proteins are labelled. The dashed line marks the median over all 63 proteins (0.042). (b) Fraction of catalogued sites that are multi-modified, by acylation, with catalogue size in parentheses. Values span 23%-93% and do not order by chemical class.

**Figure 3. Structural context of multi-modified and Kpy lysines.** (a) Relative solvent accessibility (RSA) from AlphaFold models for all lysines, catalogued single-modified, multi-modified and Kpy sites; violins with individual residues and median bars. (b) Multi-modification rate across RSA bins for catalogued lysines, with Wilson 95% CI; n gives the number of catalogued lysines per bin. (c) pLDDT distributions for the same classes; percentages give the fraction below 50, taken as disordered. Multi-modified lysines are more buried and better ordered than single-modified ones; Kpy sites do not differ from other lysines.

**Figure 4. Curation depth and the reporting protocol.** (a) Fraction of lysines carrying a curated UniProt evidence line, for all catalogued lysines, single-modified lysines and multi-modified lysines in the 63 Kpy proteins; bars are Wilson 95% CIs and the numbers give the observed counts. The association is reported as consistent with, but not demonstrating, a study-depth confounder, because CPLM and UniProt curate the same primary literature. (b) Three-item reporting protocol; a co-occupancy comparison is interpretable only when the reference set is declared, protein composition is matched, and power is stated in terms of catalogued sites.

## Placeholders still open

[ ] target journal and reference style
[ ] GitHub repository DOI for the analysis code
[ ] whether the 88-site table includes predicted sites