# C11-C Bulk Review Tooling — 2.19.4

## Canonical Art Direction runner

`run_c11c_art_direction_batch_v4.ps1` is the active 27-loop / 20-drill / 5-longform review orchestrator.

`-Workers 7` is a real concurrency contract. Loop captures are assigned to separate temporary Godot project roots, each with private Movie Maker `override.cfg` and `.godot` state. A project-global mutex is deliberately not used.

The worker pool excludes generated `artifacts/`, `.godot/`, `.git/`, caches and retired `c11c-studio/` from its project copies. Each worker reports its slot and root, and the batch records maximum observed worker concurrency.

Historical runner variants remain evidence. New operational changes should target the canonical `run_c11c_art_direction_batch_v4.ps1` and related Suite surfaces.
