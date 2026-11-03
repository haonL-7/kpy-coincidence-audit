
import os, glob, math
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import defaultdict
np.random.seed(3)
BASE = os.environ.get("KPY_BASE", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
data = os.path.join(BASE,"data"); figs = os.path.join(BASE,"figs")
plt.rcParams.update({"font.family":"Arial","font.size":7,"axes.labelsize":7.2,"axes.titlesize":7.8,
 "xtick.labelsize":6.6,"ytick.labelsize":6.6,"axes.linewidth":0.6,"xtick.major.width":0.6,"ytick.major.width":0.6,
 "xtick.major.size":2.4,"ytick.major.size":2.4,"axes.spines.top":False,"axes.spines.right":False,
 "savefig.bbox":"standard","savefig.pad_inches":0,"pdf.fonttype":42})
CB={"blue":"#0072B2","orange":"#E69F00","green":"#009E73","red":"#D55E00","grey":"#666666","lblue":"#56B4E9"}
def wilson(k,n,z=1.96):
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return (p,max(0,c-h),min(1,c+h))
site=defaultdict(set)
for f in sorted(glob.glob(os.path.join(data,"cplm","*","*.txt"))):
    mod=os.path.basename(os.path.dirname(f))
    df=pd.read_csv(f,sep="\t",header=None,usecols=[1,2,5],names=["acc","pos","sp"],dtype=str,on_bad_lines="skip")
    df=df[df["sp"].fillna("").str.contains("Homo sapiens",na=False)].dropna(subset=["acc","pos"])
    df=df[df["pos"].str.match(r"^\d+$",na=False)]
    for a,p in zip(df.acc.str.strip(),df.pos.astype(int)): site[(a,p)].add(mod)
rsa=pd.read_csv(os.path.join(data,"rsa_table.csv"))
lys=rsa[rsa.resname=="LYS"].copy(); lys["key"]=list(zip(lys.acc,lys.resseq.astype(int)))
lys["nmod"]=[len(site.get(k,())) for k in lys.key]
lys["rsa"]=lys.rsa.astype(float); lys["plddt"]=lys.plddt.astype(float)
kpy=pd.read_csv(os.path.join(data,"kpy_sites.csv"))
kpy["acc"]=kpy["Uniprot ID"].astype(str).str.strip(); kpy["pos"]=kpy["Positions within proteins"].astype(int)
kset=set((a,int(p)) for a,p in zip(kpy.acc,kpy.pos))

fig,axes=plt.subplots(1,4,figsize=(7.0,2.3),gridspec_kw={"width_ratios":[1.15,1,0.95,1.1],"wspace":0.62})
fig.subplots_adjust(left=0.065,right=0.99,top=0.88,bottom=0.17)
groups=[("all Lys",lys,CB["grey"]),("single",lys[lys.nmod==1],CB["lblue"]),("multi",lys[lys.nmod>=2],CB["green"])]
ax=axes[0]
for i,(lab,d,col) in enumerate(groups):
    v=d.rsa.values
    vp=ax.violinplot([v],[i],widths=0.72,showextrema=False)
    for b in vp["bodies"]: b.set_facecolor(col); b.set_alpha(0.32); b.set_edgecolor("none")
    ax.scatter(np.random.normal(i,0.05,len(v)),v,s=1.0,color=col,alpha=0.3,linewidths=0)
    ax.plot([i-0.2,i+0.2],[np.median(v)]*2,color="k",lw=1.0)
kv=lys[[k in kset for k in lys.key]].rsa.values
vp=ax.violinplot([kv],[3],widths=0.72,showextrema=False)
for b in vp["bodies"]: b.set_facecolor(CB["blue"]); b.set_alpha(0.32); b.set_edgecolor("none")
ax.scatter(np.random.normal(3,0.05,len(kv)),kv,s=3,color=CB["blue"],alpha=0.75,linewidths=0)
ax.plot([2.8,3.2],[np.median(kv)]*2,color="k",lw=1.0)
ax.set_xticks([0,1,2,3]); ax.set_xticklabels(["all","single","multi","Kpy"],fontsize=6.4)
ax.set_ylabel("Relative solvent accessibility"); ax.set_ylim(-0.03,1.03)
ax.set_title("a   Pooled",loc="left")

ax=axes[1]
bins=[0,0.15,0.3,0.45,0.6,1.01]; xs=[];ys=[];los=[];his=[];ns=[]
for lo,hi in zip(bins[:-1],bins[1:]):
    g=lys[(lys.rsa>=lo)&(lys.rsa<hi)&(lys.nmod>0)]
    if len(g)==0: continue
    k=(g.nmod>=2).sum(); n=len(g); o,l,h=wilson(k,n)
    xs.append((lo+min(hi,1))/2); ys.append(o*100); los.append(o*100-l*100); his.append(h*100-o*100); ns.append(n)
ax.errorbar(xs,ys,yerr=[los,his],color=CB["green"],lw=1.0,capsize=2,marker="o",ms=4.2)
ax.text(0.02,66,"n = "+", ".join(str(n) for n in ns),fontsize=5.8,color=CB["grey"])
ax.set_xlabel("RSA"); ax.set_ylabel("Multi-modified (%)"); ax.set_ylim(0,72); ax.set_xlim(-0.03,1.03)
ax.set_title("b   Pooled, by exposure",loc="left")

ax=axes[2]
for i,(lab,d,col) in enumerate(groups):
    v=d.plddt.values
    vp=ax.violinplot([v],[i],widths=0.72,showextrema=False)
    for b in vp["bodies"]: b.set_facecolor(col); b.set_alpha(0.32); b.set_edgecolor("none")
    ax.plot([i-0.2,i+0.2],[np.median(v)]*2,color="k",lw=1.0)
    ax.text(i,99,"%.0f%%"%float((v<50).mean()*100),ha="center",fontsize=5.8,color=CB["grey"])
ax.set_xticks([0,1,2]); ax.set_xticklabels(["all","single","multi"],fontsize=6.4)
ax.set_ylim(0,106); ax.set_ylabel("pLDDT")
ax.set_title("c   Disorder (%)",loc="left")

ax=axes[3]
rows=[]
for a_,d in lys[lys.nmod>0].groupby("acc"):
    m=d[d.nmod>=2].plddt; s=d[d.nmod==1].plddt
    if len(m)>=1 and len(s)>=1: rows.append((a_, m.mean()-s.mean()))
rows.sort(key=lambda r: r[1])
yy=np.arange(len(rows))
vals=[r[1] for r in rows]
ax.axvline(0,color="#999999",lw=0.8,ls=(0,(2,1.5)))
ax.hlines(yy,0,vals,color=CB["grey"],lw=0.7)
ax.plot(vals,yy,"o",color=CB["orange"],ms=3.6)
mean=np.mean(vals); se=np.std(vals,ddof=1)/math.sqrt(len(vals))
ax.plot([mean-1.96*se,mean+1.96*se],[len(rows)-0.2]*2,color=CB["red"],lw=1.2)
ax.plot(mean,len(rows)-0.2,"|",color=CB["red"],ms=9,mew=1.4)
ax.set_yticks([]); ax.set_xlabel("ΔpLDDT (multi - single)")
ax.set_title("d   Within protein",loc="left")
ax.set_ylim(-1,len(rows)+0.6)
ax.text(0.02,0.02,"mean %+.1f  (95%% CI %+.1f to %+.1f)"%(mean,mean-1.96*se,mean+1.96*se),
        transform=ax.transAxes,fontsize=5.8,color=CB["red"])
fig.savefig(os.path.join(figs,"FigS1_structure.pdf")); fig.savefig(os.path.join(figs,"FigS1_structure.png"),dpi=300)
print("FigS1 saved; proteins in panel d:", len(rows), "mean %.2f CI %.2f..%.2f"%(mean,mean-1.96*se,mean+1.96*se))
sub=os.path.join(figs,"submission"); os.makedirs(sub,exist_ok=True)
fig.savefig(os.path.join(sub,"FigS1.pdf")); fig.savefig(os.path.join(sub,"FigS1.tif"),dpi=600,pil_kwargs={"compression":"tiff_lzw"})
