
import os, glob, json, gzip
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import defaultdict
np.random.seed(1)
base=r"C:\Users\Administrator\Desktop\丙酮酰化"; data=os.path.join(base,"data"); figs=os.path.join(base,"figs")
plt.rcParams.update({"font.family":"Arial","font.size":7,"axes.labelsize":7.2,"axes.titlesize":7.8,
 "xtick.labelsize":6.6,"ytick.labelsize":6.6,"axes.linewidth":0.6,"xtick.major.width":0.6,"ytick.major.width":0.6,
 "xtick.major.size":2.4,"ytick.major.size":2.4,"axes.spines.top":False,"axes.spines.right":False,
 "savefig.bbox":"standard","savefig.pad_inches":0,"pdf.fonttype":42})
CB={"blue":"#0072B2","orange":"#E69F00","green":"#009E73","red":"#D55E00","grey":"#666666"}
site_mods=defaultdict(set)
for f in sorted(glob.glob(os.path.join(data,"cplm","*","*.txt"))):
    mod=os.path.basename(os.path.dirname(f))
    df=pd.read_csv(f,sep="\t",header=None,usecols=[1,2,5],names=["acc","pos","sp"],dtype=str,on_bad_lines="skip")
    df=df[df["sp"].fillna("").str.contains("Homo sapiens",na=False)].dropna(subset=["acc","pos"])
    df=df[df["pos"].str.match(r"^\d+$",na=False)]
    for a,p in zip(df.acc.str.strip(),df.pos.astype(int)): site_mods[(a,p)].add(mod)
per_mod=defaultdict(int); multi_by_mod=defaultdict(int)
for (a,p),v in site_mods.items():
    for m in v:
        per_mod[m]+=1
        if len(v)>=2: multi_by_mod[m]+=1

# full-length densities from UniProt sequences
seqs={}
for f in glob.glob(os.path.join(data,"uniprot","*.json")):
    raw=open(f,"rb").read()
    if raw[:2]==b"\x1f\x8b": raw=gzip.decompress(raw)
    j=json.loads(raw.decode("utf-8")); seqs[os.path.basename(f)[:-5]]=j.get("sequence",{}).get("value","")
HISTG={"P62805":"H4C1","P68431":"H3C1","P62807":"H2BC4","Q99525":"H4C7"}
dens={a: (sum(1 for s in site_mods if s[0]==a))/max(1,s.count("K")) for a,s in seqs.items() if s}
med_all=float(np.median(list(dens.values())))
med=med_all
print("proteins",len(dens),"median non-histone density %.4f"%med, {HISTG[a]:round(dens[a],2) for a in HISTG if a in dens})

fig,axes=plt.subplots(1,2,figsize=(7.0,2.8),gridspec_kw={"width_ratios":[1,1.2],"wspace":0.5})
fig.subplots_adjust(left=0.09,right=0.99,top=0.88,bottom=0.15)
ax=axes[0]
for i,(lab,sel) in enumerate([("non-histone",[a for a in dens if a not in HISTG]),("histone",[a for a in dens if a in HISTG])]):
    v=np.array([dens[a] for a in sel]); x=np.random.normal(i,0.05,len(v))
    ax.scatter(v,x,s=7,color=CB["blue"] if i==0 else CB["orange"],alpha=0.75,linewidths=0)
ax.axhspan(0.5,1.5,color=CB["orange"],alpha=0.10,lw=0)
ax.set_yticks([0,1]); ax.set_yticklabels(["non-histone","histone"]); ax.set_ylim(-0.55,1.75)
ax.set_xlim(-0.03,1.05); ax.set_xlabel("Annotation density (catalogued Lys / all Lys)")
ax.set_title("a   Annotation density differs 24-fold\nbetween protein classes",loc="left")
ax.axvline(med,color=CB["red"],ls=(0,(3,2)),lw=0.7)
ax.text(med+0.03,0.55,"median %.3f\n(all 63 proteins)"%med,color=CB["red"],fontsize=6.3,va="center")
for j,(a,lbl) in enumerate([("P62807","H2BC4"),("P68431","H3C1"),("P62805","H4C1")]):
    if a in dens:
        ax.annotate(lbl,(dens[a],1),xytext=(dens[a]-0.09,1.28+j*0.16),fontsize=6.5,color=CB["grey"],
                    arrowprops=dict(arrowstyle="-",lw=0.4,color="#AAAAAA",shrinkA=1,shrinkB=1))

ax=axes[1]
mods=sorted(per_mod, key=lambda m: multi_by_mod[m]/per_mod[m])
vals=[100*multi_by_mod[m]/per_mod[m] for m in mods]
yy=np.arange(len(mods))
ax.hlines(yy,0,vals,color=CB["green"],alpha=0.45,lw=0.9)
ax.plot(vals,yy,"o",color=CB["green"],ms=4.6)
for y,m,v in zip(yy,mods,vals):
    ax.text(v+3.0,y,"%.0f%%  (n=%d)"%(v,per_mod[m]),va="center",fontsize=6.5,color=CB["grey"])
ax.set_yticks(yy); ax.set_yticklabels(["2-HIB" if m=="2-Hydroxyisobutyrylation" else m for m in mods],fontsize=6.4)
ax.set_xlim(0,132); ax.set_xticks([0,25,50,75,100]); ax.set_ylim(-0.7,len(mods)-0.3)
ax.set_xlabel("Multi-modified sites (% of catalogued sites)")
ax.set_title("b   Multi-modification rate spans 23-93%\nacross catalogued acylations",loc="left")
fig.savefig(os.path.join(figs,"Fig2_density_and_crossmod.pdf")); fig.savefig(os.path.join(figs,"Fig2_density_and_crossmod.png"),dpi=300)
print("ok")

import os as _os
_sub=_os.path.join(os.path.dirname(os.path.dirname(_os.path.abspath(__file__))),"figs","submission")
_os.makedirs(_sub, exist_ok=True)
fig.savefig(_os.path.join(_sub,"Fig2.pdf"))
fig.savefig(_os.path.join(_sub,"Fig2.tif"), dpi=600, pil_kwargs={"compression":"tiff_lzw"})
print("submission export done")
