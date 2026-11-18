# -*- coding: utf-8 -*-
"""Formatting + quote optimization for the pet live-commerce paper."""
import copy, io, re
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC = r"C:\Users\Administrator\Desktop\丙酮酰化\测试\宠物活体论文\宠物活体运输的福利问题——被制度与舆论忽略的活体电商.docx"
DST = r"C:\Users\Administrator\Desktop\丙酮酰化\宠物活体运输的福利问题——被制度与舆论忽略的活体电商（排版优化）.docx"

doc = Document(SRC)
log = []
def L(s): log.append(s)

# ---------- helpers ----------
def rpr_of(run):
    return run._r.get_or_add_rPr()

def set_run(run, ascii_=None, ea=None, size=None, bold=None):
    rPr = rpr_of(run)
    rf = rPr.get_or_add_rFonts()
    if ascii_:
        rf.set(qn('w:ascii'), ascii_); rf.set(qn('w:hAnsi'), ascii_)
    if ea:
        rf.set(qn('w:eastAsia'), ea)
    rf.set(qn('w:hint'), 'eastAsia')
    if size is not None:
        run.font.size = Pt(size)
        szcs = rPr.find(qn('w:szCs'))
        if szcs is None:
            szcs = OxmlElement('w:szCs'); rPr.append(szcs)
        szcs.set(qn('w:val'), str(int(size * 2)))
    if bold is not None:
        run.font.bold = bold

def clear_runs(par):
    for r in list(par.runs):
        r._r.getparent().remove(r._r)

def set_ind(par, first_line_chars=None, first_line_tw=None, left=None, hanging=None):
    pPr = par._p.get_or_add_pPr()
    ind = pPr.find(qn('w:ind'))
    if ind is None:
        ind = OxmlElement('w:ind'); pPr.append(ind)
    for a in ('w:firstLine', 'w:firstLineChars', 'w:hanging', 'w:hangingChars'):
        if ind.get(qn(a)) is not None:
            del ind.attrib[qn(a)]
    if left is not None:
        ind.set(qn('w:left'), str(int(left)))
    if hanging is not None:
        ind.set(qn('w:hanging'), str(int(hanging)))
    if first_line_chars is not None:
        ind.set(qn('w:firstLineChars'), str(int(first_line_chars)))
    if first_line_tw is not None:
        ind.set(qn('w:firstLine'), str(int(first_line_tw)))

def add_outline(par, level):
    pPr = par._p.get_or_add_pPr()
    for old in pPr.findall(qn('w:outlineLvl')):
        pPr.remove(old)
    ol = OxmlElement('w:outlineLvl'); ol.set(qn('w:val'), str(level))
    # must precede rPr / sectPr / pPrChange
    anchor = None
    for tag in ('w:rPr', 'w:sectPr', 'w:pPrChange'):
        e = pPr.find(qn(tag))
        if e is not None:
            anchor = e; break
    if anchor is not None:
        anchor.addprevious(ol)
    else:
        pPr.append(ol)

def set_child(pPr, tag, val=None, attrs=None):
    e = pPr.find(qn(tag))
    if e is None:
        e = OxmlElement(tag)
        # insert before rPr/sectPr/pPrChange keeps schema order for most cases
        anchor = None
        for t in ('w:rPr', 'w:sectPr', 'w:pPrChange'):
            x = pPr.find(qn(t))
            if x is not None:
                anchor = x; break
        if anchor is not None:
            anchor.addprevious(e)
        else:
            pPr.append(e)
    if val is not None:
        e.set(qn('w:val'), val)
    for k, v in (attrs or {}).items():
        e.set(qn(k), v)
    return e

def txt(par):
    return par.text

# ---------- 1. straight double quotes -> Chinese quotes ----------
fixed = []
def fix_quotes(par):
    state = 0
    n = 0
    for run in par.runs:
        t = run.text
        if '"' not in t:
            continue
        out = []
        for ch in t:
            if ch == '"':
                out.append('\u201c' if state == 0 else '\u201d')
                state ^= 1
                n += 1
            else:
                out.append(ch)
        run.text = ''.join(out)
    return n, state

