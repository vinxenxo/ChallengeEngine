# C11D D7.3 Overlay

Apply this root-relative overlay to the current C11-D workspace.

D7.3 builds the canonical catalog from the closed D7.1 matrix and D7.2 validation.

It does not write to `release/`. Evidence is generated only under:

`artifacts/tests/c11d_d7/d7_3/`

Run:

`tools/c11d/d7/run_d7_3_canonical_catalog.ps1`

Run twice. Only after PASS/CLOSED execute:

`tools/c11d/d7/close_d7_3_handover.ps1`
