
import math, json
def hyper_two_sided(a, b, c, d):
    n = a+b+c+d; r1 = a+b; c1 = a+c
    lo, hi = max(0, c1-(n-r1)), min(r1, c1)
    def pmf(x): return math.comb(c1, x)*math.comb(n-c1, r1-x)/math.comb(n, r1)
    obs = pmf(a); tot = 0.0
    for x in range(lo, hi+1):
        p = pmf(x)
        if p <= obs*(1+1e-7): tot += p
    return tot
tests = {
 "histone  (Kpy 9/10 vs 371/756)": (9,1,371,385),
 "non-hist (Kpy 6/13 vs 14383/51651)": (6,7,14383,51651),
 "all      (Kpy 15/23 vs 14754/66767)": (15,8,14754,52013),
}
for k,(a,b,c,d) in tests.items():
    print("%-38s p = %.5f" % (k, hyper_two_sided(a,b,c,d)))
try:
    import scipy; print("scipy:", scipy.__version__)
except Exception as e:
    print("scipy: not installed")
# crude power: 2x enrichment over non-hist background 0.218, alpha .05 one-sided, power .8
p0 = 0.218; p1 = 2*p0
for n in (13, 25, 40, 60):
    from math import comb
    crit = None
    for x in range(1, n+1):
        if sum(comb(n,k)*p0**k*(1-p0)**(n-k) for k in range(x, n+1)) <= 0.05:
            crit = x; break
    pw = sum(comb(n,k)*p1**k*(1-p1)**(n-k) for k in range(crit, n+1)) if crit else 0
    print("n_annotated=%2d  crit=%s  power@2x=%.2f" % (n, crit, pw))
