
# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding="utf-8")
from PIL import Image
def bands(path, thr=200, minrun=3):
    im = Image.open(path).convert("L")
    w, h = im.size
    px = im.load()
    rows = []
    for y in range(h):
        dark = 0
        for x in range(0, w, 2):
            if px[x, y] < thr: dark += 1
        rows.append(dark)
    out, run = [], None
    for y, d in enumerate(rows):
        if d > 0:
            if run is None: run = y
        else:
            if run is not None and y - run >= minrun:
                out.append((run, y - 1))
            run = None
    if run is not None: out.append((run, h - 1))
    return out, w, h
def xrange_of(path, y0, y1, thr=200):
    im = Image.open(path).convert("L"); px = im.load(); w, h = im.size
    xs = [x for y in range(y0, y1+1) for x in range(w) if px[x, y] < thr]
    return (min(xs), max(xs)) if xs else None
for label, p in [("本稿", r"C:\Users\Administrator\Desktop\丙酮酰化\决策蒸馏_改稿\typeset\render_out2\page-0001.png"), ("六-1参照", r"C:\Users\Administrator\Desktop\丙酮酰化\决策蒸馏_改稿\typeset\ref_61\page-0001.png")]:
    bs, w, h = bands(p)
    print("===", label, "page px", w, h, "文本带数", len(bs))
    for (a, b) in bs:
        xr = xrange_of(p, a, b)
        print("   y %4d-%4d (高%3d)  x %s" % (a, b, b-a+1, xr))
