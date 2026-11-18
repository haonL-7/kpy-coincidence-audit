#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""把 manuscript.md 按中文课程论文格式装进原 docx 模板。

用法： python build_docx.py <input.md> <output.docx>

设计要点：
  * 模板只读打开，保留 body 子元素 0..26（封面 + 评分表 + 空段），
    删除其后、sectPr 之前的所有 w:p，再把新正文插到 sectPr 之前。
  * 所有格式显式写进 pPr / rPr，不依赖模板样式继承。
  * sectPr（页边距、纸型、页眉页脚）一个字节都不改。
"""
import os
import re
import sys
import zipfile

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH as ALIGN
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Pt

TEMPLATE = ("C:/Users/Administrator/Documents/xwechat_files/"
            "wxid_h72ol1ylw9hv22_d04f/msg/file/2026-11/"
            "七-6_宠物活体运输的福利问题——被制度与舆论忽略的活体.docx")

SONG = "宋体"
HEI = "黑体"
LATIN = "Times New Roman"
REF_TITLE = "参考文献"

# 模板 body 子元素 0..26 原样保留；27 起是旧正文（提纲）
KEEP_THROUGH = 26

MARKER = re.compile(r"^#(TITLE|ABSTRACT|KEYWORDS|H1|H2|P|REF|TABLE|TR)\b[ \t:：]*(.*)$")

# kind -> (中文字体, 字号pt, 加粗, 对齐, 段前pt, 段后pt, 行距倍数, 首行缩进字符, 左缩进字符)
STYLE = {
    "TITLE":    (HEI,  16.0, True,  ALIGN.CENTER,  12, 12, 1.5, None, None),
    "ABSTRACT": (SONG, 10.5, False, ALIGN.JUSTIFY,  0,  0, 1.5,    2, None),
    "KEYWORDS": (SONG, 10.5, False, ALIGN.JUSTIFY,  0,  0, 1.5,    2, None),
    "H1":       (HEI,  14.0, True,  ALIGN.LEFT,    12,  6, 1.5, None, None),
    "H2":       (HEI,  12.0, True,  ALIGN.LEFT,     6,  3, 1.5, None, None),
    "P":        (SONG, 12.0, False, ALIGN.JUSTIFY,  0,  0, 1.5,    2, None),
    "REF":      (SONG, 10.5, False, ALIGN.LEFT,     0,  0, 1.5,   -2,    2),
    "CAP":      (SONG, 10.5, True,  ALIGN.CENTER,   6,  3, 1.5, None, None),
}

# 三线表参数（w:sz 以 1/8pt 计：12=1.5pt，6=0.75pt；twips：340≈0.6cm，28≈0.05cm）
TBL_RULE_SZ = "12"
TBL_HEAD_RULE_SZ = "6"
TBL_ROW_MIN = 340
TBL_CELL_MARGIN = 28

P_PPR_SUCCESSORS = ("w:spacing", "w:ind", "w:contextualSpacing", "w:mirrorIndents",
                    "w:suppressOverlap", "w:jc", "w:textDirection", "w:textAlignment",
                    "w:textboxTightWrap", "w:outlineLvl", "w:divId", "w:cnfStyle",
                    "w:rPr", "w:sectPr", "w:pPrChange")


# ---------------------------------------------------------------- md 解析
def parse_md(path):
    """返回 [(kind, text)]；无标记的行接在当前段之后（软换行折叠）。"""
    items = []
    cur = None
    with open(path, encoding="utf-8-sig") as fh:
        for raw in fh:
            line = raw.rstrip("\r\n")
            s = line.strip()
            if not s:
                cur = None
                continue
            m = MARKER.match(s)
            if m:
                cur = [m.group(1), m.group(2).strip()]
                items.append(cur)
            elif cur is None:
                raise SystemExit("manuscript 第 %r 行缺少 #TITLE/#P 等标记" % s[:40])
            elif cur[1] and cur[1][-1].isascii() and cur[1][-1].isalnum() \
                    and s[0].isascii() and s[0].isalnum():
                cur[1] = cur[1] + " " + s
            else:
                cur[1] = cur[1] + s
    return items


def group_tables(items):
    """把 #TABLE + 紧跟的 #TR 折叠成 ("TABLE", (题注, 行列表))，其余原样返回。"""
    out, i = [], 0
    while i < len(items):
        kind, text = items[i]
        if kind == "TABLE":
            rows, i = [], i + 1
            while i < len(items) and items[i][0] == "TR":
                rows.append([c.strip() for c in items[i][1].split("|")])
                i += 1
            if not rows:
                raise SystemExit("#TABLE %r 之后没有任何 #TR 数据行，拒绝产出空表" % text[:30])
            for r in rows[1:]:
                if len(r) != len(rows[0]):
                    sys.stderr.write("警告：#TR 列数 %d 与表头 %d 不符，按表头裁齐：%s\n"
                                     % (len(r), len(rows[0]), " | ".join(r)[:40]))
            out.append(("TABLE", (text, rows)))
        elif kind == "TR":
            raise SystemExit("#TR 前面缺少 #TABLE 表题行")
        else:
            out.append((kind, text))
            i += 1
    return out


