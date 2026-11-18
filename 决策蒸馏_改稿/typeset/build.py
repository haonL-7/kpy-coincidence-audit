
# -*- coding: utf-8 -*-
import re, copy, sys, os, datetime
sys.stdout.reconfigure(encoding="utf-8")
from xml.sax.saxutils import escape
from docx import Document
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
from docx.shared import Cm
from docx.text.paragraph import Paragraph

DRAFT = r"C:\Users\Administrator\Desktop\丙酮酰化\决策蒸馏_改稿\draft_final.md"
COVER = r"C:\Users\Administrator\Documents\xwechat_files\wxid_h72ol1ylw9hv22_d04f\msg\file\2026-11\五-11_本轮生猪产能调控政策的成效评估与养殖场经营风险分.docx"
FIG   = r"C:\Users\Administrator\Desktop\丙酮酰化\决策蒸馏_改稿\figure_1.png"
OUT   = r"C:\Users\Administrator\Desktop\丙酮酰化\决策蒸馏与组织学习（成稿）.docx"

# ---------- xml helpers ----------
def rpr(cn="宋体", sz=24, bold=False, u=None, hint="eastAsia"):
    s = ('<w:rPr><w:rFonts w:hint="%s" w:ascii="Times New Roman" w:hAnsi="Times New Roman" '
         'w:eastAsia="%s" w:cs="Times New Roman"/>' % (hint, cn))
    s += "<w:b/>" if bold else '<w:b w:val="0"/>'
    s += '<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (sz, sz)
    if u: s += '<w:u w:val="%s"/>' % u
    s += "</w:rPr>"
    return s

def run(text, rp):
    sp = ' xml:space="preserve"' if (text != text.strip() or "  " in text) else ""
    return "<w:r>" + rp + "<w:t%s>%s</w:t></w:r>" % (sp, escape(text))

def brk_run(rp):
    return "<w:r>" + rp + '<w:br w:type="textWrapping"/></w:r>'

P_TITLE = ('<w:snapToGrid w:val="0"/><w:spacing w:before="240" w:after="240" w:line="360" w:lineRule="auto"/>'
           '<w:ind w:left="0" w:firstLine="0"/><w:jc w:val="center"/>')
def P_H1(center=False, pagebreak=False):
    s = "<w:keepNext/><w:keepLines/>"
    if pagebreak: s += "<w:pageBreakBefore/>"
    s += ('<w:snapToGrid w:val="0"/><w:spacing w:before="240" w:after="120" w:line="360" w:lineRule="auto"/>'
          '<w:ind w:left="0" w:firstLine="0"/><w:jc w:val="%s"/><w:outlineLvl w:val="0"/>' % ("center" if center else "left"))
    return s
P_H2 = ('<w:keepNext/><w:keepLines/><w:snapToGrid w:val="0"/>'
        '<w:spacing w:before="120" w:after="60" w:line="360" w:lineRule="auto"/>'
        '<w:ind w:left="0" w:firstLine="0"/><w:jc w:val="left"/><w:outlineLvl w:val="1"/>')
P_BODY = ('<w:widowControl/><w:snapToGrid w:val="0"/>'
          '<w:spacing w:before="0" w:after="0" w:line="360" w:lineRule="auto"/>'
          '<w:ind w:left="0" w:firstLine="480" w:firstLineChars="200"/><w:jc w:val="both"/>')
# figure paragraphs: identical pPr to 六-1 成稿 (image para / caption para)
P_FIG = ('<w:keepNext/><w:keepLines/><w:widowControl/><w:snapToGrid w:val="0"/>'
         '<w:spacing w:before="120" w:after="60" w:line="360" w:lineRule="auto"/>'
         '<w:ind w:left="0"/><w:jc w:val="center"/>')
P_CAP = ('<w:keepNext/><w:keepLines/><w:widowControl/><w:snapToGrid w:val="0"/>'
         '<w:spacing w:before="0" w:after="60" w:line="360" w:lineRule="auto"/>'
         '<w:ind w:left="0"/><w:jc w:val="center"/>')
P_REF = ('<w:widowControl/><w:snapToGrid w:val="0"/>'
         '<w:spacing w:before="0" w:after="0" w:line="360" w:lineRule="auto"/>'
         '<w:ind w:left="840" w:leftChars="200" w:hanging="420" w:hangingChars="200"/><w:jc w:val="left"/>')

# ---------- read draft ----------
raw = open(DRAFT, encoding="utf-8").read()
lines = [l.rstrip("\n") for l in raw.split("\n")]

