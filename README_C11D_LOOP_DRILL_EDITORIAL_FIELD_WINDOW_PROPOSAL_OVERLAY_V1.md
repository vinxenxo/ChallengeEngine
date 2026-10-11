# C11-D Loop/Drill Editorial Field-Window Proposal Overlay V1

## Scope

Six **new-only** files proposing and testing a temporal visibility rule for Visual Loop and Visual Drill universal editorial fields. No existing file is overwritten. This proposal is separate from the existing Challenge-only field-window proposal.

## Contract

`definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json`

The proposal binds to the exact source lineages in the frozen C11-C manifest and the existing D visual-payload, editorial-review, logical-composition, neutral-frame-program, temporal-bound and Challenge field-window contracts.

## Rule submitted for review

- `title`, `subtitle`, and `call_to_action`: full continuous span `[0, frame_count)` when non-empty.
- Empty visual values: suppressed; no window.
- `language`: metadata only; no visibility window.
- No inferred loop-cycle/drill-exercise subphases, text transformations, style rules, coordinates or renderer input.
- Use the actual request-scoped in-memory payload instance `frame_count` as authority.
- State remains `PROPOSED_NOT_APPROVED`; the validator rejects approval-state promotion and renderer/media activation.

## Verification performed in preparation workspace

- Python syntax compilation: PASS.
- Unit tests: **22/22 PASS**.
- Source lineage: exact pinned set (10/10). All source hashes were read from the source files staged for this verification.
- ZIP integrity and exact six-file allowlist are checked after packaging.

This package-preparation result does not claim the user's full checkout or Godot runtime was executed. Run the included tests in Windows after extraction.

## Apply from repository root

```powershell
Get-FileHash "$env:USERPROFILE\Downloads\C11D_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_OVERLAY_V1.zip" -Algorithm SHA256
Expand-Archive -LiteralPath "$env:USERPROFILE\Downloads\C11D_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_OVERLAY_V1.zip" -DestinationPath "." -Force
python -m py_compile .\tools\c11d\d9\d_renderer_loop_drill_editorial_field_windows.py .\tools\c11d\d9\test_d_renderer_loop_drill_editorial_field_windows.py
python .\tools\c11d\d9\test_d_renderer_loop_drill_editorial_field_windows.py
```

## Governance boundary

Proposal only. Do not edit `D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json` or the existing unified review coordinator in this overlay. Do not clear the two unresolved loop/drill field-mapping gates merely because this proposal test passes. Renderer OFF, no media, D4.8 BLOCKED, release authority NONE, and the frozen C11-C manifest SHA-256 remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
