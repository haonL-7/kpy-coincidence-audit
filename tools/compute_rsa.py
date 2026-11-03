
import os, glob, numpy as np, pandas as pd, math
base = r"C:\Users\Administrator\Desktop\丙酮酰化\data"
af = os.path.join(base, "alphafold")
RAD = {"C":1.70,"N":1.55,"O":1.52,"S":1.80,"P":1.80,"H":1.20,"SE":1.90}
MAXASA = {"ALA":129,"ARG":274,"ASN":195,"ASP":193,"CYS":167,"GLN":225,"GLU":223,"GLY":104,
          "HIS":224,"ILE":197,"LEU":201,"LYS":236,"MET":224,"PHE":228,"PRO":159,"SER":130,
          "THR":193,"TRP":285,"TYR":263,"VAL":174}
# Fibonacci sphere
def sphere(n=64):
    i = np.arange(n, dtype=float) + 0.5
    phi = np.arccos(1 - 2*i/n)
    theta = np.pi*(1+5**0.5)*i
    return np.stack([np.cos(theta)*np.sin(phi), np.sin(theta)*np.sin(phi), np.cos(phi)], 1)
SPH = sphere(64); PROBE = 1.4

def parse_pdb(path):
    rows = []
    for line in open(path):
        if line.startswith("ATOM"):
            alt = line[16]
            if alt not in (" ", "A"): continue
            res = line[17:20].strip(); ch = line[21]; num = int(line[22:26])
            x,y,z = float(line[30:38]), float(line[38:46]), float(line[46:54])
            el = line[76:78].strip() or line[12:16].strip()[0]
            bf = float(line[60:66]) if line[60:66].strip() else 0.0
            rows.append((ch,num,res,line[12:16].strip(),x,y,z,el,bf))
    return rows

def sasa(rows):
    coords = np.array([[r[4],r[5],r[6]] for r in rows], dtype=np.float64)
    radii = np.array([RAD.get(r[7].upper()[:1], 1.7) for r in rows])
    n = len(rows); acc = np.zeros(n)
    cell = (radii.max()+PROBE)*2
    grid = {}
    key = np.floor(coords/cell).astype(int)
    for i,k in enumerate(map(tuple, key)):
        grid.setdefault(k, []).append(i)
    idx = [np.array(v) for v in grid.values()]
    keys = list(grid.keys())
    for i in range(n):
        kx,ky,kz = key[i]
        nb = []
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                for dz in (-1,0,1):
                    v = grid.get((kx+dx,ky+dy,kz+dz))
                    if v: nb.extend(v)
        nb = np.array(nb)
        d = np.linalg.norm(coords[nb]-coords[i], axis=1)
        rsum = radii[nb]+radii[i]+2*PROBE
        sel = (d < rsum) & (nb != i)
        if not sel.any():
            acc[i] = 4*math.pi*(radii[i]+PROBE)**2; continue
        nb = nb[sel]; rn = radii[nb]+PROBE
        pts = coords[i] + SPH*(radii[i]+PROBE)
        exposed = np.ones(len(SPH), dtype=bool)
        for j,c in zip(nb, rn):
            dd = np.linalg.norm(pts-coords[j], axis=1)
            exposed &= dd >= c
        acc[i] = exposed.mean()*4*math.pi*(radii[i]+PROBE)**2
    return acc

out = []
for f in sorted(glob.glob(os.path.join(af, "*.pdb"))):
    acc_id = os.path.basename(f)[:-4]
    rows = parse_pdb(f)
    if not rows: continue
    a = sasa(rows)
    res_sasa = {}; res_plddt = {}
    for r, s in zip(rows, a):
        key = (r[0], r[1])
        res_sasa[key] = res_sasa.get(key,0)+s
        res_plddt[key] = max(res_plddt.get(key,0), r[8])
        resname = r[2]
    for (ch,num), s in res_sasa.items():
        resname = next(r[2] for r in rows if (r[0],r[1])==(ch,num))
        mx = MAXASA.get(resname, 200)
        out.append(dict(acc=acc_id, resseq=num, resname=resname, sasa=round(s,1),
                        rsa=round(min(1.0, s/mx),3), plddt=round(res_plddt[(ch,num)],1)))
    print(acc_id, "residues:", len(res_sasa))
df = pd.DataFrame(out)
df.to_csv(os.path.join(base, "rsa_table.csv"), index=False)
print("saved rsa_table.csv rows:", len(df), "proteins:", df.acc.nunique())
