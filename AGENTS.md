# AGENTS.md — C11-D current authority (2026-10-26 V24)

## Current continuation authority

Active Windows checkout: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. Read the current dated authority files in this order:

1. `docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md`
2. `docs/current/d/C11D_FULL_CONTEXT_CONTINUITY_CHECKPOINT_20261026_V24.md`
3. `docs/current/d/C11D_SOURCE_SNAPSHOT_RECONCILIATION_REPORT_20261026_V1.md`
4. `docs/current/d/C11D_V2B_ALLOWLISTED_COORDINATE_SOURCE_COMPOSITION_RUNTIME_REVIEW_20261026_V1.md`
5. `prompts/C11D_D_FINAL_CLOSEOUT_HANDOVER_MASTER_PROMPT_20261026_V24.md`
6. `prompts/C11D_D_FINAL_CLOSEOUT_START_PROMPT_20261026_V24.md`
7. The older dated checkpoints, gate map V5 and non-duplication register V6 for predecessor evidence and broader dependencies. Older state/next-step statements are historical when contradicted by the V24 current checkpoint.

## Current scoped evidence

The Windows operator transcript reports runtime-static V1 `113/113`, runtime-static V2 `115/115`, source-composition static `132/132` and Godot Mono runtime PASS for CHALLENGE_003/005/006/007 with 1,680/1,680 source frames and 1,680/1,680 marker frames. Runtime stdout SHA-256 `b5e1465894a9d5ad5a26715f10459bf578809d4a3fadce7fc030b4964aa2c3bb`; stderr empty SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

A new source-composition evidence V2 record plus strict schema and standard-library validator were added for review. Important provenance discrepancy: the embedded C11-C manifest in the uploaded ZIP is not byte-identical to the canonical frozen manifest; the active checkout must be checked before applying or validating. The record starts as `CAPTURED_OPERATOR_RUNTIME_PASS_PENDING_FORMAL_REVIEW`; validation and a separate operator review remain required. Historical V1 evidence is immutable and binds older source hashes.

## Immutable authority and hard locks

Frozen C11-C 2.19.12 remains authoritative until C11-D passes all gates and is separately approved/frozen/promoted. `release/C11C_FREEZE_PACKAGE_MANIFEST.json` SHA-256 must remain `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Do not modify C11-C code, frozen seed V1, simulation truth, RNG ownership, `SimulationResult`, frozen geometry or `winning_frame`; `winning_frame` is the only temporal anchor, `close_calls` is episode count only.

`renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `approved_renderer_projection_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.

## Immediate next work

Run the current source-composition evidence validator against the exact `%TEMP%` runtime logs. On failure, stop and diagnose; do not make the test permissive. On PASS, record a separate operator evidence review before any integration proposal. Do not create production callsites, renderer inputs or media in this gate. The 008/009 11-second declared duration versus 12-second phase-sum conflict remains blocked.

## Engineering rules

- PowerShell 5.1; complete single pasteable blocks inside `& { ... }`; no `&&`, no `Read-Host`, no PowerShell 7-only syntax.
- Verify ZIP, source, contract, manifest and receipt SHA-256 values. New dated deliverables are add-only.
- Stable pointer replacements require exact previous hashes, backups and post-apply checks. Do not overwrite or reclassify historical failures/acceptances.
- Keep apply and test as separate blocks. Use `Start-Process -Wait -PassThru`, capture stdout/stderr separately, and check actual process exit code.
- Stop on first mismatch. Never emit a PASS after an error.
- Do not invent mappings, read all `FrameSnapshot.custom_data`, duplicate canonical planner/adapters, introduce `c11d-control`, or infer authorization from a test pass.
