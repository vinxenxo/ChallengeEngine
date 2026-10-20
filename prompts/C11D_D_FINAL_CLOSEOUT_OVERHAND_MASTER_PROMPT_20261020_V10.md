# C11-D Final Closeout Overhand Master Prompt — V10 (2026-10-20)

## 1. Role, authority and baseline

Continue D9/D10 engineering and acceptance for `ChallengeEngineV01_STATELESS` without weakening governance. The active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` is the truth. The analysis archive `ChallengeEngineV01_STATELESS_NIGHTLY_20261710_1555.zip` has SHA-256 `aced079f3f553d81121e84940e6a7d9f2be4c278912b94abee75f277b8f32df2`, but is not proof of active-checkout identity and must not be extracted over it.

The frozen C11-C manifest SHA-256 is `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Keep it byte-identical. No D artifact may change C11-C or imply promotion before acceptance, formal approval, freeze and promotion are independently completed.

## 2. Scope-bound accepted evidence

- V2-C source-frame/route runtime: operator-confirmed 9/9 selectors, 9/9 canonical planner calls, 18/18 independent Godot 4.7.1 Mono processes, 81/81 pins; report SHA `35e5985f47055fc11cbc0fcd7317f4d0a4ebe6bfe4d8bb22bdab67b7bcbe56a7`. It does not prove gameplay-seed sensitivity of the V2-B safe state or any payload/render/media acceptance.
- Source semantic review: operator-confirmed tests 34/34, pins 81/81, bindings approved 0.
- V2-B design contract: operator-confirmed tests 90/90, files 11/11, source pins 81/81, authority-input pins 9/9, bindings approved 0. Operator-reported test stdout SHA `64403918b4d3da5d0c73bca6fd99a93313111eb01cd1707781bda349d7ce02a9`; stderr SHA `fc72bf1b57934ff830c2955a8f94aa0a4d6b3a06beaa9da3c256e1aa4e801452`. Frozen C11-C manifest was unchanged before/after.
- This V10 runtime implementation overlay is locally static-tested 198/198 in an isolated reference tree. Local stdout SHA `bb5dd1056fda04b73bc8f6d2cdcbcaec9f104e32b8f5323430e61223c3c5859c`; stderr SHA `a7094686f3f9d6a52c2b8ec5f83c771612609f6a13622bf27465ef7524045db2`. These local results do not mean the overlay has been installed or tested on the active Windows checkout; no Godot V2-B matrix was run in local preparation.

## 3. Runtime implementation identity

The add-only implementation overlay ID is `C11D_V2B_SAFE_PROJECTION_RUNTIME_IMPLEMENTATION_OVERLAY_20261020_V1`; it adds exactly 12 repository files plus the ZIP-root overlay manifest. Core pins:

- Runtime contract `definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_PROJECTION_RUNTIME_CONTRACT_V1.json`: `f89235640f40c81be6100f01f1007ed4e787990a1bbf7927fcd8d676ef2cb9a3`.
- Runtime contract schema: `0f804aeb51427286a6160aa445cdd98b2d3bbaaace19feacfa32f80e0fe738a5`.
- Runtime receipt schema: `278ef5c1e4a96955d547dc70ab2e8cebc73f5ddb904dbb66563322be5c52e52c`.
- Runtime report schema: `7152b4cb28f01dd33d140b22459d6eafd98d6a21811393d48ace97640c4a04b1`.
- Godot in-memory harness: `aa175afe2ce357473aa46ed7c55ce46edf3f56457db461be28f7ec8e2f0b5ce2`.
- Python runtime runner: `6a92aac96786acd2316f8e46b9d895f7cdcdfccbd75e9686378a4144a3a01a7f`.
- Static implementation test: `35a14f6d7ec56146b0cfaa3d304d18e5325757ed660e1fc08e1b4a0f767ecc87`.
- V2-B design: `e4f02e37fd4b9b2c89cbaa7597162f87b180da43182dc576d664263c1b937cfc`; seed matrix `d69c3fb2aca78a26c3afbfda0084f7f7aef458ee404b37f65261c6d22e43121a`; V2-C source-frame contract `6d3c59214edbdd917cf63fe9ca4859edb6968d503368ec84e867bdd56a8df74c`.

