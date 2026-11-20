# Release v1.3.4 — re-publish of v1.3.3 to trigger archiving

Date: 2026-11-20

## Why this release exists

v1.3.3 (commit `48b0038`) added `artifacts/cplm_provenance.csv` and the
"Data provenance" section of the README. Its GitHub release was published but
no corresponding Zenodo version was archived, so the deposit still resolves to
v1.3.2. Publishing a new release is the only way to re-trigger the Zenodo
GitHub integration; moving or re-pointing the existing tag would rewrite an
archived snapshot, which this repository does not do.

## What is in this release

**No analytical results changed.** Every script, table and number is identical
to v1.3.3 (commit `48b0038`). The only file added is this note.

The content of the deposit is therefore:

- `artifacts/cplm_provenance.csv` — one row per downloaded CPLM archive, with
  source URL, archive size and SHA-256, the extracted member actually read, and
  that member's SHA-256. All ten extracted files were verified byte-identical to
  their archive members.
- README, "Data provenance" — field semantics, including the statement that
  `download_date` is the local file-creation date and not an independently
  verified download date, and that ZIP-internal timestamps are not used.

## Tag history

| Tag | Commit | Content |
|---|---|---|
| v1.3.2 | `294579e` | leave-one-out comparison row corrected; S1/S4 recomputed |
| v1.3.3 | `48b0038` | CPLM archive provenance manifest added |
| v1.3.4 | this commit | re-publish of v1.3.3; no content change |
