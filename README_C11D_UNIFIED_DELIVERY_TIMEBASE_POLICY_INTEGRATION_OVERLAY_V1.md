# C11-D Unified delivery-timebase proposal integration overlay V1

## SHA-256

Computed for the packaged ZIP after all contents are finalized; verify the downloaded ZIP with `Get-FileHash` before extraction.

## What this overlay does

- Adds the source-pinned proposal `D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json` and strict JSON Schema.
- Adds a review-only validator/test module for a shared `REVIEW_720` 30 FPS target profile.
- Defines distinct timing rules per content type: identity/no resampling for 30 FPS Loops and Drills; proposed cumulative-boundary projection and separately proposed GAME sampling for 60 FPS Challenges.
- Integrates `unified_delivery_policy_parity` into the existing unified review. No Godot harness is added.
- Updates current/history docs for this milestone.

## Scope and invariants

It does not apply resampling, materialize delivery samples, create media, define music/audio processing, activate/dispatch the renderer, approve a policy, or grant baseline/D4.8/release authority. C11-C and `release/C11C_FREEZE_PACKAGE_MANIFEST.json` are immutable. The unified review's eight gates remain open.

## Windows apply and test sequence

Run once from the repository root:

```powershell
Get-FileHash "$env:USERPROFILE\Downloads\C11D_UNIFIED_DELIVERY_TIMEBASE_POLICY_INTEGRATION_OVERLAY_V1.zip" -Algorithm SHA256
Expand-Archive -LiteralPath "$env:USERPROFILE\Downloads\C11D_UNIFIED_DELIVERY_TIMEBASE_POLICY_INTEGRATION_OVERLAY_V1.zip" -DestinationPath "." -Force

python -m py_compile `
  .\tools\c11d\d9\d_renderer_unified_delivery_timebase_policy.py `
  .\tools\c11d\d9\test_d_renderer_unified_delivery_timebase_policy.py `
  .\tools\c11d\d9\d_renderer_unified_content_review.py `
  .\tools\c11d\d9\test_d_renderer_unified_content_review.py

python .\tools\c11d\d9\test_d_renderer_unified_delivery_timebase_policy.py
python .\tools\c11d\d9\test_d_renderer_unified_content_review.py
python .\tools\c11d\d9\test_d_renderer_delivery_timebase_projection.py
python .\tools\c11d\d9\test_d_renderer_challenge_temporal_alignment_policy.py
python .\tools\c11d\d9\run_d_renderer_unified_content_review.py --godot godot
python .\tools\c11d\d9\test_cross_suite_lifecycle.py
python .\tools\c11d\baseline_candidate\test_d_baseline_candidate.py
python -u .\c11c-suite\self_test.py
```

Expected integration indicators: `cross_artifact=15/15`, `source_lineage=18/18`, `unified_delivery_policy_parity=true`, `unresolved_gates=8`, `REVIEW_CHAIN_CONSISTENT_NOT_VIDEO_READY`, `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`.
