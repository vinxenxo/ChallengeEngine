# C11-D Start Prompt V3 — 2026-10-17

You are continuing ChallengeEngine V01 STATELESS C11-D from the active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`, not reconstructing the repo from a stale snapshot.

Read first:

1. `AGENTS.md`
2. `docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md`
3. `docs/current/d/C11D_FULL_CONTEXT_CONTINUITY_CHECKPOINT_20261017_V3.md`
4. `docs/current/d/C11D_RENDERER_CLOSEOUT_GATE_MAP_20261017_V3.md`
5. `docs/current/d/C11D_SEED_DOMAIN_NEXT_INCREMENT_PLAN_20261017_V2.md`
6. `docs/current/d/C11D_VISUAL_LOOP_SEED_DOMAIN_AUDIT_V2_CHECKPOINT_20261017.md`
7. `docs/current/d/C11D_WORKSTREAM_NON_DUPLICATION_REGISTER_20261017_V3.md`
8. `docs/current/d/C11D_POWERSHELL_EXECUTION_POLICY_20261016.md`
9. `prompts/C11D_D_FINAL_CLOSEOUT_OVERHAND_MASTER_PROMPT_20261017_V3.md`

## Current state

Active-Windows exact-selector Visual Loop V2 payload runtime is PASS for five geometric selectors with 70/70 source pins, 5/5 payload instances, 5/5 deterministic repeats and no renderer inputs. The new explicit seed-domain V2 runner, contract, schemas and 17-case unit test suite are an **additive overlay** that must be applied and verified before running on the active checkout. In the staging snapshot, its 17 unit tests passed and canonical request-chain preflight planned 15/15 variants; its actual Windows Godot seed runtime has NOT yet run.

## Immediate work

1. Apply `C11D_VISUAL_LOOP_SEED_DOMAIN_AUDIT_V2_OVERLAY_20261017_V1.zip` using its sidecar SHA, internal target manifest and C11-C immutable reference. Keep the operation add-only. Verify every staged/installed hash and ensure all target paths were absent before applying. No parent contract or source is replaced.
2. Run `python -B -m unittest tools.c11d.d9.test_d_renderer_visual_loop_seed_domain_audit_v2 -v`; stop unless 17/17 pass.
3. Run `tools/c11d/d9/d_renderer_visual_loop_seed_domain_audit_v2.py` on real Godot 4.7.1 from the active checkout. Capture stdout/stderr, true exit code, exact version, JSON report and hashes. Expected 30 full-chain receipts and 60 probe invocations. Do not mark PASS on synthetic/unit tests.
4. Record results in the versioned checkpoint only after operator runtime evidence exists. If pass, the next population is the canonical Challenge seed domain beyond `CHALLENGE_004`, scoped and source-pinned separately.

## Governance locks

C11-C 2.19.12 and its manifest are immutable (manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`). `renderer=OFF`; `candidate_input_admissible=false`; `media_created=false`; `D4.8=BLOCKED`; `release_authority=NONE`; `D9.10=PREPARE_ONLY`; `D9.17=BLOCKED_NO_GO`; D10 blocked; baseline approval missing; freeze eligibility false. `master_seed=NOT_ADOPTED`; automatic/default seed generation disabled; `seed_domains_complete_for_candidate_input=false`.

Do not reimplement accepted binders, write payload/media files, add `c11d-control`, mutate C11-C or promote any gate. Follow dependency order and use small additive ZIP overlays with exact source pins and separately executed tests/runtime.
