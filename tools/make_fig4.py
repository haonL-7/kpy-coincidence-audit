
import os, math
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
BASE = os.environ.get("KPY_BASE", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

base=BASE; data=os.path.join(base,"data"); figs=os.path.join(base,"figs")
plt.rcParams.update({"font.family":"Arial","font.size":7,"axes.labelsize":7.2,"axes.titlesize":7.8,
 "xtick.labelsize":6.6,"ytick.labelsize":6.6,"axes.linewidth":0.6,"xtick.major.width":0.6,"ytick.major.width":0.6,
 "xtick.major.size":2.4,"ytick.major.size":2.4,"axes.spines.top":False,"axes.spines.right":False,
 "savefig.bbox":"standard","savefig.pad_inches":0,"pdf.fonttype":42})
CB={"blue":"#0072B2","green":"#009E73","red":"#D55E00","grey":"#666666"}
def wilson(k,n,z=1.96):
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return (p,max(0,c-h),min(1,c+h))

df=pd.read_csv(os.path.join(data,"uniprot_lysines.csv"))
multi=df[df.cplm_mods>=2]; single=df[df.cplm_mods==1]
rows=[("all catalogued",int((df.up_refs>0).sum()),len(df),CB["grey"]),
      ("single-mod",int((single.up_refs>0).sum()),len(single),CB["blue"]),
      ("multi-mod",int((multi.up_refs>0).sum()),len(multi),CB["green"])]
print(rows)

fig=plt.figure(figsize=(7.0,3.0))
gs=fig.add_gridspec(1,2,width_ratios=[1.0,1.45],wspace=0.42)
fig.subplots_adjust(left=0.145,right=0.99,top=0.85,bottom=0.20)

ax=fig.add_subplot(gs[0,0])
for i,(lab,k,n,c) in enumerate(rows):
    o,lo,hi=wilson(k,n)
    ax.plot(o*100,i,"o",color=c,ms=5.2)
    ax.errorbar(o*100,i,xerr=[[o*100-lo*100],[hi*100-o*100]],color=c,lw=0.9,capsize=2)
    ax.text(hi*100+2.5,i,"%d/%d"%(k,n),va="center",fontsize=6.6,color=CB["grey"])
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows],fontsize=6.8)
ax.set_ylim(-0.6,len(rows)-0.4); ax.set_xlim(0,64)
ax.set_xlabel("Lysines with curated evidence (%)")
ax.set_title("a   Curation tracks breadth",loc="left")
ax.text(0,-0.55,"Fisher P = 5.0e-19; non-independent sources",fontsize=5.8,color=CB["red"])

ax=fig.add_subplot(gs[0,1]); ax.axis("off")
ax.set_xlim(0,100); ax.set_ylim(0,100)
ax.text(0,97,"b   reporting protocol",fontsize=7.8,fontweight="bold",va="center")
def box(x,y,w,h,txt,fc,ec,fs=6.5,bold=False):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.45,rounding_size=1.4",fc=fc,ec=ec,lw=0.8))
    ax.text(x+w/2,y+h/2,txt,ha="center",va="center",fontsize=fs,fontweight=("bold" if bold else "normal"),linespacing=1.3)
def arr(x1,y1,x2,y2,c="#777777"):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=6.5,lw=0.8,color=c,shrinkA=1,shrinkB=1))
box(1,74,44,12,"1  state the reference set","#FFFFFF","#999999")
box(1,58,44,12,"2  match protein composition","#FFFFFF","#999999")
box(1,42,44,12,"3  state power (catalogued n)","#FFFFFF","#999999")
arr(23,73.5,23,70.5); arr(23,57.5,23,54.5)
box(1,22,44,13,"all three reported?","#F2F6FA","#C9D8E6",6.6,True)
arr(23,41.5,23,35.5)
box(58,32,40,13,"comparison interpretable","#E8F5EF","#8CC9AC",6.6,True)
box(58,4,40,13,"not interpretable","#FBEDED","#E0A9A9",6.6)
arr(45.5,32.5,57.5,38.0,"#4E8F6E"); ax.text(50,37.4,"yes",fontsize=6,color="#4E8F6E",ha="center")
arr(45.5,24.5,57.5,11.5,"#B06060"); ax.text(50,15.4,"no",fontsize=6,color="#B06060",ha="center")
fig.savefig(os.path.join(figs,"Fig4_curation_and_protocol.pdf"))
fig.savefig(os.path.join(figs,"Fig4_curation_and_protocol.png"),dpi=300)
print("saved")

import os as _os

import os
_sub=_os.path.join(os.path.dirname(os.path.dirname(_os.path.abspath(__file__))),"figs","submission")
_os.makedirs(_sub, exist_ok=True)
fig.savefig(_os.path.join(_sub,"Fig4.pdf"))
fig.savefig(_os.path.join(_sub,"Fig4.tif"), dpi=600, pil_kwargs={"compression":"tiff_lzw"})
print("submission export done")
