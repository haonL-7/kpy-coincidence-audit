
import os, math
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
BASE = r"C:\Users\Administrator\Desktop\丙酮酰化"
figs = os.path.join(BASE, "figs")
plt.rcParams.update({"font.family":"Arial","font.size":7,"axes.labelsize":7.2,"axes.titlesize":7.8,
 "xtick.labelsize":6.6,"ytick.labelsize":6.6,"axes.linewidth":0.6,"xtick.major.width":0.6,"ytick.major.width":0.6,
 "xtick.major.size":2.4,"ytick.major.size":2.4,"axes.spines.top":False,"axes.spines.right":False,
 "savefig.bbox":"standard","savefig.pad_inches":0,"pdf.fonttype":42})
CB={"blue":"#0072B2","green":"#009E73","grey":"#666666","red":"#D55E00"}
def wilson(k,n,z=1.96):
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return (p,max(0,c-h),min(1,c+h))
import csv as _csv
_P=[r for r in _csv.DictReader(open(os.path.join(BASE,"data","pubmed_provenance.csv"),encoding="utf-8-sig"))]
_K={(r["Uniprot ID"].strip(),int(r["Positions within proteins"])) for r in _csv.DictReader(open(os.path.join(BASE,"data","kpy_sites.csv"),encoding="utf-8-sig")) if (r["Positions within proteins"] or "").strip().isdigit()}
_L=lambda rs: sum(1 for r in rs if r["pubmed_linked"]=="1")
_m=[r for r in _P if int(r["cplm_mods"])>=2]; _s=[r for r in _P if int(r["cplm_mods"])==1]
_rest=[r for r in _P if int(r["cplm_mods"])>=1 and (r["acc"],int(r["pos"])) not in _K]
_rm=[r for r in _rest if int(r["cplm_mods"])>=2]; _rs=[r for r in _rest if int(r["cplm_mods"])==1]
rows=[("all lysines",_L(_P),len(_P),CB["grey"],"o"),
      ("single-modified",_L(_s),len(_s),CB["blue"],"o"),
      ("single-modified, query excluded",_L(_rs),len(_rs),CB["blue"],"s"),
      ("multi-modified",_L(_m),len(_m),CB["green"],"o"),
      ("multi-modified, query excluded",_L(_rm),len(_rm),CB["green"],"s")]
fig=plt.figure(figsize=(3.4,2.0))
ax=fig.add_axes([0.42,0.30,0.55,0.59])
for i,(lab,k,n,c,mk) in enumerate(rows[::-1]):
    o,lo,hi=wilson(k,n)
    filled = mk=="o"
    ax.plot(o*100,i,marker=mk,color=c,ms=4.4,mfc=(c if filled else "white"),mec=c,mew=0.9)
    ax.errorbar(o*100,i,xerr=[[o*100-lo*100],[hi*100-o*100]],color=c,lw=0.9,capsize=2)
    ax.text(hi*100+2.5,i,"%d/%d"%(k,n),va="center",fontsize=6.0,color=CB["grey"])
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows[::-1]],fontsize=6.2)
ax.set_ylim(-0.6,len(rows)-0.4); ax.set_xlim(0,52)
ax.set_xlabel("Lysines with PubMed-linked\nMOD_RES annotations (%)",fontsize=6.6)
ax.set_ylim(-0.75,len(rows)-0.35)
fig.savefig(os.path.join(figs,"FigS2_curation.pdf")); fig.savefig(os.path.join(figs,"FigS2_curation.png"),dpi=600)
print("FigS2 rebuilt with 5 rows")
sub=os.path.join(figs,"submission"); os.makedirs(sub,exist_ok=True)
fig.savefig(os.path.join(sub,"FigS2.pdf")); fig.savefig(os.path.join(sub,"FigS2.tif"),dpi=600,pil_kwargs={"compression":"tiff_lzw"})
