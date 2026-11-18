
import sys
sys.stdout.reconfigure(encoding="utf-8")
from docx import Document
from docx.oxml.ns import qn
d = Document(r"C:\Users\Administrator\Desktop\丙酮酰化\决策蒸馏与组织学习（成稿）.docx")
def txt(el): return "".join(t.text or "" for t in el.iter(qn("w:t")))
for i,p in enumerate(d.paragraphs):
    t = txt(p._p)
    if t.startswith("摘要") or t.startswith("关键词"):
        print(i, repr(t[:20]), "runs:", len(p.runs), "children:", [c.tag.split('}')[1] for c in p._p])
        print(p._p.xml[:1200])
