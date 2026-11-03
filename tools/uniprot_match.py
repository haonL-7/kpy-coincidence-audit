
import pandas as pd, math, statistics as st
base = r"C:\Users\Administrator\Desktop\丙酮酰化\data"
df = pd.read_csv(base + r"\uniprot_lysines.csv")
kpy = pd.read_csv(base + r"\kpy_sites.csv")
kpy["acc"]=kpy["Uniprot ID"].astype(str).str.strip(); kpy["pos"]=kpy["Positions within proteins"].astype(int)
ks=set((a,int(p)) for a,p in zip(kpy["acc"],kpy["pos"]))
df["kpy"] = [ (a,p) in ks for a,p in zip(df.acc, df.pos) ]

print("== UniProt evidence depth vs modification status ==")
for lo,hi,lbl in [(0,0,"refs=0"),(1,1,"refs=1"),(2,99,"refs>=2")]:
    g = df[(df.up_refs>=lo)&(df.up_refs<=hi)]
    if len(g)==0: continue
    print("%-9s n=%4d  CPLM-annotated %4d (%.1f%%)  multi-mod %3d (%.1f%% of annotated)  Kpy %2d" % (
        lbl, len(g), (g.cplm_mods>0).sum(), 100*(g.cplm_mods>0).mean(),
        (g.cplm_mods>=2).sum(), 100*(g.cplm_mods>=2).sum()/max(1,(g.cplm_mods>0).sum()), g.kpy.sum()))

print()
print("== fair test on the 74 UniProt-curated lysines (all have >=1 curated reference) ==")
u = df[df.up_refs>=1]
ann = u[u.cplm_mods>0]
print("curated lysines: %d | CPLM-annotated: %d | of those multi-mod: %d (%.0f%%)" % (
    len(u), len(ann), (ann.cplm_mods>=2).sum(), 100*(ann.cplm_mods>=2).mean()))
print("among them, Kpy sites: %d | Kpy = %s" % (u.kpy.sum(), list(zip(u[u.kpy].acc, u[u.kpy].pos, u[u.kpy].cplm_mods))))

print()
print("== global CPLM: multi vs single, how many have any UniProt reference ==")
m = df[df.cplm_mods>=2]; s = df[df.cplm_mods==1]
print("multi-mod  n=%3d  with refs: %3d (%.0f%%)  mean refs %.2f" % (len(m), (m.up_refs>0).sum(), 100*(m.up_refs>0).mean(), m.up_refs.mean()))
print("single-mod n=%3d  with refs: %3d (%.0f%%)  mean refs %.2f" % (len(s), (s.up_refs>0).sum(), 100*(s.up_refs>0).mean(), s.up_refs.mean()))
def fisher(a,b,c,d):
    n=a+b+c+d; r1=a+b; c1=a+c
    def pmf(x): return math.comb(c1,x)*math.comb(n-c1,r1-x)/math.comb(n,r1)
    obs=pmf(a); t=0.0
    for x in range(max(0,c1-(n-r1)), min(r1,c1)+1):
        v=pmf(x)
        if v<=obs*(1+1e-7): t+=v
    return t
print("Fisher multi vs single on 'has any UniProt ref': p = %.4f" % fisher((m.up_refs>0).sum(), len(m)-(m.up_refs>0).sum(), (s.up_refs>0).sum(), len(s)-(s.up_refs>0).sum()))
