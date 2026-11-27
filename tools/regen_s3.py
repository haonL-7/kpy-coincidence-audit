
"""Generate standalone Table S3 from the archived, adjudicated coding sheets."""
import argparse
import csv
import os
from collections import Counter
from pathlib import Path

B = Path(os.environ.get("KPY_BASE") or Path(__file__).resolve().parents[1])
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output", type=Path, default=B / "artifacts" / "Table_S3.md",
                    help="output Markdown path (default: artifacts/Table_S3.md)")
args = parser.parse_args()

with (B / "artifacts" / "coding.csv").open(encoding="utf-8-sig", newline="") as handle:
    rows = list(csv.DictReader(handle))
DROP = {"37398265", "40462961"}  # preprints merged with their published versions
prim = [r for r in rows if r["C1_expected_set"] != "not assessable" and r["pmid"] not in DROP]
with (B / "artifacts" / "reviews_coding_final.csv").open(encoding="utf-8-sig", newline="") as handle:
    rev = list(csv.DictReader(handle))
for records in (prim, rev):
    if len({r["pmid"] for r in records}) != len(records):
        raise ValueError("Duplicate PMID after preprint exclusion")
L = []
A = L.append
A("**Table S3.** Reporting practice in the papers behind this argument. (A) Primary crosstalk studies for which verified full text was obtained (35 records from 40 primary studies; two are preprints merged with their published versions, leaving 33 studies; the other 5 had no accessible copy). C1 asks whether the paper states the expectation against which its coincidence statistic is judged; C2 whether protein composition is aligned across any two sets or condition groups the paper compares; C3 whether statistical power is quantified. Each item is asked only of the papers to which it applies, so the three have different bases: C1 of 19, C2 of 19, C3 of 31. For C1, the overlap unit was modified proteins in six of the 19 applicable studies and modification sites in the remaining thirteen. Fourteen studies reported no applicable modification overlap statistic: ten examined a single protein (nine followed two marks and one characterized a single mark in vitro), two compared gene lists, and two compared condition groups without computing an overlap.")
A("")
A("C3 is asked of every paper that reports a quantitative result from replicated measurements or a group comparison, whether or not it computes an overlap; partial means the paper flags a limitation of replication, sampling or resolution that bears on what it can detect, without quantifying it, and no means it reports such results without any such statement. Coding decisions, available supporting quotations and recorded source locations are provided in the deposited coding sheets. Papers were coded from their published text alone and their authors were not asked to clarify; the absence of a stated expectation describes reporting in the reviewed studies and should not be interpreted as an oversight in any individual study.")
A("")
A("**(A) Primary studies**")
A("")
A("| PMID | Year | Journal | Type | C1 | C2 | C3 |")
A("|---|---|---|---|---|---|---|")
for r in sorted(prim, key=lambda x: (x["year"], x["pmid"])):
    A("| %s | %s | %s | %s | %s | %s | %s |" % (r["pmid"], r["year"], r["journal"].replace("|","/"),
        r["study_type"].replace("|","/"), r["C1_expected_set"], r["C2_composition"], r["C3_power"]))
A("")
A("")
A("(B) Reviews from the same search. Evidence graded records whether the review assigns a level to the crosstalk evidence it surveys; Reporting gap noted records whether it names a methodological or reporting deficiency; Expectation gap noted records whether that deficiency is the absence of a stated expectation behind a coincidence statistic. The last was assessed on the full text: each of the nine was searched for a statement about the expectation, background or comparison set against which an overlap should be judged, and no explicit statement identifying an unspecified reference expectation as a reporting gap in coincidence analyses was identified.")
A("**(B) Reviews**")
A("")
A("| PMID | Year | Journal | Evidence graded | Reporting gap noted | Expectation gap noted |")
A("|---|---|---|---|---|---|")
for r in sorted(rev, key=lambda x: (x["year"], x["pmid"])):
    A("| %s | %s | %s | %s | %s | %s |" % (r["pmid"], r["year"], r["journal"].replace("|","/"),
        r["crosstalk_evidence_graded"], r["reporting_norm_gap_noted"], r["expectation_gap_noted"]))
block = chr(10).join(L) + chr(10)
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(block, encoding="utf-8")
print("table rows: primary", len(prim), "| reviews", len(rev))
for field in ("C1_expected_set", "C2_composition", "C3_power"):
    counts = Counter(r[field] for r in prim)
    applicable = sum(counts[value] for value in ("yes", "partial", "no"))
    print(f"{field}: applicable={applicable}, no={counts['no']}, "
          f"partial={counts['partial']}, yes={counts['yes']}, NA={counts['NA']}")
print("written:", args.output)
