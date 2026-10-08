# C11-D D7.3 Runner Format/Mutation Guard Fix V2

Minimal root-relative overlay for the C11-D D7.3 runner.

## What changes

`tools/c11d/d7/run_d7_3_canonical_catalog.ps1` now excludes the entire D7.3 evidence directory from the repository-wide mutation hash by temporarily moving that directory outside the worktree during each snapshot. The evidence directory is still checked separately for exactly four JSON evidence files and deterministic SHA-256 output.

The previous format-string repair is retained.

## Expected result

Two consecutive executions should finish with:

`C11-D D7.3 - PASS / CLOSED`

and:

`NEXT: D7.4 - Catalog Identity / Provenance`

No production execution, renderer execution, seed generation, or C11-C simulation code is changed.
