# AGENTS.md — C11-D current authority (2026-10-29 V28)

## Continuation authority

Active Windows checkout: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. Read in this order:

1. `AGENTS.md` and `.continue/rules/CONTINUE.md` for execution discipline.
2. `prompts/C11D_D_FINAL_CLOSEOUT_HANDOVER_MASTER_PROMPT_20261029_V28.md`.
3. `docs/current/d/C11D_FULL_CONTEXT_CONTINUITY_CHECKPOINT_20261029_V28.md`.
4. `docs/current/d/C11D_ENGINEERING_PHASE_LEDGER_20261029_V5.md`.
5. Phase S acceptance review and closeout receipt.
6. Phase S preflight `.md/.json`, schema, and test.
7. Phase R acceptance review/decision packet; Phase Q review/matrix/receipt; Phase P provenance review/runtime verification; older versions remain immutable history.

## Current scoped state

Phase P is accepted only for source/frame provenance. Phase Q is `PASS_READ_ONLY_INVENTORY`. Phase R is accepted for decision preparation only; none of its nine policies has been adopted.

Phase S is `PASS_AUDIT_ONLY_AUTHORITY_EVIDENCE_NOT_FOUND`. The static suite passed 40/40, Python exit 0; stdout SHA-256 `5858edbfbb99f3b294ddc9b7d740246d442cb01806aee2a04c19f4179f743415`; stderr SHA-256 `093372e217a39d80cc806b31c1b1af9671ac951664c1b65ab4445f2f045cea2b`. The result only establishes that no acceptable authority record was found in the specific pinned P/Q/R record set reviewed. Do not claim global absence. Receipt: `docs/current/d/C11D_PHASE_S_AUTHORITY_EVIDENCE_PREFLIGHT_CLOSEOUT_20261029_V1.md`.

**Next action:** `WAIT_FOR_EXPLICIT_AUTHORITY_EVIDENCE`. Do not invent Phase T or adjudicate R-01…R-09 without a separate authority record with exact choice, authority/scope, effective date, rationale, source pins, acceptance tests, approval provenance, and immutable location. Adjudicate only the IDs and scope actually covered by that record. A technical PASS or instruction to continue is not product/contract authority.

## Pin chronology

Phase S preflight checked source pins including the current Phase R-created guidance (`AGENTS.md` SHA-256 `710b3e112e0400e4daac3b8828c89573549f6f59393f6ae5e081e3d482b5ffea`; `.continue/rules/CONTINUE.md` SHA-256 `a5f2dcd3261b64933d85bda79c027d0bb840afda9444e4af6a6f431f01c1d7b4`) and continuity V4/V27. This V28 post-acceptance update changes guidance only after the evidence was verified; it does not invalidate the accepted preflight. Any future gate must declare fresh pins after this update. Do not restore older guidance from snapshots.

## Frozen C11-C and governance locks

C11-C 2.19.12 remains authoritative and immutable until C11-D is separately approved, frozen, and promoted. Live manifest `release/C11C_FREEZE_PACKAGE_MANIFEST.json` must remain SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`, 796318 bytes. Do not copy the manifest from an archive or alter C11-C implementation, canonical seeds, simulation truth, RNG ownership, SimulationResult, frozen geometry, or `winning_frame`.

Hard locks: `renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `approved_renderer_projection_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.

`winning_frame` is the only Challenge temporal anchor; `close_calls` counts episodes. `CHALLENGE_008` and `CHALLENGE_009` declared duration 11 s vs phase sum 12 s remains unresolved (`BLOCKER_NO_CORRECTION_INFERRED`). Never infer a correction or equate `displayed_count` and `target_count`.

## Engineering discipline

Windows PowerShell 5.1; complete pasteable blocks; no `&&`, `Read-Host`, or PS7-only syntax. Apply and test separately. Exact prehashes, add-only records, backups for guarded updates, separate stdout/stderr and real exit codes. Stop at first failure. Do not re-run Phase P/Q/R/S absent changed inputs or an explicit new gate requirement. Never infer binding, rendering, freeze, or release authority from provenance/audit evidence.