blocks, i = [], 0
while i < len(lines):
    ln = lines[i].strip()
    if not ln:
        i += 1; continue
    if ln.startswith("# "):
        blocks.append(("title", ln[2:].strip()))
    elif ln.startswith("### "):
        blocks.append(("h2", ln[4:].strip()))
    elif ln.startswith("## "):
        t = ln[3:].strip()
        if t.startswith("摘要："): blocks.append(("abs", t))
        elif t.startswith("关键词："): blocks.append(("kw", t))
        elif t == "参考文献": blocks.append(("refhead", t))
        else: blocks.append(("h1", t))
    elif re.match(r"^!\[", ln):
        blocks.append(("fig", ln))
    elif re.match(r"^图\s*\d", ln):
        blocks.append(("cap", ln))
    elif re.match(r"^注[：:]", ln):
        blocks.append(("note", ln))
    elif re.match(r"^\[\d+\]", ln):
        blocks.append(("ref", ln))
    elif ln.startswith("摘要："):
        blocks.append(("abs", ln))
    elif ln.startswith("关键词："):
        blocks.append(("kw", ln))
    else:
        blocks.append(("body", ln))
    i += 1

for k, v in blocks:
    if k in ("title", "h1", "h2"):
        print("BLOCK", k, len(v), v)

# ---------- cover base ----------
doc = Document(COVER)
body = doc.element.body
sectPr = body.find(qn("w:sectPr"))
children = list(body)
for ch in children[25:]:
    if ch is not sectPr:
        body.remove(ch)

cover_sect = copy.deepcopy(sectPr)
fr = cover_sect.find(qn("w:footerReference"))
if fr is not None:
    cover_sect.remove(fr)
brk = parse_xml('<w:p %s><w:pPr><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>%s</w:pPr></w:p>'
                % (nsdecls("w"), re.sub(r'\sxmlns(:\w+)?="[^"]*"', '', cover_sect.xml)))
body.insert(len(body) - 1, brk)

def para_text(el):
    return "".join(t.text or "" for t in el.iter(qn("w:t")))
def is_blank_para(el):
    return (el.tag == qn("w:p") and not para_text(el).strip()
            and el.find(".//" + qn("w:drawing")) is None
            and el.find(".//" + qn("w:pict")) is None)

ps = [el for el in body if el.tag == qn("w:p")]
idx_course = next(i for i, el in enumerate(ps) if para_text(el).strip() == "本科课程论文")
for step in range(2):
    if is_blank_para(ps[idx_course - 1 - step]):
        body.remove(ps[idx_course - 1 - step])
ps2 = [el for el in body if el.tag == qn("w:p")]
ic = next(i for i, el in enumerate(ps2) if para_text(el).strip() == "本科课程论文")
it = next(i for i, el in enumerate(ps2) if para_text(el).strip().startswith("题"))
mids = [x for x in ps2[ic + 1:it] if is_blank_para(x)]
KEEP = 1   # 与六-1/六-2 成稿一致：本科课程论文与「题　目」之间保留一个空行
for el in mids[KEEP:]:
    body.remove(el)
print("本科课程论文→题目 空行保留:", KEEP, "删除:", max(0, len(mids) - KEEP))
ips = [el for el in body if el.tag == qn("w:p")]
i_tea = next(i for i, el in enumerate(ips) if para_text(el).strip().startswith("任课教师"))
i_date = next(i for i, el in enumerate(ips) if para_text(el).strip().startswith("日"))
for el in ips[i_tea + 1:i_date]:
    if is_blank_para(el): body.remove(el)
ips2 = [el for el in body if el.tag == qn("w:p")]
i_date2 = next(i for i, el in enumerate(ips2) if para_text(el).strip().startswith("日"))
if i_date2 + 1 < len(ips2) and is_blank_para(ips2[i_date2 + 1]):
    body.remove(ips2[i_date2 + 1])

# 「课程名称」 one line, template underline kept
for el in body.iter(qn("w:p")):
    if para_text(el).strip().startswith("课程名称"):
        ppr = el.find(qn("w:pPr"))
        for ch in list(el):
            if ch is not ppr: el.remove(ch)
        RR = rpr("黑体", 28); RU = rpr("黑体", 28, u="single")
        piece = (run("课程名称", RR) + run("    ", RR) + run("现代动物生产行业大讲堂", RU) + run("  ", RU))
        for node in parse_xml("<w:root %s>%s</w:root>" % (nsdecls("w"), piece)):
            el.append(node)
        break

# ---------- cover title ----------
TPPR = ('<w:pStyle w:val="4"/><w:keepNext w:val="0"/><w:keepLines w:val="0"/><w:pageBreakBefore w:val="0"/>'
        '<w:widowControl w:val="0"/><w:tabs><w:tab w:val="left" w:pos="3120"/></w:tabs>'
        '<w:kinsoku/><w:wordWrap/><w:overflowPunct/><w:topLinePunct w:val="0"/><w:autoSpaceDE/>'
        '<w:autoSpaceDN/><w:bidi w:val="0"/><w:adjustRightInd/><w:snapToGrid w:val="0"/>'
        '<w:spacing w:line="360" w:lineRule="auto"/>'
        '<w:ind w:left="3120" w:hanging="1430"/><w:textAlignment w:val="auto"/>')
TITLE_TEXT = [b for b in blocks if b[0] == "title"][0][1]