def split_label(text, label):
    """把 '摘要：xxx' 拆成 ('摘要：', 'xxx')；md 里没写标签时补上。"""
    for sep in ("：", ":", " "):
        head = label + sep
        if text.startswith(head):
            return head, text[len(head):]
    return label + "：", text


# ---------------------------------------------------------------- 格式写入
def twips(points):
    """磅 -> twips（1pt = 20twips）。"""
    return int(round(points * 20))


def set_run_font(run, east_asia, size_pt, bold):
    """中文字体写 eastAsia，西文写 ascii/hAnsi，两者都显式落 XML。"""
    run.font.name = LATIN
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    rpr = run._element.get_or_add_rPr()
    rf = rpr.get_or_add_rFonts()
    rf.set(qn("w:ascii"), LATIN)
    rf.set(qn("w:hAnsi"), LATIN)
    rf.set(qn("w:cs"), LATIN)
    rf.set(qn("w:eastAsia"), east_asia)


def snap_to_grid_off(pPr):
    """模板 sectPr 有 docGrid linePitch=312，关掉段落的网格吸附，1.5 倍行距才按倍数生效。"""
    el = pPr.find(qn("w:snapToGrid"))
    if el is None:
        el = OxmlElement("w:snapToGrid")
        pPr.insert_element_before(el, *P_PPR_SUCCESSORS)
    el.set(qn("w:val"), "0")


def add_para(doc, sect, text, kind, align=None, label=None):
    east, size, bold, al, before, after, line, first_chars, left_chars = STYLE[kind]
    p = doc.add_paragraph()
    sect.addprevious(p._p)          # 永远插在 sectPr 之前
    p.style = doc.styles["Normal"]

    pf = p.paragraph_format
    pf.alignment = align if align is not None else al
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line
    pf.left_indent = Pt(size * (left_chars or 0))
    pf.first_line_indent = Pt(size * (first_chars or 0))

    pPr = p._p.get_or_add_pPr()
    ind = pPr.find(qn("w:ind"))
    if ind is not None:
        # python-docx 会把负的首行缩进改写成 w:hanging，这里统一还原成
        # w:left / w:firstLine（负值即悬挂缩进），并显式补字符单位。
        for bad in ("w:hanging", "w:hangingChars"):
            if ind.get(qn(bad)) is not None:
                del ind.attrib[qn(bad)]
        ind.set(qn("w:left"), str(twips(size * (left_chars or 0))))
        ind.set(qn("w:firstLine"), str(twips(size * (first_chars or 0))))
        if first_chars:
            ind.set(qn("w:firstLineChars"), str(int(round(first_chars * 100))))
        if left_chars:
            ind.set(qn("w:leftChars"), str(int(round(left_chars * 100))))
    snap_to_grid_off(pPr)

    if label:                       # 摘要 / 关键词：标签用黑体加粗
        head, rest = label
        set_run_font(p.add_run(head), HEI, size, True)
        if rest:
            set_run_font(p.add_run(rest), east, size, bold)
    else:
        set_run_font(p.add_run(text), east, size, bold)
    return p


