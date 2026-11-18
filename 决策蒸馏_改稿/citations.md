# 文献登记与核验状态（18 条）

核验日期：2026-11-07。方法：`curl -sL --compressed -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"` 取页面并比对标题/正文原句；期刊用 `api.crossref.org` 按 DOI 与 `query.bibliographic` 双向核对卷、期、页码、年份、作者。

## 汇总

| 状态 | 条数 | 条目 |
|---|---|---|
| 核验通过（题录与可打开页面/DOI 一致） | 12 | [1][2][3][6][7][8][11][12][15][16][17][18] |
| 部分核验（存在一条以上字段无法确认，均注明） | 3 | [5][9][13] |
| 未核验（原因见条目） | 1 | [4] |
| 预印本（题目、作者、日期已核；无正式发表版本） | 2 | [10][14] |
| 合计 | 18 | — |

B 阶段改动：更新 1 条（[6]）、补 URL 1 条（[8]）、补「[预印本]」2 条（[10][14]）、题名校正 1 条（[15]）。其余条目一字未动，编号未动。

## 逐条

### [1] 农业农村部, 中央网络安全和信息化委员会办公室. 数字农业农村发展规划（2019—2025年）[EB/OL]. (2020-01-20)[2026-10-20].
- 状态：核验通过
- 页面 https://www.moa.gov.cn/govpublic/FZJHS/202001/t20200120_6336316.htm → HTTP 200；页面标题「农业农村部 中央网络安全和信息化委员会办公室关于印发《数字农业农村发展规划（2019-2025年）》的通知」，文号 农规发〔2019〕33号，发布日期 2020-01-20，与条目一致。

### [2] PAPADOPOULOS G, PAPANTONATOU M Z, UYAR H, et al. Economic and environmental benefits of digital agricultural technological solutions in livestock farming: a review[J]. Smart Agricultural Technology, 2025, 10: 100783.
- 状态：核验通过
- Crossref：DOI 10.1016/j.atech.2025.100783；刊名 Smart Agricultural Technology，卷 10，页码 100783，2025 年，作者 Papadopoulos / Papantonatou / Uyar —— 与条目完全一致。

### [3] DAO S D, GOSTAR A K, TENNAKOON R, et al. Modernizing livestock operations: smart feedlot technologies and their impact[J]. Animals, 2026, 16(8): 1244.
- 状态：核验通过
- Crossref：DOI 10.3390/ani16081244；Animals，卷 16，期 8，页码 1244，2026 年，作者 Dao / Khodadadian Gostar / Tennakoon —— 一致。（同年有 TechRxiv 预印版本，正文引用期刊版无误。）

### [4] 靖环宇. 数字化转型对中小规模奶牛养殖场生产成本影响研究：以华盛奶牛养殖专业合作社为例[D]. 泰安: 山东农业大学, 2024.
- 状态：**未核验**
- 原因：条目未给 DOI 与 URL；中国知网学位论文库为登录制且正文由脚本渲染，用 curl 取不到题录页，无法确认作者、年份与培养单位。未删除，未改写，等待作者补 CNKI 链接或 DOI 后再核。

### [5] 谢东阳. 生猪养殖MY公司智能化养殖价值链成本管优化研究[D]. 杨凌: 西北农林科技大学, 2023. DOI: 10.27409/d.cnki.gxbnu.2023.002796.
- 状态：部分核验
- DOI 10.27409/d.cnki.gxbnu.2023.002796 经 doi.org 解析（HTTP 200）跳转至 kns.cnki.net 记录页，说明 DOI 存在且指向该论文；题录字段（题目、年份、单位）需登录后可见，未能逐字比对。另：题名中「成本管优化研究」疑缺字（应为「成本管控优化」或「成本管理优化」），属原条目写法，未擅自改动，请作者核对。

### [6] 农视网. 2024年农业农村发展成就[EB/OL]. (2024-12-25)[2026-11-07]. https://www.ntv.cn/content/1/392/991392652.html.
- 状态：核验通过（B 阶段更新）
- 页面 HTTP 200，标题「2024年农业农村发展成就」，发布日 2024-12-25。正文原句：「预计今年全国生猪养殖规模化率（年出栏500头以上的规模养殖占比）超过70%，同比提高约2个百分点。」
- 同一发布会的另一著录版本：中国新闻网 2024-12-21（证券时报转载 https://www.stcn.com/article/detail/1463240.html）：「预计今年全国生猪养殖规模化率(年出栏500头以上的规模养殖占比)超过70%，同比提高约2个百分点。」两者同源，本稿取农视网。
- 原条目（被替换）留档：光明网《农业农村部：预计2023年生猪养殖规模化率将超过68%》https://m.gmw.cn/2024-01/23/content_1303640502.htm → 页面 HTTP 200，正文含「预计2023年生猪养殖规模化率将超过68%，比2022年提升约3个百分点」；但**页面标题实为「农业农村部：抓好三方面工作 促进生猪生产稳定发展」（来源人民网）**，原条目把正文句当成了标题。这是原条目被换掉的两个理由之一（另一个是年度过旧）。

