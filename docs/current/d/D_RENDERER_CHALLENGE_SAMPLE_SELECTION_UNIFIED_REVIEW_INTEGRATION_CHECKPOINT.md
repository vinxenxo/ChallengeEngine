# C11-D — Challenge sample-selection proposal in unified review

**State: `INTEGRATED_FOR_REVIEW_ONLY / PROPOSED_NOT_APPROVED`.**

## What changed

The seven-harness unified review now includes a deterministic in-memory preview built from `D_RENDERER_CHALLENGE_SIMULATION_SAMPLE_SELECTION_PROPOSAL_V1.json`. The proposal contract is pinned in the unified review source lineage. The coordinator cross-checks source/delivery FPS and durations, source and delivery GAME ranges, the runtime `winning_frame`, the even-index 2:1 sample cadence, the exact selected anchor, `close_calls` count-only semantics, no interpolation, and the no-mutation/no-renderer boundary.

The joined Challenge item emits a compact policy/preview summary, **not** the 210-row map and not renderer-native input. The original Challenge visual payload remains 420 source-timebase records at 60 FPS; its `delivery_resampling` remains `UNRESOLVED_NOT_APPLIED`. The new check establishes proposal parity, not application or policy approval.

## Expected reference mapping

- Source: 420 GAME snapshots at 60 FPS, source absolute range `[180, 600)`.
- Proposed delivery: 210 GAME frames at 30 FPS, delivery absolute range `[90, 300)`.
- Cadence: source GAME local indices `0, 2, 4, ..., 418`; no interpolation or synthetic states.
- `winning_frame=394` remains read-only and maps from source absolute frame `574` to delivery absolute frame `287`.
- `close_calls=1` remains a count, never a timing source.

## Acceptance and governance

Expected Python output: `cross_checks=11/11`, `source_lineage=14/14`, `negative=12/12`. The Godot coordinator still runs seven existing harnesses; no eighth harness is added. The overall review remains `CONSISTENT_NOT_VIDEO_READY` with eight unresolved gates. In particular, `CHALLENGE_SIMULATION_SAMPLE_SELECTION_AND_INTERPOLATION_UNRESOLVED` remains open because a proposal in a review report is not an explicit approval.

Must remain: `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`; no Godot/FFmpeg renderer dispatch; no changes to C11-C simulation state, RNG, `SimulationResult`, `winning_frame`, `close_calls`, canonical payloads, or frozen manifest.

## Windows verification

```powershell
python -m py_compile .\tools\c11d\d9\d_renderer_unified_content_review.py .\tools\c11d\d9\test_d_renderer_unified_content_review.py .\tools\c11d\d9\run_d_renderer_unified_content_review.py
python .\tools\c11d\d9\test_d_renderer_challenge_simulation_sample_selection.py
python .\tools\c11d\d9\test_d_renderer_unified_content_review.py
python .\tools\c11d\d9\run_d_renderer_unified_content_review.py --godot godot
python .\tools\c11d\d9\test_cross_suite_lifecycle.py
python .\tools\c11d\baseline_candidate\test_d_baseline_candidate.py
python -u .\c11c-suite\self_test.py
```

Passing these tests verifies the integration contract only. Explicit human/design policy approval remains an external step; no gate is cleared by this overlay.
