# C11-D V2-B — Safe Visual Projection Runtime Harness Design V1

**Date:** 2026-10-20  
**Status:** DESIGN ONLY — NOT IMPLEMENTED, NOT A RUNTIME PASS  
**Scope:** test-only in-memory source-state observation. No payload materialization, media, renderer input, or binding approval.

## 1. Entry evidence

The operator-confirmed V2-C runtime acceptance is limited to source-frame and canonical route evidence: selectors 9/9, canonical planner 9/9, independent Godot processes 18/18, source pins 81/81, report SHA-256 `35e5985f47055fc11cbc0fcd7317f4d0a4ebe6bfe4d8bb22bdab67b7bcbe56a7`. The semantic source review is installed and its focused Windows suite passed 34/34. Neither gate approves a renderer binding or demonstrates visual seed sensitivity.

The analysis baseline is `ChallengeEngineV01_STATELESS_NIGHTLY_20261710_1555.zip`, SHA-256 `aced079f3f553d81121e84940e6a7d9f2be4c278912b94abee75f277b8f32df2`. The frozen C11-C manifest remains pinned at `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## 2. Architecture: distinguish identity classes

V2-B must not collapse input/request identity into output evidence. Each run retains separate fields:

1. `canonical_request_hash` — identity of one canonical planner request.
2. `canonical_plan_hash` — identity of the returned plan; neither request nor plan hash proves a state change.
3. `projection_instance_identity_sha256` — binds the selector, pinned source/mechanic, projection schema and variant inputs.
4. `safe_projection_state_sha256` — hashes the actual ordered source-state projection over the six base `FrameSnapshot` fields. This is the gameplay-seed sensitivity oracle.
5. `candidate_field_probe_sha256` — a separate hash for a single reviewed candidate field stream, without emitting raw values.
6. `payload_identity` — not created in V2-B. No payload hash or renderer input may be claimed.

## 3. Safe projection boundary

The only base frame fields permitted in the test-only projection are `position`, `rotation`, `scale`, `opacity`, `texture_index`, and `variant_id`. Serialize them as an ordered tuple per source frame: frame index, position x/y, rotation, scale x/y, opacity, texture index, variant id. Reject non-finite numbers, invalid types, missing fields and frame cardinality mismatches. Preserve source frame order, source FPS and raw coordinate values exactly. No coordinate conversion, resampling, frame interpolation or presentation-space remapping is permitted.

`custom_data` is not part of this projection. The full map is never enumerated or serialized. Candidate probes, when the future runtime harness is authorized, read only one listed field at a time, validate its exact semantic type/lifecycle, and emit only type/presence summaries and a per-field hash. Raw candidate values are omitted from receipts, and none of these probes is a renderer binding.

The projection runs only in memory as a measurement function over `ChallengeRuntimeBridge.run_effective_pipeline` output. It must not create scene/render nodes, call `RenderingServer`, capture a viewport, write payload/media files, dispatch production or mutate canonical simulation state.

## 4. Candidate semantics and seed oracle

| Selector | Candidate observation only | Expected field-level behavior under gameplay-seed mutation | Constraint |
|---|---|---|---|
| 001 key | No `custom_data` candidate. | Primary source-state projection must be seed-sensitive. | `presentation.static_target_position` is duplicate authority; KeyMechanic setup does not consume that presentation field. |
| 002 parking | No static target projection. | Primary source-state projection must be seed-sensitive. | Static target coordinates are blocked from visual projection because source coordinate space is undeclared. Raw state fingerprint only; no transform. |
| 003 pilot | `target_x: float`. | Candidate `target_x` is expected invariant; primary trajectory projection is expected seed-sensitive via trajectory/control streams. | Scalar in `PILOT_0X100`; never infer a Y coordinate or convert to `Vector2`. |
| 004 parking_v2 | No static target binding; keep V1 fixture immutable. | Primary source-state projection must be seed-sensitive. | No edits or replacements to the two existing CHALLENGE_004 V1 harness files. |
| 005 hit_v1 | `target_position: Vector2`. | Candidate value is a seeded per-run constant repeated on every source frame; expected change across seed variants. | Do not call it a moving per-frame target. Keep it outside the safe projection. |
| 006 catch_v1 | `target_position: Vector2`. | Per-frame target track; expected seed-sensitive. | Keep target `p_t` separate from catcher primary `p_c`; preserve frame alignment. |
| 007 find_v1 | `target_position: Vector2`. | Per-frame target track; expected seed-sensitive. | Keep `p_target` separate from scanner `p_scan`; do not project distractor topology. |
| 008 choose_v1 | `active_selection: int`. | Expected seed-sensitive at source-frame scope only. | Validate index/range/selected-position consistency. Phase/timeline acceptance remains blocked. |
| 009 count_v1 | `displayed_count: int`. | Expected seed-sensitive at source-frame scope only. | Validate count range and positional encoding. Never substitute `target_count`. Phase/timeline acceptance remains blocked. |

The six `custom_data` rows remain candidates, not bindings. The design contract still asserts `approved_bindings=0` and `approved_custom_data_bindings=0`.

## 5. Variant matrix and deterministic comparisons

For each of nine selectors, the future runtime implementation uses five independent Godot processes and five canonical planner calls:

- `BASELINE_R1`: source effective gameplay seed, music seed `840001`, original editorial input.
- `BASELINE_R2`: identical input, a distinct process/run ID.
- `GAMEPLAY_SEED_MUTATION`: mutate only gameplay seed to a deterministic distinct valid seed; keep music seed/editorial fixed.
- `MUSIC_SEED_MUTATION`: keep gameplay seed/editorial fixed; use music seed `840002`.
- `EDITORIAL_MUTATION`: keep both seed domains fixed; modify title, subtitle and call-to-action only.

The effective gameplay seed must reach the in-memory source configuration consumed by `ChallengeRuntimeBridge.run_effective_pipeline`. Use a deep copy and never write the Challenge JSON. Do not fork planner or mechanic code. For CHOOSE/COUNT, follow the mechanic's real seed precedence and record the selected effective seed; if that cannot be resolved from source, fail closed.

This matrix requires **45 planner invocations and 45 independent Godot runtime processes** across the nine selectors. That is the design denominator, not execution evidence.

Acceptance conditions:

- Baseline R1/R2: request hash, plan hash, safe-state hash and each candidate field hash agree; process/run IDs differ.
- Gameplay-seed mutation: `safe_projection_state_sha256` must actually change for each of the nine primary source-state tracks expected to be seed-consuming. Request/plan hash changes alone do not pass.
- Music-seed mutation: request identity may change, but the safe-state and candidate field hashes remain equal to baseline.
- Editorial-only mutation: editorial/request identity changes while simulation-input identity, safe-state hash and candidate hashes remain equal to baseline.
- Pilot `target_x` is not the seed-sensitivity oracle: its candidate hash is expected to remain invariant under gameplay seed mutation even when Pilot primary position/trajectory changes.
- The V2-B receipt records candidate field probe hashes separately from the base projection hash and never records raw candidate values.

If a gameplay-seed variant produces the same safe-state hash, report a blocker with selector and hashes. Never reclassify request or plan hash as output sensitivity evidence.

## 6. Fail-closed cases

The design test matrix enumerates 44 cases, including missing/mismatched source pins, selector omissions/duplicates, unknown fields, non-finite base transform values, wrong field types, whole-`custom_data` access, unauthorized custom fields, candidate track cardinality mismatch, out-of-range option/count values, no output-state sensitivity after gameplay-seed mutation, music-seed leakage, editorial leakage, repeat mismatch, hash identity substitution, claims of payload identity without a payload, prohibited side effects and timeline acceptance for selectors 008/009.

No runtime harness implementation or runtime acceptance is included in this increment. The Python design tests prove contract coherence and source pin identity only.

## 7. Governance

Keep `renderer=OFF`, `media_created=false`, `payload_materialized=false`, `candidate_input_admissible=false`, `seed_domains_complete_for_candidate_input=false`, `automatic_seed_generation=false`, `master_seed=NOT_ADOPTED`, `D4.8=BLOCKED`, `D9.10=PREPARE_ONLY`, `D9.14=BLOCKED`, `D9.16=BLOCKED`, `D9.17=BLOCKED_NO_GO`, `D10=BLOCKED_FOR_PROMOTION`, `baseline_approval=MISSING`, `freeze_eligible=false`, `release_authority=NONE` and zero approved bindings.

`CHALLENGE_008` and `CHALLENGE_009` retain declared total 11 s and phase sums 12 s. No JSON changes, inferred precedence or timeline acceptance.

## 8. Next increment

After this design overlay is applied and its contract tests pass in the active Windows checkout, implement the V2-B runtime harness in a separately versioned add-only overlay. Runtime receipts must include independent process identity, effective seed lineage, state/probe hashes, source pins, exact exit codes, stdout/stderr hashes, and explicit per-selector accepted/blocked rows. Do not implement a materializer or renderer input path.