# ---------------------------------------------------------------- 三线表
TCPR_AFTER_BORDERS = ("w:shd", "w:noWrap", "w:tcMar", "w:textDirection",
                      "w:tcFitText", "w:vAlign", "w:hideMark", "w:headers",
                      "w:cellIns", "w:cellDel", "w:cellMerge", "w:tcPrChange")


def fill_cell(cell, text, head):
    """单元格段落：显式清零缩进（否则会继承正文的首行缩进 2 字符）。"""
    p = cell.paragraphs[0]
    pf = p.paragraph_format
    pf.alignment = ALIGN.CENTER if head else ALIGN.LEFT
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = 1.0
    pf.left_indent = Pt(0)
    pf.first_line_indent = Pt(0)

    pPr = p._p.get_or_add_pPr()
    ind = pPr.find(qn("w:ind"))
    if ind is not None:
        for bad in ("w:firstLineChars", "w:leftChars", "w:hanging", "w:hangingChars"):
            if ind.get(qn(bad)) is not None:
                del ind.attrib[qn(bad)]
        ind.set(qn("w:left"), "0")
        ind.set(qn("w:firstLine"), "0")
    snap_to_grid_off(pPr)
    set_run_font(p.add_run(text), HEI if head else SONG, 10.5, head)


def add_table(doc, sect, rows):
    """rows[0] 为表头，列数以表头为准；三线表只留顶线/表头下横线/底线。"""
    ncol = len(rows[0])
    table = doc.add_table(rows=len(rows), cols=ncol)
    sect.addprevious(table._tbl)
    tbl = table._tbl

    new_tblPr = parse_xml(
        '<w:tblPr %s>'
        '<w:tblW w:type="pct" w:w="5000"/>'
        '<w:jc w:val="center"/>'
        '<w:tblBorders>'
        '<w:top w:val="single" w:sz="%s" w:space="0" w:color="000000"/>'
        '<w:left w:val="nil"/>'
        '<w:bottom w:val="single" w:sz="%s" w:space="0" w:color="000000"/>'
        '<w:right w:val="nil"/>'
        '<w:insideH w:val="nil"/>'
        '<w:insideV w:val="nil"/>'
        '</w:tblBorders>'
        '<w:tblLayout w:type="autofit"/>'
        '<w:tblCellMar>'
        '<w:top w:w="%d" w:type="dxa"/>'
        '<w:left w:w="108" w:type="dxa"/>'
        '<w:bottom w:w="%d" w:type="dxa"/>'
        '<w:right w:w="108" w:type="dxa"/>'
        '</w:tblCellMar>'
        '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="0"'
        ' w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>'
        '</w:tblPr>'
        % (nsdecls("w"), TBL_RULE_SZ, TBL_RULE_SZ, TBL_CELL_MARGIN, TBL_CELL_MARGIN))
    old = tbl.find(qn("w:tblPr"))        # tblPr 必须是 tbl 的第一个子元素
    if old is None:
        tbl.insert(0, new_tblPr)
    else:
        tbl.replace(old, new_tblPr)

    for r_idx, row in enumerate(rows):
        head = r_idx == 0
        trPr = table.rows[r_idx]._tr.get_or_add_trPr()
        trPr.append(parse_xml('<w:trHeight %s w:hRule="atLeast" w:val="%d"/>'
                              % (nsdecls("w"), TBL_ROW_MIN)))
        for c_idx in range(ncol):
            cell = table.cell(r_idx, c_idx)
            fill_cell(cell, row[c_idx] if c_idx < len(row) else "", head)
            if head:                       # 表头下横线：只能落到表头单元格下边框
                tcPr = cell._tc.get_or_add_tcPr()
                tcPr.insert_element_before(parse_xml(
                    '<w:tcBorders %s><w:bottom w:val="single" w:sz="%s"'
                    ' w:space="0" w:color="000000"/></w:tcBorders>'
                    % (nsdecls("w"), TBL_HEAD_RULE_SZ)), *TCPR_AFTER_BORDERS)
    return table


