
import sys, os, re
BASE = os.environ.get("KPY_BASE", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from docx import Document

import os
p = os.path.join(BASE, "11_manuscript_JPR.docx")
d = Document(p)
print("paragraphs:", len(d.paragraphs), "images:", len(d.inline_shapes))
print("\n-- outline --")
for par in d.paragraphs:
    t = par.text.strip()
    if not t: continue
    bold_all = all((r.bold for r in par.runs if r.text.strip())) if par.runs else False
    if bold_all and len(t) < 90:
        print("  " + t)
print("\n-- stray markdown --")
bad = [par.text[:80] for par in d.paragraphs if "**" in par.text or re.search(r"(?<!\w)\*(?!\w)", par.text)]
print(bad if bad else "(none)")
words = sum(len(par.text.split()) for par in d.paragraphs)
print("\ntotal words in docx:", words)
print("size:", os.path.getsize(p), "bytes")
