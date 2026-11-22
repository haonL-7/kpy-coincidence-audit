# sampling_frame_v2.md：全文取得情况的最终口径

本文件不改动 sampling_frame.md（2026-11-03 的检索快照），只补充其后的全文获取状态。
表中数字由 artifacts/coding.csv 与 artifacts/unobtainable.md 自动汇总，不手工填写。

## 0 与 v1 的差异（必须先读）

| 项 | sampling_frame.md（v1，2026-11-03） | 本文件（v2，最终） |
|---|---|---|
| 一手研究取得全文 | 19 | **35** |
| 未取得 | 21 | **5** |
| 去重后独立研究 | 19 | **33** |

v1 的 19 是检索当日的抓取结果，其后经文件校验修复与补抓，实际取得 35 篇。
v1 中「obtained marks the 19 papers ... coded in coding.csv」一句因此已不成立。
**以本文件与 coding.csv 为准；sampling_frame.md 的取得数字视为历史快照，不再引用。**

## 1 未取得全文的 5 篇（记为 not assessable，不进任何分母）

| PMID | 期刊 | 年 | DOI | 编码表状态 |
|---|---|---|---|---|
| 36706705 | Biochem Biophys Res Commun | 2023 | 10.1016/j.bbrc.2023.01.033 | not assessable |
| 38177062 | Chem Res Toxicol | 2024 | 10.1021/acs.chemrestox.3c00298 | not assessable |
| 41506171 | Vet Microbiol | 2026 | 10.1016/j.vetmic.2026.110871 | not assessable |
| 42248319 | Cancer Lett | 2026 | 10.1016/j.canlet.2026.218650 | not assessable |
| 42316966 | J Proteome Res | 2026 | 10.1021/acs.jproteome.5c01243 | not assessable |

四家开放获取来源（Unpaywall、Europe PMC、Semantic Scholar、OpenAlex）均无合法全文，
按预注册规则不猜、不用替代文本，如实记为 not assessable。

## 2 同一研究的两对重复版本（合并为 1 条）

| 保留（正式版） | 合并（预印本） |
|---|---|
| 37723562 | 37398265 |
| 40948406 | 40462961 |

## 3 取得全文并编码的 35 篇

| # | PMID | 年 | 期刊 | 研究类型 |
|---|---|---|---|---|
| 1 | 36528218 | 2023 | Protein Expression and Purification | single-protein modification |
| 2 | 37067567 | 2023 | Amino Acids | bioinformatic in silico |
| 3 | 37086786 | 2023 | The Journal of Biological Chemistry | single-protein mechanism |
| 4 | 37102239 | 2023 | Thoracic Cancer | single-protein mechanism |
| 5 | 37392543 | 2023 | Atherosclerosis | single-protein modification |
| 6 | 37398265 | 2023 | Research Square | wet-lab omics (preprint; duplicate of 37 |
| 7 | 37723562 | 2023 | Cell Communication and Signaling : CCS | wet-lab omics |
| 8 | 37783117 | 2023 | Biochem Biophys Res Commun | wet-lab omics |
| 9 | 37858678 | 2023 | The Journal of Biological Chemistry | single-protein mechanism |
| 10 | 38222823 | 2023 | Horticulture Research | wet-lab omics |
| 11 | 38251723 | 2024 | eLife | single-protein mechanism |
| 12 | 38336175 | 2024 | Molecular & Cellular Proteomics : MCP | wet-lab omics |
| 13 | 38351418 | 2024 | Molecular Neurobiology | wet-lab mechanistic |
| 14 | 38512671 | 2024 | Methods in Molecular Biology | method/workflow |
| 15 | 38621458 | 2024 | Cancer Letters | wet-lab mechanistic |
| 16 | 38734627 | 2024 | Biology Direct | single-protein mechanism |
| 17 | 38797435 | 2024 | Journal of Proteomics | wet-lab omics |
| 18 | 39569522 | 2024 | Journal of the American Society for Mass Spectrometry | wet-lab omics |
| 19 | 39631394 | 2025 | Molecular Cell | wet-lab chromatin |
| 20 | 40437183 | 2025 | Oncogene | single-protein mechanism |
| 21 | 40462961 | 2025 | bioRxiv | single-protein mechanism |
| 22 | 40827092 | 2025 | New Phytologist | wet-lab mechanistic |
| 23 | 40845146 | 2025 | Genomics, Proteomics & Bioinformatics | wet-lab omics |
| 24 | 40948406 | 2025 | eLife | single-protein mechanism (published vers |
| 25 | 40994443 | 2025 | aBIOTECH | method/workflow |
| 26 | 41555844 | 2026 | Journal of Agricultural and Food Chemistry | wet-lab omics |
| 27 | 41636360 | 2026 | Journal of Agricultural and Food Chemistry | wet-lab omics |
| 28 | 41724375 | 2026 | Journal of Proteomics | wet-lab omics |
| 29 | 41729159 | 2026 | Annals of Medicine | wet-lab omics |
| 30 | 41803852 | 2026 | Cell Communication and Signaling : CCS | wet-lab omics |
| 31 | 41893314 | 2026 | Metabolites | bioinformatic integration |
| 32 | 42326659 | 2026 | ACS Omega | wet-lab omics |
| 33 | 42493429 | 2026 | Journal of Biomolecular Structure and Dynamics | bioinformatic in silico |
| 34 | 42807604 | 2026 | Precision Radiation Oncology | wet-lab omics |
| 35 | 42822389 | 2026 | Redox Biology | wet-lab omics |

## 4 口径核对

```
取得全文           35
减：预印本重复版本  2
= 独立研究         33   <- 表 S3(A) 行数
未取得全文          5   <- 记为 not assessable
合计               40   <- 与 40 篇一手研究相符
```

手稿表 S3 脚注写 35 records from 40 primary studies; two are preprints merged with their
published versions, leaving 33 studies，与本文件一致。

## 5 生成与维护

由 coding.csv 的 full_text_obtained 列与 unobtainable.md 的清单汇总；
生成时断言 35 / 5 / 33 三个数，任一不符即报错，不静默改写数字。
若日后取得其中任何一篇，改 coding.csv 后重新生成本文件，表 S3 与分母同步重算。
