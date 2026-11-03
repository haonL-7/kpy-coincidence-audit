# TOC 图形（ACS/JPR）

**最终版：A2（树状分叉 + 色条）**，已按 ACS/JPR 要求交付。A2 是在 A 的结构上只改排版得到：去掉内部重复标题、彩色胶囊改为窄色条 + sig./n.s.、正文字号 6.2→7 pt、点阵 88→30 个。

## 交付文件

| 文件 | 说明 |
|---|---|
| TOC_graphic_final.svg | 可编辑矢量源（文字未转曲，Arial） |
| toc_final.pdf | 矢量 PDF，**页面实测 MediaBox [0 0 234 126] pt = 3.25 × 1.75 in** |
| toc_final.tif | 975 × 525 px ≈ 300 dpi，未压缩 TIFF（ACS 接受 TIFF/EPS/PDF） |
| toc_a2.png | 300 dpi PNG 预览 |
| toc_a2_true_size.png | 按 234 × 126 px 缩放的"真实目录尺寸"对照图 |

## 规格核对

- 尺寸：3.25 × 1.75 in（ACS TOC/Abstract Graphic 上限），PDF 页面实测一致。
- 字体：Arial，最小 6.6 pt（sig./n.s. 列），正文 7 pt。
- 颜色：绿 #009E73 / 琥珀 #E69F00 / 灰 #BBBBBB，三种在灰度下明度可分；色条与 sig./n.s. 文本冗余编码，不依赖颜色单独承载语义。
- 图内无标题：ACS 目录页会在图形旁印论文标题，图内重复属冗余。

## 淘汰与备选

- TOC_A_tree.svg（含内部标题 + 文字胶囊）：真实尺寸下胶囊文字糊成一团，已弃用。
- TOC_B_rows.svg（三段流水线）：列标题版，图示更易读但结构修辞弱，留作备选。

## 渲染方式（复现用）

Edge headless，**必须用全新的 user-data-dir**，且只有旧版 `--headless` 能截图（`--headless=new` 不出图）：

    msedge --headless --disable-gpu --no-sandbox --user-data-dir=<fresh> \
      --screenshot=out.png --window-size=975,525 file:///.../preview.html

PDF 用 `--print-to-pdf`，页面尺寸由 HTML 的 `@page { size: 3.25in 1.75in; margin: 0 }` 决定。