# ---------------------------------------------------------------- 组装
def build(md_path, out_path):
    items = group_tables(parse_md(md_path))
    doc = Document(TEMPLATE)
    body = doc.element.body
    sect = body.find(qn("w:sectPr"))
    if sect is None:
        raise SystemExit("模板缺少 sectPr，落盘中止")

    for i, el in enumerate(list(body)):      # 只删 27 起、sectPr 之前的正文
        if i > KEEP_THROUGH and el is not sect:
            body.remove(el)
    cover_paras = sum(1 for el in list(body)[:KEEP_THROUGH + 1]
                      if el.tag == qn("w:p"))

    manual_ref = any(k == "H1" and t.strip() == REF_TITLE for k, t in items)
    ref_done = False
    for kind, text in items:
        if kind == "TABLE":
            caption, rows = text
            add_para(doc, sect, caption, "CAP")
            add_table(doc, sect, rows)
        elif kind == "REF":
            if not ref_done:
                if not manual_ref:
                    add_para(doc, sect, REF_TITLE, "H1", align=ALIGN.CENTER)
                ref_done = True
            add_para(doc, sect, text, "REF")
        elif kind in ("ABSTRACT", "KEYWORDS"):
            base = "摘要" if kind == "ABSTRACT" else "关键词"
            head, rest = split_label(text, base)
            add_para(doc, sect, text, kind, label=(head, rest))
        else:
            add_para(doc, sect, text, kind)

    prev = sect.getprevious()
    if prev is not None and prev.tag == qn("w:tbl"):
        add_para(doc, sect, "", "P")      # 表格紧跟 sectPr 时 Word 需补一个段落

    parent = os.path.dirname(os.path.abspath(out_path))
    if parent and not os.path.isdir(parent):
        os.makedirs(parent, exist_ok=True)
    doc.save(out_path)               # 已存在则直接覆盖
    return cover_paras


# ---------------------------------------------------------------- 校验
def run_props(run):
    rpr = run._element.find(qn("w:rPr"))
    if rpr is None:
        return None, None, None, False
    rf = rpr.find(qn("w:rFonts"))
    ea = rf.get(qn("w:eastAsia")) if rf is not None else None
    asc = rf.get(qn("w:ascii")) if rf is not None else None
    szel = rpr.find(qn("w:sz"))
    sz = int(szel.get(qn("w:val"))) / 2.0 if szel is not None else None
    bel = rpr.find(qn("w:b"))
    bold = bel is not None and bel.get(qn("w:val")) not in ("0", "false")
    return ea, asc, sz, bold


def measure(p):
    pPr = p._p.find(qn("w:pPr"))
    ea, asc, sz, bold = run_props(p.runs[0])

    def attr(el, name):
        return el.get(qn(name)) if el is not None else None

    sp = pPr.find(qn("w:spacing")) if pPr is not None else None
    ind = pPr.find(qn("w:ind")) if pPr is not None else None
    jc = pPr.find(qn("w:jc")) if pPr is not None else None
    line, rule = attr(sp, "w:line"), attr(sp, "w:lineRule")
    spacing = "%s倍" % (int(line) / 240.0) if line and rule == "auto" else "%s(%s)" % (line, rule)
    return ("eastAsia=%s ascii=%s 字号=%spt 加粗=%s 行距=%s 段前=%s 段后=%s "
            "首行=%stwips 首行字符=%s 左缩进=%stwips 左字符=%s 对齐=%s"
            % (ea, asc, sz, bold, spacing,
               attr(sp, "w:before"), attr(sp, "w:after"),
               attr(ind, "w:firstLine"), attr(ind, "w:firstLineChars"),
               attr(ind, "w:left"), attr(ind, "w:leftChars"), attr(jc, "w:val")))


