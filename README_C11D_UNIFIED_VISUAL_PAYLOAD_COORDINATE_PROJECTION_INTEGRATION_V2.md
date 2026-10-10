# C11-D Unified Visual Payload and Coordinate Projection Integration V2

This is a minimal overlay for the existing `ChallengeEngineV01_STATELESS` checkout. It does not contain a full repository copy and does not modify the frozen C11-C source package.

## What changes

- Extends `run_d_renderer_unified_content_review.py` from five to seven sequential Godot 4.7.1 headless in-memory harnesses.
- Adds the Challenge source-timebase visual payload preview and the coordinate projection preview to the unified cross-artifact join.
- Requires the coordinate projection source-frame digest to equal the visual payload's `SimulationResult.frames` record digest for the same 420 GAME records.
- Verifies the three source SVG identities and confirms that projection remains `PROPOSED_NOT_APPROVED`, with delivery resampling/interpolation unresolved.
- Replaces the coordinate-projection documentation updater with an ASCII-only Windows PowerShell 5.1-compatible version. The previous updater included Unicode arrows in single-line PowerShell declarations, which caused a parser error on the user's Windows host.
- Adds an idempotent documentation updater for the 7-harness integration.

## Apply

From the repository root in PowerShell:

```powershell
Get-FileHash "$env:USERPROFILE\Downloads\C11D_RENDERER_UNIFIED_VISUAL_PAYLOAD_COORDINATE_PROJECTION_INTEGRATION_V2.zip" -Algorithm SHA256
Expand-Archive -LiteralPath "$env:USERPROFILE\Downloads\C11D_RENDERER_UNIFIED_VISUAL_PAYLOAD_COORDINATE_PROJECTION_INTEGRATION_V2.zip" -DestinationPath "." -Force
```

Verify the frozen C11-C manifest SHA-256 remains:

`e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`

## Validate

```powershell
python -m py_compile `
  .\tools\c11d\d9\d_renderer_unified_content_review.py `
  .\tools\c11d\d9\run_d_renderer_unified_content_review.py `
  .\tools\c11d\d9\test_d_renderer_unified_content_review.py

python .\tools\c11d\d9\test_d_renderer_unified_content_review.py
python .\tools\c11d\d9\run_d_renderer_unified_content_review.py --godot godot
```

The contract output should report `harness_contracts=7/7`, `cross_checks=10/10`, and `source_files=13/13` on the complete checkout. The Godot coordinator should report `harnesses=7/7`, `cross_artifact=10/10`, and `challenge_visual=420@60FPS_PROJECTED_420_RECORDS`.

After the unified coordinator returns a clean PASS, update documentation additively:

```powershell
.\tools\c11d\d9\append_coordinate_projection_doc_updates.ps1
.\tools\c11d\d9\append_unified_visual_payload_coordinate_projection_doc_updates.ps1
```

Then run the usual regression:

```powershell
python .\tools\c11d\d9\test_cross_suite_lifecycle.py
python .\tools\c11d\baseline_candidate\test_d_baseline_candidate.py
python -u .\c11c-suite\self_test.py
```

## Governance

The Challenge logical visual payload and coordinate projection remain in-memory review artifacts, not renderer-native input. Coordinate projection and timebase policies remain proposed, sample selection/interpolation remains unresolved, renderer activation remains OFF, no media is produced, `D4.8=BLOCKED`, and `release_authority=NONE`. This overlay does not assert D baseline approval or freeze eligibility.
