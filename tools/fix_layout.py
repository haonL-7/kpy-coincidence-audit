"""Apply the two Word layout properties the builder does not set.

Headings that are bold-only and short get keep-with-next, so a section title
cannot be stranded at the foot of a page. Every table gets a repeating header
row, so a long table shows its column names again after a page break.
"""
import sys, os
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

path = sys.argv[1]
doc = Document(path)

headings = 0
for p in doc.paragraphs:
    txt = p.text.strip()
    if not txt or len(txt) > 80:
        continue
    runs = [r for r in p.runs if r.text.strip()]
    if runs and all(r.bold for r in runs):
        p.paragraph_format.keep_with_next = True
        headings += 1

headers = 0
for t in doc.tables:
    if not t.rows:
        continue
    tr = t.rows[0]._tr
    trPr = tr.get_or_add_trPr()
    if trPr.find(qn('w:tblHeader')) is None:
        el = OxmlElement('w:tblHeader')
        el.set(qn('w:val'), 'true')
        trPr.append(el)
        headers += 1

doc.save(path)
print('keep-with-next headings:', headings, '| repeating header rows:', headers)