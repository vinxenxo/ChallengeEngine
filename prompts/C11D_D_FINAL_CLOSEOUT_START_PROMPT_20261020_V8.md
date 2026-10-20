# C11-D Final Closeout Start Prompt — 2026-10-20 V8

Continue C11-D closeout from the user's active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. The active checkout is the source of truth; the designated baseline ZIP is useful for source review only and must not overwrite a divergent checkout.

## Read first

1. `AGENTS.md`
2. `.continue/rules/CONTINUE.md`
3. `docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md`
4. Existing continuity checkpoint V6 and V7 without overwriting either
5. `docs/current/d/C11D_CHALLENGE_V2C_SOURCE_FRAME_RUNTIME_ACCEPTANCE_CHECKPOINT_20261020.md`
6. `docs/current/d/C11D_CHALLENGE_V2C_SOURCE_FRAME_RUNTIME_EVIDENCE_LEDGER_20261020.json`
7. `docs/current/d/C11D_CHALLENGE_VISUAL_PAYLOAD_SOURCE_SEMANTIC_REVIEW_V1_20261020.md`
8. `definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_SOURCE_SEMANTIC_REVIEW_V1.json`
9. `prompts/C11D_D_FINAL_CLOSEOUT_OVERHAND_MASTER_PROMPT_20261020_V8.md`

If a named V2-C or review file is missing, determine current checkout truth; do not claim this overlay was applied unless the operator output proves it. Do not overwrite V6/V7 checkpoints or re-run green V2-C suites without a changed dependency.

## Authoritative V2-C evidence (operator-confirmed)

`PASS_SOURCE_FRAME_ROUTE_ONLY`; Python 28/28; focused CHALLENGE_001 smoke 1/1 and 420 frames; Godot `4.7.1.stable.mono.official.a13da4feb`; selectors 9/9; planner 9/9; independent runtime processes 18/18; source pins 81/81 before/after. Report SHA-256 `35e5985f47055fc11cbc0fcd7317f4d0a4ebe6bfe4d8bb22bdab67b7bcbe56a7`; runner stdout `f90846bfddeb4cccf064b1bf1b4332a36e08173f0e3a9d412c66466d361d95f6`; stderr empty `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Evidence `%TEMP%\C11DVR59d6b3f0`. This proves source-frame/route acceptance only.

## Immediate task

Apply `C11D_CHALLENGE_SOURCE_SEMANTIC_REVIEW_V1_AND_V2C_CLOSEOUT_OVERLAY_20261020.zip` add-only using its guarded block, verify all 81 source pins and run the bundled test:

`C11D_SOURCE_SEMANTIC_REVIEW_TESTS_PASS=34/34`

Stop on first conflict, pin drift or failed test. Do not rerun V2-C runtime. Do not design/apply V2-B until this semantic review is installed and green.

## Source decisions that must remain intact

- Nine proposed binding rows reviewed; `approved_bindings=0`, renderer projection approvals `0`.
- Six `custom_data` selector/field candidates are still candidates only: 003 `target_x`; 005, 006 and 007 `target_position`; 008 `active_selection`; 009 `displayed_count`.
- `CHALLENGE_001` static target field duplicates a mechanic default without being consumed by `KeyMechanic.setup`.
- `CHALLENGE_002` coordinate space remains undeclared; don't infer it.
- `CHALLENGE_003.target_x` is a scalar in `PILOT_0X100`; never invent Y.
- `CHALLENGE_004` V1 harness stays byte-for-byte unchanged.
- `CHALLENGE_005.target_position` is a seeded per-run constant repeated per frame.
- `CHALLENGE_006/007.target_position` is per-frame and distinct from the primary catcher/scanner track.
- 008/009 total 11 s vs phase sum 12 s remains blocked; source-frame-only evidence does not close timing.
- Never serialize all `FrameSnapshot.custom_data`.

After the 34-test source review is accepted, the next work item is a distinct V2-B safe visual-projection runtime harness design. It must prove projection identity/repeat determinism, actual gameplay-seed sensitivity where justified by source, music-seed orthogonality at the request boundary, editorial invariance, full source lineage and negative fail-closed behavior. No payload materializer or renderer-native output yet.

## Governance locks

Preserve `renderer=OFF`, `media_created=false`, `candidate_input_admissible=false`, `seed_domains_complete_for_candidate_input=false`, `automatic_seed_generation=false`, `master_seed=NOT_ADOPTED`, `D4.8=BLOCKED`, `D9.10=PREPARE_ONLY`, `D9.14=BLOCKED`, `D9.16=BLOCKED`, `D9.17=BLOCKED_NO_GO`, `D10=BLOCKED_FOR_PROMOTION`, `baseline_approval=MISSING`, `freeze_eligible=false`, `release_authority=NONE`, `visual_seed_sensitivity=NOT_TESTED`.
