# -*- coding: utf-8 -*-
"""Set docx core properties (author/title/dates) without touching anything else."""
import os, re, sys, zipfile, shutil, datetime

ROOT = r"C:\Users\Administrator\Desktop\丙酮酰化"
AUTHOR = "朱承浩"
TARGETS = [
    ("六-1_宠物主粮的价格带与品类结构（成稿）.docx", "宠物主粮的价格带与品类结构——基于主流电商平台销量榜的抽样设计与结构分析"),
    ("六-2_宠物食品网络投诉的类型分布与处理结果（成稿）.docx", "宠物食品网络投诉的类型分布与处理结果——基于公开投诉记录与通报数据的编码框架分析"),
    ("七-6_宠物活体运输福利问题（统一结构成稿）.docx", "宠物活体运输福利问题——被制度与舆论忽略的“活体电商”"),
]
APPLY = "--apply" in sys.argv
now = datetime.datetime.now().astimezone()
stamp = now.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def set_tag(xml, tag, value):
    pat = r"<%s[^>]*>[^<]*</%s>" % (tag, tag)
    if re.search(pat, xml):
        return re.sub(r"(<%s[^>]*>)[^<]*(</%s>)" % (tag, tag), lambda m: m.group(1) + value + m.group(2), xml)
    # not present: insert before the closing root element
    ins = "<%s>%s</%s>" % (tag, value, tag)
    return re.sub(r"(</cp:coreProperties>)", lambda m: ins + m.group(1), xml)

for fname, title in TARGETS:
    path = os.path.join(ROOT, fname)
    if not os.path.exists(path):
        print("MISSING:", fname); continue
    with zipfile.ZipFile(path) as z:
        core = z.read("docProps/core.xml").decode("utf-8")
        names = z.namelist()
    new = core
    new = set_tag(new, "dc:creator", AUTHOR)
    new = set_tag(new, "cp:lastModifiedBy", AUTHOR)
    new = set_tag(new, "dc:title", title)
    new = set_tag(new, "dcterms:created", stamp) if "<dcterms:created" not in new else set_tag(new, "dcterms:created", stamp)
    new = set_tag(new, "dcterms:modified", stamp)
    print("FILE:", fname)
    for tag in ("dc:creator", "cp:lastModifiedBy", "dc:title", "dcterms:created", "dcterms:modified"):
        m = re.search(r"<%s[^>]*>([^<]*)</%s>" % (tag, tag), core)
        m2 = re.search(r"<%s[^>]*>([^<]*)</%s>" % (tag, tag), new)
        print("   %-18s %r -> %r" % (tag, m.group(1) if m else None, m2.group(1) if m2 else None))
    if APPLY:
        tmp = path + ".tmp"
        with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "docProps/core.xml":
                    data = new.encode("utf-8")
                zout.writestr(item, data)
        shutil.move(tmp, path)
        print("   APPLIED")