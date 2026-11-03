
import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"C:\Users\Administrator\Desktop\丙酮酰化\08_manuscript_v1.md"
t = open(p, encoding="utf-8").read()
body = t.split("## References")[0]
# split sentences
sents = re.split(r"(?<=[.;:])\s+", body)
hedges = {
 "cannot/can not": r"\bcannot\b|\bcan not\b",
 "do not claim": r"\bdo not claim\b|\bwe do not\b",
 "does not": r"\bdoes not\b",
 "not that it is": r"\bnot that it\b",
 "must be read": r"\bmust be\b",
 "should be treated": r"\bshould be\b",
 "only": r"\bonly\b",
 "never/always(hedged)": r"\balmost never\b|\balmost always\b",
 "argues against": r"\bargues? against\b",
 "we did not find": r"\bwe did not find\b",
 "as of our search": r"\bas of our\b",
 "suggest/infer": r"\bsuggest|\binfer",
}
print("words:", len(body.split()))
hits = {}
for name, rx in hedges.items():
    m = [s for s in sents if re.search(rx, s, re.I)]
    hits[name] = len(m)
print("\n-- hedge counts --")
for k, v in sorted(hits.items(), key=lambda x: -x[1]):
    if v: print("  %-22s %d" % (k, v))
print("\n-- sentences carrying self-limitation --")
for s in sents:
    if re.search(r"\b(cannot|do not|does not|not that it|must be read|should be treated|did not find|as of our)\b", s, re.I):
        print("  • " + " ".join(s.split())[:230])