total_q = 0
unbalanced = []
for i, par in enumerate(doc.paragraphs):
    n, state = fix_quotes(par)
    if n:
        total_q += n
        fixed.append((i, n))
        if state != 0:
            unbalanced.append(i)
for tbl in doc.tables:
    for row in tbl.rows:
        for cell in row.cells:
            for par in cell.paragraphs:
                n, state = fix_quotes(par)
                if n:
                    total_q += n
                    fixed.append(('cell', n))
L("quotes converted: %d, paragraphs=%s, unbalanced=%s" % (total_q, fixed, unbalanced))

# (5F) inside a Chinese reference title -> full width
for par in doc.paragraphs:
    if '(5F)' in par.text:
        for run in par.runs:
            if '(5F)' in run.text:
                run.text = run.text.replace('(5F)', '\uff085F\uff09')
                L("(5F) -> full width in: " + par.text[:40])

# ---------- 2. cover page: trim filler paragraphs ----------
ps = doc.paragraphs
cover = [ps[i] for i in range(25)]          # indices 0..24 snapshot (element refs stay valid)
logo, subtitle, date_line = ps[5], ps[9], ps[23]
fields = [ps[15], ps[16], ps[17], ps[18], ps[19], ps[20], ps[21]]
drop = [ps[6], ps[7], ps[10], ps[11], ps[12], ps[13], ps[22]]
for p in drop:
    p._p.getparent().remove(p._p)
L("removed %d cover filler paragraphs" % len(drop))

# consistent horizontal start for every cover field line
for p, left in ((ps[15], 1690), (ps[16], 1690), (ps[17], 1690), (ps[18], 1690),
                (ps[19], 1690), (ps[20], 1690), (ps[21], 1690), (ps[22], 1690), (ps[23], 1690)):
    if p._p.getparent() is None:
        continue
    set_ind(p, left=left)

# 题目: label + tab + title, continuation lines align under the title (not under the label)
p15 = ps[15]
title_txt = p15.text
m = re.match(r'^题\s*目\s+', title_txt)
value = title_txt[m.end():] if m else title_txt
clear_runs(p15)
run_label = p15.add_run('题\u3000\u3000目')
set_run(run_label, ascii_='Times New Roman', ea='黑体', size=14)
run_tab = p15.add_run()
set_run(run_tab, ascii_='Times New Roman', ea='黑体', size=14)
run_tab._r.append(OxmlElement('w:tab'))
chead, csep, ctail = value.partition('——')
if csep:
    run_val = p15.add_run(chead + '——')
    set_run(run_val, ascii_='Times New Roman', ea='黑体', size=14)
    run_val.add_break()
    run_val2 = p15.add_run(ctail)
    set_run(run_val2, ascii_='Times New Roman', ea='黑体', size=14)
else:
    run_val = p15.add_run(value)
    set_run(run_val, ascii_='Times New Roman', ea='黑体', size=14)
set_ind(p15, left=3120, hanging=1430)
set_child(p15._p.get_or_add_pPr(), 'w:tabs', attrs={})  # placeholder replaced below

pPr15 = p15._p.get_or_add_pPr()
tabs = pPr15.find(qn('w:tabs'))
for ch in list(tabs):
    tabs.remove(ch)
tab = OxmlElement('w:tab'); tab.set(qn('w:val'), 'left'); tab.set(qn('w:pos'), '3120')
tabs.append(tab)

# ---------- 3. section split: cover = section 1 (no page number), body = section 2 ----------
body = doc.element.body
sectPr_body = body.find(qn('w:sectPr'))
sectPr_cover = copy.deepcopy(sectPr_body)
for ref in sectPr_cover.findall(qn('w:footerReference')) + sectPr_cover.findall(qn('w:headerReference')):
    sectPr_cover.remove(ref)
end_par = ps[24]._p
end_par.get_or_add_pPr().append(sectPr_cover)
# body section restarts numbering at 1
pgnum = sectPr_body.find(qn('w:pgNumType'))
if pgnum is None:
    pgnum = OxmlElement('w:pgNumType')
    sectPr_body.insert(0, pgnum)
