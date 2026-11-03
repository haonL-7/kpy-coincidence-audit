
import os, glob, json, gzip, math, random, statistics as st
from collections import defaultdict
import pandas as pd
BASE = os.environ.get("KPY_BASE", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
base = os.path.join(BASE, "data")
print("========== 自检 ==========")

# 1 Kpy sites
kpy = pd.read_csv(os.path.join(base,"kpy_sites.csv"))
kpy["acc"]=kpy["Uniprot ID"].astype(str).str.strip(); kpy["pos"]=kpy["Positions within proteins"].astype(int)
ks=[(a,p) for a,p in zip(kpy.acc,kpy.pos)]
print("[1] Kpy rows=%d unique=%d proteins=%d duplicated=%d" % (len(ks), len(set(ks)), len(set(a for a,_ in ks)), len(ks)-len(set(ks))))

# 2 sequence consistency
seqs={}
for f in glob.glob(os.path.join(base,"uniprot","*.json")):
    raw=open(f,"rb").read()
    if raw[:2]==b"\x1f\x8b": raw=gzip.decompress(raw)
    j=json.loads(raw.decode("utf-8")); seqs[os.path.basename(f)[:-5]]=(j.get("organism",{}).get("scientificName",""), j.get("sequence",{}).get("value",""))
orgs=set(v[0] for v in seqs.values())
bad=[(a,p) for a,p in ks if a in seqs and (p>len(seqs[a][1]) or seqs[a][1][p-1]!="K")]
print("[2] organisms=%s | sites not K in UniProt seq: %d %s" % (orgs, len(bad), bad[:5]))
print("    sites whose protein has no UniProt record:", len([1 for a,_ in ks if a not in seqs]))

# 3 CPLM
site_mods=defaultdict(set); gene_of={}
per_mod=defaultdict(int)
for f in sorted(glob.glob(os.path.join(base,"cplm","*","*.txt"))):
    mod=os.path.basename(os.path.dirname(f))
    df=pd.read_csv(f,sep="\t",header=None,usecols=[1,2,4,5],names=["acc","pos","gene","sp"],dtype=str,on_bad_lines="skip")
    df=df[df["sp"].fillna("").str.contains("Homo sapiens",na=False)].dropna(subset=["acc","pos"])
    df=df[df["pos"].str.match(r"^\d+$",na=False)]
    for a,p,g in zip(df.acc.str.strip(),df.pos.astype(int),df.gene.fillna("")):
        site_mods[(a,p)].add(mod); gene_of.setdefault(a,g.strip()); per_mod[mod]+=1
tot=len(site_mods); multi=sum(1 for v in site_mods.values() if len(v)>=2)
print("[3] CPLM human sites=%d multi=%d (%.1f%%) | per-mod: %s" % (tot,multi,100*multi/tot, dict(sorted(per_mod.items(),key=lambda x:-x[1]))))

# 4 overlap
hit=[s for s in ks if s in site_mods]
mm=[s for s in hit if len(site_mods[s])>=2]
print("[4] Kpy annotated=%d (%.1f%%) | of those multi=%d (%.1f%%)" % (len(hit),100*len(hit)/len(ks),len(mm),100*len(mm)/len(hit)))
bymod=defaultdict(int)
for s in hit:
    for m in site_mods[s]-{"Kpy"}: bymod[m]+=1
print("    per-mod overlap:", dict(sorted(bymod.items(),key=lambda x:-x[1])))

# 5 histone classification
import re

import os
HIST=re.compile(r"^(H1|H2A|H2B|H2AX|H3|H4|HIST|CENP)",re.I)
hist_acc={a for a,g in gene_of.items() if HIST.match(g)}
kpy_hist=[s for s in ks if s[0] in hist_acc]
print("[5] histone proteins in CPLM=%d | Kpy histone sites=%d -> %s" % (len(hist_acc),len(kpy_hist),sorted(set(s[0] for s in kpy_hist))))
print("    genes:", {a:gene_of.get(a) for a in sorted(set(s[0] for s in kpy_hist))})
# annotation density for histones
dens={}
for a in sorted(set(s[0] for s in kpy_hist)):
    K=seqs.get(a,("",""))[1].count("K"); ann=sum(1 for s in site_mods if s[0]==a); dens[a]=(K,ann,round(ann/K,2) if K else None)
print("    histone density (Lys, annotated, ratio):", dens)

# 6 lactate + fisher
kla=[s for s,v in site_mods.items() if "Lactylation" in v]
kla_h=[s for s in kla if s[0] in hist_acc]
print("[6] Lactylation sites=%d histone=%d (%.0f%%)" % (len(kla),len(kla_h),100*len(kla_h)/len(kla)))
def fisher(a,b,c,d):
    n=a+b+c+d;r1=a+b;c1=a+c
    def pmf(x): return math.comb(c1,x)*math.comb(n-c1,r1-x)/math.comb(n,r1)
    o=pmf(a);t=0.0
    for x in range(max(0,c1-(n-r1)),min(r1,c1)+1):
        v=pmf(x)
        if v<=o*(1+1e-7): t+=v
    return t
histsites=[s for s in site_mods if s[0] in hist_acc]
hm=sum(1 for s in histsites if len(site_mods[s])>=2)
a_h=len([s for s in kpy_hist if s in site_mods]); a_hm=len([s for s in kpy_hist if s in site_mods and len(site_mods[s])>=2])
nh=[s for s in ks if s[0] not in hist_acc]; nh_a=[s for s in nh if s in site_mods]; nh_m=len([s for s in nh_a if len(site_mods[s])>=2])
nons=[s for s in site_mods if s[0] not in hist_acc]; nm=sum(1 for s in nons if len(site_mods[s])>=2)
print("    histone: Kpy %d/%d vs CPLM %d/%d p=%.4f" % (a_hm,a_h,hm,len(histsites),fisher(a_hm,a_h-a_hm,hm,len(histsites)-hm)))
print("    non-hist: Kpy %d/%d vs CPLM %d/%d p=%.4f" % (nh_m,len(nh_a),nm,len(nons),fisher(nh_m,len(nh_a)-nh_m,nm,len(nons)-nm)))

# 7 permutation stability
def perm(sites,iters,seed):
    bp=defaultdict(list)
    for a,p in sites:
        if (a,p) in site_mods: bp[a].append(p)
    ann={a:[s for s in site_mods if s[0]==a] for a in bp}
    obs=sum(1 for a,ps in bp.items() for p in ps if len(site_mods[(a,p)])>=2)
    random.seed(seed); null=[]
    for _ in range(iters):
        c=0
        for a,ps in bp.items():
            pool=ann[a]
            if not pool: continue
            d=random.sample(pool,min(len(ps),len(pool)))
            c+=sum(1 for s in d if len(site_mods[s])>=2)
        null.append(c)
    return obs, sum(null)/iters, sum(1 for x in null if x>=obs)/iters
for seed in (1,2,3):
    o,e,p=perm(ks,500,seed); print("[7] seed%d all: obs=%d null=%.1f p=%.3f" % (seed,o,e,p))

# 8 UniProt evidence table
rows=[]
for a,(org,seq) in seqs.items():
    for p in [i+1 for i,c in enumerate(seq) if c=="K"]:
        rows.append((a,p))
uprefs={}; upmods=defaultdict(set)
for f in glob.glob(os.path.join(base,"uniprot","*.json")):
    raw=open(f,"rb").read()
    if raw[:2]==b"\x1f\x8b": raw=gzip.decompress(raw)
    j=json.loads(raw.decode("utf-8")); a=os.path.basename(f)[:-5]
    for ft in j.get("features",[]):
        if ft.get("type")!="Modified residue": continue
        p=ft["location"]["start"]["value"]; refs=set()
        for ev in ft.get("evidences",[]):
            s=ev.get("source"); sid=s.get("id") if isinstance(s,dict) else s
            if sid: refs.add(str(sid))
        uprefs[(a,p)]=max(uprefs.get((a,p),0),len(refs))
ann_up=[s for s in rows if (s in uprefs)]
print("[8] lysines=%d UniProt-annotated=%d (%.1f%%)" % (len(rows),len(ann_up),100*len(ann_up)/len(rows)))
for lo,hi,lbl in [(1,1,"refs=1"),(2,99,"refs>=2")]:
    g=[s for s in ann_up if lo<=uprefs.get(s,0)<=hi]
    gm=[s for s in g if len(site_mods.get(s,()))>=2]
    print("    %-8s n=%d multi=%d (%.0f%%)" % (lbl,len(g),len(gm),100*len(gm)/max(1,len(g))))
multi_sites=[s for s in site_mods if len(site_mods[s])>=2 and s[0] in seqs]
single_sites=[s for s in site_mods if len(site_mods[s])==1 and s[0] in seqs]
a1=sum(1 for s in multi_sites if uprefs.get(s,0)>0); b1=len(multi_sites)-a1
c1=sum(1 for s in single_sites if uprefs.get(s,0)>0); d1=len(single_sites)-c1
print("    multi %d/%d vs single %d/%d  fisher p=%.2e" % (a1,len(multi_sites),c1,len(single_sites),fisher(a1,b1,c1,d1)))

# 9 structure mapping
rsa=pd.read_csv(os.path.join(base,"rsa_table.csv"))
have=set(rsa.acc)
miss=[s for s in ks if s[0] not in have]
print("[9] Kpy sites with AF model: %d/%d | missing %d from %s" % (len(ks)-len(miss),len(ks),len(miss),sorted(set(a for a,_ in miss))))