def classify(p):
    """按段落级缩进 + run 字体反推段落类型（摘要段首个 run 是黑体标签，故看最大字号）。"""
    pPr = p._p.find(qn("w:pPr"))
    ind = pPr.find(qn("w:ind")) if pPr is not None else None
    flc = ind.get(qn("w:firstLineChars")) if ind is not None else None
    fonts = [run_props(r) for r in p.runs]
    ea, _asc, sz, bold = fonts[0] if fonts else (None, None, None, False)
    if flc == "-200":
        return "REF"
    if flc == "200":
        return "ABS" if max(f[2] or 0 for f in fonts) == 10.5 else "P"
    if ea == SONG and sz == 10.5 and bold:
        return "CAP"
    if ea == HEI and bold:
        return {16.0: "TITLE", 14.0: "H1", 12.0: "H2"}.get(sz)
    return None


def _at(el, name):
    return el.get(qn(name)) if el is not None else None


def _jc(p):
    pPr = p._p.find(qn("w:pPr"))
    return _at(pPr.find(qn("w:jc")) if pPr is not None else None, "w:val")


def describe_table(tb, idx):
    """打印内容表格的行列、字体、缩进、tblBorders 实测值。"""
    out = ["内容表 %d：%d 行 × %d 列" % (idx, len(tb.rows), len(tb.columns))]
    hp = tb.cell(0, 0).paragraphs[0]
    ea, asc, sz, bold = run_props(hp.runs[0])
    out.append("  表头首格 %r：eastAsia=%s ascii=%s 字号=%spt 加粗=%s 对齐=%s"
               % (tb.cell(0, 0).text, ea, asc, sz, bold, _jc(hp)))

    bp = tb.cell(1, 0).paragraphs[0] if len(tb.rows) > 1 else hp
    ea2, asc2, sz2, bold2 = run_props(bp.runs[0])
    out.append("  表体首格 %r：eastAsia=%s ascii=%s 字号=%spt 加粗=%s 对齐=%s"
               % (tb.cell(1, 0).text if len(tb.rows) > 1 else "", ea2, asc2, sz2, bold2, _jc(bp)))
    pPr = bp._p.find(qn("w:pPr"))
    ind = pPr.find(qn("w:ind")) if pPr is not None else None
    out.append("  表体首格缩进：firstLine=%s left=%s firstLineChars=%s leftChars=%s"
               % (_at(ind, "w:firstLine"), _at(ind, "w:left"),
                  _at(ind, "w:firstLineChars"), _at(ind, "w:leftChars")))

    tblPr = tb._tbl.find(qn("w:tblPr"))
    bd = tblPr.find(qn("w:tblBorders")) if tblPr is not None else None
    parts = []
    for name in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = bd.find(qn("w:" + name)) if bd is not None else None
        if el is None:
            parts.append("%s=缺失" % name)
        elif el.get(qn("w:sz")):
            parts.append("%s=%s %s(%.2fpt)" % (name, el.get(qn("w:val")),
                                               el.get(qn("w:sz")),
                                               int(el.get(qn("w:sz"))) / 8.0))
        else:
            parts.append("%s=%s" % (name, el.get(qn("w:val"))))
    out.append("  tblBorders：" + " | ".join(parts))

    tcp = tb.cell(0, 0)._tc.find(qn("w:tcPr"))
    hb = tcp.find(qn("w:tcBorders")).find(qn("w:bottom")) \
        if tcp is not None and tcp.find(qn("w:tcBorders")) is not None else None
    out.append("  表头下横线：val=%s sz=%s(%.2fpt)"
               % (_at(hb, "w:val"), _at(hb, "w:sz"),
                  int(_at(hb, "w:sz")) / 8.0 if hb is not None else 0.0))

    tw = tblPr.find(qn("w:tblW")) if tblPr is not None else None
    tjc = tblPr.find(qn("w:jc")) if tblPr is not None else None
    out.append("  表宽：type=%s w=%s；表格对齐=%s"
               % (_at(tw, "w:type"), _at(tw, "w:w"), _at(tjc, "w:val")))

    trPr = tb.rows[0]._tr.find(qn("w:trPr"))
    th = trPr.find(qn("w:trHeight")) if trPr is not None else None
    cm = tblPr.find(qn("w:tblCellMar")) if tblPr is not None else None

    def marg(name):
        el = cm.find(qn("w:" + name)) if cm is not None else None
        return _at(el, "w:w")

    hv = _at(th, "w:val")
    out.append("  行高：hRule=%s val=%stwips(%.2fcm)；单元格内边距 上=%s 下=%s twips(0.05cm≈28)"
               % (_at(th, "w:hRule"), hv,
                  int(hv) / 1440.0 * 2.54 if hv else 0.0, marg("top"), marg("bottom")))
    return out