### [7] 上海钢联（Mysteel农产品）. 2026年5月猪市：财报亏、成本高，企业还能支撑多久？[EB/OL]. (2026-05-19)[2026-10-20]. https://www.caaa.cn/html/fw/market/zhu/2026/0519/23756.html.
- 状态：核验通过（行业机构口径）
- 页面 HTTP 200，标题「Mysteel农产品解读：2026年5月猪市：财报亏、成本高，企业还能支撑多久？（20260519）」，与条目一致；发布日期与 URL 路径 2026/0519 相符。
- 口径提示：该文是行情分析，不是统计口径。正文「饲料占生猪养殖总成本的60%–70%」一句已补「行业机构口径」（见 changes.md B-2）。

### [8] 讯飞和光打造AI"老兽医" 推动养猪业迈入智能阶段[N/OL]. 科技日报, 2026-04-29[2026-11-07]. https://www.stdaily.com/web/gdxw/2026-04/29/content_510139.html.
- 状态：核验通过（B 阶段补 URL）
- 页面 HTTP 200，标题一致，日期 2026-04-29 20:19，记者都芃，来源「科技日报」。正文原句：「声纹模型可从嘈杂环境中精准识别异常声响，健康预警提前2至3天」。
- 注：原文写「疫病预警提前2至3天」，来源写「健康预警提前2至3天」，属同义转述，数字未动；正文已补「据其公开材料」点明为企业方说法（见 changes.md B-3）。该文同段还给出「2025年全国生猪出栏量达71973万头，其中超七成来自规模化养殖场」，可作 B-1 的旁证，但不是官方统计口径。

### [9] GAO J, ZHANG Y, CHEN Y, et al. Agent-in-the-loop to distill expert knowledge into artificial intelligence models: a survey[J]. Artificial Intelligence Review, 2025, 58(9): 1-55.
- 状态：部分核验
- Crossref：DOI 10.1007/s10462-025-11255-1；Artificial Intelligence Review，卷 58，期 9，2025 年，作者 Gao / Zhang / Chen —— 作者、刊名、卷期年一致。
- 未能确认字段：页码。Crossref 记录无 page（Springer 近年以文章号著录），条目中的「1-55」无法复核。**页码以出版社页面为准，Crossref 无记录**；经作者决定保留原样，不改文章号（无记录不等于可以猜）。

### [10] GOU C, TU H, FANG Y, et al. Sample-efficient learning from agent experience[EB/OL]. (2026)[2026-10-20]. https://arxiv.org/abs/2607.21051. [预印本]
- 状态：预印本（B 阶段加标记）
- arXiv 摘要页 HTTP 200，题名一致，提交日 2026-07-23，分类 cs.CL，作者 Chenhui Gou / Haoqin Tu / Yunhao Fang / Jianfei Cai / Hamid Rezatofighi。
- 正式发表版本：arXiv 页面无 Journal reference、无 DOI，Comments 字段为空；按题名与作者检索 Crossref 未见期刊版。故按预印本著录，正文引用未动。

### [11] MANNES A E, SOLL J B, LARRICK R P. The wisdom of select crowds[J]. Journal of Personality and Social Psychology, 2014, 107(2): 276-299.
- 状态：核验通过
- Crossref：DOI 10.1037/a0036677；Journal of Personality and Social Psychology，卷 107，期 2，页码 276-299，2014 年，作者 Mannes / Soll / Larrick —— 全部一致。条目未著录 DOI，可选择性补上。

### [12] BAHLO C, DAHLHAUS P, THOMPSON H, et al. The role of interoperable data standards in precision livestock farming in extensive livestock systems: a review[J]. Computers and Electronics in Agriculture, 2019, 156: 459-466. DOI: 10.1016/j.compag.2018.12.007.
- 状态：核验通过
- Crossref：DOI 一致；Computers and Electronics in Agriculture，卷 156，页码 459-466，2019 年，作者 Bahlo / Dahlhaus / Thompson —— 全部一致。

### [13] 从ChatGPT到ChickenGPT？零一万物和正大集团把AI带进鸡舍[EB/OL]. [2026-10-20]. https://www.zgswcn.com/news.html?aid=345926.
- 状态：部分核验
- 页面 HTTP 200 但正文由前端脚本渲染，curl 取回的 HTML 只有模板占位（{{columnName}} / {{content.title}}），标题、发布时间、正文均无法从源码读取，因此未能比对题名与日期。条目未改。
- 建议：作者补发布日期，或换一条可静态读取的转载页。

