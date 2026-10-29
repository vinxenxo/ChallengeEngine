# C11-D Challenge Simulation Sample Selection Proposal Overlay V1

This is a proposal-only overlay for the unresolved source-snapshot selection/interpolation question in the C11-D unified content review.

## New files

- `definitions/c11d/production/D_RENDERER_CHALLENGE_SIMULATION_SAMPLE_SELECTION_PROPOSAL_V1.json`
- `definitions/c11d/production/D_RENDERER_CHALLENGE_SIMULATION_SAMPLE_SELECTION_PREVIEW_SCHEMA_V1.json`
- `tools/c11d/d9/d_renderer_challenge_simulation_sample_selection.py`
- `tools/c11d/d9/test_d_renderer_challenge_simulation_sample_selection.py`
- `docs/current/d/D_RENDERER_CHALLENGE_SIMULATION_SAMPLE_SELECTION_PROPOSAL_CHECKPOINT.md`

## Scope

Only adds the explicit 60→30 FPS reference proposal and a pure in-memory frame-index mapping test. It does not change existing contracts or integrate sample selection into the seven-harness unified review. Therefore `CHALLENGE_SIMULATION_SAMPLE_SELECTION_AND_INTERPOLATION_UNRESOLVED` must remain unresolved pending explicit approval and integration.

## Suggested application/test sequence

```powershell
Get-FileHash "$env:USERPROFILE\Downloads\C11D_CHALLENGE_SIMULATION_SAMPLE_SELECTION_PROPOSAL_OVERLAY_V1.zip" -Algorithm SHA256
Expand-Archive -LiteralPath "$env:USERPROFILE\Downloads\C11D_CHALLENGE_SIMULATION_SAMPLE_SELECTION_PROPOSAL_OVERLAY_V1.zip" -DestinationPath "." -Force
python -m py_compile .\tools\c11d\d9\d_renderer_challenge_simulation_sample_selection.py .\tools\c11d\d9\test_d_renderer_challenge_simulation_sample_selection.py
python .\tools\c11d\d9\test_d_renderer_challenge_simulation_sample_selection.py
```

Then re-run `python .\tools\c11d\d9\run_d_renderer_unified_content_review.py --godot godot`, `python .\tools\c11d\d9\test_cross_suite_lifecycle.py`, `python .\tools\c11d\baseline_candidate\test_d_baseline_candidate.py`, and `python -u .\c11c-suite\self_test.py`.

## Safety/governance

`PROPOSED_NOT_APPROVED`; no renderer input/dispatch/activation; no production execution; no media; frozen C11-C manifest SHA unchanged; `D4.8=BLOCKED`; `release_authority=NONE`; baseline freeze remains blocked.
