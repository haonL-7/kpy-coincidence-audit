
import os, glob, math, re
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from collections import defaultdict
BASE = os.environ.get("KPY_BASE", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

base = BASE
data = os.path.join(base,"data"); figs = os.path.join(base,"figs")
plt.rcParams.update({"font.family":"Arial","font.size":7,"axes.labelsize":7.2,"axes.titlesize":7.8,
 "xtick.labelsize":6.6,"ytick.labelsize":6.6,"axes.linewidth":0.6,"xtick.major.width":0.6,"ytick.major.width":0.6,
 "xtick.major.size":2.4,"ytick.major.size":2.4,"axes.spines.top":False,"axes.spines.right":False,
 "savefig.bbox":"standard","savefig.pad_inches":0,"pdf.fonttype":42})
CB={"blue":"#0072B2","orange":"#E69F00","red":"#D55E00","grey":"#666666"}
def wilson(k,n,z=1.96):
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return (p,max(0,c-h),min(1,c+h))

kpy=pd.read_csv(os.path.join(data,"kpy_sites.csv"))
kpy["acc"]=kpy["Uniprot ID"].astype(str).str.strip(); kpy["pos"]=kpy["Positions within proteins"].astype(int)
ks=[(a,int(p)) for a,p in zip(kpy.acc,kpy.pos)]
site_mods=defaultdict(set); gene_of={}
for f in sorted(glob.glob(os.path.join(data,"cplm","*","*.txt"))):
    mod=os.path.basename(os.path.dirname(f))
    df=pd.read_csv(f,sep="\t",header=None,usecols=[1,2,4,5],names=["acc","pos","gene","sp"],dtype=str,on_bad_lines="skip")
    df=df[df["sp"].fillna("").str.contains("Homo sapiens",na=False)].dropna(subset=["acc","pos"])
    df=df[df["pos"].str.match(r"^\d+$",na=False)]
    for a,p,g in zip(df.acc.str.strip(),df.pos.astype(int),df.gene.fillna("")):
        site_mods[(a,p)].add(mod); gene_of.setdefault(a,g.strip())
HIST=re.compile(r"^(H1|H2A|H2B|H2AX|H3|H4|HIST|CENP)",re.I)
hist_acc={a for a,g in gene_of.items() if HIST.match(g)}
kpy_h=[s for s in ks if s[0] in hist_acc]; kpy_nh=[s for s in ks if s[0] not in hist_acc]
def multi(g):
    a=[s for s in g if s in site_mods]; return sum(1 for s in a if len(site_mods[s])>=2), len(a)
mA=multi(ks); mH=multi(kpy_h); mN=multi(kpy_nh)
cH=(len([s for s in kpy_h if s in site_mods]),len(kpy_h)); cN=(len([s for s in kpy_nh if s in site_mods]),len(kpy_nh))

fig = plt.figure(figsize=(7.0,3.95))
gs = fig.add_gridspec(2,3, height_ratios=[1.25,2.15], hspace=0.58, wspace=0.95,
                      left=0.115, right=0.985, top=0.90, bottom=0.15)
ax0 = fig.add_subplot(gs[0,:]); ax0.set_xlim(0,100); ax0.set_ylim(0,10); ax0.axis("off")
ax0.text(0,9.9,"a   How each reference set samples lysines",fontsize=7.8,fontweight="bold",va="top")

def ticks(ax, x0, ymid, w, n, included):
    for i in range(n):
        x = x0 + w*(i+0.5)/n
        on = included[i]
        ax.plot([x,x],[ymid-0.46,ymid+0.46],color=CB["blue"] if on else "#D2D2D2",
                lw=1.6 if on else 0.9,solid_capstyle="butt",zorder=3)
def bar(ax,x0,y,w,h=0.95):
    ax.add_patch(FancyBboxPatch((x0,y),w,h,boxstyle="round,pad=0.10,rounding_size=0.22",
                                fc="#E9F2F8",ec="#A9BECB",lw=0.6,zorder=2))
W=20.0; X=[2.0,27.0,52.0,77.0]
def label(i,letter,name):
    ax0.text(X[i],7.7,letter,fontsize=7.4,fontweight="bold")
    ax0.text(X[i]+2.8,7.7,name,fontsize=6.6)
# A
label(0,"A","pooled across proteins")
for yy in (5.9,4.8,3.7):
    bar(ax0,X[0],yy,W); ticks(ax0,X[0],yy+0.475,W,11,[True]*11)
# B
label(1,"B","split by protein class")
bar(ax0,X[1],5.9,W); ticks(ax0,X[1],6.375,W,14,[True]*14)
bar(ax0,X[1],3.7,W); ticks(ax0,X[1],4.175,W,9,[True,False,True,False,True,False,True,False,True])
# C
label(2,"C","within protein, all lysines")
bar(ax0,X[2],4.8,W); ticks(ax0,X[2],5.275,W,12,[True]*12)
# D
label(3,"D","within protein, catalogued")
bar(ax0,X[3],4.8,W); ticks(ax0,X[3],5.275,W,12,[True,False,False,True,False,True,False,False,True,False,False,True])
ax0.text(X[0],1.9,"filled ticks = lysines entering the comparison set;  pale ticks = excluded",fontsize=6.4,color=CB["grey"])

axes=[fig.add_subplot(gs[1,i]) for i in range(3)]
ax=axes[0]
rows=[("A  pooled",*mA,14754/66790,"P = 1e-5"),("B  histone",*mH,371/756,"P = 0.011"),
      ("B  non-histone",*mN,14383/66034,"P = 0.044"),("D  histone",*mH,8.0/10,"P = 0.351"),
      ("D  non-histone",*mN,4.8/13,"P = 0.293")]
ys=np.arange(len(rows))[::-1]
for y,(lab,k,n,exp,pt) in zip(ys,rows):
    o,lo,hi=wilson(k,n)
    ax.plot([exp*100,o*100],[y,y],color="#9EC9E2",lw=0.8,zorder=1)
    ax.plot(exp*100,y,"o",mfc="white",mec=CB["grey"],ms=4.0,mew=0.8,zorder=2)
    ax.plot(o*100,y,"o",color=CB["blue"],ms=5.2,zorder=3)
    ax.errorbar(o*100,y,xerr=[[o*100-lo*100],[hi*100-o*100]],color=CB["blue"],lw=0.8,capsize=1.6,zorder=3)
    ax.text(103,y,"%d/%d   %s"%(k,n,pt),va="center",fontsize=6.4,color=CB["grey"])
ax.set_yticks(ys); ax.set_yticklabels([r[0] for r in rows],fontsize=6.6)
ax.set_xlim(0,132); ax.set_xticks([0,20,40,60,80,100])
ax.set_xlabel("Multi-modified, % of catalogued Kpy sites")
ax.set_title("b   Observed versus expected",loc="left")
ax.axvline(22.1,color=CB["red"],ls=(0,(3,2)),lw=0.7,zorder=0)
ax.text(24.5,-0.72,"global baseline 22.1%",color=CB["red"],fontsize=6.4,ha="left")
ax.set_ylim(-0.85,len(rows)-0.35)

ax=axes[1]
k,n=23,88; o,lo,hi=wilson(k,n); exp=21.0/88
ax.plot([exp*100,o*100],[0,0],color="#9EC9E2",lw=0.8,zorder=1)
ax.plot(exp*100,0,"o",mfc="white",mec=CB["grey"],ms=4.0,mew=0.8,zorder=2)
ax.plot(o*100,0,"o",color=CB["blue"],ms=5.2,zorder=3)
ax.errorbar(o*100,0,xerr=[[o*100-lo*100],[hi*100-o*100]],color=CB["blue"],lw=0.8,capsize=1.6,zorder=3)
ax.set_xlim(10,55); ax.set_ylim(-1,1); ax.set_yticks([])
ax.set_xlabel("Kpy sites catalogued at all (%)")
ax.set_title("c   Reference set C")
ax.text(o*100,0.40,"observed 26.1%",ha="center",fontsize=6.6)
ax.text(exp*100,-0.52,"expected 23.9%",ha="center",fontsize=6.4,color=CB["grey"])
ax.text(43,0,"P = 0.275",fontsize=6.0,va="center")
ax.spines["left"].set_visible(False)

ax=axes[2]
for i,(lab,g) in enumerate([("non-histone",kpy_nh),("histone",kpy_h)]):
    k=len([s for s in g if s in site_mods]); n=len(g)
    o,lo,hi=wilson(k,n)
    ax.plot(o*100,i,"o",color=CB["orange"],ms=5.2)
    ax.errorbar(o*100,i,xerr=[[o*100-lo*100],[hi*100-o*100]],color=CB["orange"],lw=0.8,capsize=1.6)
    ax.text(o*100+13,i,"%d/%d"%(k,n),va="center",fontsize=6.4,color=CB["grey"])
ax.set_yticks([0,1]); ax.set_yticklabels(["non-histone","histone"],fontsize=6.6)
ax.set_xlim(0,125); ax.set_xticks([0,25,50,75,100]); ax.set_ylim(-0.7,1.6)
ax.set_xlabel("Kpy sites catalogued at all (%)")
ax.set_title("d   Coverage by protein class")
fig.savefig(os.path.join(figs,"Fig1_reference_sets.pdf"))
fig.savefig(os.path.join(figs,"Fig1_reference_sets.png"),dpi=300)
print("saved")

import os as _os

import os
_sub=_os.path.join(os.path.dirname(os.path.dirname(_os.path.abspath(__file__))),"figs","submission")
_os.makedirs(_sub, exist_ok=True)
fig.savefig(_os.path.join(_sub,"Fig1.pdf"))
fig.savefig(_os.path.join(_sub,"Fig1.tif"), dpi=600, pil_kwargs={"compression":"tiff_lzw"})
print("submission export done")
