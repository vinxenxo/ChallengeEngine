# C11D_RENDERER_EDITORIAL_FIELD_WINDOW_PROPOSAL_OVERLAY_V1

An isolated overlay proposing explicit editorial field visibility windows for `CHALLENGE_004`, using the already verified delivery timeline. Only new files are included.

## Scope and invariants

- `hook` proposes `[0,90)`; empty `reveal` is suppressed and receives no window; `cta` proposes `[390,450)` at `REVIEW_720@30FPS`.
- Intervals are zero-based, half-open delivery-frame ranges.
- The policy is `PROPOSED_NOT_APPROVED`, not renderer input.
- Visual Loops and Visual Drills remain unmapped; this overlay does not invent editorial fields for those types.
- No geometry, typography, animation, simulation sampling, interpolation, audio, renderer dispatch, media, or persistent report is produced.
- C11-C remains immutable; `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`.

## Apply

```powershell
cd C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS
Get-FileHash "$env:USERPROFILE\Downloads\C11D_RENDERER_EDITORIAL_FIELD_WINDOW_PROPOSAL_OVERLAY_V1.zip" -Algorithm SHA256
Expand-Archive -LiteralPath "$env:USERPROFILE\Downloads\C11D_RENDERER_EDITORIAL_FIELD_WINDOW_PROPOSAL_OVERLAY_V1.zip" -DestinationPath "." -Force
(Get-FileHash .\release\C11C_FREEZE_PACKAGE_MANIFEST.json -Algorithm SHA256).Hash
```

Expected frozen manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## Validate the contract

```powershell
python -m py_compile .\tools\c11d\d9\d_renderer_editorial_field_window_proposal.py .\tools\c11d\d9\test_d_renderer_editorial_field_window_proposal.py
python .\tools\c11d\d9\test_d_renderer_editorial_field_window_proposal.py
```

## Run real Godot runtime and invariant check

```powershell
godot --headless --path . --script res://tools/c11d/d9/review_editorial_field_windows_in_memory.gd
```

Expected summary: `fields=3/3`, `visible_windows=2/3`, `hook=[0,90)`, `reveal=EMPTY_SUPPRESSED`, `cta=[390,450)`, `simulation_invariance=PASS`. If Godot does not report PASS, do not update docs and return the exact error.

Only after the Godot harness passes:

```powershell
.\tools\c11d\d9\append_editorial_field_window_proposal_doc_updates.ps1
python .\tools\c11d\d9\test_d_renderer_challenge_delivery_timeline_review.py
python .\tools\c11d\d9\test_d_renderer_profile_identity_separation.py
python .\tools\c11d\d9\test_d_renderer_editorial_review_manifest.py
python .\tools\c11d\d9\test_editorial_render_bridge.py
python .\tools\c11d\d9\test_cross_suite_lifecycle.py
python .\tools\c11d\baseline_candidate\test_d_baseline_candidate.py
python -u .\c11c-suite\self_test.py
```
