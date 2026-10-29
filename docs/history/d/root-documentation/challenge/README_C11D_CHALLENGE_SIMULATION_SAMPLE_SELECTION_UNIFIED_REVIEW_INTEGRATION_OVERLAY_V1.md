# C11-D — Sample-selection proposal integration into unified review (V1)

## State

**INTEGRATED_FOR_REVIEW_ONLY / PROPOSED_NOT_APPROVED.** This overlay joins the deterministic sample-selection preview into the existing seven-harness review. It does not apply frame resampling, build renderer input, create media, or clear any gate.

## Contents

- `tools/c11d/d9/d_renderer_unified_content_review.py`: validates the policy preview against the existing runtime `winning_frame`, source/delivery timebases and GAME ranges, confirms the proposed 2:1 even-index cadence, and joins a compact summary into the challenge item.
- `tools/c11d/d9/test_d_renderer_unified_content_review.py`: adds source-lineage, anchor-mismatch and no-approval regression coverage.
- `tools/c11d/d9/run_d_renderer_unified_content_review.py`: reports the updated cross-artifact count and sampling proposal state.
- `definitions/c11d/production/D_RENDERER_UNIFIED_CONTENT_REVIEW_V1.json`: pins the proposal contract into source lineage and explicitly keeps sample selection/interpolation unapproved.
- `definitions/c11d/production/D_RENDERER_UNIFIED_CONTENT_REVIEW_SCHEMA_V1.json`: requires the proposal summary and the additional parity check.
- `docs/current/d/D_RENDERER_CHALLENGE_SAMPLE_SELECTION_UNIFIED_REVIEW_INTEGRATION_CHECKPOINT.md`: current integration record and operator sequence.

## Proposal semantics preserved

- 420 source GAME snapshots at 60 FPS → proposed mapping of 210 delivery GAME frames at 30 FPS.
- Select local source indices `0, 2, 4, ..., 418`; interpolation remains `NONE` in the proposal.
- Reference `winning_frame=394` maps from source absolute frame 574 to delivery absolute frame 287; it remains read-only.
- `close_calls` is count-only.
- The 420 source-timebase visual payload and 420 coordinate-projection records remain unchanged. The 210-entry proposal map is validated in memory and not copied into the output manifest or renderer input.

## Apply and verify from the repository root

```powershell
Get-FileHash "$env:USERPROFILE\Downloads\C11D_CHALLENGE_SIMULATION_SAMPLE_SELECTION_UNIFIED_REVIEW_INTEGRATION_OVERLAY_V1.zip" -Algorithm SHA256
Expand-Archive `
  -LiteralPath "$env:USERPROFILE\Downloads\C11D_CHALLENGE_SIMULATION_SAMPLE_SELECTION_UNIFIED_REVIEW_INTEGRATION_OVERLAY_V1.zip" `
  -DestinationPath "." `
  -Force

python -m py_compile `
  .\tools\c11d\d9\d_renderer_unified_content_review.py `
  .\tools\c11d\d9\test_d_renderer_unified_content_review.py `
  .\tools\c11d\d9\run_d_renderer_unified_content_review.py

python .\tools\c11d\d9\test_d_renderer_challenge_simulation_sample_selection.py
python .\tools\c11d\d9\test_d_renderer_unified_content_review.py
python .\tools\c11d\d9\test_d_renderer_delivery_timebase_projection.py
python .\tools\c11d\d9\test_d_renderer_challenge_delivery_timeline_review.py
python .\tools\c11d\d9\run_d_renderer_unified_content_review.py --godot godot
python .\tools\c11d\d9\test_cross_suite_lifecycle.py
python .\tools\c11d\baseline_candidate\test_d_baseline_candidate.py
python -u .\c11c-suite\self_test.py
```

## Expected review-only state

- Python contract: `cross_checks=11/11`, `source_lineage=14/14`, `negative=12/12`.
- Godot review: `harnesses=7/7`, `cross_artifact=11/11`, `challenge_sampling=420TO210_2:1_PROPOSAL_ONLY`.
- `unresolved_gates=8`; `review=CONSISTENT_NOT_VIDEO_READY`.
- `renderer=OFF`; `media_created=false`; `D4.8=BLOCKED`; `release_authority=NONE`.

A passing proposal-integrity check is not an approval. Do not change the gate count, mark the policy approved, or apply resampling to the visual payload until a separate explicit decision authorizes it.
