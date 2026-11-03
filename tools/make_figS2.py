
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
rows=[("all catalogued",74,4748,CB["grey"],"o"),
      ("single-modified",21,354,CB["blue"],"o"),
      ("single-modified, query excluded",20,346,CB["blue"],"s"),
      ("multi-modified",53,128,CB["green"],"o"),
      ("multi-modified, query excluded",40,113,CB["green"],"s")]
fig=plt.figure(figsize=(3.4,2.0))
ax=fig.add_axes([0.42,0.27,0.55,0.62])
for i,(lab,k,n,c,mk) in enumerate(rows[::-1]):
    o,lo,hi=wilson(k,n)
    filled = mk=="o"
    ax.plot(o*100,i,marker=mk,color=c,ms=4.4,mfc=(c if filled else "white"),mec=c,mew=0.9)
    ax.errorbar(o*100,i,xerr=[[o*100-lo*100],[hi*100-o*100]],color=c,lw=0.9,capsize=2)
    ax.text(hi*100+2.5,i,"%d/%d"%(k,n),va="center",fontsize=6.0,color=CB["grey"])
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows[::-1]],fontsize=6.2)
ax.set_ylim(-0.6,len(rows)-0.4); ax.set_xlim(0,64)
ax.set_xlabel("Lysines with curated evidence (%)",fontsize=6.6)
ax.set_ylim(-0.75,len(rows)-0.35)
fig.savefig(os.path.join(figs,"FigS2_curation.pdf")); fig.savefig(os.path.join(figs,"FigS2_curation.png"),dpi=300)
print("FigS2 rebuilt with 5 rows")
