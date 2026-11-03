
import sys, re, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

BASE = r"C:\Users\Administrator\Desktop\丙酮酰化"
src = open(os.path.join(BASE, "12_cover_letter_JPR.md"), encoding="utf-8").read()
body = src.split("\n---\n")[1]          # drop the status header
body = body.split("\n## What changed")[0]  # drop the internal rationale
paras = [p.strip() for p in body.split("\n\n") if p.strip()]

doc = Document()
s = doc.sections[0]
s.top_margin = s.bottom_margin = Inches(1); s.left_margin = s.right_margin = Inches(1)
n = doc.styles["Normal"]; n.font.name = "Times New Roman"; n.font.size = Pt(12)
n.paragraph_format.line_spacing = 1.15; n.paragraph_format.space_after = Pt(8)

def add(p, text):
    for part in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", text):
        if not part: continue
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            r = p.add_run(part[2:-2]); r.bold = True
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            r = p.add_run(part[1:-1]); r.italic = True
        else:
            r = p.add_run(part)

for i, block in enumerate(paras):
    lines = [l for l in block.split("\n") if l.strip()]
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    for j, line in enumerate(lines):
        if j: p.add_run().add_break()
        add(p, line)
    p.paragraph_format.space_after = Pt(8)

out = os.path.join(BASE, "12_cover_letter_JPR.docx")
doc.save(out)
d2 = Document(out)
txt = "\n".join(p.text for p in d2.paragraphs)
print("paragraphs:", len(d2.paragraphs), "| size:", os.path.getsize(out))
print("leaked internal text:", ("What changed" in txt) or ("Status:" in txt))
print("first:", d2.paragraphs[0].text[:60])
print("last:", d2.paragraphs[-1].text[:80])
