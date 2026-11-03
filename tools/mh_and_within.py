
import sys, os, glob, math, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import numpy as np, pandas as pd
from collections import defaultdict
root = os.environ.get("KPY_BASE", r"C:\Users\Administrator\Desktop\丙酮酰化")
data = os.path.join(root, "data")

site=defaultdict(set); gene={}
for f in sorted(glob.glob(os.path.join(data,"cplm","*","*.txt"))):
    mod=os.path.basename(os.path.dirname(f))
    df=pd.read_csv(f,sep="\t",header=None,usecols=[1,2,4,5],names=["acc","pos","g","sp"],dtype=str,on_bad_lines="skip")
    df=df[df["sp"].fillna("").str.contains("Homo sapiens",na=False)].dropna(subset=["acc","pos"])
    df=df[df["pos"].str.match(r"^\d+$",na=False)]
    for a,p,g in zip(df.acc.str.strip(),df.pos.astype(int),df.g.fillna("")):
        site[(a,p)].add(mod); gene.setdefault(a,g.strip())
HIST=re.compile(r"^(H1|H2A|H2B|H2AX|H3|H4|HIST|CENP)",re.I)
hist={a for a,g in gene.items() if HIST.match(g)}

kpy=pd.read_csv(os.path.join(data,"kpy_sites.csv"))
kpy["acc"]=kpy["Uniprot ID"].astype(str).str.strip(); kpy["pos"]=kpy["Positions within proteins"].astype(int)
ks=set((a,int(p)) for a,p in zip(kpy.acc,kpy.pos))
cat={s for s in site}
kpy_cat=[s for s in ks if s in cat]
print("catalogued Kpy sites:", len(kpy_cat))
hm=[s for s in kpy_cat if s[0] in hist]
print("  of which on histones: %d (%.0f%%)" % (len(hm), 100*len(hm)/len(kpy_cat)))
hist_sites=[s for s in cat if s[0] in hist]
print("  histone share of the whole catalogue: %d/%d = %.2f%%" % (len(hist_sites), len(cat), 100*len(hist_sites)/len(cat)))
print("  histone multi-mod rate: %.1f%%" % (100*sum(1 for s in hist_sites if len(site[s])>=2)/len(hist_sites)))

# ---- Mantel-Haenszel, stratified by protein ----
strata=defaultdict(lambda:[0,0,0,0])
for s in cat:
    a_=s[0]; is_kpy = s in ks; is_multi = len(site[s])>=2
    cell = strata[a_]
    if is_kpy and is_multi: cell[0]+=1
    elif is_kpy: cell[1]+=1
    elif is_multi: cell[2]+=1
    else: cell[3]+=1
num=den=0.0; vnum=0.0; keep=0
for a_,(a,b,c,d) in strata.items():
    n=a+b+c+d
    if n==0 or (a+b)==0 or (c+d)==0: continue
    keep+=1
    R1=a+b; R2=c+d; C1=a+c; C2=b+d
    num += a*d/n; den += b*c/n
    P=(R1*R2*C1*C2)/(n*n*(n-1)) if n>1 else 0
    vnum += P
OR = num/den if den else float("nan")
se = math.sqrt(vnum)/(num) if num>0 else float("nan")  # Greenland-Robins SE of log OR (approx)
lo, hi = math.exp(math.log(OR)-1.96*se), math.exp(math.log(OR)+1.96*se)
z = math.log(OR)/se
p = math.erfc(abs(z)/math.sqrt(2))
print("\nMantel-Haenszel (strata = protein, n=%d usable):" % keep)
print("  OR = %.2f  95%% CI %.2f-%.2f  z=%.2f  P=%.3f" % (OR, lo, hi, z, p))

# ---- within-protein structural comparison ----
rsa=pd.read_csv(os.path.join(data,"rsa_table.csv"))
lys=rsa[rsa.resname=="LYS"].copy()
lys["key"]=list(zip(lys.acc, lys.resseq.astype(int)))
lys["nmod"]=[len(site.get(k,())) for k in lys.key]
lys["plddt"]=lys.plddt.astype(float); lys["rsa"]=lys.rsa.astype(float)
rows=[]
for a_,d in lys[lys.nmod>0].groupby("acc"):
    m=d[d.nmod>=2]; s=d[d.nmod==1]
    if len(m)>=1 and len(s)>=1:
        rows.append((a_, len(m), len(s), d_p := m.plddt.mean()-s.plddt.mean(), m.rsa.mean()-s.rsa.mean(), a_ in hist))
df=pd.DataFrame(rows, columns=["acc","n_multi","n_single","d_plddt","d_rsa","histone"])
print("\nwithin-protein paired comparison (proteins with both classes): %d" % len(df))
if len(df):
    for col in ["d_plddt","d_rsa"]:
        v=df[col].values
        se_=v.std(ddof=1)/math.sqrt(len(v))
        print("  %-8s mean diff %+.3f  (95%% CI %+.3f..%+.3f)  t=%.2f  sign +:%d/-:%d" % (
            col, v.mean(), v.mean()-1.96*se_, v.mean()+1.96*se_, v.mean()/se_ if se_ else 0,
            int((v>0).sum()), int((v<0).sum())))
    print("  proteins involved:", ", ".join(df.acc.head(12).tolist()), "..." if len(df)>12 else "")
