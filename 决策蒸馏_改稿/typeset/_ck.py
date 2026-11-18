
import hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
a = r"C:\Users\Administrator\Desktop\丙酮酰化\决策蒸馏_改稿\typeset\render_out2"; b = r"C:\Users\Administrator\Desktop\丙酮酰化\决策蒸馏_改稿\typeset\render_final"
for i in range(1, 13):
    n = "page-%04d.png" % i
    ha = hashlib.sha256(open(os.path.join(a, n), "rb").read()).hexdigest()[:16]
    hb = hashlib.sha256(open(os.path.join(b, n), "rb").read()).hexdigest()[:16]
    print(n, "out2", ha, "final", hb, "SAME" if ha == hb else "DIFF")
