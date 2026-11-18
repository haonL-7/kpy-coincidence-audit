
import sys
sys.stdout.reconfigure(encoding="utf-8")
from PIL import Image
def bands(path, thr=200, minrun=3):
    im = Image.open(path).convert("L"); w, h = im.size; px = im.load()
    out, run = [], None
    for y in range(h):
        dark = sum(1 for x in range(0, w, 2) if px[x, y] < thr)
        if dark:
            if run is None: run = y
        else:
            if run is not None and y - run >= minrun: out.append(run)
            run = None
    if run is not None: out.append(run)
    return out
for label, p in [("本稿", r"C:\Users\Administrator\Desktop\丙酮酰化\决策蒸馏_改稿\typeset\render_final\page-0001.png"), ("六-1", r"C:\Users\Administrator\Desktop\丙酮酰化\决策蒸馏_改稿\typeset\ref_61\page-0001.png")]:
    print("%-5s %s" % (label, bands(p)))
