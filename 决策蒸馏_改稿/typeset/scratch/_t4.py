
from docx import Document
from docx.oxml.ns import qn
import zipfile, os
COVER = r"C:\\Users\\Administrator\\Documents\\xwechat_files\\wxid_h72ol1ylw9hv22_d04f\\msg\\file\\2026-11\\五-11_本轮生猪产能调控政策的成效评估与养殖场经营风险分.docx"
print("exists", os.path.exists(COVER))
z = zipfile.ZipFile(COVER)
print("parts:", [n for n in z.namelist()])
doc = Document(COVER)
body = doc.element.body
ch = list(body)
print("body children:", len(ch))
for i, el in enumerate(ch):
    tag = el.tag.split('}')[1]
    txt = "".join(t.text or "" for t in el.iter(qn("w:t")))
    extra = ""
    if el.find(".//"+qn("w:drawing")) is not None: extra += " [DRAWING]"
    if el.find(".//"+qn("w:tbl")) is not None and tag=="tbl": extra += " [TABLE]"
    print(i, tag, repr(txt[:60]), extra)
print("sections:", len(doc.sections))
for s in doc.sections:
    print(" sec", s.page_width.cm if s.page_width else None, s.page_height.cm if s.page_height else None,
          s.top_margin.cm, s.bottom_margin.cm, s.left_margin.cm, s.right_margin.cm,
          s.footer.is_linked_to_previous, s.header.is_linked_to_previous)
print("--- sectPr xml ---")
sect = body.find(qn("w:sectPr"))
import re
print(sect.xml[:3000])
