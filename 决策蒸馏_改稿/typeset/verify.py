
# -*- coding: utf-8 -*-
import sys, re, zipfile
sys.stdout.reconfigure(encoding="utf-8")
from docx import Document
from docx.oxml.ns import qn
OUT = r"C:\Users\Administrator\Desktop\丙酮酰化\决策蒸馏与组织学习（成稿）.docx"
d = Document(OUT)
body = d.element.body
def txt(el): return "".join(t.text or "" for t in el.iter(qn("w:t")))
def ea(r):
    rf = r._r.find(qn("w:rPr"))
    rf = rf.find(qn("w:rFonts")) if rf is not None else None
    return rf.get(qn("w:eastAsia")) if rf is not None else None

print("########## 1. 节 / 页脚 / 页码 ##########")
print("节数:", len(d.sections))
for k, s in enumerate(d.sections):
    sect = s._sectPr
    fr = sect.find(qn("w:footerReference")); pgn = sect.find(qn("w:pgNumType"))
    print(" sec%d 页脚引用=%s 页码起点=%s 页面=%.2fx%.2fcm 边距 上%.2f/下%.2f/左%.2f/右%.2f" % (
        k, "有" if fr is not None else "无", pgn.get(qn("w:start")) if pgn is not None else "-",
        s.page_width.cm, s.page_height.cm, s.top_margin.cm, s.bottom_margin.cm, s.left_margin.cm, s.right_margin.cm))
f1 = d.sections[1].footer
ft = "".join(t.text or "" for t in f1._element.iter(qn("w:t")))
has_fld = "PAGE" in "".join(i.text or "" for i in f1._element.iter(qn("w:instrText")))
pp = f1.paragraphs[0]
print(" 页脚文本=%r PAGE域=%s 对齐=%s 字号=%s 东文字体=%s" % (ft, has_fld, pp.alignment,
      pp.runs[0].font.size.pt if pp.runs and pp.runs[0].font.size else None, ea(pp.runs[0]) if pp.runs else None))

print("########## 2. 标题层级 ##########")
def lvl(p):
    ppr = p._p.find(qn("w:pPr"))
    if ppr is None: return None
    ol = ppr.find(qn("w:outlineLvl"))
    return ol.get(qn("w:val")) if ol is not None else None
h1 = [p for p in d.paragraphs if lvl(p) == "0"]
h2 = [p for p in d.paragraphs if lvl(p) == "1"]
print("一级标题 %d 个:" % len(h1))
for p in h1:
    r = p.runs[0]; pf = p.paragraph_format; ppr = p._p.find(qn("w:pPr"))
    print("   %-26s 字号=%.1f 东文=%s 加粗=%s 对齐=%s 另起页=%s outlineLvl=0 段前/后=%s/%s keepNext=%s" % (
        txt(p._p)[:24], r.font.size.pt, ea(r), r.font.bold, p.alignment,
        ppr.find(qn("w:pageBreakBefore")) is not None,
        pf.space_before.twips, pf.space_after.twips, ppr.find(qn("w:keepNext")) is not None))
print("三级小节 %d 个:" % len(h2))
for p in h2:
    r = p.runs[0]; pf = p.paragraph_format; ppr = p._p.find(qn("w:pPr"))
    print("   %-10s 字号=%.1f 东文=%s 加粗=%s outlineLvl=1 段前/后=%s/%s keepNext=%s" % (
        txt(p._p), r.font.size.pt, ea(r), r.font.bold, pf.space_before.twips, pf.space_after.twips,
        ppr.find(qn("w:keepNext")) is not None))
BIG = txt(h2[0]._p)  # placeholder overwritten below
t = [p for p in d.paragraphs if txt(p._p).startswith("决策蒸馏与组织学习：宏集智能体") and lvl(p) is None][0]
print("大标题: %r 字号=%.1f 东文=%s 加粗=%s 对齐=%s 段前/后=%s/%s br数=%d" % (
    txt(t._p), t.runs[0].font.size.pt, ea(t.runs[0]), t.runs[0].font.bold, t.alignment,
    t.paragraph_format.space_before.twips, t.paragraph_format.space_after.twips,
    len(t._p.findall(".//" + qn("w:br")))))

