# Release v1.3.2 — correction to the leave-one-out comparison set

Date: 2026-11-18

## What was wrong in v1.3.1

`tools/leave_one_out.py` placed lysines that carry the query modification and
no other modification into the comparison row. The query row required at least
one other modification; the comparison row did not. Those sites have an outcome
of zero by construction, so the comparison row was diluted with structural
non-events and every Mantel-Haenszel odds ratio was inflated.

The crude column of Table S4 was computed by a different script that already
excluded those sites, so it was unaffected. Only the stratified column, and
everything derived from it, carried the error.

## What changed

`if y and others == 0: continue` — lysines carrying the query modification
alone now enter neither row. Everything in Table S1, Table S4 and the text
depends on that line and was recomputed.

| Modification | v1.3.1 OR | v1.3.2 OR |
|---|---:|---:|
| Acetylation | 11.13 | 2.13 |
| Crotonylation | 5.19 | 4.58 |
| 2-Hydroxyisobutyrylation | 4.68 | 4.44 |
| Malonylation | 2.78 | 2.64 |
| Succinylation | 3.35 | 3.24 |
| Butyrylation | 16.48 | 16.48 |
| Lactylation | 5.67 | 5.44 |
| Glutarylation | 1.97 | 1.39 |
| Propionylation | 65.12 | 64.62 |
| Pyruvylation (Kpy) | 2.60 | 2.60 |

The Kpy row is unchanged: its sites lie outside the catalogue, so no site of
its own could enter the comparison row. The paper's conclusions about
pyruvylation therefore do not depend on the correction; the comparison across
modifications does — the median falls from 5.19 to 4.44 and pyruvylation moves
from second to third lowest of the ten.

## Consequential changes elsewhere

- Spearman correlations involving the stratified-to-crude ratio were recomputed.
  The relation with catalogue size is now rho = -0.75 (n = 9); the relation with
  the multi-modification rate is +0.21 (n = 7) and is no longer used.
- Power was re-derived by exact enumeration rather than Monte Carlo. At the
  observed design the z test and the probability-ordered exact test share the
  same rejection region, so the two give the same power; that equivalence is
  reported in Methods and does not extend to the scaled designs.
- The literature check now reports 35 records from the 40 primary studies,
  merged to 33 studies after two preprints were matched to their published
  versions (37398265/37723562 and 40462961/40948406). Five records remain
  unobtainable and are listed in artifacts/unobtainable.md.

## How to verify

    python verify.py

`VERIFY.md` lists the five commands. The Table S1 row for acetylation is the
fastest check of the correction: it must return 2.13, not 11.13.
