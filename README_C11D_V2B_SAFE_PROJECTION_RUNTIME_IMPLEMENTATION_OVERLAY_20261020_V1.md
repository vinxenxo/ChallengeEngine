# C11-D V2-B Safe Projection Runtime Implementation Overlay — V1 (2026-10-20)

## Purpose and lifecycle

This is a **D-only, add-only implementation increment** for the V2-B safe source-state projection runtime test harness. It is separate from the accepted V2-B design overlay. It is not installed in the operator's active Windows checkout until the guarded apply block reports success.

The code is an isolated measurement harness and canonical-planner/Godot acceptance runner. It is not a production payload consumer, renderer, dispatcher, or media generator. Its contract status is `IMPLEMENTED_NOT_RUNTIME_ACCEPTED`; runtime status remains `NOT_EXECUTED_BY_DESIGN_OR_IMPLEMENTATION_TESTS`.

## Pinned inputs

- Frozen C11-C manifest: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- V2-B design contract: `e4f02e37fd4b9b2c89cbaa7597162f87b180da43182dc576d664263c1b937cfc`.
- V2-B seed-test matrix: `d69c3fb2aca78a26c3afbfda0084f7f7aef458ee404b37f65261c6d22e43121a`.
- V2-C source-frame runtime contract: `6d3c59214edbdd917cf63fe9ca4859edb6968d503368ec84e867bdd56a8df74c`.
- Accepted V2-C source-frame report: `35e5985f47055fc11cbc0fcd7317f4d0a4ebe6bfe4d8bb22bdab67b7bcbe56a7`.
- Frozen capability, semantic proposal and semantic review contract hashes are pinned in the V2-B design's nine `authority_input_pins`.
- The installed design must still resolve 81/81 source pins and 9/9 authority-input pins.

The supplied baseline ZIP is an analysis reference only. The active Windows checkout is authoritative.

## Runtime harness behavior

- The planner uses the existing canonical `universal_producer.evaluate_universal_request` route and the existing runtime bridge; it does not clone mechanics or the planner.
- Selector family identity is resolved from the pinned V2-C source-frame contract and cross-checked against the V2-B design selector. The design selector itself does not contain `family_id`.
- The GDScript harness performs one in-memory canonical pipeline run for its selected variant. It does not create a file payload or media, add render nodes, call a renderer, or modify challenge JSON.
- The safe-state projection preserves source frame order and source timebase. Its only base fields are `position`, `rotation`, `scale`, `opacity`, `texture_index`, and `variant_id`; no coordinate transform, interpolation or resampling is permitted.
- Candidate observations are per-field, allowlisted and hash-only. Raw values and the whole `custom_data` map are never emitted or serialized.
- Request, plan, editorial, projection-instance, safe-state and candidate-field hashes stay distinct. Only `safe_projection_state_sha256` is the gameplay-seed output sensitivity oracle. Payload identity remains `NOT_CREATED`.
- All 9 selectors have five planned variants: two baseline repeats, gameplay-seed mutation, music-seed mutation, and editorial-only mutation. The later acceptance denominator is 45 canonical planner calls and 45 independent Godot processes. This implementation overlay does not execute that matrix.

## Local static verification

In the isolated working reference tree, the focused implementation test/static audit passed **198/198**. The exact isolated runner output hashes were:

- stdout: `bb5dd1056fda04b73bc8f6d2cdcbcaec9f104e32b8f5323430e61223c3c5859c`
- stderr: `a7094686f3f9d6a52c2b8ec5f83c771612609f6a13622bf27465ef7524045db2`

Python compilation passed for the runtime runner and its test script. This was a local package/reference-tree test, not a test in the active Windows checkout. No Godot runtime execution occurred in this preparation environment, and no 45/45 matrix is claimed.

## Installation and next gate

Use the exact ZIP hash and embedded add-only manifest, and verify all destinations are absent before writing. Validate every source and authority pin and preserve the C11-C frozen manifest before and after application. Then run the separate Windows static-test block. It must produce `C11D_V2B_RUNTIME_IMPLEMENTATION_TESTS_PASS=198/198` and write a hash-bound `implementation_test_receipt.json` only after a successful process exit.

Only after operator-confirmed Windows static acceptance is the next gate the 45 planner / 45 independent Godot runtime matrix. That matrix has not been run by this overlay. It must run through Godot 4.7.1 Mono and stop at the first failure.

## Governance locks

`renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.

No change is authorized to any challenge JSON, frozen C11-C asset/manifest, or immutable CHALLENGE_004 V1 harness. CHALLENGE_008/009 timeline acceptance remains blocked by the declared 11s duration versus 12s phase sum; source-frame observations do not resolve it. No candidate binding is approved by this implementation.