print("########## 3. 正文 / 摘要 / 参考文献 ##########")
fl = [p for p in d.paragraphs if p._p.find(qn("w:pPr")) is not None
      and p._p.find(qn("w:pPr")).find(qn("w:ind")) is not None
      and p._p.find(qn("w:pPr")).find(qn("w:ind")).get(qn("w:firstLineChars")) == "200"]
print("首行缩进 2 字符(firstLineChars=200) 段落数:", len(fl))
p0 = fl[2]
ind0 = p0._p.find(qn("w:pPr")).find(qn("w:ind"))
print(" 样例: firstLine=%s firstLineChars=%s 行距=%s 对齐=%s widowControl=%s 字号=%.1f 东文=%s" % (
    ind0.get(qn("w:firstLine")), ind0.get(qn("w:firstLineChars")), p0.paragraph_format.line_spacing,
    p0.alignment, p0._p.find(qn("w:pPr")).find(qn("w:widowControl")) is not None,
    p0.runs[0].font.size.pt, ea(p0.runs[0])))
abs_p = [p for p in d.paragraphs if txt(p._p).startswith("摘要：")][0]
kw_p = [p for p in d.paragraphs if txt(p._p).startswith("关键词：")][0]
for nm, p in (("摘要", abs_p), ("关键词", kw_p)):
    lab, rest = p.runs[0], p.runs[1]
    ind = p._p.find(qn("w:pPr")).find(qn("w:ind"))
    print(" %s: 标签东文=%s 加粗=%s 字号=%.1f / 正文东文=%s 加粗=%s 字号=%.1f firstLineChars=%s" % (
        nm, ea(lab), lab.font.bold, lab.font.size.pt, ea(rest), rest.font.bold, rest.font.size.pt, ind.get(qn("w:firstLineChars"))))
refs = [p for p in d.paragraphs if re.match(r"^\[\d+\]", txt(p._p))]
ri = refs[0]._p.find(qn("w:pPr")).find(qn("w:ind"))
print("参考文献: 标题数=%d 条目数=%d 首=%s 末=%s 字号=%.1f 东文=%s 悬挂=%s 左=%s 行距=%s" % (
    len([p for p in h1 if txt(p._p) == "参考文献"]), len(refs), txt(refs[0]._p)[:4], txt(refs[-1]._p)[:5],
    refs[0].runs[0].font.size.pt, ea(refs[0].runs[0]), ri.get(qn("w:hanging")), ri.get(qn("w:left")),
    refs[0].paragraph_format.line_spacing))

print("########## 4. 图 ##########")
imgs = body.findall(".//" + qn("w:drawing"))
print("图片数量(全文):", len(imgs))
for dr in imgs:
    ext = dr.find(".//{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}extent")
    print("  尺寸 %.2f x %.2f cm" % (int(ext.get("cx"))/360000, int(ext.get("cy"))/360000))
FIGDRAW = [k for k, p in enumerate(d.paragraphs)
           if p._p.find(".//" + qn("w:drawing")) is not None
           and k + 1 < len(d.paragraphs) and txt(d.paragraphs[k+1]._p).startswith("图")]