### [14] LI Y, MIAO Y, KRISHNAN R, et al. JEV-as-a-judge: accept when confident, escalate when unsure[EB/OL]. (2026)[2026-10-20]. https://arxiv.org/abs/2609.26550. [预印本]
- 状态：预印本（B 阶段加标记）
- arXiv 摘要页 HTTP 200，题名一致，提交日 2026-09-22，分类 cs.AI，作者 Yubo Li / Yidi Miao / Ramayya Krishnan / Rema Padman。
- 正式发表版本：Comments 只有「An open-source Jev's alternative comparison is added to appendix A」，无 Journal reference、无 DOI；检索未见期刊版。按预印本著录，正文引用未动。

### [15] 全球农食产业领袖在"农业达沃斯"论坛共话AI+养猪新成果[EB/OL]. (2025-10-17)[2026-10-20]. https://www.farmer.com.cn/2025/10/17/991002119.html.
- 状态：核验通过（B 阶段题名校正：AI养猪 → AI+养猪）
- 页面 HTTP 200，标题一致，发布 2025-10-17 23:18，农民日报·中国农网记者 吴砾星、李红波。正文原句：「该客户在25万头母猪的体系中…综合成本比原来再低了0.4元/斤」；「FPF母猪养殖在线…为企业带来管理效率提升30%以上的直观改变」；「在中小规模猪场中，部分案例已验证能为每头母猪每年创造超4000元的效益增收」。三个数字均在源文中，属企业方在论坛的发布，正文已补「企业口径」。

### [16] MARCH J G. Exploration and exploitation in organizational learning[J]. Organization Science, 1991, 2(1): 71-87.
- 状态：核验通过
- Crossref：DOI 10.1287/orsc.2.1.71；Organization Science，卷 2，期 1，页码 71-87，1991 年，作者 March —— 全部一致。

### [17] LORENZ J, RAUHUT H, SCHWEITZER F, et al. How social influence can undermine the wisdom of crowd effect[J]. Proceedings of the National Academy of Sciences, 2011, 108(22): 9020-9025.
- 状态：核验通过
- Crossref：DOI 10.1073/pnas.1008636108；PNAS，卷 108，期 22，页码 9020-9025，2011 年，作者 Lorenz / Rauhut / Schweitzer —— 全部一致。条目未著录 DOI，可选择性补上。

### [18] BAZAZI S, VON ZIMMERMANN J, BAHRAMI B, et al. Self-serving incentives impair collective decisions by increasing conformity[J]. PLoS ONE, 2019, 14(11): e0224725.
- 状态：核验通过
- Crossref：DOI 10.1371/journal.pone.0224725；PLOS ONE，卷 14，期 11，页码 e0224725，2019 年，作者 Bazazi / von Zimmermann / Bahrami —— 全部一致。

## B 阶段新增/变更的来源（另附）

| 用于 | 来源 | 可核原句 |
|---|---|---|
| B-1 规模化率 | 农视网《2024年农业农村发展成就》(2024-12-25) https://www.ntv.cn/content/1/392/991392652.html | 「预计今年全国生猪养殖规模化率（年出栏500头以上的规模养殖占比）超过70%，同比提高约2个百分点。」 |
| B-1 同源旁证 | 中国新闻网 2024-12-21（证券时报转载）https://www.stcn.com/article/detail/1463240.html | 「预计今年全国生猪养殖规模化率(年出栏500头以上的规模养殖占比)超过70%，同比提高约2个百分点。」 |
| B-3 声纹口径 | 科技日报 2026-04-29 https://www.stdaily.com/web/gdxw/2026-04/29/content_510139.html | 「声纹模型可从嘈杂环境中精准识别异常声响，健康预警提前2至3天」 |
| B-3 企业数字 | 中国农网 2025-10-17 https://www.farmer.com.cn/2025/10/17/991002119.html | 「综合成本比原来再低了0.4元/斤」「管理效率提升30%以上」「每头母猪每年创造超4000元的效益增收」 |

## 查到但未采用的官方口径（供作者决定）

| 来源 | 内容 | 未采用原因 |
|---|---|---|
| 农业农村部 2026-01-22 国新办发布会 https://npecrr.agri.cn/snxwfbjj/fbjj2026/202601/t20260122_469381.htm | 「2025年我国猪牛羊禽肉产量达到10072万吨…全国畜禽养殖规模化率超过75%」 | 统计对象为「畜禽」，与「生猪」口径不同，不宜替换 |
| 养猪网 2026-08-28 https://news.zhuwang.com.cn/xinwen/20260828/650294.html | 「农业农村部数据显示，当前全国生猪养殖规模化率已达73%左右，较十年前提升约30个百分点」 | 无发布年度、无口径定义，属二次转述 |