pgnum.set(qn('w:start'), '1')
L("sections: %d" % len(doc.sections))

# ---------- 4. footer: plain centred page number instead of the framed text box ----------
sec_body = doc.sections[-1]
ftr = sec_body.footer
ftr_el = ftr._element
for child in list(ftr_el):
    ftr_el.remove(child)
fp = OxmlElement('w:p')
fpPr = OxmlElement('w:pPr')
fjc = OxmlElement('w:jc'); fjc.set(qn('w:val'), 'center'); fpPr.append(fjc)
fsp = OxmlElement('w:spacing'); fsp.set(qn('w:before'), '0'); fsp.set(qn('w:after'), '0'); fpPr.append(fsp)
fp.append(fpPr)
def fld_run(kind=None, instr=None):
    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    rf = OxmlElement('w:rFonts'); rf.set(qn('w:ascii'), 'Times New Roman'); rf.set(qn('w:hAnsi'), 'Times New Roman'); rf.set(qn('w:eastAsia'), '宋体')
    rPr.append(rf)
    sz = OxmlElement('w:sz'); sz.set(qn('w:val'), '21'); rPr.append(sz)
    szcs = OxmlElement('w:szCs'); szcs.set(qn('w:val'), '21'); rPr.append(szcs)
    r.append(rPr)
    if kind:
        f = OxmlElement('w:fldChar'); f.set(qn('w:fldCharType'), kind); r.append(f)
    if instr:
        it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = instr; r.append(it)
    return r
fp.append(fld_run('begin'))
fp.append(fld_run(instr=' PAGE  \\* MERGEFORMAT '))
fp.append(fld_run('separate'))
r_txt = OxmlElement('w:r')
rPr = OxmlElement('w:rPr')
rf = OxmlElement('w:rFonts'); rf.set(qn('w:ascii'), 'Times New Roman'); rf.set(qn('w:hAnsi'), 'Times New Roman'); rf.set(qn('w:eastAsia'), '宋体')
rPr.append(rf); r_txt.append(rPr)
t = OxmlElement('w:t'); t.text = '1'; r_txt.append(t)
fp.append(r_txt)
fp.append(fld_run('end'))
ftr_el.append(fp)
L("footer rewritten, section1 footer linked=%s" % str(doc.sections[0].footer.is_linked_to_previous))

# ---------- 5. article title: balanced manual break ----------
ps = doc.paragraphs
art_title = None
for p in ps:
    if p.text.startswith('宠物活体运输的福利问题') and p.alignment == WD_ALIGN_PARAGRAPH.CENTER:
        art_title = p
        break
L("article title found: " + str(art_title is not None) + " text=" + art_title.text)
head, sep, tail = art_title.text.partition('——')
clear_runs(art_title)
r1 = art_title.add_run(head + '——')
set_run(r1, ascii_='Times New Roman', ea='黑体', size=16, bold=True)
r1.add_break()
r2 = art_title.add_run(tail)
set_run(r2, ascii_='Times New Roman', ea='黑体', size=16, bold=True)

# ---------- 6. 摘要 / 关键词: label bold heiti, body regular songti, 小四 ----------
def rebuild_label_par(par, label):
    body_txt = par.text
    if body_txt.startswith(label):
        body_txt = body_txt[len(label):]
    clear_runs(par)
    rl = par.add_run(label)
    set_run(rl, ascii_='Times New Roman', ea='黑体', size=12, bold=True)
    rb = par.add_run(body_txt)
    set_run(rb, ascii_='Times New Roman', ea='宋体', size=12, bold=False)
    par.paragraph_format.line_spacing = 1.5
    par.paragraph_format.space_before = Pt(0)
    par.paragraph_format.space_after = Pt(0)
    set_ind(par, first_line_chars=200, first_line_tw=480, left=0)

abs_par = key_par = None
for p in doc.paragraphs:
    if p.text.startswith('摘要：'):
        abs_par = p
    elif p.text.startswith('关键词：'):
        key_par = p
rebuild_label_par(abs_par, '摘要：')
rebuild_label_par(key_par, '关键词：')
L("abstract/keywords rebuilt")

