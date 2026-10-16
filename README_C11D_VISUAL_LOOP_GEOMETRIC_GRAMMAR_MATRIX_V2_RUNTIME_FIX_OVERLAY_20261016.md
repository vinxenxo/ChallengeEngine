# C11-D Visual Loop Geometric Grammar Matrix V2 — Runtime Validator Fix

## Purpose

This overlay fixes a real Godot runtime rejection seen after Godot 4.7.1 had already launched the V2 probe. The failure was raised by `_validate_input()` at the recursive `Dictionary` comparison of each deserialized JSON matrix row against a GDScript literal. It was **not** an executable-path failure: Godot reported the expected version and executed the probe.

The validator now compares the row's exact key set and each typed field. For `grammar_index`, it accepts an integer or float JSON representation only when its finite numeric value exactly matches the pinned index. A malformed number, wrong grammar ID/branch, extra key, missing key, or wrong index still fails closed. The contract's source-lineage SHA for the changed GDScript is updated accordingly. A focused regression prevents reintroduction of the old recursive comparison.

## Scope

- Replaces the V2 GDScript probe, V2 contract JSON (only to update the source pin), and V2 Python test.
- Adds the dated runtime-fix checkpoint.
- Does not change `d_renderer_visual_loop_geometric_grammar_matrix_v2.py`, schemas, C11-C files or manifest, canonical D9.9/D9.10 request selection, renderer flags, or release authority.
- Remains preparation-only. This overlay does not claim a real Godot runtime PASS; that must be demonstrated on the active Windows checkout.

## Application

1. Put this ZIP in `C:\Users\vinxe\Downloads`.
2. Start PowerShell in `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`.
3. Run the user-provided guarded application block from the assistant response. It verifies ZIP SHA, the frozen C11-C manifest, all existing-file precondition hashes, and absence of additive destinations before extraction/copy.
4. Run the 12-test Python contract test separately.
5. Run the real Godot V2 audit separately. Accept PASS only when exit code is 0 and its success receipt/summary is present. Never type or run a standalone success print after an exception.

## Governance

`renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`, `baseline_approval=MISSING`, `freeze_eligible=false`, `D9.17=BLOCKED_NO_GO`, `D9.10=PREPARE_ONLY`, and `D10=BLOCKED_FOR_PROMOTION` remain unchanged.
