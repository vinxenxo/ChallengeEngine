# C11D D7.4 Overlay — Catalog Identity / Provenance

Minimal root-relative overlay for the immutable C11-C 2.19.12 baseline and completed D7.3 canonical catalog.

This overlay adds only D7.4 specifications, validation tooling, stage handover documentation, and master/start prompts.

No C11-C simulation, mechanics, RNG, presentation, renderer, or production execution is modified.

The D7.4 runner writes exactly four evidence files under:

`artifacts/tests/c11d_d7/d7_4/`

The mutation guard excludes only that evidence directory from the repository snapshot. `release/` is not written by D7.4.
