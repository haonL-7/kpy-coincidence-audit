# unobtainable.md

## 定义与计数（已按 v2.2 修订）

v2.2 已查明：v2.1 中 9 个「文件内容与文件名不符」的文件，系协调方 `elink` 用前缀匹配 `pubmed_pmc` 时同时命中 `pubmed_pmc_refs`（引用该文的文献）所致，属装配缺陷，非文献状态。修正后按 PubMed 出版类型分离：一手研究 40 篇（取得 19、不可得 21），综述 15 篇（取得 9、不可得 6）。

一手研究口径：

| 类别 | 篇数 |
|---|---|
| 全文真正可得并已编码 | 19 |
| 文件内容与文件名不符（等于未取得） | 9 |
| 全文未取得（无 PMCID / 接口失败） | 12 |
| 合计 | 40 |

取得率 = 19/40 = 47.5%；不可得 21/40 = 52.5%，**超过 v2 §1.4 的 30% 阈值**，故本批结论只能以 case series 陈述，不得报百分比或比率。

## A. 文件内容与文件名不符的 9 篇（本次新发现，非文献本身不可得）

这 9 个 `{PMID}.xml` 文件解析出的内部 `article-id[pub-id-type=pmid]` 与文件名不一致，题录也完全不同。属交付物装配错误，不是文献状态。

| 文件名(PMid) | 文件内真实 PMID | 文件内真实题录 | 应是哪篇 |
|---|---|---|---|
| 36528218 | 37648228 | Recent progress in vaccine development targeting pre-clinical human toxoplasmosis (Parasites, Hosts and Diseases 2023) | Comparative analysis of protein expression systems and PTM landscape（ELK-1） |
| 36706705 | 40558384 | Mettl7a alleviated bone loss in osteoporosis mice by targeting the O-GlcNAcylation of Bsp via m6A methylation (Stem Cells Transl Med 2025) | Inhibition of protein phosphatase 2A by okadaic acid |
| 37392543 | 42823400 | Vascular calcification: pathogenic mechanisms, signaling crosstalk and translational therapeutics (Signal Transduct Target Ther 2026) | SIRT3-/FAK-mediated acetylation-phosphorylation crosstalk of NFATc1 |
| 38351418 | 42934178 | Histone Modifications at the Intersection of Aging, Neuroinflammation and Metabolism in Alzheimer's Disease (Aging Cell 2026) | H3K4 Trimethylation Mediate Hyperhomocysteinemia Induced Neurodegeneration |
| 38621458 | 42848643 | UBE2S promotes gastric cancer progression through RACGAP1 stabilization (Cancer Biol Ther 2026) | Cross-talk between BCKDK-mediated phosphorylation and STUB1-dependent ubiquitination |
| 38797435 | 42922678 | Molecular Insights into PKA Activity Modulation by Lysine Acetylation (Research Square 2026) | Global proteomic analyses of lysine acetylation, malonylation, succinylation, crotonylation in human sperm |
| 39569522 | 42958244 | Non-histone protein L-lactylation in cancer (Molecular Cancer 2026) | Subcellular Proteomic Mapping of Lysine Lactylation |
| 40437183 | 41357242 | Significance of SUMOylation in breast cancer progression (Front Immunol 2025) | Crosstalk between SUMOylation and ubiquitination controls stability of ZFP |
| 40827092 | 42491232 | Autophagy as a multi-scale architect of fungal development and pathogenicity (IMA Fungus 2026) | Sumoylation-dependent control of Pmk1 phosphorylation |

后果：这 9 篇的 C1/C2/C3 一律记 `not assessable`，并在编码表中标注 `full_text_obtained = no (file mismatch)`。**不得**把它们记为 `no`。

## B. 全文未取得的 12 篇（沿用协调方清单）

| PMID | 原因 | 是否影响判定 |
|---|---|---|
| 37067567 | 无 PMCID（出版商独占） | 是，记 not assessable |
| 38177062 | 无 PMCID（出版商独占） | 是，记 not assessable |
| 38512671 | 无 PMCID（出版商独占） | 是，记 not assessable |
| 41506171 | 无 PMCID（出版商独占） | 是，记 not assessable |
| 41555844 | 无 PMCID（出版商独占） | 是，记 not assessable |
| 41636360 | 无 PMCID（出版商独占） | 是，记 not assessable |
| 41724375 | 无 PMCID（出版商独占） | 是，记 not assessable |
| 42248319 | 无 PMCID（出版商独占） | 是，记 not assessable |
| 42316966 | 无 PMCID（出版商独占） | 是，记 not assessable |
| 42493429 | 无 PMCID（出版商独占） | 是，记 not assessable |
| 37783117 | 有 PMCID 但全文接口失败 | 是，记 not assessable |
| 39631394 | 有 PMCID 但全文接口失败 | 是，记 not assessable |

## C. 未覆盖的部分：15 篇综述

任务书 §4 要求对综述单独编码两项（是否对 crosstalk 证据分级、是否指出报告规范缺失）。本次提供的 28 个文件全部为一手研究，**目录中没有任何综述全文**，故该部分未执行，不产出任何综述编码结论。若需完成，需提供 15 篇综述的全文。

## D. 综述不可得 6 篇

v2.2 记录综述共 15 篇、取得 9 篇、不可得 6 篇，但未逐一列出这 6 个 PMID。下列 6 条系**由 16_sampling_frame.md 的 55 条清单反推**：该清单中标题与栏目标记为综述/观点类的共 15 条，扣除本次已取得全文的 9 条（41872850、41888923、41978829、42318360、42461359、42728596、42968629、39127633、39164116）后所得。此为推断，需协调方核对确认。

| PMID | 年 | 期刊 | 标题（截断） | 处理 |
|---|---|---|---|---|
| 42140345 | 2026 | Cancer Lett | Crotonylation: A novel layer of the epigenetic landscape in disease | not assessable |
| 42546407 | 2026 | Biomed Pharmacother | O-GlcNAc transferase as an oncogenic regulator in hematologic malignancies | not assessable |
| 42810107 | 2026 | Cancer Treat Res Commun | Post-translational acylation of proteins in colorectal cancer | not assessable |
| 42893777 | 2026 | Exp Neurol | Novel acylation modifications in cerebrovascular disease | not assessable |
| 41384850 | 2025 | FASEB J | Ubiquitination and Acetylation in Cellular Senescence: Mechanisms, Crosstalk | not assessable |
| 37236503 | 2023 | BBA Gene Regul Mech | Fine tuning of the transcription juggernaut: acetylation and ubiquitination | not assessable |

这 6 篇按 §4 的两项（是否分级、是否指出规范缺失）一律记 `not assessable`，**不记 `no`**。

## E. 汇总口径

| 类别 | 总数 | 取得 | 不可得 | 不可得比例 | 允许的陈述方式 |
|---|---|---|---|---|---|
| 一手研究 | 40 | 19 | 21 | 52.5% | 仅 case series，不得报百分比推断 |
| 综述 | 15 | 9 | 6 | 40.0% | 仅 case series（超过 30% 阈值） |

两部分均超过 v2 §1.4 的 30% 阈值，故 `summary.md` 中的两个分布均按 case series 陈述。
