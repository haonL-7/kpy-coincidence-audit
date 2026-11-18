
# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding="utf-8")
from docx import Document
from docx.oxml.ns import qn

DRAFT = r"C:\Users\Administrator\Desktop\丙酮酰化\决策蒸馏_改稿\draft_final.md"
OUT = r"C:\Users\Administrator\Desktop\丙酮酰化\决策蒸馏与组织学习（成稿）.docx"

def norm(t):
    return re.sub(r"[\s\u3000\u200b\u2060\u00a0]+", "", t)

lines = [l.rstrip("\n") for l in open(DRAFT, encoding="utf-8").read().split("\n")]
md = []
for ln in (l.strip() for l in lines):
    if not ln: continue
    if ln.startswith("# "): md.append(("title", ln[2:].strip()))
    elif ln.startswith("### "): md.append(("h2", ln[4:].strip()))
    elif ln.startswith("## "):
        t = ln[3:].strip()
        if t == "参考文献": md.append(("refhead", t))
        else: md.append(("h1", t))
    elif re.match(r"^!\[", ln): md.append(("fig", ln))
    elif re.match(r"^图\s*\d", ln): md.append(("cap", ln))
    elif ln.startswith("摘要："): md.append(("abs", ln))
    elif ln.startswith("关键词："): md.append(("kw", ln))
    elif re.match(r"^\[\d+\]", ln): md.append(("ref", ln))
    else: md.append(("body", ln))

d = Document(OUT)
paras = d.paragraphs
def txt(el): return "".join(t.text or "" for t in el.iter(qn("w:t")))
# body paragraphs = after the section-break paragraph (first one carrying w:sectPr in pPr)
start = 0
for i, p in enumerate(paras):
    ppr = p._p.find(qn("w:pPr"))
    if ppr is not None and ppr.find(qn("w:sectPr")) is not None:
        start = i + 1
        break
body = paras[start:]
doc = []
for p in body:
    if p._p.find(".//" + qn("w:drawing")) is not None:
        doc.append(("fig", "")); continue
    doc.append(("para", txt(p._p)))

print("md 块数 =", len(md), " docx 正文段数 =", len(doc))
print("md 类型统计:")
from collections import Counter
print("  ", Counter(k for k, _ in md))
print("docx:", Counter(k for k, _ in doc))
bad = 0
j = 0
for k, v in md:
    if k == "fig":
        if doc[j][0] != "fig":
            print("  位置不一致 @%d: md=fig  docx=%r" % (j, doc[j][1][:20])); bad += 1
        j += 1; continue
    if j >= len(doc):
        print("  docx 提前结束 @", j); bad += 1; break
    if norm(doc[j][1]) != norm(v):
        bad += 1
        print("  不一致 #%d [%s]" % (j, k))
        print("    md  :", v[:120])
        print("    docx:", doc[j][1][:120])
        # char-level first difference
        a, b = norm(v), norm(doc[j][1])
        for t in range(min(len(a), len(b))):
            if a[t] != b[t]:
                print("    首个差异 @%d: md=%r docx=%r 上下文 md=%r docx=%r" % (t, a[t], b[t], a[max(0,t-12):t+12], b[max(0,t-12):t+12]))
                break
        else:
            print("    长度不同 md=%d docx=%d 尾部 md=%r docx=%r" % (len(a), len(b), a[-25:], b[-25:]))
    j += 1
print("比对完成: 不一致项 =", bad, " 未比对多余段 =", len(doc) - j)
