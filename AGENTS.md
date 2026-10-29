# AGENTS.md — C11-D current authority (2026-10-29 V26)

## Continuation authority

Active Windows checkout: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. Read in this order:

1. `AGENTS.md` and `.continue/rules/CONTINUE.md` for execution discipline.
2. `prompts/C11D_D_FINAL_CLOSEOUT_HANDOVER_MASTER_PROMPT_20261029_V26.md`.
3. `docs/current/d/C11D_FULL_CONTEXT_CONTINUITY_CHECKPOINT_20261029_V26.md`.
4. `docs/current/d/C11D_ENGINEERING_PHASE_LEDGER_20261029_V3.md`.
5. `docs/current/d/C11D_PHASE_P_SOURCE_FRAME_PROVENANCE_ACCEPTANCE_REVIEW_20261029_V1.md`.
6. `docs/current/d/C11D_PHASE_P_RUNTIME_EVIDENCE_VERIFICATION_20261029_9bb3b12b1f9b4658b5892679672bbf1a.md` and the immutable runtime-attempt records.
7. Phase P contract/schema/auditor/runner/runbook and Phase O crosswalk evidence; prior V25/V24 docs and ledger V2/V1 are historical.

## Current scoped state

Phase O remains accepted as a read-only crosswalk. Phase P is accepted only for six-selector source/frame provenance: source pins 95/95, six selectors, six canonical planner invocations, twelve isolated Godot processes, repeat hashes PASS and zero relation mismatches. Runtime report SHA-256 `9686240a0e2caa46f05cea4ca2c8fcaaa1499d006ac6ac75d128137693fc2ef7`; runner SHA-256 `e472af0dd7675e85eb2a030eaf06604a78ef409405d8f9a44fa1892d41016a3d`; decision in `C11D_PHASE_P_SOURCE_FRAME_PROVENANCE_ACCEPTANCE_REVIEW_20261029_V1.md`.

**Next action:** Phase Q review-only candidate/semantic decision matrix. Do not rerun Phase P or accepted Phase O/M/N matrices absent changed source pins and a specific gate requirement. No bindings, production callsites, renderer, payload or media are authorized by Phase P evidence.

## Pin chronology

At Phase P runtime, `AGENTS.md` SHA was `67c5f237035c121f27733c24f3b2fe2da2bb104eaaa5f95e4c7a88b573071599` (4851 bytes) and `.continue/rules/CONTINUE.md` SHA was `8ee4f47588acbc981bd11400ad4186a598e052e279b8f2e2cc0bd87cb6b21c71` (3599 bytes); these exact versions were part of the runtime source-pin reconciliation. This file and CONTINUE are now updated after the report to point to the next gate. Do not rewrite the historical report or rerun Phase P merely due to this post-acceptance documentation update. Any new gate must compute/declare fresh source pins after this update. Keep old V25/V24 instructions historical; never restore from the old snapshot.

## Frozen C11-C and governance locks

C11-C 2.19.12 remains authoritative and immutable until C11-D is separately approved, frozen, and promoted. Live manifest `release/C11C_FREEZE_PACKAGE_MANIFEST.json` must remain SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`, 796318 bytes. Do not copy the manifest from an archive or alter C11-C implementation, canonical seeds, simulation truth, RNG ownership, SimulationResult, frozen geometry, or `winning_frame`.

`winning_frame` is the only Challenge temporal anchor; `close_calls` counts episodes. `CHALLENGE_008` and `CHALLENGE_009` declared duration 11s versus phase sum 12s remains unresolved. `target_x` remains a scalar.

Hard locks: `renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `approved_renderer_projection_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.

## Engineering discipline

Windows PowerShell 5.1; complete pasteable blocks; no `&&`, `Read-Host`, or PS7-only syntax. Apply and test separately. Use exact prehashes and add-only new records; keep backups for updates. Use `Start-Process -Wait -PassThru`, separate stdout/stderr, and verify the actual process exit code plus report contents. Never print PASS after a thrown error. Preserve failure records. Never infer binding/render/release approval from provenance evidence.