# ---------- 7. headings: outline levels + keep with next ----------
h1 = h2 = 0
for p in doc.paragraphs:
    t = p.text.strip()
    if not t or len(t) > 40:
        continue
    r0 = p.runs[0] if p.runs else None
    if r0 is None or not r0.font.bold:
        continue
    sz = r0.font.size.pt if r0.font.size else 0
    if re.match(r'^[一二三四五六七八九十]+、', t) or t == '参考文献':
        add_outline(p, 0); p.paragraph_format.keep_with_next = True; p.paragraph_format.keep_together = True; h1 += 1
    elif re.match(r'^\d+\.\s', t) and sz <= 12:
        add_outline(p, 1); p.paragraph_format.keep_with_next = True; p.paragraph_format.keep_together = True; h2 += 1
L("headings: level1=%d level2=%d" % (h1, h2))

# table caption keeps with the table
for p in doc.paragraphs:
    if p.text.startswith('表1'):
        p.paragraph_format.keep_with_next = True
        set_ind(p, left=0)
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(4)

# ---------- 7b. reference entries: uniform line pitch (grid snapping off) ----------
refs = 0
for p in doc.paragraphs:
    if re.match(r'^\[\d+\]', p.text.strip()):
        pPr = p._p.get_or_add_pPr()
        snap = pPr.find(qn('w:snapToGrid'))
        if snap is None:
            snap = OxmlElement('w:snapToGrid')
            spacing = pPr.find(qn('w:spacing'))
            if spacing is not None:
                spacing.addprevious(snap)
            else:
                pPr.append(snap)
        snap.set(qn('w:val'), '0')
        refs += 1
L("reference paragraphs without grid snapping: %d" % refs)

# ---------- 8. body paragraphs: first line indent = 2 characters ----------
n_ind = 0
for p in doc.paragraphs:
    ind = p._p.find(qn('w:pPr') + '/' + qn('w:ind'))
    fl = ind.get(qn('w:firstLine')) if ind is not None else None
    if fl == '480' or (p.paragraph_format.first_line_indent is not None and p.paragraph_format.first_line_indent.twips == 480):
        set_ind(p, first_line_chars=200, first_line_tw=480, left=0)
        n_ind += 1
L("body paragraphs with 2-char first line indent: %d" % n_ind)

# ---------- 9. table: three-line table, repeating header, centred cells ----------
tbl = doc.tables[0]
tblPr = tbl._element.tblPr
borders = tblPr.find(qn('w:tblBorders'))
if borders is None:
    borders = OxmlElement('w:tblBorders'); tblPr.append(borders)
for ch in list(borders):
    borders.remove(ch)
def border(tag, val, sz=None):
    e = OxmlElement(tag)
    e.set(qn('w:val'), val); e.set(qn('w:sz'), str(sz if sz else 0))
    e.set(qn('w:space'), '0'); e.set(qn('w:color'), '000000')
    borders.append(e)
border('w:top', 'single', 12)
border('w:left', 'none')
border('w:bottom', 'single', 12)
border('w:right', 'none')
border('w:insideH', 'none')
border('w:insideV', 'none')

TC_AFTER = ('w:shd', 'w:noWrap', 'w:tcMar', 'w:textDirection', 'w:tcFitText', 'w:vAlign', 'w:hideMark')
last = len(tbl.rows) - 1
for ri, row in enumerate(tbl.rows):
    trPr = row._tr.get_or_add_trPr()
    if trPr.find(qn('w:cantSplit')) is None:
        trPr.append(OxmlElement('w:cantSplit'))
    if ri == 0 and trPr.find(qn('w:tblHeader')) is None:
        trPr.append(OxmlElement('w:tblHeader'))
    for cell in row.cells:
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        tcPr = cell._tc.get_or_add_tcPr()
        tcb = tcPr.find(qn('w:tcBorders'))
        if tcb is None:
            tcb = OxmlElement('w:tcBorders')
            anchor = None
            for tag in TC_AFTER:
                e = tcPr.find(qn(tag))
                if e is not None:
                    anchor = e; break
            if anchor is not None:
                anchor.addprevious(tcb)
            else:
                tcPr.append(tcb)
        for ch in list(tcb):
            tcb.remove(ch)
        def cb(tag, val, sz=0):
            e = OxmlElement(tag)
            e.set(qn('w:val'), val); e.set(qn('w:sz'), str(sz))
            e.set(qn('w:space'), '0'); e.set(qn('w:color'), '000000')
            tcb.append(e)
        cb('w:top', 'single', 12) if ri == 0 else cb('w:top', 'none')
        cb('w:left', 'none')
        if ri == 0:
            cb('w:bottom', 'single', 6)
        elif ri == last:
            cb('w:bottom', 'single', 12)
        else:
            cb('w:bottom', 'none')
        cb('w:right', 'none')
        for par in cell.paragraphs:
            par.paragraph_format.line_spacing = 1.0
            par.paragraph_format.space_before = Pt(2)
            par.paragraph_format.space_after = Pt(2)
            if ri < last:
                par.paragraph_format.keep_with_next = True
