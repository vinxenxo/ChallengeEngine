# C11-D D7.5 Overlay — Full D7 Acceptance

Root-relative additive overlay for the immutable C11-C 2.19.12 baseline and completed D7.0-D7.4 chain.

This overlay adds only D7.5 acceptance definitions, builder/runner/closure tooling, and documentation/prompts.

D7.5 validates predecessor evidence; it does not rewrite D7.0-D7.4 artifacts. It writes exactly four evidence JSON files under:

`artifacts/tests/c11d_d7/d7_5/`

The mutation guard excludes only that evidence directory. Python bytecode generation is disabled for the acceptance process. `release/` must not be created or modified.

No C11-C simulation, mechanics, RNG, presentation, renderer, or production execution is modified or activated.


## V2 PS5.1 repair

The D7.5 runner no longer uses `foreach` inside a parenthesized expression. Evidence hash aggregation uses ordinary PowerShell 5.1-compatible arrays and loops.


## V3 hardening

D7.5 does not assume a fixed active path for `build_factory.py`. The acceptance builder discovers active candidates by filename, excludes generated/archive trees, and requires exactly one candidate whose SHA-256 matches the frozen C11-C identity. Zero matches, stale matches, or ambiguous multiple matches are blockers.

The mutation guard remains strict: only `artifacts/tests/c11d_d7/d7_5/` is writable evidence. Applying an overlay before the runner starts does not become an allowed mutation; all overlay files are part of the baseline snapshot and any post-baseline change outside `d7_5` fails the guard.
