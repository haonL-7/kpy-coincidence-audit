# summary.md

`two independent coders; agreement and adjudication recorded in agreement_stats.csv and adjudication_log_signed.csv`

## 0. 版本（v1.3.2，2026-11-18）

v1.3.1 的 `leave_one_out.py` 把「只带查询修饰、不带其他修饰」的位点放进了对照行，
导致九个 MH OR 系统性偏高（乙酰化 11.13 → 2.13）。v1.3.2 已修复，Table S1、Table S4
及正文相关数字全部重算。Kpy 行不受影响（其位点在目录之外，2.60 不变）。详见
`RELEASE_NOTES_v1.3.2.md`。

## 1. 可陈述范围

四条 PubMed 检索式（2023-01-01 起）返回 794 条唯一记录，经标题摘要筛选余 55 条，
其中一手研究 40 篇、综述 15 篇。

| 项 | 记录数 |
|---|---|
| 一手研究 | 40 |
| 取得全文并编码 | 35 |
| 其中预印本与正式版重复 | 2 对 |
| 去重后独立研究 | 33 |
| 仍未取得 | 5 |

未取得的 5 篇逐一列在 `unobtainable.md`，在编码表中记为 not assessable，不计入任何基数。

## 2. 编码结果（按独立研究，n = 33）

| 项 | 适用 | no | partial | yes | NA |
|---|---|---|---|---|
| C1 期望集合 | 19 | 18 | 1 | 0 | 14 |
| C2 蛋白构成 | 19 | 6 | 8 | 5 | 14 |
| C3 功效 | 31 | 20 | 11 | 0 | 2 |

三项同时为 yes 的研究：0。

NA 的含义按列区分：C1 的 NA 是「没有跨修饰重合比较」，C2 的 NA 是「没有两个集合的构成比较」，
两者都不是「缺失陈述」。C3 有 2 篇 NA：这两篇没有需要功效陈述的定量比较。

## 3. 判定依据

每条判定在 `coding.csv` 的 `C1_evidence` / `C1_location` 等列中附逐字引文与所在章节，
可由第三方复核。综述表 `reviews_coding.csv` 同。

## 4. 边界

- 两名编码者独立编码，裁决由 S.L. 复核确认；一致性数字见 `agreement_stats.csv`，逐格裁决见 `adjudication_log_signed.csv`（两份文件均已随仓库提交）。
- 计数描述的是取得全文的 33 个研究，不是该领域全部文献。

- `agreement_stats.csv` 的 E、R 两行保留了 κ 数值（0.250、0.100），但正文只报一致率：n = 9、二分类、边际倾斜时 κ 不稳定，数值仅作原始记录，不作为一致性证据。
