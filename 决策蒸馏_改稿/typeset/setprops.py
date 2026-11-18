
# -*- coding: utf-8 -*-
import sys, datetime
sys.stdout.reconfigure(encoding="utf-8")
from docx import Document
OUT = r"C:\Users\Administrator\Desktop\丙酮酰化\决策蒸馏与组织学习（成稿）.docx"
TITLE = "决策蒸馏与组织学习：宏集智能体在养殖场成本管控中的作用机制与边界条件"
now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None, microsecond=0)
d = Document(OUT)
cp = d.core_properties
cp.author = "朱承浩"; cp.last_modified_by = "朱承浩"; cp.title = TITLE
cp.created = now; cp.modified = now; cp.revision = 1
cp.comments = ""; cp.subject = ""; cp.keywords = ""; cp.category = ""
d.save(OUT)
print("props:", cp.author, cp.last_modified_by, cp.title, now.isoformat() + "Z")
