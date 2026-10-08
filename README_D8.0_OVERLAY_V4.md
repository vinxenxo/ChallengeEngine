# C11-D D8.0 — Canonical Inventory Overlay V4

Incremental repair over D7.5 frozen baseline.

## V4 fix

Hardens `run_d8_0_inventory.ps1` for Windows PowerShell 5.1 by normalizing potentially scalar-returning collections to arrays before accessing `.Count`:

- relative-path segments from `Split()`;
- `Get-ChildItem` file collections;
- `Get-Content` line collections.

No D7 authority, C11-C code, production, renderer, or release execution is changed.

Apply over the existing V3/V2 overlay with `Expand-Archive -Force`.
