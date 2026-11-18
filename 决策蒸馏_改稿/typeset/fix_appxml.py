
# -*- coding: utf-8 -*-
import sys, os, re, shutil, zipfile
sys.stdout.reconfigure(encoding="utf-8")
src = r"C:\Users\Administrator\Desktop\丙酮酰化\决策蒸馏与组织学习（成稿）.docx"
PAGES = int(sys.argv[1]) if len(sys.argv) > 1 else 12
bak = src + ".bak"; shutil.copyfile(src, bak)
zin = zipfile.ZipFile(bak)
items = [(i, zin.read(i.filename)) for i in zin.infolist()]
zin.close()
tmp = src + ".tmp"
zout = zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED)
for info, data in items:
    if info.filename == "docProps/app.xml":
        txt = data.decode("utf-8")
        txt = re.sub(r"<Pages>\d+</Pages>", "<Pages>%d</Pages>" % PAGES, txt)
        data = txt.encode("utf-8")
    zout.writestr(info, data)
zout.close()
os.replace(tmp, src)
c = zipfile.ZipFile(src).read("docProps/app.xml").decode("utf-8")
print("app.xml Pages ->", PAGES, "| 校验:", re.search(r"<Pages>\d+</Pages>", c).group(0))
from docx import Document
dd = Document(src)
print("reopen ok: paragraphs=%d tables=%d sections=%d" % (len(dd.paragraphs), len(dd.tables), len(dd.sections)))
os.remove(bak)
