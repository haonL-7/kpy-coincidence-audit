
import sys, os
BASE = os.environ.get("KPY_BASE", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from PIL import Image
from PIL.TiffImagePlugin import ImageFileDirectory_v2

import os
base = BASE
sub = os.path.join(base, "figs", "submission")
# TOC png -> tiff
src = os.path.join(sub, "_toc600.png")
if os.path.exists(src):
    im = Image.open(src).convert("RGB")
    tif = os.path.join(sub, "TOC_Graphic.tif")
    im.save(tif, dpi=(600,600), compression="tiff_lzw")
    print("TOC:", im.size, "->", os.path.basename(tif))
else:
    print("TOC png missing")
rows=[]
for f in sorted(os.listdir(sub)):
    if not f.lower().endswith(".tif"): continue
    im = Image.open(os.path.join(sub,f))
    dpi = im.info.get("dpi",(0,0))
    comp = im.info.get("compression","?")
    w_in = im.size[0]/dpi[0] if dpi[0] else 0
    h_in = im.size[1]/dpi[1] if dpi[1] else 0
    rows.append((f, im.size, dpi, comp, im.mode, round(w_in,2), round(h_in,2), round(os.path.getsize(os.path.join(sub,f))/1e6,2)))
print("\n%-18s %-13s %-12s %-10s %-5s %-6s %-6s %s" % ("file","px","dpi","compression","mode","w_in","h_in","MB"))
for r in rows:
    print("%-18s %-13s %-12s %-10s %-5s %-6s %-6s %s" % (r[0], "%dx%d"%r[1], "%dx%d"%r[2], r[3], r[4], r[5], r[6], r[7]))
print("\nJPR limits: width <= 7.00 in (504 pt), height <= 9.167 in; colour >= 300 dpi")
for r in rows:
    print("  %-18s width %s in %s | height %s in %s" % (r[0], r[5], "OK" if r[5] <= 7.001 else "OVER", r[6], "OK" if r[6] <= 9.167 else "OVER"))
