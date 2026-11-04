"""Structural guard for the manuscript source.

Run after any edit. Fails loudly instead of letting a damaged file be built.
"""
import os
import re
import sys

MD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "08_manuscript_v1.md")


def main():
    text = open(MD, encoding="utf-8").read()
    problems = []

    if "(line truncated" in text:
        problems.append("truncation marker present: %d" % text.count("(line truncated"))

    lines = text.split("\n")
    longest = max(len(l) for l in lines)
    if longest > 2000:
        print("note: a line is %d chars, longer than the 2000-char read window; "
              "never load and rewrite this file whole, use targeted edits" % longest)

    sections = [l for l in lines if l.startswith("## ")]
    expected = ["## Title", "## Abstract", "## Introduction", "## Results", "## Discussion",
                "## Methods", "## Declarations", "## References", "## Tables", "## Figure legends"]
    if sections != expected:
        problems.append("section list changed: %s" % sections)

    results = re.findall(r"^### (\d)\.", text, flags=re.M)
    if results != ["1", "2", "3", "4", "5"]:
        problems.append("Results numbering broken: %s" % results)

    legends = re.findall(r"\*\*(?:Supplementary )?Figure [0-9S]+\.", text)
    if len(legends) != 5:
        problems.append("expected 5 figure legends, found %d: %s" % (len(legends), legends))

    tables = re.findall(r"\*\*Table [0-9S]+\.", text)
    if len(tables) != 4:
        problems.append("expected 4 table captions, found %d" % len(tables))

    abstract = re.search(r"## Abstract\n\n(.+?)\n", text)
    if abstract:
        n = len(abstract.group(1).split())
        if n > 200:
            problems.append("abstract is %d words" % n)

    if problems:
        print("MANUSCRIPT GUARD FAILED")
        for p in problems:
            print("  -", p)
        return 1
    print("manuscript guard: ok (sections 10, Results 1-5, legends 5, tables 4, abstract %d words, longest line %d)"
          % (n, longest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
