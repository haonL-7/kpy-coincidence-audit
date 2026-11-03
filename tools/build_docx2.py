
import sys, os, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE = r"C:\Users\Administrator\Desktop\丙酮酰化"
md_path, out_path = sys.argv[1], sys.argv[2]
header_lines = sys.argv[3].split("|") if len(sys.argv) > 3 else []

FIG = {
  "1": "figs/Fig1_reference_sets.png",
  "2": "figs/Fig2_density_and_crossmod.png",
  "3": "figs/Fig4_protocol.png",
  "S1": "figs/FigS1_structure.png",
  "S2": "figs/FigS2_curation.png",
}

md = open(md_path, encoding="utf-8").read().split("\n")
doc = Document()
s = doc.sections[0]
s.top_margin = s.bottom_margin = Inches(1); s.left_margin = s.right_margin = Inches(1)
n = doc.styles["Normal"]; n.font.name = "Times New Roman"; n.font.size = Pt(12)
n.paragraph_format.line_spacing = 2.0; n.paragraph_format.space_after = Pt(0)

def add_runs(p, text):
    for part in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", text):
        if not part: continue
        if part.startswith("**") and part.endswith("**"):
            r = p.add_run(part[2:-2]); r.bold = True
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            r = p.add_run(part[1:-1]); r.italic = True
        else:
            p.add_run(part)

ti = next(i for i, l in enumerate(md) if l.strip() == "## Title")
title = next(l.strip() for l in md[ti+1:] if l.strip())
p = doc.add_paragraph(); r = p.add_run(title); r.bold = True; r.font.size = Pt(15)
p.paragraph_format.line_spacing = 1.15; p.paragraph_format.space_after = Pt(6)
for line in header_lines:
    q = doc.add_paragraph(line); q.paragraph_format.line_spacing = 1.15
doc.add_paragraph()

rows = []
def flush_table():
    global rows
    if not rows: return
    ncol = len(rows[0])
    tbl = doc.add_table(rows=0, cols=ncol)
    tbl.style = "Table Grid"
    for ri, cells in enumerate(rows):
        cells = (cells + [""]*ncol)[:ncol]
        cells = [c.replace("**","").strip() for c in cells]
        row = tbl.add_row().cells
        for ci, txt in enumerate(cells[:ncol]):
            row[ci].text = ""
            par = row[ci].paragraphs[0]
            r = par.add_run(txt); r.font.size = Pt(8); r.font.name = "Times New Roman"
            if ri == 0: r.bold = True
            par.paragraph_format.line_spacing = 1.0
    rows = []

for line in md:
    t = line.rstrip()
    if t.strip().startswith("|"):
        cells = [c for c in t.strip().strip("|").split("|")]
        rows.append(cells)
        continue
    else:
        flush_table()
    if not t.strip() or t.startswith(">") or t.strip() == "## Title": continue
    if t.startswith("## "):
        h = doc.add_paragraph(); r = h.add_run(t[3:].strip()); r.bold = True
        r.font.name = "Times New Roman"; r.font.size = Pt(13)
        h.paragraph_format.space_before = Pt(12); h.paragraph_format.space_after = Pt(6)
        h.paragraph_format.line_spacing = 1.0
        continue
    if t.startswith("### "):
        h = doc.add_paragraph(); r = h.add_run(t[4:].strip()); r.bold = True
        r.font.name = "Times New Roman"; r.font.size = Pt(12)
        h.paragraph_format.space_before = Pt(10); h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.line_spacing = 1.0
        continue
    par = doc.add_paragraph(); add_runs(par, t.strip())

flush_table()

# figures after their legends
for par in list(doc.paragraphs):
    m = re.match(r"^(?:Supplementary )?Figure (S?\d+)\.", par.text.strip())
    if not m: continue
    key = m.group(1)
    f = os.path.join(BASE, FIG.get(key, ""))
    if not os.path.exists(f): continue
    newp = par.insert_paragraph_before("")
    newp.add_run().add_picture(f, width=Inches(6.3))
    par._p.addnext(newp._p)
    newp.alignment = WD_ALIGN_PARAGRAPH.CENTER

sectPr = doc.sections[0]._sectPr
ln = OxmlElement("w:lnNumType"); ln.set(qn("w:countBy"), "1"); ln.set(qn("w:restart"), "continuous")
sectPr.append(ln)
fp = doc.sections[0].footer.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
fld = OxmlElement("w:fldSimple"); fld.set(qn("w:instr"), "PAGE")
rr = OxmlElement("w:r"); tt = OxmlElement("w:t"); tt.text = "1"; rr.append(tt); fld.append(rr); fp._p.append(fld)

doc.save(out_path)
d2 = Document(out_path)
print("  paragraphs:", len(d2.paragraphs), "| images:", len(d2.inline_shapes), "| size:", os.path.getsize(out_path))