The runtime contract remains `IMPLEMENTED_NOT_RUNTIME_ACCEPTED` and `NOT_EXECUTED_BY_DESIGN_OR_IMPLEMENTATION_TESTS`. Verify final archive and manifest hashes from the delivered artifact rather than guessing them from these files.

## 4. Immediate operation sequence

1. Apply the new overlay only in ADD_ONLY mode after verifying outer ZIP SHA, internal manifest SHA, each of the 12 file hashes, all destinations absent, 81 source pins, nine authority-input pins, the source design/matrix/V2-C contract pins, and immutable C11-C manifest. Stop and rollback on any unexpected condition.
2. Separately run the active-Windows implementation/static source audit. Require real process exit code zero and exact marker `C11D_V2B_RUNTIME_IMPLEMENTATION_TESTS_PASS=198/198`. Verify all pins again before and after. Generate `implementation_test_receipt.json` only after that gate passes, with exact hashes of the actual checked-out contract, runner, harness, schemas, tests, logs and overlay manifest.
3. Only after the operator confirms this static Windows result and receipt should the next increment run the V2-B acceptance matrix: 9 selectors × 5 roles = 45 canonical planner invocations and 45 independent Godot 4.7.1 Mono processes. Provide a separate, deterministic, PowerShell 5.1-compatible execution block. Use `--implementation-test-receipt`, exact `--contract-sha256`, repo root, evidence directory and resolved valid Godot executable. Stop on first failure. Preserve per-run receipt/stdout/stderr, final report and hashes.
4. Do not turn a failed/partial matrix into PASS, and do not run downstream aggregation or close a gate until the full required denominator and pin audits pass.

## 5. Technical contract and measurement oracles

- Selector family identity is not present in V2-B design selector records. Resolve it through the pinned V2-C source-frame contract and cross-check selector mechanic, source path and source SHA. Never patch a missing field into the design as a workaround.
- Existing planner: `universal_producer.evaluate_universal_request(raw, root)`. Existing Godot bridge: `ChallengeRuntimeBridge.run_effective_pipeline(legacy_config: Dictionary)`. Do not clone the planner or mechanics.
- Five roles per selector: `BASELINE_R1`, `BASELINE_R2`, `GAMEPLAY_SEED_MUTATION`, `MUSIC_SEED_MUTATION`, `EDITORIAL_MUTATION`. Denominators: 45 planner calls, 45 independent Godot processes.
- Safe source projection: ordered source-frame data only, with six base fields `position`, `rotation`, `scale`, `opacity`, `texture_index`, `variant_id`; no coordinate transforms, interpolation or resampling. `safe_projection_state_sha256` is the only gameplay-seed sensitivity oracle; request/plan identities are not a substitute.
- Candidate per-field observations are individually allowlisted, hash-only, and do not output raw values. Whole `FrameSnapshot.custom_data` map access/serialization is prohibited. `payload_identity=NOT_CREATED`.
- Baseline repeats must agree on input/plan/state/candidate hashes while run/process identifiers differ. Gameplay seed must change safe-state hash for all nine selectors. Music seed and editorial-only mutation must preserve base safe-state and candidate hashes while appropriate identity hashes vary. Pilot `target_x` is expected seed-invariant; Hit target vector is per-run constant; Catch/Find targets are source-frame vector tracks; Choose `active_selection` is a checked option index; Count `displayed_count` is an integer tied to primary-position encoding.
- V2-B is source-frame-only. CHALLENGE_008/009 declared total duration 11 seconds while phase durations sum to 12 seconds; do not claim timeline acceptance or adjust those JSONs. CHALLENGE_004 V1 runtime harnesses remain immutable.

## 6. Hard governance locks

Keep `renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.

This harness is test-only and in-memory. It does not authorize a production consumer, native renderer input, output media, dispatch or baseline change. Preserve the existing canonical C11-C package and manifest exactly. Do not create or infer approvals. Report only evidence demonstrated by the exact counters, receipts and hashes.