print("  封面校徽段索引 0..24 内；正文图段索引:", FIGDRAW)
for k in FIGDRAW:
    p = d.paragraphs[k]
    if True:
        ppr = p._p.find(qn("w:pPr")); ind = ppr.find(qn("w:ind"))
        print("  图片段: 对齐=%s keepNext=%s ind属性=%s" % (
            p.alignment, ppr.find(qn("w:keepNext")) is not None, dict(ind.attrib) if ind is not None else None))
        cap = d.paragraphs[k+1]; cp2 = cap._p.find(qn("w:pPr"))
        print("  图题段: %r 字号=%.1f 东文=%s 加粗=%s 对齐=%s keepNext=%s" % (
            txt(cap._p), cap.runs[0].font.size.pt, ea(cap.runs[0]), cap.runs[0].font.bold, cap.alignment,
            cp2.find(qn("w:keepNext")) is not None))
        print("  图题前3字码点:", [hex(ord(c)) for c in txt(cap._p)[:3]])
        prev = d.paragraphs[k-1]
        print("  图片段前一段末20字: %r" % txt(prev._p)[-20:])

print("########## 5. 引号 / 占位符 ##########")
alltxt = "\n".join(txt(p._p) for p in d.paragraphs)
print('直双引号 = %d 直单引号 = %d' % (alltxt.count(chr(34)), alltxt.count(chr(39))))
print("中文引号 “ = %d ” = %d" % (alltxt.count(chr(0x201c)), alltxt.count(chr(0x201d))))
for pat in ["〔", "〕", "待核", "**", "TODO", "XXX", "请在此", "（略）", "模板", "冯文", "   "]:
    print("  扫描 %-6r = %d" % (pat, alltxt.count(pat)))
print("总段落数:", len(d.paragraphs), " 总字符数:", len(alltxt))
print("文档属性:", d.core_properties.author, d.core_properties.last_modified_by, d.core_properties.title)

print("########## 6. OOXML 子元素顺序 ##########")
z = zipfile.ZipFile(OUT)
ORDER = {
 "pPr": ["pStyle","keepNext","keepLines","pageBreakBefore","framePr","widowControl","numPr","suppressLineNumbers",
         "pBdr","shd","tabs","suppressAutoHyphens","kinsoku","wordWrap","overflowPunct","topLinePunct","autoSpaceDE",
         "autoSpaceDN","bidi","adjustRightInd","snapToGrid","spacing","ind","contextualSpacing","mirrorIndents",
         "suppressOverlap","jc","textDirection","textAlignment","textboxTightWrap","outlineLvl","divId","cnfStyle","rPr","sectPr","pPrChange"],
 "rPr": ["rStyle","rFonts","b","bCs","i","iCs","caps","smallCaps","strike","dstrike","outline","shadow","emboss",
         "imprint","noProof","snapToGrid","vanish","webHidden","color","spacing","w","kern","position","sz","szCs",
         "highlight","u","effect","bdr","shd","fitText","vertAlign","rtl","cs","em","lang","eastAsianLayout",
         "specVanish","oMath","rPrChange"],
 "tcPr": ["cnfStyle","tcW","gridSpan","hMerge","vMerge","tcBorders","shd","noWrap","tcMar","textDirection","tcFitText",
          "vAlign","hideMark"],
 "trPr": ["cnfStyle","divId","gridBefore","gridAfter","wBefore","wAfter","cantSplit","trHeight","tblHeader",
          "tblCellSpacing","jc","hidden"],
 "tblPr": ["tblStyle","tblpPr","tblOverlap","bidiVisual","tblStyleRowBandSize","tblStyleColBandSize","tblW","jc",
           "tblCellSpacing","tblInd","tblBorders","shd","tblLayout","tblCellMar","tblLook"],
}
WN = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
import xml.etree.ElementTree as ET
bad = 0
for name in z.namelist():
    if not name.startswith("word/") or not name.endswith(".xml"): continue
    root = ET.fromstring(z.read(name))
    for tag, order in ORDER.items():
        for el in root.iter(WN + tag):
            kids = [c.tag.split("}")[1] for c in el]
            idx = [order.index(k) for k in kids if k in order]
            if idx != sorted(idx):
                bad += 1; print("  顺序违规", name, tag, kids)
            unk = [k for k in kids if k not in order]
            if unk:
                bad += 1; print("  未知子元素", name, tag, unk)
print("子元素顺序违规:", bad)