def media_count(path):
    with zipfile.ZipFile(path) as z:
        return sum(1 for n in z.namelist() if n.startswith("word/media/"))


def verify(out_path, cover_paras):
    doc = Document(out_path)
    body = doc.element.body
    paras = doc.paragraphs
    kinds = [classify(p) for p in paras]
    new_paras = paras[cover_paras:]
    new_kinds = kinds[cover_paras:]

    h1 = new_kinds.count("H1")
    ref_head = sum(1 for p, k in zip(new_paras, new_kinds)
                   if k == "H1" and p.text.strip() == REF_TITLE)
    body_paras = [p for p, k in zip(new_paras, new_kinds) if k == "P"]

    t = doc.tables[0] if doc.tables else None
    rows = len(t.rows) if t is not None else 0
    cols = len(t.columns) if t is not None else 0
    sect_last = body[-1].tag == qn("w:sectPr")

    print("=" * 78)
    print("成品校验： %s" % out_path)
    print("sectPr 位于 body 末尾：%s（body 子元素 %d 个）" % (sect_last, len(body)))
    print("段落总数（body 全部 w:p，含保留的封面段 %d 个）：%d"
          % (cover_paras, len(paras)))
    print("新增正文段落数：%d" % (len(paras) - cover_paras))
    print("一级标题数：%d（其中自动生成的“参考文献”标题 %d 个）" % (h1, ref_head))
    print("二级标题数：%d" % new_kinds.count("H2"))
    print("题目段数：%d" % new_kinds.count("TITLE"))
    print("摘要/关键词段数：%d" % new_kinds.count("ABS"))
    print("正文字符数（宋体12pt 正文段合计）：%d" % sum(len(p.text) for p in body_paras))
    print("参考文献条数：%d" % new_kinds.count("REF"))
    print("media 图片数：%d（模板 %d）" % (media_count(out_path), media_count(TEMPLATE)))
    print("表格数：%d（table[0] 为模板评分表）；table[0] 行列数：%d 行 × %d 列"
          % (len(doc.tables), rows, cols))
    print("题注段数：%d" % new_kinds.count("CAP"))
    for i, tb in enumerate(doc.tables[1:], 1):
        for line in describe_table(tb, i):
            print(line)
    if body_paras:
        print("正文首段：%s" % body_paras[0].text[:24])
        print("  实测：%s" % measure(body_paras[0]))
        print("正文末段：%s" % body_paras[-1].text[:24])
        print("  实测：%s" % measure(body_paras[-1]))
    print("=" * 78)


def main(argv):
    if len(argv) != 3:
        sys.stderr.write("用法： python build_docx.py <input.md> <output.docx>\n")
        return 2
    md_path, out_path = argv[1], argv[2]
    if not os.path.isfile(md_path):
        sys.stderr.write("输入稿件不存在： %s\n" % md_path)
        return 2
    if not os.path.isfile(TEMPLATE):
        sys.stderr.write("模板不存在： %s\n" % TEMPLATE)
        return 2
    cover = build(md_path, out_path)
    verify(out_path, cover)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
