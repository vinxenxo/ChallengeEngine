# C11-D V2-B Safe Projection Runtime Implementation Checkpoint — V1 (2026-10-20)

## Status

**Implementation prepared; not yet installed or accepted in the active Windows checkout.** Status in the runtime contract is `IMPLEMENTED_NOT_RUNTIME_ACCEPTED`. The 45-planner/45-Godot runtime matrix has not been executed.

## Operator-confirmed upstream evidence

- V2-B design contract accepted: focused tests 90/90, 11/11 design-overlay files, 81/81 source pins, 9/9 authority-input pins, approved bindings `0`.
- Operator-reported output hashes: test stdout `64403918b4d3da5d0c73bca6fd99a93313111eb01cd1707781bda349d7ce02a9`; test stderr `fc72bf1b57934ff830c2955a8f94aa0a4d6b3a06beaa9da3c256e1aa4e801452`.
- C11-C manifest before/after the design tests: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- V2-C source-frame/route runtime report remains `35e5985f47055fc11cbc0fcd7317f4d0a4ebe6bfe4d8bb22bdab67b7bcbe56a7`, scope-limited to its stated acceptance.
- Source semantic review remains operator-confirmed 34/34 with approved bindings `0`.

## Prepared implementation artifacts

The add-only overlay adds 12 repository files: four strict JSON schemas/contracts; an in-memory Godot projection harness; a Python canonical-planner/Godot matrix runner; its Python implementation/static source-audit tests; README; this checkpoint; V10 continuity checkpoint; and V10 start/overhand prompts. Exact per-file digests are in the overlay manifest.

The contract pins the V2-B design, V2-B seed matrix, V2-C source-frame contract, C11-C manifest and implementation artifacts. Source identity is resolved from the pinned V2-C contract because the V2-B design selector records do not themselves carry `family_id`.

## Local implementation verification — not active Windows acceptance

The implementation test/static source audit was run in an isolated reference tree and passed 198/198. Stdout SHA-256 `bb5dd1056fda04b73bc8f6d2cdcbcaec9f104e32b8f5323430e61223c3c5859c`; stderr SHA-256 `a7094686f3f9d6a52c2b8ec5f83c771612609f6a13622bf27465ef7524045db2`. Python compilation for the runner and test script passed. This is not evidence that the overlay is installed in Windows and not runtime acceptance. No Godot process was launched for V2-B during local preparation.

## Next active steps

1. Apply the runtime-implementation ZIP in ADD_ONLY mode only after verifying its outer SHA-256 and internal manifest SHA, all 12 destination paths absent, every listed payload-file hash, all 81 design source pins, all nine authority-input pins, and the frozen C11-C manifest hash. Roll back the increment if any write or postcondition fails.
2. Run the separate Windows implementation test block. Require its real Python process exit code `0`, marker `C11D_V2B_RUNTIME_IMPLEMENTATION_TESTS_PASS=198/198`, source pins `81/81`, authority pins `9/9`, and unchanged C11-C manifest. Only on these conditions may it produce `implementation_test_receipt.json`.
3. Review the receipt and active-file SHA evidence. Do not execute the next runtime matrix until this static gate is operator-confirmed.
4. After static acceptance, run exactly 45 canonical planner calls and 45 independent Godot 4.7.1 Mono processes using the runner, with the receipt and pinned contract SHA supplied. Stop on first failure; preserve per-process stdout/stderr, receipts and final report SHA.

## Expected runtime proof obligations (future gate)

- Same-input baseline repeats agree across independent processes while process/run identities differ.
- Gameplay-seed mutation changes the six-field safe source-state hash for all nine selectors.
- Music-seed and editorial-only mutations preserve safe state, simulation input and candidate-field hashes while the appropriate request/plan/editorial identity changes.
- Pilot `target_x` remains the seed-invariant candidate exception; Hit target is a per-run constant; Catch/Find targets are source-frame tracks; Choose/Count checks remain source-frame-only.
- All 81 source pins and nine authority-input pins stay clean before and after the matrix.
- No full `custom_data` map, raw candidate observations, payload, media, renderer-native input, transform, resampling, challenge JSON edit or C11-C change appears.

## Immutable governance

`renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.

The active Windows checkout remains the authority. The analysis baseline ZIP is not permission to replace it. The frozen C11-C manifest and CHALLENGE_004 V1 runtime fixtures are immutable. CHALLENGE_008/009 declared-duration/phase-sum conflicts remain unresolved; this gate is source-frame acceptance only.