mar = tblPr.find(qn('w:tblCellMar'))
if mar is not None:
    for tag in ('w:top', 'w:bottom'):
        e = mar.find(qn(tag))
        if e is not None:
            e.set(qn('w:w'), '0')
L("table: three-line cell borders, header repeat, rows kept together")

# ---------- 10. normalise child element order to the OOXML schema ----------
PPR_ORDER = ['pStyle','keepNext','keepLines','pageBreakBefore','framePr','widowControl','numPr',
             'suppressLineNumbers','pBdr','shd','tabs','suppressAutoHyphens','kinsoku','wordWrap',
             'overflowPunct','topLinePunct','autoSpaceDE','autoSpaceDN','bidi','adjustRightInd',
             'snapToGrid','spacing','ind','contextualSpacing','mirrorIndents','suppressOverlap','jc',
             'textDirection','textAlignment','textboxTightWrap','outlineLvl','divId','cnfStyle','rPr',
             'sectPr','pPrChange']
RPR_ORDER = ['rStyle','rFonts','b','bCs','i','iCs','caps','smallCaps','strike','dstrike','outline',
             'shadow','emboss','imprint','noProof','snapToGrid','vanish','webHidden','color','spacing',
             'w','kern','position','sz','szCs','highlight','u','effect','bdr','shd','fitText','vertAlign',
             'rtl','cs','em','lang','eastAsianLayout','specVanish','oMath']
TCPR_ORDER = ['cnfStyle','tcW','gridSpan','hMerge','vMerge','tcBorders','shd','noWrap','tcMar',
              'textDirection','tcFitText','vAlign','hideMark','headers','cellIns','cellDel','cellMerge','tcPrChange']
TRPR_ORDER = ['cnfStyle','divId','gridBefore','gridAfter','wBefore','wAfter','cantSplit','trHeight',
              'tblHeader','tblCellSpacing','jc','hidden','ins','del','trPrChange']
ORDERS = {'w:pPr': PPR_ORDER, 'w:rPr': RPR_ORDER, 'w:tcPr': TCPR_ORDER, 'w:trPr': TRPR_ORDER}

def normalize_order(root):
    fixed = 0
    for tag, seq in ORDERS.items():
        for el in root.iter(qn(tag)):
            children = list(el)
            def key(item):
                i, ch = item
                name = ch.tag.split('}')[1]
                pos = seq.index(name) if name in seq else len(seq) + i
                return (pos, i)
            ordered = [ch for _, ch in sorted(enumerate(children), key=key)]
            if ordered != children:
                fixed += 1
                for ch in children:
                    el.remove(ch)
                for ch in ordered:
                    el.append(ch)
    return fixed

fixed = normalize_order(doc.element.body)
for s in doc.sections:
    for part in (s.footer, s.header, s.first_page_footer, s.first_page_header):
        try:
            if not part.is_linked_to_previous:
                fixed += normalize_order(part._element)
        except Exception:
            pass
L("elements reordered to schema order: %d" % fixed)

doc.save(DST)
io.open('_optimize_log.txt', 'w', encoding='utf-8').write('\n'.join(log))
print("saved:", DST)
