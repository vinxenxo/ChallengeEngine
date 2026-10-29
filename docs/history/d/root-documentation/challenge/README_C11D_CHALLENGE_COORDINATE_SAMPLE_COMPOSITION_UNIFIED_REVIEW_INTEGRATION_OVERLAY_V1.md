# C11-D Coordinate + Sample Composition — Unified Review Integration Overlay V1

## Purpose

Integrate the existing coordinate/sample composition proposal into the unified content-review manifest as a proposal-only cross-artifact parity check. The overlay does not materialize composed records, emit renderer input, generate media, approve policies, or alter C11-C.

## Apply target

Apply this ZIP to the current full Windows checkout at the repository root:

`C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`

Extract with `Expand-Archive -DestinationPath . -Force`. It contains seven new/modified files only:

- `definitions/c11d/production/D_RENDERER_UNIFIED_CONTENT_REVIEW_V1.json`
- `definitions/c11d/production/D_RENDERER_UNIFIED_CONTENT_REVIEW_SCHEMA_V1.json`
- `docs/current/d/D_RENDERER_CHALLENGE_COORDINATE_SAMPLE_COMPOSITION_UNIFIED_REVIEW_INTEGRATION_CHECKPOINT.md`
- `tools/c11d/d9/d_renderer_unified_content_review.py`
- `tools/c11d/d9/run_d_renderer_unified_content_review.py`
- `tools/c11d/d9/test_d_renderer_unified_content_review.py`
- this README

## Integration changes

- Adds the pinned `D_RENDERER_CHALLENGE_COORDINATE_SAMPLE_COMPOSITION_PROPOSAL_V1.json` to unified source lineage (15/15).
- Validates the composition contract and joins its declared cadence/spatial transform/anchor facts against the coordinate harness summary, the timeline and sample-selection proposal.
- Adds `coordinate_sample_composition` to the Challenge review item and `challenge_coordinate_sample_composition_proposal_parity` as the twelfth cross-artifact check.
- Updates the console PASS marker to report `cross_artifact=12/12` and `coordinate_sample_composition=PROJECT_THEN_SELECT_420_TO_210_PROPOSAL_ONLY`.
- Leaves all seven Godot harnesses unchanged. This is an additional Python review-layer check, not a new runtime harness.

The composition summary does **not** contain or claim a hash for a materialized 210-snapshot composed payload. It records the contract parity and the declared mathematical equivalence for the pinned affine uniform transform only.

## Preparation validation

- `py_compile`: PASS for updated Python review/runner files.
- `test_d_renderer_challenge_coordinate_sample_composition.py`: PASS, 18 tests.
- `test_d_renderer_challenge_simulation_sample_selection.py`: PASS, 22/22 negative controls.
- `test_d_renderer_unified_content_review.py`: PASS, 20 tests; source lineage 15/15, cross checks 12/12, negative controls 14/14.
- `jsonschema`: PASS.

Godot orchestration/full-project regressions were not executed in this packaging copy. They must be run on the operator's full Windows checkout after applying the overlay.

## Windows verification

Run in order:

```powershell
python -m py_compile `
  .\tools\c11d\d9\d_renderer_unified_content_review.py `
  .\tools\c11d\d9\test_d_renderer_unified_content_review.py `
  .\tools\c11d\d9\run_d_renderer_unified_content_review.py

python .\tools\c11d\d9\test_d_renderer_challenge_coordinate_sample_composition.py
python .\tools\c11d\d9\test_d_renderer_challenge_simulation_sample_selection.py
python .\tools\c11d\d9\test_d_renderer_challenge_coordinate_projection.py
python .\tools\c11d\d9\test_d_renderer_unified_content_review.py
python .\tools\c11d\d9\test_d_renderer_delivery_timebase_projection.py
python .\tools\c11d\d9\test_d_renderer_challenge_delivery_timeline_review.py

python .\tools\c11d\d9\run_d_renderer_unified_content_review.py --godot godot
python .\tools\c11d\d9\test_cross_suite_lifecycle.py
python .\tools\c11d\baseline_candidate\test_d_baseline_candidate.py
python -u .\c11c-suite\self_test.py
```

Expected unified review status includes:

- `content_types=3/3`
- `harnesses=7/7`
- `cross_artifact=12/12`
- `coordinate_sample_composition=PROJECT_THEN_SELECT_420_TO_210_PROPOSAL_ONLY`
- `source_lineage=15/15` in the Python contract test
- `unresolved_gates=8`
- `review=CONSISTENT_NOT_VIDEO_READY`

## Non-negotiable governance

- Keep C11-C 2.19.12 and `release/C11C_FREEZE_PACKAGE_MANIFEST.json` immutable. Expected manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- Coordinate projection, sample selection, interpolation and coordinate/sample composition remain `PROPOSED_NOT_APPROVED`.
- Do not materialize a combined output payload or turn this metadata review into a renderer input.
- `renderer=OFF`; `media_created=false`; `D4.8=BLOCKED`; `release_authority=NONE`.
- Keep all eight unresolved gates; a passing contract does not equal policy approval, D9 closure, baseline freeze or video readiness.
