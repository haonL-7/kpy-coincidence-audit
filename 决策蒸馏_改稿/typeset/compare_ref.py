
# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding="utf-8")
from docx import Document
from docx.oxml.ns import qn

def txt(el): return "".join(t.text or "" for t in el.iter(qn("w:t")))
def sig(p):
    ppr = p._p.find(qn("w:pPr"))
    kids = [c.tag.split("}")[1] for c in ppr] if ppr is not None else []
    ind = ppr.find(qn("w:ind")) if ppr is not None else None
    sp = ppr.find(qn("w:spacing")) if ppr is not None else None
    r = p.runs[0] if p.runs else None
    rp = r._r.find(qn("w:rPr")) if r is not None else None
    rf = rp.find(qn("w:rFonts")) if rp is not None else None
    sz = rp.find(qn("w:sz")) if rp is not None else None
    return "pPr=%s | ind=%s | spacing=%s | font=%s sz=%s bold=%s" % (
        kids, dict(ind.attrib) if ind is not None else None,
        dict(sp.attrib) if sp is not None else None,
        rf.get(qn("w:eastAsia")) if rf is not None else None,
        sz.get(qn("w:val")) if sz is not None else None,
        p.runs[0].font.bold if p.runs else None)

def pick(d, pred):
    for p in d.paragraphs:
        if pred(p): return p
    return None

docs = [("本稿", r"C:\Users\Administrator\Desktop\丙酮酰化\决策蒸馏与组织学习（成稿）.docx"),
        ("六-1", r"C:\Users\Administrator\Desktop\丙酮酰化\六-1_宠物主粮的价格带与品类结构（成稿）.docx")]
for label, path in docs:
    d = Document(path)
    print("==========", label)
    print(" 页面/边距:", "%.2fx%.2f cm 上%.2f 下%.2f 左%.2f 右%.2f" % (
        d.sections[-1].page_width.cm, d.sections[-1].page_height.cm,
        d.sections[-1].top_margin.cm, d.sections[-1].bottom_margin.cm,
        d.sections[-1].left_margin.cm, d.sections[-1].right_margin.cm),
        "| 节数", len(d.sections))
    def lvl(p):
        ppr = p._p.find(qn("w:pPr"))
        if ppr is None: return None
        ol = ppr.find(qn("w:outlineLvl"))
        return ol.get(qn("w:val")) if ol is not None else None
    targets = [
        ("首行缩进正文", lambda p: p._p.find(qn("w:pPr")) is not None
            and p._p.find(qn("w:pPr")).find(qn("w:ind")) is not None
            and p._p.find(qn("w:pPr")).find(qn("w:ind")).get(qn("w:firstLineChars")) == "200"
            and not txt(p._p).startswith("摘要") and not txt(p._p).startswith("关键词")),
        ("摘要段", lambda p: txt(p._p).startswith("摘要")),
        ("关键词段", lambda p: txt(p._p).startswith("关键词")),
        ("大标题", lambda p: p.runs and p.runs[0].font.size is not None and p.runs[0].font.size.pt == 16.0),
        ("一级标题", lambda p: lvl(p) == "0" and not txt(p._p).startswith("参考文献")),
        ("参考文献标题", lambda p: lvl(p) == "0" and txt(p._p).startswith("参考文献")),
        ("二级/三级小节", lambda p: lvl(p) == "1"),
        ("参考文献条目", lambda p: re.match(r"^\[\d+\]", txt(p._p)) is not None),

    ]
    for nm, pred in targets:
        p = pick(d, pred)
        if p is None:
            print(" %-8s (无)" % nm); continue
        print(" %-8s %-28s %s" % (nm, txt(p._p)[:26], sig(p)))
    # caption
    cap = None
    for i, p in enumerate(d.paragraphs):
        if txt(p._p).startswith("图1") and i and d.paragraphs[i-1]._p.find(".//" + qn("w:drawing")) is not None:
            cap = p; break
    if cap is not None:
        print(" %-8s %-28s %s" % ("图题", txt(cap._p)[:26], sig(cap)))
    print(" 文档属性:", d.core_properties.author, "/", d.core_properties.last_modified_by, "/", (d.core_properties.title or "")[:30])
