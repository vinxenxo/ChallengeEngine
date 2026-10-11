# C11-D — Coordinate + Sample Composition in Unified Content Review

**Status:** `PASS` as proposal-contract parity integration; **NOT APPROVED**, **NOT FROZEN**, and **NOT VIDEO READY**.

## Purpose

Connect the standalone coordinate/sample composition proposal to the existing unified C11-D content-review manifest. The integration adds one cross-artifact check; it does not add another Godot harness and does not build or emit a composed delivery payload.

## What the unified review now checks

- The pinned composition proposal contract is present in the canonical source lineage (15 entries total) and matches its SHA-256.
- The proposal's challenge/source and delivery timebases, GAME segment windows, snapshot counts, stride, sample origin, first/last selected indices, `winning_frame` mapping, and `close_calls` count match the runtime, timeline, and sample-selection proposal.
- The operation order remains `PROJECT_ALL_GAME_COORDINATES_IN_ORIGINAL_ORDER`, then `SELECT_EVEN_ZERO_BASED_GAME_LOCAL_INDICES`.
- The selected index set matches the sample-selection proposal (`0, 2, 4, …, 418`); the declared candidate count is 210 while the separate spatial preview remains 420 records.
- The composed transform remains uniform scale `2/3` on both axes with zero offset; the target coordinate agrees with the coordinate-projection runtime summary within float precision tolerance.
- The declared equivalence is limited to the affine, uniform, zero-offset transform. No composed snapshot payload is materialized by this review; the claim is not a runtime record-hash parity assertion.
- Proposal approvals stay false; renderer input, dispatch, activation, persistent report, production, and media remain disabled.

## Canonical output

The console report adds `coordinate_sample_composition` to the Challenge content item and the cross-artifact check `challenge_coordinate_sample_composition_proposal_parity`. The PASS line reports `cross_artifact=12/12` and `coordinate_sample_composition=PROJECT_THEN_SELECT_420_TO_210_PROPOSAL_ONLY`.

The canonical eight unresolved gates remain unchanged. Sample-selection/interpolation and coordinate-projection approval remain pending; the renderer baseline external approval is not asserted here; `D4.8=BLOCKED`; `release_authority=NONE`.

## Validation performed during preparation

- Python syntax compilation: PASS for the updated coordinator, test suite, runner, composition validator and composition tests.
- Composition proposal tests: 18 tests PASS.
- Sample-selection proposal test contract: PASS, negative controls 22/22.
- Unified review contract tests: 20 tests PASS; contract source lineage 15/15; cross checks 12/12; negative controls 14/14.
- `jsonschema` validation: PASS in the preparation environment.
- This preparation environment does not contain the full project/Godot checkout, so the seven-harness Godot orchestration and full repo regressions must be confirmed in the operator's Windows checkout after applying the overlay.

## Governance boundary

This overlay only changes the review contract, review schema, Python review coordinator/tests/console summary, and this checkpoint. It does not modify C11-C, the frozen manifest, source simulation, source snapshots, the Godot harnesses, renderer adapter, or any output media. It must not promote any proposal to `APPROVED` based on passing checks.