def set_title(par, text, br_after=None):
    for r in list(par._p):
        if r.tag in (qn("w:r"), qn("w:bookmarkStart"), qn("w:bookmarkEnd")):
            par._p.remove(r)
    ppr = par._p.find(qn("w:pPr"))
    for ch in list(ppr): ppr.remove(ch)
    for node in parse_xml("<w:root %s>%s</w:root>" % (nsdecls("w"), TPPR)):
        ppr.append(node)
    lab = run("题\u3000\u3000目", rpr("黑体", 28))
    tab = "<w:r>" + rpr("黑体", 28) + "<w:tab/></w:r>"
    val = rpr("黑体", 28, u="single")
    if br_after:
        a, b = text.split(br_after, 1)
        valruns = run(a + br_after, val) + brk_run(val) + run(b, val)
    else:
        valruns = run(text, val)
    for xmls in (lab, tab, valruns):
        for node in parse_xml("<w:root %s>%s</w:root>" % (nsdecls("w"), xmls)):
            par._p.append(node)

print("COVER TITLE len:", len(TITLE_TEXT))

# ---------- body ----------
def add(xmlstr):
    el = parse_xml("<w:root %s>%s</w:root>" % (nsdecls("w"), xmlstr))[0]
    body.insert(len(body) - 1, el)
    return el

for kind, val in blocks:
    if kind == "title":
        # 大标题: 断口落在「：」之后（首行主标题、次行副标题各占一行，无孤字）
        tp = rpr("黑体", 32, bold=True)
        if "\uff1a" in val:
            a, b = val.split("\uff1a", 1)
            runs = run(a + "\uff1a", tp) + brk_run(tp) + run(b, tp)
        else:
            runs = run(val, tp)
        add("<w:p><w:pPr>%s</w:pPr>%s</w:p>" % (P_TITLE, runs))
    elif kind == "abs":
        lab, rest = val[:3], val[3:]
        add("<w:p><w:pPr>%s</w:pPr>%s%s</w:p>" % (P_BODY, run(lab, rpr("黑体", 24, bold=True)), run(rest, rpr("宋体", 24))))
    elif kind == "kw":
        lab, rest = val[:4], val[4:]
        add("<w:p><w:pPr>%s</w:pPr>%s%s</w:p>" % (P_BODY, run(lab, rpr("黑体", 24, bold=True)), run(rest, rpr("宋体", 24))))
    elif kind == "h1":
        add("<w:p><w:pPr>%s</w:pPr>%s</w:p>" % (P_H1(), run(val, rpr("黑体", 28, bold=True))))
    elif kind == "refhead":
        add("<w:p><w:pPr>%s</w:pPr>%s</w:p>" % (P_H1(center=True, pagebreak=True), run(val, rpr("黑体", 28, bold=True))))
    elif kind == "h2":
        add("<w:p><w:pPr>%s</w:pPr>%s</w:p>" % (P_H2, run(val, rpr("黑体", 24, bold=True))))
    elif kind == "cap":
        m = re.match(r"^(图\s*\d+)\s*(.+)$", val)
        capt = m.group(1) + "\u3000\u3000" + m.group(2)
        add("<w:p><w:pPr>%s</w:pPr>%s</w:p>" % (P_CAP, run(capt, rpr("宋体", 21, bold=True))))
    elif kind == "note":
        add("<w:p><w:pPr>%s</w:pPr>%s</w:p>" % (P_CAP, run(val, rpr("宋体", 21))))
    elif kind == "ref":
        add("<w:p><w:pPr>%s</w:pPr>%s</w:p>" % (P_REF, run(val, rpr("宋体", 21))))
    elif kind == "fig":
        pel = add("<w:p><w:pPr>%s</w:pPr></w:p>" % P_FIG)
        par = Paragraph(pel, doc._body)
        par.add_run().add_picture(FIG, width=Cm(14.5))
    else:
        add("<w:p><w:pPr>%s</w:pPr>%s</w:p>" % (P_BODY, run(val, rpr("宋体", 24))))

# ---------- cover title ----------
title_par = None
for q in doc.paragraphs:
    if q.text.strip().startswith("题"):
        title_par = q; break
set_title(title_par, TITLE_TEXT, br_after=None)

# ---------- body footer ----------
secs = doc.sections
print("sections:", len(secs))
fsec = secs[1]
ftr = fsec.footer
ftr.is_linked_to_previous = False
froot = ftr._element
for ch in list(froot): froot.remove(ch)
FP = '<w:pPr><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="center"/></w:pPr>'
RP = ('<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="宋体"/>'
      '<w:sz w:val="21"/><w:szCs w:val="21"/></w:rPr>')
fxml = ('<w:p %s>%s<w:r>%s<w:fldChar w:fldCharType="begin"/></w:r>'
        '<w:r>%s<w:instrText xml:space="preserve"> PAGE  \\* MERGEFORMAT </w:instrText></w:r>'
        '<w:r>%s<w:fldChar w:fldCharType="separate"/></w:r>'
        '<w:r>%s<w:t>1</w:t></w:r>'
        '<w:r>%s<w:fldChar w:fldCharType="end"/></w:r></w:p>' % (nsdecls("w"), FP, RP, RP, RP, RP, RP))
froot.append(parse_xml(fxml))

doc.save(OUT)
print("saved", OUT)
