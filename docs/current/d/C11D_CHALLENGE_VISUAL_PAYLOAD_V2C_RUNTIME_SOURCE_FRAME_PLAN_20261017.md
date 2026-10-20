# Challenge Visual Payload V2-C — Source-Frame Runtime Receipt Plan

**Date:** 2026-10-17  
**Implementation status:** contract and harness prepared; Windows Godot runtime evidence not yet collected.  
**Analysis baseline:** `ChallengeEngineV01_STATELESS_NIGHTLY_20261710_1555.zip` (SHA-256 `aced079f3f553d81121e84940e6a7d9f2be4c278912b94abee75f277b8f32df2`).  
**Scope:** read-only source-frame/route acceptance for `CHALLENGE_001`–`CHALLENGE_009` only.

## Reconciliation

The baseline ZIP's frozen manifest `release/C11C_FREEZE_PACKAGE_MANIFEST.json` has SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`, matching the immutable C11-C manifest pin. The capability contract and its 43 declared source pins match the archive. The semantic-binding proposal contract SHA-256 is `d37cb74f360e19e664b94673bbf4b95462cad6e681a08215a95f4565c6e810aa`; its 18 Challenge/mechanic source pins match.

The V6 continuity checkpoint exists at its established path and is not modified by this increment. Some paths referenced by the supplied V7 start instructions (the V6 renderer gate map, final closeout evidence ledger, D final roadmap V1, V2-C plan, and V7 prompt files) are absent from this ZIP; existing files are retained as historical artifacts. This plan does not claim those documents or a V7 checkpoint are installed in the Windows checkout.

## Inspected runtime entry

- `core/execution/ChallengeRuntimeBridge.gd`: `static func run_effective_pipeline(legacy_config: Dictionary) -> Dictionary`.
- Success returns `context`, `runtime_input`, and `validation`; `context` carries the `SimulationResult`, source `VideoTimeline`, and `PresentationBindingResult`.
- `SimulationResult.frames` is an `Array[FrameSnapshot]`; `FrameSnapshot` has typed fields `position: Vector2`, `rotation: float`, `scale: Vector2`, `opacity: float`, `texture_index: int`, `variant_id: int`, and `custom_data: Dictionary`.
- The V2-C harness calls this canonical runtime once per process. The Python runner launches two separate Godot processes per selector. It also prepares a canonical D9.9 plan and validates the planning-only D9.10 bridge/adapter route; those envelopes are never passed into the simulation.
- The existing V1 `CHALLENGE_004` scripts are pinned and are not modified.

## Source semantic review — proposals remain unapproved

| Selector | Proposed source candidate | Source semantics | V2-C handling |
|---|---|---|---|
| `CHALLENGE_001/key` | `presentation.static_target_position` | 2D static metadata, explicit `CANVAS_1080X1920` | source pin only; no binding approval |
| `CHALLENGE_002/parking` | `difficulty.parking.target_position` | 2D static metadata; coordinate space undeclared | do not infer coordinate space |
| `CHALLENGE_003/pilot` | `custom_data.target_x` | `float` scalar in `PILOT_0X100`; snapshot has `position.x` but this field is not a `Vector2` | report only field presence/type counts |
| `CHALLENGE_004/parking_v2` | `difficulty.parking.target_position` | 2D static metadata, `CANVAS_1080X1920` | keep existing V1 harness untouched |
| `CHALLENGE_005/hit_v1` | `custom_data.target_position` | `Vector2` secondary target track, distinct from primary object position | report only field presence/type counts |
| `CHALLENGE_006/catch_v1` | `custom_data.target_position` | `Vector2` target track distinct from catcher position | report only field presence/type counts |
| `CHALLENGE_007/find_v1` | `custom_data.target_position` | `Vector2` target track distinct from scanner position | report only field presence/type counts |
| `CHALLENGE_008/choose_v1` | `custom_data.active_selection` | integer option index; snapshot position already carries selected option location | source-frame-only; phase/timeline blocked |
| `CHALLENGE_009/count_v1` | `custom_data.displayed_count` | integer display-state counter; `target_count` exists separately | source-frame-only; phase/timeline blocked |

`approved_bindings=0`; all nine semantic rows and all six base `FrameSnapshot` fields remain unapproved for payload projection. V2-C never serializes custom-data values or the complete `custom_data` map. The frame projection hash includes only the index and six source-frame base fields (`position`, `rotation`, `scale`, `opacity`, `texture_index`, `variant_id`). It is not a visual seed sensitivity test.

## Timebase conflict

`CHALLENGE_008` and `CHALLENGE_009` declare `total_duration=11s` while `hook + game + reveal + CTA = 3 + 7 + 0 + 2 = 12s`. This increment records those exact values but does not select a precedence, mutate source JSON, normalize phases or claim phase/timeline acceptance.

## Process and evidence contract

- Nine mandatory selectors; never shrink the denominator.
- Two independent Godot 4.7.1 Mono processes per successfully exercised selector; fixed inputs and source pins, no timestamps in determinism comparisons.
- The harness emits one compact JSON receipt marker per process. Receipts record actual engine version, process ID/exit code, source lineage pins, route status, effective mechanic, frame count/cardinality/shape, source FPS/game duration, safe projection hash, pinned source asset references, candidate custom-data type histograms only, repeatable receipt fields, and explicit block status.
- Any failure halts later runtime launches; remaining selector rows are explicitly `NOT_RUN_AFTER_FIRST_FAILURE` rather than omitted.
- All temporary report/stdout/stderr evidence is written only to the operator-selected `%TEMP%` evidence directory. No payload file, media, renderer node, viewport, renderer-native input or production dispatch is created.

## Required governance locks remain unchanged

`renderer=OFF`, `media_created=false`, `candidate_input_admissible=false`, `seed_domains_complete_for_candidate_input=false`, `automatic_seed_generation=false`, `master_seed=NOT_ADOPTED`, `D4.8=BLOCKED`, `D9.10=PREPARE_ONLY`, `D9.14=BLOCKED`, `D9.16=BLOCKED`, `D9.17=BLOCKED_NO_GO`, `D10=BLOCKED_FOR_PROMOTION`, `baseline_approval=MISSING`, `freeze_eligible=false`, `release_authority=NONE`. `challenge_visual_seed_sensitivity=NOT_TESTED`.

## What remains to be proven

This package does not assert the runtime is green: no Godot executable was available in the packaging environment. After the add-only overlay is applied to the authoritative Windows checkout, the operator must run Python contract tests first and then the 9-selector Godot receipt command, confirm actual exit codes, receipt markers, exactly 18 independent runtime processes for full coverage, report/source pin hashes, unchanged C11-C manifest, and all governance locks.
