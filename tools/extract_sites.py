
import pandas as pd, os
supp = r"C:\Users\Administrator\Desktop\丙酮酰化\data\supp"
out  = r"C:\Users\Administrator\Desktop\丙酮酰化\data"
f = os.path.join(supp, "MOESM2.xlsx")
raw = pd.read_excel(f, sheet_name="kpySites", header=None)
print("shape:", raw.shape)
for i in range(min(6, len(raw))):
    print(i, [str(x)[:40] for x in raw.iloc[i].tolist()[:8]])
hdr = None
for i in range(min(10, len(raw))):
    row = [str(x).strip().lower() for x in raw.iloc[i].tolist()]
    if any("site" in c or "position" in c or "protein" in c or "gene" in c for c in row):
        hdr = i; break
print("header row:", hdr)
if hdr is not None:
    df = pd.read_excel(f, sheet_name="kpySites", header=hdr)
    df = df.dropna(how="all")
    print("cols:", list(df.columns))
    print("rows:", len(df))
    print(df.head(12).to_string()[:1800])
    df.to_csv(os.path.join(out, "kpy_sites.csv"), index=False, encoding="utf-8-sig")
    print("saved kpy_sites.csv")
