# C11-D Visual Loop Grammar Parameter Instance Overlay V1

Advisory D-owned overlay, additive only. Adds a request-bound in-memory parameter instance for the single pinned selector `visual_loops / c11c_geometric_waves_v1 / harmonic_membrane`.

## Files

- Contract + strict schemas for probe input and final receipt.
- Python runner and a Godot headless probe.
- Unit/contract test and a checkpoint.

## Important boundary

This adds a grammar-specific parameter instance, **not** an exact selector visual payload and not renderer input. The pre-existing D9 dynamic request contract must continue to say the Visual Loop exact selector payload is unresolved. All renderer/media/release gates remain closed.

## How to run

From the repository root, use the copy/paste PowerShell commands provided with the overlay delivery. First run the Python contract test; then run the actual Godot 4.7.1 matrix; only after both pass run the selected regressions.

## Preparation validation

- Contract test currently passes `15/15` in the preparation tree.
- Neighbor contracts also pass locally: grammar audit `14/14`, dynamic request binding `12/12`, request-scoped materialization `9/9`, candidate I/O contract, and unified review `36/36`.
- The new real-Godot matrix was not run in the preparation environment. Run it in the Windows checkout with the console executable for Godot `4.7.1.stable.mono.official.a13da4feb` before treating this checkpoint as runtime-verified.
- The report never represents this separate parameter instance as the canonical exact visual payload. `exact_selector_visual_payload_materialized=false` and `family_authoring_envelope_gap=REMAINS_OPEN` remain deliberate.
