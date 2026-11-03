#!/usr/bin/env python3
"""Confirm that an unpacked archive reproduces the numbers in the manuscript.

Usage:  python verify.py
Exit code 0 when every check passes, 1 otherwise.
Runs on Windows, macOS and Linux; needs only numpy and pandas.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# Each check lists required literal substrings, then (label, expected, tolerance)
# triples for numbers that come out of a Monte Carlo run and cannot be exact.
CHECKS = [
    ("exact conditional estimate", "tools/exact_ci.py",
     ["MH OR = 2.60", "0.224", "0.60 - 10.25"], []),
    ("leave-one-out across nine acylations", "tools/leave_one_out.py",
     ["1.97 - 65.12", "OR=2.60"], []),
    ("power across effect sizes", "tools/power_scale.py",
     ["power at OR 2.60", "power at OR 5.19", "power at OR 10.25"],
     [("power at OR 5.19", r"power at OR 5\.19 = ([\d.]+)", 0.50, 0.05),
      ("power at OR 10.25", r"power at OR 10\.25 = ([\d.]+)", 0.80, 0.05)]),
    ("power at the observed effect size", "tools/power_sim.py",
     ["power at OR 2.6"],
     [("power at OR 2.6 (23 sites)", r"x1 \(n~23\): power at OR 2\.6 = ([\d.]+)", 0.18, 0.05),
      ("power at 92 sites", r"x4 \(n~92\): power at OR 2\.6 = ([\d.]+)", 0.56, 0.05)]),
]


def main():
    if not os.path.isdir(os.path.join(HERE, "tools")):
        print("No tools directory next to this script, so the archive has not been")
        print("extracted here. Expected contents after extraction:")
        print("  CITATION.cff  LICENSE  README.md  VERIFY.md  data  figs  requirements.txt  tools")
        print("Present instead:", sorted(os.listdir(HERE))[:10])
        return 1

    try:
        import numpy  # noqa: F401
        import pandas  # noqa: F401
    except ImportError as exc:
        print("Missing dependency: %s. Install requirements.txt first." % exc)
        return 1

    env = dict(os.environ, PYTHONIOENCODING="utf-8", KPY_BASE=HERE)
    failures = 0
    for label, script, expected, numeric in CHECKS:
        path = os.path.join(HERE, script)
        if not os.path.exists(path):
            print("== %s ==" % label)
            print("  MISSING: %s" % script)
            failures += 1
            continue
        proc = subprocess.run([sys.executable, path], capture_output=True, text=True,
                              env=env, cwd=HERE, errors="replace")
        out = (proc.stdout or "") + (proc.stderr or "")
        print("== %s ==" % label)
        print("\n".join(out.strip().splitlines()[-6:]))
        missing = [m for m in expected if m not in out]
        off = []
        for name, pattern, want, tol in numeric:
            hit = re.search(pattern, out)
            if not hit:
                off.append("%s: line not found" % name)
            elif abs(float(hit.group(1)) - want) > tol:
                off.append("%s: got %s, expected about %.2f" % (name, hit.group(1), want))
        if missing or off:
            print("  FAIL: %s" % "; ".join(missing + off))
            failures += 1
        else:
            print("  PASS: %s" % label)
        print()

    if failures:
        print("%d check(s) failed: this archive does not reproduce the manuscript." % failures)
        return 1
    print("All %d checks pass: this archive reproduces the reported numbers." % len(CHECKS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
