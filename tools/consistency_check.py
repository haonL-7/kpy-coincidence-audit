
import sys, re, json, os
import pandas as pd

import os
BASE = os.environ.get("KPY_BASE", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ms = os.path.join(BASE, "08_manuscript_v1.md")
t = open(ms, encoding="utf-8").read()
body = t.split("## References")[0]
refs = t.split("## References")[1].split("## Figure legends")[0]

# --- citations ---
marks = re.findall(r"\[([0-9,\-]+)\]", body)
cited = set()
order = []
for m in marks:
    for part in m.split(","):
        if "-" in part:
            a,b = part.split("-"); rng = range(int(a), int(b)+1)
        else:
            rng = [int(part)]
        for x in rng:
            cited.add(x)
            if x not in order: order.append(x)
have = {int(x) for x in re.findall(r"^\[(\d+)\]", refs, re.M)}
print("cited:", sorted(cited))
print("listed:", sorted(have))
print("cited-not-listed:", sorted(cited-have), "| listed-not-cited:", sorted(have-cited))
print("first-appearance order ascending:", order == sorted(order), order)

# --- numbers ---
expected = {
 "88 sites": "88 sites", "63 proteins": "63 proteins",
 "66,790": "66,790", "14,754": "14,754", "22.1": "22.1%",
 "23 of": "15 of the 23", "65.2": "65.2%",
 "1.0e-5": "1.0 × 10⁻⁵", "0.011": "0.011", "0.044": "0.044",
 "0.275": "0.275", "0.154": "0.154", "0.351": "0.351",
 "24-fold": "24-fold", "23%-93%": "23%-93%",
 "0.569": "0.569", "0.603": "0.603", "0.032": "0.032",
 "3.1": "3.1%", "34.1": "34.1%", "0.395": "0.395",
 "74 of": "74 of the 4,748", "1.6": "1.6%",
 "53/128": "53/128", "21/354": "21/354", "5.0e-19": "5.0 × 10⁻¹⁹",
 "power 53": "53% power", "40 sites": "40 such sites",
}
print("\n-- number presence --")
for k, s in expected.items():
    print(("OK  " if s in body else "MISS") + "  " + k + "  <- " + s)

# --- risky wording ---
print("\n-- risky wording --")
for w in ["first ever","novel","unprecedented","comprehensive","complete","always","never","prove","demonstrates","proves","revolution"]:
    hits = [m.start() for m in re.finditer(r"\b"+w+r"\b", body, re.I)]
    if hits:
        for h in hits[:3]:
            print("  "+w+": ..." + " ".join(body[max(0,h-60):h+60].split()))

# --- figures ---
print("\n-- figures --")
for n in [1,2,3,4]:
    print("Figure %d in text: %s | legend: %s" % (n,
        ("Figure %d"%n) in body, ("**Figure %d."%n) in t))

print("\nwords in body:", len(body.split()))