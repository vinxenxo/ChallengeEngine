# C11-D Final Closeout Overhand Master Prompt — V2-B Design Authority (2026-10-20, V9)

## 1. Authority and baseline

The active checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` is the source of truth. Analysis archive `ChallengeEngineV01_STATELESS_NIGHTLY_20261710_1555.zip` SHA-256 `aced079f3f553d81121e84940e6a7d9f2be4c278912b94abee75f277b8f32df2` is a reference only. Frozen C11-C manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` is immutable.

## 2. Current accepted evidence (scope-bound)

- V2-C source-frame/route runtime: operator-confirmed PASS, 9/9 selectors, 9/9 planner invocations, 18/18 independent Godot 4.7.1 Mono runtime processes, 81/81 source pins. Report SHA-256 `35e5985f47055fc11cbc0fcd7317f4d0a4ebe6bfe4d8bb22bdab67b7bcbe56a7`. Does not prove projected-state gameplay seed sensitivity, renderer payload acceptance, or production eligibility.
- Semantic source review: 34/34 focused Python tests; 81/81 source pins; six `custom_data` candidate rows retained; approved bindings remain zero.
- Current design overlay is the next gate, not a runtime acceptance event.

## 3. V2-B safe projection design

The add-only design contract defines a test-only, read-only in-memory ordered source-state fingerprint over the six base `FrameSnapshot` fields. It preserves raw coordinates, frame order, source FPS and cardinality and performs no transformation/resampling. It never emits renderer-native inputs, writes payload/media, creates render nodes, calls RenderingServer, captures a viewport or changes canonical simulation state.

Candidate `custom_data` probes are separate, individually allowlisted hash-only observations. Whole-map access/serialization is prohibited, raw candidate values are not emitted, and candidate observation must not imply binding approval. `target_x` is scalar/invariant as a candidate seed probe; Hit target vector is constant per run; Catch/Find target vectors are per-frame; Choose/Count candidates are source-frame-only because their timeline blocker remains unresolved.

Identity classes remain separate: canonical request hash, canonical plan hash, projection-instance identity, safe projection state hash, candidate per-field hashes; payload identity is not created. Only the safe state hash establishes gameplay seed output sensitivity. Music seed changes and editorial-only changes must preserve the state hash; repeats must agree across independent processes.

The subsequent runtime implementation is specified as 5 variants per selector and 45 planner calls plus 45 independent Godot processes total. Those are future denominators, not current evidence. No runtime implementation is included in this design overlay.

## 4. Exact current task

Verify overlay SHA-256, its add-only manifest, the 81 source pins and nine existing authority-input pins, and reject any existing destination. Apply ten new files atomically with rollback on failure. Run the focused design tests using reliable Python stdout/stderr capture and real exit code. Expected marker: `C11D_V2B_DESIGN_CONTRACT_TESTS_PASS=90/90`.

If pins drift or a destination exists, stop and reconcile; do not overwrite, use an older snapshot, or rerun all V2-C suites. After design acceptance, prepare the separately versioned V2-B runtime harness overlay. Do not begin the 45+45 runtime matrix before that implementation has its own tests and static audit.

## 5. Governance locks

Keep renderer OFF, media/payload absent, candidate input inadmissible, seed domains incomplete, automatic seed generation off, master seed NOT_ADOPTED, D4.8 BLOCKED, D9.10 PREPARE_ONLY, D9.14/D9.16 BLOCKED, D9.17 BLOCKED_NO_GO, D10 BLOCKED_FOR_PROMOTION, baseline approval missing, freeze ineligible and release authority NONE. Approved bindings and approved custom_data bindings remain zero. Keep CHALLENGE_008/009 timebase conflicts unresolved. Preserve CHALLENGE_004 V1 harness byte for byte.
